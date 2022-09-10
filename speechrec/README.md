# speechrec
Program of Microsoft Azure Speech to Text.

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

# Run
PC上でコンテナを起動してから、Sota上でUDPの送信を開始する。

## speechrecコンテナの起動
```
cd speechrec
docker run --rm -it --net mongonet --mount type=bind,source="$(pwd)"/src,target=/tmp -p 5001:5001/udp speechrec python app.py --api_key <api_key>
```

## Sotaから音声を送信
Sotaにログイン後
```
cd ffmpeg
./ffmpeg -channels 1 -f alsa -thread_queue_size 8192 -i hw:2 -preset ultrafast -tune zerolatency -ac 1 -c:a pcm_s16le -ar 16000 -f s16le udp://<host's ip>:5001?pkt_size=1024
```

### Windows PCから音声を送信する場合
Windows terminalで
```
ffmpeg -f dshow -ac 1 -thread_queue_size 8192 -i audio="マイク配列 (Realtek High Definition Audio(SST))" -f s16le -c:a pcm_s16le -ar 16000 udp://127.0.0.1:5001?pkt_size=1024
```
※マイク配列～の部分に入れる文字列は`ffmpeg -list_devices true -f dshow -i dummy`で調べられる。
