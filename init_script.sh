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

# Check if the /var/billy directory exists
if [ -d "$STORAGE_DIR" ]; then
  # If the directory exists, remove all files from it
  sudo rm -r "$STORAGE_DIR"
else
  # If the directory does not exist, create it
  mkdir "$STORAGE_DIR"
fi

# Copy the folder to /var/billy
cp -r ./ "$STORAGE_DIR"

sudo chmod +x "$STORAGE_DIR"/startup.sh

# Copy the billy.service file to /etc/systemd/billy
cp "$SERVICE_PATH" "$SERVICE_DIR"

# Restart daemon service
sudo systemctl daemon-reload
# Enable the service to start automatically on boot
sudo systemctl enable "$SERVICE_NAME"
# Start the billy service
sudo systemctl start "$SERVICE_NAME"
