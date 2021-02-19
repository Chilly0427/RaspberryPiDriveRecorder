# -*- coding: UTF-8 -*-
import micropyGPS
import serial
import threading
import time
import datetime

gps = micropyGPS.MicropyGPS(0, 'dd')

def utc_to_jst(timestamp_utc):
    datetime_utc = datetime.datetime.strptime(timestamp_utc + "+0000", "%Y-%m-%d %H:%M:%S.%f%z")
    datetime_jst = datetime_utc.astimezone(datetime.timezone(datetime.timedelta(hours=+9)))
    timestamp_jst = datetime.datetime.strftime(datetime_jst, '%Y-%m-%d %H:%M:%S.%f')
    return timestamp_jst

def rungps():
    s = serial.Serial('/dev/ttyUSB0', 9600, timeout=10)
    s.readline()
    while True:
        sentence = s.readline().decode('utf-8')
        if sentence[0] !='$':
            continue
        for x in sentence:
            gps.update(x)

gpsthread = threading.Thread(target=rungps, args=())
gpsthread.daemon = True
gpsthread.start()

while True:
    if gps.clean_sentences > 20:
        h = gps.timestamp[0] if gps.timestamp[0] < 24 else gps.timestamp[0] - 24
       # print('%4D' % (gps.date_string.year, 's_mdy', '20'))
        utc_now = "20" + str(gps.date[2]) + "-" + str(gps.date[1]) + "-" + str(gps.date[0]) + " " + str(h) + ":" + str(gps.timestamp[1]) + ":" + str(gps.timestamp[2])
        print(utc_now)
        #jst = utc_to_jst(utc_now)
        #print(jst)
        print("[JST] " + utc_to_jst(utc_now))

        print(gps.speed[2])
        print(gps.date_string('s_mdy', '20'))
        print('%2d/%2d/%2d' % (gps.date[0], gps.date[1], gps.date[2]))
        print('%2d:%02d:%04.1f' % (h, gps.timestamp[1], gps.timestamp[2]))
        print('緯度経度: %2.8f, %2.8f' % (gps.latitude[0], gps.longitude[0]))
        print('海抜: %f' % gps.altitude)
        print(gps.satellites_used)
        print('衛星番号: (仰角, 方位角, SN比)')
        for k, v in gps.satellite_data.items():
            print('%d: %s' % (k, v))
        print('')
    time.sleep(1.0)

