import readfile
import preprocessing

corpus_train, sentiments_train = readfile.openFile('50-Data-Train.csv')
reviews_test, sentiments_test = readfile.openFile('5-Data-Test.csv')
stop_words_indo = readfile.getStopWordsList('stopwordsindo.txt')
stop_words_eng = readfile.stopwords.words('english')

def getFeatureExtraction(review):
    words = set(review)
    features = {}
    for word in feature_list.keys():
        features['contains(%s)' % word] = (word in words) 
    return features

preprocess_reviews = []
tokens = []
reviews = []
handled_reviews = []
feature_list = []
for review in corpus_train:
    feature, review_for_stem = preprocessing.getFeatureVector(preprocessing.preprocessReview(review),stop_words_indo,stop_words_eng)
    preprocess_reviews.append(preprocessing.getStemmingSentence(review_for_stem))

for review in preprocess_reviews:
    tokens.append(preprocessing.nltk.word_tokenize(review))

for i in range(len(tokens)):
    neg_handled_rev = preprocessing.getNegativeHandling(tokens[i])
    handled_reviews.append(neg_handled_rev)
    reviews.append((neg_handled_rev,sentiments_train[i]))

feature_list = preprocessing.createFreqDict(handled_reviews)
training_set = preprocessing.nltk.classify.util.apply_features(getFeatureExtraction,reviews)
NBClassifier = preprocessing.nltk.NaiveBayesClassifier.train(training_set)

prediction = []
validation_test = []
for review in reviews_test:
    feature_classification, review_test_for_stem = preprocessing.getFeatureVector(review,stop_words_indo,stop_words_eng)
    handled_reviews_test = preprocessing.getNegativeHandling(feature_classification)
    classify_result = NBClassifier.classify(getFeatureExtraction(handled_reviews_test))
    prediction.append((review,classify_result))
    validation_test.append(classify_result)

num_true = 0
for k,val in enumerate(validation_test):
    if val==sentiments_test[k]: 
        num_true+=1
accuracy = (num_true/len(reviews_test))*100
