#Program Name: N-Gram Generator
#Author: Victor Paul LaBrie
#Date: October 19th, 2022
#Problem: Implement a progra  that will learn an Ngram language model from an
#arbitrary number of plain text files.

from fileinput import close
import sys
import re
from types import NoneType

#Main function
def main():
    #First, we need to set this up to get the command line arguments.
    #n and m can be grabbed from the first two arguments
    n = sys.argv[1]
    #print(n, type(n))
    m = sys.argv[2]
    #print(m, type(m))
    #Since there can be multiple text files, we can just use list slicing to
    #get the list of text files:
    textFiles = sys.argv[3:]
    #print(textFiles)
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
    allText = ""
    for txt in textFiles:
        thisFile = open(txt)
        thisText = thisFile.read().lower()
        allText += thisText
        thisFile.close()
    #print(len(allText))
    #print("No Errors.")
    return 0



main()
