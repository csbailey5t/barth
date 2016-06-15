#!/bin/env python3


import csv
import sys

import gensim
import pyLDAvis
import numpy


CORPUS = 'paragraphs/'
MODEL_KEYWORD = 'barth'


def load_doc_topics(filename):
    with open(filename) as f:
        lines = list(f)

    if lines[0].startswith('index'):
        # sane
        with open(filename) as f:
            rows = list(csv.DictReader(f, dialect='excel_tab'))

    else:
        # insane
        rows = []
        for line in lines[1:]:
            fields = line.split('\t')
            if len(fields) < 3:
                print('OOPS')
                print(fields)
                sys.exit(1)
            doc_no, name, *topics = fields
            row = {
                'index': doc_no,
                'file': name,
            }
            topics.pop()
            for topic, prob in zip(topics[::2], topics[1::2]):
                row['topic-{}'.format(topic)] = prob
            rows.append(row)

    topic_count = len(rows[0]) - 2
    data = []
    for row in rows:
        output_row = []
        for i in range(topic_count):
            key = 'topic-{}'.format(i)
            output_row.append(float(row[key]))
        data.append(output_row)

    return numpy.array(data)


def load_model(keyword):
    doc_topic_dists = load_doc_topics(keyword + '.doc.topics')
    print(doc_topic_dists)
    return {
        'doc_topic_dists': doc_topic_dists,
        'doc_lengths': None,
        'vocab': None,
        'term_frequency': None,
        'R': None,
        'lambda_step': None,
        'mds': None,
        'n_jobs': None,
        'plot_opts': None,
    }


def load_from_mallet():
    model = load_model(MODEL_KEYWORD)
    viz = pyLDAvis.prepare(model)
    with open(MODEL_KEYWORD + '.html', 'w') as f:
        pyLDAvis.save_html(viz, f)


def main():
    corpus = gensim.corpora.textcorpus.TextCorpus()


if __name__ == '__main__':
    main()
