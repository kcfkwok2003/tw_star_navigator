import time
import sys

def clear_tdiff():
    tdiff = load_tdiff()
    if tdiff !=0:
        f=open('tdiff','w')
        f.write('0')
        f.close()

def get_time():
    tzone= load_tzone()
    tdiff = load_tdiff()
    tm = time.time() + tdiff + tzone*60*60
    return tm

def load_geo_cfg():
    try:
        from geo_cfg import lat,lon,drx
        return lat,lon,drx
    except Exception as e:
        sys.print_exception(e)
    lat=22.15  # for HK
    lon=114.15
    drx='E'
    save_geo_cfg(lat,lon,drx)
    return lat,lon,drx

def load_tdiff():
    tdiff=0
    try:
        f=open('tdiff')
        tdiff = int(f.read())
        f.close()
    except Exception as e:
        sys.print_exception(e)
        f=open('tdiff','w')
        f.write('0')
        f.close()
    return tdiff

def load_tzone():
    try:
        f=open('tzone.cfg')
        tz=f.read()
        f.close()
        return int(tz)
    except:
        tz=8  # for HONG KONG 
        save_tzone(tz)
        return tz

def save_geo_cfg(lat,lon,drx):
    ss='lat=%s\nlon=%s\ndrx="%s"\n' % (lat,lon,drx)
    f=open('geo_cfg.py','w')
    f.write(ss)
    f.close()
    if 'geo_cfg' in sys.modules:
        del sys.modules['geo_cfg']
    return 'OK'

def save_tdiff(tmx):
    tdiff = tmx -time.time()
    f=open('tdiff','w')
    f.write(str(tdiff))
    f.close()

def save_tzone(tz):
    f=open('tzone.cfg','w')
    f.write(str(tz))
    f.close()

BITMASK=[0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80]
def conv_mono_to_rgb565(bs,bg,fg):
    # bs is 16 x 16
    nbs =bytearray()
    rbs=bs[:]
    while rbs:
        for i in range(2):
            for j in range(8):
                if BITMASK[j] & rbs[i]:
                    nbs.append(fg >> 8)
                    nbs.append(fg & 0xff)
                else:
                    nbs.append(bg >> 8)
                    nbs.append(bg & 0xff)                        
        rbs=rbs[2:]
    return nbs

def conv_mono2_to_rgb565(bs,bg,fg):
    # bs is 12 x 12
    nbs =bytearray()
    rbs=bs[:]
    while rbs:
        for j in range(8):
            if BITMASK[j] & rbs[0]:
                nbs.append(fg >> 8)
                nbs.append(fg & 0xff)
            else:
                nbs.append(bg >> 8)
                nbs.append(bg & 0xff)
        for j in range(4):
            if BITMASK[j] & rbs[1]:
                nbs.append(fg >> 8)
                nbs.append(fg & 0xff)
            else:
                nbs.append(bg >> 8)
                nbs.append(bg & 0xff)                    
        rbs=rbs[2:]
    return nbs    
