# ap_httpd_constel.py
version="1.0"

from color import *
import time
import machine
import gc
from httpd_util import *
from g_stars_1 import ct

USE_THREAD = False

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
    tft.fill_rect(20,50,200,100,NAVY)
    tft.rect(20,50,200,100,LIME)
    tft.text(apname, 25,60, WHITE,NAVY)
    tft.text(ip, 25,75,WHITE,NAVY)
    tft.text('starting httpd constel',25,90,WHITE,NAVY)
    
    tft.text('RESET',10,200,WHITE,NAVY)
    tft.rect(0,180,80,40,WHITE)
    if USE_THREAD:
        import _thread
        _thread.start_new_thread(_httpd,())
    else:
        _httpd()

HTML_CONSTELS="""
    <html>
    <head><title>Constellations</title></head>
    <body>
    <h2>Select Constellation</h2>
    <form action="/constels" method="get">
    <table>
    <tr><td>%(constels)s</td></tr>
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

HTML_CONSTEL="""
    <html>
    <head><title>Constellation</title></head>
    <body>
    <h2>Constellation</h2>
    <table>
    <tr><td>%(ct)s</td></tr>
    <tr>
    <td>
%(tbs)s
    </td>
    </tr>
    <tr>
    <td>
    </td>
    </tr>
    </table>
    <br>
    <br>
    <br>
    <a href="/">Refresh</a>
    <br>
    </body>
    </html>
