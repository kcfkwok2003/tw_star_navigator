from color import *
import time
import gc
import sys
import machine

USE_THREAD=False

def tch_cb(st,x,y):
    global tch, tft
    if st==0:
        return
    if y>180:
        if x <80:
            tft.text('RESETING...',10,170,WHITE)
            rtc=machine.RTC()
            rtc.memory('ap_menu')
            machine.deepsleep(1)

            
def unescape(val):
    if '%' not in val:
        return val
    res=''
    while val:
        if '%' in val:
            pos = val.find('%')
            res+=val[:pos]
            sub = val[pos+1:pos+3]
            res+= chr(int(sub,16))
            val = val[pos+3:]
        else:
            res+=val
            break
    print("unescape: %s" % res)
    return res

def get_html_parms(parms):
    dictx={}
    while parms:
        pos = parms.find(b'=')
        key = str(parms[:pos],'utf-8')
        pos2= parms.find(b'&')
        if pos2>0:
            val = str(parms[pos+1:pos2],'utf-8')
            parms = parms[pos2+1:]
        else:
            val = str(parms[pos+1:],'utf-8')
            parms=b''
        dictx[key]=unescape(val)
    return dictx

def handle_cmd_set_wifi(parms):
    print('set_wifi: %s' % str(parms))
    dictx = get_html_parms(parms)
    if dictx['ssid']=='' or len(dictx['pass'])<8:
        return 'Error'
    ss="apname='%(ssid)s'\nappass='%(pass)s'\n" % dictx
    f=open('ap.py','w')
    f.write(ss)
    f.close()
    return 'OK'

def handle_cmd_set_dt(parms):
    dictx = get_html_parms(parms)
    if 'action' not in dictx:
        return 'Error no action'
    try:
        lat =float(dictx['lat'])
        lon= float(dictx['lon'])
    except Exception as e:
        sys.print_exception(e)
        return 'Error geo location'

    drx =dictx['drx']

    yri=int( dictx['yr'])
    moni=int(dictx['mon'])
    mdayi=int(dictx['mday'])
    hri = int(dictx['hr'])
    mini =int(dictx['min'])
    tz =int(dictx['tz'])

    tmx = time.mktime((yri,moni,mdayi,hri,mini,0,0,0)) - tz*60*60
    tmy = time.localtime(tmx)
    yr = tmy[0]
    mon= tmy[1]
    mday = tmy[2]
    hr = tmy[3]
    minx = tmy[4]
    wday= tmy[6]
    #jds = hu.ymd_to_jd(yri,moni,mdayi) + hu.hms_to_decday(hri,mini,0) - tz/24.0
    #yr,mon,mday,hr,minx,_=hu.jd_to_ymdhms(jds)
    action=dictx['action']
    if action=='set':
        from tfth_util import save_tdiff, save_tzone, save_geo_cfg
        save_tdiff(tmx)
        save_tzone(tz)
        save_geo_cfg(lat,lon,drx)
        return 'OK'
    if action=='render':
        render_horo(tz, yri,moni,mdayi,hri,mini,0,wday,lat,lon,drx)
        return 'OK'
    return 'Invalid action'

def add_select(dictx):
    ranges={}
    ranges['drx']=['E','W']
    drxs=''
    for item in ['drx']:
        drxs+='<select name="%s">' % item
        for i in ranges[item]:
            if dictx[item]==i:
                drxs+='<option value="%s" selected>%s</option>' % (i,i)
            else:
                drxs+='<option value="%s">%s</option>' % (i,i)
        drxs+="</select>"
    dictx['drxs']=drxs
    return dictx

def render_horo(tz,yr,mon,mday,hr,minu,sec,wday,lat,lon,drx):
    global var_store
    tft=var_store['tft']
    from tfth import TFTHoro, WDAYS
    tfth = TFTHoro(tft,tzone=tz,lat=lat,lon=lon,drx=drx)
    try:
        from g_planet_1 import g_planet
        tfth.g_planet = g_planet
    except Exception as e:
        sys.print_exception(e)
    try:
        from g_stars_1 import ct
        tfth.constel =ct
    except Exception as e:
        sys.print_exception(e)
        
    tfth.set_datetime(yr,mon,mday,hr,minu,sec)
    tfth.cal_horo_info()
    tfth.start_gr(True)
    skip="""
    import font as fnt
    fnt.table.set_e('etfontx32cg')
    tft.draw_string_at('%d' % yr,220,5,fnt,fg=WHITE,bg=NAVY)
    tft.draw_string_at('%02d' % mon,268,37,fnt,fg=WHITE,bg=NAVY)
    tft.draw_string_at('%02d' % mday,268,69,fnt,fg=WHITE,bg=NAVY)
    tft.draw_string_at('%s' % WDAYS[wday],244,101,fnt,fg=WHITE,bg=NAVY)

    tft.draw_string_at('%02d' % hr,268,133,fnt,fg=WHITE,bg=NAVY)
    tft.draw_string_at(':%02d' % minu,244,165,fnt,fg=WHITE,bg=NAVY)
"""
    gc.collect()
    
