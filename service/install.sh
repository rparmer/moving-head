#!/bin/bash

sudo cp /home/pi/apps/moving-head/service/moving-head.service \
        /lib/systemd/system/moving-head.service
sudo systemctl daemon-reload
sudo systemctl start moving-head.service
sudo systemctl enable moving-head.service
