import nltk,csv,pickle
fp0 = open( 'fkk0.csv', 'rb' )
fp4 = open( 'fkk4.csv', 'rb' )
reader0 = csv.reader( fp0, delimiter=',', quotechar='"', escapechar='\\' )
reader4 = csv.reader( fp4, delimiter=',', quotechar='"', escapechar='\\' )
raw_tweets = []
i,j=0,0
for row in reader0:
    raw_tweets.append([row[5],row[0]])
    if j>1000:
	break
    j+=1
for row in reader4:
    raw_tweets.append([row[5],row[0]])
    if i>1000:
	break
    i+=1
"""
pos_tweets = [('I love this car', 'positive'),
	   ('This view is amazing', 'positive'),
	   ('I feel great this morning', 'positive'),
	   ('I am so excited about the concert', 'positive'),
	   ('He is my best friend', 'positive')]
neg_tweets = [('I do not like this car', 'negative'),
	   ('This view is horrible', 'negative'),
	   ('I feel tired this morning', 'negative'),
	   ('I am not looking forward to the concert', 'negative'),
	   ('He is my enemy', 'negative')]
"""
print "raw_tweets"
tweets = []
for (words, sentiment) in raw_tweets:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3] 
    tweets.append((words_filtered, sentiment))
print "tweets"

test_tweets = [
    (['feel', 'happy', 'this', 'morning'], '4'),
    (['larry', 'friend'], '4'),
    (['not', 'like', 'that', 'man'], '0'),
    (['house', 'not', 'great'], '0'),
    (['your', 'song', 'annoying'], '0')]

def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
      all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

print "seriously"
word_features = get_word_features(get_words_in_tweets(tweets))
print "esesef"
def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features
print "bivsdf"
training_set = nltk.classify.apply_features(extract_features, tweets)
classifier = nltk.NaiveBayesClassifier.train(training_set)
f = open("FSsentimentTrained.pickle","wb")
pickle.dump(classifier,f)
f.close()
print classifier.show_most_informative_features(32) 
tweet = raw_input("Give the tweet you want analysed: ")
print classifier.classify(extract_features(tweet.split()))

