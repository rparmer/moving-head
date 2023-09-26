#!/bin/bash

sudo apt update && sudo apt install -y \
    python3 python3-pip ffmpeg mpg321 libsm6 \
    libxext6 libatlas-base-dev libgtk2.0-dev \
    libgtk-3-0 libilmbase-dev libopenexr-dev \
    libgstreamer1.0-dev gnustep-gui-runtime \
    pigpiod

sudo systemctl start pigpiod
sudo systemctl enable pigpiod

pip3 install -r /home/pi/apps/moving-head/requirements.txt
