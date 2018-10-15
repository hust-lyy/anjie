#!/usr/bin/python
# -*- coding: UTF-8 -*- 
import time
import datetime
import calendar
from sklearn.ensemble import GradientBoostingRegressor
import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.externals import joblib
import cx_Oracle
lasttimestamp = -1
# class Prediction(object):
#导入数据
def load_data(path):
    df = pd.read_csv(path)   
    date = df['日期']
    x_train = df.drop(['日期','用电量'],1)
    y_train = df['用电量']
    return x_train, y_train, date

#特征工程
def pre_data(data, num=1, interate=False):
    #data.iloc[:,1] = 0.6*data.iloc[:,1].mean() + 0.4*data.iloc[:,1] 
    poly = PolynomialFeatures(degree=num, interaction_only=interate)
    poly.fit(data)
    return poly.transform(data)
    
#验证函数
def my_score(y_ture, y_pre):
    score = abs(sum(y_pre - y_ture))/sum(y_ture)
    print(score)
    return score


def train(input_path,model_path):
    #进行数据的读取与预处理
    X_train, y_train, _ = load_data(input_path)
    X_train = pre_data(X_train)
    #GBDT模型的参数进行定义
    clf=GradientBoostingRegressor(n_estimators=100,learning_rate=0.085,max_depth=20,min_samples_split=6,
                        min_weight_fraction_leaf=0.1,random_state=0,alpha=0.95,subsample=1,loss='huber')
    #模型训练
    rf=clf.fit(X_train,y_train)
    #模型保存
    joblib.dump(rf,model_path)
    #模型拟合度输出
    y_train_pre = clf.predict(X_train)
    my_score(y_train_pre, y_train)

def pre(input_path,model_path,output_path):
    #进行数据的读取与预处理
    X_pre, _,  date = load_data(input_path)
    X_pre = pre_data(X_pre)
    #加载训练好的模型
    clf=joblib.load(model_path)
    #进行预测
    y_test_pre = clf.predict(X_pre)
    #输出预测三个月用电量的总和
    print(np.sum(y_test_pre))
    #将预测量以csv格式的文件保存至指定的位置
    df=pd.DataFrame(date, columns=['日期'])
    df['用电量'] = y_test_pre
    df.to_csv(output_path,index=False)
def readcsv(docid=None,date=None):
    if date!=None:
        tempdate=time.strptime(date,'%Y%m')
        firstdayweekday,monthranage=calendar.monthrange(tempdate.tm_year,tempdate.tm_mon)
        firstday=datetime.date(year=tempdate.tm_year,month=tempdate.tm_mon,day=1)
        lastday=datetime.date(year=tempdate.tm_year,month=tempdate.tm_mon,day=monthranage)
    df=pd.read_csv("./uploads/csv/"+str(docid)+"/1.csv")
    # print(df)
    result=[]
    for ddd,elc in df.values:
        
        temptime=datetime.datetime.strptime(str(int(ddd)), '%Y%m%d')
        if date!=None:
            tempdic={}
            if firstday<= temptime.date() and temptime.date()<=lastday:
                tempdic['date']=temptime.strftime('%Y-%m-%d')
                tempdic['ele']=str(int(elc))
                result.append(tempdic)
        else:
            tempdic={}
            tempdic['date']=temptime.strftime('%Y-%m-%d')
            tempdic['ele']=str(int(elc))
            result.append(tempdic)
        
    return result
def getorderid(programIndex=None):
    global lasttimestamp
    base_timestamp = 1287888001020
    timestamp = int(round(time.time() * 1000))  # 当前时间戳 毫秒级
    program_index_bit = 6  # 商户序号所占字符数
    if programIndex==None:
        program_index=1
    else:
        program_index = programIndex  # 商户序号
    if lasttimestamp == timestamp:
        return None
    else:
        temptime = timestamp - base_timestamp
        result = temptime << program_index_bit | program_index
        lasttimestamp = timestamp
        return result


def contentoracle():
    conn = cx_Oracle.connect('NEWBI/newBIdb123@192.168.51.55/orcl')
    cursor = conn.cursor()
    cursor.execute("select substr(DEVICE_CODE,0,6) device_code ,sdate,sum(yl) yl  from FBI_IVPD_DAY where DEVICE_CODE like 'K0bjcxd4%' group by substr(DEVICE_CODE,0,6) ,sdate ORDER BY sdate")
    row = cursor.fetchall()
    print(row)
    dt=pd.DataFrame()
    
    for tempitem in row:
        dt['日期'].append(tempitem[1].strftime('%Y-%m-%d'))
        dt['用电量'].append(tempitem[2])
        
    cursor.close()
    conn.close()
# contentoracle()
        # print(df['日期'])
if __name__=='__main__':
    train(input_path = "input_data.csv",model_path = "./rf.model")
    pre(input_path = "pre_data.csv",model_path = "./rf.model",output_path = "1.csv")
# #     readcsv()
# print(readcsv('15888156279041','201807'))
