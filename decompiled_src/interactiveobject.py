#Embedded file name: /WORKSPACE/data/entities/client/interactiveobject.o
import random
import BigWorld
import Math
import const
import utils
import gameglobal
import gamelog
import formula
import clientcom
import gametypes
from helpers import modelServer
from guis import ui
from guis import cursor
from helpers import editorHelper
from sfx import sfx
from helpers import fashion
from iClient import IClient
from sMath import inRange3D
from guis import uiConst
from data import interactive_data as ID
from data import interactive_type_data as ITD
from data import interactive_chat_msg_data as ICMD
from data import couple_emote_basic_data as CEBD
from cdata import game_msg_def_data as GMDD
from cdata import furniture_model_index_data as FMID

class InteractiveObject(IClient):

    def __init__(self):
        super(InteractiveObject, self).__init__()
        self.roleName = ''
        self.trapId = None
        self.itemData = None
        self.modelServer = None
        self.fashion = None
        self.showName = ID.data.get(self.objectId, {}).get('name')
        self.chatIdleProbability = 100
        self.chatTime = 10.0
        self.chatHandle = None
        self.musicTrapId = None
        player = BigWorld.player()
        if player.spaceInHomeOrLargeRoom():
            self.roleName = ''
        else:
            self.roleName = self.showName

    def needNotifyMusic(self):
        return self.getItemData().get('needNotifyMusic', True)

    def enterWorld(self):
        super(InteractiveObject, self).enterWorld()
        data = self.getItemData()
        model = data.get('model', 0)
        if model > const.MODEL_AVATAR_BORDER:
            self.modelServer = modelServer.AvatarModelServer(self)
            td = clientcom._getModelData(model)
            self.modelServer.bodyUpdateFromData(td)
            self.initPhysique(td)
            self.fashion = fashion.Fashion(self.id)
        else:
            self.modelServer = modelServer.SimpleModelServer(self, self.isUrgentLoad())
        if data.get('useDrop'):
            self.filter = BigWorld.AvatarDropFilter()
        else:
            self.filter = BigWorld.DumbFilter()
        self.isLeaveWorld = False
        maxClickRadius = ID.data.get(self.objectId, {}).get('maxClickRadius', 2)
        if maxClickRadius > 0:
            self.trapId = BigWorld.addPot(self.matrix, maxClickRadius, self.trapCallback)
        if self.needNotifyMusic():
            notifyMusicDist = data.get('notifyMusicDist', 2)
            self.musicTrapId = BigWorld.addPot(self.matrix, notifyMusicDist, self.trapMusicCallback)
        noStory = ID.data.get(self.objectId, {}).get('noStory', 0)
        if not noStory:
            BigWorld.player().showInteractiveObjStory(self.objectId)
        p = BigWorld.player()
        if p.spaceInHomeOrLargeRoom():
            editorHelper.instance().addInteractiveObject(self.id)
        self.chatInRoom()

    def initPhysique(self, itemData):
        bodyType = itemData.get('bodyType', 0)
        school = itemData.get('school', 0)
        sex = itemData.get('sex', const.SEX_MALE)
        self.physique.sex = sex
        self.physique.school = school
        self.physique.bodyType = bodyType

    def triggerTrap(self, enteredTrap):
        maxClickRadius = ID.data.get(self.objectId, {}).get('maxClickRadius', 2)
        if not maxClickRadius:
            return
        if not inRange3D(maxClickRadius, BigWorld.player().position, self.position):
            return
        if not self.inWorld:
            return
        self.trapCallback(enteredTrap, 0)

    def afterModelFinish(self):
        super(InteractiveObject, self).afterModelFinish()
        self.model.setModelNeedHide(0, 0.5)
        self.setTargetCapsUse(True)
        self.createObstacleModel()
        self.filter = BigWorld.DumbFilter()
        self.refreshOpacityState()
        effects = self.getItemData().get('effects', [])
        self.refreshInteractiveAvatar()
        for eff in effects:
            sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
             self.getBasicEffectPriority(),
             self.model,
             eff,
             sfx.EFFECT_UNLIMIT))

        showAction = self.getDefaultShowAction()
        if showAction:
            try:
                self.model.action(showAction)()
            except Exception as e:
                gamelog.debug('m.l@InteractiveObject.afterModelFinish action error', e.message)

    def getSeekDist(self):
        return ID.data.get(self.objectId, {}).get('maxClickRadius', 0)

    def getNavPoint(self):
        return ID.data.get(self.objectId, {}).get('navPoint')

    def getType(self):
        return ID.data.get(self.objectId, {}).get('type', 0)

    def getAttachScale(self):
        scale = ID.data.get(self.objectId, {}).get('modelScale', 1.0)
        return 1.0 / scale

    def showTargetUnitFrame(self):
        return False

    def getFKey(self):
        return ID.data.get(self.objectId, {}).get('fKeyId', 161)

    def trapCallback(self, enteredTrap, handle):
        p = BigWorld.player()
        if enteredTrap:
            if not self.inWorld:
                return
            opaVal = self.getOpacityValue()
            if opaVal[0] == gameglobal.OPACITY_HIDE:
                return
            ins = editorHelper.instance()
            if ins and ins.editMode and self.ownerUUID in ins.bwEntityIdMap:
                return
            p.interactiveTrapCallback((self,))
        else:
            p.interactiveTrapCallback([])

    def createObstacleModel(self):
        iData = ID.data.get(self.objectId, {})
        obstacleModel = iData.get('obstacleModel', 0)
        scale = iData.get('obstacleScale', 1.0)
        modelName = None
        if obstacleModel:
            if obstacleModel in FMID.data:
                modelName = FMID.data.get(obstacleModel, {}).get('modelPath', '')
            else:
                modelName = 'char/%i/%i.model' % (obstacleModel, obstacleModel)
        if modelName:
            scaleMatrix = Math.Matrix()
            scaleMatrix.setScale((scale, scale, scale))
            mp = Math.MatrixProduct()
            mp.a = scaleMatrix
            mp.b = self.matrix
            BigWorld.fetchObstacleModel(modelName, mp, True, self._onLoadObstacleModel)

    def _onLoadObstacleModel(self, model):
        if model:
            self.obstacleModel = model
            self.addModel(model)
            self.obstacleModel.visible = False
            model.setEntity(self.id)
            model.setCollide(True)

    def leaveWorld(self):
        super(InteractiveObject, self).leaveWorld()
        if self.chatHandle:
            BigWorld.cancelCallback(self.chatHandle)
            self.chatHandle = None
        if self.avatarMap:
            try:
                for _entId, idx in self.avatarMap.iteritems():
                    cleanList = []
                    seatNode = utils.getInteractiveNodeName(idx)
                    for item in self.model.node(seatNode).attachments:
                        cleanList.append(item)

                    for item in cleanList:
                        self.model.node(seatNode).detach(item)

            except:
                pass

        if self.trapId != None:
            BigWorld.delPot(self.trapId)
            self.trapId = None
        p = BigWorld.player()
        if self.musicTrapId:
            BigWorld.delPot(self.musicTrapId)
            self.musicTrapId = None
            notifyMusicId = self.getItemData().get('notifyMusicId', 0)
            p.notifyMusicCallBack(False, notifyMusicId)
        self.isLeaveWorld = True
        self.trapCallback(False, None)
        self.itemData = None
        if p.spaceInHomeOrLargeRoom():
            editorHelper.instance().removeInteractiveObject(self.id)
        if self.modelServer:
            self.modelServer.release()
        if self.fashion:
            self.fashion.release()
        if self.coupleEmote:
            if self.coupleEmote[1] == p.id or self.coupleEmote[2] == p.id:
                p.cell.cancelCoupleEmote()
                p.hideZaijuUI(uiConst.ZAIJU_SHOW_TYPE_EXIT)
        gameglobal.rds.ui.interactiveObj.closeNodeSelectWidgetById(self.id)

    def getItemData(self):
        if self.itemData:
            return self.itemData
        data = dict(ID.data.get(self.objectId, {}))
        if data.has_key('furnitureModel'):
            furnitureModel = data['furnitureModel']
            data['fullPath'] = FMID.data.get(furnitureModel, {}).get('modelPath', '')
            data.pop('model', None)
        self.itemData = data
        return self.itemData

    def needBlackShadow(self):
        return not self.getItemData().get('noBlackUfo', False)

    def getModelScale(self):
        data = self.getItemData()
        scale = data.get('modelScale', 1.0)
        self.model.scale = (scale, scale, scale)
        return (scale, scale, scale)

    def getTopLogoHeight(self):
        return self.getItemData().get('topLogoHeight', super(InteractiveObject, self).getTopLogoHeight())

    def needAttachUFO(self):
        return not self.getItemData().get('noUfo', False)

    def getValidNodeIdx(self):
        canInteractiveCnt = ID.data.get(self.objectId, {}).get('canInteractiveCnt', 1)
        indexes = self.avatarMap.values()
        for i in xrange(canInteractiveCnt):
            if i not in indexes:
                return i

    def use(self):
        iData = ID.data.get(self.objectId, {})
        _useType = iData.get('useType', 0)
        isHomeStorage = iData.get('isHomeStorage', 0)
        p = BigWorld.player()
        if _useType == const.INTERACTIVE_PERSONALZONE_USETYPE:
            ins = editorHelper.instance()
            if ins.ownerGbID:
                p.getPersonalSysProxy().openZoneOther(ins.ownerGbID)
        elif isHomeStorage == const.INTERACTIVE_HOME_STORAGE_SHOW:
            if not gameglobal.rds.configData.get('enableStorageHome', False):
                p.showGameMsg(GMDD.data.HOME_STORAGE_NOT_OPEN, ())
                return
            curPage = gameglobal.rds.ui.homeTermsStorage.getPage()
            p.cell.pullStorageHome(curPage, 0)
        else:
            p = BigWorld.player()
            if p.interactiveObjectEntId > 0:
                return
            if self.canInteractiveCnt == 0:
                p.showGameMsg(GMDD.data.INTERACTIVE_FAILED_FULL, ())
                return
            if self.isOccupied:
                p.showGameMsg(GMDD.data.INTERACTIVE_FAILED_OCCUPIED, ())
                return
            ins = editorHelper.instance()
            if ins and ins.editMode and self.ownerUUID in ins.bwEntityIdMap:
                return
            enterType = iData.get('enterType', 0)
            if enterType == gameglobal.INTERACTIVE_OBJ_ENTER_TYPE_SEQ:
                idx = self.getValidNodeIdx()
                if idx is not None:
                    if not p.stateMachine.checkStatus(const.CT_CLICK_INTERACTIVE_OBJECT):
                        return
                    p.cell.clickInteractiveObject(self.id, idx)
                else:
                    gamelog.debug('m.l@InteractiveObject.use no valid index')
            elif enterType == gameglobal.INTERACTIVE_OBJ_ENTER_TYPE_SELECT:
                gameglobal.rds.ui.interactiveObj.showNodeSelectWidget(self.id)
            elif enterType == gameglobal.INTERACTIVE_OBJ_ENTER_TYPE_MENU and gameglobal.rds.configData.get('enableInteractiveCoupleEmote', False):
                p.lockTarget(self)
                gameglobal.rds.ui.target.showRightMenu(uiConst.MENU_INTERACTIVE_OBJECT, None)
            elif enterType == gameglobal.INTERACTIVE_OBJ_ENTER_TYPE_MINIGAME:
                miniGameId = iData.get('miniGameId', 0)
                if miniGameId:
                    if self.avatarMap:
                        self.miniGameConfirm()
                    else:
                        gameglobal.rds.ui.miniGameRule.show(miniGameId, self.miniGameConfirm)

    def miniGameConfirm(self):
        p = BigWorld.player()
        idx = self.getValidNodeIdx()
        if idx is not None:
            if not p.stateMachine.checkStatus(const.CT_CLICK_INTERACTIVE_OBJECT):
                return
            p.cell.clickInteractiveObject(self.id, idx)
        else:
            gamelog.debug('m.l@InteractiveObject.use no valid index')

    def onTargetCursor(self, enter):
        if enter:
            if ui.get_cursor_state() == ui.NORMAL_STATE:
                ui.set_cursor_state(ui.TARGET_STATE)
                if (self.position - BigWorld.player().position).length > cursor.TALK_DISTANCE:
                    ui.set_cursor(cursor.talk_dis)
                else:
                    ui.set_cursor(cursor.talk)
                ui.lock_cursor()
        elif ui.get_cursor_state() == ui.TARGET_STATE:
            ui.reset_cursor()

    def getInteractiveObjIdx(self, entId):
        if entId not in self.avatarMap.keys():
            return -1
        return self.avatarMap[entId]

    def set_avatarMap(self, old):
        self.refreshInteractiveAvatar()

    def refreshInteractiveAvatar(self):
        if self.avatarMap:
            for entId, _xpIndex in self.avatarMap.iteritems():
                ent = BigWorld.entities.get(entId)
                if not ent or not ent.inWorld:
                    return
                ent.modelServer.enterInteractiveObject()
                if ent == BigWorld.player():
                    gameglobal.rds.ui.interactiveActionBar.show(_xpIndex)
                    gameglobal.rds.ui.interactiveObjMounts.show()
                    type = self.getType()
                    if ITD.data.has_key(type) and not ITD.data.get(type, {}).get('hideUI', False):
                        rewardTotalTime = self.getItemData().get('rewardTotalTime', 120)
                        gameglobal.rds.ui.interactiveObj.showRewardWidget(rewardTotalTime)

    def setVisible(self, value):
        if self.model:
            self.model.visible = value
        if self.obstacleModel:
            self.obstacleModel.setCollide(value)

    def getOpacityValue(self):
        ins = editorHelper.instance()
        player = BigWorld.player()
        if ins and ins.editMode and player.spaceInHomeOrLargeRoom():
            return (gameglobal.OPACITY_HIDE, False)
        if self.isInCoupleRide():
            if self.coupleEmote[2] == self.id:
                emoteId = self.coupleEmote[0]
                if not CEBD.data.get(emoteId).get('noAttachModel', 0):
                    return (gameglobal.OPACITY_HIDE, False)
        return (gameglobal.OPACITY_FULL, True)

    def refreshOpacityState(self):
        super(InteractiveObject, self).refreshOpacityState()
        if not self.inWorld:
            return
        if getattr(self, 'obstacleModel', None):
            opValue = self.getOpacityValue()
            self.obstacleModel.visible = False
            if opValue[0] in (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, gameglobal.OPACITY_HIDE, gameglobal.OPACITY_HIDE_WITHOUT_NAME):
                self.obstacleModel.setCollide(False)
            else:
                self.obstacleModel.setCollide(True)

    def getShowActions(self):
        return self.getItemData().get('showActions', ())

    def getDefaultShowAction(self):
        showActions = self.getShowActions()
        if showActions:
            return showActions[0]

    @property
    def realAspect(self):
        return self.aspect

    @property
    def realPhysique(self):
        return self.physique

    @property
    def realAvatarConfig(self):
        return self.avatarConfig

    @property
    def realSchool(self):
        return self.physique.school

    @property
    def school(self):
        return self.physique.school

    @property
    def inFly(self):
        return 0

    @property
    def bianshen(self):
        return (0, 0)

    @property
    def inCombat(self):
        return 0

    @property
    def weaponState(self):
        return self.weaponInHandState()

    def _isOnZaijuOrBianyao(self):
        return False

    def showLeftWeaponModels(self, show, force = False):
        pass

    def showRightWeaponModels(self, show, force = False):
        pass

    def refreshWeaponVisible(self):
        pass

    def weaponInHandState(self):
        return gametypes.WEAPON_HANDFREE

    def getWeapon(self, isLeft):
        if isLeft:
            return self.realAspect.leftWeapon
        return self.realAspect.rightWeapon

    def getWeaponEnhLv(self, isLeft):
        if isLeft:
            return self.realAspect.leftWeaponEnhLv()
        return self.realAspect.rightWeaponEnhLv()

    def forceUpdateEffect(self):
        pass

    def isInCoupleRide(self, data = None):
        return self.getCoupleEmoteID(data)

    def getCoupleEmoteID(self, data = None):
        if data is None:
            data = getattr(self, 'coupleEmote', (None,))
        if len(data) == 0:
            return
        return data[0]

    def isInCoupleRideAsHorse(self, data = None):
        return self.isInCoupleRide(data) and self.coupleEmote[1] == self.id

    def isInCoupleRideAsRider(self, data = None):
        return self.isInCoupleRide(data) and self.coupleEmote[2] == self.id

    def set_coupleEmote(self, old):
        p = BigWorld.player()
        if not self.isInCoupleRide(old) and self.isInCoupleRide():
            self.modelServer.enterCoupleEmote()
            index = 0
            if self.coupleEmote[2] == self.id:
                index = 1
            interactiveVoiceId = self.getItemData().get('interactiveVoice', {}).get(self.coupleEmote[0], [0, 0])[index]
            if interactiveVoiceId:
                gameglobal.rds.sound.playSound(interactiveVoiceId)
            if p.id in self.coupleEmote:
                p.showZaijuUI(showType=uiConst.ZAIJU_SHOW_TYPE_EXIT)
        elif self.isInCoupleRide(old) and not self.isInCoupleRide():
            self.modelServer.leaveCoupleEmote(old)
            if p.id in old:
                p.hideZaijuUI(uiConst.ZAIJU_SHOW_TYPE_EXIT)
        if self == BigWorld.player().targetLocked:
            BigWorld.player().ap.releaseTargetLockedEffect()
        self.refreshOpacityState()

    def getOtherIDInCoupleEmote(self, data = None):
        if data is None:
            data = getattr(self, 'coupleEmote', (0, 0, 0))
        if len(data) == 0:
            return 0
        state = self.isInCoupleEmote(data)
        if not state:
            return 0
        elif data is not None:
            return data[3 - state]
        else:
            return self.coupleEmote[3 - state]

    def isInCoupleEmote(self, data = None):
        if data is None:
            emoteInfo = getattr(self, 'coupleEmote', (0, 0, 0))
            if len(emoteInfo) == 0:
                return 0
        else:
            emoteInfo = data
        if self.id == emoteInfo[1]:
            return 1
        if self.id == emoteInfo[2]:
            return 2
        return 0

    def getCoupleKey(self, withEmoteId = False):
        other = BigWorld.entity(self.getOtherIDInCoupleEmote())
        if getattr(other, 'modelServer', None) is None or getattr(other, 'model', None) is None:
            return
        if self.coupleEmote[2] == self.id:
            man = other
            woman = self
        else:
            man = self
            woman = other
        if not man or not man.inWorld:
            return
        elif not woman or not woman.inWorld:
            return
        sexType = man.physique.sex
        if man.physique.sex == woman.physique.sex and man.physique.sex == 1:
            sexType = gameglobal.COUPLE_SEX_MAN_MAN
        if man.physique.sex == woman.physique.sex and man.physique.sex == 2:
            sexType = gameglobal.COUPLE_SEX_WOMAN_WOMAN
        if withEmoteId:
            return (self.coupleEmote[0],
             sexType,
             man.physique.bodyType,
             woman.physique.bodyType)
        else:
            return (sexType, man.physique.bodyType, woman.physique.bodyType)

    def msgFeedBack(self, msg):
        try:
            msgFeedBacks = self.getItemData().get('msgFeedBacks', {})
            msg = msg.split(':')[0]
            feedBackIds = msgFeedBacks.get(msg, [])
            if feedBackIds:
                feedBackId = random.choice(feedBackIds)
                chatMsg = ICMD.data.get(feedBackId, {}).get('chatMsg', None)
                if not chatMsg:
                    return False
                self.topLogo.setChatMsg(chatMsg)
                return True
            return False
        except:
            return True

    def chatInRoom(self):
        if not gameglobal.rds.configData.get('enableInteractiveHomeChat', False):
            return False
        self.chatTime = self.getItemData().get('chatTime', -1.0)
        if self.chatTime <= 0:
            return
        self.chatProbability = self.getItemData().get('chatProbability', 1)
        self.chatHandle = BigWorld.callback(self.chatTime, self.sendChatMsg)

    def sendChatMsg(self):
        if self.chatHandle:
            BigWorld.cancelCallback(self.chatHandle)
        if random.randint(0, 100) < self.chatProbability:
            chatIds = self.getItemData().get('chatIds', [])
            if chatIds:
                chatId = random.choice(chatIds)
                chatMsg = ICMD.data.get(chatId, {}).get('chatMsg', '')
                self.topLogo.setChatMsg(chatMsg)
        self.chatHandle = BigWorld.callback(self.chatTime, self.sendChatMsg)

    def trapMusicCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        p = BigWorld.player()
        itemData = self.getItemData()
        notifyMusicId = itemData.get('notifyMusicId', 0)
        if enteredTrap:
            p.notifyMusicCallBack(True, notifyMusicId)
        else:
            p.notifyMusicCallBack(False, notifyMusicId)
