import csv
from nltk.corpus import stopwords

def openFile(file_name):
    with open(file_name, encoding="utf-8") as csvfile: 
        next(csvfile)
        rawArticles = csv.reader(csvfile, delimiter=',') 
        words = [] #array perkata akan menyimpan semua kalimat menjadi perkata
        sentences = [] #array perkalimat menyimpan semua kalimat menjadi perkalimat
        sentiment = []
        for row in rawArticles:
            sentences=row[3].lower()
            words.append(sentences.split())
            sentiment.append(row[5].lower())
    return words, sentiment 

def getStopWordsList(stopwordsfile):
    stopwords=[]
    file_stopwords = open(stopwordsfile,'r')
    row = file_stopwords.readline()
    while row:
        word = row.strip()
        stopwords.append(word)
        row = file_stopwords.readline()
    file_stopwords.close()
    return stopwords