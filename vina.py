import re
import sys
import readFile
import string

def punctuation(kalimat):
    kalimat_punct = []
    for word in kalimat:
        #hilangkan tanda baca
        word = word.strip('\'"?!,.():;/*')

        #hilangkan huruf yang berurutan
        word = re.sub(r'(.)\1+', r'\1', word)

        #hilangkan tanda - & '
        word = re.sub(r'(-|\')', '', word)

        kalimat_punct.append(word)

    return kalimat_punct

def handling_emoji(kalimat):
    emoji = []
    for word in kalimat:
        #Smile -- :), : ), :-), (:, ( :, (-:, :')
        word = re.sub(r'(:\s?\)|:-\)|\(\s?:|\(-:|:\'\))','EMO_POS',word)
        
        #Laugh -- :D, : D, :-D, xD, x-D, XD, X-D
        word = re.sub(r'(:\s?D|:-D|x-?D|X-?D)','EMO_POS',word)

        # Sad -- :-(, : (, :(, ):, )-:
        word = re.sub(r'(:\s?\(|:-\(|\)\s?:|\)-:)', ' EMO_NEG ', word)

        # Cry -- :,(, :'(, :"(, T_T
        word = re.sub(r'(:,\(|:\'\(|:"\(|T_T)', ' EMO_NEG ', word)

        emoji.append(word)
    return emoji

def preprocessing_komentar(kalimat):
    preprocess_emoji = handling_emoji(kalimat)
    preprocess_punctuation = punctuation(preprocess_emoji)
    return preprocess_punctuation

sentences = readFile.openarticle('Data-Train.csv')
# print(sentences)
kalimats = []
for sentence in sentences:
    kalimats.append(sentence.split())
# print(kalimats)

kata_preprocess = []
kalimat_emoji = []
kalimat_preprocess = []
for kalimat in kalimats:
    x = preprocessing_komentar(kalimat)
    kalimat_preprocess.append(x)

print(kalimat_preprocess[11])