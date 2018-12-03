from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re
import sys
import nltk


def getEmojiHandling(review):
    emoji = []
    for word in review:
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

def getPunctHandling(review):
    #menghilangkan tanda baca
    preprocess_review = []
    for word in review:
        word = word.strip('\'"?!,.():;')

        #mengkonversi huruf vocal lebih dari satu dan berurutan
        word_character = re.compile(r"(.)\1+", re.DOTALL)
        word = word_character.sub(r"\1\1", word)

        #menghilangkan tanda - & '
        word = re.sub(r'(-|\')','',word)

        preprocess_review.append(word.lower())
    return preprocess_review

def getStemmingSentence(review):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    return stemmer.stem(review)

def getFeatureVector(review,stop_words_indo,stop_words_eng):
    feature_vector = []
    list_no = ['ga','engga','enggak','gak','nggak','ngga','tdk']
    for word in review:
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", word) #menghilangkan karakter selain huruf didalam kata
        if (word in stop_words_indo or val is None or word in stop_words_eng):
            continue
        else:
            if word in list_no:
                word = 'tidak'
            feature_vector.append(word)
    for_stemming = ' '.join(feature_vector)
    return feature_vector, for_stemming

def getNegativeHandling(review):
    negative_review = []
    for i in range(len(review)):
        word = review[i]
        if review[i-1] != 'tidak':
            negative_review.append(word)
        else:
            word = 'tidak_'+word
            negative_review.append(word)
    return negative_review

def preprocessReview(review):
    return getPunctHandling(getEmojiHandling(review))

def createFreqDict(reviewHandled):
    freqOfWord = {}
    for sentence in reviewHandled:
        for word in sentence:
            if word in freqOfWord:
                freqOfWord[word] += 1
            else:
                freqOfWord[word] = 1
    return freqOfWord



