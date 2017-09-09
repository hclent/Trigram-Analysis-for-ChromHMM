# Updated 11-5-15
# Heather Lent
# Ewha Information and Telecommunications Institute
# Ewha Womans University
# Human Language Technology Program
# Department of Linguistics, University of Arizona

# Modified by Hyun-Seok Park, 7-21-17

from __future__ import division
import re
import sys

print "######READ BED FILE #####"
bf = open('wgEncodeBroadHmmHuvecHMM.bed') # Encode.bed file extension here

print "#Step 1: formal bedFile   #~40 MG"
def formatBed(bedFile):
	bedFile = bedFile.read() 
	format_bedFile = (re.sub(r'\t', ' ', format_bedFile) for format_bedFile in bedFile.lower().splitlines()) #replace \t with whitespace
	return format_bedFile 

my_bed = formatBed(bf)

print "#Step 2: (get names), starts, and stop"
def getChromInfo(bedFile):
	datas =[]
	chr_start_stop = [] 

	for lines in bedFile:
 		datas.append(lines.strip().split(' ')) 
	for datas in datas:
		chr_start_stop.append(datas[0:3]) #grab first three things #chrom #start #stop

	return chr_start_stop


chr_start_stop = getChromInfo(my_bed)


print "#Step 3: makeIndicies with start stops for list of slice objects"
def makeIndicies(bedFile, chromInfo):
	chunks = [] # list of slice objects [slice(num,num,None)]

	for chrom, start, stop in chromInfo: #unpack
		chunks.append(slice(int(start), int(stop))) #makes a slice object

	return chunks

chunk_objs = makeIndicies(my_bed, chr_start_stop)

chunk_objs2 = (slice(int(start), int(stop)) for chrom, start, stop in chr_start_stop)

bf.close()

print "###### READ FA FILE #########"

f = open('chr1.fa') # chrx.fa file extension here  #254.2 MB

#Step 4: format .fa file
def formatFa(faFile):
	faFile = faFile.read()
	faFile = faFile.lower() 
	faFile = re.sub(r'^.{5}', '', faFile) #ignore the title
	formatted_fa = re.sub(r'[^natcg]', '', faFile) #delete unwanted chars
	return formatted_fa

my_format = formatFa(f)

def getResultPerBED(indice, atgcString):
        subString = atgcString[indice]
        n = len(subString)
        return '(a={}, t={}, g={}, c={})'.format(subString.count('a') / n, subString.count('t') / n, subString.count('g') / n, subString.count('c') / n)

print "#takes result of makeIndicies and result of formatFa"

#my_results = (getResultPerBED(indice, my_format) for indice in chunk_objs)
my_results = [getResultPerBED(indice, my_format) for indice in chunk_objs]

f.close()




