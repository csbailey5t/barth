#!/usr/bin/env python


import argparse
from collections import Counter
import csv
import itertools
from multiprocessing.pool import Pool
import operator
import os
import pickle
import random
import statistics
import sys

import nltk
import nltk.corpus
from nltk.corpus import brown, names, stopwords
# from nltk.probability import ConditionalFreqDist
from sklearn.base import clone
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import cross_validation as xv
from sklearn.metrics import confusion_matrix
from sklearn import naive_bayes as nb
import numpy as np

from barth.corpus import get_english_stopset, Corpus
from barth.tagging import build_tagger


CORPUS = [
    'texts/paragraphs_before_election',
    'texts/paragraphs_after_election',
    ]
TEST_SET_RATIO = 0.2
TAGGER_CACHE = '.tagger.pickle'


first = operator.itemgetter(0)
second = operator.itemgetter(1)


def produce_confusion_matrix(test_features, classifier):
    """Produces a confusion matrix for the test classifier"""

    gold = [feature for (__, feature) in test_features]
    test = [classifier.classify(features) for (features, __) in test_features]
    cm = nltk.ConfusionMatrix(gold, test)
    print(cm.pretty_format(sort_by_count=True, show_percents=True, truncate=9))


def cross_validate(cls, training_features, num_folds=10):
    """Takes a set of classifier builder, training features, trains a
    classifier based on it, and cross validates it against a specified
    number of folds. Prints out the average accuracy for the
    classifier across num_folds as well as the individual accuracies
    for the subsections."""
    print('Cross validating {}'.format(cls.__name__))
    accuracies = []
    subset_size = int(len(training_features) / num_folds)
    for i in range(num_folds):

        accuracy = 0
        testing_this_round = training_features[i*subset_size:][:subset_size]
        training_this_round = (training_features[:i*subset_size] +
                               training_features[(i+1)*subset_size:])
        classifier = cls.train(training_this_round)
        accuracy = nltk.classify.accuracy(classifier, testing_this_round)
        accuracies.append(accuracy)
        print('Accuracy for fold {} = {}'.format(i, accuracy))

    average = sum(accuracies) / num_folds

    print('Cross-validated accuracy = {}'.format(average))
    return average


def cross_validate_sets(cls, training_features, num_folds=10):
    """Takes a set of classifier builder, training features, trains a
    classifier based on it, and cross validates it against a specified
    number of folds. It yields the classifier class and accuracy."""
    subset_size = int(len(training_features) / num_folds)
    for i in range(num_folds):
        testing_this_round = training_features[i*subset_size:][:subset_size]
        training_this_round = (training_features[:i*subset_size] +
                               training_features[(i+1)*subset_size:])
        yield (cls, training_this_round, testing_this_round)


def cross_validate_p(cls, training, test):
    """This performs the cross-validation on one fold."""
    classifier = cls.train(training)
    accuracy = nltk.classify.accuracy(classifier, test)
    return (cls, accuracy)


def cross_validate_means(accuracies):
    """This takes the means output from cross_validate_p, groups them
    by class, and averages them. It yields the classes and averages."""
    accuracies = list(accuracies)
    accuracies.sort(key=lambda x: first(x).__name__)
    for (cls, accuracy) in itertools.groupby(accuracies, first):
        yield (cls, statistics.mean(x for (_, x) in accuracy))


def get_sets(featuresets, ratio):
    """This breaks a sequence of feature sets into two groups based on
    the ratio."""
    test_size = int(ratio * len(featuresets))
    test_set = featuresets[:test_size]
    training_set = featuresets[test_size:]
    return (test_set, training_set)


def get_baseline(cls, training, test, base_value):
    """This returns the accuracy for a baseline training, i.e.,
    training based on everything being `base_value`."""
    baseline = [(fs, base_value) for (fs, _) in training]
    classifier = cls.train(baseline)
    return nltk.classify.accuracy(classifier, test)


def report_classifier(cls, accuracy, training, test, featureset, outdir):
    """This reports on a classifier, comparing it to a baseline, and
    pickling it into a directory."""
    name = cls.__name__
    output = os.path.join(outdir, name + '.pickle')
    baseline = get_baseline(cls, training, test, False)
    classifier = cls.train(featureset)
    with open(output, 'wb') as fout:
        pickle.dump(classifier, fout)
    return (output, accuracy, baseline)


tokenize = nltk.wordpunct_tokenize


def tokenize_corpus(corpus_dir):
    """This tokenism all the files in a directory, returning a dict
    from filename to tokens."""
    print('walking {}'.format(corpus_dir))
    corpus = Corpus([corpus_dir])
    return corpus.tokenize_corpus()


def read_corpus_features(directories, stopset=None):
    """This reads a list of directories and pulls the features from its
    documents. The tag for each document is its immediate directory's
    name."""
    corpus_tokenizer = Corpus(
        directories, tagger=build_tagger(), stopset=stopset,
    )
    corpus = TfidfCorpus(
        list(corpus_tokenizer.walk_corpus()),
        corpus_tokenizer.tokenize,
    )
    return corpus


