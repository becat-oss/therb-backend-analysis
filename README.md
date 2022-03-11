# therb-backend. 
THERB-backendはTHERB(HASP)のシミュレーション結果を分析、管理するためのwebアプリを構成するAPIサーバーです。
[THERB-UI](https://github.com/becat-oss/therb-UI)をフロントエンドとして、THERB-webを構成します。  
THERB-webには以下のような機能が実装される予定です。

1. THERB-GHからアップロードされた入力データを元にシミュレーションを回し、結果を抽出、データベースに保存.  
2. データベースに保存されているデータをグラフ表示してくれるUI  
3. データを外部と連携するためのAPIインターフェース  

## 機能説明  
3. データを外部と連携するためのAPIインターフェース  

## 環境設定(Windows PCの場合）    
1. command promptを開き、ディレクトリ移動  
2. pipenv shellを叩いて、仮想環境を構築  
3. 以下のコマンドを叩く  
```
set FLASK_APP=run
flask run
```

## 使い方  
### データ処理側  
1. NewHaspデータをuploadする(以下のようにfileとnameをbodyパラメータの構成要素とする)    
http://localhost:5000/run  
![image](https://user-images.githubusercontent.com/90674244/157411568-a7c7edf7-4700-4c46-9512-a66f6f07981c.png)  

2. uploadされたデータのproject名とidを取得する  
http://localhost:5000/projects 

3. uploadされたデータのtimeseriesデータを取得する  
http://localhost:5000/results/{projectId}  

### モデリング側  

