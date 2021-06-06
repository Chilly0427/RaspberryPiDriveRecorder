cmd_/home/pi/work/mcp2221_0_1/modules.order := {   echo /home/pi/work/mcp2221_0_1/i2c-mcp2221.ko; :; } | awk '!x[$$0]++' - > /home/pi/work/mcp2221_0_1/modules.order
