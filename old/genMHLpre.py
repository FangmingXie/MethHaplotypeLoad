#!/usr/bin/env python

# return readList from hapinfo
# region is 0-based coordinate
def genMHLpre(hapinfoPath, chrN, lo, hi, readLength=100):
	### get all reads overlap with the region
	with open(hapinfoPath, 'r') as hapFile:
		# initialize readList
		readList_cg = []
		readList_ca = []
		readList_ct = []
		readList_cc = []
		# read the first read
		line1_t = hapFile.readline()
		line2_t = hapFile.readline()
		line3_t = hapFile.readline()
		while line1_t:
			### deal with this read
			readID, chrN_t, strand_t, pos_start_t = line1_t.strip('\n').split('\t')[0:4]
			pos_start_t = int(pos_start_t)
			# !!! ---- pre-select reads overlapping with the defined region ---- !!!
			# !!! caution: the 100 below indicates that this is only valid when readLength == 100 !!!
			if line2_t != '\n' and line3_t !='\n' \
			   and chrN_t == chrN and lo - readLength < pos_start_t < hi:
				### carefully consider this read
				#for item in line2_t.strip('\n').split('\t'):
				#	try:
				#		cPosList_t = [int(item) for item in line2_t.strip('\n').split('\t')]
				#	except:
				#		print 'not an int %s' % readID 

				cPosList_t = [int(item) for item in line2_t.strip('\n').split('\t')]
				biSeq_t = [item for item in line3_t.strip('\n').split('\t')]
				length_t = len(cPosList_t)
				#print biSeq_t
				#print cPosList_t
				### more carefully look at it
				# overlap must exists
				if cPosList_t[0] < hi and cPosList_t[length_t - 1] >= lo: 
					# ind_i as initial 
					ind_i = 0
					while ind_i < length_t and cPosList_t[ind_i] < lo:
						ind_i += 1
					# ind_j as final
					ind_j = length_t
					while ind_j > 0 and cPosList_t[ind_j-1] >= hi:
						ind_j -= 1
					# overlapped: send into readList
					if ind_i < ind_j:
						# update 5/16/2017 include ch
						tempRead = biSeq_t[ind_i:ind_j]
						cgRead = [item.isupper() for item in tempRead if item == 'g' or item == 'G']
						caRead = [item.isupper() for item in tempRead if item == 'a' or item == 'A']
						ctRead = [item.isupper() for item in tempRead if item == 't' or item == 'T']
						ccRead = [item.isupper() for item in tempRead if item == 'c' or item == 'C']
						if cgRead:
							# [0, 1 ...] bool
							readList_cg.append(cgRead)
						if caRead:
							# [0, 1 ...] bool
							readList_ca.append(caRead)
						if ctRead:
							# [0, 1 ...] bool
							readList_ct.append(ctRead)
						if ccRead:
							# [0, 1 ...] bool
							readList_cc.append(ccRead)
						#print biSeq_t[ind_i:ind_j]
						#print cPosList_t[ind_i:ind_j]
						#print (ind_i, ind_j)
			# read the next read
			line1_t = hapFile.readline()
			line2_t = hapFile.readline()
			line3_t = hapFile.readline()
	return readList_cg, readList_ca, readList_ct, readList_cc

if __name__ == '__main__':
	hapinfoPath = '03.hapinfo.txt'
	chrN = 'chr1'
	lo = 1000000
	hi = lo + 100
	readList, readList2, readList3, readList4 = genMHLpre(hapinfoPath, chrN, lo, hi, readLength=100)
	print readList