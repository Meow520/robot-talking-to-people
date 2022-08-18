# robot-talking-to-people
人々に声掛けするロボットシステム

# Install

- NVIDIA Driver for Cuda on WSLのインストール
- コードのダウンロード
- Yolo_deepsortの重みファイルのダウンロード
- Dockerビルド
- Docker実行

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
docker build -t robot-talking-to-people .
```

# Run
```
docker run --name robot-talking-to-people --mount type=bind,source="$(pwd)"/src,target=/tmp --gpus all --rm robot-talking-to-people python sample.py
```
