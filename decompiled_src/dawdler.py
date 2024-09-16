#Embedded file name: /WORKSPACE/data/entities/client/dawdler.o
import math
import random
import BigWorld
import const
import copy
import gameglobal
import gamelog
import gametypes
import formula
import keys
import clientcom
import appSetting
from guis import uiConst
from impl.impPot import ImpPot
from iNpc import INpc
from iDisplay import IDisplay
from sfx import sfx
from helpers import weaponModel
from helpers import action as ACT
from helpers import modelServer as MS
from helpers import charRes
from helpers import tintalt
from callbackHelper import Functor
from data import dawdler_data as DRD
from data import dialogs_data as GD
from data import npc_model_client_data as NMCD
from data import sys_config_data as SCD
from data import dawdler_action_data as DAD
from cdata import game_msg_def_data as GMDD

class Dawdler(INpc, IDisplay, ImpPot):
    COLLIDE_LEFTFRONT = 0
    COLLIDE_RIGHTFRONT = 1
    COLLIDE_LEFTBACK = 2
    COLLIDE_RIGHTBACK = 3

    def __init__(self):
        super(Dawdler, self).__init__()
        self.hp = 1000000
        self.trapId = None
        self.refreshOnTimerHandle = None

    def getItemData(self):
        defaultModel = {'model': gameglobal.defaultModelID,
         'dye': 'Default'}
        nd = NMCD.data.get(self.npcId, None)
        if not nd:
            gamelog.error('zf11:Dawdler.getItemData model not found ', self.npcId)
            return defaultModel
        isGraveState = gameglobal.rds.ui.mapGameMapV2.isGraveState()
        if isGraveState:
            if hasattr(self, 'getOpacityValue'):
                opacityValue = self.getOpacityValue()
                if opacityValue[0] == gameglobal.OPACITY_FULL:
                    nd = copy.deepcopy(NMCD.data.get(self.npcId, None))
                    nd['extraTint'] = SCD.data.get('ghostmatte', 'refaction002')
            else:
                nd = copy.deepcopy(NMCD.data.get(self.npcId, None))
                nd['extraTint'] = SCD.data.get('ghostmatte', 'refaction002')
        modelId = nd.get('model', 0)
        if modelId == 0:
            return defaultModel
        if modelId > const.MODEL_AVATAR_BORDER and self.fashionId:
            return self.getFashionInfo(modelId, nd)
        return nd

    def getFashionInfo(self, modelId, extra = None):
        oldItemData = clientcom._getModelData(modelId)
        bodyType = oldItemData.get('bodyType', 0)
        sex = oldItemData.get('sex', 0)
        if self.fashionId:
            modelId = charRes.transBodyType(sex, bodyType)
            fashionId = self.fashionId * 100000 + modelId
            if fashionId > const.MODEL_AVATAR_BORDER:
                newData = clientcom._getModelData(fashionId)
            else:
                newData = None
        else:
            newData = None
        if newData:
            for part in ('hand', 'body', 'leg', 'shoe', 'dyesDict'):
                if newData.has_key(part):
                    oldItemData[part] = newData[part]

        if extra:
            school = oldItemData.get('school', 0)
            oldItemData.update(extra)
            if oldItemData.has_key('model'):
                oldItemData.pop('model')
            if school:
                oldItemData['school'] = school
        return oldItemData

    def needMoveNotifier(self):
        return True

    def movingNotifier(self, isMoving, moveSpeed = 1.0):
        self.isMoving = isMoving
        if isMoving:
            self.fashion.stopAction()
        elif self.isPlaySchemedIdleAct():
            self.fashion.playSingleAction(self.idleActName)
        if not self.isMoving and gameglobal.rds.ui.multiNpcChat.uiAdapter.quest.npcType == uiConst.NPC_MULTI and gameglobal.rds.ui.multiNpcChat.uiAdapter.quest.isShow:
            self.faceTo(BigWorld.player())

    def isPlaySchemedIdleAct(self):
        if self.idleActName and not self.isMoving:
            return True
        return False

    def enterWorld(self):
        super(Dawdler, self).enterWorld()
        self.trapId = BigWorld.addPot(self.matrix, SCD.data.get('npcDialogLength', 4), self.trapCallback)
        self.addTrapEvent()

    def leaveWorld(self):
        self.npcTrapCallback(True)
        super(Dawdler, self).leaveWorld()
        if self.trapId != None:
            BigWorld.delPot(self.trapId)
            self.trapId = None
        self.delTrapEvent()
        if self.refreshOnTimerHandle:
            BigWorld.cancelCallback(self.refreshOnTimerHandle)
            self.refreshOnTimerHandle = None

    def afterModelFinish(self):
        super(Dawdler, self).afterModelFinish()
        drd = DRD.data.get(self.npcId, {})
        if drd.get('useAvatarFilter', False):
            self.filter = BigWorld.AvatarFilter()
        else:
            self.filter = BigWorld.AvatarDropFilter()
        if self.modelServer and self.modelServer.avatarConfig:
            self.setAvatarConfig(self.modelServer.avatarConfig.get('avatarConfig', ''))
        nmcd = NMCD.data.get(self.npcId, None)
        if not nmcd:
            return
        if nmcd.has_key('feetDist'):
            self.filter.enableBodyPitch = True
            self.filter.feetDist = nmcd['feetDist']
        collideRadius = nmcd.get('collideRadius', 0)
        if collideRadius:
            self.collideWithPlayer = True
            self.collideRadiusRatio = collideRadius
        p = BigWorld.player()
        if p and p.quests and nmcd and nmcd.has_key('triggerEff'):
            for questId in p.quests:
                effScale = nmcd['effScale'] if nmcd.has_key('effScale') else nmcd.get('modelScale', 1)
                chaterInfo = p.getQuestData(questId, const.QD_QUEST_CHAT)
                isTriggered = chaterInfo and chaterInfo.get(self.npcId, 1)
                if isTriggered or not chaterInfo:
                    continue
                if self.npcId in chaterInfo.keys():
                    fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
                     self.getBasicEffectPriority(),
                     self.model,
                     nmcd['triggerEff'],
                     sfx.EFFECT_LIMIT))
                    if fxs:
                        for fx in fxs:
                            fx.scale(effScale, effScale, effScale)

                        self.addFx(nmcd['triggerEff'], fxs)

        self.refreshOpacityOnTimer()
        if self.actionStatus:
            self.playActions((self.actionStatus,))
        lifeEquip = drd.get('lifeEquip', None)
        if lifeEquip:
            self.modelServer.lifeSkillModel.equipItem(lifeEquip)
        self.addTint()
        self.addLingShiExtraTint()

    def addLingShiExtraTint(self):
        p = BigWorld.player()
        if not getattr(p, 'lingShiFlag', False):
            return
        lingShiTintName = DRD.data.get(self.npcId, {}).get('lingShiTintName', '')
        if lingShiTintName:
            tintalt.ta_reset(self.allModels)
            tintalt.ta_add(self.allModels, lingShiTintName, tintType=tintalt.NPC_LINGSHI)

    def delLingShiExtraTint(self):
        tintalt.ta_reset(self.allModels)

    def addTint(self):
        tint = self.getItemData().get('extraTint', None)
        if tint:
            tintalt.ta_add(self.allModels, tint)

    def use(self):
        p = BigWorld.player()
        if gameglobal.rds.configData.get('enableForbidNpcAndDawdler', False):
            nd = NMCD.data.get(self.npcId, None)
            if nd:
                p.showGameMsg(GMDD.data.FORBIDDEN_MAP_GAME_GRAVE, nd.get('name', ''))
            return
        if p.life == gametypes.LIFE_DEAD:
            p.showGameMsg(GMDD.data.FORBIDDEN_WRONG_LIFE, ())
            return
        if self.forbidUse():
            return
        if p.inBooth():
            return
        super(Dawdler, self).use()
        p.cell.useDawdler(self.id)
        soundIdx = self.getItemData().get('useNpcSound', 0)
        gameglobal.rds.sound.playSound(soundIdx)

    def faceTo(self, target):
        if not target:
            return
        nd = NMCD.data.get(self.npcId, None)
        if not nd:
            return
        keepYaw = nd.get('keepYaw', 0)
        if keepYaw:
            return
        self.filter.setYaw((target.position - self.position).yaw)

    def faceDirection(self, yaw):
        self.filter.setYaw(yaw)

    def getDefaultChatId(self):
        pass

    def showMultiNpcChatWin(self, isQuestChat = True):
        chatIds = []
        if isQuestChat:
            player = BigWorld.player()
            drd = DRD.data.get(self.npcId, {})
            if drd.has_key('quests'):
                questIds = drd['quests']
                chatIds = drd.get('chatIds', [])
                for i, questId in enumerate(questIds):
                    if questId in player.quests:
                        if i < len(chatIds):
                            chatIds = [chatIds[i]]
                            break

        else:
            chatIds = DRD.data.get(self.npcId, {}).get('defaultChatId', [])
        if chatIds:
            chatId = chatIds[0]
            if chatId in GD.data:
                gameglobal.rds.ui.multiNpcChat.openMultiNpcChatWindow(self.id, self.npcId, chatIds, isQuestChat)
            else:
                BigWorld.player().showChatWindow(chatId, self.id, Functor(self.onChatChoice, chatId))
            self.playChatSound(isQuestChat)

    def playChatSound(self, isQuestChat):
        drd = DRD.data.get(self.npcId, {})
        if not isQuestChat:
            gossipType = drd.get('gossipType', None)
        else:
            gossipType = drd.get('gossipQuestType', None)
        if gossipType:
            gameglobal.rds.sound.playSound(gossipType)

    def questChat(self):
        if not getattr(self, 'isMoving', False):
            self.faceTo(BigWorld.player())
            actionName = self.fashion.action.getTalkAction()
            self.fashion.playSingleAction(actionName)
        self.showMultiNpcChatWin()

    def onChatChoice(self, chatId):
        if not self.inWorld:
            return
        drd = DRD.data[self.npcId]
        if drd.has_key('chatIds'):
            if chatId in drd['chatIds']:
                BigWorld.player().cell.onQuestDialog(self.id, chatId)

    def defaultChat(self):
        if not getattr(self, 'isMoving', False):
            self.faceTo(BigWorld.player())
            actionName = self.fashion.action.getTalkAction()
            self.fashion.playSingleAction(actionName)
        self.showMultiNpcChatWin(False)

    def getModelScale(self):
        nd = NMCD.data.get(self.npcId, {})
        scale = nd.get('modelScale', 1.0)
        return (scale, scale, scale)

    def playActions(self, actNames):
        if type(actNames) != tuple or len(actNames) < 1:
            return
        self.fashion.stopAction()
        self.fashion.playActionSequence(self.model, actNames, None)

    def playLifeActions(self, actionId):
        self.fashion.stopAllActions()
        actionData = DAD.data.get(actionId, {})
        if actionData:
            actions = []
            startActions = actionData.get('startActions', ())
            if startActions:
                actions.extend(startActions)
            loopActions = actionData.get('loopActions', ())
            if loopActions:
                actions.extend(loopActions)
            lifeEquip = actionData.get('lifeEquip', None)
            actionTime = actionData.get('actionTime', [])
            duration = sum(actionTime[0:2]) if actionTime else 0
            if lifeEquip:
                self.releaseLifeModel()
                lifeSkillModel = self.modelServer.lifeSkillModel
                lifeSkillModel.equipItem(lifeEquip)
                lifeSkillModel.attach(self.model)
            if actions:
                BigWorld.callback(0, Functor(self.realPlayLifeActions, actionId, actions, duration, lifeEquip))

    def realPlayLifeActions(self, actionId, actions, duration, lifeEquip):
        if not self.inWorld:
            return
        if actions:
            self.fashion.playAction(actions, ACT.LIFE_ACTION)
        BigWorld.callback(duration, Functor(self.playLifeActionsEnd, actionId, lifeEquip))

    def playLifeActionsEnd(self, actionId, lifeEquip):
        if not self.inWorld:
            return
        actionData = DAD.data.get(actionId, {})
        if not actionData:
            return
        endActions = actionData.get('endActions', ())
        if not endActions:
            if lifeEquip:
                self.releaseLifeModel()
                return
        else:
            self.fashion.playActionSequence(self.model, endActions, Functor(self.playLifeActionsEndCB, lifeEquip))

    def playLifeActionsEndCB(self, lifeEquip):
        if not self.inWorld:
            return
        if lifeEquip:
            self.releaseLifeModel()

    def releaseLifeModel(self):
        lifeSkillModel = self.modelServer.lifeSkillModel
        if lifeSkillModel.state == weaponModel.ATTACHED:
            lifeSkillModel.detach()
        lifeSkillModel.release()

    def stopAllActions(self):
        self.fashion.stopAllActions()

    def playCollideAction(self):
        collideActions = self.fashion.action.getCollideAction(self.fashion)
        if not collideActions:
            return
        collideDir = self.__getCollideWithPlayerDir()
        if self.fashion.doingActionType() not in [ACT.NPC_COLLIDE_ACTION]:
            self.fashion.playAction([collideActions[collideDir]], ACT.NPC_COLLIDE_ACTION, None, blend=True)
            self.__playCollideChat()

    def __playCollideChat(self):
        nd = NMCD.data.get(self.npcId, {})
        collideChats = nd.get('collideChat', False)
        if not collideChats:
            return
        chatId = random.choice(collideChats)
        chatData = GD.data.get(chatId, {})
        chatMsg = chatData.get('details', '')
        if self.topLogo:
            self.topLogo.setChatMsg(chatMsg)

    def __getCollideWithPlayerDir(self):
        p = BigWorld.player()
        angle = self.getTgtAngle(p)
        if angle >= -math.degrees(math.pi / 2) and angle <= 0.0:
            return Dawdler.COLLIDE_LEFTFRONT
        elif angle > 0.0 and angle <= math.degrees(math.pi / 2):
            return Dawdler.COLLIDE_RIGHTFRONT
        elif angle > math.degrees(math.pi / 2) and angle <= math.degrees(math.pi):
            return Dawdler.COLLIDE_LEFTBACK
        else:
            return Dawdler.COLLIDE_RIGHTBACK

    def needCollideAction(self):
        nd = NMCD.data.get(self.npcId, None)
        return nd.get('collideRadius', False)

    def npcTrapCallback(self, leaveWorld = False):
        if self.forbidUse():
            return
        p = BigWorld.player()
        if (self.position - p.position).length <= SCD.data.get('npcDialogLength', 4) and not leaveWorld:
            if self.getNpcPriority() in (gameglobal.NPC_WITH_NO_CHAT, gameglobal.NPC_WITH_NO_FUNC):
                return
            p.npcTrapInCallback((self,))
        else:
            p.npcTrapOutCallback((self,))

    def trapCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        if self.forbidUse():
            return
        p = BigWorld.player()
        if enteredTrap:
            if self.getNpcPriority() in (gameglobal.NPC_WITH_NO_CHAT, gameglobal.NPC_WITH_NO_FUNC):
                return
            p.npcTrapInCallback((self,))
        else:
            p.npcTrapOutCallback((self,))

    def enterTopLogoRange(self, rangeDist = -1):
        self.isEnterTopLogoRange = True
        super(Dawdler, self).enterTopLogoRange(rangeDist)
        notTurn = NMCD.data.get(self.npcId, {}).get('notTurn', 0)
        if not notTurn:
            self.fashion.beginHeadTracker(False)
        if self.topLogo:
            if gameglobal.gHideNpcName:
                self.topLogo.hideName(True)
            if gameglobal.gHideNpcTitle:
                self.topLogo.hideTitleName(True)

    def leaveTopLogoRange(self, rangeDist = -1):
        self.fashion.stopHeadTracker()
        super(Dawdler, self).leaveTopLogoRange(rangeDist)

    def needBlackShadow(self):
        nmcd = NMCD.data.get(self.npcId, {})
        noBlackUfo = nmcd.get('noBlackUfo', False)
        return not noBlackUfo

    def getNpcPriority(self):
        drd = DRD.data.get(self.npcId, {})
        player = BigWorld.player()
        if drd.has_key('quests'):
            questIds = drd['quests']
            for questId in questIds:
                if questId in player.quests:
                    return gameglobal.NPC_WITH_AVAILABLE_QUEST

        return gameglobal.NPC_WITH_NO_FUNC

    def getOpacityValue(self):
        if self.needToHide():
            return (gameglobal.OPACITY_HIDE, False)
        opacityVal = super(Dawdler, self).getOpacityValue()
        drd = DRD.data.get(self.npcId, {})
        if drd.has_key('islingshi'):
            return clientcom.getEntityLingShiOpacityValue(drd)
        if drd.has_key('displayXingjiTimes'):
            xingjiTimes = drd['displayXingjiTimes']
            if not formula.isInXingJiTimeIntervals(xingjiTimes):
                return (gameglobal.OPACITY_HIDE, False)
        return opacityVal

    def refreshOpacityOnTimer(self):
        if not self.inWorld:
            return
        self.refreshOpacityState()
        nextTime = 0
        drd = DRD.data.get(self.npcId)
        if drd and drd.has_key('displayXingjiTimes'):
            for startTime, endTime in drd['displayXingjiTimes']:
                tmpNextTime = formula.getRealTimeToAXingJiMoment(startTime)
                if nextTime == 0 or tmpNextTime < nextTime:
                    nextTime = tmpNextTime
                tmpNextTime = formula.getRealTimeToAXingJiMoment(endTime)
                if nextTime == 0 or tmpNextTime < nextTime:
                    nextTime = tmpNextTime

        if self.refreshOnTimerHandle:
            BigWorld.cancelCallback(self.refreshOnTimerHandle)
            self.refreshOnTimerHandle = None
        if nextTime > 0:
            self.refreshOnTimerHandle = BigWorld.callback(nextTime + 2, self.refreshOpacityOnTimer)

    def set_actGroupId(self, old):
        actGroupId = self.actGroupId if self.actGroupId else self.getItemData().get('actGroupid', None)
        if self.fashion and self.fashion.action:
            self.fashion.action.actGroupId = actGroupId
            idleCap = self.fashion.action.getActCaps()
            if isinstance(idleCap, tuple):
                self.am.matchCaps = list(idleCap)
            else:
                self.am.matchCaps = [idleCap, keys.CAPS_GROUND]

    def set_fashionId(self, old):
        modelId = NMCD.data.get(self.npcId, {}).get('model', 0)
        itemData = self.getFashionInfo(modelId)
        MS.loadModelByItemData(self.id, gameglobal.DEFAULT_THREAD, self.modelServer._singlePartModelFinish, itemData, True)

    def attachLifeEquip(self, lifeEquip):
        if lifeEquip:
            self.releaseLifeModel()
            lifeSkillModel = self.modelServer.lifeSkillModel
            lifeSkillModel.equipItem(lifeEquip)
            lifeSkillModel.attach(self.model)

    def detachLifeEquip(self):
        self.releaseLifeModel()

    def getTopIcon(self):
        return NMCD.data.get(self.npcId, {}).get('topIcon')

    def isFunctionNpc(self):
        drd = DRD.data.get(self.npcId, {})
        questIds = drd.get('quests', None)
        if questIds:
            return True
        return False

    def getShowLoadLv(self):
        if self.isFunctionNpc():
            return gameglobal.SHOWLOADDEFAULTLV
        npcData = NMCD.data.get(self.npcId, {})
        noNeedHide = npcData.get('noNeedHide', False)
        if noNeedHide:
            return gameglobal.SHOWLOADDEFAULTLV
        showLoadLv = npcData.get('showLoadLv', gameglobal.SHOWLOADDEFAULTLV)
        if clientcom.getNpcModelMaxCnt() < gameglobal.CURRENT_NPC_MODEL_CNT:
            return gameglobal.SHOWLOADMAXLV
        return showLoadLv

    def needToHide(self):
        if not gameglobal.rds.configData.get('enableHideNpc', True):
            return False
        p = BigWorld.player()
        if p.spaceNo != const.SPACE_NO_BIG_WORLD:
            return False
        showLoadLv = self.getShowLoadLv()
        videoSettingLv = appSetting.VideoQualitySettingObj.getVideoQualityLv()
        if videoSettingLv >= showLoadLv:
            return False
        return True
