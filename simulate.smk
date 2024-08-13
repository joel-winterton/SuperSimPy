configfile: 'config.yaml'

rule all:
    input:
        expand("{output_dir}/result.jsonl.gz",output_dir=config['output_directory']),
        expand("{output_dir}/sim.substitutions.tree",output_dir=config['output_directory']),
        expand("{output_dir}/datefile.txt",output_dir=config['output_directory']),
        expand("{output_dir}/sim.mat.pb",output_dir=config['output_directory']),
        expand("{output_dir}/sim.tree",output_dir=config['output_directory']),
        expand("{output_dir}/newick_output_tree.nwk",output_dir=config['output_directory']),
        expand("{output_dir}/newick_output_sample_population.tsv",output_dir=config['output_directory']),
        expand("{output_dir}/newick_output_metadata.tsv",output_dir=config['output_directory']),

rule VGsim:
    input:
        expand("{param_dir}.{extension}",param_dir=config['vgsim-params']['ppmg'],extension=['pp', 'mg'])
    output:
        newick_tree=expand("{output_dir}/newick_output_tree.nwk",output_dir=config['output_directory']),
        locations=expand("{output_dir}/newick_output_sample_population.tsv",output_dir=config['output_directory']),
        metadata=expand("{output_dir}/newick_output_metadata.tsv",output_dir=config['output_directory']),
    shell:
        "python3 ./bin/VGsim_cmd.py -it {config[vg_iterations]} -s {config[vg_samples]} -pm {config[vgsim-params][ppmg]}.pp {config[vgsim-params][ppmg]}.mg --createNewick {config[output_directory]}/newick_output --writeMigrations {config[output_directory]}/migrations"

rule timeScale:
    input:
        rules.VGsim.output.newick_tree,
        rules.VGsim.output.metadata
    output:
        genealogy=expand("{output_dir}/genealogy.nwk",output_dir=config['output_directory']),
        dated_metadata=expand("{output_dir}/full_metadata.csv",output_dir=config['output_directory']),
    shell:
        "python3 ./simulation_processing/time_scaler.py --folder={config[output_directory]}"

rule relabelCountries:
    input:
        rules.timeScale.output.dated_metadata,
        "population_data/output/census_2013.csv"
    output:
        complete_metadata=expand("{output_dir}/labelled_metadata.tsv",output_dir=config['output_directory'])
    shell:
        "python3 population_data/relabel_populations.py --metadata {config[output_directory]}/full_metadata.csv --dictionary population_data/output/manypop_country_ids.csv --output {config[output_directory]}/labelled_metadata"

rule phastSim:
    input:
        rules.timeScale.output.genealogy,
    output:
        sim_pb=expand("{output_dir}/sim.mat.pb",output_dir=config['output_directory']),
        sim_tree=expand("{output_dir}/sim.tree",output_dir=config['output_directory']),
    shell:
        "phastSim --output sim --outpath {config[output_directory]}/ --reference {config[phastsim-params][ref]} --scale {config[phastsim-params][scale]} --createMAT --treeFile {input} --eteFormat {config[phastsim-params][ete3_mode]} --mutationRates {config[phastsim-params][mr_model]} {config[phastsim-params][mut_rates]} --createNewick --createFasta"

rule postProcess:
    input:
        rules.phastSim.output.sim_tree,
        rules.relabelCountries.output.complete_metadata
    output:
        substitution_tree=expand("{output_dir}/sim.substitutions.tree",output_dir=config['output_directory']),
        datefile=expand("{output_dir}/datefile.txt",output_dir=config['output_directory']),
    shell:
        "python3 ./simulation_processing/post_process.py --datapath {config[output_directory]}"

rule annotateTree:
    input:
        rules.phastSim.output.sim_pb,
        rules.relabelCountries.output.complete_metadata,
    output:
        annotated_tree=expand("{output_dir}/result.jsonl.gz",output_dir=config['output_directory'])
    shell:
        "usher_to_taxonium --input {config[output_directory]}/sim.mat.pb --output {config[output_directory]}/result.jsonl.gz --metadata {config[output_directory]}/labelled_metadata.tsv --columns location,time"
