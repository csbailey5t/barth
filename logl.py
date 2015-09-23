#!/usr/bin/env python3


import argparse
from collections import namedtuple
import os
import sys

import nltk
import nltk.probability


Location = namedtuple('Location', ['volpart', 'n', 'paragraph'])


def parse_args(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--corpus', metavar='CORPUS_DIR',
                        dest='corpus_dir',
                        help='The directory containing the corpus to '
                             'process.')
    parser.add_argument('-p', '--paragraph', metavar='PARAGRAPH_NO', type=int,
                        dest='paragraph',
                        help='The paragraph number to split the input on when '
                             'creating subcorpora.')
    parser.add_argument('-X', action='store_true', dest='cut_paragraph',
                        help='If given, drop the *paragraph* data from the '
                             'corpus.')
    parser.add_argument('-o', '--output', metavar='CSV_FILE',
                        dest='output',
                        help='The output CSV file.')

    args = parser.parse_args(argv)
    if (args.corpus_dir is None or args.paragraph is None or
        args.output is None):
        parser.error('You must supply all arguments.')
    return args


def tokenize_corpus(corpus_dir):
    """This tokenizes all the files in a directory, returning a dict
    from filename to tokens."""
    for (root, dirs, files) in os.walk(corpus_dir):
        for fn in files:
            full_fn = os.path.join(root, fn)
            with open(full_fn) as fin:
                yield (full_fn, nltk.word_tokenize(fin.read()))


def get_location(filename):
    """This returns the location of the filename in the *Dogmatics*, assuming
    that file names look like 'xx-yy-pp-name.txt':
      * *xx* is the volume and part number combined;
      * *yy* is a complete running paragraph number within a volpart; and
      * *pp* is the canoncial paragraph numbering.
    """
    basename = os.path.basename(filename)
    parts = [int(part) for part in basename.split('-')[:3]]
    return Location(*parts)


def split_list(input_list, fn):
    """This splits a list on a fn. The first item returned will be the
    first chunk where fn returns False, and the second item returns
    will be everything following."""
    input_list = list(input_list)
    prefix = []
    while input_list and not fn(input_list[0]):
        prefix.append(input_list.pop(0))
    return (prefix, input_list)


class IterableMixin:
    """This wraps an probability distribution to also iterate over its
    samples."""

    def __iter__(self):
        samples = list(self.samples())
        for s in samples:
            yield self.prob(s)


class IterableProbDist(nltk.probability.ELEProbDist, IterableMixin):
    pass


class RandIterableProbDist(nltk.probability.RandomProbDist, IterableMixin):
    pass


def create_pdist(corpusa, corpusb):
    """This returns a conditional probability distribution with the
    condition being which corpus the frequency is for."""
    cfdist = nltk.probability.ConditionalFreqDist()

    for (_, tokens) in corpusa:
        for token in tokens:
            cfdist[0][token] += 1
    for (_, tokens) in corpusb:
        for token in tokens:
            cfdist[1][token] += 1

    pdist = nltk.probability.ConditionalProbDist(
        cfdist,
        IterableProbDist,
    )
    return pdist


def main():
    args = parse_args()

    print('reading')
    corpus = [
        (get_location(fn), tokens)
        for (fn, tokens) in tokenize_corpus(args.corpus_dir)
    ]
    print('splitting')
    prefix, suffix = split_list(
        corpus,
        lambda c: c[0].paragraph == args.paragraph,
    )
    if args.cut_paragraph and suffix:
        suffix.pop(0)

    print('computing distributions')
    pdist = create_pdist(prefix, suffix)
    print('computing log likelihoods')

    logl0 = nltk.probability.log_likelihood(
        pdist[1],
        pdist[0],
    )
    logl1 = nltk.probability.log_likelihood(
        pdist[0],
        pdist[0],
    )
    logl2 = nltk.probability.log_likelihood(
        pdist[0],
        RandIterableProbDist(pdist[0].samples()),
    )

    print('log likelihood between corpora = {}'.format(logl0))
    print('log likelihood between identical corpora = {}'.format(logl1))
    print('log likelihood against a random distrbution = {}'.format(logl2))


if __name__ == '__main__':
    main()
