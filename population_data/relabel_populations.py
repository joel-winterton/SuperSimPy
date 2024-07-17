"""
Runs from command line.
Populations in metadata are integer ID's. This replaces the integer ID's with full country names.
"""
import pandas as pd
import argparse

parser = argparse.ArgumentParser(
    prog='RelabelPopulations',
    description="Populations in metadata are integer ID's. This replaces the integer ID's with full country names.")
parser.add_argument('-m', '--metadata')
parser.add_argument('-c', '--census')
parser.add_argument('-o', '--output')

args = vars(parser.parse_args())

metadata = pd.read_csv(args['metadata'], sep='\t')
census = pd.read_csv(args['census'])
census['location'] = census.index
result = pd.merge(metadata, census, on='location', how='left')
result = result[['strain', 'fullname', 'time']]
result.rename(columns={'fullname': 'location'}, inplace=True)
result.to_csv(args['output'] + '.tsv', header=True, index=None, mode="w", sep='\t')
