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
cd speechrec
docker run --rm -it --name speechrec -p 5001:5001/udp --mount type=bind,source="$(pwd)"/src,target=/tmp speechrec python app.py --api_key <api_key>
```

## Sota
Run FFmpeg for sending sound from the mic.
```
cd ffmpeg
./ffmpeg -channels 1 -f alsa -thread_queue_size 8192 -i hw:2 -preset ultrafast -tune zerolatency -ac 1 -c:a pcm_s16le -ar 16000 -f s16le udp://[host's ip]:5001?pkt_size=1024
```

Sotaを使わずWindows PCのFFmpegを使う場合
```
ffmpeg -f dshow -ac 1 -thread_queue_size 8192 -i audio="マイク配列 (Realtek High Definition Audio(SST))" -f s16le -c:a pcm_s16le -ar 16000 udp://127.0.0.1:5001?pkt_size=1024
```
※マイク配列～の部分に入れる文字列は`ffmpeg -list_devices true -f dshow -i dummy`で調べられる。

