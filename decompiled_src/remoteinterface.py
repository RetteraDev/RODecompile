#Embedded file name: /WORKSPACE/data/entities/client/helpers/remoteinterface.o
import re
import httplib
import urllib
import urllib2
import time
import socket
import random
import win32dns
import os
import json
import BigWorld
import pyBgTask
import utils
import const
import gameglobal
import gametypes
import gamelog
from helpers import seqTask
from helpers import httpHelper
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SYSD
from callbackHelper import Functor
ECARD_PLATFORM = 'ty'

def unicode2gbkDict(dct, encoding = 'gbk'):
    newDct = {}
    if isinstance(dct, dict):
        for k, v in dct.items():
            if isinstance(k, unicode):
                try:
                    k = k.encode(encoding)
                except:
                    pass

            elif isinstance(k, tuple):
                k = unicode2gbkArray(k)
            if isinstance(v, unicode):
                try:
                    v = v.encode(encoding)
                except:
                    pass

            elif isinstance(v, dict):
                v = unicode2gbkDict(v)
            elif isinstance(v, tuple) or isinstance(v, list):
                v = unicode2gbkArray(v)
            newDct[k] = v

    return newDct


def unicode2gbkArray(arr, encoding = 'gbk'):
    newArr = []
    if isinstance(arr, tuple) or isinstance(arr, list):
        for v in arr:
            if isinstance(v, unicode):
                try:
                    v = v.encode(encoding)
                except:
                    pass

            elif isinstance(v, dict):
                v = unicode2gbkDict(v)
            elif isinstance(v, tuple) or isinstance(v, list):
                v = unicode2gbkArray(v)
            newArr.append(v)

    if isinstance(arr, tuple):
        return tuple(newArr)
    if isinstance(arr, list):
        return list(newArr)
    return newArr


def _jsonEncoderHook(dct):
    if isinstance(dct, dict):
        dct = unicode2gbkDict(dct)
    return dct


def __getNetKey(callback):
    try:
        conn = httplib.HTTPConnection('string.xy.163.com:22330')
        conn.request('GET', '/strxy/whoami')
        r = conn.getresponse()
        if r.status != 200:
            callback('')
            return
        data = r.read()
        conn.close()
        if len(data) == 0:
            callback('')
            return
        callback(data)
        return
    except:
        callback('')
        return


def getNetKey(callback):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__getNetKey, (mgr.make_callback(callback),))


def getServerStatus(callback):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__getServerStatus, (mgr.make_callback(callback),))


def __getServerStatus(callback):
    try:
        if BigWorld.isPublishedVersion():
            conn = httplib.HTTPConnection('42.186.107.200:27181')
            conn.request('GET', '/queryallserverstatus')
        else:
            conn = httplib.HTTPConnection('pgpp-util02.i.nease.net:9001')
            conn.request('GET', '/reserve/queryallserverstatus')
        r = conn.getresponse()
        if r.status != 200:
            callback('')
            return
        data = r.read()
        conn.close()
        if len(data) == 0:
            callback('')
            return
        callback(data)
        return
    except:
        callback('')
        return


def _getSpriteAutoHotWordsByPrefix(prefix, callback):
    headers = {'Content-type': 'application/x-www-form-urlencoded',
     'Accept': 'text/plain'}
    try:
        conn = httplib.HTTPConnection('tip.chatbot.nie.163.com')
        path = '/cgi-bin/good_evaluate_question_tip.py?game=37&prefix=%s&max_num=30&enc=gbk&renc=gbk' % prefix
        conn.request('GET', path, '', headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        callback(prefix, data)
        return
    except:
        callback(prefix, None)
        return


def getSpriteAutoHotWordsByPrefix(prefix, callback):
    try:
        mgr = pyBgTask.getMgr()
        if mgr:
            mgr.add_task(_getSpriteAutoHotWordsByPrefix, (prefix, mgr.make_callback(callback)))
    except:
        callback(prefix, None)


def __quickEvaluateSprite(vipgrade, pid, name, urs, plv, host, school, birthday, tOn, tOff, spaceName, isSecondClick, gameid, question, answer, evaluate, isTopClick, callback):
    p = {'remarks': 'hostnum=%s,gbId=%s,name=%s,urs=%s,grade=%d,VIP=%d,faction=%s,birthday=%s,online_time=%d,lastQuit=%s,thelogintime=%s,iz=%s,click=%d,isTopClick=%d,new=%d' % (host,
                 pid,
                 name,
                 urs,
                 plv,
                 vipgrade,
                 school,
                 birthday,
                 utils.getNow() - tOn,
                 time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tOff)),
                 time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tOn)),
                 spaceName,
                 isSecondClick,
                 isTopClick,
                 plv <= 30),
     'gameid': '%d' % gameid,
     'question': question,
     'answer': answer,
     'evaluate': '%d' % evaluate}
    params = urllib.urlencode(p)
    headers = {'Content-type': 'application/x-www-form-urlencoded',
     'Accept': 'text/plain'}
    try:
        conn = httplib.HTTPConnection('chatbot.nie.163.com:8080')
        conn.request('POST', '/cgi-bin/save_evaluate.py', params, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        callback(data, evaluate)
        return
    except:
        callback('·þÎñÆ÷Á´½ÓÊ§°Ü', evaluate)
        return


def evaluateSprite(vipgrade, pid, name, urs, plv, host, school, birthday, tOn, tOff, spaceName, isSecondClick, gameid, quest, answer, evaluate, isTopClick, callback):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__quickEvaluateSprite, (vipgrade,
     pid,
     name,
     urs,
     plv,
     host,
     school,
     birthday,
     tOn,
     tOff,
     spaceName,
     isSecondClick,
     gameid,
     quest,
     answer,
     evaluate,
     isTopClick,
     mgr.make_callback(callback)))


