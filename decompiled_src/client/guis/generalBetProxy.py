#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/generalBetProxy.o
import BigWorld
import time
import copy
import gameglobal
import uiConst
import gametypes
from guis.asObject import ASObject
from guis.asObject import Tweener
from guis import events
from uiProxy import UIProxy
import bet
import utils
from gamestrings import gameStrings
from data import sys_config_data as SCD
from data import formula_client_data as FCD
from cdata import game_msg_def_data as GMDD
from helpers import tickManager
from callbackHelper import Functor
import const
GENERAL_TAB_BET = 0
GENERAL_TAB_MY_BET = 1
TAB_NUM = 2
BET_ITEM_HEIGHT = 97
EXPAND_ITEM_HEIGHT = 101
MY_BET_ITEM_HEIGHT = 97
ANSWER_MAX_NUM = 4
DEFALUT_EXPANEDAREA_X = 7
ANSWER_WIDTH = 161
QUERY_INTERVAL = 4

class GeneralBetProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GeneralBetProxy, self).__init__(uiAdapter)
        self.widget = None
        self.expandBId = 0
        self.currExpandItem = None
        self.currentTab = GENERAL_TAB_BET
        self.betItemList = []
        self.hideEndBet = False
        self.callback = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GENERAL_BET, self.hide)

    def reset(self):
        self.expandBId = 0
        self.currExpandItem = None
        self.callback = None
        self.currentTab = GENERAL_TAB_BET

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GENERAL_BET:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GENERAL_BET)
        if self.callback:
            BigWorld.cancelCallback(self.callback)
        self.reset()

    def show(self, betId = 0):
        self.expandBId = betId
        gameglobal.rds.ui.rewardGiftActivityIcons.removeMessage('betIcon')
        p = BigWorld.player()
        if self.hasNewInfo():
            setattr(p, 'isBetDataUpdate', False)
            gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_GENERAL_BET)
        else:
            self.refreshInfo()
        self.queryServerInfo()

    def popIconMessage(self, msg):
        if self.widget:
            return
        gameglobal.rds.ui.rewardGiftActivityIcons.popMessage('betIcon', msg, 20)

    def queryServerInfo(self):
        if gameglobal.rds.GameState == gametypes.GS_PLAYGAME:
            p = BigWorld.player()
            p.base.queryAllBet()

    def initUI(self):
        self.currExpandItem = None
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.betMc.hideCheck.removeEventListener(events.EVENT_SELECT, self.onHideCheckSelected)
        self.widget.betMc.hideCheck.selected = self.hideEndBet
        self.widget.betMc.hideCheck.addEventListener(events.EVENT_SELECT, self.onHideCheckSelected)
        self.widget.helpIcon.helpKey = 436
        self.widget.shopBtn.visible = False
        self.widget.shopBtn.addEventListener(events.BUTTON_CLICK, self.onShopBtnClick)
        self.widget.rankBtn.addEventListener(events.BUTTON_CLICK, self.onRankBtnClick)
        for i in xrange(TAB_NUM):
            tabMc = self.widget.getChildByName('tabBtn%d' % i)
            tabMc.addEventListener(events.BUTTON_CLICK, self.onTabBtnClick)

        self.betTickFunc(False, False)

    def onShopBtnClick(self, *args):
        shopId = SCD.data.get('betRewardShopId', 0)
        if shopId:
            gameglobal.rds.ui.compositeShop.closeShop()
            p = BigWorld.player()
            p.base.openPrivateShop(0, shopId)

    def onRankBtnClick(self, *args):
        gameglobal.rds.ui.rankCommon.showRankCommon(gametypes.TOP_TYPE_GENERAL_BET)

    def refreshMyBetMc(self):
        myBetMc = self.widget.myBetMc
        myBetMc.lvText.text = ''
        p = BigWorld.player()
        betDatas = getattr(p, 'betDatas', [])
        myBetDict = getattr(p, 'myBetDict', {})
        totalCash = 0
        for i, betData in enumerate(betDatas):
            if betData.bId in myBetDict:
                myBetInfo = myBetDict[betData.bId]
                totalCash += self.calcBonusCash(betData, myBetInfo)

        myBetMc.getNum.text = totalCash
        myBetMc.icon.bonusType = 'yunChui'
        self.refreshMyBetList()

    def refreshMyBetList(self):
        if not self.widget:
            return
        myBetMc = self.widget.myBetMc
        betList = myBetMc.betList
        self.removeAllChild(betList.canvas)
        p = BigWorld.player()
        betDatas = getattr(p, 'betDatas', [])
        myBetDict = getattr(p, 'myBetDict', {})
        currY = 0
        for i, betData in enumerate(betDatas):
            if betData.bId in myBetDict:
                myBetInfo = myBetDict[betData.bId]
                betItemMc = self.widget.getInstByClsName('GeneralBet_myBetItem')
                betList.canvas.addChild(betItemMc)
                betItemMc.y = currY
                currY += MY_BET_ITEM_HEIGHT
                self.setMyBetInfo(betItemMc, betData, myBetInfo)

        betList.refreshHeight()
        if not myBetDict:
            myBetMc.noText.visible = True
        else:
            myBetMc.noText.visible = False

    def setMyBetInfo(self, betMc, betData, myBetData):
        p = BigWorld.player()
        betInfo = betMc.betInfo
        if betData.state == bet.BET_STATE_WRONG:
            betMc.betState.visible = True
            betMc.betState.gotoAndStop('stateWrong')
        else:
            betState = p.getBetState(betData.bId)
            if betState:
                betMc.betState.visible = True
                betMc.betState.gotoAndStop('state%d' % betState)
            else:
                betMc.betState.visible = False
        if betData.state == bet.BET_STATE_DDL:
            betInfo.gotoAndStop('end')
        elif betData.state == bet.BET_STATE_CALC:
            betInfo.gotoAndStop('finish')
            betInfo.icon1.bonusType = 'yunChui'
            betInfo.getNum.text = self.calcBonusCash(betData, myBetData)
        else:
            betInfo.gotoAndStop('start')
            betInfo.overTime.text = self.getBetOverTimeText(betData.tDDL)
        betInfo.icon.bonusType = 'yunChui'
        betInfo.answer.htmlText = betData.option[myBetData.choice]
        if utils.isCustomeBet(betData.bId):
            descInfo = betData.desc.split(bet.BET_SPLIT)
            if len(descInfo) >= 2:
                title, desc = descInfo[0], descInfo[1]
            else:
                title = gameStrings.DEFAULT_BET_TITLE
                desc = descInfo
        else:
            title, desc = ('', '')
        betInfo.quest.htmlText = desc
        betInfo.num.text = myBetData.fame

    def calcBonusCash(self, betData, myBetInfo):
        fId = SCD.data.get('betCalcBonusClientFormulaId', 0)
        f = FCD.data.get(fId, {}).get('formula', None)
        total = sum(betData.reward)
        bonus = 0
        if betData.reward[myBetInfo.choice]:
            if myBetInfo.choice == betData.ans:
                if f:
                    bonus = f({'rWrong': float(total - betData.reward[myBetInfo.choice]),
                     'rRight': float(betData.reward[myBetInfo.choice]),
                     'rSelf': float(myBetInfo.fame)})
        return int(bonus)

    def isOpen(self):
        p = BigWorld.player()
        betDatas = getattr(p, 'betDatas', [])
        for betData in betDatas:
            if not betData.isInShowTime():
                continue
            if self.hideEndBet and betData.state in (bet.BET_STATE_CALC, bet.BET_STATE_WRONG):
                continue
            return True

        return False

    def hasNewInfo(self):
        if not self.isOpen():
            return False
        p = BigWorld.player()
        if getattr(p, 'isBetDataUpdate', False):
            return True
        return False

    def refreshInfo(self):
        if not self.widget:
            return
        for i in xrange(TAB_NUM):
            tabMc = self.widget.getChildByName('tabBtn%d' % i)
            tabMc.selected = i == self.currentTab

        self.widget.betMc.visible = self.currentTab == GENERAL_TAB_BET
        self.widget.myBetMc.visible = self.currentTab == GENERAL_TAB_MY_BET
        if self.currentTab == GENERAL_TAB_BET:
            self.refreshBetMc()
        else:
            self.refreshMyBetMc()
        self.refreshCash()

    def stopTickFunc(self):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
            self.callback = None

    def betTickFunc(self, queryServerInfo = False, refreshWnd = True):
        if not gameglobal.rds.configData.get('enableBet', False):
            return
        else:
            nextRefreshTime = self.getNextRefreshTime()
            if self.callback:
                BigWorld.cancelCallback(self.callback)
                self.callback = None
            if refreshWnd:
                self.refreshInfo()
            if queryServerInfo:
                self.queryServerInfo()
            if nextRefreshTime < QUERY_INTERVAL:
                nextRefreshTime = QUERY_INTERVAL
            self.callback = BigWorld.callback(nextRefreshTime, Functor(self.betTickFunc, True))
            return

    def getNextRefreshTime(self):
        p = BigWorld.player()
        now = utils.getNow()
        nextTime = now + 30
        betDatas = getattr(p, 'betDatas', [])
        for i, betData in enumerate(betDatas):
            if betData.tStart + QUERY_INTERVAL > now:
                if nextTime > betData.tStart + QUERY_INTERVAL:
                    nextTime = betData.tStart + QUERY_INTERVAL
            if betData.tDDL > now:
                if nextTime > betData.tDDL + QUERY_INTERVAL:
                    nextTime = betData.tDDL + QUERY_INTERVAL
            elif betData.tCalc > now:
                if nextTime > betData.tCalc + QUERY_INTERVAL:
                    nextTime = betData.tCalc + QUERY_INTERVAL

        return max(0, nextTime - now)

    def refreshBetMc(self):
        self.refreshBetList()

    def refreshCash(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.widget.num.text = p.getFame(const.YUN_CHUI_JI_FEN_FAME_ID)
        self.widget.icon.bonusType = 'yunChui'

    def betDataSortFunc(self, data1, data2):
        if data1.state == data2.state:
            return cmp(data1.tDDL, data2.tDDL)
        if data1.state == bet.BET_STATE_START:
            return -1
        if data2.state == bet.BET_STATE_START:
            return 1
        return cmp(data1.tDDL, data2.tDDL)

    def refreshBetList(self):
        if not self.widget:
            return
        p = BigWorld.player()
        betMc = self.widget.betMc
        betDatas = copy.copy(getattr(p, 'betDatas', []))
        betDatas.sort(cmp=self.betDataSortFunc)
        betList = betMc.betList
        scrollTo = -1
        self.removeAllChild(betList.canvas)
        self.betItemList = []
        currentY = 0
        for i, betData in enumerate(betDatas):
            if not betData.isInShowTime():
                continue
            if self.hideEndBet and betData.state in (bet.BET_STATE_CALC, bet.BET_STATE_WRONG):
                continue
            betItemMc = self.widget.getInstByClsName('GeneralBet_betItem')
            betList.canvas.addChild(betItemMc)
            betItemMc.y = currentY
            if betData.state == bet.BET_STATE_WRONG:
                betItemMc.betState.gotoAndStop('stateWrong')
            else:
                betState = p.getBetState(betData.bId)
                if betState:
                    betItemMc.betState.visible = True
                    betItemMc.betState.gotoAndStop('state%d' % betState)
                else:
                    betItemMc.betState.visible = False
            betItemMc.bId = betData.bId
            if self.expandBId == betData.bId:
                betItemMc.expandArea.y = EXPAND_ITEM_HEIGHT
                scrollTo = currentY
                currentY += EXPAND_ITEM_HEIGHT
                self.expandItem(betItemMc, True)
            else:
                betItemMc.expandArea.y = 0
            currentY += BET_ITEM_HEIGHT
            self.betItemList.append(betItemMc)
            self.setBetInfo(betItemMc, betData)
            self.setBetAnswers(betItemMc, betData)
            betItemMc.betInfo.addEventListener(events.MOUSE_CLICK, self.onExpandItemClick)

        betList.refreshHeight()
        if not betDatas:
            betMc.noText.visible = True
        else:
            betMc.noText.visible = False
        if scrollTo >= 0:
            betList.scrollTo(scrollTo)

    def setBetAnswers(self, betMc, betData):
        expandArea = betMc.expandArea
        p = BigWorld.player()
        total = sum(betData.reward)
        myBetInfo = p.myBetDict.get(betData.bId, None)
        for i in xrange(ANSWER_MAX_NUM):
            answerMc = expandArea.betItems.getChildByName('item%d' % i)
            if i < len(betData.option):
                answerMc.visible = True
                option = betData.option[i]
                fId = SCD.data.get('betCalcRatioFormulaId', 0)
                f = FCD.data.get(fId, {}).get('formula', None)
                ratio = 1
                if not betData.reward[i]:
                    ratioText = gameStrings.EMPTY_BET_RATIO
                else:
                    if f:
                        ratio = f({'Other': float(total - betData.reward[i]),
                         'Self': float(betData.reward[i])})
                    ratioText = gameStrings.BET_RATIO % ratio
                reward = betData.reward[i]
                answerMc.icon.bonusType = 'yunChui'
                answerMc.labels = [option,
                 ratioText,
                 gameStrings.BET_IN,
                 reward]
                answerMc.bId = betData.bId
                answerMc.index = i
                answerMc.option = option
                if betData.state == bet.BET_STATE_START:
                    answerMc.enabled = True
                    answerMc.addEventListener(events.BUTTON_CLICK, self.onAnswerBtnClick)
                else:
                    answerMc.enabled = False
                    answerMc.removeEventListener(events.BUTTON_CLICK, self.onAnswerBtnClick)
                if myBetInfo:
                    if myBetInfo.choice == i:
                        answerMc.enabled = True
                    else:
                        answerMc.enabled = False
            else:
                answerMc.visible = False

        expandArea.betItems.x = DEFALUT_EXPANEDAREA_X + (ANSWER_MAX_NUM - len(betData.option)) * ANSWER_WIDTH / 2

    def onAnswerBtnClick(self, *args):
        e = ASObject(args[3][0])
        index = e.currentTarget.index
        bId = e.currentTarget.bId
        option = e.currentTarget.option
        p = BigWorld.player()
        betDatas = getattr(p, 'betDatas', [])
        if bId in p.myBetDict:
            p.showGameMsg(GMDD.data.COMMON_MSG, (gameStrings.AREADY_BETED,))
            return
        for betData in betDatas:
            if betData.bId == bId:
                if betData.state == bet.BET_STATE_START:
                    gameglobal.rds.ui.generalBetPay.show(bId, index, option)
                else:
                    p.showGameMsg(GMDD.data.COMMON_MSG, (gameStrings.NOT_IN_BET_TIME,))

    def setBetInfo(self, betMc, betData):
        betInfo = betMc.betInfo
        if betData.state == bet.BET_STATE_DDL:
            betInfo.gotoAndStop('end')
        elif betData.state == bet.BET_STATE_CALC:
            betInfo.gotoAndStop('finish')
        else:
            betInfo.gotoAndStop('start')
            betInfo.overTime.text = self.getBetOverTimeText(betData.tDDL)
        if utils.isCustomeBet(betData.bId):
            descInfo = betData.desc.split(bet.BET_SPLIT)
            if len(descInfo) >= 2:
                title, desc = descInfo[0], descInfo[1]
            else:
                title = gameStrings.DEFAULT_BET_TITLE
                desc = descInfo
        else:
            title, desc = ('', '')
        betInfo.mainTitle.htmlText = title
        betInfo.question.htmlText = desc

    def getBetOverTimeText(self, tDDL):
        t = utils.localtimeEx(tDDL)
        timeTxt = gameStrings.BET_TIME_TEXT % (t.tm_year,
         t.tm_mon,
         t.tm_mday,
         t.tm_hour,
         t.tm_min)
        return timeTxt

    def onExpandItemClick(self, *args):
        e = ASObject(args[3][0])
        isExpand = e.currentTarget.parent.expand
        self.expandItem(e.currentTarget.parent, isExpand)

    def expandItem(self, expandBetItem, unExpand = False):
        if self.currExpandItem:
            self.currExpandItem.expand = False
        self.currExpandItem = expandBetItem
        self.expandBId = expandBetItem.bId
        self.currExpandItem.expand = not unExpand
        self.doPosAnim()

    def doPosAnim(self):
        calcY = 0
        for i, betItem in enumerate(self.betItemList):
            if betItem.y != calcY:
                Tweener.addTween(betItem, {'y': calcY,
                 'time': 0.08,
                 'transition': 'easeinsine'})
            calcY += BET_ITEM_HEIGHT
            expandY = 0
            if betItem.expand:
                calcY += EXPAND_ITEM_HEIGHT
                expandY = EXPAND_ITEM_HEIGHT
            if betItem.expandArea.y != expandY:
                Tweener.addTween(betItem.expandArea, {'y': expandY,
                 'time': 0.08,
                 'transition': 'easeinsine'})

    def onTabBtnClick(self, *args):
        e = ASObject(args[3][0])
        tabName = e.currentTarget.name
        tabIdx = int(tabName[-1])
        if self.currentTab != tabIdx:
            self.currentTab = tabIdx
            self.refreshInfo()
        self.queryServerInfo()

    def removeAllChild(self, canvasMc):
        while canvasMc.numChildren > 0:
            canvasMc.removeChildAt(0)

    def onHideCheckSelected(self, *args):
        e = ASObject(args[3][0])
        self.hideEndBet = e.currentTarget.selected
        self.refreshBetList()

    def generateTestData(self):
        self.betDatas = []
        for i in xrange(5):
            self.betDatas.append(bet.BetVal())

        self.refreshInfo()
