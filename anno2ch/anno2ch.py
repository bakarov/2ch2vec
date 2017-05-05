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
    except JSONDecodeError:
        print('No board with such name.')
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
        print('REFERENCE:')
        print(reference)
        print('MESSAGE:')
        print(i)
        while (True):
            label = input()
            if label == 'quit':
                return labels
            try:
                label = int(label)
            except ValueError:
                print('1 or 0')
                continue
            if label == 1 or label == 0:
                label = int(label)
                break
            else:
                print('1 or 0')
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
    print('Enter board name')
    while (True):
        board = input()
        threads = load_page(board)
        if threads:
            break
    print('Loading data from /' + board)
    while (True):
        show_thread_names(get_thread_names(threads, board))
        print('Enter thread id')
        while (True):
            id = input()
            if id == 'quit':
                exit('Thank for annotating')
            try:
                id = int(id)
            except ValueError:
                print('Print number!')
                continue
            if id >= 15:
                print('No such thread in list')
            else:
                break
        reference, comments = get_annotate_data(board, threads[id])
        labels = start_annotating(reference, comments)
        make_df(reference, comments[:len(labels)], labels)
        print('Done, loading thread list from /' + board)