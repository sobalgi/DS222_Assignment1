
# coding: utf-8

# unit test code
# cat out_calc_accuracy_map.txt | LANG=C sort | python calc_accuracy_red.py | LANG=C sort > out_calc_accuracy_red.txt  & cat out_calc_accuracy_red.txt

import sys
import numpy as np

previous_doc_id = None
previous_label = None
previous_labels = None
total_cond_prob = 0


# #uncomment to use dummy test file
# # read from test file
# with open("out_calc_accuracy_map.txt") as f:
#     raw_data = f.readlines()
# for line in raw_data:

# input comes from STDIN (standard input)
for line in sys.stdin:
    # Read combined output data from red2_new and model_params from STDIN using identity mapper

    try:
        key, val = line.strip().split('\t', 1)
    except ValueError:
        continue
    
    current_doc_id, current_label = key.split(' ',1)
    current_post_prob, current_labels = val.split(' ', 1)
    
    if previous_doc_id == current_doc_id and previous_label == current_label:
        total_cond_prob += float(current_post_prob)
    elif previous_doc_id == current_doc_id and not(previous_label == current_label):
        print('%s %s\t%f %s' % (previous_doc_id, previous_label, total_cond_prob, previous_labels))  # emit key-val for each class to find the class counts
        previous_label = current_label
        total_cond_prob = float(current_post_prob)
    else:
        if previous_doc_id:
            print('%s %s\t%f %s' % (previous_doc_id, previous_label, total_cond_prob, previous_labels))  # emit key-val for each class to find the class counts

        total_cond_prob = float(current_post_prob)
        previous_label = current_label
        previous_doc_id = current_doc_id
        previous_labels = current_labels

print('%s %s\t%f %s' % (previous_doc_id, previous_label, total_cond_prob, previous_labels))  # emit key-val for each class to find the class counts

