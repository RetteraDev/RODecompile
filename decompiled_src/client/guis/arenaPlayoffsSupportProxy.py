#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/arenaPlayoffsSupportProxy.o
import BigWorld
import gametypes
import gameglobal
import uiConst
import utils
from guis import uiUtils
from guis import events
from uiProxy import UIProxy
from guis.asObject import ASObject
from callbackHelper import Functor
from gamestrings import gameStrings
from data import duel_config_data as DCD
from cdata import game_msg_def_data as GMDD
TOP_SHOW_NUM = 3
TEAM_ITEM_HEIGHT = 190
TEAM_ITEM_WIDTH = 170

class ArenaPlayoffsSupportProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ArenaPlayoffsSupportProxy, self).__init__(uiAdapter)
        self.widget = None
        self.rankData = {}
        self.teamDatas = {}
        self.selectLvKey = gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEY_60_69
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ARENA_PLAYOFFS_SUPPORT, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ARENA_PLAYOFFS_SUPPORT:
            self.widget = widget
            self.initSelectLvKey()
            self.queryServerData()
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ARENA_PLAYOFFS_SUPPORT)

    def initSelectLvKey(self):
        p = BigWorld.player()
        if p.isPlayoffs5V5():
            if p.lv <= 69:
                self.selectLvKey = gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEY_60_69
                self.widget.lvGroup.lvBtn0.selected = True
            else:
                self.widget.lvGroup.lvBtn1.selected = True
                self.selectLvKey = gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEY_70_79
            self.widget.lvGroup.visible = True
            self.widget.lvGroup.lvBtn0.data = gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEY_60_69
            self.widget.lvGroup.lvBtn1.data = gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEY_70_79
            self.widget.lvGroup.lvBtn0.addEventListener(events.BUTTON_CLICK, self.onLvBtnSelected)
            self.widget.lvGroup.lvBtn1.addEventListener(events.BUTTON_CLICK, self.onLvBtnSelected)
        elif p.isBalancePlayoffs():
            self.widget.lvGroup.visible = False
            self.selectLvKey = gametypes.CROSS_ARENA_PLAYOFFS_LV_KEY_BALANCE
        else:
            self.selectLvKey = gametypes.CROSS_ARENA_PLAYOFFS_LV_KEY_70_79

    def onLvBtnSelected(self, *args):
        e = ASObject(args[3][0])
        selectKey = e.currentTarget.data
        self.selectLvKey = selectKey
        self.queryTeamData(self.selectLvKey)
        self.refreshTeam()

    def show(self):
        if not gameglobal.rds.configData.get('enableArenaPlayoffsAid', False):
            return
        p = BigWorld.player()
        if not p.isPlayoffAidStateValid():
            BigWorld.player().showGameMsg(GMDD.data.COMMON_MSG, (gameStrings.ARENA_PLAYOFFS_SUPPORT_NOT_TIME,))
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ARENA_PLAYOFFS_SUPPORT)
        else:
            self.refreshInfo()

    def onGetServerRankData(self, data):
        self.rankData = data
        self.refreshRank()

    def onGetServerTeamData(self, data):
        lvKey = data.get('key', '')
        if lvKey:
            self.teamDatas[lvKey] = data
            self.refreshTeam()

    def queryServerData(self):
        self.queryRankData()
        self.queryTeamData(self.selectLvKey)

    def queryRankData(self):
        p = BigWorld.player()
        p.base.getTopArenaPlayoffsAid(self.rankData.get('version', 0))

    def queryTeamData(self, lvKey):
        p = BigWorld.player()
        p.cell.getTopArenaPlayffsTeamAid(self.teamDatas.get(lvKey, {}).get('version', 0), lvKey)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.teamList.column = 3
        self.widget.teamList.itemHeight = TEAM_ITEM_HEIGHT
        self.widget.teamList.itemWidth = TEAM_ITEM_WIDTH
        self.widget.teamList.itemRenderer = 'ArenaPlayoffsSupport_teamItem'
        self.widget.teamList.labelFunction = self.teamLabelFunction
        self.widget.teamList.dataArray = []
        self.widget.rankList.itemRenderer = 'ArenaPlayoffsSupport_rankItem'
        self.widget.rankList.labelFunction = self.rankItemLabelFunction
        self.widget.rankList.dataArray = []
        self.widget.rewardBtn.addEventListener(events.BUTTON_CLICK, self.onRewardBtnClick)
        self.widget.fullRankBtn.addEventListener(events.BUTTON_CLICK, self.onFullRankBtnClick)

    def memberSort(self, val1, val2):
        return cmp(val2[2], val1[2])

    def teamLabelFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.voteBtn.nuid = itemData.gbId
        itemMc.voteBtn.addEventListener(events.BUTTON_CLICK, self.onVoteBtnClik)
        itemMc.teamName.text = '%s-%s' % (itemData.roleName, utils.getServerName(itemData.fromHostId))
        itemMc.itemCount.text = itemData.value
        members = itemData.members
        members.sort(cmp=self.memberSort)
        for i in xrange(TOP_SHOW_NUM):
            topMc = itemMc.getChildByName('topName%d' % i)
            if i < len(members):
                topMc.visible = True
                topMc.text = '%s' % members[i][1]
            else:
                topMc.visible = False

    def rankItemLabelFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        self.setRankInfo(itemData.rank, itemMc)
        itemMc.roleName.text = '%s-%s' % (itemData.roleName, utils.getServerName(itemData.fromHostId))
        itemMc.itemCount.text = itemData.value
        p = BigWorld.player()
        photoBorderIcon = p.getPhotoBorderIcon(itemData.photoBorder, uiConst.PHOTO_BORDER_ICON_SIZE40)
        itemMc.headIcon.borderImg.fitSize = True
        itemMc.headIcon.borderImg.loadImage(photoBorderIcon)
        photo = itemData.photo
        if uiUtils.isDownloadImage(photo):
            itemMc.headIcon.icon.fitSize = True
            itemMc.headIcon.icon.imgType = uiConst.IMG_TYPE_NOS_FILE
            itemMc.headIcon.icon.serverId = itemData.fromHostId
            itemMc.headIcon.icon.url = photo
        else:
            itemMc.headIcon.icon.fitSize = True
            itemMc.headIcon.icon.loadImage(photo)

    def setRankInfo(self, rank, mc):
        if rank in (1, 2, 3):
            mc.top3Icon.visible = True
            mc.rankText.text = ''
            mc.top3Icon.gotoAndStop('top%d' % rank)
        else:
            mc.top3Icon.visible = False
            mc.rankText.text = rank

    def onFullRankBtnClick(self, *args):
        gameglobal.rds.ui.rankCommon.showRankCommon(gametypes.TOP_TYPE_ARENA_PLAYOFFS_PLAYER_AID_VALUE)

    def onVoteBtnClik(self, *args):
        e = ASObject(args[3][0])
        teamNUID = e.currentTarget.nuid
        lvKey = self.selectLvKey
        msg = gameStrings.ARENA_PLAYOFFS_SUPPORT_VOTE_TEXT
        p = BigWorld.player()
        voteItemIds = DCD.data.get('arenaPlayoffsAidItems', {}).keys()
        if voteItemIds:
            voteItemId = voteItemIds[0]
            itemNum = p.inv.countItemInPages(voteItemId, enableParentCheck=True)
            gameglobal.rds.ui.messageBox.showCounterMsgBox(msg, Functor(self.onConfirmVote, lvKey, teamNUID, voteItemId), title=gameStrings.ARENA_PLAYOFFS_SUPPORT_VOTE_TITLE, counterData=uiUtils.getGfxItemById(voteItemId), counterRange=(0, itemNum))

    def onConfirmVote(self, lvKey, teamNUID, voteItemId, cnt):
        p = BigWorld.player()
        if cnt <= 0:
            return
        p.cell.aidArenaPlayoffs(lvKey, long(teamNUID), voteItemId, cnt)

    def onRewardBtnClick(self, *args):
        gameglobal.rds.ui.generalReward.show(gametypes.GENERAL_REWARD_ARENA_PLAYOFFS_SUPPORT)

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshRank()
        self.refreshTeam()

    def refreshRank(self):
        if not self.widget:
            return
        self.calcRank()
        self.widget.rankList.dataArray = self.rankData.get('data', [])
        self.widget.rankList.validateNow()

    def calcRank(self):
        data = self.rankData.get('data', [])
        for i in xrange(len(data)):
            data[i]['rank'] = i + 1

    def refreshTeam(self):
        if not self.widget:
            return
        teamData = self.teamDatas.get(self.selectLvKey, {})
        self.widget.teamList.dataArray = teamData.get('data', [])
        self.widget.teamList.validateNow()

    def handelLvKeySelect(self, *args):
        e = ASObject(args[3][0])
        lvKey = e.currentTarget.lvKey
        self.selectLvKey = lvKey
        self.queryTeamData(lvKey)
        self.refreshTeam()

    def onArenaPlayoffsAidSucc(self, aidNum, teamName):
        teamData = self.teamDatas.get(self.selectLvKey, {})
        datas = teamData.get('data', [])
        for data in datas:
            if data.get('roleName', '') == teamName:
                data['value'] = data.get('value', 0) + aidNum

        if not self.widget:
            return
        self.widget.teamList.dataArray = datas
        self.widget.teamList.validateNow()
