#!/usr/bin/env python3


"""\
Examines the similarity of pre- and post-election paragraphs by performing a
Wilcoxon signed-rank test on sufficiently occurring shared vocabulary in both
divisions of the Dogmatics.
"""


import argparse
import collections
import csv
import operator
import random
import sys

import numpy as np
from sparklines import sparklines
import scipy.stats

import barth
import barth.corpus
import barth.tagging


def make_samples(corpus, num_samples, sample_size, min_freq):
    """Make a number of samples for passing to the test.

    Returns a tuple pair of the list of tokens and a dictionary of the token
    groups and a list of vectors for each sample.
    """
    print('make-samples')
    samples = {}
    token_groups = {}
    token_set = None

    # Get the tokens for each group and their frequencies.
    # Also get a set of tokens that occur often enough.
    for name, group in corpus.data.groupby('tag'):
        tokens = []
        for doc in group['tokens']:
            tokens += doc
        token_groups[name] = tokens
        counts = collections.Counter(tokens)

        if token_set is None:
            token_set = {
                token for token, freq in counts.items() if freq >= min_freq
            }
        else:
            token_set &= {
                token for token, freq in counts.items() if freq >= min_freq
            }

    # Filter the tokens for each group by whether they are
    # found often enough.
    for name in list(token_groups.keys()):
        token_groups[name] = [
            token for token in token_groups[name] if token in token_set
        ]

    # Create token vectors.
    all_tokens = list(enumerate(sorted(list(token_set))))
    for name, tokens in token_groups.items():
        samples[name] = []
        for _ in range(num_samples):
            start = random.randrange(len(tokens) - sample_size)
            s_tokens = tokens[start:start+sample_size]
            counts = collections.Counter(s_tokens)
            v_array = [0] * len(s_tokens)
            for i, t in all_tokens:
                v_array[i] = counts[t]

            samples[name].append(np.array(v_array))

    return (all_tokens, samples)


def make_pairs(all_tokens, samples):
    """Return pairs of samples from each tag."""
    print('make-pairs')
    for i in range(len(all_tokens)):
        pair = {}
        for k, values in samples.items():
            pair[k] = np.array([v[i] for v in values])
        yield pair


def wilcoxon(pair, zero_method):
    keys = [p[1] for p in sorted(pair.items())]
    if any(p[0] - p[1] != 0 for p in zip(keys[0], keys[1])):
        try:
            return scipy.stats.wilcoxon(*keys, zero_method=zero_method)
        except ValueError:
            print('ERROR with ({})'.format(keys))
            raise
    else:
        return None


def load_corpus(corpus_csv):
    """Load and initialize the corpus."""
    print('load-corpus')
    corpus = barth.corpus.CsvCorpus(
        corpus_csv,
        tagger=barth.tagging.build_tagger(),
        stopset=barth.corpus.get_english_stopset(),
    )

    corpus.tokenize()
    corpus.filter_stopset()
    corpus.filter_short()
    corpus.filter_alnum()
    corpus.tag_tokens()
    corpus.tag_rows(lambda row: int(not barth.is_before_election(row)))

    return corpus


def parse_args(argv=None):
    """Parses command-line options."""
    argv = sys.argv[1:] if argv is None else argv
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-c', '--corpus', action='store', dest='corpus',
                        metavar='CORPUS_CSV_FILE',
                        help='The location of a `corpus.csv` file for a '
                             'corpus to process.')
    parser.add_argument('-n', '--num-samples', action='store', type=int,
                        dest='num_samples', metavar='N',
                        help='The number of samples in each group to create.')
    parser.add_argument('-k', '--k', action='store', dest='sample_size',
                        metavar='K', type=int,
                        help='The size of each sample.')
    parser.add_argument('-m', '--min-freq', action='store', dest='min_freq',
                        metavar='MINIMUM_FREQUENCY', type=int, default=5,
                        help='The minimum frequency of term to consider. '
                             'Default=5.')
    parser.add_argument('-z', '--zero-method', action='store',
                        default='wilcox', dest='zero_method',
                        metavar='ZERO_METHOD',
                        choices=('pratt', 'wilcox', 'zsplit'),
                        help='How to handle zero differences. One of pratt, '
                             'wilcox, or zsplit. The default is wilcox. '
                             'See http://docs.scipy.org/doc/scipy/reference'
                             '/generated/scipy.stats.wilcoxon.html '
                             'for details.')
    parser.add_argument('-o', '--output', action='store', dest='output',
                        metavar='CSV_FILE',
                        help='The CSV file to write the output to.')
    parser.add_argument('-w', '--word-list', action='store', dest='word_list',
                        metavar='WHITELIST_FILE',
                        help='A file listing the words that you are '
                             'interested in testing similarity.')

    args = parser.parse_args(argv)
    if args.corpus is None:
        parser.error('You must specify the corpus file location.')
    if args.output is None:
        parser.error('You must specify an output file.')

    return args


def main(argv=None):
    """main"""
    args = parse_args(argv)
    corpus = load_corpus(args.corpus)
    all_tokens, samples = make_samples(
        corpus,
        args.num_samples,
        args.sample_size,
        args.min_freq,
    )

    if args.word_list:
        with open(args.word_list) as fin:
            word_list = set(line.strip() for line in fin)
    else:
        word_list = None

    counts = corpus.count_vectorize()
    percs = corpus.percent_vectorize()

    print('wilcoxon')
    output_rows = []
    for token, pair in zip(all_tokens, make_pairs(all_tokens, samples)):
        if word_list is None or token[1] in word_list:
            w = wilcoxon(pair, args.zero_method)
            if w is not None:
                t = token[1].split('/')[0]
                output_rows.append((
                    token[1],
                    w.statistic,
                    w.pvalue,
                    '\n'.join(sparklines(counts[t])),
                    '\n'.join(sparklines(percs[t])),
                ))

    output_rows.sort(key=operator.itemgetter(2))
    with open(args.output, 'w') as fout:
        writer = csv.writer(fout)
        writer.writerows(output_rows)


if __name__ == '__main__':
    main()
