#!/usr/bin/env python


import numpy as np
#import time
#import MHLlib

# return MHL score from reads (may not be in the same length)
# reads are binary sequence stored in the form of nested list
def genMHL(readList):
	# get l_max:
	l_max = 0
	num_reads = len(readList)
	for read in readList:
		if len(read) > l_max:
			l_max = len(read)
	# calculate weight w = [w1, w2, ..., w_l_max]
	l_sum = sum(range(1, l_max+1))
	w = np.asarray([float(i)/l_sum for i in range(1, l_max+1)])
	### calculate methyl counts
	m_t = np.zeros(l_max)
	m_t2 = np.zeros(l_max)
	n_t = np.zeros(l_max)
	# loop over each read k, get m^(k)_i, n^(k)_i
	for read in readList:
		l_k = len(read)
		# loop over all possible length
		for i in range(1, l_k+1):
			n_ki = l_k - i + 1
			m_ki = 0
			m_ki2 = 0
			# compute m_ki count
			for j in range(n_ki):
				if read[j:j+i] == [1]*i:
					m_ki += 1
				elif read[j:j+i] == [0]*i:
					m_ki2 += 1
			# update n_t and m_t 
			n_t[i-1] += n_ki
			m_t[i-1] += m_ki
			m_t2[i-1] += m_ki2
	if l_max == 0:
		return -1, -1, -1, 0
	else:
		return (np.sum(w*(m_t/n_t)), np.sum(w*(m_t2/n_t)), m_t[0]/float(n_t[0]), num_reads)






if __name__ == '__main__':
	#readList = [[0,0,0,0], [1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1], [1,1,0,0], [1,0,1,0], [1,0,0,1],\
	#		[0,1,1,0], [0,1,0,1], [0,0,1,1], [1,1,1,0], [1,0,1,1], [1,1,0,1], [1,1,1,0], [1,1,1,1]]
	#readList = [[1]*4 for i in range(16)]
	#readList = [[0]*4 for i in range(16)]
	#readList = [[0]*4 for i in range(8)] + [[1]*4 for i in range(8)]
	#readList = [[0]*2 + [1]*2 for i in range(8)] + [[1]*2 + [0]*2 for i in range(8)]
	#readList = [[1,1,0], [0,0], [0], [0,0,0,0]]
	readList = [[1, 1, 1], [0, 0, 0]]

	#start_time = time.time()
	mhl, umhl, ml, num_reads = genMHL(readList)
	print mhl, umhl, ml, num_reads
	#print time.time() - start_time
	#start_time = time.time()
	#mhl = MHLlib.genMHL(readList)
	#print mhl
	#print time.time() - start_time