def uploadFileToNos(md5, timeStamp, imagePath, fileType, fileSrc, extra, callback):
    try:
        player = BigWorld.player()
        ip = gameglobal.rds.configSect.readString('nos/ip')
        port = gameglobal.rds.configSect.readInt('nos/port')
        if fileSrc == gametypes.NOS_FILE_SRC_CAMERA_SHARE:
            ext = os.path.splitext(imagePath)[1]
        else:
            ext = ''
        url = '/NosService?md5=' + str(md5) + '&gbId=' + str(getattr(player, 'gbId', 0) or player.playerName + imagePath) + '&timeStamp=' + str(timeStamp) + '&ext=' + ext
        gamelog.info('@szh uploadFileToNos imagepath=%s' % imagePath)
        BigWorld.httpUploadFile(ip, port, url, imagePath, Functor(nosUploadCallback, fileType, fileSrc, extra, callback))
    except Exception as e:
        print e
        nosUploadCallback(fileType, fileSrc, extra, callback, '')


def downloadFileFromNos(directory, key, fileType, status, callback):
    if fileType == gametypes.NOS_FILE_MP3:
        path = const.AUDIOS_DOWNLOAD_DIR + '\\' + key + '.mp3'
        BigWorld.ayncFileExist(path, Functor(_downloadAudioFileAfterLocalCheck, directory, key, fileType, True, callback))
    elif status == gametypes.NOS_FILE_STATUS_SERVER_APPROVED:
        path = const.IMAGES_DOWNLOAD_DIR + '\\' + key + '.dds'
        BigWorld.ayncFileExist(path, Functor(_downloadFileAfterLocalCheck, directory, key, fileType, True, callback))
    elif status == gametypes.NOS_FILE_STATUS_DOWNLOAD_DIRECTLY:
        path = const.IMAGES_DOWNLOAD_DIR + '\\' + key + '.dds'
        BigWorld.ayncFileExist(path, Functor(_downloadFileAfterLocalCheck, directory, key, fileType, False, callback))


def _downloadFileAfterLocalCheck(directory, key, fileType, flushCache, callback, isExist):
    if not isExist:
        if gameglobal.rds.configData.get('enableNOSCDNDeploy', False) and hasattr(BigWorld, 'httpDownloadFileNew'):
            host = gameglobal.rds.configSect.readString('nos/host', 'nos.netease.com')
            port = 80
            url = '/' + key
            url = urllib.quote(url)
            if fileType == gametypes.NOS_FILE_PICTURE:
                fileName = key + '.dds'
            else:
                fileName = key
            BigWorld.httpDownloadFileNew(host, port, url, directory, fileName, Functor(nosDownloadCallback, callback, key, fileType, flushCache))
        else:
            host = gameglobal.rds.configSect.readString('nos/host', '') if utils.isInternationalVersion() else 'nos.netease.com'
            port = 80
            account = gameglobal.rds.configSect.readString('nos/account')
            url = '/' + account + '/' + key
            url = urllib.quote(url)
            if fileType == gametypes.NOS_FILE_PICTURE:
                fileName = key + '.dds'
            else:
                fileName = key
            BigWorld.httpDownloadFile(host, port, url, directory, fileName, Functor(nosDownloadCallback, callback, key, fileType, flushCache))
    else:
        nosDownloadCallback(callback, key, fileType, flushCache, 1)


def _downloadAudioFileAfterLocalCheck(directory, key, fileType, flushCache, callback, isExist):
    if not isExist:
        host = 'nos.netease.com'
        port = 80
        try:
            prefix = key.split('_')[0]
        except:
            prefix = 'test-tianyu-pc'

        url = '/%s/%s?audioTrans&type=mp3&ar=44100' % (prefix, key)
        fileName = key + '.mp3'
        gamelog.debug('bgf@_downloadAudioFileAfterLocalCheck', host, port, url, directory, fileName)
        BigWorld.httpDownloadFile(host, port, url, directory, fileName, Functor(nosDownloadCallback, callback, key, fileType, flushCache))
    else:
        nosDownloadCallback(callback, key, fileType, flushCache, 1)


