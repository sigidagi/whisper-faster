## Docker 

```
docker build . -t faster-whisper
docker buildx build --platform linux/arm64 . -t faster-whisper-arm64
docker run -dit faster-whisper -p 8006:8006 --name whisper-ai
docker exec -it whisper-ai bash
```

```
docker save -o whisper-arm64.tar faster-whisper-arm64:latest
docker load -i whisper-arm64.tar
```

## RUN

`docker run -dit --name whisper -p 8006:8006 faster-whisper-arm64:latest`

Bash in to the docker
`docker exec -it whisper bash`
`ps aux | grep python`

## TEST

`curl -X POST -F "file=@jfk.wav" http://rock5b.local:8005/upload`
