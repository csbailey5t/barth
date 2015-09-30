#!/usr/bin/env python3

import nltk
import logl
import os
import csv

tokenized_corpus = logl.tokenize_corpus('paragraphs')
stemmer = nltk.stem.snowball.SnowballStemmer('english')
stopwords = set(nltk.corpus.stopwords.words('english'))

cfdist = nltk.probability.ConditionalFreqDist()
columns = []

for (filename, words) in tokenized_corpus:
    filename = os.path.basename(filename)
    columns.append(filename)
    for word in words:
        if word in stopwords:
            continue
        cfdist[stemmer.stem(word)][filename] += 1

with open('freqencies.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow([None] + columns)
    for word in cfdist:
        row = [word]
        for column in columns:
            row.append(cfdist[word][column])
        writer.writerow(row)
