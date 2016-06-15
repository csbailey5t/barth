import numpy as np
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

CORPUS = ['texts/paragraphs_before_election', 'texts/paragraphs_after_election']


def read_corpus(corpus_dir):
    files = []
    for dirname in corpus_dir:
        for (root, _, file_list) in os.walk(dirname):
            files += [os.path.join(root, fn) for fn in file_list]


    vectorizer = TfidfVectorizer(input='filename', stop_words='english', ngram_range=(1,3))
    X = vectorizer.fit_transform(files)
    features = vectorizer.get_feature_names()

    return top_mean_feats(X, features)


def top_tfidf_feats(row, features, top_n=50):
    top_ids = np.argsort(row)[::-1][:50]
    top_features = [(features[i], row[i]) for i in top_ids]

    df = pd.DataFrame(top_features)
    df.columns = ['feature', 'tfidf']

    # print(df)
    return df


def top_feats_in_doc(X, features, row_id, top_n=50):

    row = np.squeeze(X[40].toarray())

    return top_tfidf_feats(row, features, top_n)


def top_mean_feats(X, features, grp_ids=None, min_tfidf=0.1, top_n=50):
    ''' Return the top n features that on average are most important amongst documents in rows
        indentified by indices in grp_ids. '''
    if grp_ids:
        D = X[grp_ids].toarray()
    else:
        D = X.toarray()

    D[D < min_tfidf] = 0
    tfidf_means = np.mean(D, axis=0)

    featsDf = top_tfidf_feats(tfidf_means, features, top_n)

    return featsDf

# top_mean_feats(X, features)
print('before')
beforeDf = read_corpus(['texts/paragraphs_before_election'])
print('after')
afterDf = read_corpus(['texts/paragraphs_after_election'])
print('election')
electionDf = read_corpus(['texts/paragraphs_election_only'])

frames = [beforeDf, electionDf, afterDf]

combinedFrames = pd.concat(frames, axis=1)

print(combinedFrames)

combinedFrames.to_csv('tfidf_ngram.csv')
