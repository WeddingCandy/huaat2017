# coding=utf-8
"""
根据上一步骤得到的CSV文件，将搜索文本以及三个属性剥离，保存为相应的文件
注意路径
"""
import pandas as pd
#path of the train and test files
trainname = r'/data/hive_home/weibo_cluster_concerned/data/train.csv'
testname = r'/data/hive_home/weibo_cluster_concerned/data/test.csv'

data = pd.read_csv(trainname)  #read the data from csv
print(data.info()) #get information of dataset
#generate three labels for age/gender/education
data.age.to_csv(r'/data/hive_home/weibo_cluster_concerned/data/train_age.csv', index=False)
data.gender.to_csv(r'/data/hive_home/weibo_cluster_concerned/data/train_gender.csv', index=False)
data.edu.to_csv(r'/data/hive_home/weibo_cluster_concerned/data/train_education.csv', index=False)
#generate trainfile's text file
data.QueryList.to_csv(r'/data/hive_home/weibo_cluster_concerned/data/train_querylist.csv', index=False)

data2 = pd.read_csv(testname)
print(data2.info())
#generate testfile's text file
data2.QueryList.to_csv(r'/data/hive_home/weibo_cluster_concerned/data/test_querylist.csv', index=False)