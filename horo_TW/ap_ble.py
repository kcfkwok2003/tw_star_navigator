# ap_ble.py
version='1.0'

from color import *
import time
import font as fnt
fnt.table.set_e('etfontx32cg')

btnC_v=0
def tch_cb(st,x,y):
    global btnC_v
    print('st:%s x:%s y:%s' % (st,x,y))
    btnC_v=0
    if st==0:
        return
    if y > 200:
        if x > 160:
            btnC_v=1
            
btn={'C':False}
def chk_btn():
    global  var_store
    if btnC_v:
        if not btn['C']:
            btn['C']=True
            return True
    else:
        btn['C']=False

def show_btns():
    global var_store,tft
    # btnC enter
    tft.fill_rect(160,200,80,40,GREEN)
    tft.rect(160,200,80,40,YELLOW)
    tft.draw_string_at('C',190,202,fnt,YELLOW,GREEN)
    
def main(var_store):
    global tft
    hm = var_store['horo_main']
    tft = var_store['tft']
    tft.set_tch_cb(tch_cb)
    tft.use_buf(False)
    #info = hm.info
    #apname = info['apname']
    #ip = info['ip']
    tft.fill_rect(20,20,200,100,NAVY)
    tft.rect(20,20,200,100,LIME)
    #tft.text(apname, 25,30, WHITE,NAVY)
    #tft.text(ip, 25,40,WHITE,NAVY)    
    tft.text('starting ble',25,50,WHITE,NAVY)
    import ble_set_ap
    ble_uart = ble_set_ap.start(hm.AP_ESSID)
    var_store['ble_uart']=ble_uart
    var_store['ble_started']=True
    tft.text('BLE:%s' % hm.AP_ESSID, 25,50,WHITE,NAVY)
    tft.text('Press C to exit',25,60,WHITE,NAVY)
    show_btns()
    while True:
        if chk_btn():
            if btn['C']:
                break
        time.sleep(1)        
    return var_store['old_app_name']


