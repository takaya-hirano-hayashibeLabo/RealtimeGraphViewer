# RealtimeGraphViewer
CSVを与えてリアルタイムにグラフを描画するツール  
とりあえずバックエンドの部分だけ

yml形式のconfigを書き換えると, リアルタイムにグラフを書き換えることができる

## how to use

### アプリの起動
~~~bash
python app.py --config_root {描画設定のテンプレートがあるパス} --fps {描画のFPS} --saveto {描画設定を保存するパス}
#実行例) python app.py --config_root src/configs --fps 4 --saveto history/data
~~~

- `--congfig_root`  
  描画設定のテンプレートがあるパス    
  初回は引数自体を与えなくてOK  
  前回の描画設定をそのまま使いたいときはここに前回の`configs`ディレクトリを指定する  
- `--fps`  
  描画のFPS
- `--saveto`  
  描画設定を保存するパス    
  ここに`configs`ディレクトリが作成され, その中に`--config_root`で指定したパスの内容がコピーされる  
  実行時はこの`configs`ディレクトリの中身を書き換えることで, リアルタイムにグラフを描画することができる
