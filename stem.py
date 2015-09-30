#!/usr/bin/env python3

import nltk
import logl
import os
import csv

tokenized_corpus = logl.tokenize_corpus('paragraphs')
stemmer = nltk.stem.snowball.SnowballStemmer('english')
stopwords = set(nltk.corpus.stopwords.words('english'))

texts = []
columns = []

for (filename, words) in tokenized_corpus:
    filename = os.path.basename(filename)
    columns.append(filename)
    words = [
        stemmer.stem(word)
        for word in words
        if word not in stopwords
        ]
    text = nltk.text.Text(words, filename)
    texts.append(text)

collection = nltk.text.TextCollection(texts)

with open('freqencies.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow([None] + columns)
    for word in collection.vocab():
        row = [word]
        for column in columns:
            row.append(collection.tf_idf(word, column))
        writer.writerow(row)
