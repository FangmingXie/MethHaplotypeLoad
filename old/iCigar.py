#!/usr/bin/env python

def isNumber(char):
	numList = [str(i) for i in range(0, 10)]
	for num in numList:
		if char == num:
			# is number
			return 1
	# isn't number
	return 0

def isCigarChar(char):
	cigCharList = ['M', 'I', 'D', 'N', 'S', 'H', 'P', '=', 'X']
	for cigChar in cigCharList:
		if char == cigChar:
			# is cigChar
			return 1
	return 0

# cigar is a sring "77M1D2I3M"
def iCigar(cigar):
	cigarList = list(cigar)
	numList = []
	cigCharList = []
	tempQue = []
	for char in cigarList:
		if isNumber(char):
			# in queue
			tempQue.append(char)
		else:
			# must be a cigarChar
			if isCigarChar(char):
				# combine numbers; put info into numList & cigarList
				numList.append(int(''.join(tempQue)))
				cigCharList.append(char)
				# clear tempQue
				tempQue = []
			else:
				# error
				print ">error: abnormal cigar %s" % char
				return [], []
	return numList, cigCharList

if __name__ == '__main__':
	testCigar = '77M2D3I'
	testCigar = '32K'
	numList, cigCharList = iCigar(testCigar)
	print numList
	print cigCharList
