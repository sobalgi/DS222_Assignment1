
# coding: utf-8

# unit test code
# cat unit_test.txt | python get_classwordcount_map.py | LANG=C sort | python get_classwordcount_red.py | LANG=C sort > out_get_classwordcount_red.txt
# cat out_get_classwordcount_map.txt | python get_classwordcount_red.py | LANG=C sort > out_get_classwordcount_red.txt

import sys

previous_word = None
previous_label = None
current_word = None
current_label = None
label_count = 0
labelword_count = 0

total_label_count = 0
total_labelword_count = 0

vocab = []  # set for vocabulary

# #uncomment to use dummy test file
# # read from test file
# with open("out_get_classwordcount_map.txt") as f:
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

    key_tokens = key.split(' ')
    if len(key_tokens) == 2:
        _, current_label = key.split(' ', 1)
        # update label count
        if current_label == previous_label:
            label_count += int(val)  # increment the label count
        else:
            if previous_label:
                # write result to STDOUT
                #print(f'{previous_label}\t{label_count}')  # emit (key, val) = (label, count)
                print('-02_prior %s\t%d'%(previous_label, label_count))  # emit (key, val) = (label, count)
                total_label_count += label_count

            label_count = int(val)
            previous_label = current_label

            # print('%s %s\t%f'%(prior_key, label_key, math.log((int(val)) / (label_count))))
    elif len(key_tokens) == 3:
        _, current_label, current_word = key.split(' ', 2)

        if previous_label == current_label and previous_word == current_word:
            labelword_count += int(val)
        elif previous_label == current_label and not (previous_word == current_word):
            print('03_cond %s %s\t%d'%(previous_label, previous_word, labelword_count))  # emit (key, val) = (label word, count)

            if previous_word not in vocab:
                vocab.append(previous_word)

            total_labelword_count += labelword_count
            labelword_count = int(val)
            previous_word = current_word
        else:

            if previous_word:
                print('03_cond %s %s\t%d'%(previous_label, previous_word, labelword_count))  # emit (key, val) = (label word, count)
                total_labelword_count += labelword_count

                if previous_word not in vocab:
                    vocab.append(previous_word)
            else:
                previous_label = None

            if previous_label:
                print('03_cond %s 00_total\t%d'%(previous_label, total_labelword_count))  # emit (key, val) = (label word, count)

            previous_label = current_label
            previous_word = current_word
            labelword_count = int(val)
            total_labelword_count = 0  # reset counter for current_label
    else:
        raise (IndexError)

if previous_word not in vocab:
    vocab.append(previous_word)

# print last word
print('03_cond %s %s\t%d'%(previous_label, previous_word, labelword_count))  # emit (key, val) = (label word, count)
total_labelword_count += labelword_count

# print word count for last label
print('03_cond %s 00_total\t%d'%(previous_label, total_labelword_count))  # emit (key, val) = (label word, count)

# print last class count
print('-02_prior %s\t%d' % (previous_label, label_count))  # emit (key, val) = (label, count)
total_label_count += label_count

# print total count of class
print('-02_prior 00_total\t%d' % (total_label_count))  # emit (key, val) = (totallabelcount, total_label_count)

# write vocabulary size
print('--01_vocablen\t%d'%(len(vocab)))  # emit (key, val) = (vocabsize, count)
