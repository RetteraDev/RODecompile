#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/noticeBoardProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import ui
import const
import gametypes
import commQuest
import utils
import datetime
from guis.uiProxy import UIProxy
from guis import uiConst, uiUtils
from item import Item
from data import delegation_data as DELD
from callbackHelper import Functor
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
from data import item_data as ID
from cdata import font_config_data as FCD
from data import fame_data as FD
delegationPos = SCD.data.get('delegationPos', ())

class NoticeBoardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NoticeBoardProxy, self).__init__(uiAdapter)
        self.modelMap = {'initDone': self.onInitDone,
         'acceptDelegation': self.onAcceptDel,
         'openDlg': self.onOpenDlg}
        self.refreshEnable = True
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_NOTICE_BOARD, self.hide)
        uiAdapter.registerEscFunc(uiConst.WIDGET_DELEGATION_DETAIL, self.hideDetail)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_NOTICE_BOARD:
            self.med = mediator
            return uiUtils.array2GfxAarry(delegationPos)
        if widgetId == uiConst.WIDGET_DELEGATION_DETAIL:
            self.detailMed = mediator
            return self.selectDlg

    def _asWidgetClose(self, widgetId, multiID):
        if widgetId == uiConst.WIDGET_NOTICE_BOARD:
            self.hide(self.destroyOnHide)
        elif widgetId == uiConst.WIDGET_DELEGATION_DETAIL:
            self.hideDetail()

    def checkCanOpen(self):
        openQuestLv = SCD.data.get('openDelegationLv', 0)
        p = BigWorld.player()
        if p.lv < openQuestLv:
            p.showGameMsg(GMDD.data.ENTRUST_LEVEL_LOW, ())
            return False
        return True

    def show(self, *args):
        if args and len(args):
            self.union = args[0]
            self.ranks = args[1]
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_NOTICE_BOARD)
        self.checkCanOpen()

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_NOTICE_BOARD)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DELEGATION_DETAIL)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def hideDetail(self):
        self.detailMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DELEGATION_DETAIL)

    def reset(self):
        self.med = None
        self.detailMed = None
        self.delegations = {}
        self.callback = None
        self.union = 1
        self.ranks = ()
        self.lastDelegations = None
        if hasattr(self, 'pollingCallback') and self.pollingCallback:
            BigWorld.cancelCallback(self.pollingCallback)
        self.pollingCallback = None
        self.selectDlg = None

    def onInitDone(self, *args):
        self.startPolling(True)
        self.callback = BigWorld.callback(0.2, Functor(self.updataAllDelegtion, False))

    @ui.callFilter(1)
    def onAcceptDel(self, *args):
        nuid = long(args[3][0].GetString())
        did = int(args[3][1].GetString())
        if BigWorld.player().benefitDgts.has_key(nuid):
            src = gametypes.DELEGATE_AC_SRC_BENEFIT
        else:
            src = gametypes.DELEGATE_AC_SRC_STUB
        BigWorld.player().cell.acceptDelegation(nuid, did, src)

    def onOpenDlg(self, *args):
        if self.checkCanOpen():
            self.selectDlg = args[3][0]
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DELEGATION_DETAIL)

    def acceptDone(self, nuid, src, dId):
        if self.detailMed:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DELEGATION_DETAIL)
            self.detailMed = None
            if src == gametypes.DELEGATE_AC_SRC_BENEFIT:
                self.delDgts([str(nuid)])

    def startPolling(self, forceRef = False):
        BigWorld.player().fetchDelegations(self.union, self.ranks, forceRef)
        if self.med:
            self.pollingCallback = BigWorld.callback(1, self.startPolling)

    def refreshAllDelegation(self):
        if self.pollingCallback:
            BigWorld.cancelCallback(self.pollingCallback)
        self.startPolling()

    def updataAllDelegtion(self, cancelCallBack = True):
        if self.callback and cancelCallBack:
            BigWorld.cancelCallback(self.callback)
            self.callback = None
        if self.med:
            delDatas = self._getAllGfxDelegation()
            self.med.Invoke('setAllWeiTuo', delDatas)
        self.lastDelegations = BigWorld.player().delegations

    def delDgts(self, delNUIDs):
        if self.med:
            self.med.Invoke('delDelegations', uiUtils.array2GfxAarry(delNUIDs))
        if self.detailMed:
            self.detailMed.Invoke('beenAccepted', uiUtils.array2GfxAarry(delNUIDs))

    def _getAllGfxDelegation(self):
        p = BigWorld.player()
        result = []
        for nuid, delData in p.allDelegations.items():
            delId = delData.get('dId', 0)
            dConData = DELD.data.get(delId)
            gfxData = self.getDlgInfo(nuid, delData)
            if p.benefitDgts.has_key(nuid):
                suggestType = gametypes.DELEGATE_MARK_RECOMMEND
            elif dConData.get('type') == gametypes.DELEGATE_TYPE_LIMIT:
                suggestType = gametypes.DELEGATE_MARK_LIMIT
            else:
                suggestType = gametypes.DELEGATE_MARK_URGENT
            gfxData['suggestType'] = suggestType
            if gfxData.has_key('deadLine') and gfxData['deadLine'] - BigWorld.player().getServerTime() <= 0:
                continue
            result.append(gfxData)

        for nuid, dlgData in p.benefitDgts.items():
            did = dlgData.get(const.DD_DID)
            dConData = DELD.data.get(did, {})
            if dConData and dConData.get('union') == self.union and dConData.get('rank') in self.ranks:
                gfxData = gameglobal.rds.ui.delegationBook._getDlgInfo(did, dlgData, False, False)
                gfxData['id'] = str(nuid)
                gfxData['needFame'] = self.getNeedItem(dConData, False)
                if gfxData.has_key('deadLine') and gfxData['deadLine'] - BigWorld.player().getServerTime() <= 0:
                    continue
                result.append(gfxData)

        return uiUtils.array2GfxAarry(result, True)

    def getDlgInfo(self, nuid, delData):
        delId = delData.get('dId', 0)
        gfxData = {'id': str(nuid),
         'did': str(delId)}
        p = BigWorld.player()
        cTime = p.getServerTime()
        dConData = DELD.data.get(delId, {})
        gfxData['type'] = dConData.get('type')
        gfxData['subType'] = dConData.get('subType', 0)
        gfxData['isNew'] = not BigWorld.player().getPreDgtFlag(delId)
        questDetail = p.genQuestLoopDetail(dConData.get('quest', 0))
        gfxData['name'] = questDetail.get('taskName', '')
        gfxData['detail'] = questDetail.get('taskDesc', '')
        gfxData['star'] = dConData.get('star', 0)
        gfxData['lv'] = dConData.get('exploreLv', 0)
        gfxData['rank'] = dConData.get('rank', 0)
        gfxData['bonusType'] = delData.get('bonusType', 0)
        gfxData['deadLine'] = delData.get('deadline', 0)
        gfxData['bonusRate'] = delData.get('bonusRate', 0)
        gfxData['delegator'] = dConData.get('delegator', '')
        if delData.has_key('deadline'):
            gfxData['endTimeStr'] = datetime.datetime.fromtimestamp(gfxData['deadLine']).strftime('%H:%M')
            gfxData['endTime'] = delData.get('deadline') - cTime
        gfxData['needFame'] = self.getNeedItem(dConData, gfxData['type'] == gametypes.DELEGATION_UI_TYPE_ZHUAN_FA)
        if delData.has_key('timeLeft'):
            gfxData['duration'] = utils.formatTime(delData.get('timeLeft', 0))
        else:
            gfxData['duration'] = utils.formatTime(dConData.get('timeLimit', 0))
        gfxData['baseAward'] = self.getDelegationAward(delId)
        if delData.has_key('agentCash'):
            gfxData['baseAward']['agentCash'] = delData.get('agentCash', 0)
        gfxData['baseAward']['tips'] = {'cash': gameStrings.TEXT_INVENTORYPROXY_3296,
         'bindCash': gameStrings.TEXT_INVENTORYPROXY_3297,
         'exp': gameStrings.TEXT_GAMETYPES_6408,
         'fame': gameStrings.TEXT_DELEGATIONBOOKPROXY_304}
        gfxData['newTip'] = self.getNewDlgTip()
        gfxData['delegatorId'] = dConData.get('delegatorId', 1)
        fameNum = dConData.get('award', ((4, 0),))[0][0]
        gfxData['fameName'] = FD.data.get(fameNum, {}).get('name', '')
        return gfxData

    def getNewDlgTip(self):
        return gameStrings.TEXT_NOTICEBOARDPROXY_220 % (SCD.data.get('dgtRookieFameBonus', 2),
         SCD.data.get('dgtRookieExpBonus', 2),
         SCD.data.get('dgtRookieCashBonus', 2),
         SCD.data.get('dgtRookieItemBonus', 2))

    def getNeedItem(self, dConData, isTran = False):
        result = []
        needItems = dConData.get('needFames', ())
        for itemNum in needItems:
            tip = FD.data.get(itemNum[0], {}).get('name', '')
            result.append({'icon': 'item/icon/%s.dds' % const.FAME_ICONS.get(itemNum[0], ''),
             'tip': tip,
             'num': itemNum[1]})

        return result

    def getDelegationAward(self, dId):
        dData = DELD.data.get(dId)
        award = {}
        items = []
        p = BigWorld.player()
        agentCash = p.delegationData.get(dId, {}).get(const.DD_AGENT_CASH, 0)
        if agentCash:
            award['agentCash'] = agentCash
        if dData:
            exp, cash = commQuest.calcDelegationReward(BigWorld.player(), dId)
            award['cash'] = int(cash)
            award['exp'] = int(exp)
            for itemNum in dData.get('award', ()):
                if itemNum[0] == const.FAME_TYPE_ORG:
                    award['fame'] = itemNum[1]
                else:
                    tip = FD.data.get(itemNum[0], {}).get('desc', '')
                    items.append({'icon': 'item/icon/%s.dds' % const.FAME_ICONS.get(itemNum[0], ''),
                     'tip': tip,
                     'num': itemNum[1],
                     'isItem': False})

            for item in commQuest.genDelegationRewardItems(p, dId):
                path = uiUtils.getItemIconFile40(item[0])
                quality = ID.data.get(item[0], {}).get('quality', 1)
                color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                tip = gameglobal.rds.ui.inventory.GfxToolTip(Item(item[0]))
                items.append({'icon': path,
                 'num': item[1],
                 'color': color,
                 'isItem': True,
                 'tip': tip})

            award['items'] = items
        return award
