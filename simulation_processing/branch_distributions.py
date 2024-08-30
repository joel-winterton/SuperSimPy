"""
Plots the distribution of the branch lengths of an input newick tree.
"""
import argparse
from Bio import Phylo
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(
    prog='SuperSimPyPostProcess',
    description="Post processing script for SuperSimPy.")
parser.add_argument('-t', '--treepath', required=True)
args = vars(parser.parse_args())
tree = Phylo.read(args['treepath'], 'newick', rooted=True)


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
    stack = [(root, 0)]  # Stack to hold nodes and their current distances
    distances = []

    while stack:
        node, current_distance = stack.pop()

        # Calculate the new distance
        if node.branch_length:
            distance = current_distance + node.branch_length
        else:
            distance = 0

        # If the node is terminal, add the distance to the result list
        if node.is_terminal():
            distances.append(31101 * distance)
        else:
            # Add all child nodes to the stack with the updated distance
            for clade in node.clades:
                stack.append((clade, distance))

    return distances



plt.hist(store_branch_lengths(tree), density=True)
plt.show()
plt.hist(root_to_tip(tree.clade), density=True)
plt.show()
