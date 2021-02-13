#!/usr/bin/python
# -*- coding: utf-8 -*-

# Library
import picamera
import datetime
import time
import sys
import os

from subprocess import call

# Const Value
DIR_NAME = '/home/pi/RaspberryPiDriveRecorder/Video/'
BASE_FILE_NAME = 'DriveRecorder'
FILE_EXT = '.h264'
MOVIE_INTERVAL = 10
MAX_FILE_NUM = 30

# Value

def h264tomp4(FILE_NAME):
    cmdcnv = "MP4Box -add " + FILE_NAME + " " + FILE_NAME_WITHOUT_EXT + ".mp4"
    call([cmdcnv], shell = True)

    cmdrm = "rm " + FILE_NAME
    call([cmdrm], shell = True)


# main
with picamera.PiCamera() as camera:
    camera.rotation = 270
    camera.resolution = (1280, 720)
    camera.framerate = 24
    camera.start_preview()
    camera.annotate_background = picamera.Color('black')
    camera.annotate_text = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

    while(True):
        if not os.path.isdir(DIR_NAME):
            os.mkdir(DIR_NAME)
        files = os.listdir(DIR_NAME)
        if len(files) >= MAX_FILE_NUM:
            files.sort()
            os.remove(DIR_NAME + files[0])
        dt_now = datetime.datetime.now()
        dt_now_str = dt_now.strftime("%Y%m%d%H%M%S")
        FILE_NAME_WITHOUT_EXT = DIR_NAME + str(dt_now_str) + "_" + BASE_FILE_NAME
        FILE_NAME = FILE_NAME_WITHOUT_EXT + FILE_EXT

        camera.start_recording(FILE_NAME)
        start = datetime.datetime.now()
        while (datetime.datetime.now() - start).seconds < MOVIE_INTERVAL:
            camera.annotate_text = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            camera.wait_recording(0.2)
        camera.stop_recording()
        h264tomp4(FILE_NAME)


