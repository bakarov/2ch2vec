from pickle import dump
from nltk import word_tokenize
from pandas import DataFrame

df = DataFrame.from_csv('dsr.csv')
inp = 5
VALUE = 2546

for i, k in df[VALUE:].iterrows():
    print(i)
    print('=======')
    print(k['comment'])
    print('-------')
    print(k['reference'])
    #print(i)
    while (True):
        inp = input()
        if inp == '1' or inp == '0' or inp == 'exit':
            break
    if inp == 'exit':
        df.to_csv('dsr.csv')
        print(i)
        break
    df.loc[i, 'is_related'] = int(inp)
    print('=======')
    print()

# replace all nines
