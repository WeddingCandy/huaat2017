#! usr/bin/python
#coding=utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def loadDataSet(path):
    tmp=[];
    with open(path, encoding='utf-8') as f:
      for line in f.readlines():
          lineArr = line.split()
          tmp.append(lineArr)
    return tmp

path = r'D:\data\assosiation\association.txt'

dataset= []
dataset = loadDataSet(path)

label = dataset[0][1:]
print(label)

s = pd.Series(dataset[1:])

