# ap_httpd_planet.py
version="1.0"

from color import *
import time
import gc
import machine
from httpd_util import *
from g_planet_1 import g_planet, g_width
planets = ['Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto']

BITMASK =  [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80]
BITMASK2 = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x01,0x02,0x04,0x08]
USE_THREAD=False

def tch_cb(st,x,y):
    global tch, tft
    if st==0:
        return
    if y>180:
        if x <80:
            tft.text('RESETING...',10,170,WHITE,RED)
            rtc=machine.RTC()
            rtc.memory('ap_menu')
            machine.deepsleep(1)

            

def main(vs):
    global var_store,tft
    var_store=vs    
    horo_main = var_store['horo_main']
    tft = var_store['tft']
    tft.set_tch_cb(tch_cb)
    tft.use_buf(False)
    info = horo_main.info
    apname = info['apname']
    ip = info['ip']
    tft.fill_rect(20,20,200,100,NAVY)
    tft.rect(20,20,200,100,LIME)
    tft.text(apname, 25,30, WHITE,NAVY)
    tft.text(ip, 25,40,WHITE,NAVY)
    tft.text('starting httpd planet',25,50,WHITE,NAVY)
    tft.text('RESET',10,200,WHITE,NAVY)
    tft.rect(0,180,80,40,WHITE)
    
    if USE_THREAD:
        import _thread
        _thread.start_new_thread(_httpd,())
    else:
        _httpd()

HTML_PLANETS="""
    <html>
    <head><title>Planets</title></head>
    <body>
    <h2>Select Planet</h2>
    <form action="/planets" method="get">
    <table>
    <tr><td>%(planets)s</td></tr>
    <tr>
    <td>
    <input type="Submit" value="submit" 
    </td>
    </tr>
    </table>
    </form>
    <br>
    <br>
    <br>
    <a href="/">Refresh</a>
    <br>
    </body>
    </html>
"""

HTML_PLANET="""
    <html>
    <head><title>Planet</title></head>
    <body>
    <h2>Edit Planet symbol</h2>
    <form action="/planet" method="get">
    <table>
    <tr><td>%(planet)s</td></tr>
    <tr>
    <td>
    <table>
%(bmp)s
    </tr>
    </table>
    </td>
    </tr>
    <tr>
    <td>
<input type="Submit" value="submit">
<input type="hidden" name="pn" value="%(planet)s">
    </td>
    </tr>
    </table>
    </form>
    <br>
    <br>
    <br>
    <a href="/">Refresh</a>
    <br>
    </body>
    </html>
"""

def add_select(dictx):
    pns =''
    pns +='<select name="planet">'
    for item in planets:
        pns +='<option value="%s">%s</option>' % (item,item)
    pns+="</select>"
    dictx['planets']=pns
    return dictx

def add_hline(hb,lb,y):
    hs ='<tr>'
    x=0
    for bm in BITMASK:
        if (hb & bm):
            hs+='<td><input type="radio" name="%x%x" checked></td>' % (x,y)
        else:
            hs+='<td><input type="radio" name="%x%x"></td>' % (x,y)
        x+=1
    for bm in BITMASK[:4]:
        if (lb & bm):
            hs+='<td><input type="radio" name="%x%x" checked></td>' % (x,y)
        else:
            hs+='<td><input type="radio" name="%x%x"></td>' % (x,y)            
        x+=1
    hs+="</tr>"
    return hs

def add_symbol(dictx):
    pn = dictx['planet']
    bs = g_planet[pn]
    mx =''
    y=0
    while bs:
        hb,lb,bs = bs[0],bs[1],bs[2:]
        mx +=add_hline(hb,lb,y)
        y+=1
    dictx['bmp']=mx
    return dictx    
        
def save_symbols():
    global g_planet, g_width
    print('save_symbols')
    code_txt='''
g_width=%s
g_planet={}
'''  % g_width
    for pn in planets:
        txt="g_planet['%s']=bytearray([\n" % pn
        bs = g_planet[pn]
        i=0
        for bx in bs:
            txt+=' 0x%02x,' % bx
            i+=1
            if i % 12==0:
                txt+='\n'
        txt+='])\n'
        code_txt+=txt
    f=open('g_planet_1.py','w')
    f.write(code_txt)
    f.close()

def _httpd():
    global var_store

    import socket
    addr = socket.getaddrinfo('0.0.0.0',80)[0][-1]
    s=socket.socket()
    s.bind(addr)
    s.listen(1)
    print('listening on',addr)
    tft = var_store['tft']
    tft.text('httpd planet listening',25,50,WHITE,NAVY)
    while True:
        conn,addr = s.accept()
        print("connected from",addr)
        req = conn.recv(1024)
        print("content=%s" % str(req))
        if req==b'':
            continue
        if req[:4]==b'GET ':
            pos = req.find(b' HTTP/')
            cmd = req[4:pos]
            res = handle_cmd(cmd)
            if type(res)==type(()):
                resp=res[1]
                conn.send(resp)
                conn.close()
                continue
            if res is not None:
                
                resp="""<html><body>Result: %s<br><br><a href="/">Home</a></body></html>""" % res
                conn.send(resp)
                conn.close()
                continue

        dictx={}
        dictx = add_select(dictx)
        resp = HTML_PLANETS % dictx
        conn.send(resp)
        conn.close()

def handle_c_planets(parms):
    print('set_planets: %s' % str(parms))
    dictx = get_html_parms(parms)
    print('dictx:%s' % dictx)
    dictx = add_symbol(dictx)
    resp = HTML_PLANET % dictx
    return ('OK', resp)

def handle_c_planet(parms):
    print('set_planet: %s' % str(parms))
    dictx = get_html_parms(parms)
    print('dictx:%s' % dictx)
    pn = dictx['pn']
    del dictx['pn']
    bs=bytearray()
    for y in range(12):
        bx=0
        for x in range(8):
            k = '%x%x' % (x,y)
            if k in dictx:
                bx |= BITMASK[x]
        bs.append(bx)
        bx =0
        for x in range(8,12):
            k = '%x%x' % (x,y)
            if k in dictx:
                bx |= BITMASK2[x]            
        bs.append(bx)
    g_planet[pn]=bs
    save_symbols()
    return 'OK'

def handle_cmd(cmd):
    print('cmd:%s' % str(cmd))
    pos=cmd.find(b'?')
    cmdx = cmd[:pos]
    if cmdx==b'/planets':
        return handle_c_planets(cmd[pos+1:])
    if cmdx==b'/planet':
        return handle_c_planet(cmd[pos+1:])
    return None


