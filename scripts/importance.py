#!/usr/bin/env python3

import pandas as pd
# import matplotlib.pyplot as plt
import os

ELECTION = '04-03-33-the_election_of_jesus_christ.txt'
N = 25

df = pd.read_csv('freqencies.csv', index_col=0, encoding='latin-1')
# dft = df.transpose()
# by_election = dft.sort_values(ELECTION)
# most_common = by_election[-N:][[ELECTION]]
#
# god = by_election['god']
#
# graph = god.plot()


# print(most_common)
# plt.show()

my_path = os.path.dirname(os.path.abspath(__file__))
full_path = os.path.join(my_path, 'graphs')
print("my path = " + full_path)

# elect = df.elect
# election = df.election
# plt.figure('elect')
# elect.plot(kind='bar')
# plt.figure('election')
# election.plot(kind='bar')
# plt.savefig(os.path.join(my_path, 'election'))
# plt.savefig(os.path.join(my_path, 'elect'))
# plt.show()
