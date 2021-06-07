#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Library
import picamera
import datetime
import time
import locale
import sys
import os
import glob
import micropyGPS
import serial
import threading
import re
from subprocess import call
from multiprocessing import Process
import readtime_ds3231 as rt

# Const Value
GPS_DEVICE = '/dev/ttyUSB0'
GPS_BAUDRATE = 9600
TEXT_SIZE = 50

DIR_NAME = '/media/pi/DriveRecorder/Video/'
BASE_FILE_NAME = 'DriveRecorder'
FILE_EXT = '.h264'
MOVIE_INTERVAL = 300
MAX_FILE_NUM = 300

ROTATION = 0
WINDOW_W = 1280
WINDOW_H = 720
FPS = 25
EX_MODE = 'night'
AWB_MODE = 'sunlight'

# Variable
gps = micropyGPS.MicropyGPS(0, 'dd')
time_convert_flag = False

# Set RTC time to System
def setrtctimetosystem():
    t = rt.read_rtc()
    year = format(t[0],'04')
    month = format(t[1], '02')
    day = format(t[2], '02')
    weekday = t[3]
    hour = format(t[4], '02')
    minute = format(t[5], '02')
    second = format(t[6], '02')

    string = 'sudo date -s ' + '"' + str(year) + '/' + str(month) + '/' + str(day) + ' ' + str(hour) + ':' + str(minute) + ':' + str(second) + '"'

    os.system(string)

    print('Time set Successfully.')

    return

# Get year from system
def getyear():
    year = str(datetime.datetime.now().year).zfill(4)
    return year

# Get month from system
def getmonth():
    month = str(datetime.datetime.now().month).zfill(2)
    return month

# Get day from system
def getday():
    day = str(datetime.datetime.now().day).zfill(2)
    return day

# Get weekday from system
def getweekday():
    ymd = getyear() + '-' + getmonth()+ '-' + getday()
    weekday = datetime.datetime.strptime(ymd, '%Y-%m-%d').strftime('%a')
    return weekday

# Get hour from system
def gethour():
    hour = str(datetime.datetime.now().hour).zfill(2)
    return hour

# Get minute from system
def getminute():
    minute = str(datetime.datetime.now().minute).zfill(2)
    return minute

# Get second from system
def getsecond():
    second = str(datetime.datetime.now().second).zfill(2)
    return second 

# Run GPS
def rungps():
    s = serial.Serial(GPS_DEVICE, GPS_BAUDRATE, timeout=10)
    s.readline()
    while True:
        sentence = s.readline().decode('utf-8')
        if sentence[0] !='$':
            continue
        for x in sentence:
            gps.update(x)

# Get speed
def getspeed():
    if gps.clean_sentences > 20 or time_convert_flag == True:
        gps_speed = round(gps.speed[2])
    else:
        gps_speed = 'NULL'
    return gps_speed

# Get altitude
def getaltitude():
    if gps.clean_sentences > 20 or time_convert_flag == True:
        gps_altitude = round(gps.altitude, 1)
    else:
        gps_altitude = 'NULL'
    return gps_altitude

# Get latitude
def getlatitude():
    if gps.clean_sentences > 20 or time_convert_flag == True:
        gps_latitude = round(gps.latitude[0], 5)
    else:
        gps_latitude = 'NULL'
    return gps_latitude

# Get longitude
def getlongitude():
    if gps.clean_sentences > 20 or time_convert_flag == True:
        gps_longitude = round(gps.longitude[0], 5)
    else:
        gps_longitude = 'NULL'
    return gps_longitude

def getdatedisplayformat():
    date = getyear() + '/' + getmonth() + '/' + getday() + '(' + getweekday() + ')' + ' ' + gethour() + ':' + getminute() + ':' + getsecond()
    return date

def getdatefilenameformat():
    date = getyear() + getmonth() + getday() + gethour() + getminute() + getsecond()
    return date

# Get H.264 list
def getH264():
    h264list = glob.glob(DIR_NAME + '*' + FILE_EXT, recursive=True)
    print(h264list)
    return h264list

# Convert H.264 to mp4
def h264tomp4(FILE_NAME_WITHOUT_EXT):
    cmdcnv = 'MP4Box -add ' + FILE_NAME_WITHOUT_EXT + FILE_EXT + ' ' + FILE_NAME_WITHOUT_EXT + '.mp4'
    call([cmdcnv], shell = True)
    cmdrm = 'rm ' + FILE_NAME_WITHOUT_EXT + FILE_EXT
    call([cmdrm], shell = True)

# main
def main():
    setrtctimetosystem()

    gpsthread = threading.Thread(target=rungps, args=())
    gpsthread.daemon = True
    gpsthread.start()

    list = getH264()
    for n in list:
        ex = os.path.splitext(n)
        cnvprocess = Process(target=h264tomp4, args=(ex[0], ))
        cnvprocess.start()

    with picamera.PiCamera() as camera:
        camera.rotation = ROTATION
        camera.resolution = (WINDOW_W, WINDOW_H)
        camera.framerate = FPS
        camera.exposure_mode = EX_MODE
        camera.awb_mode = AWB_MODE

        camera.start_preview()
        camera.annotate_background = picamera.Color('black')
        camera.annotate_text_size = TEXT_SIZE

        while(True):
            if not os.path.isdir(DIR_NAME):
                os.mkdir(DIR_NAME)
            files = os.listdir(DIR_NAME)
            if len(files) >= MAX_FILE_NUM:
                files.sort()
                os.remove(DIR_NAME + files[0])
            dt_now_str = getdatefilenameformat()
            FILE_NAME_WITHOUT_EXT = DIR_NAME + str(dt_now_str) + '_' + BASE_FILE_NAME
            FILE_NAME = FILE_NAME_WITHOUT_EXT + FILE_EXT

            camera.start_recording(FILE_NAME)
            start = datetime.datetime.now()
            while (datetime.datetime.now() - start).seconds < MOVIE_INTERVAL:
                date = getdatedisplayformat()
                speed = str(getspeed()) + 'km/h'
                altitude = str(getaltitude()) + 'm'
                latitude = str(getlatitude()) + '"N'
                longitude = str(getlongitude()) + '"E'
                camera.annotate_text = date + '\n' + speed + ' ' + latitude + ' ' + longitude + ' ' + altitude
            camera.stop_recording()
            cnvprocess = Process(target=h264tomp4, args=(FILE_NAME_WITHOUT_EXT, ))
            cnvprocess.start()

if __name__ == '__main__':
    main()
