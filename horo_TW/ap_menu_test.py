# -*- coding: utf-8 -*-
# ap_menu_test.py
version='ap_menu_test-1.0'

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

def item_dialog(n):
    global tft,menu,msel,dialog_on
    text = menu['items'][msel][0]
    tft.fill_rect(10,40,100,40,NAVY)
    tft.text(text,12,42,WHITE)
    tft.rect(10,40,100,40,WHITE)
    dialog_on=True
    
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
    global msel,dialog_on
    if dialog_on:
        clear_dialog()
    if msel>0:
        msel-=1
        show_menu()
    print('on_up %s msel:%s' % (menu['name'],msel))

def on_down(n):
    global msel, menu, dialog_on
    if dialog_on:
        clear_dialog()
    if msel < len(menu['items']) -1:
        msel+=1
        print('on_down %s msel:%s' % (menu['name'],msel))
        show_menu()

def on_enter(n):
    global msel, menu, next_app,quit_f
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
    
MENU_TEST={
    'name':'Test',
    'items':[
        ('Back',''),
        ('Item 1',item_dialog),
        ('Item 2',item_dialog),
        ('Quit', quit),
        ('Reset',reset),
        ]
    }

    
def show_menu(refresh=False):
    global msel,mstart,menu,tft
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
    items = menu['items']
    i=0
    for item in items[mstart:]:
        if i > MLINES:
            break
        menux = item[0]
        if i+mstart==msel:
            tft.text(menux,x,y,BLACK,WHITE)
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
    global var_store,tft,msel,mstart,menu,btn,dialog_on,quit_f,next_app
    var_store=vs
    tft = var_store['tft']
    tft.set_tch_cb(tch_cb)
    
    dialog_on=False
    quit_f=False
    msel=0
    mstart=0
    MENU_TEST['items'][0]=('Back',var_store['old_app_name'])    
    menu=MENU_TEST
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
