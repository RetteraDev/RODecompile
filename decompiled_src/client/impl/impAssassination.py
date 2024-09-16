#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impAssassination.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import assassinationUtils as assUtils
import utils
from guis import events
from assassination import Assassination
from callbackHelper import Functor
from guis import topLogo
from cdata import assassination_config_data as ACD
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD

class ImpAssassination(object):

    def onLogOnAssassination(self, dto, aType):
        myAssData = Assassination().fromDTO(dto)
        self.handleAssassinationData(myAssData, aType)

    def doAssassinationSuccOwner(self, tombId, roleName, position):
        posListData = list()
        posListData.append(1)
        posListData.extend(position)
        posStr = ','.join(map(str, posListData))
        self.showGameMsg(GMDD.data.ASSASSINATION_SUCC_OWNER_MSG, (str(roleName), str(posStr)))
        gameglobal.rds.ui.assassinationTombstone.setNewUpdateMsgCallBack()
        gameglobal.rds.ui.assassinationTombstone.pushNewUpdateMsg(tombId)

    def doAssassinationSuccTarget(self, isShow, roleName, msgId):
        roleName = roleName if isShow else ACD.data.get('assassinationAnonymityName', gameStrings.TEXT_ASSASSINATIONTOMBSTONEPROXY_264)
        gameglobal.rds.ui.assassinationLeaveBook.show(roleName, msgId)

    def notifyAssassinationKillState(self, identity, state, assassinationKillTargetStamp):
        if state == assUtils.ASSASSINATION_STATE_START:
            gameglobal.rds.ui.assassinationProcess.show('start', assassinationKillTargetStamp)
        elif state == assUtils.ASSASSINATION_STATE_FAIL:
            if identity == assUtils.ASSASSINATION_KILLER:
                gameglobal.rds.ui.assassinationProcess.show('fail')
            elif identity == assUtils.ASSASSINATION_TARGET:
                gameglobal.rds.ui.assassinationProcess.show('defendSuccess')
        elif state == assUtils.ASSASSINATION_STATE_SUCC:
            if identity == assUtils.ASSASSINATION_KILLER:
                gameglobal.rds.ui.assassinationProcess.show('success')
            elif identity == assUtils.ASSASSINATION_TARGET:
                gameglobal.rds.ui.assassinationProcess.show('defendFail')
        self.refreshAllUIName()

    def set_assassinationTeleport(self, old):
        self.setAvatarAssassinationTeleportFinish()
        self.refreshAllUIName()

    def set_assassinationKillTargetStamp(self, old):
        apEffectEx = getattr(self, 'apEffectEx', None)
        if apEffectEx:
            apEffectEx.resetEffect()
        self.refreshAllUIName()

    def set_assassinationKillTargetGbId(self, old):
        pass

    def onSearchAssassinationTargetByRoleName(self, infoList):
        if not infoList:
            return
        else:
            info = infoList[0] if infoList and len(infoList) >= 1 else None
            if info:
                self.onSearchAssassinationTarget(info[0], info[1], info[2], info[5], info[7], info[8])
            return

    def onSearchAssassinationTarget(self, gbId, roleName, lv, school, photo, sex):
        if not gameglobal.rds.configData.get('enableAssassination', False):
            return False
        targetData = gameglobal.rds.ui.assassinationEnemy.updateInfoFormat(gbId, roleName, lv, school, False, photo, sex)
        gameglobal.rds.ui.assassinationIssue.confirmToSelectEmeny(targetData)

    def checkAssassination(self, entity):
        if not gameglobal.rds.configData.get('enableAssassination', False):
            return False
        elif not entity:
            return False
        avatarEntity = entity
        if hasattr(entity, 'IsAvatar') and entity.IsAvatar:
            avatarEntity = entity
        elif hasattr(entity, 'IsSummonedSprite') and entity.IsSummonedSprite and hasattr(entity, 'getOwner'):
            avatarEntity = entity.getOwner()
        elif hasattr(entity, 'IsSummonedBeast') and entity.IsSummonedBeast and hasattr(entity, 'ownerId'):
            avatarEntity = BigWorld.entity(entity.ownerId)
        if avatarEntity and hasattr(avatarEntity, 'assassinationKillTargetStamp') and avatarEntity.assassinationKillTargetStamp:
            return True
        else:
            return False

    def getAssTargetEntId(self):
        p = BigWorld.player()
        if hasattr(p, 'assassinationKillTargetEntId') and p.assassinationKillTargetEntId:
            return p.assassinationKillTargetEntId
        return 0

    def refreshAllUIName(self):
        if hasattr(self, 'refreshToplogoTitle'):
            self.refreshToplogoTitle()
        if hasattr(self, 'refreshTopLogoName'):
            self.refreshTopLogoName()
        if hasattr(self, 'refreshAvatarSummonedSpriteTopLogo'):
            self.refreshAvatarSummonedSpriteTopLogo()
        if hasattr(self, 'refreshKillTargetTopLogo'):
            self.refreshKillTargetTopLogo()

    def refreshKillTargetTopLogo(self):
        targetEntId = self.getAssTargetEntId()
        if targetEntId:
            ent = BigWorld.entity(targetEntId)
            if ent:
                ent.topLogo.updateRoleName(ent.topLogo.name)
                BigWorld.player().lockTarget(ent)

    def getAssassinationKillerName(self, entity):
        if hasattr(entity, 'IsAvatar') and entity.IsAvatar:
            name = ACD.data.get('assassinationKillerName', '')
        elif hasattr(entity, 'IsSummonedSprite') and entity.IsSummonedSprite:
            name = ACD.data.get('assassinationKillerYinglingName', '')
        else:
            name = ACD.data.get('assassinationKillerBeastName', '')
        info = {'name': name,
         'title': ''}
        return info

    def setAvatarAssassinationTeleportFinish(self):
        if not gameglobal.rds.configData.get('enableAssassination', False):
            return
        if not (hasattr(self, 'IsAvatar') and self.IsAvatar):
            return
        if not (hasattr(self, 'gbId') and hasattr(BigWorld.player(), 'gbId')):
            return
        if self.gbId == BigWorld.player().gbId:
            return
        if hasattr(self, 'assassinationTeleport') and self.assassinationTeleport:
            self.refreshAvatarAssassinationOpacity(True)
        else:
            self.refreshAvatarAssassinationOpacity(False)

    def setAssassinationModelFinish(self):
        if not gameglobal.rds.configData.get('enableAssassination', False):
            return
        if not (hasattr(self, 'gbId') and hasattr(BigWorld.player(), 'gbId')):
            return
        if self.gbId == BigWorld.player().gbId:
            return
        if self.checkAssassination(self):
            if self.assassinationTeleport:
                self.assassinationTeleport = 0
            self.refreshAvatarAssassinationOpacity(False)
            self.refreshAllUIName()

    def refreshAvatarAssassinationOpacity(self, opacityEnable):
        if opacityEnable and self.topLogo == None:
            self.topLogo = topLogo.TopLogo(self.id)
        if hasattr(self, 'refreshOpacityState'):
            self.refreshOpacityState()
        if hasattr(self, 'spriteObjId') and BigWorld.entity(self.spriteObjId):
            BigWorld.entity(self.spriteObjId).refreshOpacityState()

    def openAssassinationMainUI(self, isDown):
        if isDown:
            if gameglobal.rds.ui.assassinationMain.widget:
                gameglobal.rds.ui.assassinationMain.hide()
            else:
                gameglobal.rds.ui.assassinationMain.show()

    def handleAssassinationData(self, myAssData, myAssType):
        self.updateOnBoardData(myAssData)
        self.updateOffBoardData(myAssData)
        self.updateAssExtraData(myAssData)
        if myAssType == assUtils.ASSASSINATION_SYNC_LOG_ON:
            pass
        elif myAssType == assUtils.ASSASSINATION_SYNC_ON_BOARD:
            gameglobal.rds.ui.assassinationMain.requestGetAllData()
        elif myAssType == assUtils.ASSASSINATION_SYNC_OFF_BOARD:
            gameglobal.rds.ui.assassinationMain.requestGetAllData()
        elif myAssType == assUtils.ASSASSINATION_SYNC_KILL_START:
            pass
        elif myAssType == assUtils.ASSASSINATION_SYNC_KILL_END:
            pass
        gameglobal.rds.ui.assassinationPush.show()

    def updateOnBoardData(self, myAssData):
        self.myAssOnBoardData = {}
        for gbId, timeStamp in zip(myAssData.onBoard.iterkeys(), myAssData.onBoard.itervalues()):
            if utils.isSameDay(timeStamp):
                self.myAssOnBoardData[gbId] = timeStamp

    def updateOffBoardData(self, myAssData):
        self.myAssOffBoardData = {}
        if myAssData.offBoard:
            self.myAssOffBoardData[assUtils.OFF_BOARD_TIME_OFF] = myAssData.offBoard.get(assUtils.OFF_BOARD_TIME_OFF, 0)
            self.myAssOffBoardData[assUtils.OFF_BOARD_GBID] = myAssData.offBoard.get(assUtils.OFF_BOARD_GBID, 0)
            self.myAssOffBoardData[assUtils.OFF_BOARD_FROM_GBID] = myAssData.offBoard.get(assUtils.OFF_BOARD_FROM_GBID, 0)
            if assUtils.OFF_BOARD_TIME_KILL in myAssData.offBoard:
                self.myAssOffBoardData[assUtils.OFF_BOARD_TIME_KILL] = myAssData.offBoard.get(assUtils.OFF_BOARD_TIME_KILL, 0)
            if assUtils.OFF_BOARD_TIME_END in myAssData.offBoard:
                self.myAssOffBoardData[assUtils.OFF_BOARD_TIME_END] = myAssData.offBoard.get(assUtils.OFF_BOARD_TIME_END, 0)
        self.myAssOffBoardData['state'] = assUtils.getOffBoardStateByData(myAssData.offBoard)

    def updateAssExtraData(self, myAssData):
        self.myAssExtraData = {}
        offCount = myAssData.extra.get(assUtils.EXTRA_OFF_CNT, 0)
        offStamp = myAssData.extra.get(assUtils.EXTRA_OFF_STAMP, 0)
        if utils.isSameDay(offStamp):
            self.myAssExtraData[assUtils.EXTRA_OFF_CNT] = offCount
        else:
            self.myAssExtraData[assUtils.EXTRA_OFF_CNT] = 0

    def getDummyAssOffBoardData(self, entId, killStartTime, endStartTime, state):
        self.myAssOffBoardData = {}
        self.myAssOffBoardData[assUtils.OFF_BOARD_TIME_OFF] = utils.getNow() - 60
        self.myAssOffBoardData[assUtils.OFF_BOARD_GBID] = BigWorld.entity(entId).gbId
        self.myAssOffBoardData[assUtils.OFF_BOARD_FROM_GBID] = BigWorld.player().gbId
        if killStartTime:
            self.myAssOffBoardData[assUtils.OFF_BOARD_TIME_KILL] = utils.getNow() - 30
        if endStartTime:
            self.myAssOffBoardData[assUtils.OFF_BOARD_TIME_END] = utils.getNow()
        self.myAssOffBoardData['state'] = state
