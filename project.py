from nltk.corpus import stopwords
import os
import fitz
import string
import nltk
import PyPDF2
from nltk.tokenize import word_tokenize
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import pandas as pd
from functions import readPDF, processPDF, lemmatizeAndStem, toDataFrame

string.punctuation += "”"
string.punctuation += "“"
string.punctuation += "’"
string.punctuation += "‘"


keywords = ['philosophy', 'orient', 'oriental philosophy', 'orient', 'eastern philosophy', 'india', 'china',
            'chinese philosophy', 'ancient', 'dao', 'theory', 'theories', 'confucian', 'western', 'eastern',
            'gender', 'feminism', 'feminist', 'feminist theory', 'gender theory', 'religion', 'religious',
            'buddhism', 'contemporary', 'contemporary philosophy', 'spiritual']


# Reading the files and convert from pdf to string/dict
articles = readPDF('sources')

# Basic text-processing, tokenize and filtering
processedArticles = processPDF(articles)


# Gensim, LDA stuff
dataFrame = toDataFrame(processedArticles)
print(dataFrame)
