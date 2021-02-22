#!/bin/bash
/usr/bin/sh /home/pi/RaspberryPiDriveRecorder/setdatefromgps.sh
systemctl stop gpsd
/usr/bin/python3 /home/pi/RaspberryPiDriveRecorder/RaspberryPiDriveRecorder.py
