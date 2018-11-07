import re
import sys
import readfile
import nltk.tokenize

def preprocessing_word(word):
    #menghilangkan tanda baca
    word = word.strip('\'"?!,.():;*')

    # #mengkonversi huruf vocal lebih dari satu dan berurutan
    word = re.sub(r'(.)\1+', r'\1\1', word)

    # #menghilangkan tanda - & '
    word = re.sub(r'(-|\')','',word)

    return word

sentence = readfile.openarticle('Data-Train.csv')
print((sentence[0]))                                  

