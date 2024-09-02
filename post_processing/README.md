# Post-processing
After the pipeline has complete, the scripts in here are used to create any visualisations or summary statistics that are wanted from the simulation.
All *scripts* in this folder are accessible by the command line, and accept as an argument `-f, --folder` which is the absolute path to the output of the simulation.
The Jupyter notebook is not run by default, so you'll need to open it and point it towards your simulated data to visualise migrations, this is because the plotting library doesn't work 'offline'.