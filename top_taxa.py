#!/usr/bin/env python3

#Theo Allnutt 2021. r3.4
#Get highest count taxon from kraken report in mpa style.

#Usage: top_taxa.py "kraken_results/*" kraken.out
#Results are reported as full taxonomy of the hit with the most reads. In brackets after each level is the proportion of total reads for that taxon.

import sys
import re
import glob
import subprocess
import os


def tokenize(filename):
	digits = re.compile(r'(\d+)')
	return tuple(int(token) if match else token for token, match in ((fragment, digits.search(fragment)) for fragment in digits.split(filename)))


def tophit(infolder,outfile):

	filelist=glob.glob(infolder)
	filelist.sort(key=tokenize)
	
	taxlevels=["d","k","p","c","o","f","g","s"]
	
	outfile.write("sample\tD\tK\tP\tC\tO\tF\tG\tS\ttotal_reads_mapped\n")
	
	for i in filelist:
	
		sample=i.split("/")[-1].split(".")[0]
		outfile.write(sample)
		
		outline=["","","","","","","",""]
		outcounts=[0,0,0,0,0,0,0,0]
		
		print(i)
		f=open(i,'r')
		data={}
		readtotal=str(f.readline().rstrip("\n").split("\t")[-1])
		f.seek(0)
		
		for x in f:
		
			k = x.rstrip("\n").split("|")
			lev = k[-1].split("__")[0]
			tax = k[-1].split("\t")[0].split("__")[1]
			readcount=float(k[-1].split("\t")[1])
			
			if lev not in data.keys():
				data[lev]={}
				data[lev][tax]=readcount
			
			else:
				if tax not in data[lev].keys():
					data[lev][tax]=readcount
				
		#print(data)
		toptax=[]
		
		for v in taxlevels:
			ranktotal=0
			rank=[]
			
			if v in data.keys():
			
				for j in data[v].keys():
					rank.append((j,data[v][j]))
					ranktotal=ranktotal+data[v][j]
				
				rank.sort(key = lambda x: x[1],reverse=True)
				
				p=rank[0][1]/ranktotal #((ranktotal/float(len(rank)))/rank[0][1])/float(len(rank))
				
				toptax.append((rank[0][0],p))
			else:
				toptax.append(("",0))
		#print(toptax)
				
		for x in toptax:
			outfile.write("\t"+x[0]+"("+str(round(x[1],5))+")")
		
		outfile.write("\t"+readtotal+"\n")
		
	
		
		
def main():

	infolder = sys.argv[1] #result folder
	outfile = open(sys.argv[2],'w') 

	tophit(infolder, outfile)

	print("done")
	
	

if __name__ == '__main__': main()


	
		
		
		
		