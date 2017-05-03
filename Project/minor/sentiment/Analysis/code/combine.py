"""This code combines the output of the tokeniser and the input tweet set and returns the final input file in the following format"""
""" tweet Id, Tweet tokens, POS tokens, label """

from itertools import izip
import os


BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def combine():
	data = []
	print BASE_DIR
	path=os.path.join(BASE_DIR,"dataset","testingDatasetProcessed.txt")
	f1 = open(path, 'r')

	path=os.path.join(BASE_DIR,"dataset","testingTokenised.txt")
	f2 = open(path, 'r')
	for line1, line2 in izip(f1,f2):
		words1 = line1.strip().split('\t')
		words2 = line2.strip().split('\t')
		string = words1[0] + '\t' + words2[0] + '\t' + words2[1] + '\t' + words1[2] +'\n'
		data.append(string)
	f1.close()
	f2.close()
	path=os.path.join(BASE_DIR,"dataset","finalTestingInput.txt")
	f = open(path, 'w')
	f.write("".join(data))
	f.close()
		
