from flask import Flask, json,request,jsonify
import werkzeug
from flask.helpers import make_response
from flask_restful import reqparse
import os
import shutil
import subprocess
import time
import pandas as pd
from flask_restful import Resource, Api,reqparse
from flask_sqlalchemy import SQLAlchemy
from src.database import init_db
from subprocess import Popen, PIPE
import datetime
from src.app import app
from src.parser import ResultTable,ProjectTable
from src.models.models import Project,Result
from flask_cors import CORS

UPLOAD_DIR = "lib/hasp/"
HASP_DIR = "RunHasp.bat"

api=Api(app)
CORS(app,origins="http://localhost:8000",allow_headers=["Access-Control-Allow-Credentials"])

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

#API endpointの設定
class ProjectEndpoint(Resource):
    def get(self):
        projectTable=ProjectTable()
        return jsonify({"data":projectTable.retrieve()})

class ResultEndpoint(Resource):
    def get(self,project_id):
        #parser=reqparse.RequestParser()
        #pId=parser.parse_args()
        resultTable=ResultTable()
        return {"data":resultTable.retrieve(project_id)}

api.add_resource(ProjectEndpoint,'/projects')
api.add_resource(ResultEndpoint,'/results/<project_id>')

@app.route('/run',methods=['POST'])
def upload_multipart():
    if 'uploadFile' not in request.files:
        make_response(jsonify({'result':'uploadFile is required.'}))
    #print ('request.files',request.files)
    file = request.files['b']
    fileName = file.filename

    saveFileName = werkzeug.utils.secure_filename(fileName)
    #TODO:ここでdataフォルダに移動すべき
    #file.save(os.path.join(UPLOAD_DIR, saveFileName))
    print('saveFileName: {}'.format(saveFileName))
    file.save(saveFileName)
    #print ('directory',os.path.join(os.getcwd(), HASP_DIR))

    #batchファイルをrunする
    p = Popen(os.path.join(os.getcwd(), HASP_DIR))
    
    stdout,stderr=p.communicate()
    print('STDOUT: {}'.format(stdout))

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
        #TODO:名前を変えてファイルを保存する方法必要
    else:
        os.makedirs(new_path)
        shutil.move("input001.txt",os.path.join("data",folder, "input001.txt"))
        shutil.move("out20.datweath.dat",os.path.join("data",folder, "out20.datweath.dat"))
        i=1

        #projectTable=ProjectTable()
        #projectInstance=projectTable.insert(folder)
        db=SQLAlchemy()
        p=Project(name=folder)

        roomExist=True
        while roomExist:
            output_file1='out20.dat___{}.csv'.format(i)
            print ('output_file1',output_file1)
            try:     
                #データをparseして、データベースに保存する   
                df1=pd.read_csv(output_file1)
                #print ('df1',df1)
                resultTable=ResultTable()
                roomT=df1["ROOM-T"].to_json()
                clodS=df1["CLOD-S"].to_json()
                rhexS=df1["RHEX-S"].to_json()
                ahexS=df1["AHEX-S"].to_json()
                fs=df1["FS"].to_json()
                roomH=df1["ROOM-H"].to_json()
                clodL=df1["CLOD-L"].to_json()
                rhexL=df1["RHEX-L"].to_json()
                ahexL=df1["AHEX-L"].to_json()
                fl=df1["FL"].to_json()
                mrt=df1["MRT'"].to_json()

                #時間を計算する
                month=df1["MO"].tolist()
                day=df1["DY"].tolist()
                hour=df1["HR"].tolist()
                #print('month',month)
                timeData={}
                for i in range(len(month)):
                    #timeseriesデータはjson serializableじゃない
                    #timeData[i]=datetime.datetime(2021,month[i],day[i],hour[i]-1)
                    timeData[i]=f'2021/{str(month[i])}/{str(day[i])} {str(hour[i])}:00'

                #r=resultTable.insert(roomT,clodS,rhexS,ahexS,fs,roomH,clodL,rhexL,ahexL,fl,mrt)
                r=Result(hour=timeData,roomT=roomT,clodS=clodS,rhexS=rhexS,ahexS=ahexS,fs=fs,roomH=roomH,clodL=clodL,rhexL=rhexL,ahexL=ahexL,fl=fl,mrt=mrt)
                print ('r',r.project_id)
                p.results.append(r)
                db.session.add(r)
         
                shutil.move(output_file1,os.path.join("data",folder, output_file1))
                i+=1
            except:
                roomExist=False

        db.session.add(p)
        db.session.commit()

    return make_response((jsonify({
        'status':'success',
        'url':f'http://localhost:8000/{str(r.project_id)}/timeseries'
        })))

if __name__=="__main__":
    app.run(debug=True)