"""

def add_select(dictx):
    global ct
    ct_keys = list(ct.keys())
    ct_keys.sort()
    cts='<select name="ct">'
    for item in ct_keys:
        cts+='<option value="%s">%s</option>' % (item,item)
    cts+="</select>"
    dictx['constels']=cts
    return dictx

def add_table(dictx):
    global ct
    ctx = dictx['ct']
    stars = ct[ctx]['stars']
    tb ='<table border="1"><tr><th>star</th><th>RA</th><th>Dec</th></tr>'
    for stx in stars:
        ra, dec = stars[stx]
        tb+="<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (stx,ra,dec)
    tb +='</table><br>'
    lines = ct[ctx]['lines']
    max_len=0
    for line in lines:
        if len(line) > max_len:
            max_len = len(line)
    tb +='<table border="1"><tr><th></th>'
    for i in range(max_len):
        tb +='<th>S%d</th>' % i
    tb+='<th><form action="/constels" method="get"><input type="hidden" name="ct" value="%s"><input type="Submit" value="render"></form></th>' % ctx
    tb+="</tr>"
    lx=0
    for line in lines:
        tb+="<tr><td>L%d</td>" % lx
        for i in range(max_len):
            if i < len(line):
                tb +="<td>%s</td>" % line[i]
            else:
                tb +="<td></td>"
        tb+='<td><form action="/ln" method="get"><input type="hidden" name="ct" value="%s"><input type="hidden" name="ln" value="%s"><input type="Submit" value="render"></form></tr>' % (ctx,lx)
        lx +=1
    tb+="</table>"
    dictx['tbs']=tb
    return dictx

def draw_ct(ctx):
    global var_store, ct, tft
    tft = var_store['tft']
    stars = ct[ctx]['stars']
    lines = ct[ctx]['lines']
    min_max = [128,64,0,-90] # xmin, ymin, xmax, ymax
    plines=[]
    for line in lines:
        plines.append([])
        for stx in line:
            ra, dec = stars[stx]
            chk_min_max(ra,dec,min_max)
            plines[-1].append((ra,dec))
    if min_max[2] - min_max[0] >20:
        # it seems wrap around in 24hr, retry
        plines =[]
        min_max=[128,64,0,-90] # xmin,ymin,xmax,ymax
        for line in lines:
            plines.append([])
            for starx in line:
                ra,dec=stars[starx]
                if ra <10:
                    ra+=24  # fix wrap around value
                    chk_min_max(ra,dec,min_max)
                    plines[-1].append((ra,dec))
    tft.fill_rect(0,0,128,64, NAVY)
    tft.rect(0,0,128,64,LIME)
    for points in plines:
        tft_plot_line(points,min_max)

def draw_ct_line(ctx, ix):
    global tft, var_store, ct
    tft = var_store['tft']
    stars = ct[ctx]['stars']
    lines = ct[ctx]['lines']    
    min_max=[128,64,0,-90] # xmin,ymin,xmax,ymax
    plines=[]
    for line in lines:
        plines.append([])
        for starx in line:
            ra,dec = stars[starx]
            chk_min_max(ra,dec,min_max)
            plines[-1].append((ra,dec))
    if min_max[2] - min_max[0] >20:
        # it seems wrap around in 24hr, retry
        plines=[]
        min_max=[128,64,0,-90] # xmin,ymin,xmax,ymax
        for line in lines:
            plines.append([])
            for starx in line:
                ra,dec=stars[starx]
                if ra <10:
                    ra+=24  # fix wrap around value
                    chk_min_max(ra,dec,min_max)
                    plines[-1].append((ra,dec))
    tft.fill_rect(0,0,128,64, NAVY)
    tft.rect(0,0,128,64,LIME)                    
    tft_plot_line(plines[ix],min_max)

def chk_min_max(x,y,min_max):
    if x< min_max[0]:
        min_max[0]=x
    if y< min_max[1]:
        min_max[1]=y
    if x > min_max[2]:
        min_max[2]=x
    if y > min_max[3]:
        min_max[3]=y

def tft_plot_line(points,min_max):
    global tft
    #scale to 2 pixel for 1 deg
    XSCALE=15 * 2  # 1hr=15 deg
    YSCALE= 2
    xr=min_max[0] * XSCALE
    yr=min_max[1] * YSCALE
    xrng = min_max[2] *XSCALE - xr
    yrng = min_max[3] *YSCALE - yr
    print('xrng %s yrng:%s' % (xrng,yrng))
    XOFS=int((128 - xrng)/2)
    YOFS=int((64-yrng)/2)
    xp = 128 -int(points[0][0] * XSCALE -xr + XOFS)
    yp = 64 -int(points[0][1] * YSCALE -yr + YOFS)
    tft_plot_star(xp,yp)
    for x,y in points[1:]:
        xv = 128 -int(x * XSCALE - xr + XOFS)
        yv = 64 - int(y * YSCALE - yr + YOFS)
        tft.line(xp,yp,xv,yv,BLUE)
        tft_plot_star(xv,yv)
        xp=xv
        yp=yv

def tft_plot_star(x,y):
    global tft
    tft.pixel(x-1,y,WHITE)
    tft.pixel(x, y-1,WHITE)
    tft.pixel(x+1,y,WHITE)
    tft.pixel(x, y+1,WHITE)

    
def _httpd():
    global var_store

    import socket
    addr = socket.getaddrinfo('0.0.0.0',80)[0][-1]
    s=socket.socket()
    s.bind(addr)
    s.listen(1)
    print('listening on',addr)
    tft = var_store['tft']
    tft.text('httpd constel listening',25,130,WHITE,NAVY)
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
        resp = HTML_CONSTELS % dictx
        conn.send(resp)
        conn.close()

def handle_c_constels(parms):
    print('set constels %s' % str(parms))
    dictx = get_html_parms(parms)
    dictx = add_table(dictx)
    resp = HTML_CONSTEL % dictx
    draw_ct(dictx['ct'])
    return ('OK',resp)

def handle_c_ln(parms):
    print('set constel %s' % str(parms))
    dictx = get_html_parms(parms)
    dictx = add_table(dictx)
    resp = HTML_CONSTEL % dictx
    ix = int(dictx['ln'])
    draw_ct_line(dictx['ct'], ix)
    return ('OK',resp)

def handle_cmd(cmd):
    print('cmd:%s' % str(cmd))
    pos=cmd.find(b'?')
    cmdx = cmd[:pos]
    if cmdx==b'/constels':
        return handle_c_constels(cmd[pos+1:])
    if cmdx==b'/ln':
        return handle_c_ln(cmd[pos+1:])    
    return None


