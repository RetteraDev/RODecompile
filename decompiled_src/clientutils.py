#Embedded file name: /WORKSPACE/data/entities/client/clientutils.o
import time
import socket
import os
import decorator
import BigWorld
import Pixie
import gameconfigCommon
import gametypes
import commcalc
import utils
import formula
import const
import gameglobal
import Math
import gamelog
import guideUtils
from datetime import datetime
from callbackHelper import Functor
from data import bonus_data as BD
from data import exp_space_data as ESD
from data import fame_data as FD
from data import mall_item_data as MID
from data import guild_config_data as GCD
from cdata import teleport_destination_data as TDD

def genItemBonus(bonusId, mustItem = True):
    if bonusId <= 0:
        return []
    if not BD.data.has_key(bonusId):
        return []
    bData = BD.data[bonusId]
    bonus = []
    fixedBonus = utils.filtItemByConfig(bData.get('fixedBonus', []), lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
    for bType, itemId, itemNum in fixedBonus:
        if mustItem and bType != gametypes.BONUS_TYPE_ITEM:
            continue
        bonus.append((itemId, itemNum))

    return bonus


def genItemBonusEx(bonusId, mustItem = True):
    displayItems = BD.data.get(bonusId, {}).get('displayItems', ())
    if displayItems:
        return displayItems
    return genItemBonus(bonusId, mustItem)


def timeStrToInt(timeStr):
    return int(timeStr[0:2]) * 60 + int(timeStr[-2:])


def timeIntToStr(time):
    time = int(time)
    hour = time / 60
    if hour < 10:
        hour = '0' + str(hour)
    minute = time % 60
    if minute < 10:
        minute = '0' + str(minute)
    return str(hour) + ':' + str(minute)


def reportEngineException(msg):
    p = BigWorld.player()
    if p and hasattr(p, 'reportClientException'):
        user = p.realRoleName
        localIP = socket.gethostbyname(socket.gethostname())
        msg = 'Traceback :' + msg
        p.reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_SCRIPT, [msg], 10, {'clientUser': user,
         'clientIP': localIP})


callList = []

def callFilter(time = 0, showMsg = True):

    def func(method, *args):
        if method not in callList:
            callList.append(method)
            BigWorld.callback(time, Functor(delFuncFromList, method))
            return method(*args)
        else:
            showMsg and BigWorld.player().showTopMsg('ÇëÇó¹ýÓÚÆµ·±')
            return None

    return decorator.decorator(func)


def delFuncFromList(method):
    callList.remove(method)


def itemMsgParse(msg):
    itemId = -1
    if msg.find('ret') != -1:
        pos1 = msg.find('ret')
        pos2 = msg.find('<u>')
        itemId = int(msg[pos1 + 3:pos2 - 2])
    elif msg.find('item') != -1:
        pos1 = msg.find('item')
        pos2 = msg.find('<u>')
        itemId = int(msg[pos1 + 4:pos2 - 2])
    return itemId


def relativePath2AbsolutePath(path):
    apath = os.getcwd().split('\\')
    rpath = path.split('/')
    for s in rpath:
        if s == '..':
            if len(apath) < 1:
                return ''
            apath.pop()
        elif s:
            apath.append(s)

    return '\\'.join(apath)


def hasExpBonus():
    p = BigWorld.player()
    if p.expBonusFreeze:
        return False
    now = utils.getNow()
    for d in p.expBonus.values():
        remainTime, expireTime, _, _ = d
        if expireTime != 0 and expireTime < now:
            continue
        if remainTime > 0:
            return True

    return False


def _mayHasGuideMode(mapId):
    if not ESD.data.has_key(mapId):
        return False
    if ESD.data[mapId].has_key('guideLowLv') or ESD.data[mapId].has_key('guideLowLvFId'):
        return True
    if gameconfigCommon.enableGuideModeWithXiuweiLv():
        return ESD.data[mapId].has_key('guideLowXiuweiLv') or ESD.data[mapId].has_key('guideLowXiuweiLvFId')
    return False


def getGroupGuideMode(owner, spaceNo, mlLv):
    mapId = formula.getMapId(spaceNo)
    if _mayHasGuideMode(mapId):
        teamerLvs = [ (x['level'], x['xiuweiLevel']) for x in owner.members.itervalues() if owner.id != x['id'] and x['isOn'] ]
        if len(teamerLvs) == 0:
            return const.GUIDE_NONE_MODE
        minLv = min(teamerLvs, key=lambda x: x[0])[0]
        minXiuweiLv = min(teamerLvs, key=lambda x: x[1])[1]
        return guideUtils.getGuideMode(mapId, owner.lv, minLv, owner.xiuweiLevel, minXiuweiLv)
    else:
        return const.GUIDE_NONE_MODE


