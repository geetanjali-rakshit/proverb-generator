#!/usr/bin/python
import codecs
import urllib.request
from bs4 import BeautifulSoup

def getQuote(url, filename):
    outp = codecs.open(filename, encoding='utf-8', mode='w')
    content = urllib.request.urlopen(url).read()
    bs2 = BeautifulSoup(content, "lxml")

    #div class="quoteText"
    #div class="quoteDetails "
    #a class="authorOrTitle"
    #quotes = bs2.findAll("h3", {"class": "quoted-title"})

    #quotes = bs2.findAll("li")
    quotes = bs2.findAll("dd")
    
    for quote in quotes:
       q_text = quote.getText()
       print(q_text)
       q_text = q_text.replace("\"", "")
       outp.write(str(q_text)+"\n")
    outp.close()

def containsYear(line):
    flag = False
    for token in line:
        if(len(token) >= 6):
             if(token[1].isdigit() and token[2].isdigit() and token[3].isdigit() and token[4].isdigit()):
                 flag = True
                 break
    return flag

def clean_wiki_proverbs():
    fp = open("wiki_proverbs.txt", "r")
    fw = open("wiki_proverbs_cleaned.txt", "w")
    
    for line in fp:
        line = line.split()
        if(line == "\n"):	
             continue
        elif("Meaning:" in line):
             continue
        elif("translation:" in line):
             continue
        elif("Variant:" in line):
             continue
        elif("Variation:" in line):
             continue
        elif("By:" in line):
             continue
        elif("Note:" in line):
             continue
        elif("ISBN:" in line):
             continue
        elif(containsYear(line)):
             continue
        elif(len(line) > 20):
             continue
        else:
             fw.write("\n")
             fw.write(" ".join(line))
             

    fp.close()
    fw.close()
    
    fp = open("wiki_proverbs_cleaned.txt", "r")
    fw = open("wiki_proverbs_cleaned_ver1.txt", "w")

    for line in fp:
        if(line == "\n"):
           continue
        else:
           fw.write(line)


    fp.close()
    fw.close()
	

if __name__=="__main__":

    #url = "http://www.phrasemix.com/collections/the-50-most-important-english-proverbs"
    #filename = 'top_proverbs.txt'

    '''url = "https://en.wikiquote.org/wiki/English_proverbs_(alphabetically_by_proverb)"
    filename = 'wiki_proverbs.txt'
    getQuote(url, filename)
    '''
    url = "https://en.wiktionary.org/wiki/Appendix:English_proverbs"
    filename = 'wiktionary_proverbs.txt'
    getQuote(url, filename)

    #clean_wiki_proverbs()
