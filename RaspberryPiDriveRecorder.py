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

# Variable
gps = micropyGPS.MicropyGPS(0, 'dd')
time_convert_flag = False

# Convert GPS UTC to JST
def utctojst(timestamp_utc):
    try:
        datetime_utc = datetime.datetime.strptime(timestamp_utc + '+0000', '%Y-%m-%d %H:%M:%S.%f%z')
        datetime_jst = datetime_utc.astimezone(datetime.timezone(datetime.timedelta(hours=+9)))
        timestamp_jst = datetime.datetime.strftime(datetime_jst, '%Y-%m-%d %H:%M:%S.%f')
        time_convert_flag = True
    except ValueError:
        print('Time Convert Error(UTC to JST)')
        time_convert_flag = False
    return timestamp_jst

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

# Get time
def gettime():
    if gps.clean_sentences > 20:
        h = gps.timestamp[0] if gps.timestamp[0] < 24 else gps.timestamp[0] - 24
        utc_now = '20' + str(gps.date[2]) + '-' + str(gps.date[1]) + '-' + str(gps.date[0]) + ' ' + str(h) + ':' + str(gps.timestamp[1]) + ':' + str(gps.timestamp[2])
        jst = utctojst(utc_now)
    else:
        jst = datetime.datetime.now()
        jst = jst.strftime('%Y-%m-%d %H:%M:%S')
    return jst 

# Get year
def gettime_year(time):
    if len(time) > 5 or time_convert_flag == True: 
        year = re.findall('[0-9]+', time)
        year = year[0].zfill(4)
    else:
        year = str(datetime.datetime.now().year).zfill(4)
    return year

# Get month
def gettime_month(time):
    if len(time) > 5 or time_convert_flag == True: 
        month = re.findall('[0-9]+', time)
        month = month[1].zfill(2)
    else:
        month= str(datetime.datetime.now().month).zfill(2)
    return month

# Get day
def gettime_day(time):
    if len(time) > 5 or time_convert_flag == True: 
        day = re.findall('[0-9]+', time)
        day = day[2].zfill(2)
    else:
        day= str(datetime.datetime.now().day).zfill(2)
    return day

# Get hour
def gettime_hour(time):
    if len(time) > 5 or time_convert_flag == True: 
        hour = re.findall('[0-9]+', time)
        hour = hour[3].zfill(2)
    else:
        hour = str(datetime.datetime.now().hour).zfill(2)
    return hour

# Get minute
def gettime_minute(time):
    if len(time) > 5 or time_convert_flag == True: 
        minute = re.findall('[0-9]+', time)
        minute = minute[4].zfill(2)
    else:
        minute = str(datetime.datetime.now().minute).zfill(2)
    return minute

# Get second
def gettime_second(time):
    if len(time) > 5 or time_convert_flag == True: 
        second = re.findall('[0-9]+', time)
        second = second[5].zfill(2)
    else:
        second = str(datetime.datetime.now().second).zfill(2)
    return second

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
        gps_latitude = gps.latitude[0]
    else:
        gps_latitude = 'NULL'
    return gps_latitude

# Get longitude
def getlongitude():
    if gps.clean_sentences > 20 or time_convert_flag == True:
        gps_longitude = gps.longitude[0]
    else:
        gps_longitude = 'NULL'
    return gps_longitude

# Get date display format
def getdatedisplayformat():
    year = gettime_year(str(gettime()))
    month = gettime_month(str(gettime()))
    day = gettime_day(str(gettime()))
    ymd = year + '-' + month + '-' + day
    weekday = datetime.datetime.strptime(ymd, '%Y-%m-%d').strftime('%a')
    hour = gettime_hour(str(gettime()))
    minute = gettime_minute(str(gettime()))
    second = gettime_second(str(gettime()))
    if time_convert_flag == True:
        date =  str(year) + '/' + str(month) + '/' + str(day) + '(' + str(weekday) + ')' + ' ' + str(hour) + ':' + str(minute) + ':' + str(second)
    else:
        date =  'NO_GPS ' + str(year) + '/' + str(month) + '/' + str(day) + '(' + str(weekday) + ')' + ' ' + str(hour) + ':' + str(minute) + ':' + str(second)
    return date

# Get date file name format
def getdatefilenameformat():
    year = gettime_year(str(gettime()))
    month = gettime_month(str(gettime()))
    day = gettime_day(str(gettime()))
    hour = gettime_hour(str(gettime()))
    minute = gettime_minute(str(gettime()))
    second = gettime_second(str(gettime()))
    if time_convert_flag == True:
        date =  str(year) + str(month) + str(day) + str(hour) + str(minute) + str(second)
    else:
        date =  'NO_GPS_' + str(year) + str(month) + str(day) + str(hour) + str(minute) + str(second)
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
        camera.start_preview()
        camera.annotate_background = picamera.Color('black')
        camera.annotate_text_size = TEXT_SIZE
        date = getdatedisplayformat()
        speed = str(getspeed()) + ' km/h'
        camera.annotate_text = date + ' ' + speed

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
                speed = str(getspeed()) + ' km/h'
                camera.annotate_text = date + ' ' + speed
            camera.stop_recording()
            cnvprocess = Process(target=h264tomp4, args=(FILE_NAME_WITHOUT_EXT, ))
            cnvprocess.start()

if __name__ == '__main__':
    main()
