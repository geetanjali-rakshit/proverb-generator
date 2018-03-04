import gzip
import os


def readFreqList(filename):
	if(os.path.isfile(filename)):
		f = open(filename, 'r')
		
	else:
		f = gzip.open(filename+'.gz', 'rb')
	file_content = f.read()
	f.close()
	return(createDict(file_content))

def createDict(file_content):
	freqDist = {}
	file_content = file_content.split("\n") 
	for line in file_content:
		line = line.strip()
		line = line.split(" ")
		if(line[0] != ""):
			freqDist[line[2]+"_"+line[3]] = int(line[1])
	return freqDist
		

if __name__ == "__main__":
	filename = 'lemma.al'
	freqDist = readFreqList(filename)
	print(freqDist)
