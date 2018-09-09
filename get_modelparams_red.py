
# coding: utf-8

# cat out_get_modelparams_map.txt | python get_modelparams_red.py | LANG=C sort > out_get_modelparams_map.txt
# cat out_get_classwordcount_red.txt | python get_modelparams_map.py | LANG=C sort | python get_modelparams_red.py | LANG=C sort > out_get_modelparams_red.txt

import sys
import numpy as np
#import math

# dummy initialization
label_count = 1
labelword_count = 1
vocablen = 1

# #uncomment to use dummy teset file
# # read from test file
# with open("out_get_modelparams_map.txt") as f:
#     raw_data = f.readlines()
# for line in raw_data:


# input comes from STDIN (standard input)
for line in sys.stdin:
    # Read get_modelparams_map.py output data

    # print('%s'%line.strip())

    # remove leading and trailing whitespace
    data_str = line.strip()

    # parse the input we got from mapper.py
    try:
        key, val = data_str.split('\t', 1)
    except:
        continue  # invalid key-value, got to next key-val

    with np.errstate(divide='ignore'):  # ignore divide by zero runtime warning
        # string processing

        key_tokens = key.split(' ')
        if len(key_tokens) == 1:
            vocablen = int(val)
        elif len(key_tokens) == 2:
            prior_key, label_key = key.split(' ', 1)
            if label_key == '00_total':
                label_count = int(val)
            else:
                print('--00_prior %s\t%f'%(label_key, np.log((int(val)) / (label_count))))
        elif len(key_tokens) == 3:
            cond_key, current_label, current_word = key.split(' ', 2)
            if current_word == '00_total':
                labelword_count = int(val)
                #print('01_cond %s 01_UNK\t%f'%(current_label, np.log(1 / (labelword_count + vocablen))))  # add unknown word probability
                #print('01_UNK %f\t%s'%(np.log(1 / (labelword_count + vocablen)), current_label))  # add unknown word probability
                print('-01_UNK %s\t%f'%(current_label, np.log(1 / (labelword_count + vocablen))))  # add unknown word probability
            else:
                #print('01_cond %s %s\t%f'%(current_label, current_word, np.log((int(val) + 1) / (labelword_count + vocablen))))
                #print('%s %f\t%s'%(current_word, np.log((int(val) + 1) / (labelword_count + vocablen)), current_label))
                print('%s %s\t%f'%(current_word, current_label, np.log((int(val) + 1) / (labelword_count + vocablen))))  # add unknown word probability

        else:
            raise(IndexError)

        # Send key-val as
        # 00_prior prior_prob \t label
        # 01_UNK   cond_prob  \t label
        # word     cond_prob  \t label
        #
        # to facilitate dictionary creation
