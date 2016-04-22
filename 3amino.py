from __future__ import division 
import re
import sys
import nltk
from operator import itemgetter 

# Input: BED and FASTA file
# Output: Trigram counts

##################### READ BED FILE ################################
bf = open('wgEncodeBroadHmmHuvecHMM.bed') # Encode.bed file extension here

#Step 1: formal bedFile   #~40 MG
def formatBed(bedFile):
	bedFile = bedFile.read() 
	bedFile = bedFile.lower() #lowercase 
	format_bedFile = bedFile.splitlines()
	format_bedFile = [re.sub(r'\t', ' ', format_bedFile) for format_bedFile in format_bedFile] #replace \t with whitespace
	return format_bedFile 


my_bed = formatBed(bf)


#Step 2: (get names), starts, and stop
def getChromInfo(bedFile):
	datas =[]
	chr_start_stop = [] 

	for lines in bedFile:
 		datas.append(lines.strip().split(' ')) 
	for datas in datas:
		chr_start_stop.append(datas[0:3]) #grab first three things #chrom #start #stop

	return chr_start_stop

chr_start_stop = getChromInfo(my_bed)


#Step 3: makeIndicies with start stops for list of slice objects
def makeIndicies(bedFile, chromInfo):
	chunks = [] # list of slice objects [slice(num,num,None)]

	for chrom, start, stop in chromInfo: #unpack
		chunks.append(slice(int(start), int(stop))) #makes a slice object

	return chunks

chunk_objs = makeIndicies(my_bed, chr_start_stop)

bf.close()


##################### READ FA FILE #############################

f = open('chr1.fa') # chrx.fa file extension here  #~250 MB

#Step 4: format .fa file
def formatFa(faFile):
	faFile = faFile.read()
	faFile = faFile.lower() 
	faFile = re.sub(r'^.{5}', '', faFile) #ignore the title
	formatted_fa = re.sub(r'[^natcg]', '', faFile) #delete unwanted chars
	return formatted_fa

my_format = formatFa(f)


# Using a SMALL sample here for an example 
sample = my_format[10000:10600] # 
sample = list(sample)



# SLOW 
# takes result of makeIndicies and result of formatFa
# def getResults(indicies,faFormat):

# 	chunks = [] #initialize empty list
# 	for c in indicies: #start_stop slice objects can extract stuff from chunk windows
# 		chunks.append(faFormat[c]) #matches
# 	sample = list(chunks[:600])
# 	print sample

#
#chars = getResults(chunk_objs, my_format) # ['a' 't' 'c' 'g']


f.close()

############################## TRIGRAMS #######################
def makeTrigrams(elements): #takes a list
	the_trigrams = [] #list of tuples 
	for trigrams in nltk.trigrams(elements): #make trigrams
		the_trigrams.append(trigrams)

	collapsed = []
	for bits in the_trigrams: #collapse
		collapsed.append( (''.join([w+'' for w in bits])).strip()) #strip ('a','t','g') to ('atc')
	
	return collapsed 

my_trigrams = makeTrigrams(sample) #['atg', 'atc', 'atc' ...]


def makeTrigramDict(trigrams):
	countsDict = nltk.defaultdict(int) #define counts
	for elem in trigrams:
		countsDict[elem] +=1  #make a dictionary, key=trigram, value=count
	return countsDict

countsDict = makeTrigramDict(my_trigrams)


countsTups = sorted(countsDict.items(), key=itemgetter(1), reverse=True) 
print countsTups 