#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/emoteActionProxy.o
import math
import BigWorld
import gametypes
import gameglobal
import uiConst
import events
import const
import skillInfoManager
import clientUtils
import utils
from helpers import charRes
from uiProxy import UIProxy
from asObject import ASObject
from helpers import capturePhoto
from guis import ui
from helpers import clientSkillHelper
from callbackHelper import Functor
from gamestrings import gameStrings
from sfx import sfx
from guis.asObject import ASUtils
from data import sys_config_data as SCD
from data import emote_reverted_data as ERD
from data import emote_data as ED
from data import emote_action_skill_data as EASD
from data import face_emote_data as FED
from data import couple_emote_basic_data as CEBD
from cdata import game_msg_def_data as GMDD
NUM_IN_LINE = 6
SLOT_WIDTH = 75
SLOT_HEIGHT = 75
FACE_PANEL_NUM_IN_LINE = 3
FACE_PANEL_OFFSET_X = 226
PANEL_TAB_OFFSET = 74
FACE_EMOTE_SLOT = 9999
EMOTE_LOCK_STATE = 1
EMOTE_UNLOCK_STATE = 2
EMOTE_LIMIT_UNLOCK_STATE = 3
EMOTE_EXPIRE_STATE = 4
GAO_GUAI_WU_DAO = 14
ZHAN_SHI_DONG_ZUO = 41
IDLE_EMOTE = 6001
DEFULT_SKILL_LEVEL = 1

class EmoteActionProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EmoteActionProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_EMOTE_ACTION, self.hide)

    def reset(self):
        self.emoteInfo = []
        self.isFaceEmotion = False
        self.headGen = None
        self.faceEmoteXmlInfo = {}
        self.tempFaceEmoteXmlInfo = {}
        self.tempCallback = None
        self.emoteActionSelectedSkills = []
        self.entId = None
        self.existedSkills = {}
        self.existedStates = {}
        self.dist = 10

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_EMOTE_ACTION:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_EMOTE_ACTION)
        BigWorld.destroyEntity(self.entId)
        self.entId = None
        if gameglobal.rds.configData.get('enableNewCamera', False) and gameglobal.rds.ui.cameraV2.widget:
            gameglobal.rds.ui.cameraV2.widget.bg.content.playBtn.visible = False
            gameglobal.rds.ui.cameraV2.widget.bg.content.stopBtn.visible = False
            BigWorld.setParticleFrameRateMagnitude(1, 0)
            BigWorld.setActionFrameRateMagnitude(1, 0)
        self.resetHeadGen()
        for stateId in self.existedStates.keys():
            BigWorld.player().removeBuffIconByClient(stateId)
            self.existedStates.pop(stateId)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_EMOTE_ACTION)

    def initUI(self):
        self.initHeadGen()
        self.takePhoto3D()
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.generalEmoteScrollWnd.visible = True
        self.widget.emotionView.faceEmotionPanel.visible = False
        self.widget.emotionView.tabBtn0.addEventListener(events.BUTTON_CLICK, self.handleChangeBtn, False, 0, True)
        self.widget.emotionView.tabBtn1.addEventListener(events.BUTTON_CLICK, self.handleChangeBtn, False, 0, True)
        self.widget.emotionView.tabBtn2.addEventListener(events.BUTTON_CLICK, self.handleChangeBtn, False, 0, True)
        self.widget.emotionView.tabBtn3.addEventListener(events.BUTTON_CLICK, self.handleChangeBtn, False, 0, True)
        self.widget.emotionView.faceEmotionPanel.picture.faceEmotionSlot.addEventListener(events.MOUSE_CLICK, self.faceEmotionslotClickListener, False, 0, True)
        if not gameglobal.rds.ui.cameraV2.isShow and not gameglobal.rds.ui.camera.isShow:
            self.widget.emotionView.tabBtn2.visible = False
            self.widget.emotionView.tabBtn3.x -= PANEL_TAB_OFFSET
        self.widget.emotionView.faceEmotionPanel.picture.faceEmotionSlot.binding = 'emote0.' + str(FACE_EMOTE_SLOT)
        if self.getFaceEmoteInfo():
            self.widget.emotionView.faceEmotionPanel.picture.faceEmotionSlot.setItemSlotData(self.getFaceEmoteInfo())
        self.initTabLabel()
        self.emoteInfo = self.getEmoteInfoByTab(1)
        p = BigWorld.player()
        position = self.getEntPosition(self.dist)
        self.entId = BigWorld.createEntity('StaticCombatCreation', p.spaceID, 0, position, (0, 0, 1), {})
        BigWorld.callback(0.1, self.refreshEmotePanel)

    def refreshInfo(self):
        if not self.widget:
            return

    def initTabLabel(self):
        for i in xrange(4):
            tabName = 'tabBtn' + str(i)
            tab = getattr(self.widget.emotionView, tabName, None)
            if tab:
                tab.label = gameStrings.EMOTE_ACTION_LABEL[i]

    def getEmoteInfoByTab(self, tabId):
        if tabId == 4:
            tabId = 3
        ret = []
        if tabId != 1:
            ret = self.getEmoteInfoBySubTab(tabId)
        else:
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

        return ret

    def getEmoteInfoBySubTab(self, tabId):
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

        return ret

    def handleChangeBtn(self, *args):
        e = ASObject(args[3][0])
        if e.target == self.widget.emotionView.tabBtn0:
            self.emoteInfo = self.getEmoteInfoByTab(1)
            self.isFaceEmotion = False
        elif e.target == self.widget.emotionView.tabBtn1:
            self.emoteInfo = self.getEmoteInfoByTab(2)
            self.isFaceEmotion = False
        elif e.target == self.widget.emotionView.tabBtn2:
            self.refreshSkillPanel()
        elif e.target == self.widget.emotionView.tabBtn3:
            self.emoteInfo = self.getEmoteInfoByTab(4)
            self.isFaceEmotion = True
        if e.target != self.widget.emotionView.tabBtn2:
            self.refreshEmotePanel()

    def faceEmotionslotClickListener(self, *args):
        e = ASObject(args[3][0])
        if e.buttonIdx == uiConst.RIGHT_BUTTON:
            p = BigWorld.player()
            p.cell.resetCurFaceEmote()
            self.useEmote(IDLE_EMOTE, False)

    def refreshSkillPanel(self):
        MARGIN_X = 10
        self.widget.generalEmoteScrollWnd.visible = True
        self.widget.emotionView.faceEmotionPanel.visible = False
        scrollWnd = self.widget.generalEmoteScrollWnd
        while scrollWnd.canvas.numChildren > 0:
            scrollWnd.canvas.removeChildAt(0)

        p = BigWorld.player()
        self.emoteActionSelectedSkills = []
        skills = EASD.data.values()
        for skill in skills:
            if skill['school'] == p.school:
                self.emoteActionSelectedSkills.append(skill)

        for i, skill in enumerate(self.emoteActionSelectedSkills):
            skillId = int(skill['skill'])
            isWsSkill = skill['isWsSkill']
            skillMc = self.widget.getInstByClsName('GeneralSkill_GeneralIcon')
            skillMc.x = i % NUM_IN_LINE * SLOT_WIDTH + MARGIN_X
            skillMc.y = int(i / NUM_IN_LINE) * SLOT_HEIGHT
            skillInfo = self.genSkillInfo(skillId, isWsSkill)
            skillMc.levelField.visible = False
            skillMc.skillName.textField.text = skillInfo['skillName']
            mcWidth = skillMc.skillName.textField.width
            ASUtils.autoSizeWithFont(skillMc.skillName.textField, 14, mcWidth, 5)
            skillMc.skillId = skillId
            skillMc.skillLv = skillInfo['skillLv']
            skillMc.states = skill.get('stateId', ())
            skillMc.creationInfo = skill.get('creationInfo', ())
            skillMc.effectInfo = skill.get('effectInfo', [])
            skillMc.dist = skill.get('dist', 10)
            skillMc.slot.setItemSlotData(skillInfo['icon'])
            if not self.canUseSkill():
                skillMc.slot.setSlotState(uiConst.SKILL_ICON_STAT_GRAY)
                skillMc.addEventListener(events.MOUSE_CLICK, self.useSkillForbiden, False, 0, True)
            else:
                skillMc.addEventListener(events.MOUSE_CLICK, self.useSkillClientOnly, False, 0, True)
            skillMc.slot.dragable = False
            scrollWnd.canvas.addChild(skillMc)

        scrollWnd.refreshHeight()

    def useSkillForbiden(self, *args):
        BigWorld.player().showGameMsg(GMDD.data.EMOTE_ACTION_FROBID_SKILL, ())

    def useSkillClientOnly(self, *args):
        if not self.canUseSkill():
            return
        e = ASObject(args[3][0])
        skillId = e.target.parent.skillId
        skillLv = e.target.parent.skillLv
        states = e.target.parent.states
        dist = e.target.parent.dist
        creationInfo = e.target.parent.creationInfo
        effectInfo = e.target.parent.effectInfo
        tempEntities = self.existedSkills.get(skillId, [])
        for entId in tempEntities:
            BigWorld.destroyEntity(entId)

        self.existedSkills[skillId] = []
        BigWorld.destroyEntity(self.entId)
        p = BigWorld.player()
        position = self.getEntPosition(dist)
        self.entId = BigWorld.createEntity('StaticCombatCreation', p.spaceID, 0, position, (0, 0, 1), {})
        self.existedSkills[skillId].append(self.entId)
        clientSkill = clientSkillHelper.getInstance()
        clientSkill.clientUseSkill(p, skillId, DEFULT_SKILL_LEVEL, self.entId)
        for state in states:
            if self.existedStates.has_key(state[0]):
                p.removeBuffIconByClient(state[0])
            self.existedStates[state[0]] = utils.getNowMillisecond()
            p.addBuffIconByClient(state[0])
            BigWorld.callback(state[1], Functor(self.removeBuffIconByClient, state[0], state[1]))

        for creationItem in creationInfo:
            BigWorld.callback(creationItem[0], Functor(self.createCreation, creationItem[1], creationItem[2], skillId, dist))

        if len(effectInfo) == 3:
            BigWorld.callback(effectInfo[0], Functor(self.setEffect, effectInfo[1], effectInfo[2], skillId, dist))

    def removeBuffIconByClient(self, stateId, existTime):
        if self.existedStates.has_key(stateId) and utils.getNowMillisecond() - self.existedStates[stateId] + 200 >= existTime * 1000:
            self.existedStates.pop(stateId)
            BigWorld.player().removeBuffIconByClient(stateId)

    def createCreation(self, existTime, creationId, skillId, dist):
        p = BigWorld.player()
        position = self.getEntPosition(dist)
        entId = BigWorld.createEntity('StaticCombatCreation', p.spaceID, 0, position, (0, 0, 1), {'cid': creationId})
        self.existedSkills[skillId].append(entId)
        BigWorld.callback(existTime, Functor(self.destoryEnt, entId, skillId))

    def destoryEnt(self, entId, skillId):
        if gameglobal.rds.ui.cameraV2.isShow and gameglobal.rds.ui.cameraV2.widget.bg.content.playBtn.visible == True:
            BigWorld.callback(2, Functor(self.destoryEnt, entId, skillId))
        else:
            BigWorld.destroyEntity(entId)
            if entId in self.existedSkills.get(skillId, []):
                self.existedSkills[skillId].remove(entId)

    def setEffect(self, existTime, effectId, skillId, dist):
        fx = clientUtils.pixieFetch(sfx.getPath(effectId))
        p = BigWorld.player()
        position = self.getEntPosition(dist)
        entId = BigWorld.createEntity('StaticCombatCreation', p.spaceID, 0, position, (0, 0, 1), {})
        self.existedSkills[skillId].append(entId)
        BigWorld.entity(entId).model.node('Scene Root').attach(fx)
        BigWorld.callback(existTime, Functor(self.destoryEnt, entId, skillId))

    def genSkillInfo(self, skillId, isWsSkill):
        skillManager = skillInfoManager.getInstance()
        skillInfo = skillManager.commonSkillIns.getSkillItemInfo(skillId)
        if isWsSkill:
            wsSkills = BigWorld.player().wsSkills
            if skillId in wsSkills.keys():
                skillInfo['skillLv'] = BigWorld.player().wsSkills[skillId].level
                skillInfo['learnedSkill'] = True
        return skillInfo

    def refreshEmotePanel(self):
        cHeight = 0
        MARGIN_Y = 7
        numInLine = NUM_IN_LINE
        scrollWnd = self.widget.generalEmoteScrollWnd
        if self.isFaceEmotion:
            numInLine = FACE_PANEL_NUM_IN_LINE
            scrollWnd = self.widget.emotionView.faceEmotionPanel.emoteScrollWnd
            self.widget.generalEmoteScrollWnd.visible = False
            self.widget.emotionView.faceEmotionPanel.visible = True
        else:
            self.widget.generalEmoteScrollWnd.visible = True
            self.widget.emotionView.faceEmotionPanel.visible = False
        while scrollWnd.canvas.numChildren > 0:
            scrollWnd.canvas.removeChildAt(0)

        for info in self.emoteInfo:
            cateMc = self.widget.getInstByClsName('GeneralSkill_EmoteCate')
            cateMc.cateName.text = info['cateName']
            scrollWnd.canvas.addChild(cateMc)
            cateMc.y = cHeight
            cHeight += cateMc.height + MARGIN_Y
            emotions = info['emotions']
            for i, emotion in enumerate(emotions):
                emoteMc = self.widget.getInstByClsName('GeneralSkill_GeneralIcon')
                emoteMc.x = i % numInLine * SLOT_WIDTH
                emoteMc.y = cHeight + int(i / numInLine) * SLOT_HEIGHT
                emoteMc.emoteId = emotion['id']
                emoteMc.levelField.visible = False
                emoteMc.skillName.textField.text = emotion['name']
                emoteMc.slot.binding = 'emote0.' + str(emoteMc.emoteId)
                emoteMc.slot.setItemSlotData(emotion)
                if emotion.get('remain', 0) > 0:
                    emoteMc.slot.playCooldown(emotion['total'], emotion['remain'])
                else:
                    emoteMc.slot.stopCooldown()
                if emotion['state'] == EMOTE_LIMIT_UNLOCK_STATE:
                    emoteMc.slot.setSlotState(8)
                elif emotion['state'] == EMOTE_EXPIRE_STATE:
                    emoteMc.slot.setSlotState(2)
                if emotion['state'] in (EMOTE_LOCK_STATE, EMOTE_EXPIRE_STATE):
                    ASUtils.setMcEffect(emoteMc.slot, 'gray')
                else:
                    ASUtils.setMcEffect(emoteMc.slot, '')
                emoteMc.addEventListener(events.MOUSE_CLICK, self.slotClickListener, False, 0, True)
                emoteMc.slot.dragable = True
                scrollWnd.canvas.addChild(emoteMc)

            cHeight += math.ceil(1.0 * len(emotions) / numInLine) * SLOT_HEIGHT + MARGIN_Y

        scrollWnd.refreshHeight()

    def slotClickListener(self, *args):
        e = ASObject(args[3][0])
        isRightBtn = False
        if e.buttonIdx == uiConst.RIGHT_BUTTON:
            isRightBtn = True
        self.useEmote(e.target.parent.emoteId, isRightBtn)

    def useEmote(self, emoteId, isRightButton):
        p = BigWorld.player()
        if utils.needDisableUGC() and emoteId in range(1009, 1019):
            p.showGameMsg(GMDD.data.CHATROOM_MSG_TABOO, ())
            return
        emoteId = self.getRealEmoteId(emoteId)
        if not emoteId:
            return
        ed = ED.data.get(emoteId, {})
        type = ed.get('type', 0)
        needUnlock = ed.get('needUnlock', 0)
        p = BigWorld.player()
        if isRightButton and type == const.EMOTE_TYPE_FACE:
            self.setCurFaceEmote(emoteId)
            self.tryFaceEmote(int(emoteId))
        else:
            if needUnlock and not p.getSocialEmoteEnableFlags(emoteId):
                return
            p.wantToDoEmote(emoteId)
            self.tryFaceEmote(int(emoteId))

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

    def getFaceEmoteInfo(self):
        p = BigWorld.player()
        info = self.getEmoteInfoById(p.curFaceEmoteId)
        return info

    def initHeadGen(self):
        if not self.headGen:
            self.headGen = capturePhoto.EmoteActionPhotoGen.getInstance('gui/taskmask.tga', 396)
        self.headGen.initFlashMesh()
        self.headGen.setModelFinishCallback(self.afterPlayerModelFinished)

    def takePhoto3D(self):
        if not self.headGen:
            self.headGen = capturePhoto.EmoteActionPhotoGen.getInstance('gui/taskmask.tga', 396)
        self.headGen.startCaptureEnt(BigWorld.player())

    def resetHeadGen(self):
        if self.headGen:
            self.headGen.endCapture()
            self.headGen = None

    def setLoadingIconVisible(self, value):
        if self.widget:
            self.widget.emotionView.faceEmotionPanel.picture.loadingIcon.visible = value

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

    def moveEmoteIcon(self, fromId, toId):
        if toId == FACE_EMOTE_SLOT and FED.data.get(fromId):
            self.setCurFaceEmote(fromId)
            self.tryFaceEmote(fromId)

    def getEntPosition(self, dist):
        if not dist:
            dist = 10
        p = BigWorld.player()
        yaw = p.yaw
        x = math.sin(yaw)
        z = math.cos(yaw)
        position = p.position + (x * dist, 0, z * dist)
        return position

    def canUseSkill(self):
        p = BigWorld.player()
        if gameglobal.rds.ui.skill.inAirBattleState():
            return False
        if p._isOnZaijuOrBianyao() or p.inRiding() or p.inWenQuanState:
            return False
        if not p.stateMachine.checkStatus(const.CT_SOCIAL_ACTION):
            return False
        return True

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
            emoteInfo['state'] = self.getEmoteUnlockState(emoteId)
            self.setEmoteCoolDown(emoteId, emoteInfo)
            ret.append(emoteInfo)

        return ret

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

    def getEmotePath(self, key):
        data = ED.data.get(key)
        if data:
            p = BigWorld.player()
            itemNos = data.get('itemNos', [])
            eType = data.get('type', 0)
            icon = 'icon'
            state = self.getEmoteUnlockState(key)
            if itemNos:
                icon = 'icon2'
                equipIds = self.getEquipId()
                for itemNo in itemNos:
                    if itemNo in equipIds:
                        icon = 'icon'

            elif eType == const.EMOTE_TYPE_FACE:
                if self.getEmoteExpireRemainTime(key, False) == EMOTE_LOCK_STATE:
                    icon = 'icon2'
            elif eType == const.EMOTE_TYPE_ACTION:
                funcType = data.get('funcType', 0)
                if funcType == uiConst.EMOTE_FUNTYPE_COUPLE_EMOTE and eType == const.EMOTE_TYPE_ACTION:
                    coupleEmoteId = int(data.get('res', gametypes.COUPLE_EMOTE_TYPE_PRINCESS_HUG))
                    cebd = CEBD.data.get(coupleEmoteId)
                    if cebd.get('needFlag') and not p.getEmoteEnableFlags(coupleEmoteId):
                        icon = 'icon2'
                elif not funcType:
                    needUnlock = data.get('needUnlock', 0)
                    if needUnlock and not p.getSocialEmoteEnableFlags(key):
                        icon = 'icon2'
            elif eType == const.EMOTE_TYPE_EMOTION:
                needUnlock = data.get('needUnlock', 0)
                if needUnlock and not p.getSocialEmoteEnableFlags(key):
                    icon = 'icon2'
            return 'emote/%s.dds' % data.get(icon, '')

    def getEquipId(self):
        equipmentId = []
        for equip in BigWorld.player().equipment:
            if equip:
                equipmentId.append(equip.id)

        return equipmentId

    def getEmoteExpireRemainTime(self, key, isTimeOrState = True):
        p = BigWorld.player()
        needUnlock = FED.data.get(key, {}).get('needUnlock', 0)
        keyMap = p.faceEmoteExpire.get(key, {})
        tExpire = keyMap.get('tExpire', 1)
        if not needUnlock or p.isValidVipProp(gametypes.VIP_SERVICE_UNLOCK_FACE_EMOTE) or tExpire == const.FACE_EMOTE_VALID_TIME_INFINITE:
            if isTimeOrState:
                return None
            return EMOTE_UNLOCK_STATE
        remainTime = tExpire - utils.getNow()
        if remainTime > 0:
            if isTimeOrState:
                return remainTime
            return EMOTE_LIMIT_UNLOCK_STATE
        elif keyMap != {}:
            if isTimeOrState:
                return None
            return EMOTE_EXPIRE_STATE
        elif isTimeOrState:
            return None
        else:
            return EMOTE_LOCK_STATE

    def getEmoteUnlockState(self, emoteId):
        p = BigWorld.player()
        state = EMOTE_UNLOCK_STATE
        data = ED.data.get(emoteId, {})
        eType = data.get('type', 0)
        needUnlock = data.get('needUnlock', 0)
        if eType == const.EMOTE_TYPE_FACE:
            state = self.getEmoteExpireRemainTime(emoteId, False)
        elif needUnlock and not p.getSocialEmoteEnableFlags(emoteId):
            state = EMOTE_LOCK_STATE
        else:
            state = EMOTE_UNLOCK_STATE
        return state

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

    def setCurFaceEmote(self, emoteId):
        p = BigWorld.player()
        state = self.getEmoteExpireRemainTime(emoteId, False)
        if state == EMOTE_EXPIRE_STATE:
            p.showGameMsg(GMDD.data.FACE_EMOTE_SET_FAILED_EXPIRED, ())
        elif state == EMOTE_LOCK_STATE:
            p.showGameMsg(GMDD.data.FACE_EMOTE_SET_FAILED_UNLOCK, ())
        elif p.stateMachine.checkStatus(const.CT_EQUIP_FACE_EMOTE):
            p.cell.setCurFaceEmote(emoteId)

    def getEmoteInfoById(self, emoteId):
        emoteInfo = {}
        if emoteId == 0:
            return emoteInfo
        emoteInfo['id'] = emoteId
        emoteInfo['name'] = ED.data.get(emoteId, {}).get('name', '')
        emoteInfo['iconPath'] = self.getEmotePath(emoteId)
        emoteInfo['state'] = self.getEmoteUnlockState(emoteId)
        return emoteInfo

    def getTip(self, emoteId):
        data = ED.data.get(emoteId)
        if data:
            shortCommands = data.get('shortcommand', '')
            tips = ''
            if shortCommands:
                tips = gameStrings.EMOTE_ACTION_SHORT_TIPS % shortCommands[0]
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
