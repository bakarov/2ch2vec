from glove import Corpus, Glove
from os import path, makedirs
from pickle import dump, load

CORPUS_FILE = 'all_lem_tokenized.pickle'
OUTPUT_FILE = 'all_lem_100'

WINDOW = 10
DIMENSIONALITY = 100


def load_data():
    with open(path.join('corpus', CORPUS_FILE), 'rb') as f:
        return load(f)


def train_model(model_data):
    corpus = Corpus()
    corpus.fit(model_data, window=WINDOW)
    glove = Glove(no_components=DIMENSIONALITY, learning_rate=0.05)
    glove.fit(corpus.matrix, epochs=2, no_threads=4, verbose=True)
    glove.add_dictionary(corpus.dictionary)
    g_vocab = glove.dictionary
    return glove


def serialize_model(model):
    subdir = path.join('models', 'glove')
    if not path.exists(subdir):
        makedirs(subdir)
    with open(path.join(subdir, OUTPUT_FILE), 'wb') as fp:
        dump(model, fp)


if __name__ == "__main__":
    serialize_model(train_model(load_data()))
