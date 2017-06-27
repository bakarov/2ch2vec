from pandas import DataFrame, concat
from os import listdir, path
from utils.string_utils import *
from numpy import savetxt
from pickle import dump
from nltk import word_tokenize

BOARD_LIST = ['pr', 'vg', 'b', 'me', 'po', 'diy', 'a', 'rf']
FILENAME = 'all_lem'


def merge_corpora(board_list, filename, lemmatize=False):
    df = DataFrame()
    for board in board_list:
        df = concat((df, DataFrame.from_csv(path.join('pickle', '{}.csv'.format(board)), encoding='utf-8'))).drop_duplicates().dropna()
    df.comment = df.comment.apply(cut)
    if lemmatize:
        df.comment = df.comment.apply(morph_parse)
    print('Corpus size = {}'.format(len(df)))
    save_corpus_to_text(df, filename)
    picklize_corpus(df, filename)


def save_corpus_to_text(df, filename):
    with open(path.join('corpus', '{}.txt'.format(filename)), 'w') as f:
        f.write('\n'.join(df.comment.values))


def picklize_corpus(df, filename):
    with open(path.join('corpus', '{}_tokenized.pickle'.format(filename)), 'wb') as f:
        dump([word_tokenize(sentence) for sentence in df.comment.values], f)


if __name__ == "__main__":
    merge_corpora(BOARD_LIST, FILENAME, True)