def nosUploadCallback(fileType, fileSrc, extra, callback, feedback):
    gamelog.info('@szh nosUploadCallback, feedback=%s' % str(feedback))
    method, callbackArgs = callback
    pat = re.compile('<!(\\d+):(\\S+)>')
    keys = pat.findall(feedback)
    player = BigWorld.player()
    if not player or not player.inWorld:
        return
    if len(keys) > 0:
        ret, key = int(keys[0][0]), keys[0][1]
        if ret == gametypes.NOS_UPLOAD_RET_SUC:
            if gameglobal.rds.GameState > gametypes.GS_LOGIN:
                player.base.onSucUploadFile(key, fileType, fileSrc, str(extra))
        elif ret == gametypes.NOS_UPLOAD_RET_AUTHFAIL:
            key = None
            if gameglobal.rds.GameState > gametypes.GS_LOGIN:
                player.reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_SCRIPT, ['@szh: nos authorization failed'], 0, {})
        elif ret == gametypes.NOS_UPLOAD_RET_FATAL_ERROR:
            key = None
            if gameglobal.rds.GameState > gametypes.GS_LOGIN:
                player.reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_SCRIPT, ['@szh: nos failed due to tomcat abort!'], 0, {})
        elif ret == gametypes.NOS_UPLOAD_RET_ARGS_INVALID:
            key = None
            if gameglobal.rds.GameState > gametypes.GS_LOGIN:
                player.reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_SCRIPT, ['@szh: nos failed due to invalid args!'], 0, {})
        elif ret == gametypes.NOS_UPLOAD_RET_NOS_INVALID:
            key = None
            if gameglobal.rds.GameState > gametypes.GS_LOGIN:
                player.reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_SCRIPT, ['@szh: nos failed due to nos service abort!'], 0, {})
    else:
        key = None
    if method is not None:
        method(key, *callbackArgs)


def nosDownloadCallback(callback, key, fileType, flushCache, feedback):
    gamelog.info('@szh nosDownloadCallback, feedback=%s' % str(feedback))
    seqTask.gNOSDownloadTaskMgr.onTaskDone()
    if feedback:
        status = gametypes.NOS_FILE_STATUS_APPROVED
    else:
        status = gametypes.NOS_FILE_STATUS_DOWNLOAD_FAIL
    player = BigWorld.player()
    if player is None:
        return
    if flushCache:
        if player.nosFileStatusCache.has_key(key):
            extra = player.nosFileStatusCache[key][2]
        else:
            extra = {}
        player.nosFileStatusCache[key] = (status, fileType, extra)
    method, callbackArgs = callback
    if method is not None:
        method(status, *callbackArgs)


def getYixinFilePath(account, urlPath):
    return const.IMAGES_DOWNLOAD_DIR + '\\' + account + '\\' + urlPath.replace('?', '')


def downloadFileFromYixin(account, urlPath, callback):
    path = getYixinFilePath(account, urlPath)
    BigWorld.ayncFileExist(path, Functor(_downloadYixinFile, account, urlPath, callback))


def _downloadYixinFile(account, urlPath, callback, isExist):
    if not isExist:
        ip = 'nos.netease.com'
        port = 80
        url = '/' + account + '/' + urlPath
        directory = const.IMAGES_DOWNLOAD_DIR
        fileName = urlPath.replace('?', '')
        gamelog.info('@szh _downloadYixinFile, file not exist', account, urlPath)
        BigWorld.httpDownloadFile(ip, port, url, directory, fileName, Functor(yixinDownloadCallback, callback))
    else:
        yixinDownloadCallback(callback, gametypes.YIXIN_DOWNLOAD_SUC)


def yixinDownloadCallback(callback, feedback):
    gamelog.info('@szh yixinDownloadCallback, feedback=%s' % str(feedback))
    seqTask.gYixinTaskMgr.onTaskDone()
    if feedback:
        status = gametypes.YIXIN_DOWNLOAD_SUC
    else:
        status = gametypes.YIXIN_DOWNLOAD_FAIL
    method, callbackArgs = callback
    if method is not None:
        method(status, *callbackArgs)


def getServerList(serverListUrl, callback):
    try:
        protocol, rest = urllib.splittype(serverListUrl)
        host, rest = urllib.splithost(rest)
        conn = httplib.HTTPConnection(host)
        conn.request('GET', rest)
        r = conn.getresponse()
        if r.status != 200:
            callback('')
            return
        data = r.read()
        conn.close()
        if len(data) == 0:
            callback('')
            return
        callback(data)
        return
    except:
        callback('')
        return


def __getChargeUrl(callback, useName, pwd, amount):
    try:
        url = 'ecard.163.com'
        parth = '/script/bill_interface/get_url/?'
        ip = socket.gethostbyname(socket.gethostname())
        m = {'platform': ECARD_PLATFORM,
         'reason': 1,
         'user_name': useName,
         'pwd': pwd,
         'product_type': 100,
         'amount': amount,
         'ip': ip,
         'mode': 1}
        params = urllib.urlencode(m)
        parth += params
        conn = httplib.HTTPSConnection(url)
        conn.request('GET', parth)
        r = conn.getresponse()
        if r.status != 200:
            callback(1, '')
            return
        content = r.read()
        conn.close()
        if content.isdigit():
            callback(int(content), '')
            return
        callback(0, content)
        return
    except:
        callback(1, '')
        return


