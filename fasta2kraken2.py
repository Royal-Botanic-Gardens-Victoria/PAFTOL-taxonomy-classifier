#!/usr/bin/env python3

#r3.3
#convert paftol fasta format to kraken db library fasta format

import sys
import re
import glob
import subprocess
import os


def tokenize(filename):
	digits = re.compile(r'(\d+)')
	return tuple(int(token) if match else token for token, match in ((fragment, digits.search(fragment)) for fragment in digits.split(filename)))

def taxid2dict(taxidfile):
	data={}
	for i in taxidfile:
	
		k=i.split("\t")
		taxid=k[1]
		spp=k[0] #.split(";")[-1].rstrip("\n")
		
		if taxid!="no_taxid_found\n":
		
			data[spp]=taxid
		
	return data

def fasta2kraken2(infolder,taxids,outfile):

	#paftol format
	#>6483 Gene_Name:RPL13 Species:Cyperus_laevigatus Repository:INSDC Sequence_ID:ERR3650073
	#kraken2 format
	#>kraken:taxid|3635|NC_030074.1 Gossypium hirsutum cultivar TM-1 chromosome 1, ASM98774v1, whole genome shotgun sequence
	
	filelist=glob.glob(infolder)
	filelist.sort(key=tokenize)

	errfile=open("taxa.notfound",'w')
	
	for i in filelist:
	
		print(i)
		f=open(i,'r')
		notfound=[]
		c=0
		for x in f:
		
			if x[0]==">":
				
				spp=x.split(":")[2].replace(" Repository","").replace("_"," ")
				#print(spp)
				#input()
				try:
					tax=taxids[spp]
					c=1
				except:
					c=0
						
				if c==1:
					id1=">kraken:taxid|"+tax+"|"+x[1:]
					
					outfile.write(id1)
			
			else:
				if c==1:
				
					outfile.write(x)
			

def main():

	infolder = sys.argv[1] #input folder/file
	taxidfile=open(sys.argv[2],'r')
	outfile = open(sys.argv[3],'w') #output file
	
	taxids=taxid2dict(taxidfile)

	fasta2kraken2(infolder, taxids,outfile)

	print("done")
	
	

if __name__ == '__main__': main()


	
		
		
		
		