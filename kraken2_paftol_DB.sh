#!/bin/bash

#Scripts to create Kraken2 database of PAFTOL V2.0 Angio353 genes. An excellent database for taxonomic identification of plants.
#https://treeoflife.kew.org/
#https://github.com/DerrickWood/kraken2/wiki
#Prior to using this script, download and install kraken2 and make sure it is working and in your PATH.
#Make sure the location of the python scripts used below are also in your PATH

#After building the DB, the scripts kraken2paired.py and top_taxa.py can be used to identify taxonomy of unknown samples.
#e.g.
#kraken2paired.py "reads/*.fastq" kraken_results/ 0 24 kraken2_paftol2/
#top_taxa.py "kraken_results/*" kraken.out

#Download PAFTOL V2.0 Angio353 genes from Kew
mkdir fasta

cd fasta

wget --no-parent -r http://sftp.kew.org/pub/paftol/current_release/fasta/by_gene/

cd ..

cat fasta/* > paftol2.fasta

rm -r fasta

#Reformat fasta

grep ">" paftol2.fasta |cut -d ":" -f3 >names1.txt
sed -i 's/ Repository//g' names1.txt
sed -i 's/_/ /g' names1.txt

#Get the TaxID of all species. See https://github.com/Royal-Botanic-Gardens-Victoria/species2taxid.py

species2taxid.py names1.txt names.tax tax2lin.txt "Viridiplantae"

#Reformat fasta headers to kraken2 and add TaxIDs

fasta2kraken2.py "paftol2.fasta" names.tax paftol2_tax.fasta

#Make kraken2 DB directory and add NCBI taxonomy.

mkdir kraken2_paftol2

kraken2-build --download-taxonomy --db kraken2_paftol2

kraken2-build --add-to-library paftol2_tax.fasta --db kraken2_paftol2

kraken2-build --build --threads 1 --db kraken2_paftol2

#n.b. currently there is a bug that prevents kraken2-build from using more than one thread