def getChargeUrl(useName, pwd, amount, callback):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__getChargeUrl, (mgr.make_callback(callback),
     useName,
     pwd,
     amount))


def onGetChargeUrl(opCode, url):
    p = BigWorld.player()
    if opCode != 0:
        if opCode == 101:
            p.showGameMsg(GMDD.data.COMMON_MSG, ('\xcf\xb5\xcd\xb3\xb4\xed\xce\xf3',))
        elif opCode == 102:
            p.showGameMsg(GMDD.data.COMMON_MSG, ('\xb8\xc3\xb3\xe4\xd6\xb5\xc0\xe0\xd0\xcd\xd4\xdd\xcd\xa3\xb7\xfe\xce\xf1',))
        elif opCode == 103:
            p.showGameMsg(GMDD.data.COMMON_MSG, ('\xb8\xc3\xb5\xe3\xbf\xa8\xc0\xe0\xd0\xcd\xd4\xdd\xcd\xa3\xb7\xfe\xce\xf1',))
        elif opCode == 104:
            p.showGameMsg(GMDD.data.COMMON_MSG, ('\xb5\xc7\xc2\xbc\xca\xa7\xb0\xdc\xa3\xa8\xd5\xca\xba\xc5/\xc3\xdc\xc2\xeb\xd3\xd0\xce\xf3\xa3\xa9',))
        else:
            p.showGameMsg(GMDD.data.COMMON_MSG, ('\xb2\xce\xca\xfd\xd3\xd0\xce\xf3',))
        return
    if not url:
        return
    BigWorld.openUrl(url)


def _getQRCodePng(idString, callback):
    p = {'uuid': idString,
     'size': 136,
     'format': 'png'}
    params = urllib.urlencode(p)
    try:
        url = 'reg.163.com'
        conn = httplib.HTTPConnection(url)
        conn.request('GET', '/services/getqrcode?' + params)
        r = conn.getresponse()
        if r.status != 200:
            callback(None)
            return
        data = r.read()
        conn.close()
        if not data or len(data) == 0:
            callback(None)
            return
        callback(data)
        return
    except:
        callback(None)
        return


def getQRCodePng(idString, callback):
    mgr = pyBgTask.getMgr()
    mgr.add_task(_getQRCodePng, (idString, mgr.make_callback(callback)))


def __quickPayFillOrder(callback, useName, amount, fillTime, signature):
    try:
        url = 'ecard.163.com'
        parth = '/script/game_quick_pay/fill_order_with_sign?'
        m = {'platform': ECARD_PLATFORM,
         'user_name': useName,
         'reason': 1,
         'amount': amount,
         'fill_time': fillTime,
         'signature': signature}
        params = urllib.urlencode(m)
        parth += params
        conn = httplib.HTTPConnection(url)
        conn.request('POST', parth)
        r = conn.getresponse()
        if r.status != 200:
            callback(r.status, {})
            return
        content = r.read()
        conn.close()
        callback(r.status, eval(content))
        return
    except:
        callback(1, {})
        return


def quickPayFillOrder(useName, amount, fillTime, signature, callback):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__quickPayFillOrder, (mgr.make_callback(callback),
     useName,
     amount,
     fillTime,
     signature))


def __newQuickPayFillOrder(callback, useName, amount, fillTime, signature, payType):
    try:
        url = 'ecard.163.com'
        parth = '/script/game_quick_pay/fill_order_with_sign?'
        m = {'platform': ECARD_PLATFORM,
         'user_name': useName,
         'reason': 1,
         'amount': amount,
         'fill_time': fillTime,
         'signature': signature}
        params = urllib.urlencode(m)
        parth += params
        conn = httplib.HTTPConnection(url)
        conn.request('POST', parth)
        r = conn.getresponse()
        if r.status != 200:
            callback(r.status, {}, payType)
            return
        content = r.read()
        conn.close()
        callback(r.status, eval(content), payType)
        return
    except:
        callback(1, {}, payType)
        return


def newQuickPayFillOrder(useName, amount, fillTime, signature, callback, payType = ''):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__newQuickPayFillOrder, (mgr.make_callback(callback),
     useName,
     amount,
     fillTime,
     signature,
     payType))


def __getAliPayQrcodeData(callback, useName, amount, signature):
    try:
        url = 'ecard.163.com'
        parth = '/script/game_quick_pay/show_alipay_qrcode?'
        m = {'platform': ECARD_PLATFORM,
         'user_name': useName,
         'reason': 1,
         'amount': amount,
         'signature': signature}
        params = urllib.urlencode(m)
        parth += params
        conn = httplib.HTTPConnection(url)
        conn.request('POST', parth)
        r = conn.getresponse()
        if r.status != 200:
            callback(r.status, {})
            return
        content = r.read()
        conn.close()
        callback(r.status, json.loads(content, object_hook=_jsonEncoderHook))
        return
    except:
        callback(1, {})
        return


