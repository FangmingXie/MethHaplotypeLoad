#!/usr/bin/env python

import iCigar



# flag interpretation
def iFlag(flag):
	if flag == '99' or flag == '147':  # template + strand
		strand = '+'
	elif flag == '163' or flag == '83':  # template - strand
		strand = '-'
	else:								# yet unknown
		strand = ''
	return strand


def siteConversion(site):
	if site.upper() == 'A':
		return 'T'
	elif site.upper() == 'T':
		return 'A'
	elif site.upper() == 'G':
		return 'C'
	elif site.upper() == 'C':
		return 'G'

# -1 mismatched; lower unmethylated; upper methylated; N/n not known
def compareSite_v1(bamSite, refSite, refSitePrevious, refSiteNext, option='+'):
	if option == '+':
		pass
	elif option == '-':
		# reverse back to '-' strand
		bamSite = siteConversion(bamSite)
		refSite = siteConversion(refSite)
		# Previous -> Next !!!
		refSiteNext = siteConversion(refSitePrevious)

	if refSite == 'C':
		if bamSite == 'C':
			# i, methyl=1
			return refSiteNext.upper()
		elif bamSite == 'T':
			# i, methyl=0
			return refSiteNext.lower()
		else:
			# mismatch; treat it as genome uncovered -1
			return -1

# disgard 05/30/2017
# # -2 not interested; -1 mismatched; 0 unmethylated; 1 methylated
# def compareSite(bamSite, refSite, refSitePrevious, refSiteNext, option='+'):
# 	if option == '+':
# 		if refSite == 'C': 
# 			if refSiteNext == 'G':
# 				if bamSite == 'C':
# 					# i, methyl=1
# 					return 1
# 				elif bamSite == 'T':
# 					# i, methyl=0
# 					return 0
# 				else:
# 					# mismatch; treat it as genome uncovered -1
# 					return -1
# 			# nonCG CH
# 			else:
# 				if bamSite == 'C':
# 					# i, methyl=1 (3)
# 					return 3
# 				elif bamSite == 'T':
# 					# i, methyl=0 (2)
# 					return 2
# 				else:
# 					# mismatch; treat it as genome uncovered -1
# 					return -1
# 		else:
# 			# reference not a c site
# 			return -2
# 	elif option == '-':
# 		if refSite == 'G': 
# 			if refSitePrevious == 'C':
# 				if bamSite == 'G':
# 					# i, methyl=1
# 					return 1
# 				elif bamSite == 'A':
# 					# i, methyl=0
# 					return 0
# 				else:
# 					# mismatch; treat it as genome uncovered -1
# 					return -1
# 			# nonCG CH
# 			else:
# 				if bamSite == 'G':
# 					# i, methyl=1
# 					return 3
# 				elif bamSite == 'A':
# 					# i, methyl=0
# 					return 2
# 				else:
# 					# mismatch; treat it as genome uncovered -1
# 					return -1
# 		else:
# 			# reference not a g site
# 			return -2


# input two lists of uppercase chars
def compareSeq(bamSeq, refSeq, cigar, option='+'):
	# extract cigar info
	numList, cigCharList = iCigar.iCigar(cigar)
	# initialization
	posList = []
	methylList = []
	# start from 0
	i = 0
	# start from 1 Updated 4/28/2017
	j = 1
	ni = len(bamSeq)
	nj = len(refSeq)
	# loop over cigar info
	for cigInd, cigar in enumerate(cigCharList):
		# look at cigarChar, if M - compare; I - insert ref; D - delete ref
		if cigar == 'M':
			# compare numList[cigInd] times
			for n in range(numList[cigInd]):
				# proceed if i and j is within limit
				if i < ni and 0 < j < nj-1: # (1-nj-2)
					re = compareSite_v1(bamSeq[i], refSeq[j], refSeq[j-1], refSeq[j+1], option=option)
					# update 5/30/2017: re = a/t/g/c/A/T/G/C/ n/N/-1
					# update 5/16/2017: re = 0/1 CG; re = 2/3 CH
					if re in ['a', 't', 'g', 'c', 'A', 'T', 'G', 'C']:
						# 4/28/17 update (restore correct pos)
						posList.append(j-1)
						methylList.append(re)
					else:
						# re == n/N/-1
						pass
					i += 1
					j += 1
				# i or j exceeds limit
				else:
					break
				
		elif cigar == 'D':
			# delete ref (shift ref)
			j += numList[cigInd]
		elif cigar == 'I':
			# insert ref (shift bam)
			i += numList[cigInd]
		else:
			# cigChar == other char
			pass
	return posList, methylList


def gen1Read(bamSeq, refSeq, flag, cigar, pos):
	# examine flag
	strand = iFlag(flag)
	if strand: # not void
		posList, methylList = compareSeq(bamSeq, refSeq, cigar, option=strand)
	else:      # void strand (unknow flag)
		print "discarded_flag: " + flag
	# restore chrN pos
	pos_cList = [(pos + i) for i in posList]

	return strand, pos_cList, methylList

def list2file(lst, f):
	if not lst:
		return
	for i, item in enumerate(lst):
		if i == len(lst) - 1:
			f.write(str(item) + '\n')
		else:
			f.write(str(item) + '\t')
	return



def compareReads(inputSamPath, inputFastaPath, outputPath):
	# matched files: # of lines in .fa = 2*# of lines in .sam
	with open(inputSamPath, 'r') as isamFile, open(inputFastaPath, 'r') as ifaFile, \
    	 open(outputPath, 'w') as outputFile:
		# first read
		ID = 1
		isamLine = isamFile.readline()
		ifaLine = ifaFile.readline()
		ifaLine = ifaFile.readline()
		while isamLine and ifaFile:
			# read info
			isamLineList = isamLine.strip('\n').split('\t')
			flag, chrN, pos, qual, cigar = isamLineList[1:6]
			# to 0-based pos (int)
			pos = int(pos) - 1
			# bam seq is a list of uppercase chars
			bamSeq = list(isamLineList[9].upper())
			#print flag, chrN, pos, qual, cigar
			#print bamSeq
			# reference seq is a list of uppercase chars
			refSeq = list(ifaLine.strip('\n').upper())
			# methyl info for a single read 
			strand, pos_cList, methylList = gen1Read(bamSeq, refSeq, flag, cigar, pos)
			# output to file
			outputFile.write('>' + str(ID) + '\t' + chrN + '\t' + strand + '\t' + str(pos) + '\n')
			if pos_cList and methylList:
				list2file(pos_cList, outputFile)
				list2file(methylList, outputFile)
			else:
				# occupy 2 empty lines
				outputFile.write('\n')
				outputFile.write('\n')
			# next read
			ID += 1
			isamLine = isamFile.readline()
			ifaLine = ifaFile.readline()
			ifaLine = ifaFile.readline()

			# oversee progress
			#if ID%1000000 == 2:
			#	print chrN, ID



if __name__ == '__main__':
	inputSamPath = "/cndd/fangming/cfDNA/02.sample.sam"
	inputFastaPath = "/cndd/fangming/cfDNA/temp.refReads.fa"
	outputPath = "/cndd/fangming/cfDNA/03.hapinfo.txt"
	compareReads(inputSamPath, inputFastaPath, outputPath)