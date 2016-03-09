#!/usr/bin/env python3


import argparse
from collections import Counter
from contextlib import closing
import csv
import os
import sys
import sqlite

from nltk.corpus import stopwords

from barth.tagging import build_tagger
from barth.corpus import get_english_stopset, Corpus
import classify


SCHEMA = """
CREATE TABLE IF NOT EXISTS files (
  id INTEGER PRIMARY KEY,
  tag TEXT,
  filename TEXT,
  token_count INTEGER,
  CONSTRAINT UNIQUE (filename)
);
CREATE TABLE IF NOT EXISTS word_types (
  id INTEGER PRIMARY KEY,
  text TEXT,
  tag TEXT,
  CONSTRAINT UNIQUE (text, tag)
);
CREATE TABLE IF NOT EXISTS collocates (
  id INTEGER PRIMARY KEY,
  file_id INTEGER,
  center_id INTEGER,
  col_id INTEGER,
  frequency INTEGER,
  FOREIGN KEY (file_id) REFERENCES files(id),
  FOREIGN KEY (center_id) REFERENCES word_types(id),
  FOREIGN KEY (col_id) REFERENCES word_types(id)
);
"""


def opendb(filename):
    """This opens the database and creates the schema."""
    cxn = sqlite.connect(filename)
    with closing(cxn.cursor()) as c:
        c.executescript(SCHEMA)
    return cxn


def collocates(seq, i, j=None):
    """\
    This iterates over the collocates in seq. It goes from i before to
    j behind the current item. By default, j is the same as i.
    """

    j = i if j is None else j
    len_seq = len(seq)
    for x in range(len_seq):
        current = seq[x]
        for y in range(max(0, x - i), min(x + j + 1, len_seq)):
            yield (current, seq[y])


def get_counter(index, key):
    """Gets a Counter from a dict, creating it if necessary."""
    counter = index.get(key)
    if counter is None:
        counter = Counter()
        index[key] = counter
    return counter


def corpus_collocates(dirnames, tagger, stopset, term=None):
    if term is not None:
        term += '/'

    term_freqs = []
    tag_freqs = {}

    corpus = Corpus(dirnames, tagger, stopset)
    for (filename, tag, tokens) in corpus.tokenize_corpus():
        tag_counter = get_counter(tag_freqs, tag)

        cols = collocates(tokens, 5)
        if term is not None:
            cols = (d for c, d in cols if c.lower().startswith(term))
        cols = list(cols)

        freqs = Counter(cols)
        tag_counter.update(cols)
        term_freqs.append((tag, filename, freqs, len(cols), len(tokens)))

    return (tag_freqs, term_freqs)


def parse_args(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-c', '--corpus', dest='corpus', action='append',
                        default=classify.CORPUS,
                        help='The input directory containing the training '
                        'corpus.')
    parser.add_argument('-t', '--term', dest='term', action='store',
                        help='The term to search for.')
    parser.add_argument('-o', '--output', dest='output',
                        action='store', default='collocates.csv',
                        help='The file to write the output files to. '
                        ' Default = ./collocates.csv')

    return parser.parse_args(argv)


def main():
    args = parse_args()

    stopset = set(stopwords.words('english'))
    tagger = classify.build_tagger()
    tag_freqs, term_freqs = corpus_collocates(args.corpus, tagger, stopset,
                                              args.term)
    with open(args.output, 'w') as fout:
        writer = csv.writer(fout)
        writer.writerow(COL_HEADER)


if __name__ == '__main__':
    main()
