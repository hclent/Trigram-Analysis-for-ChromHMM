#updated 12-30-2015
from __future__ import division #percentages
import sys # for output
import nltk # for trigrams
from operator import itemgetter #for tuples
from math import log, exp, expm1
from decimal import Decimal, getcontext
import plotly
import plotly.plotly as py
from plotly.tools import FigureFactory as FF
py.sign_in('hclent', 'eeg49e9880')
import numpy as np
import re


###### INPUTTING A PRE-FORMATTED BED FILE ##########
gm12878 = open('Gm12878.txt') # Converted cell line file here
def preprocessing(cell):
	raw = cell.read()
	#print raw #fd8b7bab9a
	chars = []
	for line in raw:
		for c in line:
			chars.append(c)
	chars.pop() #delete '\n' off the end
	return chars

chars = preprocessing(gm12878) #fd8b7bab9a
#print chars ['f' 'd' , '8']

###########################################

def makeTrigrams(elements):
	the_trigrams = [] #list of tuples
	for trigrams in nltk.trigrams(elements): #make trigrams
		the_trigrams.append(trigrams)

	collapsed = []
	for bits in the_trigrams: #collapse
		collapsed.append( (''.join([w+'' for w in bits])).strip()) #strip ('f','d','8') to ('fd8')
	
	return collapsed 

my_trigrams = makeTrigrams(chars) #['fd8', 'd8b', '8b7', 'b7b', '7ba'...]
print my_trigrams


def makeTrigramDict(trigrams):
	countsDict = nltk.defaultdict(int) #define counts
	for elem in trigrams:
		countsDict[elem] +=1  #make a dictionary, key=trigram, value=count
	return countsDict

countsDict = makeTrigramDict(my_trigrams)


countsTups = sorted(countsDict.items(), key=itemgetter(1), reverse=True) 
print countsTups


def generateAllGrams(): #list of strings #all possible trigrams
	first_n = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
	second_n = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
	third_n = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

	grams = [] #get all possible results
	for x in first_n:
		for y in second_n:
			for z in third_n:
				xyz = x + y + z
				grams.append(xyz)
	return grams

all_grams = generateAllGrams()


#Need zeros for trigram table
#All possible results - seen results = zeros 
def getZeros():
	non_zeros = [x[0] for x in countsTups] #anything that is in results #doesn't have ebb
	just_zeros = (set(all_grams)) - (set(non_zeros)) # has ebb
	return just_zeros

just_zeros = getZeros() #type set


def makeZeroDict():
	zero_countsDict = nltk.defaultdict(int) #define counts
	for elem in just_zeros:
		zero_countsDict[elem] == 0  #make a dictionary, key=trigram, value=count
	return zero_countsDict

zero_countsDict = makeZeroDict()


# def makeOneDictionary(counts,zeros): #combine counts dictionary and zero dictionary 
# 	d = counts.copy()
# 	d.update(zeros)
# 	return d

allDict = makeOneDictionary(countsDict, zero_countsDict)
#print allDict # 1 6 0 6

total = sum(allDict.values()) #get total number for percentages #571337
#print total

def getTuples(counts, zeros):
	new_tuples = [] #initialize list make zeros into tuples
	for zeros in zeros:
		new = (zeros, 0)
		new_tuples.append(new)

	everything = counts + new_tuples 

	all_tuples = sorted(everything, key=itemgetter(0)) #sort from 111-fff #list of tuples
	return all_tuples

allTups = getTuples(countsTups, just_zeros)


def makePercentDict():
	decimalDict = nltk.defaultdict(lambda: 0) # 1 6 0 6 
	exponentDict = nltk.defaultdict(lambda: 0) # 1 6 0 6 
	lnDict = nltk.defaultdict(lambda: 0) # 1 6 0 6 
	
	getcontext().prec = 20
		
	for gram in allDict:
 		if allDict.has_key(gram):
 			value = allDict.get(gram)
 			new_value = Decimal((float(value) / float(total)))
 			#gram 6a6, count 1
 			#print new_value #prints full decimal 0.000001750280482447312181777129785048053950645590955950691

 			exponents = expm1(new_value) #prints with exponenets 1.75028201419e-06
 			
 			#logged_value = log(float(new_value)) #Math Domain Error #because log(0)
 			if new_value == 0:
 				logged_value = "Undefined"
 			else:
 				logged_value = Decimal(new_value).ln() #log

 			decimalDict[gram] = new_value
 			exponentDict[gram] = exponents
 			lnDict[gram] = logged_value
 			
 	return decimalDict, exponentDict, lnDict

decimalDict, exponentDict, lnDict = makePercentDict()



# #z in upside down..
# z = [[1, 9, 3],  #row ac
#      [15, 4, 5], #row ab
#      [0, 9, 8]]  #row aa


# x = ['a', 'b', 'c'] 
# y = ['ac', 'ab', 'aa'] #UPSIDE DOWN >:( (aa at top)

# z_text = [['aca', 'acb', 'acc'],  #Z text is upside down
#           ['aba', 'abb', 'abc'],
#           ['aaa', 'aab', 'aac']]

# # z_text = ['0.0 %', '0.0 %', '0.0 %'], #row aa
# # 		['0.011675492805095755 %', '1.7502957999455144e-05 %', '6.651287021587147e-05 %'], #row ab
# #	['2.275390513798777e-05 %', '2.275390513798777e-05 %', '0.0 %']]

# #aba = 0.011675492805095755
# #'abb': 1.7502957999455144e-05
# #'abc': 6.651287021587147e-05

# fig = FF.create_annotated_heatmap(z, x=x, y=y, annotation_text=z_text, colorscale='Viridis')
# py.iplot(fig, filename='annotated_heatmap_text')


###################################

#TO-DO LIST
# 3: dict with percentages
# 4: make a table!

############GRAVEYARD###########
#sys.stdout = open("RENAME ME RENAME ME RENAME ME RENAME ME RENAME ME.txt", "w")