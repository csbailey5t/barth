""" usage: kmeans.py N INPUT_FILE """

import csv
import sys
import operator
import os
from itertools import groupby
from numpy import array
from scipy.cluster.vq import kmeans2, whiten

def main():
    k, input_file = sys.argv[1:]
    k = int(k)
    with open(input_file) as f:
        reader = csv.DictReader(f)
        file_names = []
        data_rows = []
        keys = None
        for row in reader:
            file_names.append(os.path.basename(row['file']))
            if not keys:
                keys = []
                for key in row.keys():
                    if key.startswith('topic'):
                        keys.append(key)
                keys.sort()
            topic_probs = []
            for topic in keys:
                topic_probs.append(row[topic])
            data_rows.append(topic_probs)

    topic_vector = array(data_rows, float)
    codebook, label = kmeans2(topic_vector, k)
    clusters = list(zip(file_names, list(label)))
    clusters.sort(key=operator.itemgetter(1))
    for n,files in groupby(clusters, operator.itemgetter(1)):
        for file in files:
            print(file)
        print()

if __name__ == "__main__":
    main()
