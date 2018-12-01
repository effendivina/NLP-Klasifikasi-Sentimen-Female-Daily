from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import readfile
import re
import sys
import nltk
from nltk.corpus import stopwords
import nltk.classify


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

def ektraksi_fitur(kalimat):
    words = set(kalimat)
    features = {}
    for word in featureList.keys():
        features['contains(%s)' % word] = (word in words) 
    return features


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
    komentar.append((a,kelas[i]))

# print(komentar)

featureList = create_freq_dict(after_handling)

training_set = nltk.classify.util.apply_features(ektraksi_fitur,komentar)

NBClassifier = nltk.NaiveBayesClassifier.train(training_set)

kalimat_test = []
test_preprocess = []
hasil = []
test,kelas_test = readfile.openarticle('Data-Test.csv')
for kalimat in test:
    klasifikasi,stemming = getFeatureVector(kalimat,stopwords_indo,stopwords_eng)
    ekstraksi_handling = handling_neg(klasifikasi)
    sentiment = NBClassifier.classify(ektraksi_fitur(ekstraksi_handling))
    hasil.append((kalimat,sentiment))

for sentiment in hasil:
    print(sentiment)



