# state_manager
This is a program for managing robot's state.

# Docker build
```
cd state
docker build -t state_manager .
```


# Run
```
cd state
docker run --rm -it --net mongonet --mount type=bind,source="$(pwd)"/src,target=/tmp state_manager python app.py
```