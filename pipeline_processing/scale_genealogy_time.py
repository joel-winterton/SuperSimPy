"""
Outputs: Rescaled genealogy tree.
Convert VGSim timescale to days.
The simulation runs with its own unit of time,
 using SIR parameters beta = 2, alpha=1 which indicates a sensible timescale is 1 time unit = 10 days.
"""
from Bio import Phylo
import argparse
import datetime
import pandas as pd

parser = argparse.ArgumentParser(
    prog='SuperSimPyTimeScaler',
    description="Time scaling script for VGSim output.")
parser.add_argument('-f', '--folder', required=True)
parser.add_argument('-y', '--year', default=2020)
parser.add_argument('-m', '--month', default=1)
parser.add_argument('-d', '--day', default=1)
parser.add_argument('-u', '--unit', default=10)
args = vars(parser.parse_args())

sim_data_path = args['folder'] if args['folder'][-1] == '/' else args['folder'] + '/'
unit_of_time_in_days = args['unit']
start_date = datetime.date(args['year'], args['month'], args['day'])

print(
    f"Rescaling tree from {sim_data_path}newick_output_tree.nwk using 1 unit of time =  {str(unit_of_time_in_days)} days.")

tree = Phylo.read(sim_data_path + 'newick_output_tree.nwk', 'newick')


def rescale_tree(root):
    stack = [root.clade]
    while stack:
        node = stack.pop()
        node.branch_length = node.branch_length * 10 if node.branch_length else None
        if not node.is_terminal():
            for clade in node.clades:
                stack.append(clade)

    return root


metadata = pd.read_csv(sim_data_path + 'newick_output_metadata.tsv', sep='\t',
                       dtype={'strain': str, 'location': str, 'time': float})
metadata['time'] = unit_of_time_in_days * metadata['time']


def days_plus_date(days: float):
    return start_date + datetime.timedelta(days=days)


print(f"Writing date time-scaled metadata to {sim_data_path + 'dated_metadata.csv'}.")
metadata['time'] = metadata['time'].apply(lambda x: days_plus_date(x))
metadata.rename({'time': 'date'})
metadata.to_csv(sim_data_path + 'dated_metadata.csv', index=False, sep=',')
print(f"Writing time-scaled genealogy to {sim_data_path + 'genealogy.nwk'}")
Phylo.write(trees=rescale_tree(tree), file=sim_data_path + 'genealogy.nwk', format='newick')
