#!/bin/bash
app="pydvr.docker"
docker build -t ${app} .
docker run -d -p 35000:80 \
   --name=${app} \
   -v $PWD:/app ${app}
