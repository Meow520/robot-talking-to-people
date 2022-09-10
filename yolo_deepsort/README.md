# robot-talking-to-people
人々に声掛けするロボットシステム

# Install

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

# Run
PC上でコンテナを起動してから、Sota上でUDPの送信を開始する。

## yolo_deepsortコンテナの起動
GPUを使わない場合は`--gpus all`と`--gpu`を削除する。
```
cd yolo_deepsort
docker run --rm -it --net mongonet --mount type=bind,source="$(pwd)"/src,target=/tmp -p 5000:5000/udp --gpus all yolo_deepsort python app.py --gpu
```


## Sotaから映像を送信
Sotaにログイン後
```
cd ffmpeg
./ffmpeg -f v4l2 -s 320x240 -thread_queue_size 8192 -i /dev/video0 -c:v libx264 -preset ultrafast -tune zerolatency -f h264 udp://<host's ip>:5000?pkt_size=1024
```

### Windows PCから映像を送信する場合
Windows terminalで
```
ffmpeg -re -f dshow -i video="Surface Camera Front" -s 320x240 -r 30 -c:v libx264 -preset ultrafast -tune zerolatency -an -f h264 udp://localhost:5000?pkt_size=1024
```
※Surface～の部分に入れる文字列は`ffmpeg -list_devices true -f dshow -i dummy`で調べられる。

