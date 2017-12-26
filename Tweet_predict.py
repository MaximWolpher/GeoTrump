import nltk
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import string
from nltk.stem import WordNetLemmatizer

class Sentiment:
    def __init__(self):
        with open("sentiment_clf.pickle","rb") as clf_f:
            classifier=pickle.load(clf_f)
        with open("word_features5k.pickle","rb") as word_f:
            word_features=pickle.load(word_f)
        self.clf = classifier
        self.word_feat = word_features


    def find_features(self,document):
        tknzr = TweetTokenizer(strip_handles=True, reduce_len=True, preserve_case=False)
        words = tknzr.tokenize(document)
        punctuation = list(string.punctuation)
        stop = stopwords.words('english')+punctuation+['rt','via']
        terms_stop = [term for term in words if term not in stop and not term.startswith('http')]
        lemmatizer = WordNetLemmatizer()
        lemmed_data = [lemmatizer.lemmatize(x) for x in terms_stop]
        features = {}
        for w in self.word_feat:
            features[w] = (w in lemmed_data)
        return features


    def sentiment(self,text):
        feats = self.find_features(text)
        pos_prob = self.clf.prob_classify(feats).prob('pos')
        return pos_prob
