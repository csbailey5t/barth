#!/usr/bin/env python3


import argparse
import csv
import sys

import nltk


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
    parser.add_argument('-o', '--output', metavar='CSV_FILE',
                        dest='output',
                        help='The output CSV file.')

    args = parser.parse_args(argv)
    if (args.corpus_dir is None or args.paragraph is None or
        args.output is None):
        parser.error('You must supply all arguments.')
    return args


def main():
    args = parse_args()
    print(args)


if __name__ == '__main__':
    main()
