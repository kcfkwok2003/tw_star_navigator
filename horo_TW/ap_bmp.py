# ap_bmp.py
version='1.0'

import time

tch=0

def tch_cb(st,x,y):
    global tch
    print('st:%s x:%s y:%s' % (st,x,y))
    tch=st
    
def main(vs):
    global var_store, tft, tch
    var_store=vs
    tft=var_store['tft']
    tft.set_tch_cb(tch_cb)
    tft.use_buf(False)
    render_bmp(vs,12,0,215,215)
    if 'old_app_name' not in var_store:
        return
    while True:
        if tch:
            break
        time.sleep(1)
    return var_store['old_app_name']

def render_bmp(vs,x=12,y=0,w=215,h=215):
    global tft, tch
    f=open('test3.bmp','rb')
    f.seek(0x8a)
    ss = f.read((w+1)*2)
    n=0
    y0=y
    y = y+h
    while ss:
        if tch:
            break
        n+=1
        bs=bytearray()
        bx=ss[:]
        while bx:
            bs.append(bx[0])
            bs.append(bx[1])            
            bx=bx[2:]
            if tch:
                break
        tft.blit_buffer(bs,x,y,w,1)
        ss=f.read((w+1)*2)
        y-=1
        if y<=y0:
            break
    print('n:%s' % n)
