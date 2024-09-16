#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/celebrityXiuWeiRankProxy.o
import BigWorld
import events
import const
import gametypes
import gameglobal
from uiProxy import UIProxy
from gameStrings import gameStrings
from guis import uiUtils
from guis import rankPanelUtils
from data import hall_of_fame_config_data as HOFCD

class CelebrityXiuWeiRankProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CelebrityXiuWeiRankProxy, self).__init__(uiAdapter)
        self.widget = None
        self.proxyId = const.PROXY_KEY_HALL_OF_FAME_XIUWEI
        self.topType = gametypes.TOP_TYPE_HALL_OF_FAME_XIUWEI
        self.lvBtnUtil = rankPanelUtils.LvButtonsUtil()
        self.rankListUtil = rankPanelUtils.RankListUtil()
        self.refreshBtnUtil = rankPanelUtils.RefreshBtnUtil()
        self.dataCache = {}
        self.value = 0

    def clearAll(self):
        self.dataCache = {}
        self.value = 0

    def unRegisterPanel(self):
        if self.widget:
            self.refreshBtnUtil.unRegister()
            self.lvBtnUtil.unRegister()
            self.rankListUtil.unRegister()
            self.widget = None

    def initPanel(self, widget):
        self.widget = widget
        self.widget.describeText.text = HOFCD.data.get('rankDesc', {}).get(self.topType, '')
        self.widget.voteTitle.visible = False
        self.widget.noneVoteTitle.visible = True
        self.widget.noneVoteTitle.valueName.text = gameStrings.CELEBRITY_RANK_XIUWEI_VALUE
        helpKeyDict = HOFCD.data.get('rankNameToHelpkey', {})
        self.widget.noneVoteTitle.help.helpKey = helpKeyDict[self.proxyId][0]
        self.widget.lv0.visible = True
        self.widget.lv1.visible = True
        self.widget.schoolMc.visible = False
        self.refreshBtnUtil.register(self.widget.refreshBtn, self.handleClickRefreshBtn, 30)
        lvBtnInfoMap = self.uiAdapter.celebrityRank.getLvBtnInfoMap()
        lvMc = self.uiAdapter.celebrityRank.getInitLvMcName()
        self.lvBtnUtil.register(self.widget, getattr(self.widget, lvMc, None), lvBtnInfoMap, self.getData)
        rankItemMap = gameglobal.rds.ui.celebrityRank.getListItemInfoMap()
        self.rankListUtil.register(self.widget.scrollWndList, itemHeight=37, itemRenderer='CelebrityNoneVote_listItem', itemDataMap=rankItemMap, listItemCalBack=gameglobal.rds.ui.celebrityRank.listItemCommonFunc)
        self.getData()
        self.widget.myValueT.visible = True
        self.updateMyHofXiuWeiValue(self.value)

    def queryData(self, needRefresh = False):
        if not self.lvBtnUtil.currentData:
            return
        key = self.getCurrentKey()
        ver = self.dataCache.get(key, {}).get('ver', 0)
        p = BigWorld.player()
        lvKey = self.lvBtnUtil.currentData
        if needRefresh:
            BigWorld.player().cell.refreshTopHallOfFame(self.topType, ver, lvKey, 0)
        else:
            p.base.getTopHallOfFame(self.topType, ver, lvKey, 0)

    def getData(self):
        if not self.lvBtnUtil.currentData:
            return
        key = self.getCurrentKey()
        info = self.dataCache.get(key, {})
        if not info:
            info = {'key': key}
        self.refreshView(info)
        self.queryData()

    def updateData(self, info):
        key = info.get('key', 0)
        self.dataCache[key] = info
        self.refreshView(info)

    def refreshView(self, info):
        if not self.widget or info.get('key', 0) != self.getCurrentKey():
            return
        gameglobal.rds.ui.celebrityRank.refreshCommonView(self.widget, info)

    def getCurrentKey(self):
        return self.lvBtnUtil.currentData + '_%d' % const.SCHOOL_DEFAULT

    def handleClickAwardBtn(self):
        if not self.widget:
            return
        key = self.getCurrentKey()
        myRank = self.dataCache.get(key, {}).get('myRank', 0)
        gameglobal.rds.ui.celebrityRankReward.show(self.topType, myRank, self.lvBtnUtil.currentData, const.SCHOOL_DEFAULT)

    def handleClickRefreshBtn(self):
        self.queryData(needRefresh=True)

    def getXiuWeiValue(self):
        if not self.widget:
            return
        key = self.getCurrentKey()
        info = self.dataCache.get(key, {})
        myRank = info.get('myRank', 0)
        if myRank:
            self.widget.myValueT.text = ''
            p = BigWorld.player()
            p.cell.getMyHofRankValue(gametypes.TOP_TYPE_HALL_OF_FAME_XIUWEI)
        else:
            self.widget.myValueT.text = gameStrings.HALL_OF_FAME_XIUWEI_VALUE % gameStrings.RANK_NOT_IN_TEXT

    def updateMyHofXiuWeiValue(self, value):
        if not self.widget:
            return
        if self.value != value:
            self.value = value
        if self.value:
            self.widget.myValueT.text = gameStrings.HALL_OF_FAME_XIUWEI_VALUE % str(self.value)
        else:
            self.widget.myValueT.text = gameStrings.HALL_OF_FAME_XIUWEI_VALUE % gameStrings.RANK_NOT_IN_TEXT
