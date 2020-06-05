#main.py
version="main-1.0"
import axp202
import time
from machine import Pin,PWM,reset,RTC,I2C
from pcf8563 import PCF8563
import sys

MOTOR_PIN=4
motor=PWM(Pin(MOTOR_PIN),freq=12000, duty=8)
time.sleep(0.2)
motor.duty(0)

def free_mem():
    for item in sys.modules:
        del sys.modules[item]
    objs = globals()
    for obj in ['tfth',]:
        if obj in objs:
            print('del %s' % objs[obj])
            del objs[obj]
    gc.collect()

from color import *
from axp202 import pmu_start
pmu=pmu_start()


try:
    import horo_main1 as horo_main
    print('horo_main1 used')
except Exception as e:
    import horo_main

from wifi_stt import *
wifi_state= get_wifi_state()
if wifi_state==WIFI_CONN:
    try:
        horo_main.setup_sta(scl=21,sda=22)
    except Exception as e:
        sys.print_exception(e)
elif wifi_state ==WIFI_AP:
    horo_main.setup_ap1()
        
i2c=I2C(scl=Pin(22),sda=Pin(21), freq=400000)
rtcx = PCF8563(i2c,0x51)

import twatch
tft = twatch.TFT()
tft.set_pmu(pmu)
tft.bl_on()
tft.start_spi()
tft.fill_rect(0,0,240,20,NAVY)
tft.text('starting...',5,5, WHITE,NAVY)
import gc
gc.collect()
var_store={'tft':tft,'horo_main':horo_main,'free_mem':free_mem,'motor':motor,'rtcx':rtcx}

rtc=RTC()
app_name=rtc.memory()
if not app_name:
    import ap_bmp_1
    ap_bmp_1.main(var_store)
    free_mem()
    app_name='ap_lunar'
else:
    app_name=app_name.decode('utf-8')

var_store['old_app_name']=app_name
while app_name:
    old_app_name=app_name
    app = __import__(old_app_name)
    app_name = app.main(var_store)
    var_store['old_app_name']=old_app_name
    del sys.modules[old_app_name]
    gc.collect()


tft.fill(NAVY)
try:
    info = horo_main.info
    ip = info['ip']
    if ip=='-':
        horo_main.setup_ap1()
        tft.text(info['appass'], 5,35, WHITE,NAVY)

    ip = info['ip']
    apname = info['apname']
    tft.text(apname, 5,5,WHITE,NAVY)
    tft.text(ip, 5,15,WHITE,NAVY)
    tft.text('Use webrepl to program', 5,25,WHITE,NAVY)
except Exception as e:
    sys.print_exception(e)
    
tft.text('RESET',10,200, WHITE,NAVY)
tft.rect(0,180,80,40,WHITE)

def tch_cb(st,x,y):
    global tch
    if st==0:
        return
    if y>180:
        if x <80:
            tft.text('RESETING...',10,100,WHITE,RED)
            reset()

tft.set_tch_cb(tch_cb)

