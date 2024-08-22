# Population processing

This folder contains parts of the pipeline relevant to processing population data.

## Pre-pipeline scripts

These scripts do not need to be run as they compile into static data that is used in the pipeline.

### 1. `census_cleanup.ipynb`

Cleans up census data to work with migration matrix (so country names are consistent across files).

### 2. `migration_matrix.ipynb`

Creates a migration probability matrix between 209 countries, using a uniform stay-at-home probability and effective
distance data.

### 3. `sampling_multipliers.ipynb`

**TODO:** re-input into VGsim.

Calculates sampling rates for each country based off COVID case data and sampling data.

## Pipeline script

These scripts are run during the pipeline

### 1. `relabel_populations.ipynb`
VGsim labels countries in order using integer IDs, this script relabels these IDs with human-readable country names.

## Input data
#### World population by country 
Count of each countries' population. 
Filepath: `original_data/population2013.csv`

Source: https://data-explorer.oecd.org/vis?tenant=archive&df[ds]=DisseminateArchiveDMZ&df[id]=DF_EDU_DEM&df[ag]=OECD&dq=..&pd=2013%2C2013&to[TIME_PERIOD]=false

#### Effective distance matrix
Matrix of effective distance between countries, as defined in https://www.science.org/doi/10.1126/science.1245200.

Filepath: `original_data/effective.distance.matrix.country.csv`
