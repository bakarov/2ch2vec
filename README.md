### Automated Detection of Non-Relevant Posts on the Russian Imageboard 2ch: Importance of the Choice of Word Representations

Repostiry with code, dataset and and links to the models proposed in the paper.

Results of the comparison of the word embedding models are in the Jupyter notebooks at the directory `paper`:

* `semantic_relatedness.ipynb` for the semantic relatedness task
* `word_similarity.ipynb` for the word similarity task

To reproduce the results of the experiments, download folders [`models`](https://yadi.sk/d/tFHYZcCQ3KxEac) and [`datasets`](https://yadi.sk/d/c_pg4k6b3KxEkr) and place them into `paper` folder. Then the following Python 3.X packages should be installed:

* gensim
* pandas
* numpy
* scikit-learn
* nltk
* pymorphy2
* matplotlib
* seaborn
* [glove-python](https://github.com/maciejkula/glove-python)
* [python-adagram](https://github.com/lopuhin/python-adagram)

After that, one can try to execute code in the notebooks.

*2ch Semantic Relatedness Dataset* could be found at `paper/datasets`.

Models compared in the study:

* [Word2Vec (CBOW)](https://github.com/RaRe-Technologies/gensim). Computation of the prediction loss of the target words from the context words.
* [GloVe](https://github.com/maciejkula/glove-python). Dimensionality reduction on the co-occurrence matrix.
* [Word2Vec-f](https://bitbucket.org/yoavgo/word2vecf). Extension of Word2Vec with the use of arbitrary context features of dependency parsing. For training Word2Vec-f the raw corpus was represented in CONLL-U format through the parsing of SyntaxNet Parsey McParseface trained on SynTagRus.
* [Wang2Vec (Structured Skip-N-Gram)](https://github.com/wlin12/wang2vec). Extension of Word2Vec with the sensitivity to the word order.
* [AdaGram](https://github.com/lopuhin/python-adagram). Extension of Word2Vec learning multiple word representations with capturing different word meanings. Since AdaGram has an opportunity to predict multiple meanings for a single word, we used the most probable predicted meaning..
* [FastText (CBOW)](https://github.com/facebookresearch/fastText). Extension of Word2Vec which represents words as bags of character n-grams.
* [Swivel](https://github.com/tensorflow/models/tree/master/swivel) Capturing unobserved (word, context) pairs in sub-matrices of a co-occurrence matrix.

All of the models were trained on the [lemmatized corpus of posts from 2ch](https://yadi.sk/d/TXY9XRxn3KxFjs).

If you have any questions, feel free to contact me: `a.bakarov@expasoft.ru`
