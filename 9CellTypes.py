
from __future__ import division
import re
import sys
#Input: ChromHMM BED file
#Output: File containing all promoter types coded as 1-9a-f 
#Use: Feed to trigram_table.py 

gm12878 = open('wgEncodeBroadHmmGm12878HMM.bed') #Encode.bed file extension here

def format(hmmCellLine):

	hmmCellLine = hmmCellLine.read().splitlines()
	format = [re.sub(r'\t', ' ', hmmCellLine) for hmmCellLine in hmmCellLine] #replace tabs 
	return format

my_bed = format(gm12878)

def getCellType(bedFile):
        return (line.strip().split(' ')[3] for line in bedFile)

working_format = getCellType(my_bed)

encode15States = {
        "1_Active_Promoter":'1',
        "2_Weak_Promoter":'2', 
        "3_Poised_Promoter":'3', 
        "4_Strong_Enhancer":'4', 
        "5_Strong_Enhancer":'5', 
        "6_Weak_Enhancer":'6',
        "7_Weak_Enhancer":'7',
        "8_Insulator":'8', 
        "9_Txn_Transition":'9', 
        "10_Txn_Elongation":'a', 
        "11_Weak_Txn":'b', 
        "12_Repressed":'c', 
        "13_Heterochrom/lo":'d', 
        "14_Repetitive/CNV":'e', 
        "15_Repetitive/CNV":'f'
        }

final = [encode15States[key] for key in working_format]

#sys.stdout = open("Gm12878.txt", "w")
#print final
#Huvev: o m h g e g k j k... #CORRECT!!!!! 

gm12878.close()