def getAliPayQrcodeData(useName, amount, signature, callback):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__getAliPayQrcodeData, (mgr.make_callback(callback),
     useName,
     amount,
     signature))


def __queryAliPayBill(callback, useName, beginTime, endTime, signature):
    try:
        url = 'ecard.163.com'
        parth = '/script/interface/query_urs_bills?'
        m = {'platform': ECARD_PLATFORM,
         'begin_time': beginTime,
         'end_time': endTime,
         'urs': useName,
         'signature': signature}
        params = urllib.urlencode(m)
        parth += params
        conn = httplib.HTTPConnection(url)
        conn.request('GET', parth)
        r = conn.getresponse()
        if r.status != 200:
            callback(r.status, {})
            return
        content = r.read()
        conn.close()
        callback(r.status, json.loads(content, object_hook=_jsonEncoderHook))
        return
    except:
        callback(1, {})
        return


def queryAliPayBill(useName, beginTime, endTime, signature, callback):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__queryAliPayBill, (mgr.make_callback(callback),
     useName,
     beginTime,
     endTime,
     signature))


def __getAliPayQrcode(callback, url):
    try:
        r = urllib2.urlopen(url)
        content = r.read()
        r.close()
        callback(200, content)
        return
    except:
        callback(1, {})
        return


def saveAliPayQrcode(fileName, callback, res):
    try:
        f = open(const.IMAGES_DOWNLOAD_DIR + '/' + fileName + '.png', 'wb')
        f.write(res)
    finally:
        f.close()

    BigWorld.convert2DXT5(const.IMAGES_DOWNLOAD_DIR + '/' + fileName + '.png', const.IMAGES_DOWNLOAD_DIR)
    path = const.IMAGES_DOWNLOAD_DIR + '/' + fileName + '.dds'
    downloadAliPayQrcodeCallback(path, callback)


def downloadAliPayQrcodeCallback(path, callback):
    if callback:
        BigWorld.callback(0, Functor(callback, path))


def getAliPayQrcode(url, callback):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__getAliPayQrcode, (mgr.make_callback(callback), url))


def __getWeChatPayQrcode(callback, useName, amount, signature):
    try:
        url = 'ecard.163.com'
        parth = '/script/game_quick_pay/show_weixin_qrcode?'
        m = {'platform': ECARD_PLATFORM,
         'user_name': useName,
         'reason': 1,
         'amount': amount,
         'signature': signature}
        params = urllib.urlencode(m)
        parth += params
        conn = httplib.HTTPConnection(url)
        conn.request('POST', parth)
        r = conn.getresponse()
        if r.status != 200:
            callback(r.status, {})
            return
        content = r.read()
        conn.close()
        callback(r.status, json.loads(content, object_hook=_jsonEncoderHook))
        return
    except:
        callback(1, {})
        return


def getWeChatPayQrcode(useName, amount, signature, callback):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__getWeChatPayQrcode, (mgr.make_callback(callback),
     useName,
     amount,
     signature))


def __queryWeChatPay(callback, useName, bill_id, signature):
    try:
        url = 'ecard.163.com'
        parth = '/script/interface/query_urs_bill?'
        m = {'platform': ECARD_PLATFORM,
         'bill_id': bill_id,
         'urs': useName,
         'encode': 'gbk',
         'signature': signature}
        params = urllib.urlencode(m)
        parth += params
        conn = httplib.HTTPSConnection(url)
        conn.request('GET', parth)
        r = conn.getresponse()
        if r.status != 200:
            callback(r.status, {})
            return
        content = r.read()
        conn.close()
        callback(r.status, json.loads(content, object_hook=_jsonEncoderHook))
        return
    except:
        callback(1, {})
        return


def queryWeChatPay(useName, bill_id, signature, callback):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__queryWeChatPay, (mgr.make_callback(callback),
     useName,
     bill_id,
     signature))


def __queryJiangjunlingPay(callback, useName, uuid, signature):
    try:
        url = 'm.mkey.netease.com'
        parth = '/api/manage/get_ecard_qrcode_message_client?'
        m = {'uuid': uuid,
         'pid': ECARD_PLATFORM,
         'urs': useName,
         'sign': signature}
        gamelog.debug('@zq __queryJiangjunlingPay', m)
        params = urllib.urlencode(m)
        parth += params
        conn = httplib.HTTPConnection(url)
        conn.request('GET', parth)
        r = conn.getresponse()
        if r.status != 200:
            callback(r.status, {})
            return
        content = r.read()
        conn.close()
        callback(r.status, json.loads(content, object_hook=_jsonEncoderHook))
        return
    except:
        callback(1, {})
        return


def queryJiangjunlingPay(useName, uuid, signature, callback):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__queryJiangjunlingPay, (mgr.make_callback(callback),
     useName,
     uuid,
     signature))


