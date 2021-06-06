#! /usr/bin/python3
# Read time from DS3231

import smbus
import time

bus = smbus.SMBus(11)

address = 0x68

w = ["Sun.", "Mon.", "Tue.", "Wed.", "Thu.", "Fri.", "Sat."]

def SetTime(address):
    bus.write_byte_data(address, 0x00, 0x00) # set seconds and start clock
    bus.write_byte_data(address, 0x01, 0x00) # set minutes
    bus.write_byte_data(address, 0x02, 0x00) # set hours in 24 hour mode
    bus.write_byte_data(address, 0x03, 0x00) # set day of week[0:Sun. - 7:Sat.]
    bus.write_byte_data(address, 0x04, 0x01) # set day
    bus.write_byte_data(address, 0x05, 0x01) # set month
    bus.write_byte_data(address, 0x06, 0x21) # set year - last 2 digits

SetTime(address)
print("Time set successfully")
