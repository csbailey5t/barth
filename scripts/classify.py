#!/usr/bin/env python3


import argparse
from collections import namedtuple
import csv
from multiprocessing import Pool
import operator
import os
import pickle
import sys

import numpy as np
import pandas
from sklearn import cross_validation as xv
from sklearn import ensemble
from sklearn import linear_model as lm
from sklearn import naive_bayes as nb
from sklearn import svm
from sklearn import tree
from sklearn.base import clone
from sklearn.feature_selection import VarianceThreshold
from sklearn.metrics import (
    confusion_matrix, precision_score, recall_score, f1_score
)

from barth import is_before_election, is_election, is_after_election
from barth.corpus import get_english_stopset, CsvCorpus
from barth.tagging import build_tagger


TEST_SET_RATIO = 0.2
RESULTS_HEADER = [
    'classifier_name',
    'test_ratio',
    'feature_count',
    'select_features',
    'ngram_range',
    'precision',
    'recall',
    'f1',
    'true_positives',
    'true_negatives',
    'false_positives',
    'false_negatives',
]

CLASSIFIERS = [
    nb.GaussianNB,
    lm.LogisticRegression,
    svm.SVC,
    tree.DecisionTreeClassifier,
    ensemble.RandomForestClassifier,
]


ArgTuple = namedtuple(
    'ArgTuple',
    ('corpus', 'ratio', 'feature_file', 'ngram_range', 'select_features',
        'result_fields', 'min_df')
)


first = operator.itemgetter(0)
second = operator.itemgetter(1)


def read_corpus_features(csv_file, stopset=None, tfidf_args=None):
    """This reads a list of directories and pulls the features from its
    documents. The tag for each document is its immediate directory's
    name."""
    corpus = ClassifierCorpus(
        csv_file, tagger=build_tagger(), stopset=stopset,
        tfidf_args=tfidf_args,
    )

    corpus.tokenize()
    corpus.filter_stopset()
    corpus.filter_short()
    corpus.tag_tokens()
    corpus.tag_rows()

    return corpus


def report_classifier(classifier, confusion_matrix, precision, recall, f1):
    title = repr(classifier)
    print(title)
    print('=' * max(len(tline) for tline in title.splitlines()))
    print(confusion_matrix)
    print('precision = {}'.format(precision))
    print('recall    = {}'.format(recall))
    print('F1        = {}'.format(f1))
    print()
    sys.stdout.flush()


class ClassifierCorpus(CsvCorpus):

    def __init__(self, file, tagger=None, stopset=None, tfidf_args=None):
        super(ClassifierCorpus, self).__init__(file, tagger, stopset)
        self.file = file
        self.tfidf_args = None
        self.__tfidf = None
        self.__array = None
        self.labels = np.array([0, 1])

    @staticmethod
    def tag_row(row):
        return int(not is_before_election(row))

    def tag_rows(self):
        return super(ClassifierCorpus, self).tag_rows(self.tag_row)

    @property
    def tfidf(self):
        if self.__tfidf is None:
            tfidf_args = {} if self.tfidf_args is None else self.tfidf_args
            self.__tfidf = self.tfidf_vectorize(**tfidf_args)
        return self.__tfidf

    @property
    def array(self):
        if self.__array is None:
            self.__array = self.tfidf.values
        return self.__array

    @property
    def targets(self):
        return self.data['tag']

    def select_features(self, threshold=0.0):
        selector = VarianceThreshold(threshold=threshold)
        tfidf = self.tfidf
        selector.fit(tfidf)
        self.__tfidf = pandas.DataFrame(
            selector.transform(tfidf),
            columns=tfidf.columns[selector.get_support(True)],
            index=tfidf.index,
        )
        return self.__tfidf

    def cross_validate(self, classifier, k=10, verbose=0):
        """Run k-fold cross validation on the data in this corpus."""
        return xv.cross_val_score(
            classifier, self.array, self.targets, cv=k, verbose=verbose
        )

    def confused_x_validate(self, classifier, k=10):
        """\
        Run k-fold cross validation and return the scores and confusion
        matrixes."""
        X = self.array
        y = self.targets
        kf = xv.KFold(len(y), n_folds=k)

        for (train_index, test_index) in kf:
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]

            classifier2 = clone(classifier)
            self.fit(classifier2, X_train, y_train)
            predict = self.predict_all(classifier2, X_test)

            c_matrix = confusion_matrix(y_test, predict)
            precision = precision_score(y_test, predict, average='binary',
                                        labels=self.labels)
            recall = recall_score(y_test, predict, average='binary',
                                  labels=self.labels)
            f1 = f1_score(y_test, predict, average='binary',
                          labels=self.labels)

            yield {
                'classifier': classifier2,
                'confusion_matrix': c_matrix,
                'precision': precision,
                'recall': recall,
                'f1': f1,
            }

    def fit(self, classifier, X=None, y=None):
        """Train a classifier on this corpus or other data."""
        X = X if X is not None else self.array
        y = y if y is not None else self.targets
        classifier.fit(X, y)

    def predict(self, classifier, i):
        """Predict for the ith sample in this corpus."""
        return self.predict_all(classifier, self.array[i:i+1])[0]

    def predict_all(self, classifier, X=None):
        """Predict based on all inputs, which default to this corpus."""
        X = X if X is not None else self.array
        return classifier.predict(X)


