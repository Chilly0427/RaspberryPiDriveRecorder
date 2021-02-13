# RaspberryPiDriveRecorder
# Clone
```
cd /home/pi/
git clone https://github.com/Chilly0427/RaspberryPiDriveRecorder.git 
ls
RaspberryPiDriveRecorder
```

# Install video convert tool
```
sudo apt install gpac
```

# GPS Setting
```
sudo apt-get install gpsd gpsd-clients python-gps
sudo apt-get install cu
cd /home/pi/RaspberryPiDriveRecorder/
sudo cp gpsd /etc/default/
sudo systemctl enable gpsd.socket
sudo systemctl start gpsd.socket
reboot
```

# Setting service file of PiRecorder
```
cd /home/pi/RaspberryPiDriveRecorder/
sudo cp RaspberryPiDriveRecorder.service /etc/systemd/system/
sudo systemctl enable RaspberryPiDriveRecorder
sudo reboot
```

