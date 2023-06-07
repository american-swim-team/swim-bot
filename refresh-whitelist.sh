#!/bin/bash

CONTAINER_NAME="assetto-hub"
PACKAGE_NAME="procps"

if podman exec -it "$CONTAINER_NAME" which kill >/dev/null 2>&1; then
  echo "kill command found within container"
else
  echo "kill command not found within container - installing $PACKAGE_NAME package"
  podman exec -it "$CONTAINER_NAME" apt-get update && podman exec -it "$CONTAINER_NAME" apt-get install -y "$PACKAGE_NAME"
fi

echo "Sending USR1 signal to PID 1 within container"
podman exec -it "$CONTAINER_NAME" kill -USR1 1
