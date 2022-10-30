#Program Name: N-Gram Generator
#Author: Victor Paul LaBrie
#Date: October 19th, 2022
#Problem: Implement a program that will learn an Ngram language model from an
#arbitrary number of plain text files.

#imports
from fileinput import close
from posixpath import splitext
from random import randint
import sys
import re
import this
import numpy as np
import random



#Main function
def main():
    #First, we need to set this up to get the command line arguments.
    #n and m can be grabbed from the first two arguments
    n = sys.argv[1]
    m = sys.argv[2]
    #Since there can be multiple text files, we can just use list slicing to
    #get the list of text files:
    textFiles = sys.argv[3:]
    #I will then validate the input:
    if not re.match(r'^[1-9]+[0-9]*$', n):
        raise ValueError("First argument must be a valid integer.")
    if not re.match(r'^[1-9]+[0-9]*$', m):
        raise ValueError("Second argument must be a valid integer.")
    for txt in textFiles:
        if not re.match(r'.*\.txt', txt):
            raise ValueError("Invalid text file. Text files must end with \".txt\".")
    #Print out values
    print(n,m, *textFiles)
    n = int(n)
    m = int(m)
    allText = ""
    #open every file and read into one very long string
    for txt in textFiles:
        thisFile = open(txt)
        thisText = thisFile.read().lower()
        allText += thisText
        thisFile.close()
    #Remove all non alphanumeric-text:
    cleanedText = re.sub(r"[^a-zA-Z0-9 \.\,\?\!]", "", allText)
    #Put space between words and ends of sentences, add start of sentence markers
    #Just going to replace punctuation with sentence start and end markers. Will add punctuation after sentence built
    cleanedText = re.sub(r"([\.\?\!])", r" </s> <s> ", cleanedText)
    #Just gonna get rid of commas
    cleanedText = re.sub(r"([,])", r" ", cleanedText)
    #Call ngram model generator and printer:
    #print(cleanedText)
    ngramModel, typeCount = ngrams(n, cleanedText)
    
    sentenceGenerator(m, ngramModel);
    #Last line printed will be number of tokens in corpus.
    print("Tokens in corpus:", len(cleanedText.split()))
    print("N-Gram types in corpus:", typeCount)
    return 0

#Function for generating and printing random sentences
def sentenceGenerator(m, model):
    #Each sentence will be built word by word before being printed
    thisSentence = ""
    nGramsWith = []
    justNgrams = []
    probsForThis = []
    totalNgramsForThis = 0
    n = len(model[0][0].split())

    #Loop for building each setence
    for i in range(0, m):
        
        #NEED TO FIRST CHOOSE random 
        thisSentence = ""
        nGramsWith = []
        justNgrams = []
        probsForThis = []
        totalNgramsForThis = 0
        
        #For probability calculation, we just find the count of each with a specific prefix and then divide by
        #the total number of ngrams with that prefix

        for x in model:
            if x[0].split()[0] == "<s>":
                #find all ngrams with start of sentence at beginning.
                nGramsWith.append(x)
        for y in nGramsWith:
            probsForThis.append(y[1])
            justNgrams.append(y[0])
            totalNgramsForThis += int(y[1])
        
        probsForThis = [value * (1/totalNgramsForThis) for value in probsForThis]
        thisSentence += "".join(random.choices(justNgrams, probsForThis))
        
        #while end of sentence not reached
        while thisSentence.split()[-1]!="</s>":
            nGramsWith = []
            justNgrams = []
            probsForThis = []
            totalNgramsForThis = 0
            #print(thisSentenc)
            for x in model:
                
                if x[0].split()[1:] == thisSentence.split()[len(thisSentence.split())-n+1:]:
                    #find all ngrams with start of sentence at beginning.
                    nGramsWith.append(x)
                    #print(thisSentence.split()[:-1])
                    #print(x[0].split()[1:])
            for y in nGramsWith:
                probsForThis.append(y[1])
                justNgrams.append(y[0])
                totalNgramsForThis += int(y[1])
            #not even gonna mess with smoothing, but if an ngram can't be found I'll pull a completely random one
            if len(nGramsWith)==0:
                justNgrams.append(model[randint(0,len(model))][0])
                justNgrams.append("</s>")
                #print(justNgrams)
                totalNgramsForThis = 2
                probsForThis = [1.6,0.4]

            probsForThis = [value * (1/totalNgramsForThis) for value in probsForThis]
            nextWord = "".join(random.choices(justNgrams, probsForThis)).split()[-1]
            #print(nextWord)
            thisSentence = thisSentence + " " + nextWord
            print(thisSentence)
            #print(justNgrams)
        thisSentence = re.sub(r"<s>",r"", thisSentence)
        thisSentence = re.sub(r"</s>",r"", thisSentence)
        thisSentence += "."
        print(thisSentence)
       

      

#Function for generating ngram model
def ngrams(n, text) -> tuple[list,int]:
    ngramDict = {}
    tokenSum = 0
    
    #Look at each word
    splitText = text.split();
    #create list of all ngrams
    for i in range(0, len(splitText)-n):
        thisNgram = ""
        for j in range(i,i+n):
            thisNgram += splitText[j]
            thisNgram += " "
        if thisNgram not in ngramDict:
            ngramDict[thisNgram] = 1
        else:
            ngramDict[thisNgram] += 1
            
    #next, we sort the dictionary
    sortedGramList = sorted(ngramDict, key = ngramDict.get, reverse=True)
    sortedGramDict = {}
    for y in sortedGramList:
        sortedGramDict[y]=ngramDict[y]
    sortedKeys = list(sortedGramDict.keys())
    sortedItems = list(sortedGramDict.items())
    
    typeCount = len(sortedKeys)

    return sortedItems, typeCount
    

main()
