#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fishingGameProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import const
import utils
import formula
import ui
from uiProxy import UIProxy
from guis import uiUtils
from ui import gbk2unicode
from crontab import CronTab
from item import Item
from data import fishing_top_reward_data as FTRD
from data import item_data as ID
from data import activity_basic_data as ABD
TYPE_NORMAL = -1
TYPE_FISHING_GAME = 0
TYPE_FISHING_EXERCISE = 1
TYPE_FISHING_GAME_ING = 2
FISHING_GAME_ID = 10004

class FishingGameProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FishingGameProxy, self).__init__(uiAdapter)
        self.modelMap = {'showRank': self.onShowRank,
         'getTime': self.onGetTime,
         'getRankInfo': self.onGetRankInfo,
         'refreshRank': self.onRefreshRank,
         'closeRank': self.onCloseRank,
         'getMyRank': self.onGetMyRank,
         'openGuide': self.onOpenGuide,
         'isInLine': self.onIsInLine,
         'enterLine': self.onEnterLine,
         'getGameType': self.onGetGameType,
         'gotoGuildRank': self.onGotoGuildRank}
        self.noticeMediator = None
        self.rankMediator = None
        self.buttonMediator = None
        self.fishingActs = FTRD.data.keys()
        self.ver = 0
        self.info = None
        self.startTime = 0
        self.callBackHandler = None
        self.gameFishes = []
        self.myVal = None
        self.callback = None
        self.buttonCallback = None
        self.showType = -1

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FISHINGGAME_RANK:
            self.rankMediator = mediator
        elif widgetId == uiConst.WIDGET_FISHINGGAME_NOTICE:
            self.noticeMediator = mediator
            self.onGetRankInfo(None)
        elif widgetId == uiConst.WIDGET_FISHING_ENTER:
            self.buttonMediator = mediator

    def showRank(self, type = -1):
        """
        for questId in self.fishingQuests:
            if self.checkInGameById(questId):
                self.gameFishes = FTRD.data.get(questId, {}).get('gameFishIds', [])
                break
        """
        if len(self.fishingActs) > 0:
            actID = self.fishingActs[0]
            self.gameFishes = FTRD.data.get(actID, {}).get('gameFishIds', [])
        self.showType = type
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FISHINGGAME_RANK)

    def showNotice(self):
        if BigWorld.player()._isSoul():
            return
        else:
            for actId in self.fishingActs:
                if self.checkInGameById(actId):
                    self.gameFishes = FTRD.data.get(actId, {}).get('gameFishIds', [])
                    break

            if self.rankMediator:
                self.closeRank()
            if self.buttonMediator:
                self.closeButton()
            if self.noticeMediator:
                self.noticeMediator.Invoke('setContent', self.onIsInLine(None))
            else:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FISHINGGAME_NOTICE)
            return

    def showButton(self):
        if not self.buttonMediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FISHING_ENTER)

    def closeRank(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FISHINGGAME_RANK)
        self.rankMediator = None
        self.showType = -1

    def closeNotice(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FISHINGGAME_NOTICE)
        self.noticeMediator = None
        if self.callback:
            BigWorld.cancelCallback(self.callback)

    def closeButton(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FISHING_ENTER)
        self.buttonMediator = None
        if self.buttonCallback:
            BigWorld.cancelCallback(self.buttonCallback)

    def clearWidget(self):
        self.closeRank()
        self.closeNotice()
        self.closeButton()

    def _genRankInfo(self, info):
        p = BigWorld.player()
        ret = {'rank': [],
         'option': {}}
        myVal = None
        for idx, item in enumerate(info):
            fishData = []
            for i, fish in enumerate(self.gameFishes):
                if i == len(self.gameFishes) - 2:
                    continue
                if i != len(self.gameFishes) - 1:
                    fishNum = item[3].get(fish, 0)
                else:
                    fishNum = item[3].get(fish, 0) + item[3].get(self.gameFishes[i - 1], 0)
                iconId = ID.data.get(fish, {}).get('icon', fish)
                fishData.append(['item/icon/%d.dds' % iconId, fishNum])

            ret['rank'].append([idx + 1,
             gbk2unicode(item[1]),
             int(item[3].get('score', 0)),
             item[0] == p.gbId,
             item[4],
             fishData])
            if item[0] == p.gbId:
                myVal = [idx + 1, item]

        if myVal:
            myRank = myVal[0]
            ret['option']['rank'] = myRank
            if myRank > 10 and myRank <= 100:
                ret['option']['info'] = []
                for idx in xrange(myRank - 1, myRank + 2):
                    if idx <= min(len(info), 100):
                        fishData = []
                        for i, fish in enumerate(self.gameFishes):
                            if i == len(self.gameFishes) - 2:
                                continue
                            if i != len(self.gameFishes) - 1:
                                fishNum = info[idx - 1][3].get(fish, 0)
                            else:
                                fishNum = info[idx - 1][3].get(fish, 0) + info[idx - 1][3].get(self.gameFishes[i - 1], 0)
                            iconId = ID.data.get(fish, {}).get('icon', fish)
                            fishData.append(['item/icon/%d.dds' % iconId, fishNum])

                        ret['option']['info'].append([idx,
                         gbk2unicode(info[idx - 1][1]),
                         int(info[idx - 1][3].get('score', 0)),
                         info[idx - 1][0] == p.gbId,
                         info[idx - 1][4],
                         fishData])
                    else:
                        ret['option']['info'].append([-1,
                         '',
                         '',
                         False,
                         0,
                         [['item/icon/notFound.dds', 0]] * 3])

            elif myRank > 100:
                ret['option']['score'] = int(myVal[1][3].get('score', 0))
            self.setMyRank(myVal[1])
        else:
            ret['option']['rank'] = 0
            self.setMyRank([0,
             0,
             0,
             {}])
        ret['showType'] = self.getShowType()
        return ret

    def setRank(self, proxyId, ver, info):
        self.ver = ver
        self.info = info
        ret = self._genRankInfo(info)
        if self.rankMediator:
            self.rankMediator.Invoke('setRank', uiUtils.dict2GfxDict(ret))

    def queryFishingScore(self, showType = -1):
        p = BigWorld.player()
        if showType == TYPE_NORMAL:
            for actID in self.fishingActs:
                fData = ABD.data.get(actID, {})
                if not fData:
                    continue
                p.cell.refreshFishingScore(self.ver, actID)
                return

        elif showType == TYPE_FISHING_GAME:
            p.cell.refreshFishingScore(self.ver, FISHING_GAME_ID)

    def getLastTime(self, actID):
        startTime = ABD.data.get(actID, {}).get('startTimes', ('0 19 * * 3,6',))[0]
        endTime = ABD.data.get(actID, {}).get('endTimes', ('20 19 * * 3,6',))[0]
        sEntry = CronTab(startTime)
        eEntry = CronTab(endTime)
        now = utils.getNow()
        return eEntry.next(now + sEntry.next(now))

    def checkNeedLoadByNotice(self):
        p = BigWorld.player()
        if p and hasattr(p, 'fishingActivityData'):
            for actID in p.fishingActivityData:
                self.checkNeedLoadByActivityID(actID)

    def checkNeedLoadByActivityID(self, actID):
        fData = FTRD.data.get(actID, {})
        p = BigWorld.player()
        if not fData:
            return
        else:
            if actID in p.fishingActivityData:
                actData = ABD.data.get(actID)
                now = utils.getNow()
                inActTime = False
                nextStartDelay = 0
                for i in range(len(actData.get('startTimes', ()))):
                    startCT = CronTab(actData['startTimes'][i])
                    endCT = CronTab(actData['endTimes'][i])
                    nextStart = startCT.next(now)
                    nextEnd = endCT.next(now)
                    if nextStart > nextEnd:
                        self.startTime = now + startCT.previous(now + 60) + 60
                        gameglobal.rds.ui.fishingGame.showNotice()
                        inActTime = True
                        break
                    if not nextStartDelay or nextStart < nextStartDelay:
                        nextStartDelay = nextStart

                if not inActTime:
                    self.startTime = now + nextStartDelay
                    if self.callback:
                        BigWorld.cancelCallback(self.callback)
                        self.callback = None
                    self.callback = BigWorld.callback(nextStartDelay, gameglobal.rds.ui.fishingGame.showNotice)
            return

    def setMyRank(self, info):
        ret = {}
        ret['score'] = int(info[3].get('score', 0))
        ret['icon'] = []
        for i, fish in enumerate(self.gameFishes):
            if i == len(self.gameFishes) - 2:
                continue
            if i != len(self.gameFishes) - 1:
                fishNum = info[3].get(fish, 0)
            else:
                fishNum = info[3].get(fish, 0) + info[3].get(self.gameFishes[i - 1], 0)
            iconId = ID.data.get(fish, {}).get('icon', fish)
            ret['icon'].append(['item/icon/%d.dds' % iconId, fishNum])

        self.myVal = ret
        if self.noticeMediator and self.showType == TYPE_NORMAL:
            self.noticeMediator.Invoke('setMyRankInfo', uiUtils.dict2GfxDict(ret))

    def checkInGame(self):
        for actID in self.fishingActs:
            if self.checkInGameById(actID):
                return True

        return False

    def checkInGameById(self, actID):
        p = BigWorld.player()
        aData = ABD.data.get(actID, {})
        if not aData:
            return False
        weekSet = aData.get('weekSet', 0)
        if not hasattr(p, 'fishingActivityData'):
            p.fishingActivityData = {}
        if actID in p.fishingActivityData:
            for i in range(len(aData['startTimes'])):
                if utils.inCrontabRange(aData['startTimes'][i], aData['endTimes'][i], p.getServerTime(), weekSet=weekSet):
                    return True

        return False

    def getShowType(self):
        ret = self.showType
        if ret == TYPE_NORMAL:
            ret = TYPE_FISHING_GAME_ING
        return ret

    def onShowRank(self, *arg):
        self.closeNotice()
        self.showType = TYPE_NORMAL
        if self.rankMediator:
            self.onGetRankInfo(None)
        else:
            self.showRank()

    def onGetTime(self, *arg):
        for actID in self.fishingActs:
            fData = ABD.data.get(actID, {})
            weekSet = fData.get('weekSet', 0)
            if not fData:
                continue
            if self.showType == TYPE_NORMAL and actID in BigWorld.player().fishingActivityData:
                for i in range(len(fData['startTimes'])):
                    if utils.inCrontabRange(fData['startTimes'][i], fData['endTimes'][i], BigWorld.player().getServerTime(), weekSet=weekSet):
                        return GfxValue(self.getLastTime(actID) - (BigWorld.player().getServerTime() - self.startTime))

        return 0

    def onGetRankInfo(self, *arg):
        if self.info != None:
            self.setRank(const.PROXY_KEY_TOP_FISHING_SCORE, self.ver, self.info)
        self.queryFishingScore(self.showType)

    @ui.callFilter(5)
    def onRefreshRank(self, *arg):
        self.queryFishingScore(self.showType)

    def onCloseRank(self, *arg):
        isClose = arg[3][0].GetBool()
        if not isClose or self.checkInGame():
            self.showNotice()
        self.closeRank()

    def onGetMyRank(self, *arg):
        ret = {}
        if self.myVal:
            ret = self.myVal
        else:
            ret['score'] = 0
            ret['icon'] = []
            for i, fish in enumerate(self.gameFishes):
                if i == len(self.gameFishes) - 2:
                    continue
                iconId = ID.data.get(fish, {}).get('icon', fish)
                ret['icon'].append(['item/icon/%d.dds' % iconId, 0])

        return uiUtils.dict2GfxDict(ret)

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        slot = int(key.split('.')[1][4:])
        if slot == len(self.gameFishes) - 2:
            slot += 1
        item = Item(self.gameFishes[slot])
        return gameglobal.rds.ui.inventory.GfxToolTip(item)

    def onOpenGuide(self, *arg):
        guideType = int(arg[3][0].GetNumber())
        gameglobal.rds.ui.lifeSkillGuide.show(guideType)

    def onIsInLine(self, *arg):
        p = BigWorld.player()
        spaceNo = formula.getMLGNo(p.spaceNo)
        return GfxValue(spaceNo == const.ML_GROUP_NO_FISHING)

    def onEnterLine(self, *arg):
        gameglobal.rds.ui.diGong.show(0, const.ML_GROUP_NO_FISHING)

    def onGetGameType(self, *arg):
        ret = self.getShowType()
        return GfxValue(ret)

    def onGotoGuildRank(self, *args):
        self.uiAdapter.ranking.showGuildRankPanel(const.PROXY_KEY_TOP_GUILD_FISH_ACTIVITY)

    def clearAndHide(self):
        self.hide()
        self.info = None
        self.myVal = None
        if self.callBackHandler:
            BigWorld.cancelCallback(self.callBackHandler)
            self.callBackHandler = None
