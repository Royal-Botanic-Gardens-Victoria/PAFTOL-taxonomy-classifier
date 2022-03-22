#!/usr/bin/env python3

#Theo Allnutt 2021.
#Usage:
#kraken2paired.py "reads/*.fastq" kraken_results/ 0 24 kraken2_paftol2/

#Where 'reads/' is a directory containing paired fastq read files for all samples to be analysed
#0 is the kraken2 confidence value. In this case we want all read hits, so use zero
#24 is the number of threads
#kraken2_paftol2/ is the kraken2 report output directory

import sys
import re
import glob
import subprocess
import os

digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))


folder = sys.argv[1] 
folder = os.path.expanduser(folder)

filelist=glob.glob(folder)

filelist.sort(key=tokenize)

print(filelist)
	
outfolder=sys.argv[2]

subprocess.Popen("mkdir -p %s" %outfolder,shell=True).wait()
#subprocess.Popen("module load kraken2",shell=True).wait()

conf= sys.argv[3]

threads=sys.argv[4]

db= sys.argv[5]

for i in range(0,len(filelist)-1,2):
	print('Processing:',filelist[i],filelist[i+1])
	
	filename=filelist[i].split("/")[-1].split("_")[0]
	
	outname=outfolder+filename
	
	subprocess.Popen("kraken2 --db %s %s %s --threads %s  --confidence %s --report %s.report --use-names --paired" %(db,filelist[i],filelist[i+1],threads,conf,outname),shell=True).wait()

#--unclassified-out %s#.nohit.fastq --classified-out %s#.hit.fastq --use-mpa-style -output %s.out