def __quickPaySendAuthCode(callback, sessionId, billId, interfaceType, quickPayId):
    try:
        url = 'ecard.163.com'
        parth = '/script/game_quick_pay/send_auth_sms?'
        m = {'platform': ECARD_PLATFORM,
         'sid': sessionId,
         'bill_id': billId,
         'interfaceType': interfaceType}
        if interfaceType == 4:
            m['quickPayId'] = quickPayId
        params = urllib.urlencode(m)
        parth += params
        conn = httplib.HTTPConnection(url)
        conn.request('POST', parth)
        r = conn.getresponse()
        if r.status != 200:
            callback(r.status, {})
            return
        content = r.read()
        conn.close()
        callback(r.status, eval(content))
        return
    except:
        callback(1, {})
        return


def quickPaySendAuthCode(sessionId, billId, interfaceType, quickPayId, callback):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__quickPaySendAuthCode, (mgr.make_callback(callback),
     sessionId,
     billId,
     interfaceType,
     quickPayId))


def __quichPayCompleteBalancePay(callback, sessionId, billId, authCode):
    try:
        url = 'ecard.163.com'
        parth = '/script/game_quick_pay/complete_balance_pay?'
        m = {'platform': ECARD_PLATFORM,
         'sid': sessionId,
         'bill_id': billId,
         'mobileAuthCode': authCode}
        params = urllib.urlencode(m)
        parth += params
        conn = httplib.HTTPConnection(url)
        conn.request('POST', parth)
        r = conn.getresponse()
        if r.status != 200:
            callback(r.status, {})
            return
        content = r.read()
        conn.close()
        callback(r.status, eval(content))
        return
    except:
        callback(1, {})
        return


def quichPayCompleteBalancePay(sessionId, billId, authCode, callback):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__quichPayCompleteBalancePay, (mgr.make_callback(callback),
     sessionId,
     billId,
     authCode))


def __quickPayCompleteQuickPay(callback, sessionId, billId, authCode, quickPayId, bankCode, chargeId, oriMerchSeq):
    try:
        url = 'ecard.163.com'
        parth = '/script/game_quick_pay/complete_quick_pay?'
        m = {'platform': ECARD_PLATFORM,
         'sid': sessionId,
         'bill_id': billId,
         'mobileAuthCode': authCode,
         'quickPayId': quickPayId,
         'bankCode': bankCode,
         'chargeId': chargeId,
         'oriMerchSeq': oriMerchSeq}
        params = urllib.urlencode(m)
        parth += params
        conn = httplib.HTTPConnection(url)
        conn.request('POST', parth)
        r = conn.getresponse()
        if r.status != 200:
            callback(r.status, {})
            return
        content = r.read()
        conn.close()
        callback(r.status, eval(content))
        return
    except:
        callback(1, {})
        return


def quickPayCompleteQuickPay(sessionId, billId, authCode, quickPayId, bankCode, chargeId, oriMerchSeq, callback):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__quickPayCompleteQuickPay, (mgr.make_callback(callback),
     sessionId,
     billId,
     authCode,
     quickPayId,
     bankCode,
     chargeId,
     oriMerchSeq))


def redirectWangYiBaoToPay(sessionId, billId, alipay = False):
    url = 'https://ecard.163.com/script/game_quick_pay/redirect_to_repay?'
    m = {'platform': ECARD_PLATFORM,
     'sid': sessionId,
     'bill_id': billId}
    if not gameglobal.rds.ui.easyPay.alipayConfig():
        alipay = False
    if alipay:
        m['gate_type'] = 'alipay'
    params = urllib.urlencode(m)
    url += params
    p = BigWorld.player()
    if p:
        p.autoLoginUrl = url
        p.base.exchangeTicketByCookie()
    else:
        BigWorld.openUrl(url)


def redirectWangYiBaoToRegisterqp(sessionId, orderId):
    url = 'https://ecard.163.com/script/game_quick_pay/redirect_to_registerqp?'
    m = {'platform': ECARD_PLATFORM,
     'sid': sessionId,
     'orderId': orderId}
    params = urllib.urlencode(m)
    url += params
    p = BigWorld.player()
    if p:
        p.autoLoginUrl = url
        p.base.exchangeTicketByCookie()
    else:
        BigWorld.openUrl(url)


gIPCache = None
gDNSCache = None

def getIP():
    global gIPCache
    if gIPCache != None:
        return gIPCache
    ip = '127.0.0.1'
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except:
        if not BigWorld.isPublishedVersion():
            import traceback
            traceback.print_exc()

    gIPCache = ip
    return ip


def getDNS():
    global gDNSCache
    if gDNSCache != None:
        return gDNSCache
    dnsIP = '0.0.0.0'
    try:
        dnsIP = win32dns.RegistryResolve()[0]
    except:
        if not BigWorld.isPublishedVersion():
            import traceback
            traceback.print_exc()

    gDNSCache = dnsIP
    return dnsIP


