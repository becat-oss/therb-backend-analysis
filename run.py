from unittest import result
from flask import Flask, json,request,jsonify
import werkzeug
from flask.helpers import make_response
import os
import shutil
import time
import pandas as pd
from flask_restful import Resource, Api
from src.database import init_db
from subprocess import Popen, PIPE
from src.app import app
from src.parser import ProjectTable,TherbTable
from src.models.models import Project, db_session,Therb
from flask_cors import CORS
import shutil
from zipfile import ZipFile
import sys
from flask_sqlalchemy import SQLAlchemy

UPLOAD_DIR = "lib/hasp/"
HASP_DIR = "RunHasp.bat"

#frontendからのデータ取得を可能にする
api=Api(app)
CORS(app,origins="http://localhost:8000",allow_headers=["Access-Control-Allow-Credentials"])
CORS(app,origins="http://localhost:3000",allow_headers=["Access-Control-Allow-Credentials"])

@app.route("/")
def hello_world():
    return "<p>this is API server</p>"

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
class ProjectListEndpoint(Resource):
    def get(self):
        projectTable=ProjectTable()
        return jsonify({"data":projectTable.retrieve()})

    def delete(self,id):
        projectTable=ProjectTable()
        projectTable.delete(id)
        return {"status":"success"}

class ProjectEndpoint(Resource):
    def delete(self,id):
        projectTable=ProjectTable()
        projectTable.delete(id)
        #TODO:projectを消したときに紐づいているresultも消すようにしたい
        return {"status":"success"}

class ResultEndpoint(Resource):
    def get(self,project_id):
        #parser=reqparse.RequestParser()
        #pId=parser.parse_args()
        resultTable=ResultTable()
        return {"data":resultTable.retrieve(project_id)}

    def delete(self,project_id):
        resultTable=ResultTable()
        resultTable.delete(project_id)
        # obj=Result.query.filter_by(project_id=project_id).one()
        # db=SQLAlchemy()
        # db.session.delete(obj)
        # db.session.commit()
        return {"status":"success"}

class TherbEndpoint(Resource):
    def get(self,project_id):
        therbTable=TherbTable()
        return {"data":therbTable.retrieve(project_id)}

api.add_resource(ProjectListEndpoint,'/projects')
api.add_resource(ProjectEndpoint,'/projects/<id>')
api.add_resource(ResultEndpoint,'/results/<project_id>')
api.add_resource(TherbEndpoint,'/therb/<project_id>')

@app.route('/download/<project_name>',methods=['GET'])
def download(project_name):
    response = make_response(jsonify({"data":"download"}))
    #FIXME: pathをproject_nameではなく、project_idにそろえる
    #データをzip化する
    shutil.make_archive(f'data/{project_name}', 'zip', f'data/{project_name}')
    response.data = open(f'data/{project_name}.zip', 'rb').read()
    response.headers['Content-Type'] = 'application/zip'
    response.headers['Content-Disposition'] = 'attachment; filename={project_name}.zip'.format(project_name=project_name)
    return response

@app.route('/therb/run',methods=['POST'])
def run_therb():
    # dataset = request.files['dataset']
    # datasetName = dataset.filename

    # folder = os.path.join("data",datasetName.replace(".zip",""))
    # #zipファイルを保存する
    # saveFile(dataset)

    # #zipファイルを解凍する
    # with ZipFile(datasetName, 'r') as zip:
    #     zip.extractall("data")

    # shutil.copy("lib/therb/therb.exe",os.path.join(folder, "therb.exe"))
    # shutil.copy("lib/therb/libifcoremd.dll",os.path.join(folder, "libifcoremd.dll"))
    # shutil.copy("lib/therb/libmmd.dll",os.path.join(folder, "libmmd.dll"))
    # shutil.copy("lib/therb/svml_dispmd.dll",os.path.join(folder, "svml_dispmd.dll"))

    # #zipファイルを削除する
    # os.remove(datasetName)
    # os.chdir(folder)
    # #print (os.getcwd())
    # #therbシミュレーションをrunする
    # p = Popen("therb.exe")
    
    # stdout,stderr=p.communicate()
    # print('STDOUT: {}'.format(stdout))

    # #root directoryに戻る必要
    # os.chdir(sys.path[0])
    # p=Project(name=datasetName.replace(".zip",""))

    # df=parseTherb(folder)

    # roomCount=int((len(df.columns)-4)/6)
    # db=SQLAlchemy()

    # for i in range(1,roomCount+1):
    #     time = df['time'].to_json()
    #     temperature=df[f'room{i}_temperature'].to_json()
    #     relativeHumidity=df[f'room{i}_relative_humidity'].to_json()
    #     absoluteHumidity=df[f'room{i}_absolute_humidity'].to_json()

    #     r=Therb(
    #         project_id=p.id,
    #         time=time,
    #         name=f'room{i}',
    #         temp=temperature,
    #         relHumidity=relativeHumidity,
    #         absHumidity=absoluteHumidity
    #     )

    #     p.therb.append(r)
    #     db.session.add(p)

    # db.session.add(p)
    # db.session.commit()

    # #dataフォルダのデータも削除する
    # shutil.rmtree(os.path.join("data",datasetName.replace(".zip","")))

    return make_response((jsonify({
        'status':'success',
        'message':'therb simulation is finished',
        'data':{
            'project_id':"temp",
            'url':"not implemented yet",
            'api':f'https://oyster-app-8jboe.ondigitalocean.app/therb/temp'
        }
    })))

