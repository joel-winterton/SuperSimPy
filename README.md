# SuperSimPy
Workflow for simulation of 5million+ genome pandemic that can be used to test phylogenetic methods on large scale epidemics.
The current setup simulates a pandemic between 209 countries, with country codes listed in `population_data/output/census_2013.csv`.
Data for realistic migration and sampling dynamics are obtained through air travel data (2013) and COVID sampling data (2024).
### Small example output in Taxonium
![image](https://github.com/user-attachments/assets/a7cc77d0-07ee-446c-a546-9968d3df16b8)



## Setup
Clone the project and navigate inside: 

`git clone https://github.com/joely-w/SuperSimPy.git`

`cd SuperSimPy`

Create and activate a conda environment
```shell
conda create -n simulation_test
conda activate simulation_test
```
Install Python, a C++/C compiler and Snakemake (a workflow management tool):
```shell
conda install python=3.9
conda install -c conda-forge gxx
conda install bioconda::snakemake
```
Then install python requirements and go make a cup of tea ☕: 
```shell
python3 -m pip install -r requirements.txt
```
## Running simulation
You can then run the simulation using the snakemake workflow:
```shell 
snakemake -s simulate.smk -c1 -F
```
### Migration data
The migration data is pre-generated in this repository, but should you want to create different data,
the process of generating this data is done in the Jupyter notebook files in `/population_data`. 

An important element you may want to change is the `in_country_probability` variable in the migration matrix script (just re-running this script will re-populate the data with changes).
This variable controls the uniform probability that an individual stays in their country per-unit time, so a lower value will cause more migration. 

The notebooks collate several sources together and so work in the order of `census_cleanup -> migration_matrix -> sampling_multipliers`.
This directory also contains a script to relabel locations from their integer ID's to readable location names.

### Changing number of samples 
You can change the number of samples in a simulation through the `config.yml` file, through the `samples` property of the 
`vgsim-params` object. If you want lots of samples, you'll also need to increase the number if iterations so that the simulation does not stop before the number of samples have been achieved (using `it` in the same object).
## Result 
The result of this pipeline is all tied into one file `data/results.jsonl.gz` which is an annotated tree which contains 
the scaled time, along with the location of each sample, and each internal node. This can be visualised in Taxonium: 
https://taxonium.org/

## Development setup
Unless you want to develop the libraries used locally, ignore this. 
To develop locally, you'll need the following dependencies install:
1. VGsim https://github.com/joely-w/VGsim [Note: This is a modified VGSim, normal VGSim will not work!]
2. PhastSim https://github.com/NicolaDM/phastSim
3. Snakemake https://snakemake.readthedocs.io/en/stable/getting_started/installation.html
4. Taxonium `pip install taxoniumtools`
### Configuration
Once everything is installed you'll need to point snakemake towards the correct executables, by editing the fields in the `executables` field of `config.yaml`.
#### phastSim
Change the value of `phastexec` to the absolute path of `bin/phastSim` contained within the installation of phastSim. 
#### VGsim
Change the value of `vgexec` to the absolute path of `VGsim_cmd.py` (located within the cloned repository of VGsim, but once VGsim has been installed `VGsim_cmd.py` can be moved anywhere).
### Pipeline
Snakemake is used to run the workflow, which runs as VGSim -> phastSim -> taxonium.

To run the workflow:
```snakemake -s simulate.smk -c1```
To force the workflow to start from scratch: 
```snakemake -s simulate.smk -c1 -F```
