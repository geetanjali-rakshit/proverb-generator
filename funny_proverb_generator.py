#!/usr/bin/python

import pronouncing
import random
import nltk
import csv
from gensim.models import Word2Vec
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

def getRhymingList(word):
	rhyme_list = pronouncing.rhymes(word)
	if not rhyme_list:
		return -1
	else:	
		return rhyme_list

def pickFirstNoun(proverb):
	sent_words = nltk.word_tokenize(proverb)
	word_pos_tuples = nltk.pos_tag(sent_words)
	for tup in word_pos_tuples:
		word = tup[0]
		pos = tup[1]
		if(pos in ("NN", "NNS", "NNP", "NNPS")):
			break
	return (word, pos)

def pickSecondNoun(proverb):
	sent_words = nltk.word_tokenize(proverb)
	word_pos_tuples = nltk.pos_tag(sent_words)
	count = 0
	for tup in word_pos_tuples:
		word = tup[0]
		pos = tup[1]
		if(pos in ("NN", "NNS", "NNP", "NNPS")):
			count = count+1
		if(count == 2):
			return (word, pos)
	return (-1, -1)
	
def pickRhymingWord(rhyme_list, word_pos, criteria = 0):
	word_pos_tuples = nltk.pos_tag(rhyme_list)
	word = " "

	if(criteria == 0):
		length = len(rhyme_list)
		for i in range(0, length):
			rand = random.randint(0, length-1)
			candidate_word = rhyme_list[rand]
			if(candidate_word+"_n" in freqDist) or (candidate_word+"_v" in freqDist) or (candidate_word+"_a" in freqDist) or (candidate_word+"_prep" in freqDist) or (candidate_word+"_adv" in freqDist):
				word = candidate_word 
				break

	elif(criteria == 1):
		for tup in word_pos_tuples:
			candidate_word = tup[0]
			pos = tup[1]
			if(pos == word_pos):
				if (candidate_word+"_n" in freqDist) or (candidate_word+"_v" in freqDist) or (candidate_word+"_a" in freqDist) or (candidate_word+"_prep" in freqDist) or (candidate_word+"_adv" in freqDist):
					word = candidate_word 
					break
	return word


def applyOneWordTransform(word, pos, proverb, criteria):
	rhyme_list = getRhymingList(word)
	if(rhyme_list == -1):
		modified_proverb = proverb
	else:
		new_word = pickRhymingWord(rhyme_list, pos, criteria)
		if(new_word == " "):
			modified_proverb = proverb
		else:
			modified_proverb = proverb.replace(word, new_word)
	return modified_proverb

	
'''def applyTwoWordTransform(word1, pos1, word2, pos2, proverb, criteria):
	rhyme_list = getRhymingList(word2)
	if(rhyme_list == -1):
		modified_proverb = proverb
	else:
		new_word2 = pickRhymingWord(rhyme_list, pos2, criteria)
		print("New word 2: "+new_word2)
		print("word 1, word 2: "+word1+" "+word2)
		new_word1 = word_vectors.most_similar(positive=[word2, new_word2], negative=[word1])[0][0]
		print("New word 1: "+new_word1)

		modified_proverb = proverb.replace(word1, new_word1)
		modified_proverb = proverb.replace(word2, new_word2)

	return modified_proverb
'''

def modifyProverb(proverb, criteria, transformation):
	proverb = proverb.lower()

	if(transformation == 1):
		word, pos = pickFirstNoun(proverb)
		modified_proverb = applyOneWordTransform(word, pos, proverb, criteria)
		
	'''elif(transformation == 2):
		word1, pos1 = pickFirstNoun(proverb)
		word2, pos2 = pickSecondNoun(proverb)
		print("nouns picked: "+word1+" "+word2)
		if(word2 == -1):
			modified_proverb = applyOneWordTransform(word1, pos1, proverb, criteria)
		else:
			modified_proverb = applyTwoWordTransform(word1, pos1, word2, pos2, proverb, criteria)
	'''
	#print("Proverb: "str(proverb))
	#print("Modified Proverb: "str(modified_proverb))

	return modified_proverb


def getModifiedProverbs(filename, criteria, transformation):
	fr = open(filename, "r")
	fw = open(filename.split(".")[0]+"_modified_criteria_"+str(criteria)+"_"+str(transformation)+".txt", "w")
	for proverb in fr:
		modifiedProverb = modifyProverb(proverb, criteria, transformation)
		fw.write(modifiedProverb)
	fr.close()
	fw.close()

def generateCSV(filename1, filename2, filename3, outputfile):
	f1 = open(filename1, "r")
	f2 = open(filename2, "r")
	f3 = open(filename3, "r")

	array = [[filename1.split(".")[0], filename2.split(".")[0], filename3.split(".")[0]]]

	for line in f1:
		array.append([line, f2.readline(), f3.readline()])

	outfile = open(outputfile,'w')
	a = csv.writer(outfile)
	a.writerows(array)
	outfile.close()

	f1.close()
	f2.close()
	f3.close()

		
if __name__=="__main__":
	#word = "cake"
	#print(find_rhyme(word))

	#proverb = "Money doesn't grow on trees."
	#proverb = "A watched pot never boils."

	#filename = "top_proverbs.txt"

	#w2vecmodel = "GoogleNews-vectors-negative300.bin"

	#word_vectors = Word2Vec.load_word2vec_format(w2vecmodel, binary=True)

	#word_vectors.most_similar(positive=['woman','king'],negative=['man'])

	freq_words_file = 'lemma.al'
	freqDist = readFreqList(freq_words_file)

	#filename = "top_proverbs.txt"
	filename = "proverbs578.txt"
	transformation = 1
	criteria = 0
		
	getModifiedProverbs(filename, criteria, transformation)
	criteria = 1
	getModifiedProverbs(filename, criteria, transformation)
	
	generateCSV(filename, filename.split(".")[0]+"_modified_criteria_0_"+str(transformation)+".txt", filename.split(".")[0]+"_modified_criteria_1_"+str(transformation)+".txt", filename.split(".")[0]+"_"+str(transformation)+"_modifications.csv")
	
