#! /usr/bin/python3
# Read time from DS3231

import smbus
import time

bus = smbus.SMBus(11)

address = 0x68

w = ["Sun.", "Mon.", "Tue.", "Wed.", "Thu.", "Fri.", "Sat."]

def ReadTime(address):
    sec = bus.read_byte_data(0x68, 0)
    min = bus.read_byte_data(0x68, 1)
    hour = bus.read_byte_data(0x68, 2)
    dow = bus.read_byte_data(0x68, 3)
    day = bus.read_byte_data(0x68, 4)
    month = bus.read_byte_data(0x68, 5)
    year2 = bus.read_byte_data(0x68, 6)
    year1 = bus.read_byte_data(0x68, 7)

    return [year1, year2, month, day, dow, hour, min, sec]

while True:
    t = ReadTime(address)

    year1l = t[0]//16*10+t[0]%16
    year2l = t[1]//16*10+t[1]%16
    monthl = t[2]//16*10+t[2]%16
    dayl = t[3]//16*10+t[3]%16
    datel = t[4]//16*10+t[4]%16
    hourl = t[5]//16*10+t[5]%16
    minl = t[6]//16*10+t[6]%16
    secl = t[7]//16*10+t[7]%16

    print("{:0=2}{:0=2}-{:0=2}-{:0=2} {:0=2}:{:0=2}:{:0=2}".format(year1l, year2l, monthl, dayl, hourl, minl, secl))
