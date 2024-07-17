# SuperDimPy
Workflow for simulation of 5million+ genome pandemic that can be used to test phylogenetic methods on large scale epidemics.
The current setup simulates a pandemic between 209 countries, with country codes listed in `population_data/output/census_2013.csv`.
Data for realistic migration and sampling dynamics are obtained through air travel data (2013) and COVID sampling data (2024).
## Setup
### Installation
This simulation requires the following libraries. As noted in VGSim, it's recommended that all of these installations are done within a conda environment.
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
## Pipeline
Snakemake is used to run the workflow, which runs as VGSim -> phastSim -> taxonium.

To run the workflow:

```snakemake -s simulate.smk -c1```
