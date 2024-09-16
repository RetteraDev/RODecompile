#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/celebrityVoteRankProxy.o
import BigWorld
import gameglobal
import events
import gametypes
from uiProxy import UIProxy
from gameStrings import gameStrings
from guis import uiUtils
from guis import rankPanelUtils
from data import hall_of_fame_toprank_data as HOFTD
from data import personal_zone_gift_data as PZGD
from data import hall_of_fame_config_data as HOFCD
from cdata import game_msg_def_data as GMDD

class CelebrityVoteRankProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CelebrityVoteRankProxy, self).__init__(uiAdapter)
        self.widget = None
        self.rankListUtil = rankPanelUtils.RankListUtil()
        self.hongyanRefreshBtnUtil = rankPanelUtils.RefreshBtnUtil()
        self.yingcaiRefreshBtnUtil = rankPanelUtils.RefreshBtnUtil()
        self.guibaoRefreshBtnUtil = rankPanelUtils.RefreshBtnUtil()
        self.shituRefreshBtnUtil = rankPanelUtils.RefreshBtnUtil()
        self.qiaojiangRefreshBtnUtil = rankPanelUtils.RefreshBtnUtil()
        self.currentRefreshBtnUtil = None
        self.topType = None
        self.proxyId = None
        self.dataCache = {}
        self.topTypeToValues = {}

    def clearAll(self):
        self.proxyId = None
        self.topType = None
        self.dataCache = {}
        self.topTypeToValues = {}

    def unRegisterPanel(self):
        if self.widget:
            self.rankListUtil.unRegister()
            self.currentRefreshBtnUtil.unRegister()
            self.currentRefreshBtnUtil = None
            self.topType = None
            self.proxyId = None
            self.widget = None

    def initPanel(self, widget):
        self.widget = widget
        self.widget.voteTitle.visible = False
        self.widget.noneVoteTitle.visible = True
        self.widget.noneVoteTitle.valueName.text = gameStrings.CELEBRITY_RANK_VOTE_VALUE
        self.widget.schoolMc.visible = False
        self.widget.lv0.visible = False
        self.widget.lv1.visible = False
        self.topType, self.proxyId = gameglobal.rds.ui.celebrityRank.getCurrentVoteRank()
        if not self.topType or not self.proxyId:
            return
        self.widget.describeText.text = HOFCD.data.get('rankDesc', {}).get(self.topType, '')
        if self.topType == gametypes.TOP_TYPE_HALL_OF_FAME_HONGYAN:
            self.currentRefreshBtnUtil = self.hongyanRefreshBtnUtil
        elif self.topType == gametypes.TOP_TYPE_HALL_OF_FAME_YINGCAI:
            self.currentRefreshBtnUtil = self.yingcaiRefreshBtnUtil
        elif self.topType == gametypes.TOP_TYPE_HALL_OF_FAME_QIAOJIANG:
            self.currentRefreshBtnUtil = self.qiaojiangRefreshBtnUtil
        elif self.topType == gametypes.TOP_TYPE_HALL_OF_FAME_GUIBAO:
            self.currentRefreshBtnUtil = self.guibaoRefreshBtnUtil
        elif self.topType == gametypes.TOP_TYPE_HALL_OF_FAME_MINGSHI:
            self.currentRefreshBtnUtil = self.shituRefreshBtnUtil
        self.currentRefreshBtnUtil.register(self.widget.refreshBtn, self.handleClickRefreshBtn, 30)
        rankItemMap = gameglobal.rds.ui.celebrityRank.getListItemInfoMap()
        self.rankListUtil.register(self.widget.scrollWndList, 37, 'CelebrityNoneVote_listItem', rankItemMap, clickListItemCalBack=self.handleClickListItem, listItemCalBack=gameglobal.rds.ui.celebrityRank.listItemCommonFunc)
        self.getData()
        if self.topType not in self.topTypeToValues:
            self.topTypeToValues[self.topType] = 0
        self.updateMyHofVoteValue(self.topType, self.topTypeToValues[self.topType])

    def queryData(self, needRefresh = False):
        if not self.proxyId or not self.topType:
            return
        ver = self.dataCache.get(self.proxyId, {}).get('ver', 0)
        p = BigWorld.player()
        if needRefresh:
            p.cell.refreshTopHallOfFame(self.topType, ver, gametypes.ALL_LV_TOP_RANK_KEY, 0)
        else:
            p.base.getTopHallOfFame(self.topType, ver, gametypes.ALL_LV_TOP_RANK_KEY, 0)

    def getData(self):
        if not self.proxyId:
            return
        info = self.dataCache.get(self.proxyId, {})
        if not info:
            info = {'proxyId': self.proxyId}
        self.refreshView(info)
        self.queryData()

    def updateData(self, realInfo):
        proxyId = realInfo.get('proxyId', 0)
        self.dataCache[proxyId] = realInfo
        self.refreshView(realInfo)

    def handleClickListItem(self, e):
        if e.target.name == 'voteBtn':
            itemMc = e.currentTarget
            gbid = int(itemMc.data.get('gbid', 0))
            p = BigWorld.player()
            if gbid == p.gbId:
                p.showGameMsg(GMDD.data.CANNOT_TO_YOURSELF_SEND_GIFT, ())
            else:
                hostId = itemMc.data.get('hostId', 0)
                roleName = itemMc.data.get('roleName', '')
                giftId = HOFTD.data.get(self.topType, {}).get('giftId', 0)
                gameglobal.rds.ui.spaceGiftGiving.show(gbid, roleName, hostId=hostId, giftId=giftId)

    def refreshView(self, info):
        proxyId = info.get('proxyId', 0)
        if not self.widget or self.proxyId != proxyId:
            return
        giftId = HOFTD.data.get(self.topType, {}).get('giftId', 0)
        giftName = PZGD.data.get(giftId, {}).get('name', '')
        mainState = gameglobal.rds.ui.celebrityRank.getCurrentMainState()
        helpKeyDict = HOFCD.data.get('rankNameToHelpkey', {})
        if mainState == gametypes.CLIENT_HALL_OF_FAME_STAGE_VOTE:
            self.widget.myValueT.visible = True
            self.widget.voteTitle.visible = True
            self.widget.noneVoteTitle.visible = False
            self.widget.voteTitle.valueName.text = giftName
            self.widget.scrollWndList.itemRenderer = 'CelebrityVote_listItem'
            self.widget.voteTitle.help.helpKey = helpKeyDict[proxyId][1]
        else:
            self.widget.myValueT.visible = False
            self.widget.voteTitle.visible = False
            self.widget.noneVoteTitle.visible = True
            self.widget.scrollWndList.itemRenderer = 'CelebrityNoneVote_listItem'
            if mainState == gametypes.CLIENT_HALL_OF_FAME_STAGE_ENTER:
                if self.topType == gametypes.TOP_TYPE_HALL_OF_FAME_MINGSHI:
                    self.widget.noneVoteTitle.valueName.text = gameStrings.CELEBRITY_RANK_SHITU_VALUE
                elif self.topType == gametypes.TOP_TYPE_HALL_OF_FAME_GUIBAO:
                    self.widget.noneVoteTitle.valueName.text = gameStrings.CELEBRITY_RANK_GUIBAO_VALUE
                elif self.topType == gametypes.TOP_TYPE_HALL_OF_FAME_QIAOJIANG:
                    self.widget.noneVoteTitle.valueName.text = gameStrings.CELEBRITY_RANK_QIAOJIANG_VALUE
                else:
                    self.widget.noneVoteTitle.valueName.text = gameStrings.CELEBRITY_RANK_VOTE_VALUE
            elif mainState == gametypes.CLIENT_HALL_OF_FAME_STAGE_SHOW:
                self.widget.noneVoteTitle.valueName.text = giftName
            self.widget.noneVoteTitle.help.helpKey = helpKeyDict[proxyId][0]
        gameglobal.rds.ui.celebrityRank.refreshCommonView(self.widget, info)

    def handleClickAwardBtn(self):
        if not self.widget:
            return
        myRank = self.dataCache.get(self.proxyId, {}).get('myRank', 0)
        gameglobal.rds.ui.celebrityRankReward.show(self.topType, myRank)

    def handleClickRefreshBtn(self):
        self.queryData(needRefresh=True)

    def getVoteValue(self):
        if not self.widget:
            return
        p = BigWorld.player()
        p.cell.getMyHofRankValue(self.topType)

    def updateMyHofVoteValue(self, topType, value):
        if not self.widget:
            return
        if self.topTypeToValues[topType] != value:
            self.topTypeToValues[topType] = value
        self.widget.myValueT.text = gameStrings.HALL_OF_FAME_VOTE_VALUE % str(self.topTypeToValues[topType])
