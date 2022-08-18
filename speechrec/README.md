# speechrec
Program of Microsoft Azure Speech to Text.

# Docker build
```
docker build -t speechrec .
```

# Run
PC上でコンテナを起動してから、Sota上でUDPの送信を開始する。

## PC
```
docker run --name speechrec --mount type=bind,source="$(pwd)"/src,target=/tmp --net amqnet --rm speechrec python main.py --api_key <api_key> [--amq_host <amq_host> --amq_port <amq_port>]
```

## Sota
Run FFmpeg for sending sound from the mic.
```
cd ffmpeg
./ffmpeg -channels 1 -f alsa -thread_queue_size 8192 -i hw:2 -preset ultrafast -tune zerolatency -ac 1 -c:a pcm_s16le -ar 16000 -f s16le udp://[host's ip]:5001?pkt_size=1024
```


# 備考
ffmpeg-pythonを用いて、受信したudpの音声パケットを標準出力にパイプで流し、そのパイプに入ってきたデータをAzureの音声認識APIに流している。
そのため、printを書いても標準出力に表示されない（プログラムの終了後にまとめて表示される）