def __doStatSend(delay, clip, sip, gid, nettype):
    p = {'time': '%f' % int(delay * 1000),
     'clip': clip,
     'dns': getDNS(),
     'sip': sip,
     'gid': gid,
     'nettype': '%d' % nettype,
     'timestamp': '%f' % int(time.time())}
    gamelog.info('jjh@latency: stat param ', p)
    params = urllib.urlencode(p)
    try:
        conn = httplib.HTTPConnection('pg.netaly.nie.163.com')
        conn.request('GET', '/query?' + params)
        r = conn.getresponse()
        if r.status != 200:
            gamelog.info('jjh@latency: stat send not success', r.status)
            return
        data = r.read()
        conn.close()
        gamelog.info('jjh@latency: ret ', r.status, data)
        return data
    except:
        if not BigWorld.isPublishedVersion():
            import traceback
            traceback.print_exc()
        return


gServerid = None
gStarted = False
gLastid = None
tInterval = 60

def __actualSend():
    global gServerid
    mgr = pyBgTask.getMgr()
    delay = BigWorld.LatencyInfo().value.w
    clip = getIP()
    sip = gameglobal.rds.loginManager.hostIP()
    gid = gServerid
    nettype = gameglobal.rds.loginManager.realVendor()
    mgr.add_task(__doStatSend, (delay,
     clip,
     sip,
     gid,
     nettype))


def __doSend():
    global gLastid
    global tInterval
    if gServerid != None:
        __actualSend()
    next = 5 * tInterval
    if gLastid != gServerid:
        next = random.uniform(4, 6) * tInterval
        gLastid = gServerid
    BigWorld.callback(next, __doSend)


def getServerId():
    return gServerid


def statisticSend(gid):
    global gStarted
    global gLastid
    global gServerid
    gServerid = gid
    if gid == None:
        gLastid = None
    if not gStarted:
        gStarted = True
        BigWorld.callback(random.uniform(1, 2) * tInterval, __doSend)


def getMicCardPath(urlPath):
    index = urlPath.rfind('/')
    if index:
        return const.IMAGES_DOWNLOAD_DIR + '\\' + urlPath[index + 1:]


def downloadMicCardFromCC(urlPath, callback = None):
    path = getMicCardPath(urlPath)
    if path:
        BigWorld.ayncFileExist(path, Functor(_downloadMicCard, urlPath, callback))


def _downloadMicCard(urlPath, callback, isExist):
    index = urlPath.rfind('/')
    fileName = urlPath[index + 1:]
    if not isExist:
        try:
            fd = urllib.urlopen(urlPath)
            res = fd.read()
            fd.close()
            if res:
                BigWorld.callback(0, Functor(saveMicCard, fileName, callback, res))
        except:
            res = ''

    else:
        downloadMicCardCallback(fileName, callback)


def saveMicCard(fileName, callback, res):
    try:
        f = open('images/%s' % fileName, 'wb')
        f.write(res)
    finally:
        f.close()

    downloadMicCardCallback(fileName, callback)


def downloadMicCardCallback(fileName, callback):
    if callback:
        BigWorld.callback(0, Functor(callback, fileName))


def _getMicCardInfo(channeld, callback):
    try:
        conn = httplib.HTTPConnection('cc.163.com')
        path = '/live/game_miccard/?channelid=%d' % channeld
        conn.request('GET', path, '', {})
        response = conn.getresponse()
        gamelog.debug('getMicCardInfo', response.status, channeld)
        if response.status == 200:
            data = response.read()
            callback(data)
        else:
            callback(None)
        conn.close()
    except:
        callback(None)


def getMicCardInfo(channeld, callback):
    mgr = pyBgTask.getMgr()
    mgr.add_task(_getMicCardInfo, (channeld, mgr.make_callback(callback)))


def queryRemotePicVersion(remoteKey, callback):
    mgr = pyBgTask.getMgr()
    mgr.add_task(_queryRemotePicVersion, (remoteKey, mgr.make_callback(callback)))


def _queryRemotePicVersion(remoteKey, callback):
    try:
        url = 'hd.tianyu.163.com'
        path = '/points/getPhotoUrl.json?key=' + remoteKey
        conn = httplib.HTTPConnection(url)
        conn.request('GET', path, '', {})
        r = conn.getresponse()
        if r.status != 200:
            callback(r.status, {})
            return
        content = r.read()
        conn.close()
        callback(r.status, eval(content))
        return
    except:
        callback(1, {})
        return


def soundHttpReturn(fileType, filePathOrkey, extra, callback, ret):
    gamelog.debug('bgf@soundHttpReturn', fileType, filePathOrkey, len(ret), ret)
    if not ret:
        return
    if ret.find('200 OK') == -1:
        return
    index = ret.find('\r\n\r\n')
    if index == -1:
        return
    ret = ret[index + 4:]
    index = ret.find('\n')
    status = ret[:index]
    content = ret[index + 1:]
    status = int(status)
    player = BigWorld.player()
    if status != gametypes.SOUND_FILE_RET_SUCCESS:
        player.reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_SCRIPT, [content], 0, {})
        return
    method, args = callback
    if fileType == gametypes.SOUND_FILE_DOWNLOAD:
        if not os.path.exists(const.SOUND_DOWNLOAD_RELATIVE_DIR):
            os.mkdir(const.SOUND_DOWNLOAD_RELATIVE_DIR)
        with open('%s/%s.amr' % (const.SOUND_DOWNLOAD_RELATIVE_DIR, filePathOrkey), 'wb') as f:
            f.writelines(content)
        if method:
            method(filePathOrkey, *args)
    elif method:
        method(filePathOrkey, content, *args)


