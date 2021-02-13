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

# Setting service file of PiRecorder
```
cd /home/pi/RaspberryPiDriveRecorder/
sudo cp RaspberryPiDriveRecorder.service /etc/systemd/system/
sudo systemctl enable RaspberryPiDriveRecorder
sudo reboot
```

