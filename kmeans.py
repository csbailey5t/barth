""" usage: kmeans.py N INPUT_FILE """

import csv
import sys
from numpy import array
from scipy.cluster.vq import kmeans, whiten

def main():
    k, input_file = sys.argv[1:]
    k = int(k)
    with open(input_file) as f:
        reader = csv.DictReader(f)
        file_names = []
        data_rows = []
        keys = None
        for row in reader:
            file_names.append(row['file'])
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

    topic_vector = array(data_rows)
    normalized = whiten(topic_vector)


if __name__ == "__main__":
    main()
