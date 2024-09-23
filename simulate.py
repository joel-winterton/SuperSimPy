"""
This is not the main simulation!
This is a test to see if GemLib simulations are more efficien than VGSim.
"""
import numpy as np
import tensorflow as tf
import gemlib
import pandas as pd

dtype = np.float64
gld = gemlib.distributions

# load data
country_ids = pd.read_csv('./parameters/manypop_country_ids.csv')
country_ids.sort_values(by='location', inplace=True)
migration_probabilities = pd.read_csv(
    './parameters/manypop.mg', skiprows=1, sep=' ',
    header=None)
migration_probabilities.set_index(country_ids['location'], inplace=True)
migration_probabilities.columns = country_ids['location']
# format data for initial state
state_data = list(country_ids['population'].apply(lambda x: [x, 0, 0]).values)
state_data[0] = [state_data[0][0] - 1, 1, state_data[0][2]]

# create a probability matrix from migration data
probability_matrix = migration_probabilities.to_numpy()
np.fill_diagonal(probability_matrix, 0.00)


def make_transition_fn(beta, psi, alpha, omega, prob_matrix, pop_counts):
    # easier to pass population counts here than sum over state each time
    def transition_function(t, state):
        I = state[:, 1]
        M = tf.math.divide(I, pop_counts)
        between = psi * tf.tensordot(prob_matrix.transpose(), M, 1)
        within = beta * I
        si_rate = between + within
        ir_rate = tf.broadcast_to(alpha, si_rate.shape)
        rs_rate = tf.broadcast_to(omega, si_rate.shape)
        return si_rate, ir_rate, rs_rate

    return transition_function


@tf.function(jit_compile=True)
def large_model():
    """
    Large scale model with 208 countries.
    """

    # Params
    initial_state = np.array(state_data, dtype=dtype)

    # Epidemic model
    incidence_matrix = np.array(
        [  # SI  IR  RS
            [-1, 0, 1],  # S
            [1, -1, 0],  # I
            [0, 1, -1],  # R
        ],
        dtype=dtype
    )

    pop_counts = np.sum(initial_state, axis=1)

    params = dict(beta=2, psi=2.5, alpha=0.5, omega=0.5, prob_matrix=np.array(probability_matrix, dtype=dtype),
                  pop_counts=pop_counts)
    return gld.ContinuousTimeStateTransitionModel(
        transition_rate_fn=make_transition_fn(**params),
        incidence_matrix=incidence_matrix,
        initial_state=initial_state,
        num_steps=2000,
        name="sirs"
    ).sample()


events = large_model()
sim_data = pd.DataFrame(data=dict(time=events.time, deme=events.unit, event_type=events.transition))
sim_data.to_csv('./gemlib_output.csv')
