# -*- coding: UTF-8 -*- 
from sklearn.ensemble import GradientBoostingRegressor
import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.externals import joblib

#导入数据
def load_data(path):
    df = pd.read_csv(path)
    date = df['data']
    x_train = df.drop(['data','yl','max','min'],1)
    y_train = df['yl']
    return x_train, y_train, date

#特征工程
def pre_data(data, num=1, interate=False):
    data.iloc[0:30,0] = 0.6*data.iloc[0:30,0].mean() + 0.4*data.iloc[0:30,0]
    data.iloc[30:60,0] = 0.6*data.iloc[30:60,0].mean() + 0.4*data.iloc[30:60,0]
    data.iloc[60:,0] = 0.6*data.iloc[60:,0].mean() + 0.4*data.iloc[60:,0]
    #poly = PolynomialFeatures(degree=num, interaction_only=interate)
    #poly.fit(data)
    #return poly.transform(data)
    return data
#验证函数



def train(input_path,model_path):
    #进行数据的读取与预处理
    X_train, y_train, _ = load_data(input_path)
    #GBDT模型的参数进行定义
    clf=GradientBoostingRegressor(n_estimators=100,learning_rate=0.085,max_depth=20,min_samples_split=6,
                           min_weight_fraction_leaf=0.1,random_state=0,alpha=0.95,subsample=1,loss='huber')
    #模型训练
    rf=clf.fit(X_train,y_train)
    #模型保存
    joblib.dump(rf,model_path)
    #模型拟合度输出
    y_train_pre = clf.predict(X_train)
    

def pre(input_path,model_path,output_path):
    #进行数据的读取与预处理
    X_pre, _,  date = load_data(input_path)
    X_pre = pre_data(X_pre)
    #print(X_pre)
    #加载训练好的模型
    clf=joblib.load(model_path)
    #进行预测
    y_test_pre = clf.predict(X_pre)
    #输出预测三个月用电量的总和
    print(np.sum(y_test_pre))
    #将预测量以csv格式的文件保存至指定的位置
    df=pd.DataFrame(date, columns=['data'])
    df['yl'] = y_test_pre
    df.to_csv(output_path,index=False)
    
# if __name__=='__main__':
#     train(input_path = "./input_data.csv",model_path = "./rf.model")
#     pre(input_path = "./pre_data.csv",model_path = "./rf.model",output_path = "./1.csv")
