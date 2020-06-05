# httpd_util.py
version="1.0"

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
