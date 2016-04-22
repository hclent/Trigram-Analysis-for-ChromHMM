
from __future__ import division
import re
import sys
#Input: ChromHMM BED file
#Output: File containing all promoter types coded as 1-9a-f 
#Use: Feed to trigram_table.py 


gm12878 = open('wgEncodeBroadHmmGm12878HMM.bed') #Encode.bed file extension here


def format(hmmCellLine):

	hmmCellLine = hmmCellLine.read()
	hmmCellLine = hmmCellLine.lower() 
	hmmCellLine = hmmCellLine.splitlines()
	format = [re.sub(r'\t', ' ', hmmCellLine) for hmmCellLine in hmmCellLine] #replace tabs 
	return format

my_bed = format(gm12878)



def getCellType(bedFile):
	datas =[]
	cell_types = []
	cells_format = []

	for line in bedFile:
		datas.append(line.strip().split(' '))

	for datas in datas:
	 	cell_types.append(datas[3]) #append promoter type
	#print cell_types

	cells_format = ' '.join(cell_types)
	
	return cells_format #type str

working_format = getCellType(my_bed)



def doRegex121f(formattedBedFile): #convert promoter type to symbol for trigram analysis

	converted = []
	converted = re.sub(r'\D', ' ',  formattedBedFile)
	converted = re.sub(r'\D1\D', '1', converted) # Active Promoter
	converted = re.sub(r'\D2\D', '2', converted) # Weak Promoter
	converted = re.sub(r'\D3\D', '3', converted) # Poised Promoter
	converted = re.sub(r'\D4\D', '4', converted) # Strong Enhancer
	converted = re.sub(r'\D5\D', '5', converted) # Strong Enhancer
	converted = re.sub(r'\D6\D', '6', converted) # Weak Enhancer
	converted = re.sub(r'\D7\D', '7', converted) # Weak Enhancer
	converted = re.sub(r'\D8\D', '8', converted) # Insulator
	converted = re.sub(r'\D9\D', '9', converted) # Txn Transition
	converted = re.sub(r'1{1}0{1}', 'a', converted) #Txn Enlongation
	converted = re.sub(r'1{2}', 'b', converted) # Weak txn
	converted = re.sub(r'1{1}2{1}', 'c', converted) # Repressed
	converted = re.sub(r'1{1}3{1}', 'd', converted) # Heterochrom/lo
	converted = re.sub(r'1{1}4{1}', 'e', converted) # Repetitive/CNV
	converted = re.sub(r'1{1}5{1}', 'f', converted) # Repetitive/CNV

	#converted has lots of whitespace

	final = []
	final = re.sub(r'\s', '', converted)
	return final

final = doRegex121f(working_format)


#sys.stdout = open("Gm12878.txt", "w")
#print final
#Huvev: o m h g e g k j k... #CORRECT!!!!! 


gm12878.close()