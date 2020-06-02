# -*- coding: utf-8 -*-
# ap_menu.py
version='1.0'

from color import *
import time
import font as fnt
fnt.table.set_e('etfontx32cg')

MLINES=10

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
        
def clear_dialog():
    global tft
    tft.fill_rect(10,40,100,40,NAVY)
    tft.rect(10,40,100,40,NAVY)
    dialog_on=False
    
def reset(n):
    global tft
    print('reset')
    tft.text('Reseting...',5,5,WHITE)
    import machine
    machine.reset()
    
def quit(n):
    global quit_f
    print('quit')
    quit_f=True
    
    
def on_up(n):
    global msel,menu,dialog_on
    if dialog_on:
        clear_dialog()

    msel-=1
    if msel<0:
        msel=len(menu['items'])-1
    show_menu()
    print('on_up %s msel:%s' % (menu['name'],msel))

def on_down(n):
    global msel, menu, dialog_on
    if dialog_on:
        clear_dialog()
    msel+=1
    if msel >=len(menu['items']):
        msel=0
    print('on_down %s msel:%s' % (menu['name'],msel))
    show_menu()

def on_enter(n):
    global msel, menu,next_app,quit_f
    print('on_enter')
    items=menu['items']
    action= items[msel][1]
    if action:
        if type(action)==type(''):
            next_app=action
            quit_f=True
        elif type(action)==type(()):
            start_app(action[0],action[1])
        else:
            action(n)

def start_app(act_name,msg):
    global tft
    tft.text(msg,5,5,WHITE)
    from machine import RTC, deepsleep
    rtc=RTC()
    rtc.memory(act_name)
    time.sleep(1)
    deepsleep(1) # use deepsleep to reset and release memory
    
MENU_MAIN={
    'name':'Main Menu',
    'items':[
        ('1.Back', ''),
        ('2.Hello','ap_hello'),
        ('3.Horo','tfth',),
        ('4.Lunar calendar','ap_lunar'),
        ('5.WIFI','ap_wifi'),
        ('6.Bluetooth(BLE)','ap_ble'),
        #('6.Frequency test','ap_freq_test'),
        ('7.Menu test', 'ap_menu_test'),        
        ('8.Httpd constellation',('ap_httpd_constel','httpd set constellation...')),
        ('9.Httpd horo',('ap_httpd_horo','httpd set horo...')),        
        ('10.Httpd planet',('ap_httpd_planet','httpd set planet...')),        
        ('11.Show Bitmap','ap_bmp'),
        ('12.Reset',reset),
        ('13.Quit', quit),        
        ]
    }

def show_menu(refresh=False):
    global msel,mstart,menu,tft,longest_len
    if refresh:
        tft.fill(NAVY)
    if msel< mstart:
        mstart=msel
    if msel >= mstart+MLINES:
        mstart= msel -MLINES+1

    x=0
    y=0
    w= 240
    h=20
    menu_name=menu['name']
    tft.text(menu_name,x+2,y+5,WHITE)
    tft.rect(x,y,w,h,WHITE)
    
    y+=25
    items = menu['items'][mstart:]
    for i in range(MLINES):
        if len(items) < i:
            item=' '
        else:
            item=items[i][0]
        menux = '{m: <{w}}'.format(m=item,w=longest_len)
        if i+mstart==msel:
            tft.text(menux,x,y,NAVY,WHITE)
        else:
            tft.text(menux,x,y,WHITE,BG_NAVY)
        y+=15
        i+=1
    

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
    global var_store,tft,msel,mstart,menu,btn,dialog_on,quit_f,next_app,longest_len
    var_store=vs
    tft = var_store['tft']
    tft.set_tch_cb(tch_cb)
    
    dialog_on=False
    quit_f=False
    next_app=None
    msel=0
    mstart=0
    MENU_MAIN['items'][0]=('1.Back',var_store['old_app_name'])
    menu=MENU_MAIN
    longest_len=0
    for item in menu['items']:
        if len(item[0])>longest_len:
            longest_len=len(item[0])
            
    show_menu(True)
    show_btns()
    while True:
        if chk_btn():
            if btn['A']:
                on_up('A')
            elif btn['B']:
                on_down('B')
            elif btn['C']:
                on_enter('C')
            
        time.sleep(0.1)
        if quit_f:
            break
    return next_app
