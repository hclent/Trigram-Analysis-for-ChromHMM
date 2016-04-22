# Trigram-Analysis-for-ChromHMM
Uses trigrams to analyze the 9 Cell Lines from ENCODE's ChromHMM. Project for Bioinformatics lab at Ewha Woman's University in Summer 2015

README File
Heather Lent
Updated 2-15-2016
----------------------------

both_read.py

This program takes any .BED file as an input and collects the start-stop bp information for each line.


Then it takes an .FA file and extracts atgcn counts with the the start-stop bp information, and it returns the percent of atgcn for each window.

Sample of output:

(n=0.0%, a=29.1666666667%, t=15.6666666667%, g=48.6666666667%, c=6.5%)

(n=0.0%, a=16.7597765363%, t=6.14525139665%, g=30.9124767225%, c=46.1824953445%)

(n=0.0%, a=20.1666666667%, t=26.5%, g=25.8333333333%, c=27.5%)


-------------------------------------------

9CellTypes.py


This program takes .bed files and extracts the cell type from each line. 
For example the program would extract “15_Repetitive/CNV” from the line below:
(chr1	10000	10600	15_Repetitive/CNV	0	.	10000	10600	245,245,245)

Then the program converts the cell type into symbols (123456789abcdef)

- 1_Active_Promoter == 1
- 2_Weak_Promoter == 2
- 3_Poised_Promoter == 3
- 4_Strong_Enhancer == 4
- 5_Strong_Enhancer == 5
- 6_Weak_Enhancer == 6
- 7_Weak_Enhancer == 7
- 8_Insulator == 8
- 9_Txn_Transition == 9
- 10_Txn_Elongation == a
- 11_Weak_Txn == b
- 12_Repressed == c
- 13_Heterochrom/lo == d
- 14_Repetitive/CNV == e
- 15_Repetitive == f

Sample of output: 'fd8b7bab9a92123cdcd7b8d8d76d8d8d8ddc....'

This code is pre-processing for the 3promoters code, which does the trigram analysis

-------------------------------------------

3promoters.py

Takes the output of 9CellTypes.py and makes trigrams of the cell types, with counts.
For any 3grams that do not exist in the output of 9CellsTypes.py, a datapoint is made with the value “0”.

Example:
‘fd8b7bab9a’ becomes ['fd8', 'd8b', '8b7', 'b7b', '7ba']

And then the trigrams are counted. 

Sample of output: 'c3c': 2899, 'c3b': 1, '2a3': 0

This means that “12_Repressed, 2_Weak_Promoter, 12_Repressed” happens 2899 times,
but “2_Weak_Promoter, 10_Txn_Elongation, 3_Poised_Promoter” happens 0 times. 

The goal of this program is to take this information and make a transition table. 

-------------------------------------------

3amino.py

This code does trigram analysis for ATGC rather than for promoter types. 

