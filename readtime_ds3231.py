#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Read time from DS3231

import smbus

bus = smbus.SMBus(11)
address = 0x68
w = ["Sun.", "Mon.", "Tue.", "Wed.", "Thu.", "Fri.", "Sat."]

def read_year():
    year2 = bus.read_byte_data(address, 6)
    year1 = bus.read_byte_data(address, 7)
    year = str(year1//16*10+year1%16) + str(year2//16*10+year2%16)
        
    return int(year)

def read_month():
    month = bus.read_byte_data(address, 5)
    month = month//16*10+month%16
        
    return month

def read_day():
    day = bus.read_byte_data(address, 4)
    day = day//16*10+day%16
        
    return day

def read_day_of_the_week():
    dow = bus.read_byte_data(address, 3)
    dow = dow//16*10+dow%16
        
    return w[dow]

def read_hour():
    hour = bus.read_byte_data(address, 2)
    hour = hour//16*10+hour%16
        
    return hour

def read_minute():
    min = bus.read_byte_data(address, 1)
    min = min//16*10+min%16
        
    return min

def read_second():
    sec = bus.read_byte_data(address, 0)
    sec = sec//16*10+sec%16
        
    return sec 

def read_rtc():
    year = read_year()
    month = read_month()
    day = read_day()
    dow = read_day_of_the_week()
    hour = read_hour()
    min = read_minute()
    sec = read_second()

    return [year, month, day, dow, hour, min, sec]
