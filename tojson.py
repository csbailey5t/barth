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


def dist(xs, ys):
    return math.sqrt(sum((x-y)**2 for (x, y) in zip(xs, ys)))


get_weight = operator.itemgetter(2)


def task(by_word, job_data):
    (i, (w0, rows0)) = job_data
    links = []
    for (j, (w1, rows1)) in by_word:
        if w0 == w1:
            continue
        weights0 = (get_weight(w) for w in rows0)
        weights1 = (get_weight(w) for w in rows1)
        links.append({
            'source': i,
            'target': j,
            'weight': dist(weights0, weights1),
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


def main():
    print('Reading weights')
    with open('barth.weights') as f:
        rows = [
            (int(t), w, float(n)) for (t, w, n) in csv.reader(f, 'excel-tab')
            ]

    # sort rows by word
    print('Preparing data')
    rows.sort(key=operator.itemgetter(1))
    by_word = [
        (w, list(rws))
        for (w, rws) in itertools.groupby(rows, operator.itemgetter(1))
        ]
    nodes = [
        {'name': w, 'topic': max(rws, key=operator.itemgetter(2))[0]}
        for (w, rws) in by_word
        ]

    links = get_links(by_word)

    print('Writing output')
    with open('weights.json', 'w') as f:
        json.dump({'nodes': nodes, 'links': links}, f)

    print('done')


if __name__ == '__main__':
    main()
