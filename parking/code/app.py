#gevent
from gevent import monkey
monkey.patch_all()
from gevent.pywsgi import WSGIServer

#gevent end
import logging;
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='myapp.log',
                    filemode='a')
import os
import EntityAccess.Access

#import flask
from flask import Flask, request, render_template,redirect,url_for,escape,session,jsonify



app = Flask(__name__)
app.config['DEBUG']=True
app.secret_key=os.urandom(12)
@app.route('/',methods=['GET'])
def home():
    return render_template('sentrybox.html')
# 入场信息流水
@app.route('/GetCarIn',methods=['GET','POST'])
def GetCarIn():
    st=request.form['starttime']
    et=request.form['endtime']
    carinA=EntityAccess.Access.Carin()
    print(st,et)   
    if st !='' and et != '':
        carinlist=carinA.select(['ID','CardID','CarNO','EmpName','InTime','InControlName','InUserName','CardType','InWayName'],' from Vw_Park_CarIn where InTime >= %s and InTime <= %s'%(carinA.gdy(st),carinA.gdy(et)),['InWayName'])
    else:
        carinlist=carinA.select(['CardID','CarNO','InTime','InControlName','CardType'],' from Vw_Park_CarIn')
 
    
    if carinlist:
        result={'data':carinlist}
        return jsonify(result)
    else:
        return jsonify({'type':300,'message':'Not Data'})
@app.route('/sentrybox',methods=['GET'])
def sentrybox():
    return render_template('sentrybox.html')
# 出场信息流水
@app.route('/GetCarOut',methods=['POST'])
def GetCarOut():
    caroutA=EntityAccess.Access.Carin()
    caroutlist=caroutA.select(['InTime','OutTime','OutControlName','CardID','CardType','CarNO'],' from Vw_parK_CarOut')
    if caroutlist:
        result={'data':caroutlist}
        return jsonify(result)
    else:
        return jsonify({'type':300,'message':'Not Data'})
# 长期滞留车辆
@app.route('/GetRetention',methods=['POST'])
def GetRetention():
    st=request.form['starttime']
    et=request.form['endtime']
    carinA=EntityAccess.Access.Carin()
    carinlist=carinA.select(['ID','CardID','EmpName','CarNO','CardType','CarNoType','InControlName','InTime','InUserName']," from Vw_Park_CarIn where InTime >= %s and InTime <= %s"%(carinA.gdy(st),carinA.gdy(et)))
    print(carinlist)
    if carinlist:
        result={'data':carinlist}
        return jsonify(result)
    else:
        return jsonify({'type':300,'message':'Not Data'})
@app.route('/DelRetention',methods=['POST'])
def DelRetention():
    id=request.form['ID']
    carinA=EntityAccess.Access.Carin()
    result=carinA.delect('Vw_Park_CarIn','where ID = '+id)
    if result:
        return jsonify({'type':200,'message':'delect success'})
    else:
        return jsonify({'type':400,'message':'delect fail'})
@app.route('/retention',methods=['GET'])
def Retention():
    return render_template('retention.html')
# 设备异常登记
@app.route('/GetAnomaly',methods=['POST'])
def GetAnomaly():
    st=request.form['starttime']
    et=request.form['endtime']
    # status=request.form['DeviceStatus'] 
    carinA=EntityAccess.Access.Carin()
    carinlist=carinA.select(['ID','DeviceIP','DeviceName','UserDate','DeviceStatus','CreateUserName']," from Park_AllDeviceStatus where  UserDate >= %s and UserDate <= %s"%(carinA.gdy(st),carinA.gdy(et)))
    print(carinlist)
    if carinlist:
        result={'data':carinlist}
        return jsonify(result)
    else:
        return jsonify({'type':300,'message':'Not Data'})
@app.route('/anomaly',methods=['GET'])
def anomaly():
    return render_template('anomaly.html')
# 场内车辆查询
@app.route('/vehicleQuery',methods=['GET'])
def vehicleQuery():
    return render_template('vehicleQuery.html')
# 非法开闸查询
@app.route('/GetIllegality',methods=['POST'])
def GetIllegality():
    st=request.form['starttime']
    et=request.form['endtime'] 
    carinA=EntityAccess.Access.Carin()
    carinlist=carinA.select(['ID','CarNO','OutTime','OutControlName','OutUserName','CardTypeName','UnusualMemo']," from Vw_ParK_CarOut where  InTime >= %s and InTime <= %s and CardType < 5 and UnusualMemo !=''"%(carinA.gdy(st),carinA.gdy(et)))
    print(carinlist)
    if carinlist:
        result={'data':carinlist}
        return jsonify(result)
    else:
        return jsonify({'type':300,'message':'Not Data'})
@app.route('/Illegality',methods=['GET'])
def Illegality():
    return render_template('illegality.html')
# 异常出场查询
@app.route('/GetAbnormal',methods=['POST'])
def GetAbnormal():
    st=request.form['starttime']
    et=request.form['endtime']
    # status=request.form['DeviceStatus']    
    carinA=EntityAccess.Access.Carin()
    carinlist=carinA.select(['ID','CarNO','EmpName','CardType','CardID','AccountCharge','InTime','InControlName','OutTime','OutControlName','InUserName','OutUserName','OutWayName']," from Vw_ParK_CarOut where  OutTime >= %s and OutTime <= %s and CardType > 7 and OutWay > 0"%(carinA.gdy(st),carinA.gdy(et)),['InUserName','OutWayName'])
    # print(carinlist)
    if carinlist:
        result={'data':carinlist}
        return jsonify(result)
    else:
        return jsonify({'type':300,'message':'Not Data'})
@app.route('/abnormal',methods=['GET'])
def abnormal():
    return render_template('abnormal.html')
# 车流量统计
@app.route('/GetStatistics',methods=['GET','POST'])
def GetStatistics():
    TableType=request.form['tabletype']  
    st=request.form['starttime']      
    carinA=EntityAccess.Access.Carin()
    carinlist=carinA.CallProcedurec('Sp_Park_CarInOutTrafficHour',(st,TableType))
    if carinlist:
        result={'data':carinlist}
        return jsonify(result)
    else:
        return jsonify({'type':300,'message':'Not Data'})
@app.route('/statistics',methods=['GET'])
def statistics():
    return render_template('statistics.html')
@app.route('/ffkz',methods=['POST'])
def ffkz():
    st=request.form['starttime']
    et=request.form['endtime']
    logging.debug(st)
    logging.debug(et)
    print(st,et)
    return jsonify({'type':200,'message':'success','content':{'starttime':st,'endtime':et}})
@app.route('/illegality',methods=['GET'])
def illegality():
    return render_template('illegality.html')
if __name__ == '__main__':
    #app.run(host='0.0.0.0',port=8099)

    http_server=WSGIServer(('0.0.0.0',8099),app)
    #logging.debug('服务已启动当前为调试模式')
    # logging.debug('debug message')
    # logging.info('info message')
    # logging.warn('warn message')
    # logging.error('error message')
    # logging.critical('critical message')

    print('yiqidong')
    http_server.serve_forever()