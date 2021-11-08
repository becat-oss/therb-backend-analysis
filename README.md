# therb-backend. 
THERB-backendはTHERB(HASP)のシミュレーション結果を分析、管理するためのwebアプリを構成するAPIサーバーです。
[THERB-UI](https://github.com/becat-oss/therb-UI)をフロントエンドとして、THERB-webを構成します。  
THERB-webには以下のような機能が実装される予定です。

THERB-GHからアップロードされた入力データを元にシミュレーションを回し、結果を抽出、データベースに保存.
データベースに保存されているデータをグラフ表示してくれるUI
データを外部と連携するためのAPIインターフェース
