"""
Outputs: Description

sim.substitutions.tree: Rescaled tree from phastSim, branch lengths now represent substitutions per site.
datefile.txt: Space seperated table of sample ID's and sampling time (real number).
divergence_distribution.png: Histogram of the divergence (genetic distance between root and tip) for all tips.
"""
from Bio import Phylo
import pandas as pd
import numpy as np
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(
    prog='SuperSimPyPostProcess',
    description="Post processing script for SuperSimPy.")
parser.add_argument('-d', '--datapath')
parser.add_argument('-s', '--sites', default=31101)

args = vars(parser.parse_args())
sim_data_path = args['datapath'] if args['datapath'][-1] == '/' else args['datapath'] + '/'
genome_length = args['sites']

mut_tree = Phylo.read(sim_data_path + 'sim.tree', 'newick', rooted=True)


# Rescale tree
def subs_per_site(mutation_comment):
    return (mutation_comment.count(',') + 1) / genome_length


def subs_per_site_tree(root):
    stack = [root.clade]
    tip_ids = []
    while stack:
        node = stack.pop()
        node.branch_length = subs_per_site(node.comment)
        if not node.is_terminal():
            for clade in node.clades:
                stack.append(clade)
        if node.is_terminal():
            tip_ids.append(node.name)

    return root, np.array(tip_ids)


def root_to_tip(root):
    stack = [(root.clade, 0)]  # Stack to hold nodes and their current distances
    distances = []
    tip_ids = []
    while stack:
        node, current_distance = stack.pop()
        # Calculate the new distance
        if node.branch_length:
            node.branch_length = subs_per_site(node.comment)
            distance = current_distance + node.branch_length
        else:
            distance = 0

        # If the node is terminal, add the distance to the result list
        if node.is_terminal():
            distances.append(31101 * distance)
            tip_ids.append(node.name)
        else:
            # Add all child nodes to the stack with the updated distance
            for clade in node.clades:
                stack.append((clade, distance))

    return root, np.array(tip_ids), np.array(distances)


rescaled_tree, sample_ids, genetic_divergences = root_to_tip(mut_tree)
Phylo.write(rescaled_tree, sim_data_path + 'sim.substitutions.tree', 'newick')
# Write date-file
metadata = pd.read_csv(sim_data_path + 'newick_output_metadata.tsv', sep='\t',
                       dtype={'strain': str, 'location': str, 'time': float})
sample_times = metadata[metadata['strain'].isin(sample_ids)][['strain', 'time']]
sample_times.to_csv(sim_data_path + 'datefile.txt', index=False, sep=' ', header=None)

# Write distribution image to file
plt.hist(genetic_divergences, density=True)
plt.title('Root to Tip Genetic Divergence Distribution')
plt.savefig(sim_data_path + 'divergence_distribution.png')
