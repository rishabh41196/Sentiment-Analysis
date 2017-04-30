import sys

def extractDataset():

	data = []
	data1 = []
	f = open(".//dataset//testingDatasetComplete.txt",'r')
	for line in f:
		words = line.split('\t')
		if words[3] != "Not Available\n":
			data.append(line)
			data1.append(words[3])
	f.close()

	f = open(".//dataset//testingDatasetProcessed.txt",'w')
	f.write("".join(data))
	f.close()

	f = open(".//dataset//example_tweets.txt",'w')
	f.write("".join(data1))
	f.close()
	
			
		
