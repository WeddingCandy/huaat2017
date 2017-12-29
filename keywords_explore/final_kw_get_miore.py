from gensim.models import word2vec
import pandas as pd
import jieba
import re
import numpy as np
def deal_special(s):
    pattern = re.compile(r"[^\u4e00-\u9f5aa-zA-Z0-9]")
    return pattern.sub('',s)
def len_big_zero(item):
    if len(item)>0:
       return 1
    return 0
def cut_str(s):
    line = str(s).upper().strip()
    # 切词，去除特殊符号，去除0串========================
    filted_data = filter(len_big_zero, map(deal_special, jieba.cut_for_search(line)))
    data = list(filted_data)
    if len(data) > 0:
        return ' '.join(data)
    return np.nan
#获取某个类别下的关键词对应的相似关键词
def get_more_kw(model,topic,give_kw,topn=50,min_simi=0.7,min_cate_simi=0.4):
    kw_lst=[]
    for kw in give_kw:
        tmp=cut_str(kw)
        kw_lst+=tmp.split(' ')
    kw_lst=list(set(kw_lst))
    kw_lst=[item for item in kw_lst if len(str(item).strip()) > 1]
    kw_lst = [item for item in kw_lst if item in model.wv]
    result=[]
    print('&',len(kw_lst),kw_lst)
    kw_lst=list(set(kw_lst))
    parent_dict={} #父字典表
    for kw in kw_lst:
        m_s=model.wv.most_similar(kw, topn=topn)
        result.append([kw, kw, 1]) #将自身放入
        parent_dict[kw] = kw
        for k in m_s:
            if k[1]>=min_simi: #相似度要求要高一点
                result.append([kw,k[0],k[1]])
                parent_dict[k[0]]=kw  #关键词父字典
    df_3=pd.DataFrame(result)
    df_3.columns=['2_parent','3_keyword','4_similarity']
    #计算各个词群之间的相似度=========================='
    v_lst=df_3['3_keyword']
    data=[]
    for i in v_lst:
        for j in v_lst:
            if str(i)==str(j):
                continue
            p_i=parent_dict[i]
            p_j=parent_dict[j]
            if p_i==p_j:
                continue
            data.append([str(i), str(j), model.wv.similarity(str(i), str(j))])
    if len(data)==0:
        df_3['1_category']=topic
        return df_3
    df_4=pd.DataFrame(data)
    df_4.columns=['3_keyword','kw3','4_similarity']
    r_4=df_4.groupby('3_keyword').mean().reset_index().sort_values('4_similarity')
    tmp_r=r_4.loc[r_4.index[r_4['4_similarity']>=min_cate_simi],:] #至少0.4以上
    def get_parent(v):
        return parent_dict[v]
    tmp_r['1_category']=topic
    tmp_r['2_parent']=tmp_r['3_keyword'].map(get_parent)
    print('结果',tmp_r.shape)
    return tmp_r
#得到更多关键词主调函数
def get_more(in_path,df_data,model,max_i):
    cate_lst=df_data['1_category'].unique()

    dir_name = os.path.dirname(in_path)
    file_name = in_path[len(dir_name) + 1:]
    tiem_str = time.strftime('%Y%m%d%H%M%S', time.localtime())
    out_path = dir_name + '/' + file_name + tiem_str + '.txt'
    for i,item in enumerate(cate_lst):
        df_result = pd.DataFrame()
        if i < max_i:
            continue
        print('类别：',i,item,'==============================================================')
        df_tmp=df_data.loc[df_data.index[df_data['1_category']==item],:]
        df_tmp['4_similarity']=1
        df_tmp['2_parent'] = 'None'
        item_kw_lst=df_tmp['3_keyword'].tolist()
        print('关键词为：',item_kw_lst)
        df_result = df_result.append(df_tmp, ignore_index=True)
        df_item_kw=get_more_kw(model,item,item_kw_lst,topn=50,min_simi=0.7,min_cate_simi=0.4)
        df_result=df_result.append(df_item_kw,ignore_index=True)

        df_result['len']=df_result['3_keyword'].map(len)
        df_result=df_result.loc[df_result.index[(df_result['len']>1)&(df_result['len']<=25)],:]
        del df_result['len']
        with open(out_path, 'a') as f:
            df_result.to_csv(f,sep='\t',header=None)
'==============================调用方法================================================'
import os
import time
#导入模型
model_path = r'/Volumes/d/huaat/关键词放大方法/pycode/ke_w2v_search.model'
model = word2vec.Word2Vec.load(model_path)
#导入数据
in_path='/Volumes/d/group.csv' #输出路径与输入路径相同
df_data=pd.read_csv(in_path,header=None,encoding='gbk')
df_data.columns=['1_category','3_keyword']#列名不要更改

#调用函数，生成文件为输入文件所在位置
get_more(in_path,df_data,model,max_i=0)
#输出结果有个相似性的值，越大表示越与全局的类别相似，越小表示越有可能不是该群的关键词



