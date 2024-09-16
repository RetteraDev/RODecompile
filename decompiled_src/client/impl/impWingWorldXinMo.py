#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impWingWorldXinMo.o
from gamestrings import gameStrings
import BigWorld
import utils
import const
import gameglobal
import gamelog
import formula
import gametypes
from guis import uiConst
from guis import uiUtils
from callbackHelper import Functor
from cdata import game_msg_def_data as GMDD
from data import wing_world_config_data as WWCD

class ImpWingWorldXinMo(object):
    """
    \xe6\xb4\xbb\xe5\x8a\xa8\xe7\x8a\xb6\xe6\x80\x81
    const.WING_WORLD_XINMO_STATE_CLOSE = 0
    const.WING_WORLD_XINMO_STATE_ARENA = 1    # \xe6\x93\x82\xe5\x8f\xb0\xe8\xb5\x9b
    const.WING_WORLD_XINMO_STATE_UNIQUE_BOSS = 2  # \xe5\x94\xaf\xe4\xb8\x80BOSS
    const.WING_WORLD_XINMO_STATE_NORMAL_BOSS = 3  # \xe5\x85\xa8\xe6\xb0\x91BOSS
    
    \xe6\x93\x82\xe5\x8f\xb0\xe7\x9b\xb8\xe5\x85\xb3\xe7\x9a\x84\xe4\xb8\x89\xe4\xb8\xaa\xe9\x9d\xa2\xe6\x9d\xbf\xe6\x95\xb0\xe6\x8d\xae\xe5\x8f\x91\xe9\x80\x81
    const.PROXY_KEY_WING_WORLD_ARENA = 309    # \xe5\x8f\x91\xe9\x80\x81\xe6\x93\x82\xe5\x8f\xb0\xe9\x80\x89\xe6\x8b\xa9\xe9\x9d\xa2\xe6\x9d\xbf\xe4\xbf\xa1\xe6\x81\xaf
    const.PROXY_KEY_WING_WORLD_ARENA_HISTORY = 310    # \xe5\x8f\x91\xe9\x80\x81\xe5\xaf\xb9\xe6\x88\x98\xe5\x8e\x86\xe5\x8f\xb2\xe9\x9d\xa2\xe6\x9d\xbf\xe4\xbf\xa1\xe6\x81\xaf
    const.PROXY_KEY_WING_WORLD_ARENA_ROUND_MATCH = 311    # \xe5\x8f\x91\xe9\x80\x81\xe6\x8c\x87\xe5\xae\x9a\xe8\xbd\xae\xe6\xac\xa1\xe6\x8c\x87\xe5\xae\x9a\xe6\xaf\x94\xe8\xb5\x9b\xe7\x9a\x84\xe5\xaf\xb9\xe6\x88\x98\xe4\xbf\xa1\xe6\x81\xaf
    """

    def _showWingWorldXinMoStateChangeMsg(self, state, skip = False):
        if state == const.WING_WORLD_XINMO_STATE_ENTER_ML:
            self.showGameMsg(GMDD.data.WING_WORLD_XINMO_ML_ENTER_NOTIFY, ())
        if state == const.WING_WORLD_XINMO_STATE_ARENA:
            self.showGameMsg(GMDD.data.WING_WORLD_XINMO_ARENA_START_NOTIFY, ())
        elif state == const.WING_WORLD_XINMO_STATE_UNIQUE_BOSS:
            self.showGameMsg(GMDD.data.WING_WORLD_XINMO_UNIQUE_BOSS_START_NOTIFY, ())
        elif state == const.WING_WORLD_XINMO_STATE_NORMAL_BOSS:
            if skip:
                self.showGameMsg(GMDD.data.WING_WORLD_XINMO_NORMAL_BOSS_START_BY_SKIP_UNIQUE_NOTIFY, ())
            else:
                self.showGameMsg(GMDD.data.WING_WORLD_XINMO_NORMAL_BOSS_START_NOTIFY, ())
        elif state == const.WING_WORLD_XINMO_STATE_PRE_END:
            self.showGameMsg(GMDD.data.WING_WORLD_XINMO_PRE_END_NOTIFY, ())

    def onGetWingWorldXinMoStateOnLogon(self, state, startTime):
        self._showWingWorldXinMoStateChangeMsg(state)
        self.showPushWidget(state, startTime)

    def onWingWorldXinMoStateChange(self, state, startTime, skip):
        self._showWingWorldXinMoStateChangeMsg(state, skip=skip)
        self.showPushWidget(state, startTime)

    def showPushWidget(self, state, startTime):
        if not gameglobal.rds.configData.get('enableWingWorld', False) or not gameglobal.rds.configData.get('enableWingWorldXinMo', False):
            return
        endTime = startTime
        if state == const.WING_WORLD_XINMO_STATE_CLIENT_PREPARE or state == const.WING_WORLD_XINMO_STATE_ENTER_ML:
            endTime = int(utils.getNextCrontabTime(WWCD.data.get('xinmoStartCrontab')))
        elif state == const.WING_WORLD_XINMO_STATE_UNIQUE_BOSS:
            endTime += WWCD.data.get('xinmoUniqueBossTime', 0)
            gameglobal.rds.ui.zhiQiangDuiJue.hide()
            gameglobal.rds.ui.wingStageChoose.hide()
        elif state == const.WING_WORLD_XINMO_STATE_NORMAL_BOSS:
            endTime += WWCD.data.get('xinmoNormalBossTime', 0)
            gameglobal.rds.ui.zhiQiangDuiJue.hide()
            gameglobal.rds.ui.wingStageChoose.hide()
        elif state == const.WING_WORLD_XINMO_STATE_PRE_END:
            endTime += WWCD.data.get('xinmoPreEndTime', 0)
        gameglobal.rds.ui.wingCombatPush.show(state, endTime)

    def onGetWingWorldXinMoArenaAllows(self, allowGroupNUIDs, arenaWinnerGroupNUID, cnt, arenaWinnerWaitEndTime):
        """
        \xe6\x9f\xa5\xe8\xaf\xa2\xe5\xbd\x93\xe5\x89\x8dallows\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param allowGroupNUIDs:\xe5\xbd\x93\xe5\x89\x8d\xe8\xa2\xab\xe8\xb5\x8b\xe4\xba\x88\xe8\xb5\x84\xe6\xa0\xbc\xe7\x9a\x84\xe9\x98\x9f\xe4\xbc\x8d 
        """
        gameglobal.rds.ui.zhiQiangDuiJue.onGetAllowsData(allowGroupNUIDs, arenaWinnerGroupNUID, cnt, arenaWinnerWaitEndTime)

    def onWingWorldXinMoArenaMatchApplySucc(self, matchNo, maxWaitingTime, isFull):
        """
        \xe9\x80\x89\xe6\x8b\xa9\xe6\x93\x82\xe5\x8f\xb0\xe6\x88\x90\xe5\x8a\x9f\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83\xef\xbc\x8c\xe8\xbf\x9b\xe5\x85\xa5\xe7\xad\x89\xe5\xbe\x85\xe7\x8a\xb6\xe6\x80\x81
        :param matchNo:\xe6\x89\x80\xe9\x80\x89\xe6\x8b\xa9\xe7\x9a\x84\xe6\x93\x82\xe5\x8f\xb0\xe7\xbc\x96\xe5\x8f\xb7
        :param maxWaitingTime: \xe6\x9c\x80\xe5\xa4\x9a\xe7\x9a\x84\xe7\xad\x89\xe5\xbe\x85\xe6\x97\xb6\xe9\x97\xb4\xef\xbc\x88\xe4\xb8\xba\xe6\x9c\xac\xe8\xbd\xae\xe6\x93\x82\xe5\x8f\xb0\xe5\x89\xa9\xe4\xbd\x99\xe7\xad\x89\xe5\xbe\x85\xe6\x97\xb6\xe9\x97\xb4\xef\xbc\x8c\xe8\xb6\x85\xe6\x97\xb6\xe4\xbc\x9a\xe5\xbc\xba\xe5\x88\xb6\xe5\x88\x86\xe9\x85\x8d\xe7\x9a\x84\xef\xbc\x89
        :param isFull:\xe6\x93\x82\xe5\x8f\xb0\xe6\x98\xaf\xe5\x90\xa6\xe4\xba\xba\xe6\x95\xb0\xe8\xb6\xb3\xe5\xa4\x9f\xef\xbc\x8c\xe5\x87\x86\xe5\xa4\x87\xe5\xbc\x80\xe5\xa7\x8b\xe4\xba\x86
        """
        if not isFull:
            self.showGameMsg(GMDD.data.WING_WORLD_XINMO_APPLY_SUCC, (matchNo,))
        gameglobal.rds.ui.wingStageChoose.onApplyArenaSucc(matchNo)

    def onWingWorldXinMoArenaApplyTimeOut(self, roundNo, matchNo):
        """
        \xe6\xb2\xa1\xe6\x9c\x89\xe9\x80\x89\xe6\x8b\xa9\xe6\x93\x82\xe5\x8f\xb0\xef\xbc\x8c\xe8\xb6\x85\xe6\x97\xb6\xe8\xa2\xab\xe8\x87\xaa\xe5\x8a\xa8\xe5\x88\x86\xe9\x85\x8d\xe5\x88\xb0\xe6\x8c\x87\xe5\xae\x9a\xe6\x93\x82\xe5\x8f\xb0\xef\xbc\x8c\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe5\xbc\xb9\xe5\x87\xba\xe4\xba\x8c\xe6\xac\xa1\xe7\xa1\xae\xe8\xae\xa4\xef\xbc\x8c\xe6\x9d\xa5\xe8\xbf\x9b\xe5\x85\xa5\xe6\x93\x82\xe5\x8f\xb0
        :param roundNo: 
        :param matchNo: 
        :return: 
        """
        if formula.spaceInWingWorldXinMoArena(self.spaceNo):
            return
        msg = gameStrings.TEXT_IMPWINGWORLDXINMO_108 % matchNo
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.selectXimoArena, matchNo), yesBtnText=gameStrings.TEXT_IMPWINGWORLDXINMO_109, noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1, isModal=False)

    def selectXimoArena(self, matchNo):
        BigWorld.player().cell.applyEnterWingWorldXinMoArena()

    def onWingWorldXinMoArenaCanEnter(self, matchNo):
        """
        \xe6\x93\x82\xe5\x8f\xb0\xe7\xa9\xba\xe9\x97\xb4\xe5\xb7\xb2\xe5\x88\x9b\xe5\xbb\xba\xef\xbc\x8c\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe5\xbc\xb9\xe5\x87\xba\xe4\xba\x8c\xe6\xac\xa1\xe7\xa1\xae\xe8\xae\xa4\xef\xbc\x8c\xe6\x9d\xa5\xe8\xbf\x9b\xe5\x85\xa5\xe6\x93\x82\xe5\x8f\xb0
        :param roundNo: 
        :param matchNo: \xe5\xa6\x82\xe6\x9e\x9cmatchNo\xe4\xb8\xba-1\xef\xbc\x8c\xe5\xb0\xb1\xe6\x98\xaf\xe4\xbb\x8eset_fbStatusList\xe8\xb0\x83\xe8\xbf\x9b\xe6\x9d\xa5\xe7\x9a\x84
        :return:
        """
        if formula.spaceInWingWorldXinMoArena(self.spaceNo):
            return
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_ENTER_WING_WOLRD_XINMO_ARENA)
        self.onClickEnterWingWorldXinmoArena()

    def onWingWorldXinMoArenaFuBenUpdated(self):
        if formula.spaceInWingWorldXinMoArena(self.spaceNo):
            return
        if getattr(gameglobal.rds.ui.wingCombatPush, 'activityState', 0) != const.WING_WORLD_XINMO_STATE_ARENA:
            return
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_ENTER_WING_WOLRD_XINMO_ARENA)

    def onClickEnterWingWorldXinmoArena(self):
        if formula.spaceInWingWorldXinMoArena(self.spaceNo):
            return
        msg = gameStrings.TEXT_IMPWINGWORLDXINMO_138
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.enterXimoArena, yesBtnText=gameStrings.TEXT_IMPWINGWORLDXINMO_109, noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1, isModal=False)

    def enterXimoArena(self):
        BigWorld.player().cell.applyEnterWingWorldXinMoArena()
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_ENTER_WING_WOLRD_XINMO_ARENA)
        gameglobal.rds.ui.wingStageChoose.hide()
        gameglobal.rds.ui.zhiQiangDuiJue.hide()

    def onWingWorldXinMoUniqueNotifyToArenaWinner(self):
        """
        \xe6\x88\x90\xe4\xb8\xba\xe6\x93\x82\xe4\xb8\xbb\xe5\x90\x8e\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83\xef\xbc\x8c\xe6\x93\x82\xe4\xb8\xbb\xe9\x98\x9f\xe4\xbc\x8d\xe6\x88\x90\xe5\x91\x98\xe4\xbc\x9a\xe8\xa2\xab\xe8\xb0\x83\xe7\x94\xa8\xef\xbc\x8c\xe8\xb0\x83\xe7\x94\xa8\xe6\x97\xb6\xe6\x9c\xba\xe4\xb8\xba\xe5\x94\xaf\xe4\xb8\x80boss\xe9\x98\xb6\xe6\xae\xb5\xe7\x99\xbb\xe5\xbd\x95\xe6\x88\x96\xe8\xb7\xa8\xe6\x9c\x8d\xef\xbc\x8c\xe4\xb8\x94\xe5\x94\xaf\xe4\xb8\x80boss\xe7\x8e\xb0\xe5\x9c\xa8\xe6\xb2\xa1\xe4\xba\xba\xe6\x89\x93\xe8\xbf\x87
        """
        if self.groupHeader == self.id:
            msg = gameStrings.TEXT_IMPWINGWORLDXINMO_152
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.applyXinmoUnique), yesBtnText=gameStrings.TEXT_FUBENDEGREEPROXY_153_1, noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1, isModal=False)

    def applyXinmoUnique(self):
        BigWorld.player().cell.applyWingWorldXinMoUniqueBoss()

    def onGetWingWorldXinMoInspire(self, roundNo, matchNo, inspireInfo, readyTime, myInspireGroupNUID):
        """
        \xe9\xbc\x93\xe8\x88\x9e\xe4\xbf\xa1\xe6\x81\xaf\xe5\x9b\x9e\xe8\xb0\x83
        :param roundNo:\xe8\xbd\xae\xe6\xac\xa1 
        :param matchNo: \xe6\x93\x82\xe5\x8f\xb0\xe7\xbc\x96\xe5\x8f\xb7
        :param inspireInfo: \xe9\xbc\x93\xe8\x88\x9e\xe4\xbf\xa1\xe6\x81\xaf inspireInfo = {groupNUID:(inspireNum, teamName), ...}\xe5\xa6\x82\xe6\x9e\x9cgroupNUID\xe4\xb8\x8d\xe5\x9c\xa8inspireInfo\xe9\x87\x8c\xe9\x9d\xa2\xef\xbc\x8c\xe8\xaf\xb4\xe6\x98\x8e\xe8\xbf\x98\xe6\xb2\xa1\xe6\x9c\x89\xe8\xa2\xab\xe9\xbc\x93\xe8\x88\x9e\xef\xbc\x8c\xe6\x98\xbe\xe7\xa4\xba0\xe5\xb0\xb1\xe5\x8f\xaf\xe4\xbb\xa5\xe4\xba\x86
        :param readyTime: \xe6\x9c\xac\xe5\xb1\x80\xe5\xbc\x80\xe5\xa7\x8b\xe5\x87\x86\xe5\xa4\x87\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4\xe6\x88\xb3
        :param myInspireGroupNUID: \xe6\x9c\xac\xe6\x93\x82\xe5\x8f\xb0\xe4\xb8\xad\xe6\x88\x91\xe9\xbc\x93\xe8\x88\x9e\xe7\x9a\x84groupNUID\xef\xbc\x8c\xe4\xb8\xba0\xe8\xa1\xa8\xe7\xa4\xba\xe6\xb2\xa1\xe6\x9c\x89\xe9\xbc\x93\xe8\x88\x9e\xe6\x9c\xac\xe5\x9c\xba\xe4\xb8\xad\xe4\xbb\xbb\xe4\xb8\x80\xe6\x96\xb9\xef\xbc\x88\xe5\x8f\xaf\xe8\x83\xbd\xe6\x98\xaf\xe6\xb2\xa1\xe9\xbc\x93\xe8\x88\x9e\xef\xbc\x8c\xe4\xb9\x9f\xe5\x8f\xaf\xe8\x83\xbd\xe6\x98\xaf\xe5\xb7\xb2\xe7\xbb\x8f\xe9\xbc\x93\xe8\x88\x9e\xe4\xba\x86\xe5\x88\xab\xe7\x9a\x84\xe6\x93\x82\xe5\x8f\xb0\xef\xbc\x89
        """
        endCheerTime = readyTime + WWCD.data.get('xinmoArenaCheerTime', 30)
        gameglobal.rds.ui.cheerTopBar.onGetServerData(roundNo, matchNo, inspireInfo, endCheerTime, myInspireGroupNUID)

    def onWingWorldXinMoArenaMatchResult(self, isWin, isDirectly):
        """
        \xe9\x80\x9a\xe7\x9f\xa5\xe6\x93\x82\xe5\x8f\xb0\xe5\x8f\x82\xe4\xb8\x8e\xe8\x80\x85\xe6\xaf\x94\xe8\xb5\x9b\xe7\xbb\x93\xe6\x9e\x9c
        :param isWin:\xe6\x98\xaf\xe5\x90\xa6\xe8\x83\x9c\xe5\x88\xa9 
        :param isDirectly:\xe6\x98\xaf\xe5\x90\xa6\xe8\x83\x9c\xe8\xbd\xae\xe7\xa9\xba\xe7\x9b\xb4\xe6\x8e\xa5\xe8\x83\x9c\xe5\x88\xa9
        """
        pass

    def onWingWorldXinMoUniqueBossResult(self, isSucc):
        """
        \xe6\xaf\x8f\xe5\x9c\xba\xe5\x94\xaf\xe4\xb8\x80BOSS\xe7\xbb\x93\xe6\x9d\x9f\xe5\x90\x8e\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83\xef\xbc\x8c\xe5\x8f\xaa\xe6\x9c\x89allows\xe7\x9a\x84\xe9\x98\x9f\xe4\xbc\x8d\xe6\x88\x90\xe5\x91\x98\xe4\xbc\x9a\xe6\x94\xb6\xe5\x88\xb0\xe8\xbf\x99\xe4\xb8\xaa\xe5\x9b\x9e\xe8\xb0\x83
        :param isSucc: \xe6\x8c\x91\xe6\x88\x98\xe7\xbb\x93\xe6\x9e\x9c\xef\xbc\x8c\xe6\x98\xaf\xe5\x90\xa6\xe6\x88\x90\xe5\x8a\x9f
        """
        gameglobal.rds.ui.zhiQiangDuiJue.onBossFinished(isSucc)

    def onGetWingWorldXinMoAnnalUUID(self, uuid, roundNo, matchNo):
        """
        \xe8\x8e\xb7\xe5\xbe\x97\xe6\x93\x82\xe5\x8f\xb0\xe8\xa7\x82\xe6\x88\x98\xe5\xbd\x95\xe5\x83\x8fuuid\xef\xbc\x8c\xe4\xbd\xbf\xe7\x94\xa8cell.startAnnalReplay(uuid)\xef\xbc\x8c\xe5\xbc\x80\xe5\xa7\x8b\xe8\xa7\x82\xe6\x88\x98
        :param uuid: 
        :param roundNo: 
        :param matchNo: 
        """
        BigWorld.player().cell.startAnnalReplay(uuid, True, False)

    def onGetWingWorldXinMoUniqueBossAnnalUUID(self, uuid):
        """
        \xe8\x8e\xb7\xe5\xbe\x97\xe5\x94\xaf\xe4\xb8\x80BOSS\xe8\xa7\x82\xe6\x88\x98\xe5\xbd\x95\xe5\x83\x8fuuid
        :param uuid: 
        """
        BigWorld.player().cell.startAnnalReplay(uuid, True, False)

    def onGetWingWorldXinMoArenaFinalWinnerInfo(self, members, headerGbId, fromHostId):
        """
        \xe6\x93\x82\xe4\xb8\xbb\xe9\x98\x9f\xe4\xbc\x8d\xef\xbc\x8c\xe7\xbf\xbc\xe4\xb8\x96\xe7\x95\x8c\xe5\x9f\x8e\xe6\x88\x98buff\xe5\x8a\xa0\xe6\x88\x90\xe4\xb9\x8b\xe5\x89\x8d\xe5\x8f\x91\xe9\x80\x81\xef\xbc\x8c\xe5\x9b\xa0\xe4\xb8\xba\xe9\x9c\x80\xe8\xa6\x81\xe5\x9c\xa8\xe6\x8c\x87\xe5\xae\x9abuff\xe7\x9a\x84tips\xe4\xb8\x8a\xe6\x98\xbe\xe7\xa4\xba\xe6\x93\x82\xe4\xb8\xbb\xe9\x98\x9f\xe5\x91\x98\xe5\x90\x8d\xe5\xad\x97
        :param members:\xe6\x88\x90\xe5\x91\x98\xe5\x90\x8d\xe5\xad\x97 {gbId:name, ...} 
        :param headerGbId: \xe9\x98\x9f\xe9\x95\xbfgbId
        :param fromHostId: \xe6\x9d\xa5\xe6\xba\x90\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8hostId
        """
        self.wingWorldXinmoArenaFinalWinnerBuffDesc = members

    def onGetWingWorldXinMoUniqueBossWinnerInfo(self, members, headerGbId, fromHostId):
        """
        \xe5\x94\xaf\xe4\xb8\x80BOSS\xe8\x8e\xb7\xe8\x83\x9c\xe9\x98\x9f\xe4\xbc\x8d\xef\xbc\x8c\xe5\x85\xa8\xe6\xb0\x91BOSS\xe5\x89\xaf\xe6\x9c\xacbuff\xe5\x8a\xa0\xe6\x88\x90\xe4\xb9\x8b\xe5\x89\x8d\xe5\x8f\x91\xe9\x80\x81\xef\xbc\x8c\xe5\x9b\xa0\xe4\xb8\xba\xe9\x9c\x80\xe8\xa6\x81\xe5\x9c\xa8\xe6\x8c\x87\xe5\xae\x9abuff\xe7\x9a\x84tips\xe4\xb8\x8a\xe6\x98\xbe\xe7\xa4\xba\xe6\x93\x82\xe4\xb8\xbb\xe9\x98\x9f\xe5\x91\x98\xe5\x90\x8d\xe5\xad\x97
        :param members:\xe6\x88\x90\xe5\x91\x98\xe5\x90\x8d\xe5\xad\x97 {gbId:name, ...} 
        :param headerGbId: \xe9\x98\x9f\xe9\x95\xbfgbId
        :param fromHostId: \xe6\x9d\xa5\xe6\xba\x90\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8hostId
        """
        self.wingWorldXinMoUniqueBossWinnerBuffDesc = members

    def onWingWorldArenaMatchAnnalCntThreshold(self, roundNo, matchInfos):
        """
        \xe6\x93\x82\xe5\x8f\xb0\xe8\xa7\x82\xe6\x88\x98\xe4\xba\xba\xe6\x95\xb0\xe8\xbe\xbe\xe5\x88\xb0\xe5\x85\xac\xe5\x91\x8a\xe9\x98\x88\xe5\x80\xbc\xef\xbc\x8c\xe5\x8f\xaf\xe8\x83\xbd\xe4\xb8\x80\xe6\xac\xa1\xe5\x8f\x91\xe6\x9d\xa5\xe5\xa4\x9a\xe4\xb8\xaa\xe6\x93\x82\xe5\x8f\xb0\xef\xbc\x8c\xe9\x9c\x80\xe8\xa6\x81\xe5\x87\xba\xe7\x8e\xb0\xe5\xa4\x9a\xe6\x9d\xa1\xe6\xb6\x88\xe6\x81\xaf
        \xe6\xb6\x88\xe6\x81\xaf\xe9\x93\xbe\xe6\x8e\xa5\xe4\xb8\xad\xe9\x9c\x80\xe8\xa6\x81\xe4\xbf\x9d\xe7\x95\x99roundNo\xe5\x92\x8cmatchNo\xef\xbc\x8c\xe5\x86\x8d\xe5\x8e\xbb\xe8\xb0\x83\xe7\x94\xa8\xe8\xa7\x82\xe6\x88\x98\xe5\x85\xa5\xe5\x8f\xa3
        :param roundNo: \xe8\xbd\xae\xe6\xac\xa1\xe7\xbc\x96\xe5\x8f\xb7
        :param matchInfos: matchInfos[matchNo] = [teamAHostid, teamAName, teamAHeaderName, teamBHostId, teamBName, teamBHeaderName, annalFakeCnt]
        """
        gamelog.debug('@xzh onWingWorldArenaMatchAnnalCntThreshold', roundNo, matchInfos)
        for i, matchNo in enumerate(matchInfos):
            teamAName = matchInfos[matchNo][1]
            teamAHeaderNameB = matchInfos[matchNo][2]
            teamBName = matchInfos[matchNo][4]
            teamBHeaderName = matchInfos[matchNo][5]
            annalFakeCnt = matchInfos[matchNo][6]
            self.showGameMsg(GMDD.data.WING_WORLD_XINMO_MATCH_ANNAL_CTN, (teamAHeaderNameB,
             teamAName,
             teamBHeaderName,
             teamBName,
             annalFakeCnt,
             roundNo,
             matchNo))

    def onWingWorldXinMoUniqueBossAnnalCntThreshold(self, fromHostId, teamName, headerName, annalFakeCnt):
        """
        \xe5\x94\xaf\xe4\xb8\x80BOSS\xe8\xa7\x82\xe6\x88\x98\xe4\xba\xba\xe6\x95\xb0\xe8\xbe\xbe\xe5\x88\xb0\xe5\x85\xac\xe5\x91\x8a\xe9\x98\x88\xe5\x80\xbc
        \xe6\xb6\x88\xe6\x81\xaf\xe9\x93\xbe\xe6\x8e\xa5\xe4\xb8\xad\xe7\x9b\xb4\xe6\x8e\xa5\xe8\xb0\x83\xe7\x94\xa8\xe5\x94\xaf\xe4\xb8\x80BOSS\xe7\x9a\x84\xe8\xa7\x82\xe6\x88\x98
        :param fromHostId: \xe6\x8c\x91\xe6\x88\x98\xe9\x98\x9f\xe4\xbc\x8d\xe6\x9d\xa5\xe6\xba\x90\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8id
        :param headerName: \xe9\x98\x9f\xe9\x95\xbf\xe5\x90\x8d\xe5\xad\x97
        :param annalFakeCnt: \xe5\xbd\x93\xe5\x89\x8d\xe8\xa7\x82\xe6\x88\x98\xe4\xba\xba\xe6\x95\xb0\xef\xbc\x88\xe8\xb0\x83\xe6\x95\xb4\xe5\x90\x8e\xef\xbc\x89
        """
        gamelog.debug('@xzh onWingWorldXinMoUniqueBossAnnalCntThreshold', fromHostId, headerName, annalFakeCnt)
        fromHostName = utils.getServerName(fromHostId)
        self.showGameMsg(GMDD.data.WING_WORLD_XINMO_BOSS_ANNAL_CTN, (headerName, teamName, annalFakeCnt))

    def onGetWingWorldXinMoAnnalCount(self, annalFakeCnt):
        """
        \xe8\xa7\x82\xe6\x88\x98\xe4\xba\xba\xe6\x95\xb0\xe5\x90\x8c\xe6\xad\xa5
        :param annalFakeCnt:\xe5\xbd\x93\xe5\x89\x8d\xe8\xa7\x82\xe6\x88\x98\xe4\xba\xba\xe6\x95\xb0\xef\xbc\x88\xe8\xb0\x83\xe6\x95\xb4\xe5\x90\x8e\xef\xbc\x89 
        """
        gamelog.debug('@xzh onGetWingWorldXinMoAnnalCount', annalFakeCnt)
        self.xinMoAnnalFakeCnt = annalFakeCnt
        if formula.spaceInWingWorldXinMoUniqueBoss(formula.getAnnalSrcSceneNo(self.spaceNo)) or formula.spaceInWingWorldXinMoUniqueBoss(self.spaceNo):
            gameglobal.rds.ui.cheerTopBarBoss.refreshInfo()

    def onWingWorldXinMoArenaFinalFinish(self, members, headerGbId, fromHostId, teamName):
        """
        \xe6\x93\x82\xe5\x8f\xb0\xe5\x86\xb3\xe8\xb5\x9b\xe7\xbb\x93\xe6\x9d\x9f
        :param members: members[gbId] = name 
        :param headerGbId: \xe9\x98\x9f\xe9\x95\xbfgbId
        :param fromHostId: \xe9\x98\x9f\xe4\xbc\x8d\xe6\x9d\xa5\xe6\xba\x90\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8
        :return: 
        """
        gamelog.debug('@xzh onWingWorldXinMoArenaFinalFinish', members, headerGbId, fromHostId)
        nameTxt = WWCD.data.get('rightMenuNameTxtLink', "<u><a href=\'event:menuName:%s,%s,%s,%s\'><font color=\'#FFFF66\'>%s</font></a></u>")
        headerName = ''
        teamMember = ''
        for index, gbId in enumerate(members):
            roleName = members[gbId]
            linkName = nameTxt % (roleName,
             gbId,
             1,
             fromHostId,
             roleName)
            if gbId == headerGbId:
                headerName = linkName
            else:
                teamMember = teamMember + ',' + linkName

        teamMember = headerName + teamMember
        self.showGameMsg(GMDD.data.WING_WORLD_XINMO_ARENA_FINAL_RESULT_NOTIFY, (teamMember, teamName))

    def onWingWorldXinMoUniqueBossFinish(self, members, headerGbId, fromHostId, teamName):
        gamelog.debug('@xzh onWingWorldXinMoUniqueBossFinish', members, headerGbId, fromHostId)
        nameTxt = WWCD.data.get('rightMenuNameTxtLink', "<u><a href=\'event:menuName:%s,%s,%s,%s\'><font color=\'#FFFF66\'>%s</font></a></u>")
        headerName = ''
        teamMenber = ''
        for index, gbId in enumerate(members):
            roleName = members[gbId]
            linkName = nameTxt % (roleName,
             gbId,
             1,
             fromHostId,
             roleName)
            if gbId == headerGbId:
                headerName = linkName
            else:
                teamMenber = teamMenber + ',' + linkName

        teamMenber = headerName + teamMenber
        self.showGameMsg(GMDD.data.WING_WORLD_XINMO_UNIQUE_BOSS_SUCC_NOTIFY, (teamMenber, teamName))

    def onEnterWingWorldXinMoArenaAnnal(self, roundNo, matchNo):
        """
        \xe8\xbf\x9b\xe5\x85\xa5\xe6\x93\x82\xe5\x8f\xb0\xe8\xa7\x82\xe6\x88\x98\xe5\x9c\xba\xe6\x99\xaf\xef\xbc\x8c\xe4\xb8\x8b\xe5\x8f\x91\xe8\xa7\x82\xe6\x88\x98\xe7\x9a\x84\xe8\xbd\xae\xe6\xac\xa1\xe5\x92\x8c\xe6\x93\x82\xe5\x8f\xb0\xe5\x8f\xb7
        :param roundNo: 
        :param matchNo: 
        """
        gameglobal.rds.ui.cheerTopBar.updateEnterXinMoData(roundNo, matchNo)

    def onEnterWingWorldXinMoArena(self, roundNo, matchNo):
        """
        \xe8\xbf\x9b\xe5\x85\xa5\xe6\x93\x82\xe5\x8f\xb0\xe5\x9c\xba\xe6\x99\xaf\xef\xbc\x8c\xe4\xb8\x8b\xe5\x8f\x91\xe6\x93\x82\xe5\x8f\xb0\xe7\x9a\x84\xe8\xbd\xae\xe6\xac\xa1\xe5\x92\x8c\xe6\x93\x82\xe5\x8f\xb0\xe5\x8f\xb7
        :param roundNo: 
        :param matchNo: 
        """
        gameglobal.rds.ui.cheerTopBar.updateEnterXinMoData(roundNo, matchNo)

    def onEnterWingWorldXinMoUniqueBoss(self, teamName):
        """
        \xe8\xbf\x9b\xe5\x85\xa5BOSS\xe5\x9c\xba\xe6\x99\xaf
        :param teamName: \xe9\x98\x9f\xe4\xbc\x8d\xe5\x90\x8d\xe5\xad\x97
        """
        if formula.spaceInWingWorldXinMoUniqueBoss(self.spaceNo):
            BigWorld.callback(1, Functor(gameglobal.rds.ui.cheerTopBarBoss.show, teamName))

    def onEnterWingWorldXinMoUniqueBossAnnal(self, teamName):
        """
        \xe8\xbf\x9b\xe5\x85\xa5BOSS\xe8\xa7\x82\xe6\x88\x98\xe5\x9c\xba\xe6\x99\xaf
        :param teamName: \xe9\x98\x9f\xe4\xbc\x8d\xe5\x90\x8d\xe5\xad\x97
        """
        if formula.spaceInWingWorldXinMoUniqueBoss(formula.getAnnalSrcSceneNo(self.spaceNo)):
            BigWorld.callback(1, Functor(gameglobal.rds.ui.cheerTopBarBoss.show, teamName))
