configfile: 'config.yaml'
rule all:
    input:
        expand("{output_dir}/result.jsonl.gz", output_dir=config['output_directory']),
        expand("{output_dir}/sim.substitutions.tree",output_dir=config['output_directory']),
        expand("{output_dir}/datefile.txt",output_dir=config['output_directory']),
        expand("{output_dir}/sim.mat.pb",output_dir=config['output_directory']),
        expand("{output_dir}/sim.tree",output_dir=config['output_directory']),
        expand("{output_dir}/newick_output_tree.nwk", output_dir=config['output_directory']),
        expand("{output_dir}/newick_output_sample_population.tsv", output_dir=config['output_directory']),
        expand("{output_dir}/newick_output_metadata.tsv", output_dir=config['output_directory']),

rule annotateTree:
    input:
        expand("{output_dir}/sim.mat.pb",output_dir=config['output_directory']),
        expand("{output_dir}/labelled_metadata.tsv",output_dir=config['output_directory']),
    output:
        expand("{output_dir}/result.jsonl.gz",output_dir=config['output_directory'])
    shell:
        "usher_to_taxonium --input {config[output_directory]}/sim.mat.pb --output {config[output_directory]}/result.jsonl.gz --metadata {config[output_directory]}/labelled_metadata.tsv --columns location,time"

rule postProcess:
    input:
        expand("{output_dir}/sim.tree",output_dir=config['output_directory']),
        expand("{output_dir}/full_metadata.tsv",output_dir=config['output_directory']),
    output:
        expand("{output_dir}/sim.substitutions.tree",output_dir=config['output_directory']),
        expand("{output_dir}/datefile.txt",output_dir=config['output_directory']),
    shell:
        "python3 ./simulation_processing/post_process.py --datapath {config[output_directory]}"

rule phastSim:
    input:
        expand("{output_dir}/genealogy.nwk",output_dir=config['output_directory']),
    output:
        expand("{output_dir}/sim.mat.pb",output_dir=config['output_directory']),
        expand("{output_dir}/sim.tree", output_dir=config['output_directory']),

    shell:
        "phastSim --output sim --outpath {config[output_directory]}/ --reference {config[phastsim-params][ref]} --scale {config[phastsim-params][scale]} --createMAT --treeFile {input} --eteFormat {config[phastsim-params][ete3_mode]} --mutationRates {config[phastsim-params][mr_model]} {config[phastsim-params][mut_rates]} --createNewick --createFasta"

rule relabelCountries:
    input:
        expand("{output_dir}/full_metadata.tsv",output_dir=config['output_directory']),
        "population_data/output/census_2013.csv"
    output:
        expand("{output_dir}/labelled_metadata.tsv",output_dir=config['output_directory'])
    shell:
        "python3 population_data/relabel_populations.py --metadata {config[output_directory]}/full_metadata.tsv --dictionary population_data/output/manypop_country_ids.csv --output {config[output_directory]}/labelled_metadata"

rule timeScale:
    input:
        expand("{output_dir}/newick_output_tree.nwk",output_dir=config['output_directory']),
        expand("{output_dir}/newick_output_metadata.tsv", output_dir=config['output_directory']),
    output:
        expand("{output_dir}/genealogy.nwk",output_dir=config['output_directory']),
        expand("{output_dir}/full_metadata.csv", output_dir=config['output_directory']),
    shell:
        "python3 ./simulation_processing/time_scaler.py --folder={config[output_directory]}"



rule VGsim:
    input:
        expand("{param_dir}.{extension}", param_dir=config['vgsim-params']['ppmg'], extension=['pp','mg'])
    output:
        expand("{output_dir}/newick_output_tree.nwk",output_dir=config['output_directory']),
        expand("{output_dir}/newick_output_sample_population.tsv",output_dir=config['output_directory']),
        expand("{output_dir}/newick_output_metadata.tsv",output_dir=config['output_directory']),
    shell:
        "python3 ./bin/VGsim_cmd.py -it {config[vg_iterations]} -s {config[vg_samples]} -pm {config[vgsim-params][ppmg]}.pp {config[vgsim-params][ppmg]}.mg --createNewick {config[output_directory]}/newick_output --writeMigrations {config[output_directory]}/migrations"