# SuperDimPy
Scripts used to create simulation of 5million+ genome pandemic that can be used to test phylogenetic methods on large scale epidemics.
## Current pipeline: 
**@todo:** both VGsim and Phastsim have been modified to interface properly with this simulator, so a fork of both needs to be included here instead of the original repositories which will break the pipeline.

**@todo:** pandemic-simulator is not needed since it just creates several workflows, and we use one of them, consider creating our own snakemake workflow.
Prerequisites: 
Both these prerequisites have been modified to work with the pipeline, so you'll need to use my forked version: 
1. VGsim https://github.com/joely-w/VGsim, and the path to `VGsim_cmd.py` needs to be known.
2. PhastSim https://github.com/NicolaDM/phastSim, and the path to the directory `bin/phastSim` contained within the installation of phastSim needs to be known.
3. pandemic-simulator https://github.com/jmcbroome/pandemic-simulator this ties together phastSim and vgSim into a single pipeline

Pipeline:

Using the pandemic-simulator workflow, data must be created (in this repository data for a simulation using 209 countries is generated),
this created data must be placed in the pandemic-simulator workflow and referenced in the `config.yml` in place of the basic 2 population configuration.

The snakemake workflow can then be run.
https://github.com/jmcbroome/pandemic-simulator/