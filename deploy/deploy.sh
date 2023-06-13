#!/bin/bash

VERSION=0.0.1
IMAGE_REPOSITORY=core.36.111.128.21.nip.io:31514/library
IMAGE_NAME=$IMAGE_REPOSITORY/learnware-backend:$VERSION
PORT=8088

set -e

docker build -f deploy/dockerfile -t $IMAGE_NAME .
docker push $IMAGE_NAME

cat deploy/deployment.yaml \
  | sed "s#{{IMAGE_NAME}}#$IMAGE_NAME#g" \
  | sed "s#{{PORT}}#$PORT#g" \
  | kubectl --insecure-skip-tls-verify apply -f -
kubectl --insecure-skip-tls-verify rollout restart statefulset learnware-backend -n learnware