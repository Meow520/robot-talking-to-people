# mongodb
How to run mongodb.

# Docker build
```
docker pull mongo
```
# Create network
```
docker network create -d bridge mongonet
```
# Run
```
docker run --name mongo --net mongonet --rm mongo
```

# Tips
DBの中身を確認するためには、別ターミナルでmongodbのコンテナを操作可能な状態で起動し、もともと立ち上げてあったDBに接続すればよい。
```
docker run --net mongonet --rm -it mongo /bin/bash
mongo --host mongo
db.[collection].find()
```



