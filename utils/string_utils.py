from re import sub, compile
from os import path
from pymorphy2 import MorphAnalyzer
from nltk.tokenize import word_tokenize

morph = MorphAnalyzer()


with open(path.join('corpus', 'stopwords.txt')) as f:
    stopwords = set(f.read().splitlines())


def remove_html(text):
    html = compile(r'<.*?>')
    return html.sub('', text)

def make_tokens(text, vocab):
    return [token for token in word_tokenize(text) if token in vocab]


def morph_parse(text):
    return ' '.join([morph.parse(word)[0].normal_form for word in word_tokenize(text) if morph.parse(word)[0].normal_form not in stopwords])


def cut(text):
    r = compile(r'\(OP\)|&#(\d*);|&quot;|&gt;|&#47;|(http|https):.*')
    return r.sub('', make_alpha(remove_html(punctuate_sent(punctuate_word(text))))).lower().strip()


def make_alpha(text):
    alpha = compile('[^a-zа-яA-ZА-Я,\.\?! ]')
    return alpha.sub('', text)


def punctuate_sent(data):
    r = compile(r'([a-zA-Zа-яА-Я])([.!\?])')
    return r.sub(r'\1. ', data)


def punctuate_word(data):
    r = compile(r'([a-zA-Zа-яА-Я])([,])')
    return r.sub(r'\1, ', data)
