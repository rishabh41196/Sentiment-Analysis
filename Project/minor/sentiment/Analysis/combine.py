"""This code combines the output of the tokeniser and the input tweet set and returns the final input file in the following format"""
""" tweet Id, Tweet tokens, POS tokens, label """

from itertools import izip

def combine():
	data = []
	f1 = open(".//dataset//testingDatasetProcessed.txt", 'r')
	f2 = open(".//dataset//testingTokenised.txt", 'r')
	for line1, line2 in izip(f1,f2):
		words1 = line1.strip().split('\t')
		words2 = line2.strip().split('\t')
		string = words1[0] + '\t' + words2[0] + '\t' + words2[1] + '\t' + words1[2] +'\n'
		data.append(string)
	f1.close()
	f2.close()

	f = open(".//finalTestingInput", 'w')
	f.write("".join(data))
	f.close()
		
