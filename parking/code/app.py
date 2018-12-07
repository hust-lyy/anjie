#gevent
from gevent import monkey
monkey.patch_all()
from gevent.pywsgi import WSGIServer

#gevent end
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='myapp.log',
                    filemode='a')
import os
import datetime
import EntityAccess.Access

#import flask
from flask import Flask, request, render_template, redirect, url_for, escape, session, jsonify,Response,flash,make_response,send_file,send_from_directory
import flask_uploads
import mimetypes
import EntityAccess.GBDT as pr
import EntityAccess.Utility as au

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = os.urandom(12)
app.config['UPLOADS_DEFAULT_DEST'] = 'uploads'
app.config['UPLOADED_FILES_DENY'] = set(['csv'])
csv = flask_uploads.UploadSet('csv')
flask_uploads.configure_uploads(app, csv)

# 首页
@app.route('/', methods=['GET'])
@app.route('/index',methods=['GET'])
def home():    
    return render_template('index.html')
@app.route('/GetParkingMessage',methods=['GET'])
def GetParkingMessage():
    carinA=EntityAccess.Access.Carin()
    result=carinA.indexProcedurec()
    if result:
        return jsonify({'data':result})
    else:
        return jsonify({'type':100,'message':'Not reason'})
# 获取实时出入场信息
@app.route('/GetInOut',methods=['GET'])
def GetInOut():
    carinA=EntityAccess.Access.Carin()
    carin=carinA.nowcarin()
    car=EntityAccess.Access.Carin()
    carout=car.nowcarout()
    if carin and carout:
        return jsonify({'type':200,'message':{'in':carin,'out':carout}})
    elif carin:
        return jsonify({'type':201,'message':{'in':carin}})
    elif carout:
        return jsonify({'type':202,'message':{'out':carout}})
    else:
        return jsonify({'type':300,'message':'Not data'})
# 入场信息流水


@app.route('/GetCarIn', methods=['GET', 'POST'])
def GetCarIn():
    st = request.form['starttime']
    et = request.form['endtime']
    carinA = EntityAccess.Access.Carin()
    if st != '' and et != '':
        carinlist = carinA.select(['ID', 'CardID', 'CarNO', 'EmpName', 'InTime', 'InControlName', 'InUserName', 'CardTypeName', 'InWayName'],
                                  ' from Vw_Park_CarIn where InTime >= %s and InTime <= %s' % (carinA.gdy(st), carinA.gdy(et)), ['InWayName'])
    else:
        carinlist = carinA.select(
            ['CardID', 'CarNO', 'InTime', 'InControlName', 'CardTypeName'], ' from Vw_Park_CarIn')

    if carinlist:
        result = {'data': carinlist}
        return jsonify(result)
    else:
        return jsonify({'type': 300, 'message': 'Not Data'})


@app.route('/sentrybox', methods=['GET'])
def sentrybox():
    return render_template('sentrybox.html')
# 出场信息流水


@app.route('/GetCarOut', methods=['POST'])
def GetCarOut():
    caroutA = EntityAccess.Access.Carin()
    caroutlist = caroutA.select(
        ['InTime', 'OutTime', 'OutControlName', 'CardID', 'CardTypeName', 'CarNO'], ' from Vw_parK_CarOut')
    if caroutlist:
        result = {'data': caroutlist}
        return jsonify(result)
    else:
        return jsonify({'type': 300, 'message': 'Not Data'})
# 控制器状态


@app.route('/GetControl', methods=['GET'])
def GetControl():
    control = EntityAccess.Access.Carin()
    controllist = control.select(
        ['ContName', 'BoxName', 'DIP', 'RealStatus'], ' from Vw_Park_DeviceStatus')
    print(controllist)
    if controllist:
        templist = []        
        for control in controllist:
            print(control)
            print(control['RealStatus'])
            if control['RealStatus']!='None':
                templist = control['RealStatus'][:7].split(',')            
                control['Communication']=templist[0]            
                control['Induction']=templist[1]
                control['Gate']=templist[2]
                control['CardMachine']=templist[3]
            else:
                control['Communication']='0'           
                control['Induction']='0'
                control['Gate']='0'
                control['CardMachine']='0'
    
            
        return jsonify({'type': 200, 'message': controllist})
    else:
        return jsonify({'type': 300, 'message': 'Not Data'})
