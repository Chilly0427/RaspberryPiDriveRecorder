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
UUID=43EAF0604C063676 /media/pi/DriveRecorder ntfs-3g defaults 0 0
```

# Install video convert tool
```
sudo apt install gpac
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

