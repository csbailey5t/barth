#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('freqencies.csv', index_col=0, encoding='latin-1')

elect_words = ['elect', 'electa', 'electi', 'electio',
               'election', 'electionem', 'electioni', 'electo',
               'elector', 'electorum']


def create_plot(word):
    word_frame = df.word
    plt.figure(word)
    word_frame.plot(kind='bar')
    plt.savefig(word)

for word in elect_words:
    create_plot(word)


# plt.show()

# elect = df.elect
# election = df.election
# plt.figure('elect')
# elect.plot(kind='bar')
# plt.figure('election')
# election.plot(kind='bar')
# # plt.savefig('election')
# plt.show()
