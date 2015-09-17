""" usage: kmeans.py N INPUT_FILE """

import csv
import sys
import os
import json
from numpy import array
from scipy.cluster.vq import kmeans2
from sklearn.decomposition import PCA


def main():
    k, input_file = sys.argv[1:]
    k = int(k)
    with open(input_file) as f:
        reader = csv.DictReader(f)
        file_names = []
        keys = None
        data_rows = list(reader)
        data_vectors = []
        for row in data_rows:
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
            data_vectors.append(topic_probs)

    topic_vector = array(data_vectors, float)
    codebook, label = kmeans2(topic_vector, k)

    pca = PCA(n_components=2)
    positions = pca.fit_transform(topic_vector)

    for data, filename, cluster, xy in zip(data_rows, file_names,
                                           label, positions):
        data['filename'] = filename
        data['cluster'] = int(cluster)
        data['xy'] = xy.tolist()

    with open('clusters.json', 'w') as f:
        json.dump(data_rows, f)

if __name__ == "__main__":
    main()
