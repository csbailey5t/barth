#!/usr/bin/env python


import argparse
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


CORPUS = [
    'texts/paragraphs_before_election',
    'texts/paragraphs_after_election',
    ]
TEST_SET_RATIO = 0.2


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


def read_corpus_features(directories):
    """This reads a list of directories and pulls the features from its
    documents. The tag for each document is its immediate directory's
    name."""
    for dirname in directories:
        dirname = os.path.abspath(dirname)
        (_, tag) = os.path.split(dirname)
        for (root, _, files) in os.walk(dirname):
            for fn in files:
                full_fn = os.path.join(root, fn)
                # TODO: tokenize the file
                # TODO: POS tagging?
                # TODO: stopwords
                # TODO: featureset (dict between tokens/tags => existence or frequency)


def parse_args(argv=None):
    """This parses the command line."""
    argv = sys.argv[1:] if argv is None else argv
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-c', '--corpus', dest='corpus', action='append',
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

    featuresets = read_corpus_features(args.corpu)
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
