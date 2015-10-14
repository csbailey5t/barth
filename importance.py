#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

ELECTION = '04-03-33-the_election_of_jesus_christ.txt'
N = 25

df = pd.read_csv('freqencies.csv', index_col=0, encoding='latin-1')
dft = df.transpose()
by_election = dft.sort_values(ELECTION)
most_common = by_election[-N:][[ELECTION]]

god = by_election['god']

graph = god.plot()


print(most_common)
plt.show()
