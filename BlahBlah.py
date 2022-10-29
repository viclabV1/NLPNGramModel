#Program Name: N-Gram Generator
#Author: Victor Paul LaBrie
#Date: October 19th, 2022
#Problem: Implement a program that will learn an Ngram language model from an
#arbitrary number of plain text files.

#imports
from fileinput import close
from posixpath import splitext
import sys
import re


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
    #Then, convert all text to lower case and store in a string:
    print(n,m, *textFiles)
    n = int(n)
    m = int(m)
    allText = ""
    for txt in textFiles:
        thisFile = open(txt)
        thisText = thisFile.read().lower()
        allText += thisText
        thisFile.close()
    #Remove all non alphanumeric-text:
    cleanedText = re.sub(r"[^a-zA-Z0-9 \.\,\?\!]", "", allText)
    #Put space between words and punctuation
    cleanedText = re.sub(r"([,\.\?\!])", r" \1 ", cleanedText)
    #Call ngram model generator and printer:
    #print(cleanedText)
    ngrams(n, cleanedText)
    
    #Last line printed will be number of tokens in corpus.
    print("Tokens in corpus:", len(cleanedText.split()))
    return 0

#Function for generating ngram model
def ngrams(n, text):
    ngramDict = {}
    tokenSum = 0
    #Look at each word
    #print(text.split())
    tokenList = list(text)
    splitText = text.split();
    #print(splitText)
    
    #for ngrams
    for i in range(0, len(splitText)-n):
        thisNgram = ""
        for j in range(i,i+n):
            thisNgram += splitText[j]
            thisNgram += " "
        if thisNgram not in ngramDict:
            ngramDict[thisNgram] = 1
        else:
            ngramDict[thisNgram] += 1

    #for single words
    # for i in splitText:
    #         if i not in ngramDict:
    #             ngramDict[i] = 1
    #         else:
    #             ngramDict[i] += 1
            
    #next, we sort the dictionary
    sortedWordList = sorted(ngramDict, key = ngramDict.get, reverse=True)
    sortedWordDict = {}
    for y in sortedWordList:
        sortedWordDict[y]=ngramDict[y]
    sortedKeys = list(sortedWordDict.keys())
    sortedItems = list(sortedWordDict.items())
    
    tokenSum = len(text.split())
    print("Number of tokens: ", tokenSum)
    print("Number of types: ", len(sortedKeys))
    for i in range(0,100):
        thisItem = sortedItems[i]
        print(thisItem)
    

main()
