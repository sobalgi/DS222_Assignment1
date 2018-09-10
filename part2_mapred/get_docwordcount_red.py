
# coding: utf-8

# unit test code
# cat out_get_docwordcount_map.txt | python get_docwordcount_red.py | LANG=C sort > out_get_docwordcount_red.txt
# cat unit_train.txt | python get_docwordcount_map.py | LANG=C sort | python get_docwordcount_red.py | LANG=C sort > out_get_docwordcount_red.txt

import sys

previous_doc_id = None
previous_word = None
current_word = None
previous_classlabels = None
doc_word_count = 0

# #uncomment to use dummy test file
# # read from test file
# with open("out_get_docwordcount_map.txt") as f:
#     raw_data = f.readlines()
# for line in raw_data:

# input comes from STDIN (standard input)
for line in sys.stdin:
    # Read get_classwordcount_map.py output data

    # remove leading and trailing whitespace
    data_str = line.strip()

    # parse the input we got from mapper.py
    try:
        key, val = data_str.split('\t', 1)
    except:  # indicates only class key, so count only class
        continue  # invalid key-value, got to next key-val

    current_doc_id, current_word = key.split(' ', 1)
    count_, current_classlabels = val.split(' ', 1)

    # update doc word count
    if current_doc_id == previous_doc_id and current_word == previous_word:
        doc_word_count += int(count_)  # increment the label count
    elif current_doc_id == previous_doc_id and not (current_word == previous_word):
        if previous_word:
            print('%s ~00_dummy_lbl %d\t%s %s'%(previous_word, doc_word_count, previous_doc_id, previous_classlabels))  # emit key-val for each class to find the class counts
            # for previous_classlabel in previous_classlabels.split(','):
            #     print('%s %s %d\t%s'%(previous_word, previous_classlabel, doc_word_count, current_doc_id)) # emit key-val for each class to find the class counts
        doc_word_count = int(count_)
        previous_word = current_word
    else:
        if previous_word:
            print('%s ~00_dummy_lbl %d\t%s %s'%(previous_word, doc_word_count, previous_doc_id, previous_classlabels))  # emit key-val for each class to find the class counts
            # for previous_classlabel in previous_classlabels.split(','):
            #     print('%s %s %d\t%s'%(previous_word, previous_classlabel, doc_word_count, current_doc_id))  # emit key-val for each class to find the class counts
        doc_word_count = int(count_)
        previous_doc_id = current_doc_id
        previous_word = current_word
        previous_classlabels = current_classlabels

# print the last word count
print('%s ~00_dummy_lbl %d\t%s %s'%(previous_word, doc_word_count, current_doc_id, previous_classlabels))
# for previous_classlabel in previous_classlabels.split(','):
#     print('%s %s %d\t%s'%(previous_word, previous_classlabel, doc_word_count, current_doc_id))  # emit key-val for each class to find the class counts

# Send key-val as
# word ~00_dummy_lbl doc_word_count\tdoc_id classlabels
