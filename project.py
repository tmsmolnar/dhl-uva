# [WIP]
# Will be re-written into functions!
# [WIP]
# Just outlining the structure yet!
# [WIP]

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
from functions import readPDF, tokenizePDF, lemmatizeAndStem, toDataFrame

string.punctuation += "”"
string.punctuation += "“"
string.punctuation += "’"
string.punctuation += "‘"


keywords = ['philosophy', 'orient', 'oriental philosophy', 'orient', 'eastern philosophy', 'india', 'china',
            'chinese philosophy', 'ancient', 'dao', 'theory', 'theories', 'confucian', 'western', 'eastern',
            'gender', 'feminism', 'feminist', 'feminist theory', 'gender theory', 'religion', 'religious',
            'buddhism', 'contemporary', 'contemporary philosophy', 'spiritual']


# Reading the files and convert from pdf to string/dict

articles = dict()

for root, dirs, files in os.walk('sources'):
    for file in files:
        file_path = os.path.join(root, file)

        pdf = fitz.open(file_path)
        text = ""
        output = []

        with open(file_path, 'rb') as pdf2:
            reader = PyPDF2.PdfFileReader(pdf2)
            numberPages = reader.numPages

            for index in range(0, numberPages):
                page = pdf[index]
                text += page.getText('text')

        articles[file] = text
        output.append(text)

# Basic text-processing, tokenize and filtering

tokenizedArticles = dict()

nltkStopWords = stopwords.words('english')
gensimStopWords = STOPWORDS

for key in articles:
    articles[key] = articles[key].replace('\n', ' ').lower()

    tokenized = word_tokenize(articles[key])
    tokenized = [word for word in tokenized if not word in nltkStopWords]
    tokenized = [word for word in tokenized if not word in gensimStopWords]
    tokenized = [word for word in tokenized if not word in string.punctuation]
    tokenized = [lemmatizeAndStem(word) for word in tokenized]
    tokenizedArticles[key] = tokenized


# Gensim, LDA stuff

dataFrame = pd.DataFrame(tokenizedArticles.items(),
                         columns=['file_name', 'content'])

print(dataFrame)
