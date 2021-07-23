#!/usr/bin/env python
# coding: utf-8

import sqlite3
import numpy as np
import pandas as pd

conn = sqlite3.connect('music.db')

train_labels = pd.read_csv("./data/labels.csv")
train_features = pd.read_csv("./data/features.csv")

train_labels = train_labels.merge(train_features[['trackID','title']], on='trackID', how='left')
train_labels.reset_index(drop=True, inplace=True)

# Write to sqlite database
train_labels.to_sql(name='music', con=conn)



