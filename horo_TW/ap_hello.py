# -*- coding: utf-8 -*-
# hello.py
version='1.0'
import time
from color import *
import font as fnt
fnt.table.set_e('etfontx32cg')

btnA_v=0
btnB_v=0
btnC_v=0
def tch_cb(st,x,y):
    global btnA_v, btnB_v, btnC_v
    print('st:%s x:%s y:%s' % (st,x,y))
    btnA_v=0
    btnB_v=0
    btnC_v=0
    if st==0:
        return
    if y > 200:
        if x < 80:
            btnA_v=1
        elif x > 160:
            btnC_v=1
        else:
            btnB_v=1
            
btn={'A':False, 'B':False, 'C':False}
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

def show_btns():
    global var_store,tft
    # btnA up
    tft.fill_rect(0,200,80,40,GREEN)
    tft.rect(0,200,80,40,YELLOW)
    tft.line(20,230,40,210,YELLOW)
    tft.line(60,230,40,210,YELLOW)
    tft.line(60,230,20,230,YELLOW)
    
    # btnB down
    tft.fill_rect(80,200,80,40,GREEN)
    tft.rect(80,200,80,40,YELLOW)
    tft.line(80+20,210,80+40,230,YELLOW)
    tft.line(80+60,210,80+40,230,YELLOW)
    tft.line(80+60,210,80+20,210,YELLOW)    

    # btnC enter
    tft.fill_rect(160,200,80,40,GREEN)
    tft.rect(160,200,80,40,YELLOW)
    tft.draw_string_at('C',190,202,fnt,YELLOW,GREEN)
    
def main(vs):
    global var_store,tft
    var_store=vs
    tft = var_store['tft']
    tft.set_tch_cb(tch_cb)
    tft.use_buf(False)
    tft.fill(NAVY)
    tft.rect(20,20,200,100,LIME)
    tft.text('Hello World!',25,50,WHITE,NAVY)
    tft.text('Press C to exit',25,60,WHITE,NAVY)
    cnt=0
    show_btns()
    while True:
        if chk_btn():
            if btn['C']:
                break
        time.sleep(1)
        tft.text('%s' % cnt, 25,80,WHITE,NAVY)
        cnt+=1
    return var_store['old_app_name']
