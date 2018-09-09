# coding: utf-8

# In[1]:

# unit test code
# cat unit_test.txt | python get_docwordcount_map.py | LANG=C sort > out_get_docwordcount_map.txt

import sys
import re

import nltk
nltk.data.path.append("/home/sourabhbalgi/nltk_data/")

#nltk.download('stopwords')
#nltk.download('punkt')
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# String preprocessing (stemming, stopword removal, tokenization)
stemmer = PorterStemmer()  # Porter Stemmer from NLTK
#stemmer = nltk.stem.SnowballStemmer('english')  # Snowball Stemmer from NLTK
#stemmer = nltk.stem.lancaster.LancasterStemmer()  # Lancaster Stemmer from NLTK
stop_words = set(stopwords.words('english'))  # remove stopwords in english


# # manual list of nltk stopwords
# stop_words = {'of', 's', 'against', 'being', 'all', 'its', 'have', "wasn't", 'doing', 'very', 'few', 'why', 'doesn', 'ourselves', 'herself', 'am', 'having', 'nor', 'theirs', 'ain', 'there', 'out', 'from', 'you', "that'll", 'haven', 'any', "doesn't", 'wasn', 'because', 'can', "mustn't", 'too', 'off', 'hadn', "isn't", 'has', 'it', 'while', 'd', 'is', 'some', 'were', "weren't", 'myself', 'his', 'whom', 'if', 'other', "haven't", 'him', 'after', "mightn't", 'isn', 'my', 'their', 'was', 'had', 'each', "you've", 'down', "she's", 'before', 'don', "didn't", 'couldn', 'just', "needn't", 'shouldn', "should've", 'where', 'our', 'not', 'hasn', 'such', "couldn't", "shouldn't", 'for', 'who', 'that', "it's", 'over', 're', 'needn', 'didn', "shan't", "won't", 'only', 'itself', 'on', 'a', 'do', 'more', 'ours', 'above', "wouldn't", 'hers', 'when', 'which', 'under', 'below', 'me', 'your', 'are', 'own', 'aren', "hasn't", "you'd", 'then', 'now', 'o', 'about', 'so', 'be', 'an', 'both', 'himself', 'but', 'again', 'than', 'as', 'should', "you'll", 'until', "aren't", 'further', "you're", 'those', 'does', 't', 'mightn', 'yours', 'through', 'will', "hadn't", 'i', "don't", 'y', 'themselves', 'm', 'the', 'ma', 'shan', 'yourself', 'into', 'her', 'most', 'this', 'no', 'what', 'wouldn', 'll', 'or', 'them', 'by', 'once', 'mustn', 'did', 'between', 'she', 'during', 'how', 'same', 'he', 'with', 'to', 'weren', 'we', 'at', 'won', 'yourselves', 'here', 'up', 'they', 'been', 'in', 've', 'and', 'these'}


# Read train data and label

# #uncomment to use dummy teset file
# # read from test file
# with open("unit_test.txt") as f:
#     raw_data = f.readlines()
# for line in raw_data:

doc_id = 0
# input comes from STDIN (standard input)
for line in sys.stdin:
    # Read train data and label
    try:
        classlabels, data_str = line.strip().split(' \t', 1)
    except ValueError:
        continue
    #classlabels_list = classlabels.split(',')  # get class labels as list

    # string processing
    m = re.findall('".*"@en', data_str.lower())  # extract useful_data between " <useful_data>"@en
    #data_str = re.sub('\\\\\w\d*', ' ', m[0])  # remove tags
    data_str = bytes(m[0], 'utf-8').decode("unicode_escape")
    data_str = re.sub('@en', '', data_str)  # remove end of sentence
    data_str = re.sub('[^a-zA-Z]', ' ', data_str)  # remove all punctuations, special-char and digits
    data_str = re.sub('\s+', ' ', data_str)  # replace multiple spaces
    data_str = data_str.strip()  # replace multiple spaces

    # tokenize
    words = word_tokenize(data_str)
    #words = data_str.split()

    # remove stopwords and stem
    filtered_words = [stemmer.stem(w) for w in words if w not in stop_words]
    #filtered_words = [w for w in words if not w in stop_words]

    # send key value as STDOUT. key = (classlabel word) , value = (count 1)
    for word in filtered_words:
        print('%.7d %s\t1 %s' % (doc_id, word, classlabels))  # emit key-val for each class to find the class counts

    doc_id += 1