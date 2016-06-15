#!/usr/bin/env python3

import nltk
import os
import csv
from sklearn.feature_extraction.text import TfidfVectorizer

stemmer = nltk.stem.snowball.SnowballStemmer('english')

path = 'texts/paragraphs'


def tokenizer(text):
    tokens = nltk.word_tokenize(text)
    words = [
        stemmer.stem(word)
        for word in tokens
        if word.isalpha()
        ]
    return words

all_files = []

for dirpath, dirs, files in os.walk(path):
    for f in files:
        full_fn = os.path.join(dirpath, f)
        all_files.append(full_fn)
# all_files = all_files[:2]

tfidf = TfidfVectorizer(
    tokenizer=tokenizer, stop_words='english', input='filename'
    )
tfs = tfidf.fit_transform(all_files)
print('minimum={}'.format(tfs.min()))
print('maximum={}'.format(tfs.max()))

with open('frequencies.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow([None] + tfidf.get_feature_names())
    for i, file in enumerate(all_files):
        writer.writerow([os.path.basename(file)] + tfs.getrow(i).toarray().flatten().tolist())
