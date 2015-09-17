#!/usr/bin/env python3


"""\
usage: doc_topics_csv.py < INPUT > OUTPUT
"""


import csv
import math
import sys


def order_weights(weight_pairs):
    topic_count = math.floor(len(weight_pairs) / 2)
    topics = [None] * topic_count

    while weight_pairs:
        topic, weight = weight_pairs[:2]
        weight_pairs = weight_pairs[2:]
        topics[int(topic)] = float(weight)

    return topics


def line2row(line):
    fields = line.split()

    n = fields[0]
    name = fields[1]
    topics = order_weights(fields[2:])

    row = [n, name] + topics
    return row


def main():
    csv.writer(sys.stdout).writerows(
        line2row(line) for line in sys.stdin
    )


if __name__ == '__main__':
    main()