def parseTherb(folder):
    def setColumn(df):
        #roomCount=(len(df.columns)-3)/3
        roomCount=(len(df.columns)-4)/6
        colName=['month','day','hour','outdoor']
        for i in range(1,int(roomCount)+1):
            colName.append(f'room{i}_temperature')
            colName.append(f'room{i}_relative_humidity')
            colName.append(f'room{i}_absolute_humidity')
            colName.append(f'room{i}_knknown1')
            colName.append(f'room{i}_knknown2')
            colName.append(f'room{i}_knknown3')

        df.columns=colName

        return df

    def formatData(col):
        temp = int(col)
        if len(str(temp))==1:
            return '0'+str(temp)
        else:
            return str(temp)

    def date_parser(x):
        return f'{formatData(x.month)}/{formatData(x.day)}/{formatData(int(x.hour))}:00'
        #return datetime.datetime.strptime(f'{formatData(x.month)}/{formatData(x.day)}/{formatData(int(x.hour)-1)}','%m/%d/%H')
    
    outputFile=os.path.join(os.path.join(folder,"o.dat"))
    #outputFile='data/therb/test/o.dat'
    df=pd.read_csv(outputFile,delim_whitespace=True,header=None)
    df = setColumn(df)
    #TODO:flexibleなロジックにすべき
    df = df[:8641]
    df['time']=df.apply(date_parser,axis=1)
    
    return df

def saveFile(source):
    file = source
    fileName = file.filename

    saveFileName = werkzeug.utils.secure_filename(fileName)
    file.save(saveFileName)

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
        
        #db=SQLAlchemy()
        p=Project(name=folder)

        roomId=1
        roomExist=True
        while roomExist:
            #FIXME:ファイルの命名規則を理解してここのロジックをブラッシュアップする必要
            #output_file1='out20.dat___{}.csv'.format(i)
            output_file1='out20.datS__{}.csv'.format(roomId)
            print ('output_file1',output_file1)
            try:     
                #データをparseして、データベースに保存する   
                df1=pd.read_csv(output_file1)
                #print ('df1',df1)
                #resultTable=ResultTable()
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

                #print ('roomT',roomT)
                #r=resultTable.insert(roomT,clodS,rhexS,ahexS,fs,roomH,clodL,rhexL,ahexL,fl,mrt)
                r=Results(hour=timeData,roomT=roomT,clodS=clodS,rhexS=rhexS,ahexS=ahexS,fs=fs,roomH=roomH,clodL=clodL,rhexL=rhexL,ahexL=ahexL,fl=fl,mrt=mrt)
                print ('r',r.project_id)
                p.results.append(r)
                db_session.add(r)
         
                shutil.move(output_file1,os.path.join("data",folder, output_file1))
                roomId+=1
            except:
                roomExist=False

        db_session.add(p)
        db_session.commit()

    return make_response((jsonify({
        'status':'success',
        'url':f'http://localhost:8000/{str(r.project_id)}/timeseries'
        })))

if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0',port=8080)
    #app.run(debug=True,host='0.0.0.0',port=5000)