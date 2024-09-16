#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/emoteProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
import gametypes
import utils
from guis import uiConst
from guis.ui import gbk2unicode
from guis import uiUtils
from guis.uiProxy import SlotDataProxy
from helpers import capturePhoto
from guis import ui
from helpers import charRes
from data import emote_data as ED
from data import sys_config_data as SCD
from data import emote_reverted_data as ERD
from data import face_emote_data as FED
from data import couple_emote_basic_data as CEBD
from cdata import game_msg_def_data as GMDD
EMOTE_PATH_TMPLATE = 'emote/%s.dds'

class EmoteProxy(SlotDataProxy):
    FACE_EMOTE_SLOT_ID = 9999
    EMOTE_LOCK_STATE = 1
    EMOTE_UNLOCK_STATE = 2
    EMOTE_LIMIT_UNLOCK_STATE = 3
    EMOTE_EXPIRE_STATE = 4

    def __init__(self, uiAdapter):
        SlotDataProxy.__init__(self, uiAdapter)
        self.bindType = 'emote'
        self.type = 'emote'
        self.modelMap = {'getSubTabsInfo': self.onGetSubTabsInfo,
         'getEmoteInfoByTab': self.onGetEmoteInfoByTab,
         'useEmote': self.onUseEmote,
         'isFaceEmotionTab': self.isFaceEmotionTab,
         'unLoadFaceEmoteSlot': self.onUnLoadFaceEmoteSlot,
         'getFaceEmoteInfo': self.onGetFaceEmoteInfo,
         'getCurrentMc': self.onGetCurrentMc}
        self.reset()
        self.headGen = None

    def reset(self):
        self.faceEmoteXmlInfo = {}
        self.tempFaceEmoteXmlInfo = {}
        self.tempCallback = None
        self.mc = None

    def show(self, *args):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GENERAL_SKILL)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GENERAL_SKILL)

    def showEmote(self, emoteId):
        p = BigWorld.player()
        if p and p.topLogo:
            p.topLogo.showEmote(emoteId)

    def showEmoteByCommand(self, command):
        key = self.getEmoteIdByCommand(command)
        if key:
            p = BigWorld.player()
            if p and p.topLogo:
                p.topLogo.showEmote(key)

    def getEmoteIdByCommand(self, command):
        for key in ED.data.keys():
            shortCommand = ED.data.get(key, {}).get('shortcommand', {})
            for subCommand in shortCommand:
                if subCommand == command.strip().lower():
                    return key

    def isEmoteVail(self, emoteData):
        p = BigWorld.player()
        modelId = charRes.transDummyBodyType(p.realPhysique.sex, p.realPhysique.bodyType, True)
        school = p.school
        if emoteData.has_key('modelId'):
            if modelId not in emoteData.get('modelId'):
                return False
        if emoteData.has_key('school'):
            if school not in emoteData.get('school'):
                return False
        if emoteData.get('hideIcon', False):
            return False
        return True

    def onNotifySlotUse(self, *arg):
        pass

    def getSlotID(self, key):
        page, idItem = key.split('.')
        return (int(page[5:]), int(idItem))

    def getEmoteId(self, pageIndex, index):
        return index

    def getEmotePath(self, key):
        data = ED.data.get(key)
        if data:
            p = BigWorld.player()
            itemNos = data.get('itemNos', [])
            eType = data.get('type', 0)
            icon = 'icon'
            if itemNos:
                icon = 'icon2'
                equipIds = self.getEquipId()
                for itemNo in itemNos:
                    if itemNo in equipIds:
                        icon = 'icon'

            elif eType == const.EMOTE_TYPE_FACE:
                if self.getEmoteExpireRemainTime(key, False) == EmoteProxy.EMOTE_LOCK_STATE:
                    icon = 'icon2'
            elif eType == const.EMOTE_TYPE_ACTION:
                funcType = data.get('funcType', 0)
                if funcType == uiConst.EMOTE_FUNTYPE_COUPLE_EMOTE and eType == const.EMOTE_TYPE_ACTION:
                    coupleEmoteId = int(data.get('res', gametypes.COUPLE_EMOTE_TYPE_PRINCESS_HUG))
                    cebd = CEBD.data.get(coupleEmoteId)
                    if cebd.get('needFlag') and not p.getEmoteEnableFlags(coupleEmoteId):
                        icon = 'icon2'
            elif eType == const.EMOTE_TYPE_EMOTION:
                needUnlock = data.get('needUnlock', 0)
                if needUnlock and not p.getSocialEmoteEnableFlags(key):
                    icon = 'icon2'
            return 'emote/%s.dds' % data.get(icon, '')

    def isFaceEmoteExpire(self, key):
        p = BigWorld.player()
        needUnlock = FED.data.get(key, {}).get('needUnlock', 0)
        tExpire = p.faceEmoteExpire.get(key, {}).get('tExpire', 1)
        if needUnlock and not p.isValidVipProp(gametypes.VIP_SERVICE_UNLOCK_FACE_EMOTE) and tExpire != const.FACE_EMOTE_VALID_TIME_INFINITE and utils.getNow() > tExpire:
            return True
        return False

    def getTip(self, emoteId):
        data = ED.data.get(emoteId)
        if data:
            shortCommands = data.get('shortcommand', '')
            tips = ''
            if shortCommands:
                tips = gameStrings.TEXT_EMOTEPROXY_151 % shortCommands[0]
            desc = data.get('desc', '')
            if desc:
                if tips:
                    tips = tips + '\n' + desc
                else:
                    tips = desc
            expireTime = self.getEmoteExpireRemainTime(emoteId)
            if expireTime:
                tips = tips + '\n' + uiUtils.formatTime(expireTime)
            return tips

    def getEmoteExpireRemainTime(self, key, isTimeOrState = True):
        p = BigWorld.player()
        needUnlock = FED.data.get(key, {}).get('needUnlock', 0)
        keyMap = p.faceEmoteExpire.get(key, {})
        tExpire = keyMap.get('tExpire', 1)
        if not needUnlock or p.isValidVipProp(gametypes.VIP_SERVICE_UNLOCK_FACE_EMOTE) or tExpire == const.FACE_EMOTE_VALID_TIME_INFINITE:
            if isTimeOrState:
                return None
            return EmoteProxy.EMOTE_UNLOCK_STATE
        remainTime = tExpire - utils.getNow()
        if remainTime > 0:
            if isTimeOrState:
                return remainTime
            return EmoteProxy.EMOTE_LIMIT_UNLOCK_STATE
        elif keyMap != {}:
            if isTimeOrState:
                return None
            return EmoteProxy.EMOTE_EXPIRE_STATE
        elif isTimeOrState:
            return None
        else:
            return EmoteProxy.EMOTE_LOCK_STATE

    def getEquipId(self):
        equipmentId = []
        for equip in BigWorld.player().equipment:
            if equip:
                equipmentId.append(equip.id)

        return equipmentId

    def checkEmotePlay(self, key):
        data = ED.data.get(key, {})
        itemNos = data.get('itemNos', [])
        if not itemNos:
            return True
        equipId = self.getEquipId()
        for itemNo in itemNos:
            if itemNo and itemNo in equipId:
                return True

        return False

    def getRealEmoteId(self, emoteId):
        data = ED.data.get(emoteId, {})
        flag = gameglobal.rds.emoteFlag.get(emoteId, 0)
        if not flag:
            gameglobal.rds.emoteFlag[emoteId] = 1
            return emoteId
        if data.get('nextEmote', 0):
            gameglobal.rds.emoteFlag[emoteId] = 0
            return data.get('nextEmote', 0)
        return emoteId

    def onUseEmote(self, *arg):
        emoteId = int(arg[3][0].GetNumber())
        isRightButton = arg[3][1].GetBool()
        emoteId = self.getRealEmoteId(emoteId)
        ed = ED.data.get(emoteId, {})
        type = ed.get('type', 0)
        p = BigWorld.player()
        if isRightButton and type == const.EMOTE_TYPE_FACE:
            self.setCurFaceEmote(emoteId)
        else:
            p.wantToDoEmote(emoteId)
            self.tryFaceEmote(int(emoteId))

    def setCurFaceEmote(self, emoteId):
        p = BigWorld.player()
        state = self.getEmoteExpireRemainTime(emoteId, False)
        if state == self.EMOTE_EXPIRE_STATE:
            p.showGameMsg(GMDD.data.FACE_EMOTE_SET_FAILED_EXPIRED, ())
        elif state == self.EMOTE_LOCK_STATE:
            p.showGameMsg(GMDD.data.FACE_EMOTE_SET_FAILED_UNLOCK, ())
        elif p.stateMachine.checkStatus(const.CT_EQUIP_FACE_EMOTE):
            p.cell.setCurFaceEmote(emoteId)

    @ui.callFilter(2, False)
    def tryFaceEmote(self, emoteId):
        ed = ED.data.get(emoteId, {})
        type = ed.get('type', 0)
        duration = ed.get('duration', 4)
        if type == const.EMOTE_TYPE_FACE:
            if self.tempFaceEmoteXmlInfo:
                self.endPhotoFaceEmote(self.tempFaceEmoteXmlInfo)
                self.tempFaceEmoteXmlInfo = {}
            if self.faceEmoteXmlInfo:
                self.endPhotoFaceEmote(self.faceEmoteXmlInfo)
                self.faceEmoteXmlInfo = {}
            if self.tempCallback:
                BigWorld.cancelCallback(self.tempCallback)
                self.tempCallback = None
            self.tempFaceEmoteXmlInfo = self.startPhotoFaceEmote(emoteId)
            self.tempCallback = BigWorld.callback(duration, self.faceEmoteTimeOut)

    def isFaceEmotionTab(self, *arg):
        tabId = int(arg[3][0].GetNumber())
        return GfxValue(tabId == SCD.data.get('FaceEmotionTab', 3))

    def onUnLoadFaceEmoteSlot(self, *arg):
        p = BigWorld.player()
        p.cell.resetCurFaceEmote()

    def onGetFaceEmoteInfo(self, *arg):
        p = BigWorld.player()
        info = self.getEmoteInfoById(p.curFaceEmoteId)
        return uiUtils.dict2GfxDict(info)

    def onGetCurrentMc(self, *arg):
        self.mc = arg[3][0]

    def setFaceEmote(self):
        p = BigWorld.player()
        info = self.getEmoteInfoById(p.curFaceEmoteId)
        self.setFaceEmotionSlotData(info)
        if self.faceEmoteXmlInfo:
            self.endPhotoFaceEmote(self.faceEmoteXmlInfo)
            self.faceEmoteXmlInfo = {}
        if self.tempFaceEmoteXmlInfo:
            self.endPhotoFaceEmote(self.tempFaceEmoteXmlInfo)
            self.tempFaceEmoteXmlInfo = {}
        if p.curFaceEmoteId:
            self.faceEmoteXmlInfo = self.startPhotoFaceEmote(p.curFaceEmoteId)

    def startPhotoFaceEmote(self, emoteId):
        if not self.headGen:
            return
        else:
            p = BigWorld.player()
            model = self.headGen.adaptor.attachment
            if not model:
                return
            xmlName = ED.data.get(emoteId, {}).get('res', None)
            return p.realStartFaceEmote(xmlName, model, p.realPhysique)

    def endPhotoFaceEmote(self, faceEmoteXmlInfo):
        if not self.headGen:
            return
        p = BigWorld.player()
        model = self.headGen.adaptor.attachment
        if not model:
            return
        p.realEndFaceEmote(model, p.realPhysique, faceEmoteXmlInfo)

    def faceEmoteTimeOut(self):
        if self.tempFaceEmoteXmlInfo:
            self.endPhotoFaceEmote(self.tempFaceEmoteXmlInfo)
            self.tempFaceEmoteXmlInfo = {}
        if self.tempCallback:
            self.tempCallback = None
        p = BigWorld.player()
        if p.curFaceEmoteId:
            self.faceEmoteXmlInfo = self.startPhotoFaceEmote(p.curFaceEmoteId)

    def afterPlayerModelFinished(self):
        p = BigWorld.player()
        model = self.headGen.adaptor.attachment
        model.soundCallback(None)
        if not model:
            return
        else:
            if p.curFaceEmoteId:
                self.faceEmoteXmlInfo = self.startPhotoFaceEmote(p.curFaceEmoteId)
            self.setLoadingIconVisible(False)
            return

    def setFaceEmotionSlotData(self, data):
        key = 'emote0.%d' % self.FACE_EMOTE_SLOT_ID
        if key not in self.binding:
            return
        if not data:
            data = GfxValue(1)
            data.SetNull()
            self.binding[key][1].InvokeSelf(data)
        else:
            self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data))

    def moveEmoteIcon(self, fromId, toId):
        if toId == self.FACE_EMOTE_SLOT_ID and FED.data.get(fromId):
            self.setCurFaceEmote(fromId)

    def onGetSubTabsInfo(self, *arg):
        ret = []
        tabKeys = ERD.data.keys()
        tabNames = SCD.data.get('emotionTabName', {})
        tabKeys.sort()
        if not gameglobal.rds.configData.get('enableFaceEmote', False):
            tabId = SCD.data.get('FaceEmotionTab', 3)
            if tabId in tabKeys:
                tabKeys.remove(tabId)
        for tabId in tabKeys:
            tabInfo = {}
            tabInfo['tabId'] = tabId
            tabInfo['tabName'] = tabNames.get(tabId, '')
            if tabInfo['tabName']:
                ret.append(tabInfo)

        return uiUtils.array2GfxAarry(ret, True)

    def onGetEmoteInfoByTab(self, *arg):
        tabId = int(arg[3][0].GetNumber())
        ret = []
        cateNames = SCD.data.get('emotionCateName', {})
        tabData = ERD.data.get(tabId, {})
        cateKeys = tabData.keys()
        cateKeys.sort()
        for cateId in cateKeys:
            cateInfo = {}
            emotions = []
            cateInfo['cateId'] = cateId
            cateInfo['cateName'] = cateNames.get(cateId, '')
            if cateInfo['cateName']:
                emotions = self.genEmoteInfos(tabData, cateId)
            if len(emotions) > 0:
                cateInfo['emotions'] = emotions
                ret.append(cateInfo)

        return uiUtils.array2GfxAarry(ret, True)

    def getEmoteInfoById(self, id):
        emoteInfo = {}
        if id == 0:
            return emoteInfo
        emoteInfo['id'] = id
        emoteInfo['name'] = ED.data.get(id, {}).get('name', '')
        emoteInfo['iconPath'] = self.getEmotePath(id)
        emoteInfo['state'] = self.getEmoteExpireRemainTime(id, False)
        return emoteInfo

    def genEmoteInfos(self, tabData, cateId):
        ret = []
        emoteDatas = tabData.get(cateId, {})
        emoteKeys = emoteDatas.keys()
        emoteKeys.sort()
        for emoteId in emoteKeys:
            emoteInfo = {}
            emoteData = emoteDatas[emoteId]
            if not self.isEmoteVail(emoteData):
                continue
            emoteInfo['id'] = emoteId
            emoteInfo['name'] = emoteData.get('name', '')
            emoteInfo['iconPath'] = self.getEmotePath(emoteId)
            emoteInfo['state'] = self.getEmoteExpireRemainTime(emoteId, False)
            self.setEmoteCoolDown(emoteId, emoteInfo)
            ret.append(emoteInfo)

        return ret

    def setEmoteCoolDown(self, emoteId, emoteInfo):
        if emoteId == uiConst.EMOTE_BIDONG:
            eId = ED.data.get(uiConst.EMOTE_BIDONG, {}).get('res', None)
            eId = int(eId) if eId else 0
            total = CEBD.data.get(eId, {}).get('skillCD', 60)
            endTime = BigWorld.player().cpEmoteSkillCD.get(eId, None)
            remain = endTime - utils.getNow() if endTime else -1
            remain = total - remain + 1
            emoteInfo['total'] = total * 1000
            emoteInfo['remain'] = remain * 1000

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        page, pos = self.getSlotID(key)
        emoteId = self.getEmoteId(page, pos)
        return GfxValue(gbk2unicode(self.getTip(emoteId)))

    def initHeadGen(self):
        if not self.headGen:
            self.headGen = capturePhoto.FaceEmotePhotoGen.getInstance('gui/taskmask.tga', 324)
        self.headGen.initFlashMesh()
        self.headGen.setModelFinishCallback(self.afterPlayerModelFinished)

    def takePhoto3D(self):
        if not self.headGen:
            self.headGen = capturePhoto.FaceEmotePhotoGen.getInstance('gui/taskmask.tga', 324)
        self.headGen.startCaptureEnt(BigWorld.player())

    def resetHeadGen(self):
        if self.headGen:
            self.headGen.endCapture()
            self.headGen = None

    def setLoadingIconVisible(self, value):
        if self.mc:
            self.mc.Invoke('setLoadingIconVisible', GfxValue(value))
