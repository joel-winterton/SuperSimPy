## Data estimation
These scripts create realistic data that can be inputted into the simulations.
The end result of these scripts is data describing migration between 203 countries based off airline flights in 2013, 
with the data being in a compatible format to be used in the simulation pipeline.

### Input data
#### World population by country 
Count of each countries' population. 
Filepath: `original_data/population2013.csv`

Source: https://data-explorer.oecd.org/vis?tenant=archive&df[ds]=DisseminateArchiveDMZ&df[id]=DF_EDU_DEM&df[ag]=OECD&dq=..&pd=2013%2C2013&to[TIME_PERIOD]=false

#### Effective distance matrix
Matrix of effective distance between countries, as defined in https://www.science.org/doi/10.1126/science.1245200.

Filepath: `original_data/effective.distance.matrix.country.csv`

### Output data
#### Cleaned census file
Filepath: `migration_data/output/census_2013.csv`
#### Alpha 2 codes of countries used in data
Filepath: `migration_data/output/country_codes.csv`
#### Migration probability matrix
In format that will be compatible with the VGsim migration model.
Order of countries is the same as in `migration_data/output/country_codes.csv`.

Filepath: `migration_data/output/country_migration.mg`

### Scripts 
#### Census cleanup 
Creates a census in the format used in the effective distance data.
Specifically makes sure all country codes are the same format as in effective distance (alpha2).

Filepath: `migration_data/census_cleanup.ipynb`

#### Probability matrix calculator 
Calculates migration probability matrix from cleaned census data and effective distance matrix, along with some parameters used in 
the supplementary materials of https://www.science.org/doi/10.1126/science.1245200#supplementary-materials.
If a different data was used, parameters $$\Omega, \Phi$$ in this script will need to be recalculated from data. 

Filepath: `migration_data/migration_matrix.ipynb`