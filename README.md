<<<<<<< HEAD
# 概要
人物認識器（yolo_deepsort）と音声認識器（speechrec）の出力をデータベース（MongoDB）に保持し、その結果に基づいて状態を変更し、その状態に応じた行動を実行するロボットシステムのサンプル。

# 事前準備
1. コードのクローン
1. Dockerネットワークの作成
1. mongodb用のボリュームの作成
1. mongodbイメージの作成
1. yolo_deepsortイメージの作成
1. speechrecイメージの作成
1. state_managerイメージの作成
1. behavior_managerイメージの作成

## コードのクローン
```
https://github.com/social-robotics-lab/robot-talking-to-people.git
```
=======
# robot-talking-to-people

各種認識結果を保持するデータベース（mongodb）と人物認識器（yolo_deepsort）と音声認識器（speechrec）をDockerを使って連携するシステムのサンプル。


# 起動順序
1. Dockerネットワークの作成
1. mongodb用のボリュームの作成
1. mongodbコンテナの起動
1. yolo_deepsortコンテナの起動
1. speechrecコンテナの起動
1. Sotaから映像を送信
1. Sotaから音声を送信
>>>>>>> 50d2a7d6c5fe1caa1a3f366a0af8944c96a99c06

## Dockerネットワークの作成
```
docker network create -d bridge mongonet
```

## mongodb用のボリュームの作成
```
docker volume create --name mongovolume
```

<<<<<<< HEAD
## mongodbイメージの作成
```
docker pull mongo
```

## yolo_deepsortイメージの作成
- NVIDIA Driver for Cuda on WSLのインストール
- コードのダウンロード
- Yolo_deepsortの重みファイルのダウンロード
- Dockerビルド

### NVIDIA Driver for Cuda on WSLのインストール
https://developer.nvidia.com/cuda/wsl/download

### Yolo_deepsortの重みファイルのダウンロード
```
cd yolo_deepsort
wget -P src/weights https://pjreddie.com/media/files/yolov3.weights
wget -P src/weights https://pjreddie.com/media/files/darknet53.conv.74
```
Download [ckpt.t7](https://drive.google.com/drive/folders/1xhG0kRH1EX5B9_Iz8gQJb7UNnn_riXi6)
and put it to src/weights.

### Dockerビルド
```
cd yolo_deepsort
docker build -t yolo_deepsort .
```

## speechrecイメージの作成
- Microsoft Azureでの音声認識サービスの登録
- コードのダウンロード
- Dockerビルド

### Microsoft Azureでの音声認識サービスの登録
- Azureサブスクリプションの無料アカウントを作成する。
- ポータルからCognitive Servicesを選択し、音声サービスを作成
- リソースグループは適当？、リージョンはJapan West、価格レベルはFree
- 作成できたら、ブックマークしておく（あとでAPIキーをコピーするとき便利なため）

「Azure 音声認識サービス　使い方」などで検索し、やり方を調べる。

### Dockerビルド
```
cd speechrec
docker build -t speechrec .
```

## state_managerイメージの作成
```
cd state
docker build -t state_manager .
```

## behavior_managerイメージの作成
```
cd behavior
docker build -t behavior_manager .
```


# 起動順序
1. mongodbコンテナの起動
1. yolo_deepsortコンテナの起動
1. speechrecコンテナの起動
1. state_managerコンテナの起動
1. behavior_managerコンテナの起動
1. Sotaから映像を送信
1. Sotaから音声を送信


=======
>>>>>>> 50d2a7d6c5fe1caa1a3f366a0af8944c96a99c06
## mongodbコンテナの起動
```
docker run --rm -it --net mongonet --mount type=volume,src=mongovolume,dst=/data/db -p 27017:27017 --name mongo mongo
```

## yolo_deepsortコンテナの起動
<<<<<<< HEAD
GPUを使わない場合は`--gpus all`と`--gpu`を削除する。
=======
>>>>>>> 50d2a7d6c5fe1caa1a3f366a0af8944c96a99c06
```
cd yolo_deepsort
docker run --rm -it --net mongonet --mount type=bind,source="$(pwd)"/src,target=/tmp -p 5000:5000/udp --gpus all yolo_deepsort python app.py --gpu
```

## speechrecコンテナの起動
```
cd speechrec
docker run --rm -it --net mongonet --mount type=bind,source="$(pwd)"/src,target=/tmp -p 5001:5001/udp speechrec python app.py --api_key <api_key>
```

## state_managerコンテナの起動
```
cd state
<<<<<<< HEAD
docker run --rm -it --net mongonet --mount type=bind,source="$(pwd)"/src,target=/tmp state_manager python app.py
```

## behavior_managerコンテナの起動
```
cd behavior
docker run --rm -it --net mongonet --mount type=bind,source="$(pwd)"/src,target=/tmp behavior_manager python app.py
=======
docker run --rm -it --net mongonet --mount type=bind,source="$(pwd)"/src,target=/tmp state_manager python app.py [--db_host <db_host> --db_port <db_port>]
>>>>>>> 50d2a7d6c5fe1caa1a3f366a0af8944c96a99c06
```


## Sotaから映像を送信
Sotaにログイン後
```
cd ffmpeg
./ffmpeg -f v4l2 -s 320x240 -thread_queue_size 8192 -i /dev/video0 -c:v libx264 -preset ultrafast -tune zerolatency -f h264 udp://<host's ip>:5000?pkt_size=1024
```

<<<<<<< HEAD
### Windows PCから映像を送信する場合
Windows terminalで
```
ffmpeg -re -f dshow -i video="Surface Camera Front" -s 320x240 -r 30 -c:v libx264 -preset ultrafast -tune zerolatency -an -f h264 udp://localhost:5000?pkt_size=1024
```
※Surface～の部分に入れる文字列は`ffmpeg -list_devices true -f dshow -i dummy`で調べられる。

=======
>>>>>>> 50d2a7d6c5fe1caa1a3f366a0af8944c96a99c06
## Sotaから音声を送信
Sotaにログイン後
```
cd ffmpeg
./ffmpeg -channels 1 -f alsa -thread_queue_size 8192 -i hw:2 -preset ultrafast -tune zerolatency -ac 1 -c:a pcm_s16le -ar 16000 -f s16le udp://<host's ip>:5001?pkt_size=1024
```
<<<<<<< HEAD

### Windows PCから音声を送信する場合
Windows terminalで
```
ffmpeg -f dshow -ac 1 -thread_queue_size 8192 -i audio="マイク配列 (Realtek High Definition Audio(SST))" -f s16le -c:a pcm_s16le -ar 16000 udp://127.0.0.1:5001?pkt_size=1024
```
※マイク配列～の部分に入れる文字列は`ffmpeg -list_devices true -f dshow -i dummy`で調べられる。


# データベースの内容の確認
MongoDB compassを利用する。公式サイト: https://www.mongodb.com/ja-jp/products/compass

=======
>>>>>>> 50d2a7d6c5fe1caa1a3f366a0af8944c96a99c06