class Job:

    def __init__(self, cls, args, chunking):
        self.cls = cls
        self.args = args
        self.chunking = chunking
        self.__corpus = None

    @classmethod
    def make_jobs(cls, args):
        for classifier_cls in CLASSIFIERS:
            yield cls(classifier_cls, args, None)

    def get_corpus(self):
        if self.__corpus is None:
            self.__corpus = self.load_corpus()
        return self.__corpus

    def set_corpus(self, corpus):
        self.__corpus = corpus

    def del_corpus(self):
        self.__corpus = None

    corpus = property(get_corpus, set_corpus, del_corpus)

    def get_frozen_file(self):
        if self.args.ngram_range:
            ngram = '_'.join(str(n) for n in self.args.ngram_range)
        else:
            ngram = 1

        if not os.path.exists('frozen'):
            os.makedirs('frozen')
        return 'frozen/{}-{}-{}-{}.pickle'.format(
            self.chunking, ngram, self.args.select_features, self.args.min_df,
        )

    def freeze_corpus(self):
        corpus = self.corpus
        with open(self.get_frozen_file(), 'wb') as fout:
            buf = pickle.dumps(corpus, -1)

            i = 0
            window = 2**30
            while i < len(buf):
                fout.write(buf[i:i+window])
                i += window

    def thaw_corpus(self):
        filename = self.get_frozen_file()
        if os.path.exists(filename):
            try:
                with open(filename, 'rb') as fin:
                    buf = b''
                    window = 2**30
                    while True:
                        tmp = fin.read(window)
                        buf += tmp
                        if not tmp:
                            break
                    self.corpus = pickle.loads(buf)
            except OSError:
                sys.stderr.write('ERROR reading {}:'.format(filename))
                raise

    def load_corpus(self):
        args = self.args

        corpus = read_corpus_features(
            args.corpus,
            get_english_stopset(),
            tfidf_args={
                'ngram_range': args.ngram_range,
                'min_df': args.min_df,
            },
        )
        corpus.tfidf
        if args.select_features is not None:
            corpus.select_features(args.select_features)

        if args.feature_file:
            with open(args.feature_file, 'w') as fout:
                for row in corpus.tfidf.columns:
                    fout.write('{}\n'.format(row))

        return corpus

    def classify(self, debug=False):
        cls, args = self.cls, self.args
        corpus = self.corpus

        feature_count = len(corpus.tfidf.columns)
        if args.ngram_range:
            ngram_range = '-'.join(str(x) for x in args.ngram_range)
        else:
            ngram_range = 1

        cls_name = cls.__name__
        if debug:
            print("{}...".format(cls_name))
        classifier = cls()

        for result in corpus.confused_x_validate(classifier):
            report_classifier(**result)

            cmatrix = result['confusion_matrix']
            result.update(args.result_fields)
            result.update(
                classifier_name=cls_name,
                test_ratio=args.ratio,
                feature_count=feature_count,
                select_features=args.select_features,
                ngram_range=ngram_range,
                true_positives=try_index(cmatrix, 0, 0),
                false_negatives=try_index(cmatrix, 0, 1),
                false_positives=try_index(cmatrix, 1, 0),
                true_negatives=try_index(cmatrix, 1, 1),
            )
            yield result


def int_pair(value):
    return tuple(int(x) for x in value.split('-'))


def try_index(matrix, x, y):
    try:
        v = matrix[x][y]
    except IndexError:
        v = 0.0
    return v


def parse_args(argv=None):
    """This parses the command line."""
    argv = sys.argv[1:] if argv is None else argv
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-c', '--corpus', dest='corpus', action='store',
                        help='The input CSV file containing the training '
                             'corpus.')
    parser.add_argument('-r', '--ratio', dest='ratio', type=float,
                        default=TEST_SET_RATIO,
                        help='The ratio of documents to use as a test set. '
                        'Default = {}'.format(TEST_SET_RATIO))
    parser.add_argument('-f', '--feature-file', dest='feature_file',
                        action='store', default=None,
                        help='If given, write the features used to a file.')
    parser.add_argument('-n', '--ngram-range', dest='ngram_range',
                        action='store', default=None, type=int_pair,
                        help='If given, sets a range of n-grams to use for '
                             'features. Formatted like FROM-TO. E.g., 1-3.')
    parser.add_argument('-F', '--select-features', dest='select_features',
                        action='store', default=False, type=float,
                        help='Select features.')
    parser.add_argument('-R', '--results', dest='results_file', action='store',
                        default=os.devnull,
                        help='A CSV file to write results to as they\'re '
                             'output. Default = {}.'.format(os.devnull))
    parser.add_argument('--result-field', dest='result_fields', action='append',
                        help='Fields with constant values to include in the '
                             'results file. Formatted like "field:value"')
    parser.add_argument('--min-df', dest='min_df', action='store',
                        type=int,
                        help='Minimum document frequency allowed. Any '
                             'less than this will be culled.')

    return parser.parse_args(argv)


def main(argv=None):
    """The main function."""
    args = parse_args(argv)

    result_fields = dict(fv.split(':', 1) for fv in args.result_fields)
    results_new = not os.path.exists(args.results_file)
    results_header = sorted(result_fields.keys()) + RESULTS_HEADER
    with open(args.results_file, 'a') as fout:
        writer = csv.DictWriter(fout, results_header, extrasaction='ignore')
        if results_new:
            writer.writeheader()

        with Pool() as pool:
            for result in pool.map(lambda j: j.classify(),
                                   Job.make_jobs(args)):
                writer.writerow(result)

    print('done.')


if __name__ == '__main__':
    main()
