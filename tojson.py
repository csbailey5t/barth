import csv
import json
import itertools
import operator
import math


def dist(xs, ys):
    return math.sqrt(sum((x-y)**2 for (x, y) in zip(xs, ys)))


get_weight = operator.itemgetter(2)


def task(by_word, i, job_data):
    (w0, rows0) = job_data
    links = []
    for (j, (w1, rows1)) in enumerate(by_word):
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


def main():
    with open('barth.weights') as f:
        rows = [
            (int(t), w, float(n)) for (t, w, n) in csv.reader(f, 'excel-tab')
            ]

    # sort rows by word
    rows.sort(key=operator.itemgetter(1))
    by_word = [
        (w, list(rws))
        for (w, rws) in itertools.groupby(rows, operator.itemgetter(1))
        ]
    nodes = [
        {'name': w, 'topic': max(rws, key=operator.itemgetter(2))[0]}
        for (w, rws) in by_word
        ]

    links = []
    for (i, job) in enumerate(by_word):
        links += task(by_word, i, job)

    with open('weights.json', 'w') as f:
        json.dump({'nodes': nodes, 'links': links}, f)


if __name__ == '__main__':
    main()
