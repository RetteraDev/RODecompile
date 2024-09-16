#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/zhanXunRankListProxy.o
from gamestrings import gameStrings
import BigWorld
from uiProxy import UIProxy
import gameglobal
import utils
import gametypes
from guis import uiConst
from guis import uiUtils
from Scaleform import GfxValue
from ui import gbk2unicode
from cdata import game_msg_def_data as GMDD
from data import zhanxun_rank_data as ZRD
from data import bonus_data as BD
from data import mail_template_data as MTD

class ZhanXunRankListProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ZhanXunRankListProxy, self).__init__(uiAdapter)
        self.modelMap = {'requestZhanXunList': self.onRequstZhanXunList,
         'updateList': self.onUpdateList,
         'getCountDown': self.onGetCountDown}
        self.mediator = None
        self.cachaData = None
        self.countDown = 0
        self.timerId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_ZHANXUN_RANK_LIST, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ZHANXUN_RANK_LIST:
            self.mediator = mediator

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ZHANXUN_RANK_LIST)
        self.refreshUpdateBtn()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ZHANXUN_RANK_LIST)

    def onGetCountDown(self, *arg):
        return GfxValue(self.countDown)

    def onRequstZhanXunList(self, *arg):
        self._requestRankData()

    def _requestRankData(self):
        version = 0
        if self.cachaData != None:
            version = self.cachaData['version']
            self.updateZhanXunData(self.cachaData)
        if self.countDown <= 0:
            BigWorld.player().cell.refreshTopZhanXun(version)
            self.countDown = 120
            self.timerId = BigWorld.callback(1.0, self.updateTimer)

    def onUpdateList(self, *arg):
        if self.countDown > 0:
            BigWorld.player().showGameMsg(GMDD.data.CALL_ZHAN_XUN_RANK_TOO_FREQUNCY, ())
        else:
            self._requestRankData()

    def updateZhanXunData(self, data):
        p = BigWorld.player()
        self.cachaData = data
        rankList = data['data']
        rankList = sorted(rankList, key=lambda x: x['timestamp'])
        rankList = sorted(rankList, key=lambda x: x['val'], reverse=True)
        ret = []
        for i in xrange(len(rankList)):
            rank = rankList[i]
            obj = {}
            isMySelf = rank['gbId'] == p.gbId
            obj['rankIndex'] = i + 1
            obj['isMySelf'] = isMySelf
            obj['rank'] = uiUtils.toHtml(i + 1, color='#a65b11') if isMySelf else i + 1
            obj['playerName'] = uiUtils.toHtml(rank['roleName'], color='#a65b11') if isMySelf else rank['roleName']
            obj['zhanxun'] = uiUtils.toHtml(rank['val'], color='#a65b11') if isMySelf else rank['val']
            junjie = gameStrings.TEXT_ZHANXUNRANKLISTPROXY_89 % self._getJunjieReward(i + 1)
            obj['junjie'] = uiUtils.toHtml(junjie, color='#a65b11') if isMySelf else junjie
            obj['items'] = self._getItemsByRank(i + 1)
            obj['gbId'] = rank['gbId']
            ret.append(obj)

        if self.mediator:
            self.mediator.Invoke('updateZhanXunList', uiUtils.array2GfxAarry(ret, True))
        self.updateMyRankList(ret)

    def updateMyRankList(self, rankList):
        if len(rankList) == 0:
            return []
        p = BigWorld.player()
        myGbId = p.gbId
        myRankList = []
        for i in xrange(len(rankList)):
            if myGbId == rankList[i]['gbId']:
                if i == 0:
                    myRankList.append(rankList[i])
                    if i + 1 < len(rankList):
                        myRankList.append(rankList[i + 1])
                    if i + 2 < len(rankList):
                        myRankList.append(rankList[i + 2])
                elif i == len(rankList) - 1:
                    myRankList.append(rankList[i])
                elif i > 0 and i < len(rankList):
                    myRankList.append(rankList[i - 1])
                    myRankList.append(rankList[i])
                    myRankList.append(rankList[i + 1])

        if self.mediator:
            self.mediator.Invoke('updateMyZhanXunList', uiUtils.array2GfxAarry(myRankList, True))

    def _getJunjieReward(self, rank):
        data = ZRD.data
        for key in data:
            rangeMin = key[0]
            rangeMax = key[1]
            if rangeMin <= rank <= rangeMax:
                return data[key].get('rewardJunJie', 0)

        return 0

    def _getItemsByRank(self, rank):
        data = ZRD.data
        mailId = 0
        items = []
        for key in data:
            rangeMin = key[0]
            rangeMax = key[1]
            if rangeMin <= rank <= rangeMax:
                mailId = data[key].get('mailId', 0)
                break

        bonusId = MTD.data.get(mailId, {}).get('bonusId', 0)
        fixedBonus = BD.data.get(bonusId, {}).get('fixedBonus', [])
        fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
        for item in fixedBonus:
            if item[0] == 1:
                items.append(uiUtils.getGfxItemById(item[1], count=item[2]))

        return items

    def updateTimer(self):
        self.refreshUpdateBtn()
        if self.countDown > 0:
            self.countDown -= 1
            self.timerId = BigWorld.callback(1.0, self.updateTimer)
        else:
            BigWorld.cancelCallback(self.timerId)

    def refreshUpdateBtn(self):
        if self.mediator:
            label = gameStrings.TEXT_XINMORECORDPROXY_50
            enable = True
            if self.countDown > 0:
                label = gameStrings.TEXT_ZHANXUNRANKLISTPROXY_168 % self.countDown
                enable = False
            self.mediator.Invoke('refreshUpdateBtn', (GfxValue(gbk2unicode(label)), GfxValue(enable)))
