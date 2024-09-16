#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/uuControl.o
import httplib
import urllib
import hashlib
import time
import subprocess
from Crypto.Cipher import AES
from callbackHelper import Functor
UU_IP = '127.0.0.1'
HttpServerWhisper = 'netease_uu_http_whisper'
GAME_STAMP_FORMAT = 'iamty_%d_ytmai'
EMBED_ID = '52b29af8d5a35cba55e2774a'
REAL_PORT = 0
UU_PORT = range(2013, 2023)
UU_STATUS = 0

def genAuthCodeKey(originalKey):
    md5 = ''
    binStr = hashlib.md5(originalKey).digest()
    index = (15, 0, 13, 2, 11, 4, 9, 6, 7, 8, 5, 10, 3, 12, 1, 14)
    for i in index:
        md5 += binStr[i]

    return md5


def strPad(s):
    BS = AES.block_size
    return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)


def strUnpad(s):
    return s[0:-ord(s[-1])]


def genNeteaseUUAuthCode():
    stamp = int(time.time() * 1000)
    content = GAME_STAMP_FORMAT % stamp
    key = genAuthCodeKey(HttpServerWhisper)
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = cipher.encrypt(strPad(content))
    encrypted = encrypted.encode('hex')
    return encrypted


def httpResponse(url):

    def fwrap(fn):

        def wrapper(*args, **kwargs):
            ip = UU_IP
            port = args[0]
            method, body, headers, callback = fn(*args, **kwargs)
            __request(ip, port, url, method, body, headers, callback)

        return wrapper

    return fwrap


def __request(ip, port, url, method, body, headers, callback):
    try:
        conn = httplib.HTTPConnection('%s:%d' % (ip, port), timeout=0.001)
        body = urllib.urlencode(body)
        conn.request(method, url, body, headers)
        r = conn.getresponse()
        if r.status == 200:
            content = r.read()
            callback(r.status, content)
        else:
            callback(r.status, '')
        conn.close()
    except:
        callback(0, '')


@httpResponse(' /get_status')
def getStatus(port, callback):
    method = 'GET'
    body = {}
    headers = {'NeteaseUU-Auth-Code': genNeteaseUUAuthCode()}
    return (method,
     body,
     headers,
     callback)


@httpResponse(' /get_external_ip')
def getExternalIP(port, callback):
    method = 'GET'
    body = {}
    headers = {'NeteaseUU-Auth-Code': genNeteaseUUAuthCode()}
    return (method,
     body,
     headers,
     callback)


@httpResponse(' /set_real_mobile')
def setRealMobile(port, id, isMobile, callback):
    method = 'POST'
    body = {'id': id,
     'mobile': isMobile}
    headers = {'NeteaseUU-Auth-Code': genNeteaseUUAuthCode()}
    return (method,
     body,
     headers,
     callback)


def excuteUU():
    cmd = 'uu\\UU.exe /auto_acc /embed_id ' + EMBED_ID
    return subprocess.Popen(cmd, close_fds=True, shell=True)


def getRealPort(port, status, content):
    global UU_STATUS
    global REAL_PORT
    if status == 200:
        REAL_PORT = port
        UU_STATUS = int(content)


def pollGetStatus():
    global UU_STATUS
    UU_STATUS = 0
    for port in UU_PORT:
        if REAL_PORT:
            break
        getStatus(port, Functor(getRealPort, port))
