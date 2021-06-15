# [WIP] 
# Will be re-written into functions!
# [WIP]
# Just outlining the structure yet!
# [WIP]

from nltk.corpus import stopwords
import os, fitz, string, nltk, PyPDF2
from nltk.tokenize import word_tokenize


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
        

            for index in range(0,numberPages):
                page = pdf[index]
                text += page.getText('text')

        articles[file] = text
        output.append(text)
        
# Basic text-processing, tokenize and filtering    

tokenizedArticles = dict()   

stopWords = stopwords.words('english')

for key in articles:
    articles[key] = articles[key].replace('\n', ' ').lower()
    
    tokenized = word_tokenize(articles[key])
    tokenized = [word for word in tokenized if not word in stopWords]
    tokenized = [word for word in tokenized if not word in string.punctuation]
    tokenizedArticles[key] = tokenized


for key in tokenizedArticles:
    print(key, tokenizedArticles[key])


# Gensim, LDA stuff
