from flask import Flask,request,jsonify
import werkzeug
from flask.helpers import make_response
from flask_restful import reqparse
import os
import shutil
import subprocess
import time
import pandas as pd
from flask_restful import Resource, Api
from src.database import init_db
from subprocess import Popen, PIPE
from src.app import app
from src.parser import ResultTable

UPLOAD_DIR = "lib/hasp/"
HASP_DIR = "RunHasp.bat"

api=Api(app)

@app.route("/")
def hello_world():
    return "<p>test</p>"

@app.route('/setting',methods=['POST'])
def setting():
    payload = request.json
    print ('payload',payload)

    #b.datデータを作成する
    try:
        f=open('b.dat','x')
        f.write(f'{payload["b"]["rooms"][0]["roomId"]} {payload["b"]["rooms"][0]["x1"]}\n')
        f.close()
    except:
        pass

    return {'status':payload}

class Result(Resource):
    def get(self):
        resultTable=ResultTable()
        return {'data':resultTable.retrieve()}

api.add_resource(Result,'/result')

@app.route('/run',methods=['POST'])
def upload_multipart():
    if 'uploadFile' not in request.files:
        make_response(jsonify({'result':'uploadFile is required.'}))
    #print ('request.files',request.files)
    file = request.files['b']
    fileName = file.filename

    saveFileName = werkzeug.utils.secure_filename(fileName)
    #ここでdataフォルダに移動すべき
    #file.save(os.path.join(UPLOAD_DIR, saveFileName))
    file.save(saveFileName)
    #print ('directory',os.path.join(os.getcwd(), HASP_DIR))

    #batchファイルをrunする
    p = Popen(os.path.join(os.getcwd(), HASP_DIR))
    stdout,stderr=p.communicate()
    print('STDOUT: {}'.format(stdout))

    #計算が終了したら、計算結果をパースする

    #ブラウザからデータを取得できるAPIを準備する(visualization)

    #input001.txtを消す
    #dataのほうにファイルを移動する
    folder=request.form.get('name')
    
    #フォルダ名が既にあるか確認必要
    print('path',os.path.join(os.getcwd(), folder, "input001.txt"))
    new_path=os.path.join(os.path.join("data",folder))

    #awaitする必要あり
    time.sleep(3)
    if os.path.exists(new_path):
        print("path already exist")
        pass
        #名前を変えてファイルを保存する方法必要
    else:
        os.makedirs(new_path)
        shutil.move("input001.txt",os.path.join("data",folder, "input001.txt"))
        shutil.move("out20.datweath.dat",os.path.join("data",folder, "out20.datweath.dat"))
        i=1

        roomExist=True
        while roomExist:
            output_file1='out20.dat___{}.csv'.format(i)
            #print ('output_file1',output_file1)
            try:     
                #データをparseして、データベースに保存する   
                df1=pd.read_csv(output_file1)
                roomT=df1["ROOM-T"]
                #print ('df1',roomT.to_json())
                resultTable=ResultTable()
                resultTable.insert(roomT.to_json())
         
                shutil.move(output_file1,os.path.join("data",folder, output_file1))
                i+=1
            except:
                roomExist=False

        

    return make_response((jsonify({'result':'upload OK.'})))

if __name__=="__main__":
    app.run(debug=True)