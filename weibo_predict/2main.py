#coding=utf-8
import sys
import os
sys.path.append(r'D:\data\weibo_atr\testoutput\weibo_txt')
sys.path.append(r'C:\Users\Chans\PycharmProjects\SpiderTest\weibo_txt')
import class_w2v
import preprocess
import numpy as np
import csv


def input(trainname):  #导入训练集
    traindata = []
    with open(trainname, 'r',encoding="utf-8") as f:
        reader = csv.reader(f)
        count = 0
        for line in reader:      #导入到traindata里
            try:
                traindata.append(line[0]) #第一列
                count += 1
            except:#存在问题就直接连空
                print ("error:", line, count)
                traindata.append(" ")
    return traindata
if __name__ == '__main__':
    """
    使用方法：先训练wv的model，然后再生成wv的向量，最后可以使用2-fold验证效果
    主要目的：生成WV向量，提供给下一个步骤：特征融合。
    注意路径
    """
    print ("---------w2v----------")
    order = 'train w2v model'#标注当前的任务
    # order='getvec'
    # order = 'test'

    print('order is', order)
    classob = class_w2v.w2v(300) #这里在class中的参数就是self

    if order == 'train w2v model': #训练WV的model
        totalname = r'D:\data\weibo_atr\testoutput\jieba_total_cut.csv' #纯文本文件路径
        classob.train_w2v(totalname)
        exit()
    elif order == 'getvec': #利用生成的model得到文档的WV的向量，使用求和平均法
        trainname = r'D:\data\weibo_atr\testoutput\jieba_train_cut.csv'
        testname = r'D:\data\weibo_atr\testoutput\jieba_test_cut.csv'
        traindata = input(trainname)
        testdata = input(testname)

        res1 = classob.load_trainsform(traindata) #将训练集变成向量
        res2 = classob.load_trainsform(testdata)  #将测试集变成向量
        print(res1.shape,res2.shape)
        np.save('D:\data\weibo_atr\testoutput\wv300_win100_train.npy', res1) #np下存储
        np.save('D:\data\weibo_atr\testoutput\wv300_win100_test.npy', res2) #np下存储
        exit()

    #以下为测试wv向量，目的在于寻找最好参数的WV向量
    print('载入所有的w2v向量中..')
    w2vtrain = np.load(r'D:\data\weibo_atr\testoutput\wv300_win100_train.npy')
    w2vtest = np.load(r'D:\data\weibo_atr\testoutput\wv300_win100_test.npy')

    #防止出现非法值
    if np.any((np.isnan(w2vtrain))): #NAN not a number
        print ('nan to num!')
        w2vtrain = np.nan_to_num(w2vtrain)

    if np.any((np.isnan(w2vtest))):
        print('nan to num!')
        w2vtest = np.nan_to_num(w2vtest)

    #载入label文件
    label_genderfile_path = r'D:\data\weibo_atr\testoutput\train_gender.csv'
    label_agefile_path = r'D:\data\weibo_atr\testoutput\train_age.csv'
    label_edufile_path = r'D:\data\weibo_atr\testoutput\train_education.csv'
    genderdata = np.loadtxt(open(label_genderfile_path, 'r')).astype(int)
    agedata = np.loadtxt(open(label_agefile_path, 'r')).astype(int)
    educationdata = np.loadtxt(open(label_edufile_path, 'r')).astype(int)

    print('预处理中..')
    preprocessob = preprocess.preprocess() #调用预处理
    gender_traindatas, genderlabel = preprocessob.removezero(w2vtrain, genderdata) #去0
    age_traindatas, agelabel = preprocessob.removezero(w2vtrain, agedata)#去0
    edu_traindatas, edulabel = preprocessob.removezero(w2vtrain, educationdata)#去0
    # ------------------------------------------------------
    if order == 'test': #使用2-fold进行验证
        res1 = classob.validation(gender_traindatas, genderlabel, kind='gender')
        res2 = classob.validation(age_traindatas, agelabel, kind='age')
        res3 = classob.validation(edu_traindatas, edulabel, kind='edu')
        print('avg is:', (res1+res2+res3)/3.0)
    else:
        print('error!')
        exit()