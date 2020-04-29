#!/usr/bin/env python

import subprocess
import compareReads


def sam2hapinfo(samPath, refGenomePath, thread_id, outputPath='03.hapinfo.txt', readLength=100):


	# update 4/30/2017 modify naming convention of temp files to allow for parallelization
	refReadsPath = '.' + thread_id + '.temp.refReads.fa'
	tempBedPath = '.' + thread_id + '.temp.bed'

	# use sam-info to generate corresponding genome reads with readLength
	# sam to bed: extract "chr#" and "pos_start"(to 0-based) "pos_end"(to 0-based) info
	# update 4/28/17 -1/+1 to get the site before the first and after the last  
	arg1 = '''cat %s | awk '{print $5 "\t" $6-1-1 "\t" $6-1+%d+1}' > %s''' % (samPath, readLength, tempBedPath)
	subprocess.call(arg1, shell=True)
	#print ">temp.bed generated (readLength = %d)..." % readLength
	# bed to reference reads Fasta
	arg2 = 'bedtools getfasta -fi %s -bed %s -fo %s' % (refGenomePath, tempBedPath, refReadsPath)
	subprocess.call(arg2, shell=True)
	#print ">temp.refReads.fa generated..."
	# remove temp.bed
	subprocess.call('rm ' + tempBedPath, shell=True)

	# ---compare bam and genome reads to generate hapinfo in outputPath
	compareReads.compareReads(samPath, refReadsPath, outputPath)
	#print ">03.hapinfo.txt generated..."

	# remove temp.refReads.fa
	subprocess.call('rm %s' % refReadsPath, shell=True)
	#print ">Done with sam2hapinfo!" 

if __name__ == '__main__':
	# ---file locations
	# input input.sam and reference genome.fasta
	samPath = '/cndd/fangming/cfDNA/sample01.sam'
	refGenomePath = '/cndd/Public_Datasets/references/hg19/genome/hg19.fasta'
	thread_id = 'test_id'

	# default output
	sam2hapinfo(samPath, refGenomePath, thread_id, readLength=100)