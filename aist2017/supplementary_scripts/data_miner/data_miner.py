# -*- coding: utf-8 -*-

from os import path, makedirs
from re import compile
from requests import get
from itertools import chain
from nltk.tokenize import sent_tokenize
from pandas import DataFrame, concat
from sys import argv


DVACH = 'https://2ch.hk/'


def cut(data):
    r = compile(r'<.*?>|>>\d*|\(OP\)|&#(\d*);|&quot;|&gt;|(http|https):.*')
    return r.sub('', punctuate_word(punctuate_sent((data))))


def punctuate_sent(data):
    r = compile(r'([a-zA-Zа-яА-Я])([.!\?])')
    return r.sub(r'\1. ', data)


def punctuate_word(data):
    r = compile(r'([a-zA-Zа-яА-Я])([,])')
    return r.sub(r'\1, ', data)


def load_threads(board='b'):
    try:
        dvach_page = get(DVACH + board + '/catalog.json').json()
        return [i['num'] for i in dvach_page['threads']], board
    except:
        print('Нет такой доски.')


def load_comments(threads, board='b'):
    print('Загружаем комментарии с ' + board)
    comments = []

    for every_thread in threads:
        try:
            thread = get(DVACH + board + '/res/' + every_thread + '.json', timeout=5).json()
            [comments.append(sent_tokenize(cut(i['comment']))) for i in thread['threads'][0]['posts'] if
            len(cut(i['comment'])) > 2]
        except:
            pass
    print('Данные загружены, переходим к сериализации')
    return list(chain.from_iterable(comments)), board


def serialize_comments(comments, board='b'):
    df = DataFrame()
    df['comment'] = comments
    df.index.names = ['comment_id']
    subdir = '../pickle'
    try:
        file_path = path.join(subdir, board + '.csv')
        old_df = DataFrame.from_csv(file_path)
        df = concat((df, old_df)).drop_duplicates()
        print('Данные смерджены с уже существующими.')
    except FileNotFoundError:
        print('Сериализованных данных доски ' + board + ' не найдено, сделан новый файл.')
    if not path.exists(subdir):
        makedirs(subdir)
    file_path = path.join(subdir, board + '.csv')
    df.to_csv(file_path)
    print('Сериализованы данные доски ' + board)


if __name__ == "__main__":
    if len(argv) > 1:
        print('Начинаем загрузку.')
        for board in (argv[1:]):
            serialize_comments(*load_comments(*load_threads(board)))
        print('Загрузка завершена.')
