# mongodb
How to run mongodb.

# Docker build
```
docker pull mongo
```
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

# Tips
DBの中身を確認するためには、別ターミナルでmongodbのコンテナを操作可能な状態で起動し、もともと立ち上げてあったDBに接続すればよい。
```
docker run --net mongonet --rm -it mongo /bin/bash
mongo --host mongo
db.[collection].find()
```



