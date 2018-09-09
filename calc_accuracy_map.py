# coding: utf-8

# In[1]:

# unit test code
# cat out_calc_postprob_red.txt | python calc_accuracy_map.py | LANG=C sort > out_calc_accuracy_map.txt

import sys

# input comes from STDIN (standard input)
for line in sys.stdin:

    # Read Mapreduce1 output
    print('%s'%line.strip())
