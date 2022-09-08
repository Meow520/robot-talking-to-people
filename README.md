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

## Dockerネットワークの作成
```
docker network create -d bridge mongonet
```

## mongodb用のボリュームの作成
```
docker volume create --name mongovolume
```

## mongodbコンテナの起動
```
docker run --rm -it --net mongonet --mount type=volume,src=mongovolume,dst=/data/db -p 27017:27017 --name mongo mongo
```

## yolo_deepsortコンテナの起動
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
docker run --rm -it --net mongonet --mount type=bind,source="$(pwd)"/src,target=/tmp state_manager python app.py [--db_host <db_host> --db_port <db_port>]
```


## Sotaから映像を送信
Sotaにログイン後
```
cd ffmpeg
./ffmpeg -f v4l2 -s 320x240 -thread_queue_size 8192 -i /dev/video0 -c:v libx264 -preset ultrafast -tune zerolatency -f h264 udp://<host's ip>:5000?pkt_size=1024
```

## Sotaから音声を送信
Sotaにログイン後
```
cd ffmpeg
./ffmpeg -channels 1 -f alsa -thread_queue_size 8192 -i hw:2 -preset ultrafast -tune zerolatency -ac 1 -c:a pcm_s16le -ar 16000 -f s16le udp://<host's ip>:5001?pkt_size=1024
```
