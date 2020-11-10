# Temporal Resolver
API wrapper around Facebook's Duckling library - https://github.com/facebook/duckling/

# Running Instructions
```
docker build -t duckling .
docker container run --name duckling -it -p 8001:8001 duckling bash
./run.sh
```