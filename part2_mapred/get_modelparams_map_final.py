# coding: utf-8

# In[1]:
# unit test code
# cat out_get_classwordcount_red.txt | python get_modelparams_map.py | LANG=C sort > out_get_modelparams_map.txt

import sys

# input comes from STDIN (standard input)
for line in sys.stdin:

    # Read Mapreduce1 output
    print('%s'%line.strip())
