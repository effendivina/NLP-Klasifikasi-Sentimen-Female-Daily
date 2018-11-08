from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import readfile
import re
import sys
import nltk.tokenize


def stemming(kalimat):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    output   = stemmer.stem(kalimat)
    return output

def preprocessing_word(kalimat):
    #menghilangkan tanda baca
    kalimat_preprocess = []
    for word in kalimat:
        word = word.strip('\'"?!,.():;*')

        # #mengkonversi huruf vocal lebih dari satu dan berurutan
        word = re.sub(r'(.)\1+', r'\1', word)

        # #menghilangkan tanda - & '
        word = re.sub(r'(-|\')','',word)

        kalimat_preprocess.append(word)
    return ' '.join(kalimat_preprocess)

corpus,kelas  = readfile.openarticle('Data-Train.csv')

kalimat_punct = []
for kalimat in corpus:
    x = preprocessing_word(kalimat)
    kalimat_punct.append(x)

kalimat_stem=[]
for kalimat in kalimat_punct:
    x = stemming(kalimat)
    kalimat_stem.append(x)

for kalimat in kalimat_stem:
    print(kalimat)
    print()

