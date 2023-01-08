#!/bin/bash

# Set the path to the dir used by the service
STORAGE_DIR="/var/billy"
# Set the paths to the /etc/systemd/system/ directory and the billy.service file
SERVICE_DIR="/etc/systemd/system/"
SERVICE_PATH="./billy.service"
# Extract the service name from the full path to the billy.service file
SERVICE_NAME=$(basename "$SERVICE_PATH")

# Stop the billy service if it is running
systemctl stop "$SERVICE_NAME"

# Remove files used by Billy service
sudo rm -r "$STORAGE_DIR"
sudo rm -r /etc/systemd/system/"$SERVICE_NAME"

# Restart deamon service
sudo systemctl deamon-reload