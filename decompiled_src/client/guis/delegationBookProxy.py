#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/delegationBookProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
import gametypes
import commQuest
import utils
import datetime
import time
import copy
from guis.uiProxy import UIProxy
from guis import uiConst, uiUtils
from callbackHelper import Functor
from data import delegation_upgrade_data as DLGUD
from data import delegation_data as DELD
from data import sys_config_data as SCD
from data import fame_data as FD
from data import delegation_record_data as DRD
from cdata import game_msg_def_data as GMDD
delegationPos = SCD.data.get('delegationPos', ())
refreshCD = 3600
MAX_RANK = 5
TAB_ORG_INFO = 0
TAB_CAN_ACCEPT = 1
TAB_BEEN_ACCEPT = 2

class DelegationBookProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(DelegationBookProxy, self).__init__(uiAdapter)
        self.modelMap = {'getOrgInfo': self.onGetOrgInfo,
         'getAcceptableDlgsInfo': self.onGetAcceptAbleDlgsInfo,
         'getAcceptedDlgs': self.onGetAcceptedDlgs,
         'getOrgRecord': self.onGetOrgRecord,
         'abandonDlg': self.onAbandonDlg,
         'refreshDlgs': self.onRefreshDlgs,
         'acceptDlg': self.onAcceptDlg,
         'autoFindPath': self.onAutoFindPath,
         'gotoTrack': self.onGotoTrack,
         'confirmRefresh': self.onConfirmRefresh,
         'setTrack': self.onSetTrack}
        self.refreshMeditor = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_DELEGATION_BOOK, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_DELEGATION_BOOK:
            self.med = mediator
            if not self.tabIndex:
                promotionIds = self.getUnAccpetPromotions()
                if len(BigWorld.player().delegations):
                    self.tabIndex = TAB_BEEN_ACCEPT
                elif promotionIds or len(BigWorld.player().bookDgts) or len(BigWorld.player().stableDgts):
                    self.tabIndex = TAB_CAN_ACCEPT
            return GfxValue(self.tabIndex)
        if widgetId == uiConst.WIDGET_DELEGATION_RANK_UP:
            return self.getOrgGfxData()
        if widgetId == uiConst.WIDGET_DELEGATION_REFRESH_COST:
            self.refreshMeditor = mediator
            return uiUtils.array2GfxAarry([self.bookRefCost, self.totalCost])

    def _asWidgetClose(self, widgetId, multiID):
        if widgetId == uiConst.WIDGET_DELEGATION_RANK_UP:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DELEGATION_RANK_UP)
        elif widgetId == uiConst.WIDGET_DELEGATION_REFRESH_COST:
            self.refreshMeditor = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DELEGATION_REFRESH_COST)
        else:
            UIProxy._asWidgetClose(self, widgetId, multiID)

    def checkCanOpen(self):
        if not gameglobal.rds.configData.get('enableDelegation', False):
            return False
        p = BigWorld.player()
        if not BigWorld.player().checkMapLimitUI(gametypes.MAP_LIMIT_UI_DELEGATE):
            return False
        openQuestLv = SCD.data.get('openDelegationLv', 0)
        if p.lv < openQuestLv:
            p.showGameMsg(GMDD.data.DELEGATION_BOOK_LV_LOW, ())
            return False
        return True

    def onGetOrgRecord(self, *args):
        record = []
        roleName = BigWorld.player().roleName
        records = BigWorld.player().delegationRecords
        for i in records:
            data = DRD.data.get(i.rid, {})
            trueData = copy.deepcopy(data)
            if trueData.get('title'):
                trueData['title'] = trueData['title'] % roleName
            trueData['dateTitle'] = time.strftime('%Y/%m/%d', time.localtime(i.time))
            trueData['dateEnd'] = time.strftime('%Y.%m.%d  %H:%M', time.localtime(i.time))
            record.append(trueData)

        return uiUtils.array2GfxAarry(record, True)

    def show(self, *args):
        if self.checkCanOpen():
            if args and len(args) > 0:
                self.tabIndex = args[0]
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DELEGATION_BOOK)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DELEGATION_BOOK)

    def reset(self):
        self.med = None
        self.tabIndex = 0
        self.showInitDid = 0
        self.subType = 0
        self.rank = 0
        self.bookRefCost = 0
        self.totalCost = 0

    def onGetOrgInfo(self, *args):
        return self.getOrgGfxData()

    def onGetAcceptAbleDlgsInfo(self, *args):
        p = BigWorld.player()
        promotionIds = self.getUnAccpetPromotions()
        return uiUtils.array2GfxAarry([self._getBookDlg(),
         p.compDgtCnt,
         p.lastRefTime + refreshCD - p.getServerTime(),
         promotionIds], True)

    def onGetAcceptedDlgs(self, *args):
        return uiUtils.array2GfxAarry([self._getAcceptedDlg(), self.showInitDid], True)

    def onAbandonDlg(self, *args):
        dId = args[3][0].GetNumber()
        BigWorld.player().cell.abandonDelegation(dId)

    def abandonDlgSucc(self, dId):
        if self.med:
            self.med.Invoke('refreshAcceptedPanel', uiUtils.array2GfxAarry(self._getAcceptedDlg(), True))

    def acceptDone(self, nuid, src, dId):
        if self.med:
            self.med.Invoke('acceptDone', GfxValue(int(dId)))

    def refreshBook(self):
        if self.med:
            self.med.Invoke('refreshAcceptablePanel')

    def refreshAcceptedPanel(self):
        if self.med:
            self.med.Invoke('refreshAcceptedPanel', uiUtils.array2GfxAarry(self._getAcceptedDlg(), True))

    def onRefreshDlgs(self, *args):
        self.subType = args[3][0].GetNumber()
        self.rank = args[3][1].GetNumber()
        p = BigWorld.player()
        if self.rank > p.delegationRank:
            p.showGameMsg(GMDD.data.MARKER_44061, ())
            self.med.Invoke('resetRefMenu')
            return
        else:
            self.bookRefCost = commQuest.calcBookRefCost(BigWorld.player(), self.subType, self.rank)
            self.totalCost = sum(self.bookRefCost[1:3]) + max(self.bookRefCost[0] - self.bookRefCost[3], 0)
            if self.totalCost > 0:
                if self.refreshMeditor != None:
                    self.refreshMeditor.Invoke('refreshRefreshCostPanel', uiUtils.array2GfxAarry([self.bookRefCost, self.totalCost]))
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DELEGATION_REFRESH_COST)
            else:
                self.doRefresh(self.subType, self.rank)
            return

    def onConfirmRefresh(self, *arg):
        p = BigWorld.player()
        if uiUtils.checkBindCashEnough(self.totalCost, p.bindCash, p.cash, Functor(self.doRefresh, self.subType, self.rank)):
            self.doRefresh(self.subType, self.rank)
        self.refreshMeditor = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DELEGATION_REFRESH_COST)

    def onSetTrack(self, *args):
        did = args[3][0].GetNumber()
        tracked = args[3][1].GetBool()
        questLoopId = DELD.data.get(did, {}).get('quest')
        if questLoopId:
            gameglobal.rds.ui.questLog.setQuestTracked(questLoopId, gametypes.QUEST_TYPE_LOOP, tracked)

    def doRefresh(self, subType, rank):
        BigWorld.player().cell.refreshBookDelegation(subType, rank)

    def refreshCompDgtCnt(self):
        if self.med:
            self.med.Invoke('refreshCompDgtCnt', GfxValue(BigWorld.player().compDgtCnt))

    def refreshLeftTimeTxt(self):
        if self.med:
            leftTime = BigWorld.player().lastRefTime + refreshCD - BigWorld.player().getServerTime()
            self.med.Invoke('refreshLeftTimeTxt', GfxValue(leftTime))

    def onAcceptDlg(self, *args):
        nuid = long(args[3][0].GetString())
        did = args[3][1].GetNumber()
        src = args[3][2].GetNumber()
        BigWorld.player().cell.acceptDelegation(nuid, did, src)

    def onAutoFindPath(self, *args):
        gameglobal.rds.ui.questLog.onAutoFindPath(*args)

    def onGotoTrack(self, *args):
        gameglobal.rds.ui.questLog.onGotoTrack(*args)

    def _getAcceptedDlg(self):
        arr = []
        p = BigWorld.player()
        for did in p.delegations:
            dlgData = p.delegationData.get(did, {})
            gfxData = self._getDlgInfo(did, dlgData, True)
            arr.append(gfxData)

        return arr

    def _getBookDlg(self):
        arr = []
        p = BigWorld.player()
        for nuid, dlgData in p.bookDgts.items() + p.stableDgts.items():
            did = dlgData.get(const.DD_DID)
            gfxData = self._getDlgInfo(did, dlgData, False)
            gfxData['nuid'] = str(nuid)
            arr.append(gfxData)

        promotionDlgs = self.getUnAccpetPromotions()
        if promotionDlgs:
            for did in promotionDlgs:
                gfxData = self._getDlgInfo(did, None, False)
                gfxData['src'] = gametypes.DELEGATE_AC_SRC_PROMOTION
                gfxData['nuid'] = str(did)
                arr.append(gfxData)

        return arr

    def _getDlgInfo(self, did, dlgData, accepted = False, onBook = True):
        p = BigWorld.player()
        gfxData = {'did': did}
        dConData = DELD.data.get(did, {})
        gfxData['type'] = dConData.get('type')
        gfxData['subType'] = dConData.get('subType', 0)
        gfxData['isNew'] = not BigWorld.player().getPreDgtFlag(did)
        loopQuestId = dConData.get('quest', 0)
        if accepted:
            gfxData['leftTime'] = dlgData.get(const.DD_BEGIN_TIME, 0) + dlgData.get(const.DD_TIME_LIMIT, 0) - BigWorld.player().getServerTime()
            if loopQuestId in p.questLoopInfo and p.questLoopInfo[loopQuestId].getCurrentQuest():
                questId = p.questLoopInfo[loopQuestId].getCurrentQuest()
                questDetail = p.genQuestDetail(questId, loopQuestId)
                gfxData['questInfo'] = gameglobal.rds.ui.questLog.gfxQuestDetail(questDetail)
                gfxData['tracked'] = p.getQuestData(questId, const.QD_QUEST_TRACKED)
                gfxData['detail'] = questDetail.get('taskShortDesc', '')
            else:
                questDetail = p.genQuestLoopDetail(loopQuestId)
                gfxData['tracked'] = False
                gfxData['detail'] = questDetail.get('taskDesc', '')
        else:
            questDetail = p.genQuestLoopDetail(loopQuestId)
            if dlgData:
                if not onBook:
                    gfxData['deadLine'] = dlgData.get(const.DD_BEGIN_TIME, 0) + 43200
                    gfxData['endTime'] = gfxData['deadLine'] - BigWorld.player().getServerTime()
                    gfxData['endTimeStr'] = datetime.datetime.fromtimestamp(gfxData['deadLine']).strftime('%H:%M')
                elif dlgData.get(const.DD_MARK_TYPE) in (gametypes.DELEGATE_MARK_URGENT, gametypes.DELEGATE_MARK_LIMIT):
                    gfxData['leftTime'] = dlgData.get(const.DD_BEGIN_TIME, 0) + dConData.get('duration') - BigWorld.player().getServerTime()
                elif dConData.get('duration'):
                    gfxData['deadLine'] = dlgData.get(const.DD_BEGIN_TIME, 0) + dConData.get('duration')
                    gfxData['endTime'] = dlgData.get(const.DD_BEGIN_TIME, 0) + dConData.get('duration') - BigWorld.player().getServerTime()
                    gfxData['endTimeStr'] = datetime.datetime.fromtimestamp(gfxData['deadLine']).strftime('%H:%M')
            gfxData['detail'] = questDetail.get('taskDesc', '')
        gfxData['name'] = questDetail.get('taskName', '')
        gfxData['union'] = dConData.get('union', '')
        gfxData['star'] = dConData.get('star', 0)
        gfxData['lv'] = dConData.get('exploreLv', 0)
        gfxData['rank'] = dConData.get('rank', 0)
        fameNum = dConData.get('award', ((4, 0),))[0][0]
        gfxData['fameName'] = FD.data.get(fameNum, {}).get('name', '')
        if dlgData:
            gfxData['bonusType'] = dlgData.get(const.DD_BONUS_TYPE, 0)
            gfxData['bonusRate'] = dlgData.get(const.DD_BONUS_RATE, 0)
            gfxData['src'] = dlgData.get(const.DD_SRC, gametypes.DELEGATE_AC_SRC_BOOK)
            gfxData['suggestType'] = dlgData.get(const.DD_MARK_TYPE, 0)
        gfxData['delegator'] = dConData.get('delegator', '')
        gfxData['baseAward'] = gameglobal.rds.ui.noticeBoard.getDelegationAward(did)
        gfxData['baseAward']['tips'] = {'cash': gameStrings.TEXT_INVENTORYPROXY_3296,
         'bindCash': gameStrings.TEXT_INVENTORYPROXY_3297,
         'exp': gameStrings.TEXT_GAMETYPES_6408,
         'fame': gameStrings.TEXT_DELEGATIONBOOKPROXY_304}
        if dlgData and dlgData.get(const.DD_MARK_TYPE) == gametypes.DELEGATE_MARK_URGENT:
            gfxData['duration'] = utils.formatTime(dConData.get('urgentTimeLimit', 0))
        else:
            gfxData['duration'] = utils.formatTime(dConData.get('timeLimit', 0))
        gfxData['newTip'] = gameglobal.rds.ui.noticeBoard.getNewDlgTip()
        gfxData['delegatorId'] = dConData.get('delegatorId', 1)
        return gfxData

    def getOrgGfxData(self):
        result = {}
        p = BigWorld.player()
        rank = p.delegationRank
        orgProValue = p.fame.get(const.FAME_TYPE_ORG, 0)
        maxValue = 0
        lastRankMaxValue = 0
        title = gameStrings.TEXT_DELEGATIONBOOKPROXY_320
        thirdRankMaxValue = 0
        for id, upgradeData in DLGUD.data.items():
            if upgradeData.get('rank') == rank and not maxValue:
                maxValue = upgradeData.get('fame', (0, 1))[0][1]
                rankTxt = upgradeData.get('rankTxt', '')
                titleFames = upgradeData.get('titleFames', 0)
                titleNames = upgradeData.get('titleNames', '')
                if titleNames:
                    if isinstance(titleNames, str):
                        title = title % (rankTxt, str(titleNames))
                    else:
                        index = len(titleFames) - 1
                        for i in xrange(len(titleFames)):
                            if titleFames[i] > orgProValue:
                                index = i - 1
                                break

                        title = title % (rankTxt, titleNames[index])
            elif upgradeData.get('rank') == rank - 1:
                lastRankMaxValue = upgradeData.get('fame', (0, 0))[0][1]
            if rank == MAX_RANK and upgradeData.get('rank') == rank - 2:
                thirdRankMaxValue = upgradeData.get('fame', (0, 0))[0][1]

        if rank >= MAX_RANK:
            orgProValue = maxValue = 2 * lastRankMaxValue - thirdRankMaxValue
        result['lv'] = rank
        result['orgProValue'] = orgProValue - lastRankMaxValue
        result['maxValue'] = maxValue - lastRankMaxValue
        result['name'] = BigWorld.player().realRoleName
        result['title'] = title
        result['delegator'] = self._getDelegatorType()
        result['normalItemNum'] = BigWorld.player().fame.get(const.FAME_TYPE_NORMAL_XINWU, 0)
        result['advanceItemNum'] = BigWorld.player().fame.get(const.FAME_TYPE_ADVANCE_XINWU, 0)
        result['normalItemTip'] = FD.data.get(const.FAME_TYPE_NORMAL_XINWU, {}).get('desc', '')
        result['advanceItemTip'] = FD.data.get(const.FAME_TYPE_ADVANCE_XINWU, {}).get('desc', '')
        if orgProValue == maxValue:
            nextTrankTxt = ''
            if rank == MAX_RANK:
                nextTrankTxt = gameStrings.TEXT_DELEGATIONBOOKPROXY_359
            else:
                for id, upgradeData in DLGUD.data.items():
                    if upgradeData.get('rank') == rank + 1:
                        nextTrankTxt = gameStrings.TEXT_DELEGATIONBOOKPROXY_363 % upgradeData.get('rankTxt', '')
                        break

            result['tips'] = nextTrankTxt
        return uiUtils.dict2GfxDict(result, True)

    def getUnAccpetPromotions(self):
        promotionDlgs = commQuest.fetchPromotionDelegations(BigWorld.player())
        return [ dId for dId in promotionDlgs if dId not in BigWorld.player().delegations ]

    def showRankUp(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DELEGATION_RANK_UP)

    def onQuestTrackChanged(self, questId, questType, isTracked):
        self.refreshAcceptedPanel()

    def updateFame(self, fameId, oldValue, value):
        if fameId == const.FAME_TYPE_ORG:
            if oldValue > 0:
                if self._getTitleIndex(value) > self._getTitleIndex(oldValue):
                    self.showRankUp()

    def _getTitleIndex(self, fameValue):
        index = -1
        if BigWorld.player().delegationRank == MAX_RANK:
            return index
        for id, upgradeData in DLGUD.data.items():
            if upgradeData.get('rank') == BigWorld.player().delegationRank:
                titleFames = upgradeData.get('titleFames', 0)
                if titleFames:
                    if isinstance(titleFames, tuple):
                        index = len(titleFames) - 1
                        for i in xrange(len(titleFames)):
                            if titleFames[i] > fameValue:
                                index = i - 1
                                break

        return index

    def _getDelegatorType(self):
        if BigWorld.player().delegationRank == MAX_RANK:
            return 3
        if BigWorld.player().delegationRank >= 3:
            return 2
        return 1
