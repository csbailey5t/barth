"""\
Create a Matrix Market file for a corpus directory, which defaults to
the current directory.
"""


import argparse
from collections import Counter
import operator
import os
import sys

import gensim
import nltk


tokenize = nltk.wordpunct_tokenize


def tokenize_corpus(corpus_dir):
    """This tokenizes all the files in a directory, returning a dict
    from filename to tokens."""
    for (root, dirs, files) in os.walk(corpus_dir):
        for fn in files:
            full_fn = os.path.join(root, fn)
            with open(full_fn) as fin:
                yield (full_fn, tokenize(fin.read()))


def save_file_list(basename, corpus):
    output = basename + '.files'
    print('saving file list to {}.'.format(output))
    with open(output, 'w') as f:
        f.writelines(path + '\n' for (path, _) in corpus)


def save_dictionary(basename, dictionary):
    output = basename + '.dictionary'
    print('saving dictionary to {}.'.format(output))
    dictionary.save(output)


def save_token_list(basename, dictionary):
    output = basename + '.tokens'
    print('saving token list to {}.'.format(output))
    with open(output, 'w') as f:
        pairs = dictionary.items()
        pairs.sort(key=operator.itemgetter(0))
        f.writelines('{}\t{}\n'.format(*pair) for pair in pairs)


def save_mm(basename, mm):
    output = basename + '.mm'
    print('saving MM to {}.'.format(mm))
    gensim.corpora.MmCorpus.serialize(output)


def over_tokens(corpus, f):
    """This destructively maps f over the sequence of tokens in a corpus."""
    for (i, (full_fn, tokens)) in enumerate(corpus):
        corpus[i] = (full_fn, f(tokens))


def filter_tokens(corpus, pred):
    """This filters the tokens in a corpus according to the predicate f.
    This modifies corpus in place."""
    over_tokens(corpus, lambda tokens: (t for t in tokens if pred(t)))


def map_tokens(corpus, f):
    """This destructively maps f over the tokens in the corpus."""
    over_tokens(corpus, lambda tokens: (f(t) for t in tokens))


def freeze_tokens(corpus):
    """This freezes the token generator into a list."""
    over_tokens(corpus, list)


def calculate_frequencies(tokens):
    """\
    This calculates the frequencies in a token sequence and returns a dict.
    """
    return dict(Counter(tokens))


def parse_args(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--corpus', metavar='CORPUS_DIR',
                        dest='corpus_dir',
                        help='The directory containing the corpus to '
                             'process.')
    parser.add_argument('-s', '--stop-list', metavar='STOPLIST_FILE',
                        dest='stop_list', default=None,
                        help='The stop list file.')
    parser.add_argument('--stem', action='store_true',
                        dest='stem', default=False,
                        help='Stem the words? Default is no.')
    parser.add_argument('-l', '--min-word-length', metavar='LENGTH',
                        dest='min_word_len', default=None, type=int,
                        help='If given, filter the words for the minimum '
                             'length.')
    parser.add_argument('-f', '--min-word-freq', metavar='FREQUENCY',
                        dest='min_word_freq', default=None, type=int,
                        help="Cull words that aren't found very often.")
    parser.add_argument('-F', '--fold-case', action='store_true',
                        dest='fold_case', default=False,
                        help='Do we fold the case of incoming tokens?')
    parser.add_argument('-o', '--output', metavar='BASE_NAME',
                        dest='output',
                        help='The base name of all of the '
                        'various output files.')

    args = parser.parse_args(argv)
    return args


def main():
    args = parse_args()
    corpus = list(tokenize_corpus(args.corpus_dir))

    if args.fold_case:
        print('folding case...')
        map_tokens(corpus, lambda t: t.lower())

    if args.stop_list is not None:
        print('filtering stop list...')
        with open(args.stop_list) as f:
            stop_words = set(tokenize(f.read()))
        filter_tokens(corpus, lambda t: t not in stop_words)

    if args.min_word_len is not None:
        print('filtering by length...')
        filter_tokens(corpus, lambda t: len(t) >= args.min_word_len)

    if args.stem:
        print('stemming...')
        stemmer = nltk.stem.snowball.SnowballStemmer('english')
        map_tokens(corpus, stemmer.stem)

    freeze_tokens(corpus)

    over_tokens(corpus, calculate_frequencies)
    if args.min_word_freq is not None:
        print('filtering by token')
        over_tokens(
            corpus,
            lambda freqs: dict(
                (t, f)
                for (t, f) in freqs.items()
                if f >= args.min_word_freq
            )
        )

    corpus.sort(key=operator.itemgetter(0))
    print('creating the dictionary...')
    dictionary = gensim.corpora.dictionary.Dictionary(
        [tokens for (_, tokens) in corpus]
    )
    mm = [dictionary.doc2bow(tokens) for (_, tokens) in corpus]
    save_file_list(args.output, corpus)
    save_dictionary(args.output, dictionary)
    save_token_list(args.output, dictionary)
    save_mm(args.output, mm)

    print('done')


if __name__ == '__main__':
    main()
