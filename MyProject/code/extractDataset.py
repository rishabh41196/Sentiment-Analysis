"""This code takes as input the path of filename of the original dataset and the output filename"""
"""It returns the processed dataset with the relevant fields"""
"""It helps in generating Training Data with Labels or without labels"""

import sys

def main():

	if len(sys.argv)!=4:
		print "Usage :: python extractData pathOfInputFileName outputFileName tempFileToHoldTweetForNlpTagger"
		sys.exit(0)

	data = []
	data1 = []
	f = open(sys.argv[1],'r')
	for line in f:
		words = line.split('\t')
		if words[3] != "Not Available\n":
			data.append(line)
			data1.append(words[3])
	f.close()

	f = open(sys.argv[2],'w')
	f.write("".join(data))
	f.close()

	f = open(sys.argv[3],'w')
	f.write("".join(data1))
	f.close()
	
if __name__ == "__main__":
	main()
	
			
		
