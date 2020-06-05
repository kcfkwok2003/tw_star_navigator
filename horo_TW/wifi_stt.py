#wifi_stt.py
import sys
WIFI_STOP=0
WIFI_AP=1
WIFI_CONN=2

def save_wifi_state(stt):
    f=open('wifi_st','w')
    f.write('{}'.format(stt))
    f.close()

def get_wifi_state():
    try:
        f=open('wifi_st')
        st = int(f.read())
        f.close()
        return st
    except Exception as e:
        sys.print_exception(e)
    return WIFI_STOP
