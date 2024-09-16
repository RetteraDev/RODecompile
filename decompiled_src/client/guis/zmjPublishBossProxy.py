#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/zmjPublishBossProxy.o
import BigWorld
import gameglobal
import uiConst
import formula
from guis import events
from guis.asObject import ASObject
from uiProxy import UIProxy
from gamestrings import gameStrings
from data import zmj_fuben_config_data as ZFCD
import gametypes
FRIEND_TAB = 1
GUILD_TAB = 2

class ZmjPublishBossProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ZmjPublishBossProxy, self).__init__(uiAdapter)
        self.widget = None
        self.currentTab = FRIEND_TAB
        self.currBossInfo = None
        self.currBossId = 0
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ZMJ_PUBLISH_BOSS, self.hide)

    def reset(self):
        self.currentTab = FRIEND_TAB
        self.currBossInfo = None
        self.currBossId = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ZMJ_PUBLISH_BOSS:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ZMJ_PUBLISH_BOSS)

    def show(self, bossNUID):
        p = BigWorld.player()
        self.currBossId = bossNUID
        self.currBossInfo = p.zmjStarBoss.get(long(bossNUID), None)
        if not self.currBossInfo:
            self.hide()
            return
        else:
            if not self.widget:
                self.currentTab = FRIEND_TAB
                self.uiAdapter.loadWidget(uiConst.WIDGET_ZMJ_PUBLISH_BOSS)
                self.queryServerInfo(True)
            else:
                self.queryServerInfo(True)
                self.refreshInfo()
            return

    def queryServerInfo(self, queryAll = False):
        p = BigWorld.player()
        if queryAll:
            p.cell.requireZMJRecordInfo(gametypes.ZMJ_RECORD_TYPE_ALL)
        elif self.currentTab == FRIEND_TAB:
            p.cell.requireZMJRecordInfo(gametypes.ZMJ_RECORD_TYPE_FRIEND)
        else:
            p.cell.requireZMJRecordInfo(gametypes.ZMJ_RECORD_TYPE_GUILD_MEMBER)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.friendTab.addEventListener(events.BUTTON_CLICK, self.onTabBtnClick)
        self.widget.guildTab.addEventListener(events.BUTTON_CLICK, self.onTabBtnClick)
        self.widget.mainMc.scrollWndList.itemRenderer = 'ZmjPublishBoss_playerItem'
        self.widget.mainMc.scrollWndList.lableFunction = self.playerLabelFunc
        self.widget.mainMc.scrollWndList.dataArray = []

    def playerLabelFunc(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        if itemData.online:
            itemMc.gotoAndStop('online')
        else:
            itemMc.gotoAndStop('offline')
        itemMc.schoolIcon.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(itemData.school))
        itemMc.playerName.text = itemData.nameText
        itemMc.level.text = itemData.level
        itemMc.currPos.text = itemData.spaceText
        itemMc.publishBtn.gbId = itemData.gbId
        itemMc.publishBtn.addEventListener(events.BUTTON_CLICK, self.onPublishBtnClick)
        itemMc.notEnoughTime.visible = False
        itemMc.publishBtn.visible = False
        itemMc.published.visible = False
        if self.isPublished(long(itemData.gbId)):
            itemMc.published.visible = True
        elif self.getRemainPublishTime():
            itemMc.publishBtn.visible = True
        else:
            itemMc.notEnoughTime.visible = True

    def isPublished(self, gbId):
        if long(gbId) in self.currBossInfo.candidates:
            return True
        return False

    def getRemainPublishTime(self):
        publishedNum = len(self.currBossInfo.candidates)
        totalNum = ZFCD.data.get('starBossShareLimit', 0)
        return max(0, totalNum - publishedNum)

    def onTabBtnClick(self, *args):
        e = ASObject(args[3][0])
        btnName = e.currentTarget.name
        if btnName == 'friendTab':
            currentTab = FRIEND_TAB
        else:
            currentTab = GUILD_TAB
        if currentTab != self.currentTab:
            self.currentTab = currentTab
            self.queryServerInfo()
            self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        if p.guild:
            self.widget.guildTab.enabled = True
        else:
            self.widget.guildTab.enabled = False
        self.widget.friendTab.selected = self.currentTab == FRIEND_TAB
        self.widget.guildTab.selected = self.currentTab == GUILD_TAB
        self.widget.remainTip.htmlText = gameStrings.ZMJ_ACTIVITY_BOSS_PUBLISH_REMAIN_TIME % str(self.getRemainPublishTime())
        if self.currentTab == FRIEND_TAB:
            self.refreshFriendInfo()
        elif self.currentTab == GUILD_TAB:
            self.refreshGuildInfo()

    def sortFunc(self, a, b):
        return cmp(a.get('level', 0), b.get('level', 0))

    def refreshFriendInfo(self):
        self.widget.mainMc.scrollWndList.dataArray = self.getFriendList()
        if not self.widget.mainMc.scrollWndList.dataArray:
            starBossAppearLayer = ZFCD.data.get('starBossAppearLayer', 0)
            self.widget.emptyTip.text = gameStrings.ZMJ_ACTIVITY_BOSS_NO_ONLINE_FRIEND % starBossAppearLayer
            self.widget.emptyTip.visible = True
        else:
            self.widget.emptyTip.visible = False

    def refreshGuildInfo(self):
        self.widget.mainMc.scrollWndList.dataArray = self.getGuildMemberList()
        if not self.widget.mainMc.scrollWndList.dataArray:
            starBossAppearLayer = ZFCD.data.get('starBossAppearLayer', 0)
            self.widget.emptyTip.text = gameStrings.ZMJ_ACTIVITY_BOSS_NO_ONLINE_GUILD_MEMBER % starBossAppearLayer
            self.widget.emptyTip.visible = True
        else:
            self.widget.emptyTip.visible = False

    def createPlayerInfo(self, player):
        info = {'nameText': getattr(player, 'name', '') or getattr(player, 'role', ''),
         'school': player.school,
         'gbId': str(player.gbId),
         'spaceText': formula.whatAreaName(player.spaceNo, player.areaId)}
        return info

    def getFriendList(self):
        p = BigWorld.player()
        friendGbIds = p.friend.keys()
        friendList = []
        starBossAppearLayer = ZFCD.data.get('starBossAppearLayer', 0)
        for gbId in friendGbIds:
            fVal = p.friend.get(gbId)
            level = fVal.activityDict.get(gametypes.FRIEND_ACTIVITY_TYPE_ZMJ_MAX_STAR, 0)
            online = fVal.state in gametypes.FRIEND_VISIBLE_STATES
            if not fVal or not online:
                continue
            if level < starBossAppearLayer:
                continue
            memberInfo = self.createPlayerInfo(fVal)
            memberInfo['level'] = level
            memberInfo['online'] = online
            friendList.append(memberInfo)

        friendList.sort(cmp=self.sortFunc)
        return friendList

    def getGuildMemberList(self):
        p = BigWorld.player()
        guildGbIds = p.guild.member.keys()
        guildList = []
        starBossAppearLayer = ZFCD.data.get('starBossAppearLayer', 0)
        for gbId in guildGbIds:
            member = p.guild.member.get(gbId)
            level = member.activityDict.get(gametypes.FRIEND_ACTIVITY_TYPE_ZMJ_MAX_STAR, 0)
            if gbId == p.gbId or not member or not member.online:
                continue
            if level < starBossAppearLayer:
                continue
            memberInfo = self.createPlayerInfo(member)
            memberInfo['level'] = level
            memberInfo['online'] = (member.online,)
            guildList.append(memberInfo)

        guildList.sort(cmp=self.sortFunc)
        return guildList

    def onPublishBtnClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget.gbId
        p = BigWorld.player()
        p.cell.shareMyZMJStarBoss(long(self.currBossId), long(target))
