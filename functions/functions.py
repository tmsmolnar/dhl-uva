# [WIP]

import pandas as pd
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
nltk.download('wordnet')

string.punctuation += "”"
string.punctuation += "“"
string.punctuation += "’"
string.punctuation += "‘"


def readPDF(folder):

    articles = dict()

    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)

            pdf = fitz.open(file_path)
            text = ""
            output = []

            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfFileReader(f)
                numberOfPages = reader.numPages

                for index in range(0, numberOfPages):
                    page = pdf[index]
                    text += page.getText('text')

            articles[file] = text
            output.append(text)

    return articles


def lemmatizeAndStem(word):

    stemmer = SnowballStemmer('english')

    return stemmer.stem(WordNetLemmatizer().lemmatize(word, pos='v'))


def tokenizePDF(dictionary):

    tokenizedPDF = dict()
    nltkStopWords = stopwords.words('english')
    gensimStopWords = STOPWORDS

    for keys in dictionary:
        dictionary[keys] = dictionary[keys].replace('\n', ' ')
        tokenized = word_tokenize(dictionary[keys])
        tokenized = [word for word in tokenized if not word in nltkStopWords]
        tokenized = [word for word in tokenized if not word in gensimStopWords]
        tokenized = [
            word for word in tokenized if not word in string.punctuation]
        tokenized = [lemmatizeAndStem(word) for word in tokenized]
        tokenizedPDF[keys] = tokenized

    return tokenizedPDF


def toDataFrame(data):

    dataFrame = pd.DataFrame(data.items(), columns=['file_name', 'content'])

    return dataFrame
