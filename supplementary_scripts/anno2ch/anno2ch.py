# -*- coding: utf-8 -*-

from re import compile
from requests import get
from json import JSONDecodeError
from pandas import DataFrame, concat
from sys import exit

DVACH = 'https://2ch.hk/'


def remove_html(text):
    html = compile(r'<.*?>')
    return html.sub('', text)

def remove_leading(data):
    r = compile(r'^(op|gt)')
    return r.sub(r'', data)


def cut(text):
    r = compile(r'\(OP\)|gt|quot|&#(\d*);|&quot;|&gt;|&#47;|(http|https):.*')
    return remove_leading(' '.join(r.sub('',
    make_alpha(remove_html(punctuate_sent(punctuate_word(text))))).
                                   lower().strip().split()))


def make_alpha(text):
    alpha = compile('[^a-zа-яA-ZА-Я,\.\?! ]')
    return alpha.sub('', text)


def punctuate_sent(data):
    r = compile(r'([a-zA-Zа-яА-Я])([.!\?])')
    return r.sub(r'\1. ', data)


def punctuate_word(data):
    r = compile(r'([a-zA-Zа-яА-Я])([,])')
    return r.sub(r'\1, ', data)


def load_page(board='b'):
    try:
        dvach_page = get(DVACH + board + '/catalog.json',  timeout=10).json()
        threads = [i['num'] for i in dvach_page['threads']]
    except:
        print('Такой доски нет. Попробуй ввести две буквы: vg')
        return None
    return threads


def get_thread_names(threads, board):
    return [get(DVACH + board + '/res/' + thread + '.json', timeout=10).json()['threads'][0]['posts'][0]['subject'] for
            thread in threads[:15]]


def show_thread_names(threads_names, start=0):
    for index, name in enumerate(threads_names[:15]):
        print(index, ' ', cut(name))


def get_annotate_data(board, thread):
    th = get(DVACH + board + '/res/' + thread + '.json', timeout=10).json()
    reference = cut(th['threads'][0]['posts'][0]['comment'])[:200].lower()
    comments = [cut(i['comment'])[:200] for i in th['threads'][0]['posts'][1:] if len(cut(i['comment'])[:200]) > 30]
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
    return labels


def make_df(reference, comments, labels):
    df = DataFrame()
    df['comment'] = comments
    df['reference'] = reference
    df['labels'] = labels
    df.index.names = ['comment_id']
    try:
        file_path = 'annotated.csv'
        old_df = DataFrame.from_csv(file_path, encoding = 'cp1251')
        df = concat((df, old_df)).drop_duplicates(subset='comment').reset_index(drop=True)
    except FileNotFoundError:
        pass
    df.to_csv('annotated.csv', encoding = 'cp1251')


if __name__ == "__main__":
    print('Привет! Спасибо за интерес к исследованию по разметке Двача. Чтобы начать, введи имя любой доступной борды без слэша, к примеру, набери: b')
    while (True):
        board = input()
        threads = load_page(board)
        if threads:
            break
    print('Отлично. Загружаем данные с ' + board + ', подожди минутку.')
    while (True):
        show_thread_names(get_thread_names(threads, board))
        print('Перед тобой список доступных тредов. Введи номер (id) треда из списка, к примеру, 1. Набери quit для прекращения работы.')
        while (True):
            id = input()
            if id == 'quit':
                print('Спасибо за работу!')
                amount = 0
                try:
                    amount = len(DataFrame.from_csv('annotated.csv', encoding = 'cp1251'))
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
        print('Отлично, работа с этим тредом закончена. Размечено ' + str(len(labels)) + ' сообщений')
        make_df(reference, comments[:len(labels)], labels)
        print('Данные сохранены. Теперь немного подожди, снова загружаем список тредов доски ' + board)
        threads = load_page(board)