@app.route('/control',methods=['GET'])
def control():
    return render_template('control.html')
# 长期滞留车辆


@app.route('/GetRetention', methods=['POST'])
def GetRetention():
    st = request.form['starttime']
    et = request.form['endtime']
    carinA = EntityAccess.Access.Carin()
    carinlist = carinA.select(['ID', 'CardID', 'EmpName', 'CarNO', 'CardTypeName', 'CarNoType', 'InControlName', 'InTime',
                               'InUserName'], " from Vw_Park_CarIn where InTime >= %s and InTime <= %s" % (carinA.gdy(st), carinA.gdy(et)))
    if carinlist:
        result = {'data': carinlist}
        return jsonify(result)
    else:
        return jsonify({'type': 300, 'message': 'Not Data'})


@app.route('/DelRetention', methods=['POST'])
def DelRetention():
    try:
        data = request.get_json()
        ids = data['ID']
        carinA = EntityAccess.Access.Carin()
        pre = 'where ID in ('
        for index in range(len(ids) - 1):
            pre += str(ids[index]) + ','
        pre += str(ids[len(ids) - 1])
        pre += ')'
        logging.debug(pre)
        carinA.delect('Park_CarIn', pre)
    except Exception as ex:
        logging.error(ex)
        return jsonify({'type': 400, 'message': 'delect fail'})
    else:
        return jsonify({'type': 200, 'message': 'delect success'})

    # result=carinA.delect('Vw_Park_CarIn',pre)
    # if result:
    #     return jsonify({'type':200,'message':'delect success'})
    # else:
    #     return jsonify({'type':400,'message':'delect fail'})


@app.route('/retention', methods=['GET'])
def Retention():
    return render_template('retention.html')
# 设备异常登记


@app.route('/GetAnomaly', methods=['POST'])
def GetAnomaly():
    st = request.form['starttime']
    et = request.form['endtime']
    # status=request.form['DeviceStatus']
    carinA = EntityAccess.Access.Carin()
    carinlist = carinA.select(['ID', 'DeviceIP', 'DeviceName', 'UserDate', 'DeviceStatus', 'CreateUserName'],
                              " from Park_AllDeviceStatus where  UserDate >= %s and UserDate <= %s" % (carinA.gdy(st), carinA.gdy(et)))
    if carinlist:
        result = {'data': carinlist}
        return jsonify(result)
    else:
        return jsonify({'type': 300, 'message': 'Not Data'})


@app.route('/anomaly', methods=['GET'])
def anomaly():
    return render_template('anomaly.html')
# 场内车辆查询


@app.route('/vehicleQuery', methods=['GET'])
def vehicleQuery():
    return render_template('vehicleQuery.html')
# 非法开闸查询


@app.route('/GetIllegality', methods=['POST'])
def GetIllegality():
    st = request.form['starttime']
    et = request.form['endtime']
    carinA = EntityAccess.Access.Carin()
    carinlist = carinA.select(['ID', 'CarNO', 'OutTime', 'OutControlName', 'OutUserName', 'CardTypeName', 'UnusualMemo'],
                              " from Vw_ParK_CarOut where  InTime >= %s and InTime <= %s and CardType < 5 and UnusualMemo !=''" % (carinA.gdy(st), carinA.gdy(et)))
    if carinlist:
        result = {'data': carinlist}
        return jsonify(result)
    else:
        return jsonify({'type': 300, 'message': 'Not Data'})


@app.route('/Illegality', methods=['GET'])
def Illegality():
    return render_template('illegality.html')
# 异常出场查询


