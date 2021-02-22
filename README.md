# RaspberryPiDriveRecorder
# Clone
```
cd /home/pi/
git clone https://github.com/Chilly0427/RaspberryPiDriveRecorder.git 
ls
RaspberryPiDriveRecorder
```

# USB /etc/fstab
```
sudo vi /etc/fstab
UUID=26611C2C36F5A173 /media/pi/DriveRecorder ntfs-3g defaults 0 0

```

# Install video convert tool
```
sudo apt install gpac
```

# GPSD Install and Settings
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

# Import GPS module
```
https://github.com/inmcm/micropyGPS
import micropyGPS.py
```

# Setting service file of PiRecorder
```
cd /home/pi/RaspberryPiDriveRecorder/
sudo cp RaspberryPiDriveRecorder.service /etc/systemd/system/
sudo systemctl enable RaspberryPiDriveRecorder
sudo reboot
```

