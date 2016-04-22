# Updated 11-5-15
# Heather Lent
# Ewha Information and Telecommunications Institute
# Ewha Womans University
# Human Language Technology Program
# Department of Linguistics, University of Arizona
###############################################################
# SLOW RUN TIME 
from __future__ import division
import re
import sys
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

	# start_stop = [] #for just start stop
	# for chrom, start, stop in chr_start_stop: #unpack
	# 	ss = [int(start.strip()),int(stop.strip())]
	# 	for pair in ss:
	# 		start_stop.append(ss)

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

f = open('chr1.fa') # chrx.fa file extension here  #254.2 MB

#Step 4: format .fa file
def formatFa(faFile):
	faFile = faFile.read()
	faFile = faFile.lower() 
	faFile = re.sub(r'^.{5}', '', faFile) #ignore the title
	formatted_fa = re.sub(r'[^natcg]', '', faFile) #delete unwanted chars
	return formatted_fa

my_format = formatFa(f)


#takes result of makeIndicies and result of formatFa
def getResults(indicies,faFormat):

	chunks = [] #initialize empty list
	for c in indicies: #start_stop slice objects can extract stuff from chunk windows
		chunks.append(faFormat[c])

	# sys.stdout = open("Huvec_FASTA.fa", "w") #prints results to .txt
	# print chunks


	results_n = [] #intialize empty lists
	results_a = []
	results_t = []
	results_g = []
	results_c = []

	for chunk in chunks:
		denominator = len(chunk)
		
		answern = chunk.count('n') #count n
		answern = (answern / denominator) * 100 #make percent
		answern = str(answern) + "%" #make pretty
		results_n.append(answern)

		answera = chunk.count('a')
		answera = (answera / denominator) * 100
		answera = str(answera) + "%"
		results_a.append(answera)

		answert = chunk.count('t')
		answert = (answert / denominator) * 100
		answert = str(answert) + "%"
		results_t.append(answert)

		answerg = chunk.count('g')
		answerg = (answerg / denominator) * 100
		answerg = str(answerg) + "%"
		results_g.append(answerg)

		answerc = chunk.count('c')
		answerc = (answerc / denominator) * 100
		answerc = str(answerc) + "%"
		results_c.append(answerc)

		#each window sums to 100% :) 

	my_results = zip(results_n, results_a, results_t, results_c, results_g)
	return my_results


my_results = getResults(chunk_objs, my_format)



#sys.stdout = open("Huvec_natgc_results.txt", "w") #prints results to .txt
#for result in my_results:
#		print str(('(n={}, a={}, t={}, g={}, c={})'.format(*result))) + "\n"

f.close()




