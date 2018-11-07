# import Sastrawi package
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import readfile

sentences,labels = readfile.openarticle('Data-Train.csv')

# create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()
# print(factory)

print(sentences[0])
# # stem
# sentence = 'Perekonomian Indonesia sedang dalam pertumbuhan yang membanggakan'
# output   = stemmer.stem(sentence)

# print(output)
# # ekonomi indonesia sedang dalam tumbuh yang bangga

# print(stemmer.stem('Mereka meniru-nirukannya'))
# # mereka tiru