@app.route('/GetAbnormal', methods=['POST'])
def GetAbnormal():
    st = request.form['starttime']
    et = request.form['endtime']
    # status=request.form['DeviceStatus']
    carinA = EntityAccess.Access.Carin()
    carinlist = carinA.select(['ID', 'CarNO', 'EmpName', 'CardType', 'CardID', 'AccountCharge', 'InTime', 'InControlName', 'OutTime', 'OutControlName', 'InUserName', 'OutUserName',
                               'OutWayName'], " from Vw_ParK_CarOut where  OutTime >= %s and OutTime <= %s and CardType > 7 and OutWay > 0" % (carinA.gdy(st), carinA.gdy(et)), ['InUserName', 'OutWayName'])
    if carinlist:
        result = {'data': carinlist}
        return jsonify(result)
    else:
        return jsonify({'type': 300, 'message': 'Not Data'})


@app.route('/abnormal', methods=['GET'])
def abnormal():
    return render_template('abnormal.html')
# 车流量统计


@app.route('/GetStatistics', methods=['GET', 'POST'])
def GetStatistics():
    TableType = request.form['tabletype']
    st = request.form['starttime']
    carinA = EntityAccess.Access.Carin()
    carinlist = carinA.CallProcedurec(
        'Sp_Park_CarInOutTrafficHour', (st, TableType))
    if carinlist:
        result = {'data': carinlist}
        return jsonify(result)
    else:
        return jsonify({'type': 300, 'message': 'Not Data'})


@app.route('/statistics', methods=['GET'])
def statistics():
    return render_template('statistics.html')


@app.route('/ffkz', methods=['POST'])
def ffkz():
    st = request.form['starttime']
    et = request.form['endtime']
    return jsonify({'type': 200, 'message': 'success', 'content': {'starttime': st, 'endtime': et}})


@app.route('/illegality', methods=['GET'])
def illegality():
    return render_template('illegality.html')









#----------------------------------------------------预测数据-------------------------------------------------

@app.route('/forecast',methods=['GET'])
@app.route('/forecast/<docid>', methods=['GET'])
def index(docid=None):
    print('11111111',docid)
    if docid==None:
        docid=au.getorderid()
        os.mkdir("./uploads/csv/"+str(docid))
        print('1',docid)
        return render_template('first.html',docid=str(docid))
    else:
        print('2',docid)
        data=request.args.to_dict()
        print(data['state'])
        if 'state' in data and data['state']=='1':
            historydata=au.readhistorycsv(docid=docid)
            return render_template('first.html',docid=str(docid),hdata=historydata)
        else:
            return render_template('first.html',docid=str(docid))

# @app.route('/first', methods=['GET'])
# def first():
#     return render_template('first.html')
@app.route('/historydata/<docid>',methods=['GET'])
def historydata(docid=None):
    return render_template('historydata.html',docid=docid)
@app.route('/importdata/<docid>',methods=['GET'])
def importdata(docid=None):
    return render_template('importdata.html',docid=docid)
#下载文件
@app.route('/downloads/result/<docid>/<filename>',methods=['GET'])
def show(docid,filename):
    # url=csv.path(docid)
    path=os.path.abspath("./uploads/csv/"+docid)#+"/1.csv"
    print(path)
    resp=make_response(send_from_directory(path,filename+'.csv',as_attachment=True))
    # resp.headers['Content-Type']=mimetypes.guess_type(filename)[0]
    resp.headers['Content-Disposition']='attachment; filename={}'.format(docid+"_"+filename+".csv".encode().decode('latin-1'))
    return resp

#上传历史数据CSV
@app.route('/input_data', methods=['POST'])
def input_data():
    if request.method == 'POST' and 'csv' in request.files and 'docid' in request.form:
        try:
            docid=request.form['docid']
            filee = request.files['csv']            
            # print(filee)
            if filee.filename != '':
                # docid = pr.getorderid()
                print(docid)
                print(os.path.exists('./uploads/csv/' + str(docid)+'/input_data.csv'))
                if os.path.exists('./uploads/csv/' + str(docid)+'/input_data.csv'):
                    os.remove('./uploads/csv/' + str(docid)+'/input_data.csv')
                filename = csv.save(request.files['csv'], folder=str(
                    docid), name='input_data.csv')
                pr.train(input_path="./uploads/csv/" + str(docid) + "/input_data.csv",
                         model_path="./uploads/csv/" + str(docid) + "/rf.model")
        except Exception as ex:
            print(str(ex))
            return jsonify({'type': 1030, 'message': str(ex)})
        else:
            return jsonify({'type': 200, 'message': str(docid)})
        #     pass

        #     return jsonify({'type':200,'message':str(docid)})
        # else:
        #     return jsonify({'type':1010,'message':'filename is null'})
    else:
        return jsonify({'type': 1020, 'message': 'not found'})