class TfidfCorpus:

    def __init__(self, files, tokenizer=None):
        self.files = files
        self.targets = None
        self.target_key = None
        self.tfidf = None
        self.__dense = None

        self.categorize()
        self.read_corpus(tokenizer)

    def __repr__(self):
        return "<TfidfCorpus {}>".format(self.tfidf.getnnz())

    def categorize(self):
        """Identify the documents' categories based on the directory structure.
        """
        target_key = {}
        targets = []
        for filename in self.files:

            target = os.path.basename(os.path.dirname(filename))
            index = target_key.setdefault(target, len(target_key) + 1)
            targets.append(index)
        self.targets = np.array(targets)
        self.target_key = target_key

    def read_corpus(self, tokenizer=None):
        """Tokenize the corpus documents and run TF*IDF on them."""
        vectorizer = TfidfVectorizer(
            input='filename',
            tokenizer=tokenizer,
        )
        self.tfidf = vectorizer.fit_transform(self.files)

    @property
    def dense(self):
        if self.__dense is None:
            self.__dense = self.tfidf.todense()
        return self.__dense

    def cross_validate(self, classifier, k=10, verbose=0):
        """Run k-fold cross validation on the data in this corpus."""
        return xv.cross_val_score(
            classifier, self.dense, self.targets, cv=k, verbose=verbose
        )

    def confused_x_validate(self, classifier, k=10):
        """\
        Run k-fold cross validation and return the scores and confusion
        matrixes."""
        X = self.dense
        y = self.targets
        kf = xv.KFold(len(y), n_folds=k)
        for (train_index, test_index) in kf:
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            print('training size = {} ; test size = {}'.format(
                len(X_train), len(X_test),
            ))
            classifier2 = clone(classifier)
            self.fit(classifier2, X_train, y_train)
            predict = self.predict_all(classifier2, X_test)
            c_matrix = confusion_matrix(y_test, predict)
            yield {
                'classifier': classifier2,
                'confusion_matrix': c_matrix,
            }

    def fit(self, classifier, X=None, y=None):
        """Train a classifier on this corpus or other data."""
        X = X if X is not None else self.dense
        y = y if y is not None else self.targets
        classifier.fit(X, y)

    def predict(self, classifier, i):
        """Predict for the ith sample in this corpus."""
        return self.predict_all(classifier, self.dense[i:i+1])[0]

    def predict_all(self, classifier, X=None):
        """Predict based on all inputs, which default to this corpus."""
        X = X if X is not None else self.dense
        return classifier.predict(X)


def tokenizer(tagger, text, stopset):
    corpus = Corpus([], tagger, stopset)
    tokens = corpus.tokenize(text)
    if tagger is not None:
        tokens = ['%s/%s' % tag for tag in tokens]
    return tokens


def parse_args(argv=None):
    """This parses the command line."""
    argv = sys.argv[1:] if argv is None else argv
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-c', '--corpus', dest='corpus', action='append',
                        default=CORPUS,
                        help='The input directory containing the training '
                             'corpus.')
    parser.add_argument('-r', '--ratio', dest='ratio', type=float,
                        default=TEST_SET_RATIO,
                        help='The ratio of documents to use as a test set. '
                        'Default = {}'.format(TEST_SET_RATIO))
    parser.add_argument('-o', '--output-dir', dest='output_dir',
                        action='store', default='classifiers',
                        help='The directory to write the pickled classifiers '
                             'to. Default = ./classifiers/.')

    return parser.parse_args(argv)


def main():
    """The main function."""
    args = parse_args()

    stopset = get_english_stopset()
    corpus = read_corpus_features(args.corpus, stopset)

    gaussian = nb.GaussianNB()
    scores = corpus.cross_validate(gaussian, verbose=10)
    print(scores)
    print(scores.mean())
    for c_data in corpus.confused_x_validate(gaussian):
        c_matrix = c_data['confusion_matrix']
        print(c_matrix)

    target_index = dict(
        (t_key, t) for (t, t_key) in corpus.target_key.items()
    )
    target_counts = Counter(target_index[t_key] for t_key in corpus.targets)
    total_targets = len(corpus.targets)
    for (target, count) in target_counts.most_common():
        print('{:12}\t{}\t{}'.format(target, count, count / total_targets))

    # TODO: clean up functions (and the rest of this function) that we're not
    # using.
    # TODO: try different classifiers (different bayes, SVM, max ent)
    # TODO: score the election section itself
    ## TODO: look at vocabulary and limit the features used
    return
    random.shuffle(featuresets)
    test_set, training_set = get_sets(featuresets, args.ratio)

    classifiers = [
        nltk.ConditionalExponentialClassifier,
        nltk.DecisionTreeClassifier,
        nltk.MaxentClassifier,
        nltk.NaiveBayesClassifier,
        nltk.PositiveNaiveBayesClassifier,
    ]
    folds = itertools.chain.from_iterable(
        cross_validate_sets(cls, featuresets)
        for cls in classifiers
    )
    with Pool() as pool:
        means = list(cross_validate_means(
            pool.starmap(cross_validate_p, folds, 3),
        ))

    means.sort(key=second)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    with open(os.path.join(args.output_dir, 'results.csv'), 'w') as fout:
        writer = csv.writer(fout)
        writer.writerow(('Output', 'Accuracy', 'Baseline'))
        writer.writerows(
            report_classifier(cls, a, training_set, test_set, featuresets,
                              args.output_dir)
            for (cls, a) in means
        )

    # TODO: MOAR TRAINING!

if __name__ == '__main__':
    main()
