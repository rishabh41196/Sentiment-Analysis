import sys
import os
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def extract():

	data = []
	data1 = []
	f = open(os.path.join(BASE_DIR,"dataset","testingDatasetComplete.txt"),'r')
	for line in f:
		words = line.split('\t')
		if words[3] != "Not Available\n":
			data.append(line)
			data1.append(words[3])
	f.close()
	f = open(os.path.join(BASE_DIR,"dataset","testingDatasetProcessed.txt"),'w')
	f.write("".join(data))
	f.close()

	f = open(os.path.join(BASE_DIR,"dataset","example_tweets.txt"),'w')
	f.write("".join(data1))
	f.close()
	
			
		
