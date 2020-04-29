#!/usr/bin/env python

import genMHLpre
import genMHL
import pandas as pd

# disgard 05/16/2017
'''
def hapinfo2MHL(hapinfoPath, regionPath, outputPath='03.mhl.txt', readLength=100):
	
	df = pd.read_csv(regionPath, sep='\t', header=None, index_col=None)
	with open(outputPath, 'w') as outputFile:
		for (chrN, lo, hi) in zip(df[0], df[1], df[2]):
			readList = genMHLpre.genMHLpre(hapinfoPath, chrN, lo, hi, readLength=readLength)
			mhl, umhl, ml = genMHL.genMHL(readList)
			outputFile.write('%s\t%d\t%d\t%s\t%s\t%s\t%d\n' % (chrN, lo, hi, mhl, umhl, ml, num_reads))
	return
'''

def singleRegionMHL(hapinfoPath, chrN, lo, hi, readLength=100):
	# open with APPEND mode !!!
	readList_cg, readList_ca, readList_ct, readList_cc \
		= genMHLpre.genMHLpre(hapinfoPath, chrN, lo, hi, readLength=readLength)
	mhl, umhl, ml, num_reads = genMHL.genMHL(readList_cg)
	mhl2, umhl2, ml2, num_reads2 = genMHL.genMHL(readList_ca)
	mhl3, umhl3, ml3, num_reads3 = genMHL.genMHL(readList_ct)
	mhl4, umhl4, ml4, num_reads4 = genMHL.genMHL(readList_cc)
	return mhl, umhl, ml, num_reads, mhl2, umhl2, ml2, num_reads2, \
		   mhl3, umhl3, ml3, num_reads3, mhl4, umhl4, ml4, num_reads4,

# disgard 05/16/2017
'''
if __name__ == '__main__':
	# input
	hapinfoPath = '03.hapinfo.txt'
	regionPath = '02.region.bed'
	#
	hapinfo2MHL(hapinfoPath, regionPath, readLength=100)
'''
