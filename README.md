# RaspberryPiDriveRecorder
## Environment
- [Raspberry Pi 3B+](https://www.amazon.co.jp/gp/product/B087WKPWNW/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1)
- [Camera module](https://www.amazon.co.jp/gp/product/B07W5GBFF8/ref=ppx_od_dt_b_asin_title_s00?ie=UTF8&psc=1)
- [microSD Card](https://www.amazon.co.jp/gp/product/B08CXF3VH9/ref=ppx_yo_dt_b_asin_title_o09_s00?ie=UTF8&psc=1)
- [USB Flash Memory](https://www.amazon.co.jp/gp/product/B07855LJ99/ref=ppx_yo_dt_b_asin_title_o08_s00?ie=UTF8&psc=1)
- [micro USB Cable 2.4A](https://www.amazon.co.jp/gp/product/B07G6X2LJ8/ref=ppx_yo_dt_b_asin_title_o05_s00?ie=UTF8&psc=1)
- [HDMI monitor](https://www.amazon.co.jp/gp/product/B01N5HW3BP/ref=ppx_yo_dt_b_asin_title_o06_s00?ie=UTF8&psc=1)
- [USB RTC](https://www.kickstarter.com/projects/amritsingh/usb-rtc)

## Setup
### Clone
```
cd /home/pi/
git clone https://github.com/Chilly0427/RaspberryPiDriveRecorder.git 
ls
RaspberryPiDriveRecorder
```

### USB mount setting
```
sudo apt install ntfs-3g
blkid
/dev/sda1: LABEL="DriveRecorder" UUID="50E98A443FEE6101" TYPE="ntfs" PTTYPE="dos" PARTUUID="b5976904-01"
sudo vi /etc/fstab
UUID=50E98A443FEE6101 /media/pi/DriveRecorder ntfs-3g defaults 0 0
```

### Install video converter
```
sudo apt install gpac
```

### GPSD Install and Settings(T.B.D.)
```
sudo apt install gpsd gpsd-clients
systemctl stop gpsd.socket
systemctl disable gpsd.socket

vi /etc/default/gpsd
# Default settings for the gpsd init script and the hotplug wrapper.

# Start the gpsd daemon automatically at boot time
START_DAEMON="true"

# Use USB hotplugging to add new USB devices automatically to the daemon
USBAUTO="true"

# Devices gpsd should collect to at boot time.
# They need to be read/writeable, either by user gpsd or the group dialout.
DEVICES="/dev/ttyUSB0 -F /var/run/gpsd.socket"

# Other options you want to pass to gpsd
GPSD_OPTIONS=""

systemctl enable gpsd.service
```

### Import GPS module
```
https://github.com/inmcm/micropyGPS
import micropyGPS
```

### USB RTC
#### Using
https://www.kickstarter.com/projects/amritsingh/usb-rtc
https://shop.sb-components.co.uk/products/usb-rtc-for-raspberry-pi-1?_pos=1&_sid=3de43aaa2&_ss=r

#### Official
MCP2221A
https://www.microchip.com/wwwproducts/en/MCP2221A

#### How to install i2c driver for MCP2221A
##### Reference
https://gist.github.com/mamemomonga/fdb7a2330b0a3c5d2ba50528c5946ef4
```
sudo apt install raspberrypi-kernel-headers
wget https://ww1.microchip.com/downloads/en/DeviceDoc/mcp2221_0_1.tar.gz
tar zxvf mcp2221_0_1.tar.gz
cd mcp2221_0_1
sudo make modules
sudo make install
```

##### Enable module
```
sudo ./driver_load.sh
```

##### Connect check
```
sudo apt install i2c-tools
sudo i2cdetect -l
i2c-1	i2c       	bcm2835 (i2c@7e804000)          	I2C adapter
i2c-11	i2c       	i2c-mcp2221 at bus 001 device 006	I2C adapter
sudo i2cdetect -y 11
pi@raspberrypi:~/RaspberryPiDriveRecorder $ sudo i2cdetect -y 11
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- 68 -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- --                  
```

##### Set Time
```
vi settime_sample_ds3231.py
modify time:
ex)2021/12/31(Fri.) 23:59:59
def SetTime(address):
    bus.write_byte_data(address, 0x00, 0x59) # set seconds and start clock
    bus.write_byte_data(address, 0x01, 0x59) # set minutes
    bus.write_byte_data(address, 0x02, 0x23) # set hours in 24 hour mode
    bus.write_byte_data(address, 0x03, 0x06) # set day of week[0:Sun. - 7:Sat.]
    bus.write_byte_data(address, 0x04, 0x31) # set day
    bus.write_byte_data(address, 0x05, 0x12) # set month
    bus.write_byte_data(address, 0x06, 0x21) # set year - last 2 digits
after modifying, execute script:
python3 settime_sample_ds3231.py
```

##### Read Time
```
pi@raspberrypi:~/RaspberryPiDriveRecorder $ python3 readtime_sample_ds3231.py 
2021-06-06 16:29:50
2021-06-06 16:29:50
2021-06-06 16:29:51
2021-06-06 16:29:52
2021-06-06 16:29:53
```

##### Disable systemd-timesyncd
```
systemctl disable systemd-timesyncd
Removed /etc/systemd/system/dbus-org.freedesktop.timesync1.service.
Removed /etc/systemd/system/sysinit.target.wants/systemd-timesyncd.service.
```

### Setting udev
```
cd /home/pi/RaspberryPiDriveRecorder/setting_files
sudo cp 50-i2c-mcp2221.rules /etc/udev/rules.d/
```

### Setting service file of PiRecorder
```
cd /home/pi/RaspberryPiDriveRecorder/setting_files
sudo cp RaspberryPiDriveRecorder.service /etc/systemd/system/
sudo systemctl enable RaspberryPiDriveRecorder
sudo reboot
```

## System launch tuning
https://nw-electric.way-nifty.com/blog/2017/04/raspberry-pi-ze.html
https://qiita.com/peace098beat/items/c95f0ba4d9edcf89b023
