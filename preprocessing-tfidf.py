from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import readfile
import re
import nltk
import numpy as np
from nltk.corpus import stopwords
from sklearn.model_selection import StratifiedKFold
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix

def handling_emoji(kalimat):
    emoji = []
    for word in kalimat:
        #Smile -- :), : ), :-), (:, ( :, (-:, :')
        word = re.sub(r'(:\s?\)|:-\)|\(\s?:|\(-:|:\'\))','POS',word)
        
        #Laugh -- :D, : D, :-D, xD, x-D, XD, X-D
        word = re.sub(r'(:\s?D|:-D|x-?D|X-?D)','POS',word)

        # Sad -- :-(, : (, :(, ):, )-:
        word = re.sub(r'(:\s?\(|:-\(|\)\s?:|\)-:)', ' NEG ', word)

        # Cry -- :,(, :'(, :"(, T_T
        word = re.sub(r'(:,\(|:\'\(|:"\(|T_T)', ' NEG ', word)

        emoji.append(word)
    return emoji

def punctuation(kalimat):
    #menghilangkan tanda baca
    kalimat_preprocess = []
    for word in kalimat:
        word = word.strip('\'"?!,.():;')

        # #mengkonversi huruf vocal lebih dari satu dan berurutan
        word_character = re.compile(r"(.)\1+", re.DOTALL)
        word = word_character.sub(r"\1\1", word)

        # #menghilangkan tanda - & '
        word = re.sub(r'(-|\')','',word)

        kalimat_preprocess.append(word.lower())
    return kalimat_preprocess
    # return ' '.join(kalimat_preprocess)

def stemming(kalimat):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    output   = stemmer.stem(kalimat)
    return output

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
        
def getFeatureVector(kalimat,stopwords_indo,stopwords_eng):
    featureVector = []
    list_no = ['ga','engga','enggak','gak','nggak','ngga','tdk']
    for word in kalimat:
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", word) #menghilangkan karakter selain huruf didalam kata
        if (word in stopwords_indo or val is None or word in stopwords_eng ):
            continue
        else:
            if word in list_no:
                word = 'tidak'
            featureVector.append(word)
    forstemming = ' '.join(featureVector)
    return featureVector, forstemming

def handling_neg(kalimat):
    neg_word = []
    for i in range(len(kalimat)):
        word = kalimat[i]
        if kalimat[i-1] != 'tidak':
            neg_word.append(word)
        else:
            word = 'tidak_'+word
            neg_word.append(word)
    return neg_word

def preprocessing_komentar(kalimat):
    preprocess_emoji = handling_emoji(kalimat)
    preprocess_punctuation = punctuation(preprocess_emoji)
    # preprocess_stemming = stemming(preprocess_punctuation)
    return preprocess_punctuation

def create_freq_dict(after_handling):
    jumlah_kata = {}
    for kalimat in after_handling:
        for kata in kalimat:
            if kata in jumlah_kata:
                jumlah_kata[kata] += 1
            else:
                jumlah_kata[kata] = 1
    file_key = open('keys.txt','w')
    for key in jumlah_kata.keys():
        file_key.write(str(key))
        file_key.write("\n")
    file_key.close()
    return jumlah_kata

corpus,kelas  = readfile.openarticle('Data-Train.csv')
stopwords_indo = getStopWordsList('stopwords.txt')
stopwords_eng = stopwords.words('english')
# print(stopwords_eng)

kalimat_preprocess = []
featureList = []
for kalimat in corpus:
    x = preprocessing_komentar(kalimat)
    feature,y = getFeatureVector(x,stopwords_indo,stopwords_eng)
    z = stemming(y)
    kalimat_preprocess.append(z)
tokens = []
after_handling = []
for sentences in kalimat_preprocess:
    token = nltk.word_tokenize(sentences)
    tokens.append(token)

komentar = []
for i in range(len(tokens)):
    a = handling_neg(tokens[i])
    after_handling.append(a)
    komentar.append((' '.join(a),kelas[i]))

data = []
sentiments = []

for i in range(len(komentar)):
    data.append(komentar[i][0])
    sentiments.append(komentar[i][1])


labels = np.zeros(300)
labels[0:240] = 0
labels[240:300] = 1

kf = StratifiedKFold(n_splits=10)

totalNB = 0
totalMatNB = np.zeros((2,2))

for train_idx, test_idx in kf.split(data,sentiments):
    X_train = [data[i] for i in train_idx]
    X_test = [data[i] for i in test_idx]
    y_train,y_test = labels[train_idx], labels[test_idx]
    vectorizer = TfidfVectorizer(min_df=0.0, max_df=1.0, sublinear_tf=True, use_idf=True, stop_words='english')
    X_train_tf_idf = vectorizer.fit_transform(X_train)
    X_test_tf_idf = vectorizer.transform(X_test)

    model = MultinomialNB()
    model.fit(X_train_tf_idf, y_train)
    result = model.predict(X_test_tf_idf)

    totalMatNB = totalMatNB + confusion_matrix(y_test, result)
    totalNB = totalNB + sum(y_test==result)
    print(train_idx,test_idx)
    

print(totalMatNB, totalNB/len(data))