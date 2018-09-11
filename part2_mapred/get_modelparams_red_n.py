
# coding: utf-8

# unit test code
# cat unit_train.txt | python get_classwordcount_map.py | LANG=C sort | python get_classwordcount_red.py | LANG=C sort > out_get_classwordcount_red.txt
# cat out_get_classwordcount_map.txt | python get_classwordcount_red.py | LANG=C sort > out_get_classwordcount_red.txt

import sys

previous_word = None
previous_label = None
current_word = None
current_label = None
previous_vocab_word = None
label_count = 0
labelword_count = 0

total_label_count = 0
total_labelword_count = 0


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
        entity_key, current_label = key.split(' ', 1)
        # update label count
        if current_label == previous_label:
            label_count += int(val)  # increment the label count
        else:
            if previous_label:
                # write result to STDOUT
                #print(f'{previous_label}\t{label_count}')  # emit (key, val) = (label, count)
                print('01lbl %s\t%d'%(previous_label, label_count))  # emit (key, val) = (label, count)
                total_label_count += label_count

                
            label_count = int(val)
            previous_label = current_label

            # print('%s %s\t%f'%(prior_key, label_key, math.log((int(val)) / (label_count))))
    elif len(key_tokens) == 3:
        
        if total_label_count != 0:
            # print last class count
            print('01lbl %s\t%d' % (previous_label, label_count))  # emit (key, val) = (label, count)
            total_label_count += label_count

            # print last class count
            # print('01lbl %s\t%d' % (previous_label, label_count))  # emit (key, val) = (label, count)rint total count of class
            print('01lbl -total\t%d' % (total_label_count))  # emit (key, val) = (totallabelcount, total_label_count)
            total_label_count = 0
            previous_label = None

        
        entity_key, current_label, current_word = key.split(' ', 2)

        if previous_label == current_label and previous_word == current_word:
            labelword_count += int(val)
        elif previous_label == current_label and not (previous_word == current_word):
            print('02wrd %s %s\t%d'%(previous_label, previous_word, labelword_count))  # emit (key, val) = (label word, count)
            
            if not(previous_vocab_word == previous_word):
                print('00vocab %s\t1'%previous_word)  # to find vocab count in final reducer
                previous_vocab_word = previous_word

            
            
            total_labelword_count += labelword_count
            labelword_count = int(val)
            previous_word = current_word
        else:
            if previous_word:
                print('02wrd %s %s\t%d'%(previous_label, previous_word, labelword_count))  # emit (key, val) = (label word, count)
                total_labelword_count += labelword_count
                print('00vocab %s\t1'%previous_word)  # to find vocab count in final reducer

            else:
                previous_label = None


            if previous_label:
                print('02wrd %s -total\t%d'%(previous_label, total_labelword_count))  # emit (key, eval) = (label word, count)

            previous_label = current_label
            previous_word = current_word
            labelword_count = int(val)
            total_labelword_count = 0  # reset counter for current_label
    else:
        raise IndexError

# print last word
print('02wrd %s %s\t%d'%(previous_label, previous_word, labelword_count))  # emit (key, val) = (label word, count)

# print word count for last label
print('02wrd %s -total\t%d'%(previous_label, total_labelword_count))  # emit (key, val) = (label word, count)

# total_label_count += label_count

# print the last word into vocab
print('00vocab %s\t1'%previous_word)  # to find vocab count in final reducer

