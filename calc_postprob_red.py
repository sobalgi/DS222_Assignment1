
# coding: utf-8

# unit test code
# cat out_calc_postprob_map.txt | python calc_postprob_red.py | LANG=C sort > out_calc_postprob_red.txt

import sys

previous_word = None
current_word = None
prior_prob_dict = {}
UNK_cond_prob_dict = {}
word_cond_prob_dict = {}

# #uncomment to use dummy test file
# #read from test file
# with open("devel_postprob_man.txt") as f:  # out_calc_postprob_map
#    raw_data = f.readlines()
# for line in raw_data:

# input comes from STDIN (standard input)
for line in sys.stdin:
    # Read combined output data from red2_new and model_params from STDIN using identity mapper

    try:
        key, val = line.strip().split('\t', 1)
    except ValueError:
        continue

    key_tokens = key.split(' ')
    # if key_tokens[1] == 'Villages_in_Turkey':
    #     print(key)

    if len(key_tokens) == 2:  # processing from modelparams.txt
        entity_key, label_key = key.split(' ', 1)
        if entity_key == '00_prior':
            prior_prob_dict[label_key] = float(val)  # add to prior dictionary
            if prior_prob_dict[label_key] >= 0:
                raise ValueError
            print('-prior %s\t%f' %(label_key, prior_prob_dict[label_key]))

        elif entity_key == '01_UNK':
            UNK_cond_prob_dict[label_key] = float(val)  # add to conditional dictionary for UNK words
            if UNK_cond_prob_dict[label_key] >= 0:
                raise ValueError
        else:
            if float(val) >= 0:
                raise ValueError

            if previous_word is None or not(previous_word == entity_key):
                word_cond_prob_dict = UNK_cond_prob_dict.copy()  # initialize the cond prob dict for the word
                word_cond_prob_dict[label_key] = float(val)  # get cond prob for the current word

                previous_word = entity_key
            else:  # update known class word prob word
                word_cond_prob_dict[label_key] = float(val)  # get cond prob for the current word

    elif len(key_tokens) == 3:
        current_word, dummy_label, current_count = key.split(' ', 2)
        if not(previous_word == current_word):
            word_cond_prob_dict = UNK_cond_prob_dict.copy()  # initialize the cond prob dict for the word


        val_tokens = val.split(' ')
        current_doc_id = val_tokens[0]
        original_labels = val_tokens[1]

        for dict_label, dict_value in word_cond_prob_dict.items():
            print('%s %s\t%f %s' % (current_doc_id, dict_label, dict_value * int(current_count),
                                    original_labels))  # emit key-val for each class to find the class counts

        previous_word = current_word

    else:
        pass
        # raise (IndexError)


