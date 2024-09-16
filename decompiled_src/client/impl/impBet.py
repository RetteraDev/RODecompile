#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impBet.o
import BigWorld
import gameglobal
import gamelog
import utils
from bet import BetClientVal, BetVal
import bet
from guis import uiConst
from gamestrings import gameStrings

class ImpBet(object):

    def syncMyBetData(self, dtos):
        gamelog.debug('dxk@syncMyBetData')
        self.myBetDict = {}
        for dto in dtos:
            myBetInfo = BetClientVal()
            myBetInfo.fromDTO(dto)
            self.myBetDict[myBetInfo.bId] = myBetInfo

        gameglobal.rds.ui.generalBet.refreshInfo()

    def afterDoBet(self, dto):
        gamelog.debug('dxk@afterDoBet')
        myBetInfo = BetClientVal()
        myBetInfo.fromDTO(dto)
        self.myBetDict[myBetInfo.bId] = myBetInfo
        self.addTempBetFame(myBetInfo.bId, myBetInfo.choice, myBetInfo.fame)
        gameglobal.rds.ui.generalBet.refreshInfo()

    def addTempBetFame(self, bId, option, num):
        for betInfo in self.betDatas:
            if betInfo.bId == bId:
                if option >= 0 and option < len(betInfo.reward):
                    betInfo.reward[option] += num
                    return

    def getBetState(self, bId):
        if bId in self.myBetDict:
            myBetIcno = self.myBetDict[bId]
            for betInfo in self.betDatas:
                if betInfo.bId == bId:
                    if betInfo.getBetClientAnswer() == bet.DEFAULT_ANS:
                        return bet.BET_STATE_BETED
                    if betInfo.getBetClientAnswer() == myBetIcno.choice:
                        return bet.BET_STATE_SUCC

            return bet.BET_STATE_FAILED
        else:
            return bet.BET_STATE_NONE

    def onGetBetInfo(self, betDtos):
        gamelog.debug('dxk@onGetBetInfo')
        needRefresh = False
        if not getattr(self, 'betDatas', []) and betDtos:
            self.isBetDataUpdate = True
            needRefresh = True
        if getattr(self, 'betDatas', []) and not betDtos:
            needRefresh = True
        oldBetDatas = self.betDatas
        self.betDatas = []
        for betDto in betDtos:
            betInfo = BetVal()
            betInfo.fromDTO(betDto)
            self.betDatas.append(betInfo)

        self.handleBetInfoChanged(oldBetDatas, self.betDatas)
        if not self.betDatas:
            self.removeBetPushMsg()
        if not gameglobal.rds.configData.get('enableBet', False):
            return
        gameglobal.rds.ui.generalBet.betTickFunc()
        if needRefresh:
            self.addBetPushMsg()
            gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
        if self.betDatas:
            self.addBetPushMsgCallBack()

    def handleBetInfoChanged(self, oldBetDatas, newBetDatas):
        lastCheckTime = getattr(self, 'lastCheckBetTime', 0)
        self.lastCheckBetTime = utils.getNow()

    def notifyBetClient(self, nType):
        gamelog.debug('dxk@notifyBetClient', nType)
        if nType == bet.NOTIFY_TYPE_BET_START:
            gameglobal.rds.ui.generalBet.popIconMessage(gameStrings.NEW_BET_MSG)
        elif nType == bet.NOTIFY_TYPE_BET_CALC:
            gameglobal.rds.ui.generalBet.popIconMessage(gameStrings.BET_HIT_MSG)
        if nType == bet.NOTIFY_TYPE_BET_CLOSE:
            self.myBetDict = {}
            self.betDatas = []
            gameglobal.rds.ui.generalBet.stopTickFunc()
            gameglobal.rds.ui.generalBet.hide()
            gameglobal.rds.ui.generalBetPay.hide()
            gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
            self.removeBetPushMsg()
        else:
            self.base.queryAllBet()
            self.isBetDataUpdate = True
            gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()

    def addBetPushMsgCallBack(self):
        nextRefreshTime = -1
        now = utils.getNow()
        for betData in self.betDatas:
            if betData.state != bet.BET_STATE_WRONG:
                if betData.tStart and betData.tStart > now:
                    if nextRefreshTime < 0:
                        nextRefreshTime = betData.tStart - now
                    else:
                        nextRefreshTime = min(nextRefreshTime, betData.tStart - now)

        if nextRefreshTime > 0:
            if hasattr(self, 'betCallBack') and self.betCallBack:
                BigWorld.cancelCallback(self.betCallBack)
            self.betCallBack = BigWorld.callback(nextRefreshTime, self.addBetPushMsg)

    def addBetPushMsg(self):
        if hasattr(self, 'betCallBack') and self.betCallBack:
            BigWorld.cancelCallback(self.betCallBack)
        self.betCallBack = None
        betDatas = getattr(self, 'betDatas', [])
        for betData in betDatas:
            if betData.state != bet.BET_STATE_WRONG:
                if betData.isInShowTime():
                    if uiConst.MESSAGE_TYPE_BET_START not in gameglobal.rds.ui.pushMessage.msgs:
                        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_BET_START)
                        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_BET_START, {'click': self.onClickBetPushMsg})
                        return

    def onClickBetPushMsg(self):
        self.removeBetPushMsg()
        if not gameglobal.rds.configData.get('enableBet', False):
            return
        gameglobal.rds.ui.generalBet.show()

    def removeBetPushMsg(self):
        if uiConst.MESSAGE_TYPE_BET_START in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_BET_START)
