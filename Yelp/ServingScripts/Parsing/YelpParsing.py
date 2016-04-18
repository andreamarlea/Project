# Import libraries
import numpy as np
import pandas as pd
import collections
import nltk
# nltk.download()
import string

from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.collocations import *
from nltk.util import ngrams
from string import digits
from pandas import DataFrame, Series

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

# Read in the train and test data
# on Windows when reading some rows there will be EOF parsing error. Remove skiprows para in when running on AWS
reviews = pd.read_csv('E:/Berkeley/W205/FinalProject/yelp_academic_dataset_review.csv', skiprows=[1480776, 2538417], nrows=200)
reviews_by_business = reviews.groupby('business_id')['text'].apply(list)

text_list = []
for value in reviews_by_business.values:
    text_list.append(''.join(value))

reviews_by_business = pd.DataFrame({'business_id': reviews_by_business.index,'business_name' 'text': text_list})
# Drop columns: Description, Resolution, and Address
#df_train.drop(['Descript', 'Resolution','Address'], axis=1, inplace=True)
#df_test.drop(['Address'], axis=1, inplace=True)

reviews_by_business[:3]

def cleanText(text):
    """
    removes punctuation, stopwords, numbers and returns lowercase text in a list of single words
    """
    text = text.lower()
    # text = text.translate(None, string.punctuation)         #python2
    text = text.translate({ord(k): None for k in digits})     #python3
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = BeautifulSoup(text).get_text()
    tokenizer = RegexpTokenizer(r'\w+')
    text = tokenizer.tokenize(text)
    clean = [word for word in text if word not in stopwords.words('english')]
    return clean

def top5_bigram_collocations(text):
    """
    return the 5 bigrams with the highest PMI
    :param text:
    :return:
    """
    finder = BigramCollocationFinder.from_words(text)
    finder.apply_freq_filter(1)
    bigrams = finder.nbest(bigram_measures.pmi, 5)
    return bigrams

def top5_trigram_collocations(text):
    """
    return the 5 trigrams with the highest PMI
    :param text:
    :return:
    """
    finder = TrigramCollocationFinder.from_words(text)
    finder.apply_freq_filter(1)
    trigrams = finder.nbest(trigram_measures.pmi, 5)
    return trigrams

columns = ['BusinessID','CleanText', 'TotWords', 'bigrams','trigrams']
index = np.arange(reviews_by_business.shape[0])
df = pd.DataFrame(columns=columns, index = index)

i = 0
for index, row in reviews_by_business.iterrows():
    tot = 0
    totwords = 0
    if pd.notnull(row['text']):
        cleantext = cleanText(row['text'])
        totwords = len(cleantext)
        #return the 5 n-grams with the highest PMI
        bigrams = top5_bigram_collocations(cleantext)
        trigrams = top5_trigram_collocations(cleantext)

    df.ix[i, 'BusinessID']= row['business_id']
    df.ix[i, 'TotWords']= totwords
    df.ix[i, 'CleanText']= " ".join(cleantext).encode('utf-8')
    df.ix[i, 'bigrams']= bigrams
    df.ix[i, 'trigrams']= trigrams
    i += 1
pd.set_option('expand_frame_repr', False)
print(df.head(20))