def main(vs):
    global var_store,tft
    var_store=vs    
    horo_main = var_store['horo_main']
    tft = var_store['tft']
    tft.set_tch_cb(tch_cb)    
    info = horo_main.info
    apname = info['apname']
    ip = info['ip']
    tft.fill_rect(20,20,200,100,NAVY)
    tft.rect(20,20,200,100,LIME)    
    tft.text(apname, 25,30, WHITE)
    tft.text(ip, 25,40,WHITE)
    tft.text('starting httpd',25,50,WHITE)
    tft.text('RESET',10,200)
    tft.rect(0,180,80,40,WHITE)    
    if USE_THREAD:
        import _thread
        _thread.start_new_thread(_httpd,())
    else:
        _httpd()
    
def _httpd():
    global var_store
    html="""
    <html>
    <head><title>Horo setup</title></head>
    <body>
    Device Time:%(tms)s
    <br><br>
    <h2>Set Wifi Connection</h2>
    <form action="/set_wifi" method="get">
    <table border="1">
    <tr><th>Field</th><th>Value</th></tr>
    <tr><td>SSID</td><td><input type="text" name="ssid" value=""></td></tr>
    <tr><td>Pass</td><td><input type="password" name="pass" value=""></td></tr>
    <tr><td></td><td><input type="Submit" value="submit"></td></tr>
    </table>
    </form>
    <br><br>
    <h2>Set Date Time</h2>
    <form action="/set_dt" method="get">
    <table border="1">
    <tr><th>Field</th><th>Value</th></tr>
    <tr><td>Date (yyyy-mm-dd)</td><td><input type="text" name="yr" value="%(yr)s">-<input type="text" name="mon" value="%(mon)s">-<input type="text" name="mday" value="%(mday)s"></td></tr>
    <tr><td>Time (HH:MM)</td><td><input type="text" name="hr" value="%(hr)s">:<input type="text" name="min" value="%(min)s"></td></tr>
    <tr><td>Time Zone</td><td><input type="text" name="tz" value="%(tz)s"></td></tr>
    <tr><td>Latitude (N)</td><td><input type="text" name="lat" value="%(lat)s"></td></tr>
    <tr><td>Longitude</td><td><input type="text" name="lon" value="%(lon)s"> %(drxs)s</td></tr>
    <tr><td>Action type</td><td><input type="radio" name="action" value="set">Set &nbsp&nbsp<input type="radio" name="action" value="render">Render only</td></tr>
    <tr><td></td><td><input type="Submit" value="submit" value=""></td></tr>
    </table>
    </form>
    <br>
    <br>
    <br>
    <a href="/">Refresh</a>
    <br>
    <a href="https://github.com/micropython/webrepl">Webrepl download</a>
    <br>
    </body>
"""
    import socket
    addr = socket.getaddrinfo('0.0.0.0',80)[0][-1]
    s=socket.socket()
    s.bind(addr)
    s.listen(1)
    print('listening on',addr)
    tft = var_store['tft']
    tft.text('httpd listening',25,50,WHITE)    
    from tfth import get_time, load_tzone, load_geo_cfg
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
            if res is not None:
                resp="""<html><body>Result: %s<br><br><a href="/">Home</a></body></html>""" % res
                conn.send(resp)
                conn.close()
                continue
        tm = get_time()
        tzone=load_tzone()
        lat,lon,drx= load_geo_cfg()
        #tm = time.time()+tzone*60*60
        ct = time.localtime(tm)
        yr,mon,mday,hr,minu,sec,wday,_,= ct
        ds = '%d-%d-%d %02d:%02d:%02d' % (yr,mon,mday,hr,minu,sec)
        dictx={'tms':ds,'yr':yr,'mon':mon,'mday':mday,'hr':hr,'min':minu,'tz':tzone,'lat':lat,'lon':lon,'drx':drx}
        dictx=add_select(dictx)
        resp = html % dictx
        conn.send(resp)
        conn.close()

    
def handle_cmd(cmd):
    print('cmd:%s' % str(cmd))
    pos=cmd.find(b'?')
    cmdx = cmd[:pos]
    if cmdx==b'/set_wifi':
        return handle_cmd_set_wifi(cmd[pos+1:])
    if cmdx==b'/set_dt':
        return handle_cmd_set_dt(cmd[pos+1:])
    if cmdx==b'/set_misc':
        return handle_cmd_set_misc(cmd[pos+1:])
    return None
