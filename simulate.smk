configfile: 'config.yaml'
rule phastSim:
    input:
        "data/newick_output_tree.nwk"
    output:
        "data/sim.mat.pb"
    shell:
        "python3 {config[executables][phastexec]} --output data/sim --reference {config[phastsim-params][ref]} --scale {config[phastsim-params][scale]} --createMAT --treeFile {input} --eteFormat {config[phastsim-params][ete3_mode]} --mutationRates {config[phastsim-params][mr_model]} {config[phastsim-params][mut_rates]} --createNewick"

rule VGsim:
    output:
        "data/newick_output_tree.nwk",
        "data/newick_output_sample_population.tsv",
        f"data/newick_output_metadata.csv"
    shell:
        "python3 {config[executables][vgexec]} -rt {config[vgsim-params][rt]} -it {config[vgsim-params][it]} -s {config[vgsim-params][samples]} -pm {config[vgsim-params][ppmg]}.pp {config[vgsim-params][ppmg]}.mg -su {config[vgsim-params][sust]}.su -st {config[vgsim-params][sust]}.st --createNewick data/newick_output"

