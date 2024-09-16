#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPlayerUI.o
from gamestrings import gameStrings
from PIL import Image
import BigWorld
import C_ui
from Scaleform import GfxValue
import utils
import const
import gameglobal
import formula
import gametypes
import gamelog
import skillDataInfo
import appSetting
import clientUtils
import copy
import gameconfigCommon
from guis import uiConst
from helpers import navigator
from helpers import ccControl
from helpers import capturePhoto
from helpers import ccManager
from guis import messageBoxProxy
from callbackHelper import Functor
from guis import ui
from guis.asObject import TipManager
from gamestrings import gameStrings
from guis import hotkey as HK
from guis import hotkeyProxy
from data import mapSearch_ii_data as MII
from data import sys_config_data as SCD
from data import emotion_action_data as EAD
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
from data import state_data as SD
from data import monster_event_trigger_data as METD
from data import quest_marker_data as QMD
from data import play_recomm_config_data as PRCD

class ImpPlayerUI(object):

    def showRoleInfo(self, isDown):
        if isDown:
            if gameglobal.rds.ui.roleInfo.isShow:
                gameglobal.rds.ui.roleInfo.hide()
            else:
                gameglobal.rds.ui.roleInfo.show()

    def showGuild(self, isDown):
        if isDown:
            if self.crossServerFlag == const.CROSS_SERVER_STATE_IN and not BigWorld.player().inWingCity():
                BigWorld.player().showGameMsg(GMDD.data.WIDGET_IN_BLACK_LIST, ())
                return
            if BigWorld.player().guild:
                if gameglobal.rds.ui.guild.mediator:
                    gameglobal.rds.ui.guild.hide()
                elif BigWorld.player().guild:
                    gameglobal.rds.ui.guild.show()
            else:
                gameglobal.rds.ui.guildQuickJoin.show()

    def showTeamInfo(self, isDown):
        if isDown:
            p = BigWorld.player()
            if self.inFubenTypes(const.FB_TYPE_BATTLE_FIELD) and not p.isInPUBG():
                if gameglobal.rds.ui.group.isShow:
                    gameglobal.rds.ui.group.closeGroupInfoPanel()
                else:
                    gameglobal.rds.ui.group.showGroupInfoPanel()
            elif gameglobal.rds.ui.team.isShow:
                gameglobal.rds.ui.team.close()
            elif gameglobal.rds.ui.memberDetailsV2.isShow():
                gameglobal.rds.ui.memberDetailsV2.hide()
            elif gameglobal.rds.ui.group.isShow:
                gameglobal.rds.ui.group.closeGroupInfoPanel()
            elif not gameglobal.rds.ui.memberDetailsV2.isShow() and self.isInTeam():
                gameglobal.rds.ui.memberDetailsV2.show()
            elif not gameglobal.rds.ui.group.isShow and self.isInGroup():
                gameglobal.rds.ui.group.showGroupInfoPanel()
            elif not self.isInTeam() and not self.isInGroup():
                gameglobal.rds.ui.team.onQuickCreateClick()

    def showAchievementInfo(self, isDown):
        if isDown:
            if self.crossServerFlag == const.CROSS_SERVER_STATE_IN:
                BigWorld.player().showGameMsg(GMDD.data.WIDGET_IN_BLACK_LIST, ())
                return
            if gameglobal.rds.ui.achvment.widget:
                gameglobal.rds.ui.achvment.hide()
            else:
                gameglobal.rds.ui.achvment.getAchieveData()

    def showTaskLog(self, isDown):
        if isDown:
            if gameglobal.rds.ui.questLog.isShow:
                gameglobal.rds.ui.questLog.hide()
            else:
                gameglobal.rds.ui.questLog.showTaskLog()

    def showMap(self, isDown):
        spaceNo = formula.getMapId(BigWorld.player().spaceNo)
        if isDown:
            if MII.data.has_key(spaceNo) or self.inWingPeaceCityOrBornIsland():
                gameglobal.rds.ui.map.openMap(not gameglobal.rds.ui.map.isShow)
            else:
                BigWorld.player().showGameMsg(GMDD.data.NO_RESOURCE_FORBID_IN_MAP, ())

    def showSkill(self, isDown):
        if isDown:
            if gameglobal.rds.ui.skill.isShow:
                gameglobal.rds.ui.skill.onClickClose(False)
            else:
                gameglobal.rds.ui.skill.show()

    def showGeneralSkill(self, isDown):
        if isDown:
            if gameglobal.rds.ui.skill.generalMediator:
                gameglobal.rds.ui.skill.closeGeneralSkill()
            else:
                gameglobal.rds.ui.skill.showGeneralSkill()

    def showLifeSkill(self, isDown):
        if isDown:
            gameglobal.rds.ui.lifeSkillNew.toggle()

    def toggleYuyue(self, isDown):
        pass

    def toggleWorldWar(self, isDown):
        if isDown:
            if gameglobal.rds.configData.get('enableWorldWar', False):
                if not gameglobal.rds.ui.worldWar.wwMed:
                    gameglobal.rds.ui.worldWar.show()
                else:
                    gameglobal.rds.ui.worldWar.hide(True)

    def showMail(self, isDown):
        if isDown:
            if gameglobal.rds.ui.mail.mediator:
                gameglobal.rds.ui.mail.hide()
            else:
                gameglobal.rds.ui.mail.show()

    def showConsign(self, isDown):
        if isDown:
            openLv = SCD.data.get('openConsignLv', 20)
            if self.lv < openLv:
                self.showGameMsg(GMDD.data.FORBIDDEN_OPEN_CONSIGN, ())
                return
            if gameglobal.rds.ui.consign.mediator or gameglobal.rds.ui.tabAuction.mediator:
                self.closeAuctionFun()
            else:
                self.openAuctionFun()

    def showSysSetting(self, isDown):
        if isDown:
            if gameglobal.rds.ui.systemSettingV2.isShow():
                gameglobal.rds.ui.systemSettingV2.close()
            else:
                gameglobal.rds.ui.systemSettingV2.show()

    def showTopLogo(self, isHide):
        ent = BigWorld.entities.items()
        for id, e in ent:
            if utils.instanceof(e, 'DroppedItem') and e.topLogo and not e.beHide:
                e.topLogo.hide(not isHide)

        if hasattr(self, 'entityDebugNameFactory'):
            self.entityDebugNameFactory.showEntityDebugName(isHide)

    def showArenaPanel(self, isDown):
        gamelog.debug('showArenaPanel:', isDown)
        if isDown:
            p = BigWorld.player()
            if formula.isDoubleArenaCrossServerML(formula.getMLGNo(p.spaceNo)):
                gameglobal.rds.ui.pvPPanel.toggle(uiConst.PVP_BG_V2_TAB_BALANCE_ARENA_2PERSON)
                return
            if gameglobal.rds.ui.pvPPanel.todayActivityCheck():
                gameglobal.rds.ui.pvPPanel.openTodayActivity()
            else:
                gameglobal.rds.ui.pvPPanel.toggle(uiConst.PVP_BG_V2_TAB_BATTLE_FIELD)

    def showDebug(self, down):
        if not BigWorld.isPublishedVersion():
            gameglobal.rds.ui.debug.show()

    def showBattleApplyWin(self, down):
        pass

    def showMonsterDebug(self, down):
        if not BigWorld.isPublishedVersion():
            gameglobal.rds.ui.fubenMonster.showMonsterDebug()

    def startActionProgress(self, period, spellID, objId, isForce, yaw, equipId):
        gamelog.debug('jorsef: startActionProgress', period, spellID, objId)
        self.ap.stopMove()
        super(self.__class__, self).startActionProgress(period, spellID, objId, isForce, yaw, equipId)
        if self.isPathfinding:
            navigator.getNav().stopPathFinding()
        if period > 0:
            useText = ''
            if objId:
                ent = BigWorld.entities.get(objId, None)
                if ent and (utils.instanceof(ent, 'Npc') or utils.instanceof(ent, 'MovableNpc')):
                    npcId = getattr(ent, 'npcId')
                    if npcId:
                        useText = QMD.data.get(npcId, {}).get('castName', '')
                elif ent and utils.instanceof(ent, 'Monster'):
                    monsterId = getattr(ent, 'charType')
                    eventIndex = getattr(ent, 'triggerEventIndex', -1)
                    if monsterId and eventIndex >= 0:
                        try:
                            eventData = METD.data[monsterId][eventIndex]
                        except:
                            eventData = {}

                        useText = eventData.get('castName', '')
            if not useText:
                useText = EAD.data.get(spellID, {}).get('castName', '')
            if spellID == const.ACT_GUILD_INHERIT:
                useText = gameStrings.ACT_GUILD_INHERIT_STR
            gameglobal.rds.ui.generalCastbar.startGeneralCastBar(period, None, useText)
        if abs(yaw - const.DEFAULT_YAW) >= 0.1:
            self.ap.setYaw(yaw)
        ead = EAD.data.get(spellID, {})
        if ead.get('lockYaw', 0):
            self.isLockYaw = True

    def endActionProgress(self, success, oldSpellID):
        self.unlockKey(gameglobal.KEY_POS_AVATAR)
        self.isLockYaw = False
        if not success:
            gameglobal.rds.ui.generalCastbar.notifyCastInterrupt()
        super(self.__class__, self).endActionProgress(success, oldSpellID)
        self.updateActionKeyState()

    def showSingleDebug(self, down):
        if not BigWorld.isPublishedVersion():
            if down:
                adapter = gameglobal.rds.ui
                funcList = [(gameStrings.TEXT_IMPPLAYERUI_264, adapter.bodyChange.showBodyChangeProxy, uiConst.WIDGET),
                 (gameStrings.TEXT_IMPPLAYERUI_265, adapter.equipFashionChange.show, uiConst.WIDGET),
                 (gameStrings.TEXT_IMPPLAYERUI_266, adapter.pointGen.show, uiConst.WIDGET),
                 (gameStrings.TEXT_IMPPLAYERUI_267, adapter.playerPhotoGen.show, uiConst.WIDGET),
                 (gameStrings.TEXT_IMPPLAYERUI_268, adapter.actionDebug.showActionDebug, uiConst.WIDGET),
                 (gameStrings.TEXT_IMPPLAYERUI_269, adapter.particleDebug.showParticleDebug, uiConst.WIDGET),
                 (gameStrings.TEXT_IMPPLAYERUI_270, adapter.hardPointDebug.showHPDebug, uiConst.WIDGET),
                 (gameStrings.TEXT_IMPPLAYERUI_271, adapter.roleDebug.showRoleDebug, uiConst.WIDGET),
                 (gameStrings.TEXT_IMPPLAYERUI_272, adapter.storyEditDebug.showStoryEdit, uiConst.WIDGET),
                 (gameStrings.TEXT_IMPPLAYERUI_273, adapter.tdHeadGen.showTdHeadGen, uiConst.WIDGET),
                 (gameStrings.TEXT_IMPPLAYERUI_274, adapter.walkLineEdit.showWalkLineEdit, uiConst.WIDGET)]
                gameglobal.rds.ui.openDialog(gameStrings.TEXT_IMPPLAYERUI_276, gameStrings.TEXT_IMPPLAYERUI_276_1, funcList)

    def showMorphDebug(self, down):
        if not down or BigWorld.isPublishedVersion():
            return
        if self.school == 101:
            pass
        else:
            funclist = []
            for i in xrange(42):
                funclist.append((gameStrings.TEXT_IMPPLAYERUI_286 + '!' * i, lambda : 0, uiConst.WIDGET))

            gameglobal.rds.ui.openDialog(gameStrings.TEXT_IMPPLAYERUI_287, gameStrings.TEXT_IMPPLAYERUI_287_1, funclist)

    def showSummary(self, down):
        fbNo = formula.getFubenNo(self.spaceNo)
        gamelog.debug('hjx debug showSummary:', fbNo)
        if formula.whatFubenType(fbNo) in const.FB_TYPE_BATTLE_FIELD:
            if down:
                if gameglobal.rds.ui.battleField.isBFTmpResultShow:
                    gameglobal.rds.ui.battleField.closeBFTmpResultWidget()
                else:
                    gameglobal.rds.ui.battleField.showBFTmpResultWidget()
        elif self.inFubenTypes(const.FB_TYPE_ARENA):
            if down:
                if gameglobal.rds.ui.arena.isArenaTmpResultShow:
                    gameglobal.rds.ui.arena.closeArenaTmpResult(0)
                else:
                    gameglobal.rds.ui.arena.showArenaTmpResult()
        if down:
            if gameglobal.rds.ui.bossInfo.mediator:
                gameglobal.rds.ui.bossInfo.hide()
            else:
                gameglobal.rds.ui.bossInfo.show()

    def showRankList(self, down):
        if down:
            if gameglobal.rds.ui.ranking.mediator:
                gameglobal.rds.ui.ranking.hide()
            else:
                gameglobal.rds.ui.ranking.show()

    def showLittleMap(self, down):
        if down:
            if gameglobal.rds.ui.littleMap.isMapShow():
                gameglobal.rds.ui.littleMap.close()
            else:
                gameglobal.rds.ui.littleMap.open()

    def showUI(self, down):
        if down:
            if gameglobal.F12_MODE == gameglobal.F12_MODE_NORMAL:
                if gameglobal.rds.ui.quest.isShow or gameglobal.rds.ui.npcV2.isShow or gameglobal.rds.ui.map.isShow or gameglobal.rds.ui.fubenLogin.isShow:
                    return
                area = BigWorld.ChunkInfoAt((self.position.x, self.position.y + 1, self.position.z))
                unDoneArea = SCD.data.get('unDoneChunk', ())
                if area in unDoneArea:
                    return
            gameglobal.F12_MODE = (gameglobal.F12_MODE + 1) % gameglobal.F12_MODE_LENGTH
            if gameglobal.F12_MODE == gameglobal.F12_MODE_NORMAL:
                gameglobal.rds.ui.enableUI = True
                if hasattr(BigWorld.player(), 'ap') and hasattr(BigWorld.player().ap, 'aimCross'):
                    BigWorld.player().ap.aimCross.turnToAimState()
            elif gameglobal.F12_MODE == gameglobal.F12_MODE_NOUI:
                gameglobal.rds.ui.enableUI = False
                if hasattr(BigWorld.player(), 'ap') and hasattr(BigWorld.player().ap, 'aimCross'):
                    BigWorld.player().ap.aimCross.hide()
                    gameglobal.rds.ui.hideAimCross(True, True)
                    gameglobal.rds.ui.hideAimCross(True, False)
                    gameglobal.rds.ui.hideAimCross(False)
            C_ui.enableUI(gameglobal.rds.ui.enableUI)
            ccControl.setCCVisible(gameglobal.rds.ui.enableUI)

    def showChatLogWiew(self, down):
        gamelog.debug('showChatLogWiew')
        if down:
            if gameglobal.rds.ui.quest.isShow or gameglobal.rds.ui.npcV2.isShow:
                gameglobal.rds.ui.chat.showView()

    def showSchedule(self, down):
        gamelog.debug('showSchedule')

    def showMoreRecomm(self, down):
        if down:
            if gameglobal.rds.ui.playRecomm.widget:
                gameglobal.rds.ui.playRecomm.hide()
            else:
                p = BigWorld.player()
                openMoreRecommMinLv = PRCD.data.get('lvupRecommMinLv', 45)
                if p.lv < openMoreRecommMinLv:
                    p.showGameMsg(GMDD.data.OPEN_MORE_RECOMM_MIN_LV, (openMoreRecommMinLv,))
                else:
                    gameglobal.rds.ui.playRecomm.showInPage(0, 0)

    def showFriend(self, down):
        if down:
            if gameglobal.rds.ui.systemButton.friendFlowBackType:
                gameglobal.rds.ui.friendFlowBack.show()
            p = BigWorld.player()
            checkHasNewMsg = False
            if p.friend.tempMsgs:
                newMsgs = copy.deepcopy(p.friend.tempMsgs)
                for _gbId, type, _, _ in newMsgs:
                    if type == gametypes.FRIEND_MSG_TYPE_CHAT:
                        if gameglobal.rds.ui.groupChat.checkChatedId(_gbId):
                            continue
                        else:
                            p.handleFriendMsg(0, 0)
                            checkHasNewMsg = True
                    else:
                        p.handleFriendMsg(0, 0)
                        checkHasNewMsg = True

            checkHasNewMsg = True if p.handleGroupUnreadMsgs() else checkHasNewMsg
            if not checkHasNewMsg:
                if gameglobal.rds.ui.friend.isShow:
                    gameglobal.rds.ui.friend.hide(False)
                else:
                    gameglobal.rds.ui.friend.show()
            gameglobal.rds.ui.friend.showAllMinChat()
            self._checkBlink()

    def sendTransportDest(self, transportEntId, transportId, destDict):
        spaceNo = BigWorld.player().spaceNo
        if formula.spaceInGuild(spaceNo):
            spaceNo = formula.getMapId(spaceNo)
        if MII.data.has_key(spaceNo) or self.inWingPeaceCityOrBornIsland():
            gameglobal.rds.ui.map.openMap(True, uiConst.MAP_TYPE_TRANSPORT)
        else:
            BigWorld.player().showGameMsg(GMDD.data.NO_RESOURCE_FORBID_IN_MAP, ())

    def showFps(self, down):
        if down:
            if gameglobal.rds.ui.topBar.fpsShow:
                gameglobal.rds.ui.topBar.setFpsVisible(False)
            else:
                gameglobal.rds.ui.topBar.setFpsVisible(True)

    def showCamera(self, down):
        if not gameglobal.rds.configData.get('enableNewCamera', False):
            gamelog.debug('showCamera', down, gameglobal.rds.ui.camera.isShow)
            if down:
                if gameglobal.rds.ui.camera.isShow:
                    gameglobal.rds.ui.camera.hide()
                else:
                    gameglobal.rds.ui.camera.show()
        else:
            gamelog.debug('showCameraV2', down, gameglobal.rds.ui.cameraV2.isShow)
            if down:
                if gameglobal.rds.ui.cameraV2.isShow:
                    gameglobal.rds.ui.cameraV2.hide()
                else:
                    gameglobal.rds.ui.cameraV2.show()

    def assignConfirm(self, down):
        if not down:
            return
        if gameglobal.rds.ui.assign.auctionMediator:
            param = GfxValue(0)
            param.SetNull()
            gameglobal.rds.ui.assign.auctionMediator.Invoke('handleAuction', param)
        elif gameglobal.rds.ui.assign.diceMediator:
            gameglobal.rds.ui.assign.diceMediator.Invoke('diceFirstItem')

    def assignGreed(self, down):
        if not down:
            return
        if gameglobal.rds.ui.assign.diceMediator:
            gameglobal.rds.ui.assign.diceMediator.Invoke('greedFirstItem')

    def assignGiveUp(self, down):
        if not down:
            return
        if gameglobal.rds.ui.assign.auctionMediator:
            param = GfxValue(0)
            param.SetNull()
            gameglobal.rds.ui.assign.auctionMediator.Invoke('handleGiveUp', param)
        elif gameglobal.rds.ui.assign.diceMediator:
            gameglobal.rds.ui.assign.diceMediator.Invoke('giveUpFirstItem')

    def showHelp(self, down):
        if down:
            if gameglobal.rds.ui.help.isShow():
                gameglobal.rds.ui.help.hide(True)
            else:
                gameglobal.rds.ui.help.show()

    def showPlayerComm(self, down):
        if down:
            if gameglobal.rds.ui.playRecomm.widget:
                gameglobal.rds.ui.playRecomm.hide()
            else:
                gameglobal.rds.ui.playRecomm.show()
                gameglobal.rds.uiLog.addClickLog(uiConst.WIDGET_PLAY_RECOMM * 100 + 8)

    def showDelegation(self, down):
        if down:
            if gameglobal.rds.ui.delegationBook.med:
                gameglobal.rds.ui.delegationBook.hide()
            else:
                gameglobal.rds.ui.delegationBook.show()

    def gotoNextTrackTab(self, down):
        if down:
            gameglobal.rds.ui.questTrack.gotoNextTab()

    def BFgoHomeClick(self, down):
        if down and self.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            self.bfGoHome()

    def BFopenShopClick(self, down):
        if down and self.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            gameglobal.rds.ui.battleField.onOpenShopClick()

    def BFopenStatsClick(self, down):
        if down and self.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            gameglobal.rds.ui.battleField.onOpenStatsClick()

    def testHair(self):
        guadian = clientUtils.model('char/10006/model/hair/test/guadian.model')
        g1 = clientUtils.model('char/10006/model/hair/test/guajian1.model')
        g2 = clientUtils.model('char/10006/model/hair/test/guajian2.model')
        g3 = clientUtils.model('char/10006/model/hair/test/guajian3.model')
        self.model.node('biped Head').attach(guadian, 'biped Head')
        guadian.setHP('HP_YX_hair_item01', g1)
        guadian.setHP('HP_YX_hair_item02', g2)
        guadian.setHP('HP_YX_hair_item03', g3)

    def testPosYaw(self, pos, yaw):
        self.cell.adminOnCell('$goto 100 200 100 1')
        self.ap.setYaw(-1.94804775715)

    @ui.callFilter(1, False)
    def updateBackWear(self, down, haveAct = True, needCheck = True):
        self.innerUpdateBackWear(down, haveAct, needCheck)

    def innerUpdateBackWear(self, down, haveAct = True, needCheck = True):
        if down:
            if needCheck and self.stateMachine.checkShowBackWear() or not needCheck:
                if self.weaponInHandState() == gametypes.WEAPON_HANDFREE:
                    self.switchWeaponState(gametypes.WEAR_BACK_ATTACH, haveAct)
                    backwear = self.modelServer.backwear
                    self.showZaijuUI(backwear.skills, uiConst.ZAIJU_TYPE_WEAR)
                else:
                    if self.inCombat:
                        self.switchWeaponState(gametypes.WEAPON_DOUBLEATTACH, haveAct)
                    else:
                        self.switchWeaponState(gametypes.WEAPON_HANDFREE, haveAct)
                    self.hideZaijuUI()
                    gameglobal.rds.ui.vehicleSkill.hide()

    @ui.callFilter(1, False)
    def updateWaistWear(self, down, haveAct = True, needCheck = True):
        self.innerUpdateWaistWear(down, haveAct, needCheck)

    def innerUpdateWaistWear(self, down, haveAct = True, needCheck = True):
        if down:
            if needCheck and self.stateMachine.checkShowWaistWear() or not needCheck:
                if self.weaponInHandState() == gametypes.WEAPON_HANDFREE:
                    self.switchWeaponState(gametypes.WEAR_WAIST_ATTACH, haveAct)
                    waistwear = self.modelServer.waistwear
                    self.showZaijuUI(waistwear.skills, uiConst.ZAIJU_TYPE_WEAR)
                else:
                    if self.inCombat:
                        self.switchWeaponState(gametypes.WEAPON_DOUBLEATTACH, haveAct)
                    else:
                        self.switchWeaponState(gametypes.WEAPON_HANDFREE, haveAct)
                    self.hideZaijuUI()

    def useWearSkillBySlotId(self, down, slotId = 0):
        wear = self.modelServer.getShowWear()
        if wear and wear.skills and slotId < len(wear.skills) and self.stateMachine.checkShowWearActions():
            skillId, skillLv = wear.skills[slotId]
            self.useWearSkill(down, skillId, skillLv)

    @ui.callFilter(1, False)
    def useWearSkill(self, down, skillId = 0, skillLv = 0, equipPart = 0):
        wear = self.modelServer.getShowWear(equipPart)
        if down and (wear or equipPart in (gametypes.EQU_PART_FASHION_CAPE,)):
            self.cell.useWearSkill(skillId, skillLv, equipPart)

    def getSkillTipsInfo(self, skillId, SkillLv):
        return skillDataInfo.ClientSkillTips(skillId, SkillLv)

    def showSafeMode(self):
        if not hasattr(self, 'OCLI'):
            return
        if not self.OCLI[0]['safeMode'].onSafeMode:
            return
        if getattr(self, 'safeModeBoxId', 0):
            return
        MBButton = messageBoxProxy.MBButton
        buttonOk = MBButton(gameStrings.TEXT_IMPPLAYERUI_573, self.__onConfirmSafeMode)
        buttonCancel = MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1, self.__onCancelSafeMode)
        text = GMD.data.get(GMDD.data.ACCOUNT_SAFE_MODE, {}).get('text', '')
        self.safeModeBoxId = gameglobal.rds.ui.messageBox.show(True, '', text, [buttonOk, buttonCancel])

    def setSafeModeState(self):
        path = str(SD.data.get(uiConst.SAFE_MODE_SATE_ID, {}).get('iconId', 'notFound')) + '.dds'
        data = [{'id': uiConst.SAFE_MODE_SATE_ID,
          'srcId': 0,
          'type': 3,
          'iconPath': path,
          'timer': -100,
          'count': 1}]
        if self.OCLI[0]['safeMode'].onSafeMode:
            gameglobal.rds.ui.player.changeStateIcon(data, [])

    def quitSafeMode(self):
        path = str(SD.data.get(uiConst.SAFE_MODE_SATE_ID, {}).get('iconId', 'notFound')) + '.dds'
        data = [{'id': uiConst.SAFE_MODE_SATE_ID,
          'srcId': 0,
          'type': 3,
          'iconPath': path,
          'timer': -100,
          'count': 0}]
        gameglobal.rds.ui.player.changeStateIcon([], data)

    def setActivityState(self):
        if gameglobal.rds.configData.get('enableActivityStateBonus', False):
            for stateId in BigWorld.player().activityStateIds:
                BigWorld.player().addFakeState(stateId)

    def setVIPModeState(self):
        if self.vipBarRank and SCD.data.get('VIPBuff', None):
            stateID = SCD.data.get('VIPBuff', None)[self.vipBarRank]
            path = str(SD.data.get(stateID, {}).get('iconId', 'notFound')) + '.dds'
            data = [{'id': stateID,
              'srcId': 0,
              'type': 3,
              'iconPath': path,
              'timer': -100,
              'count': 1}]
            gameglobal.rds.ui.player.changeStateIcon(data, [])

    def addFakeState(self, stateID):
        if stateID <= 0:
            return
        path = str(SD.data.get(stateID, {}).get('iconId', 'notFound')) + '.dds'
        iconShowType = SD.data.get(stateID, {}).get('iconShowType', 4)
        if iconShowType <= 2:
            iconShowType = 4
        data = [{'id': stateID,
          'srcId': 0,
          'type': iconShowType,
          'iconPath': path,
          'timer': -100,
          'count': 1}]
        gameglobal.rds.ui.player.changeStateIcon(data, [])

    def quitFakeState(self, stateID):
        if stateID <= 0:
            return
        path = str(SD.data.get(stateID, {}).get('iconId', 'notFound')) + '.dds'
        iconShowType = SD.data.get(stateID, {}).get('iconShowType', 4)
        if iconShowType <= 2:
            iconShowType = 4
        data = [{'id': stateID,
          'srcId': 0,
          'type': iconShowType,
          'iconPath': path,
          'timer': -100,
          'count': 0}]
        gameglobal.rds.ui.player.changeStateIcon([], data)

    def __onConfirmSafeMode(self):
        self.safeModeBoxId = 0
        BigWorld.openUrl('https://mima.163.com/nie/ts_remind_index.aspx')

    def __onCancelSafeMode(self):
        self.safeModeBoxId = 0

    def takeFigurePhoto(self, fileName = 'figure.png', needCheck = True):
        if not self.inWorld:
            return
        if not needCheck:
            self.onCheckUploadCharSnapshot(fileName)
            return
        if self.needCharSnapshot:
            return
        current = utils.getNow()
        if utils.isSameDay(current, self.charSnapshotTime):
            return
        if self.isAppBind:
            self.onCheckUploadCharSnapshot(fileName)
            return
        gamelog.info('@szh takeFigurePhoto', fileName)
        if not self._isInCross():
            self.base.checkUploadCharSnapshot(fileName)

    def onCheckUploadCharSnapshot(self, fileName):
        gamelog.info('@szh onCheckUploadCharSnapshot', fileName)
        headGen = capturePhoto.FigurePhotoGen.getInstance('gui/taskmask.tga', 10)
        headGen2 = capturePhoto.FigureHeadPhotoGen.getInstance('gui/taskmask.tga', 10)
        if gameglobal.rds.configData.get('enableBigHeadSnapShot', False):
            headGen2.aaScale = 60
            headGen.aaScale = 192
        else:
            headGen2.aaScale = 27
            headGen.aaScale = 128
        self.startTakeFigurePhoto(headGen, fileName, self.startTakeFigurePhoto, (headGen2,
         'head' + fileName,
         self.realUploadFigurePhoto,
         (fileName, 'head' + fileName)))

    def startTakeFigurePhoto(self, headGen, fileName, callback = None, callbackArgs = ()):
        headGen.setModelFinishCallback(Functor(self.savePhoto, headGen, fileName, callback, callbackArgs))
        headGen.initFlashMesh()
        headGen.startCapture(0, None, ('1101',))

    def savePhoto(self, headGen, fileName, callback = None, callbackArgs = ()):
        if not self.inWorld:
            return
        headGen.take()
        BigWorld.callback(1, Functor(self._savePhoto, headGen, fileName, callback, callbackArgs))

    def _savePhoto(self, headGen, fileName, callback = None, callbackArgs = ()):
        if hasattr(headGen.adaptor, 'saveFrame'):
            headGen.adaptor.saveFrame(fileName)
        BigWorld.callback(1, Functor(self.endSavePhoto, headGen, fileName, callback, callbackArgs))

    def endSavePhoto(self, headGen, fileName, callback = None, callbackArgs = ()):
        headGen.endCapture()
        if callback != None:
            callback(*callbackArgs)

    def realUploadFigurePhoto(self, fileName, fileName2):
        try:
            image1 = Image.open(fileName)
            image2 = Image.open(fileName2)
            if image1 and image2:
                image2 = image2.resize((image2.size[0] * 2 / 3, image2.size[1] * 2 / 3), Image.ANTIALIAS)
                image1.paste(image2, (image1.size[0] - image2.size[0],
                 0,
                 image1.size[1],
                 image2.size[1]))
                image1.load()
                background = Image.new('RGB', image1.size, (21, 22, 23))
                background.paste(image1, mask=image1.split()[3])
                newName = fileName[0:-4] + '.jpg'
                background.save(newName)
                filePath = '../game/' + newName
                self.uploadCharSnapshot(filePath)
        except Exception as e:
            errmsg = 'failed to upload figure photo %s %s %s' % (self.gbId, e.message, str(type(e)))
            self.reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_CRITICAL, [errmsg], 0, {})

    def flashPush(self, path = 'http://tudou.com/v/sw65hx_VTwE/&resourceId=0_04_05_99&autoPlay=true/v.swf'):
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_FLASH, {'click': Functor(self.onClickFlash, path)})
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_FLASH)

    def onClickFlash(self, path):
        self.showFlash(path)
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_FLASH)

    def showFlash(self, path):
        gameglobal.rds.ui.flash.show(path)

    def showRoleCard(self, isDown):
        if isDown:
            if gameglobal.rds.ui.rolecard.collectMediator:
                gameglobal.rds.ui.rolecard.onCloseCollect()
            else:
                gameglobal.rds.ui.rolecard.show()

    def showFengWuZhi(self, isDown):
        if isDown:
            if gameglobal.rds.ui.fengWuZhi.mediator:
                gameglobal.rds.ui.fengWuZhi.clearWidget()
            else:
                gameglobal.rds.ui.fengWuZhi.show()

    def showPersonSpace(self, isDown):
        if isDown:
            if self.getPersonalSysProxy().isOpen():
                self.getPersonalSysProxy().hide()
            else:
                self.getPersonalSysProxy().openZoneMyself(const.PERSONAL_ZONE_SRC_SYSTEM)

    def showSpriteWar(self, isDown):
        if isDown:
            if gameglobal.rds.ui.summonedWarSprite.widget:
                gameglobal.rds.ui.summonedWarSprite.hide()
            else:
                gameglobal.rds.ui.summonedWarSprite.show(uiConst.WAR_SPRITE_TAB_INDEX0)

    def showMountWing(self, isDown):
        if isDown:
            if gameglobal.rds.ui.wingAndMount.mediator:
                gameglobal.rds.ui.wingAndMount.clearWidget()
            else:
                gameglobal.rds.ui.wingAndMount.show()

    def showStall(self, isDown):
        if isDown:
            if gameglobal.rds.ui.booth.boothMediator:
                gameglobal.rds.ui.booth.clearWidget()
            else:
                gameglobal.rds.ui.skill.enterBooth()

    def showPvpEnhance(self, isDown):
        if isDown:
            if gameglobal.rds.ui.pvpEnhance.mediator:
                gameglobal.rds.ui.pvpEnhance.hide()
            else:
                gameglobal.rds.ui.pvpEnhance.checkShow()

    def showChatRoom(self, isDown):
        if isDown:
            if gameglobal.rds.ui.chatRoomCreate.mediator:
                gameglobal.rds.ui.chatRoomCreate.hide()
            elif BigWorld.player().chatRoomNUID:
                BigWorld.player().showGameMsg(GMDD.data.CHATROOM_JOINED, ())
            else:
                gameglobal.rds.ui.chatRoomCreate.show(uiConst.CHATROOM_CREATE)

    def showJieQi(self, isDown):
        if isDown:
            if gameconfigCommon.enableJieQiV2():
                if gameglobal.rds.ui.jieQiV2.widget:
                    gameglobal.rds.ui.jieQiV2.hide()
                else:
                    gameglobal.rds.ui.jieQiV2.show()
            elif gameglobal.rds.ui.jieQi.mediator:
                gameglobal.rds.ui.jieQi.hide()
            else:
                gameglobal.rds.ui.jieQi.show()

    def showPvpJJC(self, isDown):
        if isDown:
            if gameglobal.rds.ui.pvPPanel.widget:
                gameglobal.rds.ui.pvPPanel.clearWidget()
            else:
                gameglobal.rds.ui.pvPPanel.show()

    def showGuibao(self, isDown):
        if isDown:
            if gameglobal.rds.ui.guibaoge.mediator:
                gameglobal.rds.ui.guibaoge.hide()
            else:
                gameglobal.rds.ui.guibaoge.show()

    def showUserBack(self, isDown):
        if isDown:
            if gameglobal.rds.ui.backflow.widget:
                gameglobal.rds.ui.backflow.hide()
            else:
                gameglobal.rds.ui.backflow.show()

    def showSummonFriend(self, isDown):
        if isDown:
            if gameglobal.rds.ui.summonFriend.mediator or gameglobal.rds.ui.summonFriendNew.widget or gameglobal.rds.ui.summonFriendBGV2.widget:
                gameglobal.rds.ui.summonFriend.hide()
                gameglobal.rds.ui.summonFriendNew.hide()
                gameglobal.rds.ui.summonFriendBGV2.hide()
            elif gameglobal.rds.configData.get('enableInvitePoint', False):
                if gameglobal.rds.configData.get('enableSummonFriendV2', False):
                    gameglobal.rds.ui.summonFriendBGV2.show(uiConst.SUMMON_FRIEND_TAB_INDEX1, 'inviteBtn')
                else:
                    gameglobal.rds.ui.summonFriendNew.show(2)
            else:
                gameglobal.rds.ui.summonFriend.show(0)

    def showMentor(self, isDown):
        if isDown:
            if gameglobal.rds.ui.mentorEx.mediator:
                gameglobal.rds.ui.mentorEx.hideMentor()
            else:
                gameglobal.rds.ui.mentorEx.show()

    def showItemSource(self, isDown):
        if not isDown:
            if gameglobal.rds.configData.get('enableNewItemSearch', False):
                gameglobal.rds.ui.itemSourceInfor.openPanel()

    def dealItemSourceConflict(self):
        BigWorld.player().showGameMsg(GMDD.data.KEY_CONFLICT_ITEM_SOURCE, ())

    def showSkillMacro(self, isDown):
        if isDown:
            gameglobal.rds.ui.skillMacroOverview.showOverviewPanel()

    def dealSkillMacroConflict(self):
        BigWorld.player().showGameMsg(GMDD.data.KEY_CONFLICT_SKILL_MACRO, ())

    def dealHotKeyConflict(self, msgId):
        BigWorld.player().showGameMsg(msgId, ())

    def removeHotKeyConflict(self, conflictKey, rdfkey):
        if conflictKey.inkeyDef(rdfkey.key, rdfkey.mods):
            conflictKey.clearPart(1)
        if conflictKey.inkeyDef(rdfkey.key2, rdfkey.mods2):
            conflictKey.clearPart(2)
        hotkeyProxy.getInstance().saveHotKey()

    def voiceCapture(self, isDown):
        mode = appSetting.SoundSettingObj._value[22]
        if mode:
            if isDown:
                ccManager.instance().startCapture(const.CC_SESSION_TEAM)
            else:
                ccManager.instance().stopCapture(const.CC_SESSION_TEAM)

    def showCardSystem(self, isDown):
        if isDown:
            gameglobal.ui.cardSystem.show()

    def showCardSystem(self, isDown):
        if isDown:
            if gameglobal.rds.ui.cardSystem.widget:
                gameglobal.rds.ui.cardSystem.hide()
            else:
                gameglobal.rds.ui.cardSystem.show()

    def dealShowCardSystemConflict(self):
        BigWorld.player().showGameMsg(GMDD.data.KEY_CARD_SYSTEM_CONFLICT, ())
