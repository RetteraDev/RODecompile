#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/CEFControl.o
import BigWorld
CEFModule = None
try:
    import CEFManager as CEFModule
except:
    CEFModule = None

import json
import urllib
import gamelog
import gametypes
import gameglobal
import utils
from helpers import taboo
registedCallbackDic = {}
callbackDic = {}
lastLogMsg = ''
lastLogTime = 0

def handleCEFRequest(request, requestLen):
    request = request[:requestLen]
    logMsg('jbx:handleCEFRequest%s' % request)
    gamelog.debug('@jbx:before unquote', request)
    request = urllib.unquote(request)
    gamelog.debug('m.l@CEFControl.handleCEFRequest', request, requestLen)
    if request.startswith('tianyu:CEFAPI//'):
        requests = request[15:].split(';')
        args = {}
        for i in requests:
            if i.startswith('param:'):
                args['param'] = i[len('param:'):]
                continue
            arg = i.split(':')
            if len(arg) > 1:
                args[arg[0]] = arg[1]

        callbackStr = args.get('callback')
        funcName = args.get('funcName', '')
        dic = json.loads(args.get('param', '{}')) if args.has_key('param') else {}
        if registedCallbackDic.has_key(funcName):
            callbackDic[funcName] = callbackStr
            registedCallbackDic[funcName](dic)


def getDPIScale():
    if 'win10' in BigWorld.getOSDesc().lower() or 'win8' in BigWorld.getOSDesc().lower():
        return BigWorld.getScreenDPI()[0] / 96.0
    return 1.0


def registerFuncCallback(func):

    def wrapper(dic):
        return func(dic)

    registedCallbackDic[func.__name__] = func
    return wrapper


def requestInnerText(cb):
    return CEFModule.requestInnerText(cb)


def execute(key, resultArg = {}):
    jsonStr = json.dumps(resultArg, encoding='gbk')
    callbackStr = callbackDic.get(key, '')
    logMsg(str(('@jbx: cef execute', callbackStr, jsonStr)))
    if callbackStr:
        CEFModule.executeJavaScript(callbackStr + '(' + jsonStr + ')')


def getUrlExtendParamsStr(*params):
    extendUrl = '?'
    for index, paramNameValue in enumerate(params):
        paramName, paramValue = paramNameValue
        if index == 0:
            extendUrl += '%s=%s' % (paramName, str(paramValue))
        else:
            extendUrl += '&%s=%s' % (paramName, str(paramValue))

    return extendUrl


def logMsg(msg):
    global lastLogTime
    global lastLogMsg
    time = utils.getNow()
    gamelog.info(msg, time)
    if lastLogTime and time - lastLogTime > 2 and gameglobal.rds.configData.get('enableCEFOverTimeWarning', False):
        BigWorld.player().reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_CRITICAL, ['CEF OverTime',
         lastLogMsg,
         str(lastLogTime),
         msg,
         str(time)], 0, {})
    lastLogMsg = msg
    lastLogTime = time


def openCEFProgress():
    if not CEFModule.isCefProcessRunning():
        CEFModule.openCefProcess(gameglobal.CEF_PROCESS_NAME, 1107, 620, gameglobal.SW_HIDE)
    CEFModule.setConnBindedCallback(connectionBindedCallback)


def connectionBindedCallback(bind):
    pass


@registerFuncCallback
def queryBattleFieldDotaRole(dic):
    p = BigWorld.player()
    p.base.queryBattleFieldDotaRole()


@registerFuncCallback
def queryBFDotaFavorEquip(dic):
    p = BigWorld.player()
    roleId = dic.get('roleId', 0)
    roleId and p.base.queryBFDotaFavorEquip(roleId)


@registerFuncCallback
def setBFDotaFavorEquip(dic):
    p = BigWorld.player()
    roleId = int(dic.get('roleId', 0))
    favorKey = int(dic.get('favorKey', 0))
    equipList = dic.get('equipList', [])
    roleId and favorKey and equipList and p.base.setBFDotaFavorEquip(roleId, favorKey, equipList)


@registerFuncCallback
def setBFDotaDefaultFavorEquip(dic):
    p = BigWorld.player()
    roleId = dic.get('roleId', 0)
    defaultFavorKey = dic.get('defaultFavorKey', 0)
    roleId and defaultFavorKey and p.base.setBFDotaDefaultFavorEquip(roleId, defaultFavorKey)


@registerFuncCallback
def setBFDotaFavorEquipAlias(dic):
    p = BigWorld.player()
    favorKey = dic.get('favorKey', 0)
    favorAlias = dic.get('favorAlias', '')
    roleId = dic.get('roleId', 0)
    favorAlias = favorAlias.encode('gbk')
    result, favorAlias = taboo.checkDisbWord(favorAlias)
    if not result:
        execute('setBFDotaFavorEquipAlias', {'succ': False})
        return
    result, favorAlias = taboo.checkBWorld(favorAlias)
    if not result:
        execute('setBFDotaFavorEquipAlias', {'succ': False})
        return
    favorKey and favorAlias and p.base.setBFDotaFavorEquipAlias(roleId, favorKey, favorAlias)
