# Import libraries
from pyspark import SparkContext
from pyspark.sql import HiveContext
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

sc = SparkContext("local", "YelpParsing")
# Read in the train and test data
reviews = sqlContext.sql("select review.business_id as business_id, \
                        review.text as text, \
                        review.stars as stars, \
                        review.date as date from review")
reviews_by_business = reviews.groupby('business_id')['text']
reviews_by_business = reviews_by_business.aggregate(lambda x: ' '.join(x))

df_reviews_by_business = pd.DataFrame({'business_id': reviews_by_business.index, 'text': reviews_by_business.values})

# Drop columns: Description, Resolution, and Address
#df_train.drop(['Descript', 'Resolution','Address'], axis=1, inplace=True)
#df_test.drop(['Address'], axis=1, inplace=True)


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

def top5_words(text):
    """
    get top5 words with highest frequency
    """
    counts = collections.Counter(text.split())
    return counts.most_common(5)

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

columns = ['business_id','clean_text', 'tot_words', 'bigrams','trigrams','stars','date']
index = np.arange(df_reviews_by_business.shape[0])
df = pd.DataFrame(columns=columns, index = index)

i = 0
for index, row in df_reviews_by_business.iterrows():
    tot = 0
    totwords = 0
    if pd.notnull(row['text']):
        cleantext = cleanText(row['text'])
        totwords = len(cleantext)
        #return the 5 n-grams with the highest PMI
        unigrams = top5_words(cleantext)
        bigrams = top5_bigram_collocations(cleantext)
        trigrams = top5_trigram_collocations(cleantext)

    df.ix[i, 'business_id']= row['business_id']
    df.ix[i, 'clean_text']= " ".join(cleantext).encode('utf-8')
    df.ix[i, 'tot_words']= totwords
    df.ix[i, 'bigrams']= bigrams
    df.ix[i, 'trigrams']= trigrams
    df.ix[i, 'stars']= row['business_id']
    df.ix[i, 'date']= row['date']
    i += 1

# Save it as a table
df.registerTempTable("dfBusiness")
sqlContext.sql("drop table if exists resultByBusiness")
sqlContext.sql("CREATE TABLE resultByBusiness AS SELECT * FROM df")