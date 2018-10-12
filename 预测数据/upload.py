import os
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


@app.route('/', methods=['GET'])
def index():
    return render_template('upload.html')
@app.route('/downloads/result/<docid>',methods=['GET'])
def show(docid):
    # url=csv.path(docid)
    path=os.path.abspath("./uploads/csv/"+docid)#+"/1.csv"
    print(path)
    resp=make_response(send_from_directory(path,"1.csv",as_attachment=True))
    # resp.headers['Content-Type']=mimetypes.guess_type(filename)[0]
    resp.headers['Content-Disposition']='attachment; filename={}'.format(docid+".csv".encode().decode('latin-1'))
    return resp


@app.route('/first', methods=['GET'])
def first():
    return render_template('first.html')


@app.route('/input_data', methods=['POST'])
def input_data():
    if request.method == 'POST' and 'csv' in request.files:
        try:
            filee = request.files['csv']
            # program=request.form['program']
            # print(program)
            print(filee)
            if filee.filename != '':
                docid = pr.getorderid()
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


@app.route('/prediction', methods=['POST'])
def prediction():
    try:
        if request.get_json(silent=True) == None:
            return jsonify({'type': 3010, 'message': 'Data is not json'})
        else:
            data = request.get_json()
            if 'docid' in data:
                pr.pre(input_path="./uploads/csv/" + str(data['docid']) + "/pre_data.csv", model_path="./uploads/csv/" + str(
                    data['docid']) + "/rf.model", output_path="./uploads/csv/" + str(data['docid']) + "/1.csv")
                if 'date' in data:
                    result = pr.readcsv(data['docid'], data['date'])
                else:
                    result = pr.readcsv(data['docid'])
    except Exception as ex:
        return jsonify({'type': 3020, 'message': str(ex)})
    else:
        if result:
            return jsonify({'type': 200, 'message': result})
        else:
            return jsonify({'type': 3030, 'message': result})


if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 8081), app)
    print('yiqidong')
    http_server.serve_forever()
