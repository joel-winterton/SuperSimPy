# -*- coding: utf-8 -*-
"""
International SIRS.ipynb

Colab file is located at
    https://colab.research.google.com/drive/1cxD6v97ea_l71GGtMsmhQZNToFwU4EDH
"""


# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp
import gemlib
import pandas as pd
import argparse
dtype=np.float32
gld = gemlib.distributions
tfd = tfp.distributions

parser = argparse.ArgumentParser(
    prog='Gemlib simulation',
    description="Gemlib simulation test")

parser.add_argument('-o', '--output', default='./')
parser.add_argument('-i', '--iterations', default=250)
args = vars(parser.parse_args())
iterations = int(args['iterations'])
output = args['output'] if args['output'][-1] == '/' else args['output'] + '/'

# %matplotlib inline
def plot_timeseries(
        times, states, plot_height=4, labels=["S", "I", "R"], alpha=1.0, population_lim=10
):
    num_plots = states.shape[-2] if states.shape[-2]<=population_lim else population_lim
    fig, ax = plt.subplots(
        1, num_plots, figsize=(num_plots*plot_height*1.5, plot_height)
    )
    for i in range(num_plots):
        for s, label in enumerate(labels):
            state = np.transpose(states[..., i, s])
            ax[i].plot(
                np.transpose(times),
                state,
                label=label,
                color=f"C{s}",
                alpha=alpha
            )
        ax[i].set_title("Subpopulation {}".format(i))
        ax[i].set_xlabel("Time")
        ax[i].set_ylabel("Individuals")
        leg_lines = [Line2D([0], [0], color=f"C{i}") for i in range(len(labels))]
        ax[i].legend(leg_lines, labels)

    return fig, ax

"""# Transition function"""

def make_transition_fn(beta, psi, alpha, omega, prob_matrix, pop_counts):
  # easier to pass population counts here than sum over state each time
  def transition_function(t, state):
    I = state[:,1]
    M = tf.math.divide(I, pop_counts)
    between = psi*tf.tensordot(prob_matrix.transpose(), M, 1)
    within = beta*I
    si_rate = between+within
    ir_rate = tf.broadcast_to(alpha, si_rate.shape)
    rs_rate = tf.broadcast_to(omega, si_rate.shape)
    return si_rate, ir_rate, rs_rate
  return transition_function

"""# Large model
208 countries.

### Convert data to model format
"""

# load data
country_ids = pd.read_csv('https://raw.githubusercontent.com/joel-winterton/SuperSimPy/main/parameters/manypop_country_ids.csv')
country_ids.sort_values(by='location', inplace=True)
migration_probabilities = pd.read_csv('https://raw.githubusercontent.com/joel-winterton/SuperSimPy/main/parameters/manypop.mg', skiprows=1, sep=' ', header=None)
migration_probabilities.set_index(country_ids['location'], inplace=True)
migration_probabilities.columns = country_ids['location']
# format data for initial state
state_data = list(country_ids['population'].apply(lambda x: [x,0,0]).values)
state_data[0] = [state_data[0][0]-1, 1, state_data[0][2]]

# create a probability matrix from migration data
probability_matrix = migration_probabilities.to_numpy()
np.fill_diagonal(probability_matrix, 0.00)

np.max(probability_matrix)

"""### Create large model"""

@tf.function(jit_compile=True)
def large_model():
  """
  Large scale model with 208 countries.
  """

  # Params
  initial_state = np.array(state_data,dtype=dtype)

  # Epidemic model
  incidence_matrix = np.array(
      [ #  SI  IR  RS
          [-1,   0,  1],  # S
          [ 1,  -1,  0],  # I
          [ 0,   1, -1],  # R
      ],
      dtype=dtype
  )

  pop_counts = np.sum(initial_state, axis=1)

  params = dict(beta = 2, psi = 2.5,alpha = 0.5,omega = 0.5,prob_matrix = np.array(probability_matrix, dtype=dtype), pop_counts=pop_counts)
  return gld.ContinuousTimeStateTransitionModel(
      transition_rate_fn=make_transition_fn(**params),
      incidence_matrix=incidence_matrix,
      initial_state=initial_state,
      num_steps=iterations,
      name="sirs"
  ).sample()

events = large_model()

"""### Save to file"""

sim_data = pd.DataFrame(data=dict(time= events.time, deme=events.unit, event_type=events.transition))
sim_data.to_csv(f'{output}gemlib_output.csv')