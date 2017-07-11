from gensim.models import Word2Vec
from os import path, makedirs
from pickle import load

CORPUS_FILE = '2ch_corpus_tokenized.pickle'
OUTPUT_FILE = 'all_lem_100'

WINDOW = 7
DIMENSIONALITY = 100


def load_data():
    with open(path.join('corpus', CORPUS_FILE), 'rb') as f:
        return load(f)


def train_model(model_data):
    return Word2Vec(model_data, min_count=5, size=DIMENSIONALITY, window=WINDOW,  workers=4)


def serialize_model(model):
    subdir = path.join('models', 'word2vec')
    if not path.exists(subdir):
        makedirs(subdir)
    model.save(path.join(subdir, OUTPUT_FILE))


if __name__ == "__main__":
    serialize_model(train_model(load_data()))
