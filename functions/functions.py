# Universiteit van Amsterdam
# Digital Humanities Lab, WG04
# Final project - Topic modelling tool
# functions.py

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

    """
    Loop through a given folder, and read all the pdf files that can be found in the folder, and save its contents to a dictionary
    The folder should ONLY contain files with the extension of .pdf, as this project is focusing on PDFs and academic papers.

    Parameters:
        folder: string
            The name of the folder where the PDFs can be found. Has to be in the same folder as the project.ipynb file.

    Returns:
        articles: dictionary
            A dictionary, containing the files' names as the key, and the contents of the files as the values.
    """


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

    """
    Lemmatize and stem a word. Change a verb to its present tense, and reduce the word to its root forms.

    Parameters:
        word: string
            The word the user wants to lemmatize and stem

    Returns:
        The lemmatized and stemmed word
    """


    stemmer = SnowballStemmer('english')

    return stemmer.stem(WordNetLemmatizer().lemmatize(word, pos='v'))


def processPDF(dictionary):

    """
    Process the PDFs that can be found in the dictionary, created by the readPDF function.
    This includes removing stopwords, punctuations, digits, whitespaces, line breaks, and lemmatizes and stems all the words.

    Parameters:
        dictionary:  dictionary
            The dictionary containing the files and its contents

    Returns:
        processedPDF: dictionary
            A new, cleaned dictionary, only with the necessary words.
    """

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

    """
    Turn the dictionary into a Pandas DataFrame, so that it can be used more easily for the topic modelling tool.
    Creates two columns, where the first is the dictionary's keys, and the second is the contents.

    Parameters:
        data: dictionary
            The dictionary the user wants to turn into a DataFrame

    Returns:
        dataFrame: a pandas DataFrame
            A DataFrame with the file names and the contents of the PDFs
    """

    dataFrame = pd.DataFrame(data.items(), columns=['file_name', 'content'])

    return dataFrame


def listOfWords(dataFrame):

    """
    Create a list of words, with the help of the gensim library, from the DataFrame's content column.
    This can be used for the topic generator part of the program.

    Parameters:
        dataFrame: a pandas DataFrame
            The dataFrame that contains the files' names and its processed contents    

    Returns:
        listOfWords: list
            The list, containing the words that can be found in the dataFrame's column
    """

    listOfWords = gensim.corpora.Dictionary(dataFrame['content'])
    #listOfWords = listOfWords.filter_extremes(no_below=5, no_above=2, keep_n=10000)

    return listOfWords

def wordsPerArticle(dataFrame):

    """
    Create a list from each articles' vocabulary. 
    This can be used for the evaluation part of the program, to find out the topic of a given article/PDF.

    Parameters:
        dataFrame: a pandas DataFrame
            The dataFrame that contains the files' names and its processed contents

    Returns:
        corpus: a list
            A list of words that can be found in each article
    """

    LoW = listOfWords(dataFrame)
    corpus = [LoW.doc2bow(article) for article in dataFrame['content']]

    return corpus


def tfidfCorpus(listOfWords, dataFrame):

    """
    Create the TF-IDF model and a list of tuple pair, with the scores of each words in a given article.
    The list of tuple pairs can be used for the TF-IDF version of topic generating part of the project

    Parameters:
        listOfWords: a list
            The return of the listOfWords function, preferably
        dataFrame: a pandas DataFrame
            The dataFrame that contains the files' names and its processed contents
    
    Returns:
        tfidfCorpus: a list of tuple pairs
            A list of tuple pairs with the scores (relevance) of each word in a given article
    """

    WpA = wordsPerArticle(dataFrame)

    tfidfModel = gensim.models.TfidfModel(WpA)
    tfidfCorpus = tfidfModel[WpA]

    return tfidfCorpus
