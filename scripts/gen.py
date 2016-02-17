import os
import gensim
from gensim import utils, corpora


def iter_documents(paragraphs):
    for fname in os.listdir(paragraphs):
        document = open(os.path.join(paragraphs, fname)).read()
        yield utils.simple_preprocess(document)


class BarthCorpus(object):
    def __init__(self, paragraphs):
        self.paragraphs = paragraphs
        self.dictionary = corpora.Dictionary(iter_documents(paragraphs))
        self.dictionary.filter_extremes()

    def __iter__(self):
        for tokens in iter_documents(self.paragraphs):
            yield self.dictionary.doc2bow(tokens)

corpus = BarthCorpus('paragraphs/')

lda = gensim.models.ldamodel.LdaModel(
    corpus,
    id2word=corpus.dictionary,
    num_topics=20)

lda.print_topics()
