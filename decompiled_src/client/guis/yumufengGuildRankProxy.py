#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/yumufengGuildRankProxy.o
import BigWorld
import copy
import const
import utils
from gamestrings import gameStrings
import uiConst
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis import events
from data import guild_config_data as GCD
REFRESH_INTERVAL = 25

class YumufengGuildRankProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(YumufengGuildRankProxy, self).__init__(uiAdapter)
        self.widget = None
        self.data = {'ver': 0,
         'info': [],
         'lastWeekInfo': []}
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_YMF_GUILD_RANK, self.hide)

    def reset(self):
        self.selectedGuildNuid = -1
        self.lastSelected = None
        self.myGuildRank = -1
        self.lastRefreshTime = 0
        self.timer = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_YMF_GUILD_RANK:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_YMF_GUILD_RANK)
        BigWorld.cancelCallback(self.timer)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_YMF_GUILD_RANK)
        else:
            self.refreshInfo()

    def updateData(self, ver, info, lastWeekRankInfo):
        self.data['ver'] = ver
        self.data['info'] = info
        self.data['lastWeekInfo'] = []
        self.refreshInfo()

    def getNewRankInfo(self):
        p = BigWorld.player()
        if not self.data['ver']:
            p.cell.getTopGuildYMF(self.data['ver'])
        else:
            p.cell.refreshTopGuildYMFScore(self.data['ver'])

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.scrollWndList.itemRenderer = 'YumufengGuildRank_ListItem'
        self.widget.scrollWndList.labelFunction = self.labelFunction
        self.widget.txtDesc.text = GCD.data.get('ymfRankDescs', {}).get('desc', '')
        self.widget.refreshBtn.enabled = True
        self.widget.refreshBtn.label = gameStrings.YMF_GUILD_RANK_REFRESH_TXT

    def labelFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        if 0 < int(itemData.rank) < 4:
            itemMc.rankIcon.visible = True
            itemMc.rankIcon.gotoAndStop('rank%d' % int(itemData.rank))
        else:
            itemMc.rankIcon.visible = False
        itemMc.tf_rank.text = str(int(itemData.rank))
        itemMc.tf_name.text = itemData.guildName
        itemMc.tf_lv.text = str(itemData.memberCnt)
        itemMc.tf_rankData.text = str(int(itemData.contribute))
        itemMc.hit.addEventListener(events.MOUSE_CLICK, self.handleItemClick, False, 0, True)
        itemMc.guildNuid = int(itemData.guildNuid)
        itemMc.hit.alpha = 0
        itemMc.selected.visible = self.selectedGuildNuid == int(itemData.guildNuid)
        if itemMc.selected.visible:
            self.selectedGuildNuid = itemMc

    def getSortedData(self):
        p = BigWorld.player()
        infoList = copy.deepcopy(self.data['info'])
        infoList.sort(cmp=self.cmpInfoItem)
        dataList = []
        self.myGuildRank = -1
        for index, info in enumerate(infoList):
            data = {}
            data['rank'] = index + 1
            contribute, memberCnt, prosperity = info[2]
            data['guildName'] = info[1]
            data['memberCnt'] = memberCnt
            data['contribute'] = contribute
            data['guildNuid'] = info[0]
            if getattr(p, 'guild', None) and p.guild.nuid == info[0]:
                self.myGuildRank = index + 1
            dataList.append(data)

        return dataList

    def cmpInfoItem(self, a, b):
        contributeA, memberCntA, prosperityA = a[2]
        contributeB, memberCntB, prosperityB = b[2]
        if contributeA != contributeB:
            return cmp(contributeB, contributeA)
        if memberCntA != memberCntB:
            return cmp(memberCntB, memberCntA)
        return cmp(prosperityB, prosperityA)

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.scrollWndList.dataArray = self.getSortedData()
        if self.myGuildRank > 0:
            self.widget.txtTips0.text = GCD.data.get('ymfRankDescs', {}).get('rankDesc', '%d') % self.myGuildRank
        else:
            self.widget.txtTips0.text = GCD.data.get('ymfRankDescs', {}).get('noRankDesc', '%d')
        self.widget.txtTips1.text = GCD.data.get('ymfRankDescs', {}).get('secondDesc', '')

    def handleItemClick(self, *args):
        e = ASObject(args[3][0])
        guildNuid = int(e.currentTarget.parent.guildNuid)
        self.selectedGuildNuid = guildNuid
        if self.lastSelected:
            self.lastSelected.selected.visible = False
        e.currentTarget.parent.selected.visible = True
        self.lastSelected = e.currentTarget.parent

    def timerFun(self):
        leftTime = REFRESH_INTERVAL - (utils.getNow() - self.lastRefreshTime)
        if leftTime > 0:
            self.widget.refreshBtn.label = gameStrings.YMF_GUILD_RANK_REFRESH_CD_TXT % leftTime
        else:
            self.widget.refreshBtn.label = gameStrings.YMF_GUILD_RANK_REFRESH_TXT
            self.widget.refreshBtn.enabled = True
            return
        self.timer = BigWorld.callback(1, self.timerFun)

    def _onViewRewardsBtnClick(self, *args):
        self.uiAdapter.ranking.openRewardPanel(const.PROXY_KEY_TOP_GUILD_YMF, 0)

    def _onRefreshBtnClick(self, *args):
        if utils.getNow() - self.lastRefreshTime < REFRESH_INTERVAL:
            return
        self.widget.refreshBtn.enabled = False
        self.lastRefreshTime = utils.getNow()
        self.timerFun()
