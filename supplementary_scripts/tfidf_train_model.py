from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from pickle import dump, load
from os import path, makedirs
from gensim.corpora import Dictionary

CORPUS_FILE = '2ch_corpus.txt'
OUTPUT_FILE = 'all_lem'

def load_data():
    with open(path.join('corpus', CORPUS_FILE)) as f:
        return list(f.read().splitlines())


def train_model(model_data):
    vectorizer = TfidfVectorizer()
    vectorizer.fit_transform(model_data)
    return dict(zip(vectorizer.get_feature_names(), vectorizer.idf_))


def serialize_model(model):
    print('Amount of terms = {}'.format(len(model)))
    subdir = path.join('models', 'tfidf')
    if not path.exists(subdir):
        makedirs(subdir)
    with open(path.join(subdir, OUTPUT_FILE), 'wb') as fp:
        dump(model, fp)

if __name__ == "__main__":
    serialize_model(train_model(load_data()))
