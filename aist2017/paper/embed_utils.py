import numpy as np
import mmap
import numpy as np
import os
import struct

def ugly_normalize(vecs):
    normalizers = np.sqrt((vecs * vecs).sum(axis=1))
    normalizers[normalizers == 0] = 1
    return (vecs.T / normalizers).T


class Word2VecF:
    def __init__(self, vecsfile, vocabfile=None, normalize=True):
        if vocabfile is None: vocabfile = vecsfile.replace("npy", "vocab")
        self._vecs = np.load(vecsfile)
        self._vocab = open(vocabfile).read().split()
        if normalize:
            self._vecs = ugly_normalize(self._vecs)
        self._w2v = {w: i for i, w in enumerate(self._vocab)}

        
    @classmethod
    def load(cls, vecsfile, vocabfile=None):
        return Word2VecF(vecsfile, vocabfile)

    
    def word2vec(self, w):
        return self._vecs[self._w2v[w]]

    
    def similar_to_vec(self, v, N=10):
        sims = self._vecs.dot(v)
        sims = heapq.nlargest(N, zip(sims, self._vocab, self._vecs))
        return sims

    
    def most_similar(self, word, N=10):
        w = self._vocab.index(word)
        sims = self._vecs.dot(self._vecs[w])
        sims = heapq.nlargest(N, zip(sims, self._vocab))
        return sims
    

class Swivel(object):
    def __init__(self, vocab_filename, rows_filename, cols_filename=None):
        with open(vocab_filename, 'r') as lines:
            self.vocab = [line.split()[0] for line in lines]
            self.word_to_idx = {word: idx for idx, word in enumerate(self.vocab)}
        n = len(self.vocab)

        with open(rows_filename, 'r') as rows_fh:
            rows_fh.seek(0, os.SEEK_END)
            size = rows_fh.tell()
            if size % (4 * n) != 0:
                raise IOError('unexpected file size for binary vector file %s' % rows_filename)
            dim = int(size / (4 * n))
            rows_mm = mmap.mmap(rows_fh.fileno(), 0, prot=mmap.PROT_READ)
            rows = np.matrix(np.frombuffer(rows_mm, dtype='float32').reshape(n, dim))
            self.vecs = rows / np.linalg.norm(rows, axis=1).reshape(n, 1)
            rows_mm.close()
         

    def similarity(self, word1, word2):
        idx1 = self.word_to_idx.get(word1)
        idx2 = self.word_to_idx.get(word2)
        if not idx1 or not idx2:
            return None
        return float(self.vecs[idx1] * self.vecs[idx2].transpose())

    def neighbors(self, query):
        if isinstance(query, basestring):
            idx = self.word_to_idx.get(query)
            if idx is None:
                return None

            query = self.vecs[idx]
        neighbors = self.vecs * query.transpose()
        return sorted(
            zip(self.vocab, neighbors.flat),
            key=lambda kv: kv[1], reverse=True)

    def lookup(self, word):
        idx = self.word_to_idx.get(word)
        return None if idx is None else self.vecs[idx]
    
    
def cosine_sim(word1, word2):
    return 1 - spatial.distance.cosine(wv(word1), wv(word2))

def wv(glove, word):
    return glove.word_vectors[glove.dictionary[word]]

def get_adagram_sense_prob(ada_model, word):
    current_prob = 0
    current_key = 0
    for prob in ada_model.word_sense_probs(word):
        if prob[1] > current_prob:
            current_prob = prob[1]
            current_key = prob[0]
    return current_key
