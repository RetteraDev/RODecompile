#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/teamRankingListProxy.o
import BigWorld
import time
import gameglobal
import uiConst
import events
import const
import utils
import gametypes
from uiProxy import UIProxy
from asObject import ASObject
from gamestrings import gameStrings
from guis import rankCommonUtils
from guis import uiUtils
from data import wing_world_config_data as WWCD
RANKLIST_ITEM_CLS = 'TeamRankingList_rankList_item'

class TeamRankingListProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(TeamRankingListProxy, self).__init__(uiAdapter)
        self.widget = None
        self.data = None
        self.fbLv = 0
        self.finishTime = 0
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_TEAM_RANKINGLIST, self.hide)

    def reset(self):
        self.lastSelMc = None
        self.lastSelIndex = -1
        self.selfRank = 0
        self.fbLv = 0
        self.finishTime = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_TEAM_RANKINGLIST:
            self.widget = widget
            self.initUI()
            self.refreshTeamInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_TEAM_RANKINGLIST)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_TEAM_RANKINGLIST)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.teamTip.visible = False
        self.widget.rankingList.itemRenderer = RANKLIST_ITEM_CLS
        self.widget.rankingList.itemHeight = 31
        self.widget.rankingList.lableFunction = self.lableFunction
        self.widget.notice.text = WWCD.data.get('xinmoRankingListTip', '')
        self.widget.deadline.text = gameStrings.WING_WORLD_XINMO_RANK_DEADLINE % self.getDeadLine()
        self.widget.teamTip.closeBtn.addEventListener(events.MOUSE_CLICK, self.hideTeamDetailInfo, False, 0, True)
        self.widget.refreshBtn.addEventListener(events.MOUSE_CLICK, self.refreshTeamInfo, False, 0, True)
        self.widget.rankingBtn.addEventListener(events.MOUSE_CLICK, self.showRankInfo, False, 0, True)
        self.updateRewardSlot()

    def updateRewardSlot(self):
        data = rankCommonUtils.getCommonAwardInfo((gametypes.TOP_TYPE_WING_WORLD_XINMO_FB, 0, 0))
        rewardList = data['list']
        for i, info in enumerate(rewardList):
            rewardSlot = self.widget.getChildByName('rewardSlot%d' % i)
            rewardText = self.widget.getChildByName('rewardText%d' % i)
            itemId = info['item0']
            itemCount = info['itemNum0']
            itemInfo = uiUtils.getGfxItemById(itemId, itemCount)
            rewardSlot.fitSize = True
            rewardSlot.dragable = False
            rewardSlot.setItemSlotData(itemInfo)
            rewardText.text = info['rank']

    def getDeadLine(self):
        startTimeCrontabStr = WWCD.data.get('xinmoStartCrontab', None)
        nextTime = utils.getNextCrontabTime(startTimeCrontabStr)
        return time.strftime('%Y.%m.%d', time.localtime(nextTime))

    def onItemMouseClick(self, *args):
        itemMc = ASObject(args[3][0]).currentTarget
        self.showTeamDetailInfo(itemMc)

    def showTeamDetailInfo(self, itemMc):
        if self.lastSelMc:
            if self.lastSelMc.listIndex == self.lastSelIndex:
                self.lastSelMc.gotoAndStop('up')
        self.lastSelMc = itemMc
        self.lastSelIndex = itemMc.listIndex
        itemMc.gotoAndStop('select')
        infoList = self.data[1]
        data = infoList[itemMc.listIndex]
        teamMc = self.widget.teamTip
        gbIds = data[0]
        extraData = data[3]
        names = extraData.get(const.WING_WORLD_XINMO_FB_RANK_EXTRA_INDEX_NAMES, (0, 0, 0, 0, 0))
        schools = extraData.get(const.WING_WORLD_XINMO_FB_RANK_EXTRA_INDEX_SCHOOLS, (0, 0, 0, 0, 0))
        originHostId = extraData.get(const.WING_WORLD_XINMO_FB_RANK_EXTRA_INDEX_HOSTID, 0)
        leaderGbId = extraData.get(const.WING_WORLD_XINMO_FB_RANK_EXTRA_INDEX_TEAM_HEADER, 0)
        teamName = extraData.get(const.WING_WORLD_XINMO_FB_RANK_EXTRA_INDEX_TEAM_NAME, '')
        teamMc.visible = True
        teamMc.teamName.text = teamName
        for i in range(5):
            playerMc = getattr(teamMc, 'player%d' % i, None)
            playerMc.visible = False

        for i in range(len(gbIds)):
            playerMc = getattr(teamMc, 'player%d' % i, None)
            playerMc.visible = True
            playerMc.teamLeaderIcon.visible = leaderGbId == gbIds[i]
            playerMc.playerSchool.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(schools[i], 'yuxu'))
            playerMc.playerName.text = names[i]

    def onGetServerData(self, data):
        self.data = data
        infoList = data[1]
        infoList.sort(self.comp, reverse=True)
        dataArr = []
        for i, data in enumerate(infoList):
            dataArr.append(i)

        self.reset()
        if not self.widget:
            return
        self.widget.rankingList.dataArray = dataArr
        self.calcBestRank()
        self.showSelfInfo()

    def calcBestRank(self):
        infoList = self.data[1]
        p = BigWorld.player()
        for index, data in enumerate(infoList):
            gbIds = data[0]
            val = data[1]
            if p.gbId in gbIds:
                self.selfRank = index + 1
                self.fbLv, self.finishTime = val[0], -val[1]
                return

    def showSelfInfo(self):
        if not self.widget:
            return
        rankInfo1 = ''
        rankInfo2 = ''
        if self.fbLv and self.finishTime:
            rankInfo1 = gameStrings.WING_WORLD_XINMO_RANK_SELF_INFO_FOMATE % (gameStrings.WING_WORLD_XIMO_RANK_LIST[self.fbLv], self.formateTime(self.finishTime))
        else:
            rankInfo1 = gameStrings.WING_WORLD_XINMO_RANK_SELF_INFO_NO_INFO
        if self.selfRank:
            rankInfo2 = self.selfRank
        else:
            rankInfo2 = gameStrings.WING_WORLD_XINMO_RANK_SELF_INFO_NO_RANK
        self.widget.playerRankInfo.text = gameStrings.WING_WORLD_XINMO_RANK_SELF_INFO % (rankInfo1, rankInfo2)

    def comp(self, a, b):
        res = cmp(a[1], b[1])
        if res == 0:
            res = cmp(b[2], a[2])
        return res

    def hideTeamDetailInfo(self, *args):
        self.widget.teamTip.visible = False

    def showRankInfo(self, *args):
        if self.selfRank:
            pos = self.widget.rankingList.getIndexPosY(self.selfRank - 1)
            self.widget.rankingList.scrollTo(pos)
            self.widget.rankingList.validateNow()
            for item in self.widget.rankingList.items:
                if item.listIndex + 1 == self.selfRank:
                    self.showTeamDetailInfo(item)

    def lableFunction(self, *args):
        index = ASObject(args[3][0])
        item = ASObject(args[3][1])
        self.setTeamInfo(item, index)

    def setTeamInfo(self, item, index):
        item.listIndex = index
        if self.lastSelIndex == item.listIndex:
            self.lastSelMc = item
            item.gotoAndStop('select')
        else:
            item.gotoAndStop('up')
        self.setBtnInfo(item)
        item.addEventListener(events.MOUSE_CLICK, self.onItemMouseClick, False, 0, True)
        item.addEventListener(events.MOUSE_ROLL_OVER, self.onItemMouseOver, False, 0, True)
        item.addEventListener(events.MOUSE_ROLL_OUT, self.onItemMouseOut, False, 0, True)

    def setBtnInfo(self, itemMc):
        infoList = self.data[1]
        data = infoList[itemMc.listIndex]
        itemMc.teamRank.text = itemMc.listIndex + 1
        itemMc.teamName.text = data[3].get(const.WING_WORLD_XINMO_FB_RANK_EXTRA_INDEX_TEAM_NAME, '')
        itemMc.teamLevel.text = gameStrings.WING_WORLD_XIMO_RANK_LIST[data[1][0]]
        itemMc.teamTime.text = self.formateTime(-data[1][1])

    def onItemMouseOver(self, *args):
        itemMc = ASObject(args[3][0]).currentTarget
        if self.lastSelIndex == itemMc.listIndex:
            return
        itemMc.gotoAndStop('over')

    def onItemMouseOut(self, *args):
        itemMc = ASObject(args[3][0]).currentTarget
        if self.lastSelIndex == itemMc.listIndex:
            return
        itemMc.gotoAndStop('up')

    def formateTime(self, time):
        minute = int(time / 60)
        sec = time - minute * 60
        return '%02d:%02d' % (minute, sec)

    def refreshTeamInfo(self, *args):
        if not self.widget:
            return
        self.hideTeamDetailInfo()
        p = BigWorld.player()
        version = 0
        if self.data:
            version = self.data[0]
            if version:
                self.onGetServerData(self.data)
        self.showSelfInfo()
        p.base.getTopWingWorldXinMoFbRank(version)
