import csv
import json
import itertools
import operator
import math
from multiprocessing import Pool
import functools
import datetime
import os


# Parallelization parameters
CPU_COUNT = os.cpu_count()
CHUNK_SIZE = 32
CUT_OFF = 1.4


def dist(xs, ys):
    return math.sqrt(sum((x-y)**2 for (x, y) in zip(xs, ys)))


get_weight = operator.itemgetter(2)


def task(by_word, job_data):
    (i, (w0, weights0)) = job_data
    links = []
    for (j, (w1, weights1)) in by_word:
        if w0 == w1:
            continue
        d = dist(weights0, weights1)
        if d < CUT_OFF:
            links.append({
                'source': i,
                'target': j,
                'weight': d,
                })
    return links


def get_links(by_word):
    print('Running ({}) parallel tasks (chunk size {})'.format(
        CPU_COUNT, CHUNK_SIZE))
    links = []

    by_word_indexed = list(enumerate(by_word))
    task_by_word = functools.partial(task, by_word_indexed)

    start = datetime.datetime.now()
    with Pool(CPU_COUNT, maxtasksperchild=10) as pool:
        links += pool.imap_unordered(task_by_word, by_word_indexed, CHUNK_SIZE)
    done = datetime.datetime.now()

    print('Elapsed time = {}'.format(done - start))
    return links


def read_weight_file(filename, weight_type=float):
    with open(filename) as f:
        return [
            (int(t), w, weight_type(n))
            for (t, w, n) in csv.reader(f, 'excel-tab')
            ]


def group_by_words(rows):
    rows.sort(key=operator.itemgetter(1))
    return [
        (w, sorted(list(rws), key=operator.itemgetter(0)))
        for (w, rws) in itertools.groupby(rows, operator.itemgetter(1))
        ]


def make_nodes(by_word):
    return [
        {'name': w, 'topic': max(rws, key=operator.itemgetter(2))[0]}
        for (w, rws) in by_word
        ]


def substitute_weight_vectors(by_word):
    return [(w, [get_weight(r) for r in rws]) for (w, rws) in by_word]


def main():
    print('Reading weights')
    rows = read_weight_file('barth.weights')

    # sort rows by word
    print('Preparing data')
    by_word = group_by_words(rows)
    nodes = make_nodes(by_word)
    by_word = substitute_weight_vectors(by_word)

    links = get_links(by_word)

    print('Writing output')
    with open('weights.json', 'w') as f:
        json.dump({'nodes': nodes, 'links': links}, f)

    print('done')


if __name__ == '__main__':
    main()
