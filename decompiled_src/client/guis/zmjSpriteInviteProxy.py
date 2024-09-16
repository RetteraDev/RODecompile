#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/zmjSpriteInviteProxy.o
import BigWorld
import gameglobal
import uiConst
import const
import events
import formula
import utils
from uiTabProxy import UITabProxy
from gamestrings import gameStrings
from guis.asObject import ASObject
from guis.asObject import MenuManager
from callbackHelper import Functor
from data import zmj_fuben_config_data as ZFCD
from cdata import game_msg_def_data as GMDD
TAB_INDEX_FRIEND = 0
TAB_INDEX_GUILD = 1

class ZmjSpriteInviteProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(ZmjSpriteInviteProxy, self).__init__(uiAdapter)
        self.tabType = UITabProxy.TAB_TYPE_CLS
        self.reset()
        self.inviteCDList = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_ZMJ_SPRITE_INVITE, self.hide)

    def reset(self):
        super(ZmjSpriteInviteProxy, self).reset()
        self.guildInfoDict = {}
        self.friendInfoDict = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ZMJ_SPRITE_INVITE:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        super(ZmjSpriteInviteProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ZMJ_SPRITE_INVITE)

    def _getTabList(self):
        return [{'tabIdx': TAB_INDEX_FRIEND,
          'tabName': 'tabBtn0',
          'view': 'ZmjSpriteInvite_DetailMc'}, {'tabIdx': TAB_INDEX_GUILD,
          'tabName': 'tabBtn1',
          'view': 'ZmjSpriteInvite_DetailMc'}]

    def show(self):
        if not gameglobal.rds.configData.get('enableZMJAssist', False):
            return
        if self.widget:
            self.widget.swapPanelToFront()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ZMJ_SPRITE_INVITE)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.helpIcon.helpKey = ZFCD.data.get('zmjSpriteInviteHelpKey', 0)
        self.initTabUI()
        self.widget.setTabIndex(self.showTabIndex)

    def onTabChanged(self, *args):
        super(ZmjSpriteInviteProxy, self).onTabChanged(*args)
        self.currentView.scrollWndList.itemRenderer = 'ZmjSpriteInvite_ScrollWndListItem'
        self.currentView.scrollWndList.dataArray = []
        self.currentView.scrollWndList.lableFunction = self.itemFunction
        self.currentView.scrollWndList.itemHeight = 37
        self.queryInfo()
        self.refreshInfo()

    def queryInfo(self):
        p = BigWorld.player()
        if self.currentTabIndex == TAB_INDEX_GUILD:
            p.base.queryZMJAssist(const.ZMJ_ASSIST_TYPE_GUILD)
        else:
            p.base.queryZMJAssist(const.ZMJ_ASSIST_TYPE_FRIEND)

    def setAssitInfo(self, qType, data):
        if qType == const.ZMJ_ASSIST_TYPE_FRIEND:
            self.friendInfoDict = {}
            for assitInfo in data:
                self.friendInfoDict[assitInfo[0]] = {'level': assitInfo[1],
                 'assistNum': assitInfo[2]}

        elif qType == const.ZMJ_ASSIST_TYPE_GUILD:
            self.guildInfoDict = {}
            for assitInfo in data:
                self.guildInfoDict[assitInfo[0]] = {'level': assitInfo[1],
                 'assistNum': assitInfo[2]}

        self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        if self.currentTabIndex == TAB_INDEX_GUILD:
            self.refreshGuildInfo()
        else:
            self.refreshFriendInfo()
        self.refreshLeftCount()

    def refreshLeftCount(self):
        if self.widget:
            p = BigWorld.player()
            leftCnt = max(ZFCD.data.get('applyAssistDayLimit', 0) - p.zmjData.get(const.ZMJ_FB_INFO_ASSIST_DAY_CNT, 0), 0)
            self.widget.remainTip.htmlText = gameStrings.ZMJ_SPRITE_INVITE_REMAIN_TXT % leftCnt

    def refreshFriendInfo(self):
        if not self.widget:
            return
        elif self.currentTabIndex != TAB_INDEX_FRIEND:
            return
        else:
            p = BigWorld.player()
            friends = p.friend
            if not friends:
                return
            friendsList = []
            for gbId, itemDetail in self.friendInfoDict.iteritems():
                friendVal = friends.get(gbId, None)
                if not friendVal:
                    continue
                friendsList.append({'gbId': gbId,
                 'school': friendVal.school,
                 'name': friendVal.name,
                 'level': itemDetail.get('level', 0),
                 'location': formula.whatAreaName(friendVal.spaceNo, friendVal.areaId),
                 'hasCnt': ZFCD.data.get('beApplyAssistDayLimit', 0) > itemDetail.get('assistNum', 0)})

            friendsList.sort(cmp=self.sort_invite)
            self.currentView.scrollWndList.dataArray = friendsList
            self.currentView.scrollWndList.validateNow()
            self.currentView.emptyHint.text = gameStrings.ZMJ_SPRITE_INVITE_FRIEND_EMPTY_TXT
            self.currentView.emptyHint.visible = len(friendsList) == 0
            return

    def refreshGuildInfo(self):
        if not self.widget:
            return
        elif self.currentTabIndex != TAB_INDEX_GUILD:
            return
        else:
            p = BigWorld.player()
            guild = p.guild
            if not guild:
                return
            guildList = []
            for gbId, itemDetail in self.guildInfoDict.iteritems():
                member = guild.member.get(gbId, None)
                if not member:
                    continue
                guildList.append({'gbId': gbId,
                 'school': member.school,
                 'name': member.role,
                 'level': itemDetail.get('level', 0),
                 'location': formula.whatAreaName(member.spaceNo, member.areaId),
                 'hasCnt': ZFCD.data.get('beApplyAssistDayLimit', 0) > itemDetail.get('assistNum', 0)})

            guildList.sort(cmp=self.sort_invite)
            self.currentView.scrollWndList.dataArray = guildList
            self.currentView.scrollWndList.validateNow()
            self.currentView.emptyHint.text = gameStrings.ZMJ_SPRITE_INVITE_GUILD_EMPTY_TXT
            self.currentView.emptyHint.visible = len(guildList) == 0
            return

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        if not itemData:
            itemMc.visible = False
            return
        itemMc.visible = True
        itemMc.overMc.visible = False
        itemMc.schoolIcon.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(itemData.school))
        itemMc.playerName.text = itemData.name
        itemMc.level.text = itemData.level
        itemMc.location.text = itemData.location
        if itemData.hasCnt:
            itemMc.noTimes.visible = False
            itemMc.inviteBtn.visible = True
            itemMc.inviteBtn.addEventListener(events.MOUSE_CLICK, self.handleClickInviteBtn, False, 0, True)
        else:
            itemMc.noTimes.visible = True
            itemMc.inviteBtn.visible = False
        gbId = long(itemData.gbId)
        itemMc.gbId = gbId
        if long(gbId) in self.inviteCDList.keys():
            itemMc.inviteBtn.disabled = True
            leftTime = self.inviteCDList[gbId] - utils.getNow()
            self.showItemCountDown(leftTime, itemMc)
        else:
            itemMc.inviteBtn.disabled = False
            itemMc.inviteBtn.label = gameStrings.ZMJ_SPRITE_INVITE_BTN_LABEL
        itemMc.addEventListener(events.MOUSE_ROLL_OVER, self.handleOverItem, False, 0, True)
        itemMc.addEventListener(events.MOUSE_ROLL_OUT, self.handleOutItem, False, 0, True)
        menuParam = {'roleName': itemData.name,
         'gbId': itemData.gbId}
        MenuManager.getInstance().registerMenuById(itemMc, uiConst.MENU_CHAT, menuParam)

    def handleClickInviteBtn(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget.parent
        gbId = long(itemMc.gbId)
        p = BigWorld.player()
        leftCnt = max(ZFCD.data.get('applyAssistDayLimit', 0) - p.zmjData.get(const.ZMJ_FB_INFO_ASSIST_DAY_CNT, 0), 0)
        if leftCnt == 0:
            p.showGameMsg(GMDD.data.ZMJ_APPLY_ASSIST_FAIL_SELF_NOT_HAS_NUM, ())
            return
        if self.currentTabIndex == TAB_INDEX_FRIEND:
            p.cell.applyZMJAssist(const.ZMJ_ASSIST_TYPE_FRIEND, gbId)
        elif self.currentTabIndex == TAB_INDEX_GUILD:
            p.cell.applyZMJAssist(const.ZMJ_ASSIST_TYPE_GUILD, gbId)
        self.inviteCDList[gbId] = utils.getNow() + 30
        itemMc.inviteBtn.disabled = True
        self.showItemCountDown(30, itemMc)

    def showItemCountDown(self, leftTime, item):
        gbId = long(item.gbId)
        if not self.widget:
            return
        if not item.inviteBtn:
            return
        if gbId in self.inviteCDList.keys() and leftTime > 0:
            leftTime -= 1
            item.inviteBtn.disabled = True
            item.inviteBtn.label = utils.formatDurationShortVersion(leftTime)
            BigWorld.callback(1, Functor(self.showItemCountDown, leftTime, item))
        elif leftTime <= 0:
            item.inviteBtn.disabled = False
            item.inviteBtn.label = gameStrings.ZMJ_SPRITE_INVITE_BTN_LABEL
            if gbId in self.inviteCDList.keys():
                del self.inviteCDList[gbId]

    def handleOverItem(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.overMc.visible = True

    def handleOutItem(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.overMc.visible = False

    def sort_invite(self, a, b):
        if a['hasCnt'] > b['hasCnt']:
            return -1
        if a['hasCnt'] < b['hasCnt']:
            return 1
        if a['level'] > b['level']:
            return -1
        if a['level'] < b['level']:
            return 1
        return 0
