# coding: utf-8

# In[1]:

# Prerequisite file command below : join out_get_docwordcount_red and out_get_modelparams_red to get the input file to this mapreduce
# cat out_get_docwordcount_red.txt out_get_modelparams_red.txt | LANG=C sort > out_docwordcount_modelparams.txt

# unit test code
# cat out_docwordcount_modelparams.txt | python calc_postprob_map.py | LANG=C sort > out_calc_postprob_map.txt

import sys

# input comes from STDIN (standard input)
for line in sys.stdin:

    
    try:
        key, val = line.strip().split('\t', 1)
    except ValueError:
        continue

    key_tokens = key.split(' ')

    if len(key_tokens) == 2:  # processing from modelparams.txt
        print('%s'%line.strip())

    elif len(key_tokens) == 3:
        
        if key_tokens[2] == '-UNK-':
            
            print('-UNK- %s\t%s'%(key_tokens[1], val))

        else:
            if key_tokens[1] == '~00_dummy_lbl':

                print('%s'%line.strip())
            else:
                print('%s %s\t%s'%(key_tokens[2], key_tokens[1], val))


