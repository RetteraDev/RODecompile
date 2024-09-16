#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impFightForLove.o
import BigWorld
import gameglobal
import gametypes
import const
import gamelog
from guis import uiConst
from guis import uiUtils
from gamestrings import gameStrings
from callbackHelper import Functor
from data import fight_for_love_config_data as FFLCD
from cdata import game_msg_def_data as GMDD

class ImpFightForLove(object):

    def onGetFFLTotalInfo(self, info):
        gamelog.debug('@zq onGetFFLTotalInfo', info)
        gameglobal.rds.ui.fightForLoveLines.refreshListData(info)

    def onCreateFightForLoveSucc(self):
        gamelog.debug('@zq onCreateFightForLoveSucc')
        gameglobal.rds.ui.fightForLoveApply.hide()

    def onApplyFightForLoveSucc(self):
        gamelog.debug('@zq onApplyFightForLoveSucc')
        self.cell.enterFightForLove()

    def onQueryAcceptFightForLoveWinner(self, winnerName):
        gamelog.debug('@zq onQueryAcceptFightForLoveWinner', winnerName)
        msg = FFLCD.data.get('confirmNormalWinnerMsg', '')
        pkConfirmTime = FFLCD.data.get('pkConfirmTime', '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.cell.cancelFightForLoveWinner), yesBtnText=gameStrings.FIGHT_FOR_LOVE_CONFIRM_WINNER, noCallback=Functor(self.cell.confirmFightForLoveWinner), noBtnText=gameStrings.FIGHT_FOR_LOVE_CANCEL_WINNER, repeat=pkConfirmTime, countDownFunctor=Functor(self.cell.confirmFightForLoveWinner))

    def onQueryAcceptFightForLovePKResult(self, winnerName):
        gamelog.debug('@zq onQueryAcceptFightForLovePKResult', winnerName)
        msg = ''
        if self.isFightForLoveCreator():
            msg = FFLCD.data.get('createrConfirmPKWinnerMsg', '')
        else:
            msg = FFLCD.data.get('fighterConfirmPKWinnerMsg', '')
        pkConfirmTime = FFLCD.data.get('pkConfirmTime', '')

        def confirm():
            if self.isFightForLoveCreator():
                self.cell.confirmFightForLovePKResult()

        mId = gameglobal.rds.ui.messageBox.showMsgBox(msg, callback=confirm, needDissMissCallBack=True)
        self.fightForLoveMsgIds['pkConfirm'] = mId

    def onNotifyFightForLoveEnter(self):
        gamelog.debug('@zq onNotifyFightForLoveEnter')

    def bHideFightForLoveFighterName(self, target = None):
        if self.isPlayingFightForLoveScenario():
            return False
        if target:
            if target.IsAvatar:
                return self.inFightForLoveFb() and not target.isFightForLoveCreator()
            return False
        return self.inFightForLoveFb() and not self.isFightForLoveCreator()

    def isFightForLoveCreator(self):
        return getattr(self, 'fightForLoveCreaterRole', None) == const.FIGHT_FOR_LOVE_CREATER

    def isFightForLoveRunning(self):
        return getattr(self, 'fightForLovePhase', None) == gametypes.FIGHT_FOR_LOVE_PHASE_RUNNING

    def inFightForLoveFb(self):
        p = BigWorld.player()
        if p.__class__.__name__ == 'PlayerAvatar':
            return p.inFubenType(const.FB_TYPE_FIGHT_FOR_LOVE)
        return False

    def isPlayingFightForLoveScenario(self):
        if self.inFightForLoveFb() and gameglobal.SCENARIO_PLAYING:
            return True
        return False

    def isFightForLoveScenarioActor(self):
        p = BigWorld.player()
        if self.gbId in p.fightForLoveResult.values():
            return True
        return False

    def getFightForLoveNameInfo(self):
        name = FFLCD.data.get('nameInFuben', '')
        title = FFLCD.data.get('titleInFuben', '')
        info = {'name': name,
         'title': title}
        return info

    def playFightForLoveScenario(self, scenarioName, createrGbId, winnerGbId):
        gamelog.debug('@zq playFightForLoveScenario', scenarioName, createrGbId, winnerGbId)
        gameglobal.rds.ui.fightForLoveRankList.removeFFLScore()
        p = BigWorld.player()
        if self == p:
            self.fightForLoveResult = {'createrGbId': createrGbId,
             'winnerGbId': winnerGbId}
            BigWorld.callback(1, Functor(self.fightForLoveScenarioPlay, createrGbId, winnerGbId))

    def confirmEnterFightForLoveScene(self):
        msg = FFLCD.data.get('creatorEnterMsg', '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.cell.enterFightForLove), yesBtnText=gameStrings.COMMON_CONFIRM, noBtnText=gameStrings.COMMON_CANCEL)

    def refreshFFLCreaterEnterPushMessage(self):
        BigWorld.callback(0.2, self._refreshFFLCreaterEnterPushMessage)

    def _refreshFFLCreaterEnterPushMessage(self):
        p = BigWorld.player()
        if self == p:
            if self.fightForLoveCreaterRole == const.FIGHT_FOR_LOVE_CREATER:
                if not self.inFightForLoveFb():
                    self.addEnterFightForLoveScenePushMessage()
                else:
                    self.removeEnterFightForLoveScenePushMessage()
            else:
                self.removeEnterFightForLoveScenePushMessage()

    def addEnterFightForLoveScenePushMessage(self):
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_FIGHT_FOR_LOVE_ENTER_SCENE, {'click': Functor(self.confirmEnterFightForLoveScene)})
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_FIGHT_FOR_LOVE_ENTER_SCENE)

    def removeEnterFightForLoveScenePushMessage(self):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_FIGHT_FOR_LOVE_ENTER_SCENE)

    def onSyncFightForLovePhase(self, phase):
        gamelog.debug('@zq onSyncFightForLovePhase', phase)
        self.fightForLovePhase = phase
        gameglobal.rds.ui.fightForLoveRankList.setPhase(phase)
        gameglobal.rds.ui.fightForLoveRankList.refreshInfo()
        p = BigWorld.player()
        if self == p:
            self.unlockTarget()
        if self.isFightForLoveCreator():
            if self.isFightForLoveRunning():
                self.topLogo.hideTitleEffect(True)
            else:
                self.topLogo.hideTitleEffect(False)

    def onSyncFightForLoveScore(self, scoreInfo):
        gamelog.debug('yedawang### onSyncFightForLoveScore', scoreInfo)
        gameglobal.rds.ui.fightForLoveRankList.setScoreInfo(scoreInfo)
        for gbId, score in scoreInfo:
            for e in BigWorld.entities.values():
                if not getattr(e, 'IsAvatar', False):
                    continue
                if hasattr(e, 'gbId') and e.gbId == gbId:
                    e.topLogo.setFFLScore(score)

    def onSyncFightForLoveMemberInfo(self, createrGbId, createrName, memberInfo):
        gamelog.debug('yedawang### onSyncFightForLoveMemberInfo', createrGbId, createrName, memberInfo)
        gameglobal.rds.ui.fightForLoveRankList.setMemberInfo(createrGbId, createrName, memberInfo)
        if self.isFightForLoveRunning():
            for gbId, _, _, _, score in memberInfo:
                for e in BigWorld.entities.values():
                    if not getattr(e, 'IsAvatar', False):
                        continue
                    if hasattr(e, 'gbId') and e.gbId == gbId:
                        e.topLogo.setFFLScore(score)

            gameglobal.rds.ui.fightForLoveRankList.refreshInfo()

    def seekFightForLoveNpc(self):
        seekId = FFLCD.data.get('npcSeekId', 0)
        msg = FFLCD.data.get('findNpcPosConfirmMsg', 0)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(uiUtils.findPosById, seekId), yesBtnText=gameStrings.COMMON_CONFIRM, noBtnText=gameStrings.COMMON_CANCEL)

    def onSyncFightForLovePhaseWithNUID(self, activityNUID, phase):
        self.cell.queryFightForLoveTotalInfo()

    def onFightForLoveLockInput(self):
        if hasattr(self, 'ap') and hasattr(self.ap, 'stopMove'):
            self.ap.stopMove()
        self.lockKey(gameglobal.KEY_FIGHT_FOR_LOVE)
