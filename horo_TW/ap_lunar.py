# -*- coding: utf-8 -*-
# ap_lunar.py
version='1.0'

from machine import lightsleep,Pin
import esp32
from color import *
from tfth_util import *
import lunar as ln
import time
import sys

import font as fnt
fnt.table.set_c('ctfontx32cg')
fnt.table.set_e('etfontx32cg')

pek_short=False
def pmu_cb(intsts3):
    global pek_short, tft
    if pek_short:
        return
    if intsts3 & 0x02:
        print('pek_short')
        pek_short=True
        
btnA_v=0
btnB_v=0
btnC_v=0
btnD_v=0
def tch_cb(st,x,y):
    global btnA_v, btnB_v, btnC_v, btnD_v, tft
    print('st:%s x:%s y:%s' % (st,x,y))
    btnA_v=0
    btnB_v=0
    btnC_v=0
    btnD_v=0
    if st==0:
        return
    if y<100:
        if x < 80:
            btnD_v=1
    if y > 180:
        if x < 80:
            btnA_v=1
        elif x > 160:
            btnC_v=1
        else:
            btnB_v=1
            
btn={'A':False, 'B':False, 'C':False, 'D':False}
def chk_btn():
    global  var_store
    if btnA_v:
        if not btn['A']:
            btn['A']=True
            return True
    else:
        btn['A']=False
    if btnB_v:
        if not btn['B']:
            btn['B']=True
            return True
    else:
        btn['B']=False
    if btnC_v:
        if not btn['C']:
            btn['C']=True
            return True
    else:
        btn['C']=False
    if btnD_v:
        if not btn['D']:
            btn['D']=True
            return True
    else:
        btn['D']=False
        
    
WDAYS=['MON','TUE','WED','THU','FRI','SAT','SUN']
skip='''
def sync_time():
    import ntptime
    try:
        print('sync time')
        ntptime.settime()
        clear_tdiff()
        return True
    except Exception as e:
        sys.print_exception(e)
        print('sync time failure')
'''
QX_NONE=0
QX_MENU=1
QX_HORO=2

def main(vs):
    global var_store, tft
    var_store=vs
    tft = var_store['tft']
    tft.set_tch_cb(tch_cb)
    motor=var_store['motor']
    tft.fill(NAVY)
    rtcx = var_store['rtcx']
    rtcx.sync_local()
    qx=QX_NONE
    while True:
        if qx:
            break
        if chk_btn():
            if btn['A']:
                qx=QX_MENU
                break
            if btn['D']:
                qx=QX_HORO
                break
        tm = get_time()
        ct = time.localtime(tm)
        yr,mon,mday,hr,minu,sec,wday,_,=ct
        show_lunar(yr,mon,mday,hr,minu,sec)
        show_datetime(yr,mon,mday,hr,minu,sec,wday)
        i=0
        sleep_btn=False
        while True:
            if chk_btn():
                if btn['A']:
                    qx=QX_MENU
                    break
                if btn['D']:
                    qx=QX_HORO
                    break
                if btn['C']:
                    sleep_btn=True
            if sleep_btn:
                sleep_btn=False
                print('lightsleep')
                #prepare sleep here
                tft.set_wake_on_pek()
                #shutdown wifi ...
                tft.bl_off()
                tft.sleep_mode(1)
                lightsleep()
                # wake up here
                print('wakeup')
                motor.duty(8)
                time.sleep(0.2)
                motor.duty(0)
                tft.sleep_mode(0)
                tft.bl_on()
                # turn on wifi... 
                break                
            time.sleep(0.5)
            tm = get_time()
            ct = time.localtime(tm)
            yr,mon,mday,hr,minu,sec,wday,_,=ct
            colon=' '
            if i:
                colon=':'
            i = not i
            tft.draw_string_at(colon,160,160,fnt,fg=WHITE,bg=NAVY)
            if sec==0:
                if minu==0:
                    # sync every hour
                    rtcx.sync_local()
                break
    if qx==QX_MENU:
        print("start ap_menu")
        return "ap_menu"
    if qx==QX_HORO:
        print("start horo")
        return "tfth"
    print("return None")
    
def show_lunar(yr,mon,mday,hr,minu,sec):
    global tft
    ct = time.mktime((yr,mon,mday,hr,minu,sec,0,0,0))
    lnx = ln.Lunar(ct)
    gz_yr = lnx.gz_year()
    sx_yr = lnx.sx_year()
    xyr, xmon, xday = lnx.ln_date()
    jie, ofs = lnx.ln_jie_2()
    gz_hr, gz_ke, gz_kev = lnx.gz_hour()
    if gz_ke >0:
        gz_hr += gz_kev
    x=10
    y=5
    tft.draw_string_at('農曆',x,y+0,fnt,bg=NAVY)
    tft.draw_string_at('%s%s年' % (gz_yr,sx_yr), x,y+32, fnt,bg=NAVY)
    tft.draw_string_at('%s月%s' % (lnx.lm[xmon-1], lnx.ld[(xday-1)*2:xday*2]), x,y+64,fnt,bg=NAVY)
    tft.draw_string_at('%s月' % lnx.gz_month(),x,y+96,fnt,bg=NAVY)
    tft.draw_string_at('%s日' % lnx.gz_day(),x,y+128,fnt,bg=NAVY)
    tft.draw_string_at('%s' % gz_hr,x,y+160,fnt,bg=NAVY)
    print('ofs:%d' % ofs)
    if ofs==0:
        tft.draw_string_at('%s' % jie,x,y+192,fnt,bg=NAVY)
    else:
        tft.draw_string_at('%s+%d' % (jie,ofs),x,y+192,fnt,bg=NAVY)

def show_datetime(yr,mon,mday,hr,minu,sec,wday):
    global tft
    tft.draw_string_at('%d' % yr,144,0,fnt,fg=WHITE,bg=NAVY)
    tft.draw_string_at('/%02d' % mon,160,32,fnt,fg=WHITE,bg=NAVY)
    tft.draw_string_at('/%02d' % mday,160,64,fnt,fg=WHITE,bg=NAVY)
    tft.draw_string_at('%s' % WDAYS[wday],160,96,fnt,fg=WHITE,bg=NAVY)

    tft.draw_string_at('%02d' % hr,186,128,fnt,fg=WHITE,bg=NAVY)
    tft.draw_string_at(':%02d' % minu,160,160,fnt,fg=WHITE,bg=NAVY)

    