#上传预测温度CSV
@app.route('/pre_data', methods=['POST'])
def pre_data():
    if request.method == 'POST' and 'csv' in request.files and 'docid' in request.form:
        filee = request.files['csv']
        docid = request.form['docid']
        print(request.form)
        print(docid)
        if filee.filename != '' and docid != None:
            if os.path.exists('./uploads/csv/' + str(docid)):
                print(os.path.exists('./uploads/csv/' + str(docid)+'/pre_data.csv'))
                if os.path.exists('./uploads/csv/' + str(docid)+'/pre_data.csv'):
                    os.remove('./uploads/csv/' + str(docid)+'/pre_data.csv')
                filename = csv.save(
                    request.files['csv'], str(docid), 'pre_data.csv')
                return jsonify({'type': 200, 'message': docid})
            else:
                return jsonify({'type': 2030, 'message': 'not found ' + str(docid)})
        else:
            return jsonify({'type': 2010, 'message': 'filename is null'})
    else:
        return jsonify({'type': 2020, 'message': 'not found'})

#生成预测数据
@app.route('/prediction', methods=['POST'])
def prediction():
    try:
        if request.get_json(silent=True) == None:
            return jsonify({'type': 3010, 'message': 'Data is not json'})
        else:
            data = request.get_json()
            if 'docid' in data and data['docid']!='':
                if os.path.exists('./uploads/csv/' + str(data['docid'])+'/input_data.csv'):
                    if os.path.exists('./uploads/csv/' + str(data['docid'])+'/pre_data.csv'):
                        if os.path.exists('./uploads/csv/' + str(data['docid'])+'/rf.model'):
                            pr.pre(input_path="./uploads/csv/" + str(data['docid']) + "/pre_data.csv", model_path="./uploads/csv/" + str(data['docid']) + "/rf.model", output_path="./uploads/csv/" + str(data['docid']) + "/result.csv")
                            result=au.readcsv(docid=data['docid'])
                        else:
                            return jsonify({'type':3020,'message':'没有找到模型'}) 
                    else:
                        return jsonify({'type':3030,'message':'没有找到预测温度CSV'}) 
                else:
                    return jsonify({'type':3040,'message':'没有找到历史数据CSV'}) 
            else:
                return jsonify({'type':3050,'message':'parameter error'}) 
    except Exception as ex:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +' upload.py prediction [ex]:', str(ex))
        return jsonify({'type':3010,'message':str(ex)}) 
    else:
        if result:
            temp={'type': 200, 'message': 'success'}
            return jsonify({**temp,**result})
        else:
            temp={'type': 3060, 'message':'success'}
            return jsonify({**temp,**result})
@app.route('/GETprediction', methods=['GET'])
def getprediction():
    try:
        data=request.args.to_dict()
        if 'docid' in data and data['docid']!='':
            if os.path.exists('./uploads/csv/' + data['docid']+'/input_data.csv'):
                if os.path.exists('./uploads/csv/' + data['docid']+'/pre_data.csv'):
                    if os.path.exists('./uploads/csv/' + data['docid']+'/rf.model'):
                        pr.pre(input_path="./uploads/csv/" + str(data['docid']) + "/pre_data.csv", model_path="./uploads/csv/" + str(data['docid']) + "/rf.model", output_path="./uploads/csv/" + str(data['docid']) + "/result.csv")
                        result=au.readcsv(docid=data['docid'])                        
                    else:
                        return jsonify({'type':3020,'message':'没有找到模型'}) 
                else:
                    return jsonify({'type':3030,'message':'没有找到预测温度CSV'}) 
            else:
                return jsonify({'type':3040,'message':'没有找到历史数据CSC'}) 
        else:
            return jsonify({'type':3050,'message':'parameter error'}) 
    except Exception as ex:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +' upload.py prediction [ex]:', str(ex))
        return jsonify({'type':3010,'message':str(ex)}) 
    else:
        if result:
            temp={'type': 200, 'message': 'success'}
            return jsonify({**temp,**result})
        else:
            temp={'type': 3060, 'message':'success'}
            return jsonify({**temp,**result})
