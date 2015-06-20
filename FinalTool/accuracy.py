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
tweets = []
for (words, sentiment) in raw_tweets:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3] 
    tweets.append((words_filtered, sentiment))

def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
      all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

word_features = get_word_features(get_words_in_tweets(tweets))

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

classifier = pickle.load(open("FSsentimentTrained.pickle",'rb')) 
correctCount,totalCount,i = 0,0,0
fptest = open( 'sentiment.csv', 'rb' )
readerTest = csv.reader( fptest, delimiter=',', quotechar='"', escapechar='\\' )
for row in readerTest:
    if row[0] != "2":
        tweet = row[5]
	if classifier.classify(extract_features(tweet.split())) == row[0]:
	    correctCount +=1
	totalCount+=1

print (correctCount*100)/totalCount,"%"
