# coding=utf-8
from sklearn.model_selection import KFold, StratifiedKFold
from gensim.models import word2vec
import numpy as np
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.svm import LinearSVC,SVC

size =300
random_rate = 8240
svc = SVC(C=1, random_state=random_rate)#支持向量机
LR = LogisticRegression(C=1.0, max_iter=100, class_weight='balanced', random_state=random_rate, n_jobs=-1)#对数机率回归
clf = LinearSVC(random_state=random_rate)#支持向量机

def fit( X, Y, T):  #  用线性回归进行分类，输入x和y
        print ('fitting..')
        LR.fit(X, Y)  #逻辑回归放训练数据样本
        res = LR.predict(T) #训练完后放入测试样本
        return res

def validation(X,Y,kind):  #分类检验
        print('validating...')
        fold_n=2    #2次的k交叉验证
        folds = list(StratifiedKFold(Y, n_folds=fold_n, random_state=0))#交叉验证
        score=np.zeros(fold_n)  #评分矩阵，
        for j, (train_idx, test_idx) in enumerate(folds): #enumerate
            print(j + 1, '-fold')
            X_train = X[train_idx]
            y_train = Y[train_idx]
            X_test = X[test_idx]
            y_test = Y[test_idx]

            res = fit(X_train, y_train, X_test)#测试出的训练集的结果
            cur = sum(y_test == res) * 1.0 / len(res)#与原始分类做对比，即判断正确率
            score[j] = cur
        print(score, score.mean())#均值矩阵
        return score.mean()

def train_w2v(filename): #训练语料库
        sentences = word2vec.LineSentence(filename)
        print('正在训练w2v 针对语料：',str(filename))
        print ('size is: ',size)
        model = word2vec.Word2Vec(sentences, size=size, window=100,workers=48)  #size 为维度数量
        savepath = 'D:\data\weibo_atr\testoutput\20w_size_win100_' + str(size)+'.model'
        print('训练完毕，已保存: ', savepath,)
        model.save(savepath)

totalname = r'D:\data\weibo_atr\output\jieba_total_cut.csv'
x=train_w2v(totalname)



def load_trainsform(X): #变成向量
        print('载入模型中')
        model = word2vec.Word2Vec.load(r'D:\data\weibo_atr\testoutput\20w_size_win100_300.model')  #载入训练完后的模型
        print('加载成功')
        res = np.zeros((len(X),size)) #结果向量
        print('生成w2v向量中..')
        for i,line in enumerate(X):
            line = line.decode('utf-8')
            terms = line.split() #生成的词用空格分开进list里
            count = 0
            for j,term in enumerate(terms):
                try:
                    count += 1
                    res[i]+= np.array(model[term])#把载入的X中的词放到model中进行训练
                except:
                    1 == 1
            if count!=0:
                res[i]=res[i]/float(count)
        return res