import pandas as pd
from nltk.stem.porter import *
from nltk.corpus import stopwords
from gensim import corpora, models
from nltk.tokenize import word_tokenize
import PyPDF2, nltk, string, fitz, os, gensim
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer

nltk.download('wordnet')

string.punctuation += "”"
string.punctuation += "“"
string.punctuation += "’"
string.punctuation += "‘"
string.punctuation += "``"
string.punctuation += "''"
string.punctuation += "|||"


def readPDF(folder):

    articles = dict()

    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)

            pdf = fitz.open(file_path)
            text = ""
            output = []

            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfFileReader(f, strict=False)
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


def processPDF(dictionary):

    processedPDF = dict()
    nltkStopWords = stopwords.words('english')
    gensimStopWords = STOPWORDS

    for keys in dictionary:
        dictionary[keys] = dictionary[keys].replace('\n', ' ')
        processed = word_tokenize(dictionary[keys])
        processed = [word for word in processed if not word in nltkStopWords]
        processed = [word for word in processed if not word in gensimStopWords]
        processed = [word for word in processed if not word in string.punctuation]
        processed = [word for word in processed if not word in string.digits]
        processed = [word for word in processed if not word in string.whitespace]
        processed = [word for word in processed if len(word) > 3]
        processed = [lemmatizeAndStem(word) for word in processed]
        processedPDF[keys] = processed

    return processedPDF


def toDataFrame(data):

    dataFrame = pd.DataFrame(data.items(), columns=['file_name', 'content'])

    return dataFrame


def listOfWords(dataFrame):

    listOfWords = gensim.corpora.Dictionary(dataFrame['content'])
    #listOfWords = listOfWords.filter_extremes(no_below=5, no_above=2, keep_n=10000)

    return listOfWords

def wordsPerArticle(dataFrame):

    LoW = listOfWords(dataFrame)
    corpus = [LoW.doc2bow(article) for article in dataFrame['content']]

    return corpus


def tfidfCorpus(listOfWords, dataFrame):

    WpA = wordsPerArticle(dataFrame)

    tfidfModel = gensim.models.TfidfModel(WpA)
    tfidfCorpus = tfidfModel[WpA]

    return tfidfCorpus
