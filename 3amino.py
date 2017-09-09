from __future__ import division 
import re
import sys
import nltk
import operator

# Modified by Hyun-Seok Park 07-22-17

# Input: BED and FASTA file
# Output: Trigram counts

##################### READ BED FILE ################################
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

chunk_objs = (slice(int(start), int(stop)) for chrom, start, stop in chr_start_stop)

bf.close()

print "#Step 4: READ FA FILE"

f = open('chr1.fa') # chrx.fa file extension here  #~250 MB

print "#Step 5: format .fa file"
def formatFa(faFile):
	faFile = faFile.read()
	faFile = faFile.lower() 
	faFile = re.sub(r'^.{5}', '', faFile) #ignore the title
	formatted_fa = re.sub(r'[^natcg]', '', faFile) #delete unwanted chars
	return formatted_fa

my_format = formatFa(f)
print my_format[10000:10600]

f.close()

print "Step 6: ######### TRIGRAMS ###########"

my_trigrams = (''.join(x) for x in nltk.trigrams(my_format))

def makeTrigramDict(trigrams):
	countsDict = nltk.defaultdict(int) #define counts
	for elem in trigrams:
		countsDict[elem] +=1  #make a dictionary, key=trigram, value=count
	return countsDict

countsDict = makeTrigramDict(my_trigrams)

countsTups = sorted(countsDict.items(), key=operator.itemgetter(1), reverse=True) 
#print countsTups 
