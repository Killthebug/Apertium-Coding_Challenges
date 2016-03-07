# !/usr/bin/python
# -*- coding : utf-8 -*-

# To run : python3 filename.py monolingual.dix

import sys
import xml.etree.ElementTree as etree

def filterData(result):
    """
    The data as extracted from the XML file
    is sent here, and the required info is 
    then filtered out.
    """
    for iterator in result:
        iterator[0] = "Lemma : "+next(iter(iterator[0].values()))
        
        if iterator[1]:
            iterator[1] = ", Surface : "+iterator[1]
        iterator[2] = ", Paradigm : "+next(iter(iterator[2].values()))
        
        print (iterator)

def getSurfaceForm(child):
    """
    Returns the Surface form if one exists
    """
    try:
        if child[0].text:
            temp = child[0].text
            res = True
        else:
            temp = None
            res = False
    
    except IndexError:
        temp = None
        res = False
    
    return (temp, res)

def getParadigm(child):
    """
    Returns the Paradigm if one exists and is found
    """
    try:
        if child[1].attrib:
            temp = child[1].attrib
            res = True
        else:
            temp = None
            res = False
    
    except IndexError:
        temp = None
        res = False
    
    return (temp, res)

def main():
    dix = sys.argv[1]
    tree = etree.parse(dix)
    root = tree.getroot()

    result = []

    noSurface, noParadigm = False, False

    for child in root[3]:
        temp = []

        lemma = child.attrib
        surface = getSurfaceForm(child)
        paradigm = getParadigm(child)
        
        temp = [lemma, surface[0], paradigm[0]]
        
        if lemma and surface[1] and paradigm[1] :
            result.append(temp)
    
    filterData(result)

if __name__ == '__main__':
    main()
