#!/usr/bin/env python
"""
Input: a bam file, a bed file, and a reference genome file
Output: a bed file with MHL score defined by Guo et al. 2017 

Fangming Xie
"""

import subprocess
import ConfigParser
import sys
import re

import bam2sam
import sam2hapinfo
import hapinfo2MHL

# ex region format: chr1:10000-20000
def gen1MHL(bamPath, chrN, lo, hi, refPath, thread_id, 
            readLength=100):
	"""
	"""

	# get region info 1-based to 0-based, region of interest to region of reads
	# possibly overlap with the region of interest (+- possible error of 10 bases)
	# this region is larger than the region of interest specified by chrN, lo, hi 
	region = "%s:%d-%d" % (chrN, lo+1-readLength-10, hi+10)
	# specify temp file Paths
	samPath = '.' + thread_id + '.temp.sam'
	hapinfoPath = '.' + thread_id + '.temp.hapinfo.txt'

	### run the pipeline
	# chop bam with the region, output to temp.sam
	bam2sam.bam2sam(bamPath, region, samPath)
	# take temp.sam and refGenome, output to temp.hapinfo
	sam2hapinfo.sam2hapinfo(samPath, refPath, thread_id, 
		outputPath=hapinfoPath, readLength=readLength)
	# get MHL of the region and output to mhlPath
	(
	mhl, umhl, ml, num_reads, mhl2, umhl2, ml2, num_reads2, 
	mhl3, umhl3, ml3, num_reads3, mhl4, umhl4, ml4, num_reads4, 
	) = hapinfo2MHL.singleRegionMHL(hapinfoPath, chrN, lo, hi, readLength=readLength)

	# remove temp files
	subprocess.call('rm ' + samPath, shell=True)
	subprocess.call('rm ' + hapinfoPath, shell=True)
	return mhl, umhl, ml, num_reads, mhl2, umhl2, ml2, num_reads2, 
		   mhl3, umhl3, ml3, num_reads3, mhl4, umhl4, ml4, num_reads4,

	
def bambed2mhl(bamPath, bedPath, refPath, mhlPath,
			   header=0, readLength=100):
	
	# print filePaths
	print '>bamPath: %s' % bamPath
	print '>bedPath: %s' % bedPath
	print '>refPath: %s' % refPath
	print '>mhlPath: %s' % mhlPath

	# use bamPath and bedPath to create a unique ID, 
	# in order to name temporary files generated by the pipe line
	thread_id = re.sub('/', '', (bamPath + bedPath))
	
	with open(bedPath, 'r') as bedFile, open(mhlPath, 'w') as outputFile:
		# header
		outputFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' 
			% ('chrN', 'lo', 'hi', 
				'mhlCG', 'umhlCG', 'mCG', 'num_reads_CG', 
				'mhlCA', 'umhlCA', 'mCA', 'num_reads_CA', 
				'mhlCT', 'umhlCT', 'mCT', 'num_reads_CT', 
				'mhlCC', 'umhlCC', 'mCC', 'num_reads_CC', 
				))
		# headerLine
		for i in range(header):
			bedFile.readline()
		# first line
		bedLine = bedFile.readline()
		progress = 1
		while bedLine:
			# region of interest 0-based
			chrN, lo, hi = bedLine.strip('\n').split('\t')[:3]
			# accomodate two format: chrN and N only (both becomes chrN after the procedure)
			chrN = chrN.strip('chr')
			chrN = 'chr' + chrN
			lo = int(lo)
			hi = int(hi)
			# use gen1MHL
			(
			mhl, umhl, ml, num_reads, mhl2, umhl2, ml2, num_reads2, 
		   	mhl3, umhl3, ml3, num_reads3, mhl4, umhl4, ml4, num_reads4,
		   	) = gen1MHL(bamPath, chrN, lo, hi, refPath, thread_id, readLength=readLength)
			
			# output to file			
			outputFile.write('%s\t%d\t%d' % (chrN, lo, hi))
			outputFile.write('\t%.9f\t%.9f\t%.9f\t%d\t%.9f\t%.9f\t%.9f\t%d\t%.9f\t%.9f\t%.9f\t%d\t%.9f\t%.9f\t%.9f\t%d'
				% (mhl, umhl, ml, num_reads, 
				   mhl2, umhl2, ml2, num_reads2,
				   mhl3, umhl3, ml3, num_reads3, 
				   mhl4, umhl4, ml4, num_reads4)
				)
			outputFile.write('\n')
			
			# check progress
			if progress % 100 == 1:
				print '>progress: %d' % progress
			# next line
			bedLine = bedFile.readline()
			progress += 1
	
	print '>Done!'
			

if __name__ == '__main__':

	config_file = sys.argv[1]

	cfg = ConfigParser.ConfigParser()
	if cfg.read(config_file):

		bamPath = cfg.get('input', 'bam_file')
		bedPath = cfg.get('input', 'bed_file')
		refPath = cfg.get('input', 'genome_fa_file')
		header = int(cfg.get('input', 'num_headerLines_in_bed'))
		readLength = int(cfg.get('input', 'read_length_in_bam'))
		mhlPath = cfg.get('output', 'mhl_file')
		bambed2mhl(bamPath, bedPath, refPath, mhlPath, header=header, readLength=readLength)
		
	else:
		print "Error: configuration file doesn't exist."

