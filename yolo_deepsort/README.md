# robot-talking-to-people
人々に声掛けするロボットシステム

# Install

- NVIDIA Driver for Cuda on WSLのインストール
- コードのダウンロード
- Yolo_deepsortの重みファイルのダウンロード
- Dockerビルド
- コンテナ起動＆映像送信

## NVIDIA Driver for Cuda on WSL
https://developer.nvidia.com/cuda/wsl/download

## Download code
```
git clone https://github.com/social-robotics-lab/yolo_deepsort.git
```

## Download weights
```
cd yolo_deepsort
wget -P src/weights https://pjreddie.com/media/files/yolov3.weights
wget -P src/weights https://pjreddie.com/media/files/darknet53.conv.74
```
Download [ckpt.t7](https://drive.google.com/drive/folders/1xhG0kRH1EX5B9_Iz8gQJb7UNnn_riXi6)
and put it to src/weights.

## Docker build
```
docker build -t yolo_deepsort .
```

# Run
PC上でコンテナを起動してから、Sota上でUDPの送信を開始する。

## PC
```
cd yolo_deepsort
docker run --rm -it --name yolo_deepsort --mount type=bind,source="$(pwd)"/src,target=/tmp --gpus all yolo_deepsort python app.py --gpu
```

## Sota
Run FFmpeg for sending video from the camera.
```
cd ffmpeg
./ffmpeg -f v4l2 -s 320x240 -thread_queue_size 8192 -i /dev/video0 -c:v libx264 -preset ultrafast -tune zerolatency -f h264 udp://<host's ip>:5000?pkt_size=1024
```

Sotaを使わずWindows PCのFFmpegを使う場合
```
ffmpeg -re -f dshow -i video="Surface Camera Front" -s 320x240 -r 30 -c:v libx264 -preset ultrafast -tune zerolatency -an -f h264 udp://localhost:5000?pkt_size=1024
```
※Surface～の部分に入れる文字列は`ffmpeg -list_devices true -f dshow -i dummy`で調べられる。