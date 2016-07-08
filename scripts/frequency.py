#!/usr/bin/env python3


"""\
Prints the frequencies of a word in each file, by raw frequency,
percentage, or TF-IDF.

The '--values' option is made to work with
[spark](https://zachholman.com/spark/).
"""

import argparse
import sys

import barth
import barth.corpus
import barth.tagging


def load_corpus(corpus_csv):
    """Load and initialize the corpus."""
    corpus = barth.corpus.CsvCorpus(
        corpus_csv,
        tagger=barth.tagging.build_tagger(),
        stopset=barth.corpus.get_english_stopset(),
    )

    corpus.tokenize()
    corpus.filter_stopset()
    corpus.filter_short()
    corpus.filter_alnum()
    corpus.tag_rows(lambda row: int(not barth.is_before_election(row)))

    return corpus


def parse_args(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-c', '--corpus', action='store', dest='corpus',
                        metavar='CORPUS_CSV_FILE',
                        help='The location of a `corpus.csv` file for a '
                             'corpus to process.')
    parser.add_argument('-q', '--query', action='store', dest='query',
                        metavar='SEARCH_QUERY',
                        help='The term to find frequencies for.')
    parser.add_argument('-C', '--counts', action='store',
                        dest='counting_method',
                        metavar='COUNTING_METHOD',
                        choices=('raw', 'percentage', 'tfidf'),
                        default='raw',
                        help='How to report the frequency. One of '
                             'raw, percentage, or tfidf. Default '
                             'is raw.')
    parser.add_argument('--values', action='store_true',
                        help='Only display values.')

    args = parser.parse_args(argv)
    if args.corpus is None:
        parser.error('You must specify the corpus file location.')
    if args.query is None:
        parser.error('You must specify query term.')

    return args


def main(argv=None):
    args = parse_args(argv)
    corpus = load_corpus(args.corpus)

    if args.counting_method == 'raw':
        counts = corpus.count_vectorize()
    elif args.counting_method == 'percentage':
        counts = corpus.percent_vectorize()
    elif args.counting_method == 'tfidf':
        counts = corpus.tfidf_vectorize()
    else:
        raise ValueError('Invalid value for --counting: "{}"'.format(
            args.counting_method,
        ))

    corpus.data[args.query] = counts[args.query]
    if args.values:
        for v in corpus.data[args.query].values:
            print(v)
    else:
        print(corpus.data[['tag', args.query]])


if __name__ == '__main__':
    main()
