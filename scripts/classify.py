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
from nltk.corpus import brown, names, stopwords
# from nltk.probability import ConditionalFreqDist
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import cross_validation as xv
from sklearn import naive_bayes as nb
import numpy as np


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
    for (root, dirs, files) in os.walk(corpus_dir):
        for fn in files:
            full_fn = os.path.join(root, fn)
            with open(full_fn) as fin:
                yield (full_fn, tokenize(fin.read()))


def build_tagger(tagged_sents=None, default_tag='DEFAULT'):
    """This builds a tagger from a corpus."""
    if os.path.exists(TAGGER_CACHE):
        with open(TAGGER_CACHE, 'rb') as f:
            tagger = pickle.load(f)
    else:
        if tagged_sents is None:
            tagged_sents = brown.tagged_sents()

        name_tagger = [
            nltk.DefaultTagger('PN').tag([
                name.lower() for name in names.words()
            ])
        ]
        patterns = [
            (r'.*ing$', 'VBG'),               # gerunds
            (r'.*ed$', 'VBD'),                # simple past
            (r'.*es$', 'VBZ'),                # 3rd singular present
            (r'.*ould$', 'MD'),               # modals
            (r'.*\'s$', 'NN$'),               # possessive nouns
            (r'.*s$', 'NNS'),                 # plural nouns
            (r'^-?[0-9]+(.[0-9]+)?$', 'CD'),  # cardinal numbers
            (r'.*ly$', 'RB'),                       # adverbs
            # comment out the following line to raise to the surface all
            # the words being tagged by this last, default tag when you
            # run debug.py.
            (r'.*', 'NN')                     # nouns (default)
        ]

        # Right now, nothing will get to the default tagger, because the
        # regex taggers last pattern essentially acts as a default tagger,
        # tagging everything as NN.
        tagger0 = nltk.DefaultTagger(default_tag)
        regexp_tagger = nltk.RegexpTagger(patterns, backoff=tagger0)
        tagger1 = nltk.UnigramTagger(tagged_sents, backoff=regexp_tagger)
        tagger2 = nltk.BigramTagger(tagged_sents, backoff=tagger1)
        tagger3 = nltk.UnigramTagger(name_tagger, backoff=tagger2)

        tagger = tagger3
        with open(TAGGER_CACHE, 'wb') as f:
            pickle.dump(tagger, f, pickle.HIGHEST_PROTOCOL)

    return tagger


def read_corpus_features(directories, stopset=None):
    """This reads a list of directories and pulls the features from its
    documents. The tag for each document is its immediate directory's
    name."""
    tagger = build_tagger()
    files = []

    for dirname in directories:
        for (root, _, file_list) in os.walk(dirname):
            files += [os.path.join(root, fn) for fn in file_list]

    corpus = TfidfCorpus(files, lambda text: tokenizer(tagger, text, stopset))
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

    def fit(self, classifier, X=None, y=None):
        """Train a classifier on this corpus or other data."""
        X = X or self.dense
        y = y or self.targets
        classifier.fit(X, y)

    def predict(self, classifier, i):
        """Predict for the ith sample in this corpus."""
        return self.predict_all(classifier, self.dense[i:i+1])[0]

    def predict_all(self, classifier, X=None):
        """Predict based on all inputs, which default to this corpus."""
        X = X or self.dense
        return classifier.predict(X)


def tokenizer(tagger, text, stopset):
    tokens = tokenize(text)
    tags = tagger.tag(tokens)
    tags = [tag for tag in tags if tag[0].isalnum()]
    if stopset is not None:
        tags = [tag for tag in tags if tag[0].lower() not in stopset]
    tags = ['%s/%s' % tag for tag in tags]
    return tags


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

    stopset = set(stopwords.words('english'))
    corpus = read_corpus_features(args.corpus, stopset)
    gaussian = nb.GaussianNB()
    scores = corpus.cross_validate(gaussian, verbose=10)
    print(scores)
    print(scores.mean())

    # TODO: clean up functions (and the rest of this function) that we're not
    # using.
    # TODO: try different classifiers (different bayes, SVM, max ent)
    # TODO: figure out the baseline
    # TODO: score the election section itself
    # TODO: look at vocabulary and limit the features used
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
