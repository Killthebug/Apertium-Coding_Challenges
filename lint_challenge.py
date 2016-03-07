#!/usr/bin/python

import re
import sys
from itertools import groupby

def extractBetween(line, start, end):
    """
    Extract substring between two strings
    """
    try:
        head = line.index(start) + len(start)
        tail = line.index(end, head)
        return line[head:tail]
    except ValueError:
        return ""

def printList(List):
    for iterator in List:
        print "Lemma : "+ iterator[0]+ " Surface : "+ iterator[1]+ " Paradigm : "+iterator[2]

def main():
    lines = []
    result = []
    dix = sys.argv[1]
    pattern = re.compile(r'<e lm=.*</e>')
   
    #Filter the lines that we need to extract info from
    with open(dix) as myFile:
        for match, y in groupby(myFile, key=lambda m:pattern.search(m)):
            if match:
                lines.append(''.join(list(y)))

    #Parse each line and extract information
    for line in lines:
        lemma = extractBetween(line, 'lm="', '">')
        surface = extractBetween(line, '<i>', '</i>')
        if surface == '':
            surface = extractBetween(line, '<b/>', '</l>')
        surface = surface.replace("<b/>", " ")
        paradigm = extractBetween(line, '<par n="', '"/>')
        temp = (lemma, surface, paradigm)
        result.append(temp)
    
    printList(result)
    exit(1)

if __name__ == '__main__':
    main()
