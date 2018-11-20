from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import readfile
import re
import sys
import nltk
from nltk.corpus import stopwords

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
            else:
                featureVector.append(word)
    return ' '.join(featureVector)

def preprocessing_komentar(kalimat):
    preprocess_emoji = handling_emoji(kalimat)
    preprocess_punctuation = punctuation(preprocess_emoji)
    # preprocess_stemming = stemming(preprocess_punctuation)
    return preprocess_punctuation

corpus,kelas  = readfile.openarticle('Data-Train.csv')
stopwords_indo = getStopWordsList('stopwords.txt')
stopwords_eng = stopwords.words('english')
# print(stopwords_eng)

kalimat_preprocess = []
komentar = []
featureList = []
for kalimat in corpus:
    x = preprocessing_komentar(kalimat)
    y = getFeatureVector(x,stopwords_indo,stopwords_eng)
    z = stemming(y)
    kalimat_preprocess.append(z)

# jumlah_kata = {}
# tokens = []
# for sentences in kalimat_preprocess:
#     token = nltk.word_tokenize(sentences)
#     tokens.append(token)

# for kalimat in tokens:
#     for kata in kalimat:
#         if kata in jumlah_kata:
#             jumlah_kata[kata] += 1
#         else:
#             jumlah_kata[kata] = 1
# # print(jumlah_kata)

# file_key = open('keys.txt','w')
# for key in jumlah_kata.keys():
#     file_key.write(str(key))
#     file_key.write("\n")
# file_key.close()
# # print('selesai')