def notifyFame(fameId):
    return not FD.data.get(fameId, {}).get('notNotifyFame', 0)


def getRealGroupGuideMode(owner, spaceNo, mlLv):
    mapId = formula.getMapId(spaceNo)
    if _mayHasGuideMode(mapId):
        guideLowLv, guideThresLv = guideUtils.genMLGuideLowLv(mapId, mlLv)
        guideLowXiuweiLv, guideThresXiuweiLv = guideUtils.genMLGuideLowXiuweiLevel(mapId, mlLv)
        macAddress = ''
        for teamer in owner.members.itervalues():
            if teamer['id'] == owner.id:
                macAddress = teamer['macAddress']
                break

        validTeamers = []
        guideConfigMode = guideUtils.getGuideConfigMode(mapId)
        checkLv = guideConfigMode in const.GUIDE_CONFIG_CHECK_LV
        checkXiuweiLv = guideConfigMode in const.GUIDE_CONFIG_CHECK_XIUWEI_LV
        for teamer in owner.members.itervalues():
            if teamer['id'] == owner.id or teamer['isOn'] == False:
                continue
            if teamer['macAddress'] == macAddress:
                continue
            if checkLv and checkXiuweiLv and (not checkLv or teamer['level'] <= guideLowLv) and (not checkXiuweiLv or teamer['xiuweiLevel'] <= guideLowXiuweiLv):
                other = BigWorld.entities.get(teamer['id'])
                if not other or other.exceedYaoliLimit():
                    continue
            validTeamers.append(teamer)

        teamerLvs = [ (x['level'], x['xiuweiLevel']) for x in validTeamers ]
        if len(teamerLvs) == 0:
            return const.GUIDE_NONE_MODE
        minLv = min(teamerLvs, key=lambda x: x[0])[0]
        maxLv = max(teamerLvs, key=lambda x: x[0])[0]
        maxXiuweiLv = max(teamerLvs, key=lambda x: x[1])[1]
        minXiuweiLv = min(teamerLvs, key=lambda x: x[1])[1]
        return guideUtils.getGuideMode(mapId, owner.lv, minLv, owner.xiuweiLevel, minXiuweiLv, maxLv, maxXiuweiLv)
    else:
        return const.GUIDE_NONE_MODE


def getMallItemDiscountInfo(mIds, mNums = None):
    discountInfo = []
    p = BigWorld.player()
    if not mNums:
        for mid in mIds:
            md = MID.data.get(mid)
            if not md:
                return None
            discountType = md.get('discountType')
            if not discountType:
                discountInfo.append(False)
                continue
            discountItem = md['discountItem']
            if p.inv.countItemInPages(discountItem, enableParentCheck=True) >= 1:
                discountInfo.append(True)
            else:
                discountInfo.append(False)

    else:
        IsDiscountItems = []
        for mid, num in zip(mIds, mNums):
            md = MID.data.get(mid)
            if not md:
                return None
            discountType = md.get('discountType')
            if not discountType:
                discountInfo.append(False)
                continue
            if discountType == 2:
                IsDiscountItems.append(False)
            else:
                IsDiscountItems.append(True)
            discountItem = md['discountItem']
            if p.inv.countItemInPages(discountItem, enableParentCheck=True) >= num:
                discountInfo.append(True)
            else:
                discountInfo.append(False)

        return (discountInfo, IsDiscountItems)
    return discountInfo


def getModelPath(modelId):
    if modelId > 10009:
        path = '%s%d/%d.model' % (gameglobal.charRes, modelId, modelId)
    else:
        path = '%s%d/dummy.model' % (gameglobal.charRes, modelId)
    return path


def getDumpFilesInfo():
    try:
        allFiles = os.listdir('../game')
    except IOError:
        return 'Error'

    dumpFiles = [ fileName for fileName in allFiles if os.path.splitext(fileName)[1] == '.dmp' ]
    dumpFiles.sort(key=lambda f: os.path.getmtime(f), reverse=True)
    if not dumpFiles:
        return 'There is no dumpFile'
    RECENT_FILE_SIZE = 20
    dumpFileSize = len(dumpFiles)
    res = 'The number of dumpFiles: %d\n' % dumpFileSize
    recentFiles = dumpFiles[:min(RECENT_FILE_SIZE, dumpFileSize)]
    for fileName in recentFiles:
        t = time.localtime(os.path.getmtime(fileName))
        date = time.strftime('%d/%.2d/%.2d %.2d:%.2d' % (t.tm_year,
         t.tm_mon,
         t.tm_mday,
         t.tm_hour,
         t.tm_min))
        res += 'time: %s,    fileName: %s,    size: %d\n' % (date, fileName, os.path.getsize(fileName))

    return res


