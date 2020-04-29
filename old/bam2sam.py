#!/usr/bin/env python

import subprocess

def bam2sam(bamPath, region, samPath):
	arg1 = 'samtools view %s %s > %s' % (bamPath, region, samPath)
	subprocess.call(arg1, shell=True)


if __name__ == '__main__':
	bamPath = \
	'/cndd/projects/dbGaP_restricted/dbGaP-12550/mapped/hippocampus_SRX838264/hippo_SRX838264_processed_reads_no_clonal.newheader.bam'
	region = 'chr1:1000000-1010000'
	samPath = '/cndd/fangming/cfDNA/02.sample.sam'
	bam2sam(bamPath, region, samPath)