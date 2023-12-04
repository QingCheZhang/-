###############################################################################
'''This parser takes as input the text files gtex_dataset.txt and 
gtex_sequence.txt, and produces a .h5 file datafile_{}_{}.h5,
which will be later processed to create dataset_{}_{}.h5. The file
dataset_{}_{}.h5 will have datapoints of the form (X,Y), and can be
understood by Keras models.'''
###############################################################################

import numpy as np
import re
import sys
import time
import h5py
from constants import *

start_time = time.time()

assert sys.argv[1] in ['train', 'test', 'all']
assert sys.argv[2] in ['0', '1', 'all']
print(sys.argv[2])

if sys.argv[1] == 'train':
    CHROM_GROUP = ['chr1', 'chr2', 'chr3', 'chr4', 'chr5']
elif sys.argv[1] == 'test':
    CHROM_GROUP = [ 'chr5']
else:
    CHROM_GROUP = ['chr1', 'chr2', 'chr3', 'chr4', 'chr5']

###############################################################################
print(CHROM_GROUP)
NAME = []      # Gene symbol
PARALOG = []   # 0 if no paralogs exist, 1 otherwise
CHROM = []     # Chromosome number
STRAND = []    # Strand in which the gene lies (+ or -)
TX_START = []  # Position where transcription starts
TX_END = []    # Position where transcription ends
JN_START = []  # Positions where gtex exons end
JN_END = []    # Positions where gtex exons start
SEQ = []       # Nucleotide sequence

fpr2 = open(sequence, 'r')

with open(splice_table, 'r') as fpr1:
    for line1 in fpr1:

        line2 = fpr2.readline()

        data1 = re.split('\n|\t', line1)[:-1]
        data2 = re.split('\n|\t|:|-', line2)[:-1]

        assert data1[2] == data2[0]
        assert int(data1[4]) == int(data2[1])+CL_max//2+1
        assert int(data1[5]) == int(data2[2])-CL_max//2

        if (data1[2] not in CHROM_GROUP):
            continue

        if (sys.argv[2] != data1[1]) and (sys.argv[2] != 'all'):
            continue

        NAME.append(data1[0])
        PARALOG.append(int(data1[1]))
        CHROM.append(data1[2])
        STRAND.append(data1[3])
        TX_START.append(data1[4])
        TX_END.append(data1[5])
        JN_START.append(data1[6::2])
        JN_END.append(data1[7::2])
        SEQ.append(data2[3])

fpr1.close()
fpr2.close()
# print(CHROM)
# print(JN_END)
# print(len(NAME))
print(type(NAME))
print(type(PARALOG))
print(type(CHROM))
print(type(STRAND))
print(type(TX_START))
print(type(TX_END))
print(type(JN_START))
print(type(JN_END))
print(type(SEQ))
###############################################################################

h5f = h5py.File(data_dir + 'datafile' 
                + '_' + sys.argv[1] + '_' + sys.argv[2]
                + '.h5', 'w')

h5f.create_dataset('NAME', data=NAME)
h5f.create_dataset('PARALOG', data=PARALOG)
h5f.create_dataset('CHROM', data=CHROM)
h5f.create_dataset('STRAND', data=STRAND)
h5f.create_dataset('TX_START', data=TX_START)
h5f.create_dataset('TX_END', data=TX_END)
h5f.create_dataset('JN_START', data=JN_START)
h5f.create_dataset('JN_END', data=JN_END)
h5f.create_dataset('SEQ', data=SEQ)
# NAME = h5f.create_group('NAME')
# NAME.create_dataset('NAME', data=np.asarray(NAME))
# PARALOG = h5f.create_group('PARALOG')
# PARALOG.create_dataset('PARALOG', data=np.asarray(PARALOG))
# CHROM = h5f.create_group('CHROM')
# CHROM.create_dataset('CHROM', data=np.array(CHROM)) 
# STRAND = h5f.create_group('STRAND')
# STRAND.create_dataset('STRAND', data=np.array(STRAND))
# TX_START = h5f.create_group('TX_START')
# TX_START.create_dataset('TX_START', data=np.array(TX_START))
# TX_END = h5f.create_group('TX_END')
# TX_END.create_dataset('TX_END', data=np.array(TX_END))
# JN_START = h5f.create_group('JN_START')
# JN_START.create_dataset('JN_START', data= np.array(JN_START))
# JN_END = h5f.create_group('JN_END')
# JN_END.create_dataset('JN_END', data=np.asarray(JN_END))
# SEQ = h5f.create_group('SEQ')
# SEQ.create_dataset('SEQ', data=np.array(SEQ)) 


h5f.close()
#print "--- %s seconds ---" % (time.time() - start_time)
print(f"--- {time.time() - start_time} seconds ---")


###############################################################################


