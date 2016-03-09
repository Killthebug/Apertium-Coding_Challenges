# !/usr/bin/python
# -*- coding : utf-8 -*-

# To run : python3 filename.py monolingual.dix

import sys
from lxml import etree

def getTree(fileName):
    return etree.parse(fileName)

def main():
    parList = []
    attributeList = []
    infoList = []
    
    fileName = sys.argv[1]
    tree = getTree(fileName)

    pars = tree.xpath('/dictionary/pardefs/pardef/@n')
    parPath = tree.xpath('/dictionary/pardefs/pardef')
    rightSub = tree.xpath('/dictionary/pardefs/pardef/e/p/r')
    leftSub = tree.xpath('/dictionary/pardefs/pardef/e/p/l')
    pPath = tree.xpath('/dictionary/pardefs/pardef/e/p')
    rePath = tree.xpath('/dictionary/pardefs/pardef/e/re')

    ePath = tree.xpath('/dictionary/pardefs/pardef/e')


    for par in pars:
        parList.append(pars)

    for par in parPath:
        for e in par:
            for p in e:
                for tags in p:
                    print (tags.tag)
    
    mainCounter = 0
    for par in parPath:
        tmpLen = len(par)
        mainCounter += tmpLen
       
    for lTags in leftSub:
        attributeList.append(lTags.text)

#Extract all the right sub tags
    for rTags in rightSub:
        temp = []
        for sTags in rTags:
            temp.append(sTags.attrib)
        infoList.append(temp)


    print (mainCounter)
    print (len(attributeList))
    print (len(infoList))
    print (len(pPath))
    print (len(rePath))
main()
