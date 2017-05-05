# -*- coding: utf-8 -*-

from re import compile
from requests import get
from json import JSONDecodeError
from pandas import DataFrame, concat
from sys import exit

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


def load_page(board='b'):
    try:
        dvach_page = get(DVACH + board + '/catalog.json').json()
        threads = [i['num'] for i in dvach_page['threads']]
    except:
        print('Такой доски нет. Попробуй ввести две буквы: vg')
        return None
    return threads


def get_thread_names(threads, board):
    return [get(DVACH + board + '/res/' + thread + '.json', timeout=5).json()['threads'][0]['posts'][0]['subject'] for
            thread in threads[:15]]


def show_thread_names(threads_names, start=0):
    for index, name in enumerate(threads_names[:15]):
        print(index, ' ', name)


def get_annotate_data(board, thread):
    th = get(DVACH + board + '/res/' + thread + '.json', timeout=5).json()
    reference = cut(th['threads'][0]['posts'][0]['comment'])[:100]
    comments = [cut(i['comment']).strip() for i in th['threads'][0]['posts'][1:] if len(i['comment']) < 100]
    return reference, comments


def start_annotating(reference, comments):
    labels = []
    for i in comments:
        print('ОП-пост:')
        print(reference)
        print('Сообщение:')
        print(i)
        while (True):
            label = input()
            if label == 'quit':
                return labels
            try:
                label = int(label)
            except ValueError:
                print('Введи 1 если сообщения относятся к одной теме, и 0 иначе. quit для выхода (данные сохранятся)')
                continue
            if label == 1 or label == 0:
                label = int(label)
                break
            else:
                print('Введи 1 если сообщения относятся к одной теме, и 0 иначе. quit для выхода (данные сохранятся)')
        labels.append(int(label))
        #clear_output()
    return labels


def make_df(reference, comments, labels):
    df = DataFrame()
    df['comment'] = comments
    df['reference'] = reference
    df['labels'] = labels
    df.index.names = ['comment_id']
    try:
        file_path = 'annotated.csv'
        old_df = DataFrame.from_csv(file_path)
        df = concat((df, old_df)).drop_duplicates(subset='comment')
    except FileNotFoundError:
        pass
    df.to_csv('annotated.csv')


if __name__ == "__main__":
    print('Привет! Спасибо за интерес к исследованию по разметке Двача. Чтобы начать, введи имя любой доступной борды без слэша, к примеру, набери: vg')
    while (True):
        board = input()
        threads = load_page(board)
        if threads:
            break
    print('Отлично. Загружаем данные с ' + board + ', подожди минутку.')
    while (True):
        try:
            show_thread_names(get_thread_names(threads, board))
        except:
            continue
        print('Перед тобой список доступных тредов. Введи номер (id) треда из списка, к примеру, 1. Набери quit для прекращения работы.')
        while (True):
            id = input()
            if id == 'quit':
                print('Спасибо за работу!')
                amount = 0
                try:
                    amount = len(DataFrame.from_csv('annotated.csv'))
                except FileNotFoundError:
                    pass
                print('На текущий момент размечено ', amount, ' пар сообщений. Отлично!')
                exit()
            try:
                id = int(id)
            except ValueError:
                print('Введи число, а не букву.')
                continue
            if id >= 15:
                print('Такого числа нет в списке.')
            else:
                break
        print('Введи 1 если сообщения относятся к одной теме, и 0 иначе. quit для выхода (данные сохранятся)')
        reference, comments = get_annotate_data(board, threads[id])
        labels = start_annotating(reference, comments)
        make_df(reference, comments[:len(labels)], labels)
        print('Отлично, работа с этим тредом закончена. Данные сохранены. Снова загружаем список тредов доски ' + board)