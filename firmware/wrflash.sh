# for COM1 = /dev/ttyS0
#esptool.py --chip esp32 --port /dev/ttyS5 write_flash -z 0x1000 mpy1.bin
esptool.py --chip esp32 --port $1 write_flash -z 0x1000 $2
