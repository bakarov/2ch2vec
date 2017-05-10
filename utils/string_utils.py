from re import sub, compile


def remove_html(text):
    html = compile(r'<.*?>')
    return html.sub('', text)


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
