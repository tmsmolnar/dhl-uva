# [WIP]

from nltk.corpus import stopwords
import os, fitz, string, nltk, PyPDF2
from nltk.tokenize import word_tokenize


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

def tokenizePDF(dictionary):

    tokenizedPDF = dict()
    stopWords = stopwords.words('english')

    for keys in dictionary:
        dictionary[keys] = dictionary[keys].replace('\n', ' ').lower()

        tokenized = word_tokenize(dictionary[keys])
        tokenized = [word for word in tokenized if not word in stopWords]
        tokenized = [word for word in tokenized if not word in string.punctuation]
        tokenizedPDF[keys] = tokenized

    return tokenizedPDF