def unpackCompInfo(compInfo):
    from data import mail_template_data as MTD
    if len(compInfo) == 2:
        mailTemplateId, rewards = compInfo
        mtd = MTD.data.get(mailTemplateId, {})
        return (mtd.get('subject', ''), mtd.get('content', ''), rewards)
    if len(compInfo) == 4:
        mailTemplateId, rewards, mailSubject, mailContent = compInfo
        mtd = MTD.data.get(mailTemplateId, {})
        return (mtd.get('subject', '') or mailSubject or '', mtd.get('content', '') or mailContent or '', rewards)
    if len(compInfo) == 6:
        mailTemplateId, rewards, mailSubject, mailContent, id, compType = compInfo
        mtd = MTD.data.get(mailTemplateId, {})
        return (mtd.get('subject', '') or mailSubject or '',
         mtd.get('content', '') or mailContent or '',
         rewards,
         id,
         compType)


def checkFallendRedGuardTime():
    startTime = GCD.data.get('fallenRedGuardStartTime', [])
    endTime = GCD.data.get('fallenRedGuardEndTime', [])
    return startTime and endTime and utils.inTimeRange(startTime, endTime)


def teleportToStone(callback, destId, fromNavigator = False):
    if gameglobal.rds.configData.get('enableKillFallenRedGuard', False):
        if checkFallendRedGuardTime():
            flag = TDD.data.get(destId, {}).get('fallenRedGuardFlag', 0)
            gamelog.info('jbx:teleportToStone', flag)
            if flag:
                BigWorld.player().base.getFallenRedGuardChunkInfo(flag)
                gameglobal.rds.ui.killFallenRedGuardRank.callback = Functor(callback, destId)
                gameglobal.rds.ui.killFallenRedGuardRank.currentCallbackFun = None
                if fromNavigator:
                    from helpers import navigator
                    navigator.getNav().stopPathFinding(False)
                    gameglobal.rds.ui.killFallenRedGuardRank.continuePathFinding = True
                return
    callback(destId)


def model(*path):
    if gameglobal.rds.configData.get('enableMaterialLoadStatistics', False):
        processModelStatistics(path[0])
    return BigWorld.Model(*path)


def fetchModel(*args):
    path = args[2]
    if gameglobal.rds.configData.get('enableMaterialLoadStatistics', False):
        processModelStatistics(path)
    return BigWorld.fetchModel(*args)


def pixieFetch(path, lv = 999, maxDelayTime = 0):
    if gameglobal.rds.configData.get('enableMaterialLoadStatistics', False):
        processEffectStatistics(path)
    return Pixie.fetch(path, lv, maxDelayTime)


def processModelStatistics(path):
    if isinstance(path, str):
        modelMark = []
        pathSplit = path.split('/')
        if pathSplit[0] != 'item' and pathSplit[0] != 'char':
            return
        modelMark.append(pathSplit[0])
        if pathSplit[0] == 'char':
            modelMark.append(pathSplit[1])
        else:
            modelMark.append(pathSplit[2])
        gameglobal.rds.uiLog.addModelCntLog(modelMark)


def processEffectStatistics(path):
    pathSplit = path.split('/')
    effectId = pathSplit[-1].split('.')[0]
    gameglobal.rds.uiLog.addEffectCntLog(effectId)


def getPeriodFromTime(t):
    dt = datetime.fromtimestamp(t)
    return '%d0%d' % (dt.year, (dt.month - 1) // 3 + 1)


def isSamePeriod(time1, time2):
    period1 = getPeriodFromTime(time1)
    period2 = getPeriodFromTime(time2)
    return period1 == period2


def RSAEncrypt(message, publicKey):
    from Crypto.Cipher import PKCS1_v1_5
    from Crypto.PublicKey import RSA
    from Crypto.Hash import SHA
    h = SHA.new(message)
    key = RSA.importKey(publicKey)
    cipher = PKCS1_v1_5.new(key)
    ciphertext = cipher.encrypt(message + h.digest())
    return ciphertext
