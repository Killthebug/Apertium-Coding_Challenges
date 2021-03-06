# !/usr/bin/python
# -*- coding : utf-8 -*-

# To run : python3 filename.py monolingual.dix

import sys
import os
import platform
from lxml import etree

def getTree(fileName):
    return etree.parse(fileName)

def extract(prop):
    """
    When sent a single indexed dictionary
    returns the value stored at the key : 'n'
    """
    try:
        return prop['n']
    except KeyError:
        return None

def extractLemma(word):
    """
    When sent a single indexed dictionary
    returns the value stored at the key : 'lm'
    """
    try:
        return word['lm']
    except KeyError:
        return None

def main():
    parList = []
    attributeList = []
    infoList = []

    """
    The paradigm table is a dictionary which stores
    the mapping of each paradigm to it's various
    rules/definitions
    """

    paradigmTable = {}
    
    for paradigm, pardef in zip(pars, parPath):
        parList.append(paradigm)                #List of paradigms                                    
        
        dataList = []
        for element in pardef:
            tempList = []
            
            for pairs in element :

                #debug statement
                
                for tags in pairs:
                    
                    if tags.tag == 'l':
                        if str(tags.text) == None: leftTag = ""
                        else: leftTag = tags.text
                    
                    if tags.tag == 'r':
                        if str(tags.text) == None: rightTag = ""
                        else: rightTag = tags.text
                    
                        infoList = []
                        
                        for properties in tags:
                            prop = extract(properties.attrib)
                            infoList.append(prop)       #infoList stores the variius attributes
                        
                        tempList.append(leftTag)
                        tempList.append(rightTag)
                        tempList.append(tuple(infoList))

                if 'n' in pairs.attrib:                 # This takes of nested paradigm entries
                    tempList.append(pairs.attrib['n'])
                
            dataList.append(tempList)
        paradigmTable[paradigm] = dataList
    
    """
    tripletList is a list of 3-tuples.
    (lemma, base form, paradigm)
    """
    tripletList = generateTriplets()         
    
    """
    generateEverything is the main function
    responsible for mapping and generating
    the various surface forms for a given lemma
    """

    generateEverything(tripletList, paradigmTable)

def generateTriplets():
    
    """
    This function takes a monolingual dictionary
    and generates a list of 3-tuples in the order
    (lemma, base form, paradigm)
    """
    
    tripletList = []

    for word in words:
        lemma = extractLemma(word.attrib)
        surface = ""
        paradigm = ""
        
        for tags in word:
           
            if tags.tag == 'i':
                if not tags.text:
                    surface = ""
                else:
                    surface = tags.text
            
            if tags.tag == 'par':
                if not extract(tags.attrib):
                    paradigm = ""
                else:
                    paradigm = extract(tags.attrib)

        triplet = (lemma, surface, paradigm)
        tripletList.append(triplet)

    return tripletList

def generateEverything(tripletList, paradigmTable):
    """
    The primary function in the script
    responsible for generating all the possible
    surface forms for a lemma, given it's
    surface form and paradigm. Also generates the
    lexical units corresponding to each surface form.
    """
    
    for triplet in tripletList:
        lemma = triplet[0]
        base = triplet[1]
        paradigm = triplet[2]
        print ("\nLemma : " + str(lemma))

        try:
            forms = paradigmTable[paradigm]
        except KeyError:
            forms = []

        for form in forms:
            try:
                if form[0] == None:
                    add = ""
                else:
                    add = form[0]
            except IndexError:
                add = ""
            word = base+add
            
            try:
                for prop in form[2]:
                    if prop:
                        try :
                            lemma = lemma + "." +  prop
                        except TypeError:
                            lemma = ""
            except IndexError:
                lemma = ""

            print ("Surface form : " + str(word) + " | Lexical unit: " + str(lemma) + " | Paradigm : "+paradigm)
            
            if len(form) == 4:                                                      # Checks for the presence of a nested paradigm
                if len(base) > 0:                                                   # Prevents empty entries from moving ahead
                    nestedPar(word, triplet[0], paradigmTable, form[3])             # Generated all possible forms
            
            lemma = triplet[0]

def nestedPar(base, lemma, paradigmTable, paradigm):
        """
        This fucnction takes care of nested paradigms
        and recursively generates all possible surface forms
        and lexical forms for nested paradigms
        """
        
        rawLemma = lemma
        
        try:
            forms = paradigmTable[paradigm]
        except KeyError:
            forms = []

        for form in forms:
            try:
                if form[0] == None:
                    add = ""
                else:
                    add = form[0]
            except IndexError:
                add = ""
            word = base+add
            
            try:
                for prop in form[2]:
                    if prop:
                        try :
                            lemma = lemma + "." +  prop
                        except TypeError:
                            lemma = ""
            except IndexError:
                lemma = ""
            
            print ("Surface form : " + str(word) + " | Lexical unit: " + str(lemma) + " | Paradigm : "+paradigm)
            
            if len(form) == 4:
                if len(word) > 0:
                    nestedPar(word, rawLemma, paradigmTable, form[3])
           
            lemma = rawLemma


if __name__ == '__main__':
   
    pyVersion = platform.python_version()

    if pyVersion < str(3.2):
        print >> sys.stderr, 'Python version not supported'
        print >> sys.stderr, 'Please use Python3.2 or higher'

    if len(sys.argv) != 2:
        print ("To use : python3 <filename>.py <monolingualDix>.dix")
        exit(1)
    
    fileName = sys.argv[1]
    
    if not os.path.isfile(fileName):
        print ("Passed file does not exists")
        exit(1)

    try:
        tree = getTree(fileName)
    except:
        print ("Not a valid monolingual dictionary")
        exit(1)

    root = tree.getroot()
    
    words = tree.xpath('/dictionary/section/e')

    pars = tree.xpath('/dictionary/pardefs/pardef/@n')
    parPath = tree.xpath('/dictionary/pardefs/pardef')
    rightSub = tree.xpath('/dictionary/pardefs/pardef/e/p/r')
    leftSub = tree.xpath('/dictionary/pardefs/pardef/e/p/l')
    pPath = tree.xpath('/dictionary/pardefs/pardef/e/p')
    ePath = tree.xpath('/dictionary/pardefs/pardef/e')
    
    main()
