#!/usr/bin/env python3


"""\
Generates a MALLET-style corpus CSV file of the words within a given term's
context."""


import argparse
import os
import sys

from barth import is_before_election
from barth.corpus import get_english_stopset, CsvCorpus
from barth.tagging import build_tagger


def load_corpus(corpus_dir, tagger, stopset):
    """Load and process the corpus."""
    print('loading {}...'.format(
        os.path.basename(os.path.dirname(corpus_dir)),
    ))
    corpus = CsvCorpus(corpus_dir, tagger, stopset)

    corpus.tokenize()
    corpus.filter_stopset()
    corpus.filter_short()
    corpus.tag_tokens()
    corpus.tag_rows(lambda row: int(not is_before_election(row)))

    return corpus


def focus_corpus(name, corpus, term, width):
    """\
    This processes a corpus to generate a MALLET CSV corpus with all the terms
    within 'width' words of 'term'.

    """
    print('writing {}.tsv...'.format(name))
    term_slash = term + '/'

    def focus(tokens):
        """\
        Return a new list of tokens of all the tokens around 'term'.
        """
        output = []
        for i, token in enumerate(tokens):
            if token.startswith(term_slash):
                output += tokens[i-width:i]
                output += tokens[i+1:i+width+1]
        return ' '.join(output)

    corpus._map(focus, 'tokens', 'focus')
    data = corpus.data
    print('data columns = {}'.format(data.columns))
    data.to_csv(
        name + '.tsv', sep='\t', header=False, index=False,
        columns=['filename', 'tag', 'focus'],
    )


def parse_args(argv=None):
    """Parses the command line."""
    argv = sys.argv[1:] if argv is None else argv
    parser = argparse.ArgumentParser(description=__doc__)

    cwd = os.getcwd()
    parser.add_argument('-c', '--corpus-collection', dest='corpus_collection',
                        action='store', default=cwd,
                        help='The parent directory containing the corpus '
                             'directories. Each subdirectory should contain a '
                             'corpus.csv file. Default is {}.'.format(cwd))
    parser.add_argument('-n', '--width', dest='n', default=3, type=int,
                        action='store',
                        help='The width of the context to search around the '
                             'term. Default = 3.')
    parser.add_argument('-t', '--term', dest='term', action='store',
                        help='The term to focus this corpus around.')

    return parser.parse_args(argv)


def main(argv=None):
    """main"""
    args = parse_args(argv)

    tagger = build_tagger()
    stopset = get_english_stopset()
    for name in os.listdir(args.corpus_collection):
        try:
            corpus = load_corpus(
                os.path.join(args.corpus_collection, name, 'corpus.csv'),
                tagger, stopset,
            )
        except:
            print('unable to load corpus {}. skipping.'.format(name))
        else:
            focus_corpus(name, corpus, args.term, args.n)


if __name__ == '__main__':
    main()
