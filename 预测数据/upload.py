import os
import datetime
from flask import Flask, request, render_template, redirect, url_for, escape, session, jsonify, Response, flash, make_response, send_file,send_from_directory
from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()
import flask_uploads
import mimetypes
import Access.GBDT as pr
app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = os.urandom(12)
app.config['UPLOADS_DEFAULT_DEST'] = 'uploads'
app.config['UPLOADED_FILES_DENY'] = set(['csv'])
csv = flask_uploads.UploadSet('csv')
flask_uploads.configure_uploads(app, csv)


@app.route('/forecast',methods=['GET'])
@app.route('/forecast/<docid>', methods=['GET'])
def index(docid=None):
    print('11111111',docid)
    if docid==None:
        docid=pr.getorderid()
        os.mkdir("./uploads/csv/"+str(docid))
        print('1',docid)
        return render_template('first.html',docid=str(docid))
    else:
        print('2',docid)
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
            # program=request.form['program']
            # print(program)
            print(filee)
            if filee.filename != '':
                # docid = pr.getorderid()
                print(docid)
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
                            result=pr.readcsv(docid=data['docid'])
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
                        result=pr.readcsv(docid=data['docid'])                        
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
                pr.BuildInputCSV(startdate=data['startdate'],enddate=data['enddate'],docid=data['docid'])
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
            pr.BuildInputCSV(startdate=data['startdate'],enddate=data['enddate'],docid=data['docid'])
            return jsonify({'type':200,'message':'success'})
        else:
            return jsonify({'type':200,'message':'parameter error'})
    except Exception as ex:
        logger.error(str(ex))
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
                pr.BuildPreCSV(startdate=data['startdate'],enddate=data['enddate'],docid=data['docid'])
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
            pr.BuildPreCSV(startdate=data['startdate'],enddate=data['enddate'],docid=data['docid'])
            return jsonify({'type':200,'message':'success'})
        else:
            return jsonify({'type':200,'message':'parameter error'})
    except Exception as ex:
        logger.error(str(ex))
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +' upload.py BuildInput [ex]:', str(ex))
        return jsonify({'type':4010,'message':str(ex)}) 

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 8081), app)
    print('yiqidong')
    http_server.serve_forever()
