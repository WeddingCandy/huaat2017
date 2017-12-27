#! usr/bin/python
#coding=utf-8

import xlrd
import pandas as pd
import numpy as np
import random
#数据读取
# totol_people_num = 3001557
# sheet = pd.read_excel(u'/Users/Apple/Desktop/working/1 isobar/lifestyle/安索帕美妆lifestyle关联分析-V1.xlsx',sheetname=u'Sheet1',encoding='utf-8')
#
# sheet[u'交叉量']/totol_people_num * 100
#
#
# sheet['dim'] = sheet[u'交叉量']/totol_people_num * 100
#
# # check1 = sheet.loc[:,[u'维度1',u'dim']]
#
# check1 = dict(list(zip(sheet[u'维度1'] , sheet[u'dim'])))
# sheet['dim2'] = sheet[u'维度2'].apply(lambda x: check1[x])

#0.-----------------------------------表格读取------------------------------------------
sheet = pd.read_excel(u'/Users/Apple/Desktop/working/1 isobar/lifestyle/安索帕美妆lifestyle关联分析-V1.xlsx',sheetname=u'Sheet4',encoding='utf-8')
sheet1 = sheet
print(sheet1.keys())
sheet1['交叉维度'] = sheet[u'维度1']+sheet[u'维度2']
#修改列顺序
cols = sheet1.columns.tolist()
cols = cols[0:2]+cols[-1:]+cols[2:]
del cols[-1:]
sheet1 = sheet1[cols]

#--------------------------放大---------------------------------
num1 = 12.8043725306566

sheet1[u'放大总量'] = sheet1['总量'] * num1
cols = sheet1.columns.tolist()
cols = cols[0:4]+cols[-1:]+cols[4:]
del cols[-1:]
sheet1 = sheet1[cols]

sheet1[u'放大交叉量'] = sheet1['交叉量'] * num1
cols = sheet1.columns.tolist()
cols = cols[0:6]+cols[-1:]+cols[6:]
del cols[-1:]
sheet1 = sheet1[cols]
print(sheet1.keys)




#1.-----------------------------------------------------按照分段比咧进行分段----------------------------------------------

#生成一列用来添加‘修改交叉量’
cols = sheet1.columns.tolist()
sheet1[u'修改交叉量'] = ' '
# cols = sheet1.columns.tolist()

#分段调整
row_total = len(sheet1)
propotion = 20   #设置划分的比例
fenduan = np.round(row_total/propotion, 0)

#设定随机数范围和随机变化
list_para = np.linspace(1.0,0.3,propotion) * 100000
list_para_rest = 1 *100000-list_para

print(list_para, end='\t')
print(list_para_rest, end='\t')
for k in range(propotion):#propotion
    if fenduan * (k+1) < row_total :
        last_num = int(fenduan * (k+1))
    else:
        last_num = int(row_total)
    for l in range(int(fenduan * k), last_num):
        para = (list_para[k] + random.randint(0, int(list_para_rest[k]))) / 100000
        # sheet1[u'放大交叉量'][0 * (k+1):fenduan * (k+1)]
        after = int(np.round(sheet1[u'放大交叉量'][l] * para,0))
        sheet1[u'修改交叉量'][l] = int(np.round(sheet1[u'放大交叉量'][l] * para,0))
        print(l, after)
        # print(l)

cols = sheet1.columns.tolist()
cols = cols[0:7]+cols[-1:]+cols[7:]
del cols[-1:]
sheet1 = sheet1[cols]


####2.自定义比例进行分段
#设定放大分段
row_total = len(sheet1)
print('当前数据行数',row_total)
list_input = input("用半角逗号隔开输入...")
list_propotion_str = list_input.split(',')
list_propotion = [int(list_propotion_str[m]) for m in range(len(list_propotion_str))]
existç_num = sum(list_propotion)

while keyword is not 'pass':
    if existç_num <= row_total:
        keyword = 'pass'
    else:
        keyword = 'reinput'

    list_input = input("数超了，重输（用半角逗号隔开输入...）")
    list_propotion_str = list_input.split(',')
    list_propotion = [int(list_propotion_str[m]) for m in range(len(list_propotion_str))]
    exist_num = sum(list_propotion)

list_rest = row_total - exist_num
print(list_propotion)
list_propotion.append(list_rest)
print(list_propotion)

# proportion_num =








#输出Excel
pd.DataFrame(sheet1).to_excel(u"./安索帕美妆lifestyle关联分析test.xlsx",sheet_name="123",index=False,header=True)



















