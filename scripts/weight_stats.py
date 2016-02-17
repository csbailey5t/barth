#!/bin/env python3


"""\
usage: weight_stats.py BINS INPUT_FILE
"""


import math
import pprint
import sys

import tojson


def strip_words(word_weights):
    for (_, weights) in word_weights:
        yield from weights


def do_stats(weights, bins=10):
    mn = sys.maxsize
    mx = 0
    for w in weights:
        mx = max(w, mx)
        mn = min(w, mn)

    width = (mx - mn) / float(bins)
    values = [0] * (bins + 1)
    for w in weights:
        b = math.floor((w - mn) / width)
        values[b] += 1

    hist = []
    start = mn + width / 2.0
    for (i, v) in enumerate(values):
        hist.append((start + i * width, v))

    return (mn, mx, hist)


def report(mn, mx, hist):
    print('Minimum: {:>f}'.format(mn))
    print('Maximum: {:>f}'.format(mx))
    print('\nHistograph:')
    for (bin, (center, value)) in enumerate(hist):
        print('{}\t{}\t{}'.format(bin, center, value))
    print('\n')


def main():
    bins, input_file = sys.argv[1:]
    bins = int(bins)

    print('Reading weights')
    weights = list(
        tojson.substitute_weight_vectors(
            tojson.group_by_words(
                tojson.read_weight_file(input_file))))

    dists = []
    for links in tojson.get_links(weights):
        dists += [link['weight'] for link in links if link['weight'] > 0.0]
    report(*do_stats(dists, bins))


if __name__ == '__main__':
    main()
