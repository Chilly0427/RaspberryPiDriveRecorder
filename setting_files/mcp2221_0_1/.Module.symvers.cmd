cmd_/home/pi/RaspberryPiDriveRecorder/setting_files/mcp2221_0_1/Module.symvers := sed 's/ko$$/o/' /home/pi/RaspberryPiDriveRecorder/setting_files/mcp2221_0_1/modules.order | scripts/mod/modpost -m -a   -o /home/pi/RaspberryPiDriveRecorder/setting_files/mcp2221_0_1/Module.symvers -e -i Module.symvers   -T -
