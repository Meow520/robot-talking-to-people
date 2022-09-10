# state_manager
This is a program for managing robot's behavior.

# Docker build
```
cd behavior
docker build -t behavior_manager .
```


# Run
```
cd behavior
docker run --rm -it --net mongonet --mount type=bind,source="$(pwd)"/src,target=/tmp behavior_manager python app.py
```