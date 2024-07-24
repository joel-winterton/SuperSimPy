configfile: 'config.yaml'

rule annotateTree:
    input:
        expand("{output_dir}/sim.mat.pb",output_dir=config['output_directory']),
        expand("{output_dir}/labelled_metadata.tsv",output_dir=config['output_directory']),
    output:
        expand("{output_dir}/result.jsonl.gz",output_dir=config['output_directory'])
    shell:
        "usher_to_taxonium --input {config[output_directory]}/sim.mat.pb --output {config[output_directory]}/result.jsonl.gz --metadata {config[output_directory]}/labelled_metadata.tsv --columns location,time"

rule relabelCountries:
    input:
        expand("{output_dir}/newick_output_metadata.tsv",output_dir=config['output_directory']),
        "population_data/output/census_2013.csv"
    output:
        expand("{output_dir}/labelled_metadata.tsv",output_dir=config['output_directory'])
    shell:
        "python3 population_data/relabel_populations.py --metadata {config[output_directory]}/newick_output_metadata.tsv --dictionary population_data/output/manypop_country_ids.csv --output {config[output_directory]}/labelled_metadata"

rule phastSim:
    input:
        expand("{output_dir}/newick_output_tree.nwk",output_dir=config['output_directory']),
    output:
        expand("{output_dir}/sim.mat.pb",output_dir=config['output_directory']),
    shell:
        "{config[executables][phastexec]} --output sim --outpath {config[output_directory]}/ --reference {config[phastsim-params][ref]} --scale {config[phastsim-params][scale]} --createMAT --treeFile {input} --eteFormat {config[phastsim-params][ete3_mode]} --mutationRates {config[phastsim-params][mr_model]} {config[phastsim-params][mut_rates]} --createNewick"

rule VGsim:
    output:
        expand("{output_dir}/newick_output_tree.nwk",output_dir=config['output_directory']),
        expand("{output_dir}/newick_output_sample_population.tsv",output_dir=config['output_directory']),
        expand("{output_dir}/newick_output_metadata.tsv",output_dir=config['output_directory']),
    shell:
        "python3 {config[executables][vgexec]} -rt {config[vgsim-params][rt]} -it {config[vgsim-params][it]} -s {config[vgsim-params][samples]} -pm {config[vgsim-params][ppmg]}.pp {config[vgsim-params][ppmg]}.mg -su {config[vgsim-params][sust]}.su -st {config[vgsim-params][sust]}.st --createNewick {config[output_directory]}/newick_output --writeMigrations {config[output_directory]}/migrations"
