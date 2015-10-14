#!/usr/bin/env python3

import pandas as pd

df = pd.read_csv('/Users/csb5t/projects/barth/freqencies.csv', index_col=0, encoding='latin-1')

elect_column = df.elect

print(elect_column)
