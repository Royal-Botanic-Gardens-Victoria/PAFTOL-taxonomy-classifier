
Scripts to create Kraken2 database of PAFTOL V2.0 Angio353 genes. An excellent database for taxonomic identification of plants. 

https://treeoflife.kew.org/ 

https://github.com/DerrickWood/kraken2/wiki

Prior to using this script, download and install kraken2 and make sure it is working and in your PATH.

Make sure the location of the python scripts used below are also in your PATH 

After building the DB with kraken2_paftol_DB.sh, the scripts kraken2paired.py and top_taxa.py can be used to identify taxonomy of unknown samples.

e.g.

kraken2paired.py "reads/*.fastq" kraken_results/ 0 24 kraken2_paftol2/

top_taxa.py "kraken_results/*" kraken.out
