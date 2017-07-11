from collections import Counter
from os import path
from nltk.corpus import stopwords

lines = open(path.join('corpus', 'b_lem.txt')).readlines()
words = [w for l in lines for w in l.rstrip().split() if w.isalpha()]

counts = Counter(words)

k = 100
stop = set()
for w, c in sorted(counts.most_common(k), reverse=True):
    stop.add(w)

nltk_stop = set(stopwords.words('russian'))
my_stop = {'весь', 'всякий', 'тот', 'это', 'самое', 'каким', 'сама', 'никак', 'она', 'она', 'оно', 'какие', 'какого', 'которая', 'многое', 'чему', 'всему', 'раза', 'сразу', 'весь', 'раз', 'пор', 'например', 'вроде', 'которые', 'который', 'просто', 'очень', 'почему', 'вообще', 'ещё', 'типа', 'ради', 'всё', 'хотя', 'тебе', 'нужно', 'пока'}
my_stop_verb = {'сделать', 'можешь', 'могу', 'могут', 'делать', 'будешь', 'быть', 'будут', 'смочь'}

stop = stop.union(nltk_stop, my_stop, my_stop_verb)

open(path.join('corpus', 'stopwords.txt'), 'w').write('\n'.join(stop))
