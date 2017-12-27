# -*- coding:utf-8 -*-
import pandas as pd
import jieba.analyse
import time
import csv
import jieba
import jieba.posseg
import os, sys
#sys.setdefaultencoding('utf8')
jieba.load_userdict(r'/data/hive_home/weibo_cluster_concerned/dict/tag_brand_dict.txt')
import csv
def input(trainname):     #输入获取的数据集
    traindata = []
    with open(trainname, 'rb') as f:
        line = f.readline()
        count = 0
        while line:
            try:
                traindata.append(line)
                count += 1
            except:
                print ("error:", line, count)
            line=f.readline()
    return traindata
start = time.clock()

filepath = r'/data/hive_home/weibo_cluster_concerned/data_for_test/test2.csv'
QueryList = input(filepath)
csvreader = csv.reader(open(filepath,'r',encoding='gbk'))
"""QueryList2 =[]
for line in csvreader:
    QueryList2.append(line)""" #存在list对象

writepath = r'/data/hive_home/weibo_cluster_concerned/data_for_test/writefile.csv'
csvfile = open(writepath, 'w',encoding='gbk')
jieba.enable_parallel()
POS = {}
for i in range(len(QueryList)):
    s = []
    strx = ""
    words = jieba.posseg.cut(QueryList[i].lower())
    allowPOS = ['n','v','j']
    for w in words:
        POS[w.flag]=POS.get(w.flag,0)+1
        if (w.flag[0] in allowPOS) and len(w.word)>=2:

            strx += w.word + " "

    s.append(strx)
    #print(s)
    csvfile.write(" ".join(s)+'\n')
csvfile.close()
print(POS)

end = time.clock()
print("total time: %f s" % (end - start))