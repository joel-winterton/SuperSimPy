"""
Plots the distribution of the branch lengths of an input newick tree.
"""
import matplotlib.pyplot as plt
from Bio import Phylo
import argparse

parser = argparse.ArgumentParser(
    prog='SuperSimPyVisualiser',
    description="Branch distribution visualisation script for SuperSimPy")

parser.add_argument('-f', '--folder', required=True)
args = vars(parser.parse_args())

sim_data_path = args['folder'] if args['folder'][-1] == '/' else args['folder'] + '/'
trees = [dict(path='sim.substitutions.tree', name='substitutions per site'),
         dict(path='sim.tree', name='time between nodes')]


def store_branch_lengths(root):
    stack = [root.clade]
    branch_lengths = []
    while stack:
        node = stack.pop()
        if node.branch_length:
            branch_lengths.append(node.branch_length)
        if not node.is_terminal():
            for clade in node.clades:
                stack.append(clade)
    return branch_lengths


def root_to_tip(root):
    stack = [(root.clade, 0)]
    distances = []
    while stack:
        node, current_distance = stack.pop()
        if node.branch_length:
            distance = current_distance + node.branch_length
        else:
            distance = 0
        if node.is_terminal():
            distances.append(31101 * distance)
        else:
            for clade in node.clades:
                stack.append((clade, distance))
    return distances


for obj in trees:
    tree = Phylo.read(sim_data_path + obj['path'], 'newick', rooted=True)
    print(f"Loaded newick tree from {sim_data_path + obj['path']}")
    branch_lengths = store_branch_lengths(tree)
    print(f"Branch lengths calculated")
    rtt_lengths = root_to_tip(tree)
    print(f"RTT lengths calculated")

    fig = plt.figure()
    fig.suptitle(f"Length distributions for {obj['name']}.")
    axis1 = fig.add_subplot(211)
    axis1.set_title('Isolated branch lengths')
    axis1.set_xlim([0, 200])
    axis2 = fig.add_subplot(212)
    axis2.set_title('Root to tip lengths')
    fig.subplots_adjust(hspace=0.5)

    axis1.hist(branch_lengths, density=True, bins=50)

    axis2.hist(rtt_lengths, density=True, bins=50)
    fig.savefig(f"{sim_data_path}/{obj['path']} distributions.png")