#生成历史数据CSV
@app.route('/Build_input',methods=['POST'])
def BuildInput():
    try:
        if request.get_json(silent=True) == None:
            return jsonify({'type': 3010, 'message': 'Data is not json'})
        else:
            data = request.get_json()
            if 'docid' in data and data['docid']!='' and 'startdate' in data and data['startdate']!='' and 'enddate' in data and data['enddate']!='':
                au.BuildInputCSV(startdate=data['startdate'],enddate=data['enddate'],docid=data['docid'])
                return jsonify({'type':200,'message':'success'})
            else:
                return jsonify({'type':4020,'message':'parameter error'})

    except Exception as ex:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +' upload.py BuildInput [ex]:', str(ex))
        return jsonify({'type':4010,'message':str(ex)}) 
@app.route('/GETBuild_input',methods=['GET'])
def GETBuildInput():
    try:
        data=request.args.to_dict()
        if 'docid' in data and data['docid']!='' and 'startdate' in data and data['startdate']!='' and 'enddate' in data and data['enddate']!='':
            au.BuildInputCSV(startdate=data['startdate'],enddate=data['enddate'],docid=data['docid'])
            return jsonify({'type':200,'message':'success'})
        else:
            return jsonify({'type':200,'message':'parameter error'})
    except Exception as ex:
        logging.error(str(ex))
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +' upload.py BuildInput [ex]:', str(ex))
        return jsonify({'type':4010,'message':str(ex)}) 
#生成预测温度CSV
@app.route('/Build_pre',methods=['POST'])
def BuildPre():
    try:
        if request.get_json(silent=True) == None:
            return jsonify({'type': 3010, 'message': 'Data is not json'})
        else:
            data = request.get_json()
            if 'docid' in data and data['docid']!='' and 'startdate' in data and data['startdate']!='' and 'enddate' in data and data['enddate']!='':
                au.BuildPreCSV(startdate=data['startdate'],enddate=data['enddate'],docid=data['docid'])
                return jsonify({'type':200,'message':'success'})
            else:
                return jsonify({'type':200,'message':'parameter error'})
    except Exception as ex:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +' upload.py BuildInput [ex]:', str(ex))
        return jsonify({'type':4010,'message':str(ex)}) 
@app.route('/GETBuild_pre',methods=['GET'])
def GETBuildPre():
    try:
        data=request.args.to_dict()
            # data = request.get_json()
        if 'docid' in data and data['docid']!='' and 'startdate' in data and data['startdate']!='' and 'enddate' in data and data['enddate']!='':
            au.BuildPreCSV(startdate=data['startdate'],enddate=data['enddate'],docid=data['docid'])
            return jsonify({'type':200,'message':'success'})
        else:
            return jsonify({'type':200,'message':'parameter error'})
    except Exception as ex:
        logging.error(str(ex))
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +' upload.py BuildInput [ex]:', str(ex))
        return jsonify({'type':4010,'message':str(ex)}) 















if __name__ == '__main__':
    #app.run(host='0.0.0.0',port=8099)

    http_server = WSGIServer(('0.0.0.0', 8099), app)
    #logging.debug('服务已启动当前为调试模式')
    # logging.debug('debug message')
    # logging.info('info message')
    # logging.warn('warn message')
    # logging.error('error message')
    # logging.critical('critical message')

    print('yiqidong')
    http_server.serve_forever()
