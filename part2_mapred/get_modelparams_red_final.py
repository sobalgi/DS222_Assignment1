
# coding: utf-8

# cat out_get_modelparams_map.txt | python get_modelparams_red.py | LANG=C sort > out_get_modelparams_map.txt
# cat out_get_classwordcount_red.txt | python get_modelparams_map.py | LANG=C sort | python get_modelparams_red.py | LANG=C sort > out_get_modelparams_red.txt

import sys
import numpy as np

# initialization
label_count = 0
labelword_count = 0

vocablen = 0
previous_word = None
previous_label = None
current_word = None
current_label = None
previous_vocab_word = None
label_count = 0
labelword_count = 0

total_label_count = 0
total_labelword_count = 0

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
        if len(key_tokens) == 2:
            entity_key, label_key = key.split(' ', 1)
            if entity_key == '00vocab':
                if not(previous_vocab_word == label_key):
                    vocablen += 1
                    print('_vocab %s'%label_key)  # store vocabulary words
                    previous_vocab_word = label_key
            else:
                current_label = label_key
                    
                if label_key == '-total':
                    total_label_count += int(val)
                else:
                    if previous_label == current_label:
                        label_count += int(val)
                    else:
                        if previous_label:
                            # print the prior prob of the label
                            print('01prior %s\t%f'%(previous_label, np.log((int(label_count)) / (total_label_count))))
                        previous_label = current_label
                        label_count = int(val)
        elif len(key_tokens) == 3:
            cond_key, current_label, current_word = key.split(' ', 2)
            
            if current_word == '-total':
                total_labelword_count += int(val)
                if previous_word:
                        print('02cond %s %s\t%f'%(previous_label, previous_word, np.log((int(labelword_count)+1) / (total_labelword_count+vocablen))))
                        print('02cond %s %s\t%f'%(previous_label, '-UNK-', np.log((1) / (total_labelword_count+vocablen))))

                precious_label = None
                previous_word = None
                    
            else:
                if previous_label == current_label and previous_word == current_word:
                    labelword_count += int(val)
                elif previous_label == current_label and not (previous_word == current_word):
                    print('02cond %s %s\t%f'%(previous_label, previous_word, np.log((int(labelword_count)+1) / (total_labelword_count+vocablen))))
            
                    labelword_count = int(val)
                    previous_word = current_word
                    total_labelword_count = 0
                else:
                    if previous_word:
                        print('02cond %s %s\t%f'%(previous_label, previous_word, np.log((int(labelword_count)+1) / (total_labelword_count+vocablen))))
                        print('02cond %s %s\t%f'%(previous_label, '-UNK-', np.log((1) / (total_labelword_count+vocablen))))

                    previous_label = current_label
                    previous_word = current_word
                    labelword_count = int(val)
                    total_labelword_count = 0  # reset counter for current_label
 
        else:
            raise IndexError

# print the prior prob of the label
print('01prior %s\t%f'%(previous_label, np.log((int(label_count)) / (total_label_count))))

print('02cond %s %s\t%f'%(previous_label, previous_word, np.log((int(labelword_count)+1) / (total_labelword_count+vocablen))))
print('02cond %s %s\t%f'%(previous_label, '-UNK-', np.log((1) / (total_labelword_count+vocablen))))

print('_vocablen %d'%vocablen)
            
        # Send key-val as
        # 01prior label\t prior prob
        # 02cond  label   word \t cond_prob
        # _vocab word
        # _vocablen 
        #
        # to facilitate dictionary creation