def uploadSound(fileType, filePath, extra, callback):
    try:
        data = ''
        try:
            with open('%s/%s' % (const.SOUND_DOWNLOAD_RELATIVE_DIR, filePath), 'rb') as file:
                data = file.read()
        except:
            soundHttpReturn(fileType, filePath, extra, callback, '')
            return

        p = BigWorld.player()
        ins = httpHelper.HttpMessage('POST', {'md5': 0,
         'host': utils.getHostId(),
         'tousers': '_1_',
         'usernum': str(p.gbId)[-6:]}, {'User-Agent': 'pg',
         'Content-Type': 'multipart/form-data',
         'Connection': 'close'}, data, {'name': 'upload',
         'filename': filePath}, 'voice.x.netease.com', 8020, '/pg/upload?')
        ins.build()
        BigWorld.httpUploadFile(ins.address, ins.port, ins.url, '%s/%s' % (const.SOUND_DOWNLOAD_DIR, filePath), Functor(soundHttpReturn, fileType, filePath, extra, callback), ins.messageHeader, ins.bodyPrefix, ins.endBoundary)
    except Exception as e:
        soundHttpReturn(fileType, filePath, extra, callback, '')


def getTranslation(fileType, key, extra, callback):
    gamelog.debug('bgf@getTranslation', fileType, key, extra, callback)
    try:
        ins = httpHelper.HttpMessage('GET', {'key': key}, {'User-Agent': 'pg',
         'Connection': 'close'}, '', {}, 'voice.x.netease.com', 8020, '/pg/get_translation?')
        ins.build()
        BigWorld.httpDownloadToMem(ins.address, ins.port, ins.url, Functor(soundHttpReturn, fileType, key, extra, callback), ins.messageHeader)
    except Exception as e:
        soundHttpReturn(fileType, key, extra, callback, '')


def downloadSound(fileType, key, extra, callback):
    path = '%s/%s.amr' % (const.SOUND_DOWNLOAD_DIR, key)
    gamelog.debug('bgf@downloadSound', fileType, path)
    BigWorld.ayncFileExist(path, Functor(_downloadSound, fileType, key, extra, callback))


def _downloadSound(fileType, key, extra, callback, exist):
    gamelog.debug('bgf@_downloadSound', exist, fileType, key)
    if not exist:
        try:
            p = BigWorld.player()
            ins = httpHelper.HttpMessage('GET', {'key': key,
             'host': '1234',
             'usernum': '5678'}, {'User-Agent': 'pg',
             'Connection': 'close'}, '', {}, 'voice.x.netease.com', 8020, '/pg/getfile?')
            ins.build()
            BigWorld.httpDownloadToMem(ins.address, ins.port, ins.url, Functor(soundHttpReturn, fileType, key, extra, callback), ins.messageHeader)
        except Exception as e:
            soundHttpReturn(fileType, key, extra, callback, '')

    else:
        method, args = callback
        if method:
            method(key, *args)


def getNeteaseVipAdInfo(adPos, callback):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__getNetEaseAppVipAdInfo, (adPos, mgr.make_callback(callback)))


def __getNetEaseAppVipAdInfo(AdPos, callback):
    try:
        url = 'a.game.163.com'
        parth = '/fz/interface/frontend/fz.do?'
        m = {'pos': AdPos}
        params = urllib.urlencode(m)
        parth += params
        conn = httplib.HTTPSConnection(url)
        conn.request('GET', parth)
        r = conn.getresponse()
        if r.status != 200:
            callback(1, {})
            return
        content = r.read()
        conn.close()
        retData = json.loads(content)
        callback(0, retData)
        return
    except:
        callback(1, {})
        return


def __sendGameAntiCheatingInfo(jsonData, keyFile, certFile, callback):
    try:
        url = SYSD.data.get('gameAntiCheatingLogUrl', 'airkafka-luoge-809-8180.apps-dev.danlu.netease.com')
        parth = SYSD.data.get('gameAntiCheatingLogParth', '/topics/airkafka_test')
        headers = {'Content-type': 'application/json',
         'Connection': 'close'}
        body = '{\"records\":' + jsonData + '}'
        conn = httplib.HTTPSConnection(host=url)
        conn.request('POST', parth, body=body, headers=headers)
        response = conn.getresponse()
        if response.status != 200:
            callback(response, {})
            return
        content = response.read()
        conn.close()
        callback(response, eval(content))
        return
    except Exception as e:
        gamelog.debug('@ZMK SendGameAntiCheatingInfo Error:', e)
        callback(None, {})
        return


def sendGameAntiCheatingInfo(jsonData, keyFile, certFile, callback):
    mgr = pyBgTask.getMgr()
    mgr.add_task(__sendGameAntiCheatingInfo, (jsonData,
     keyFile,
     certFile,
     mgr.make_callback(callback)))
