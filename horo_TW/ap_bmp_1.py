# ap_bmp.py
version='1.0'
import framebuf
import time
import struct

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
    render_bmp(tft,12,0,215,215)
    if 'old_app_name' not in var_store:
        return
    while True:
        if tch:
            break
        time.sleep(1)
    return var_store['old_app_name']

def render_bmp(tft,x=12,y=0,w=215,h=215):
    f=open('test3.bmp','rb')
    f.seek(0x8a)
    ss = f.read((w+1)*h*2)
    frmx = framebuf.FrameBuffer(bytearray(ss),w,h,framebuf.RGB565,w+1)
    from twatch import ST7789_MADCTL_MX,ST7789_MADCTL_MY,ST7789_MADCTL,ST77XX_RASET, ST77XX_CASET, ST77XX_RAMWR
    tft.write(ST7789_MADCTL, bytes([ST7789_MADCTL_MX]))
    tft.blit(frmx,x,y)
    #tft.show()
    tft.write(ST77XX_RASET, tft._encode_pos(0,240))
    tft.write(ST77XX_CASET, tft._encode_pos(0,240))
    tft.write(ST77XX_RAMWR)
    tft.write(None,tft.buf)
    v= ST7789_MADCTL_MX | ST7789_MADCTL_MY
    tft.write(ST7789_MADCTL, bytes([v]))

    
def render_bmp_(tft,x=12,y=0,w=215,h=215):
    global tch
    f=open('test3.bmp','rb')
    f.seek(0x8a)
    ss = f.read((w+1)*2)
    n=0
    y0=y
    y = y+h
    bs = bytearray()
    while ss:
        if tch:
            break
        n+=1
        #bs=bytearray()
        bx=ss[:-2]
        while bx:
            bs.append(bx[0])
            bs.append(bx[1])            
            bx=bx[2:]
            if tch:
                break
        #frm = framebuf.FrameBuffer(bytearray(
        #tft.blit_buffer(bs,x,y,w,1)
        ss=f.read((w+1)*2)
        y-=1
        if y<=y0:
            break
    frm = framebuf.FrameBuffer(bs,w,h,framebuf.RGB565)
    tft.blit(frm,x,0)
    tft.show()
    print('n:%s' % n)    
    
