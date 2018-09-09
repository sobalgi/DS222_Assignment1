# coding: utf-8

# In[1]:

# Prerequisite file command below : join out_get_docwordcount_red and out_get_modelparams_red to get the input file to this mapreduce
# cat out_get_docwordcount_red.txt out_get_modelparams_red.txt | LANG=C sort > out_docwordcount_modelparams.txt

# unit test code
# cat out_docwordcount_modelparams.txt | python calc_postprob_map.py | LANG=C sort > out_calc_postprob_map.txt

import sys

# input comes from STDIN (standard input)
for line in sys.stdin:

    # Read Mapreduce1 output
    print('%s'%line.strip())
