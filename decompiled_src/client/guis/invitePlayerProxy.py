#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/invitePlayerProxy.o
import BigWorld
import const
import gameglobal
import uiConst
import formula
import events
import utils
from uiProxy import UIProxy
from guis import menuManager
from guis import relationLabelUtils
from guis.asObject import MenuManager
from guis.asObject import ASObject
from gamestrings import gameStrings
from guis.teamGoalMenuHelper import TeamGoalMenuHelper
from cdata import game_msg_def_data as GMDD
from data import guild_config_data as GCD
TOTAL_LABEL_CNT = 3
STATE_NONE = 0
STATE_IN_TEAM = 1
STATE_NO_TIME = 2

class InvitePlayerProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(InvitePlayerProxy, self).__init__(uiAdapter)
        self.widget = None
        self.lastRequestTime = [0,
         0,
         0,
         0]
        self.data = [{},
         {},
         {},
         {}]
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_INVITE_PLAYER, self.hide)

    def reset(self):
        self.teamGoalMenu = None
        self.curData = {}
        self.invitedPlayers = []
        self.showTab = -1

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_INVITE_PLAYER:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_INVITE_PLAYER)

    def show(self, idx = 0):
        if not gameglobal.rds.configData.get('enableTeamInvite', True):
            BigWorld.player().showGameMsg(GMDD.data.SERVICE_TEMPORARY_UNAVAILABLE, ())
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_INVITE_PLAYER)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.initTeamGoal()
        self.initListProp()
        self.setTab(0)
        self.addEvent(events.EVENT_TEAM_GOAL_CHANGED, self.onTeamGoalChanged)
        self.addEvent(events.EVENT_CHANGE_GROUP_HEADER, self.onTeamHeaderChanged)
        self.widget.emptyHintTf.addEventListener(events.EVENT_TEXTLINK, self.handleTextLink, False, 0, True)
        self.widget.tab0.addEventListener(events.BUTTON_CLICK, self.handleTabBtnClick, False, 0, True)
        self.widget.tab1.addEventListener(events.BUTTON_CLICK, self.handleTabBtnClick, False, 0, True)
        self.widget.tab2.addEventListener(events.BUTTON_CLICK, self.handleTabBtnClick, False, 0, True)
        self.widget.tab3.addEventListener(events.BUTTON_CLICK, self.handleTabBtnClick, False, 0, True)

    def initTeamGoal(self):
        self.teamGoalMenu = TeamGoalMenuHelper(self.widget.goalTypeMenu, self.widget.goal1Menu, self.widget.goal2Menu)
        self.teamGoalMenu.initTeamGoal()
        self.widget.goalTypeMenu.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handleGoalChange, False, 0, True)
        self.widget.goal1Menu.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handleGoalChange, False, 0, True)
        self.widget.goal2Menu.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handleGoalChange, False, 0, True)

    def initListProp(self):
        self.widget.playerList.itemRenderer = 'InvitePlayer_PlayerItem'
        self.widget.playerList.lableFunction = self.itemLabelFunc

    def setTab(self, newTab):
        if not self.widget:
            return
        oldTab = self.showTab
        if oldTab == newTab:
            return
        oldTabBtn = getattr(self.widget, 'tab%d' % oldTab)
        if oldTabBtn:
            oldTabBtn.selected = False
        newTabBtn = getattr(self.widget, 'tab%d' % newTab)
        if newTabBtn:
            newTabBtn.selected = True
        self.widget.emptyHintTf.visible = False
        self.showTab = newTab
        self.curData = self.data[self.showTab]
        self.requestInviteListData() or self.refreshTabHintText()
        self.updateScrollList()

    def requestInviteListData(self):
        if not self.judgeCanRequestData():
            return False
        p = BigWorld.player()
        if self.showTab == const.GROUP_INVITE_LIST_RECOMMENDATION:
            p.cell.getGroupInviteListFromRecommendate()
        elif self.showTab == const.GROUP_INVITE_LIST_FRIEND:
            p.cell.getGroupInviteListFromFriend()
        elif self.showTab == const.GROUP_INVITE_LIST_GUILD:
            p.cell.getGroupInviteListFromGuild()
        elif self.showTab == const.GROUP_INVITE_LIST_INTERACTION:
            p.cell.getGroupInviteListFromInteract()
        return True

    def judgeCanRequestData(self):
        curTime = utils.getNow()
        oldRequestTime = self.lastRequestTime[self.showTab]
        intervalTime = curTime - oldRequestTime
        if intervalTime < const.REQUEST_INVITE_PLAYER_INTERVAL_TIME:
            return False
        else:
            self.lastRequestTime[self.showTab] = curTime
            return True

    def onSyncGroupInviteData(self, dataType, data):
        if not self.widget:
            return
        self.updateInviteData(dataType, data)
        self.updateScrollList()
        self.refreshTabHintText()

    def updateInviteData(self, dataType, data):
        if dataType == const.GROUP_INVITE_LIST_RECOMMENDATION:
            self.data[dataType] = {gbId:pInfo for gbId, pInfo in data.iteritems() if pInfo.get('restCnt', 0) != 0}
        else:
            self.data[dataType] = data
        self.curData = self.data[self.showTab]

    def updateScrollList(self, needReset = True):
        if not self.widget:
            return
        self.widget.playerList.dataArray = self.getCurSortKey()
        self.widget.playerList.validateNow()
        needReset and self.widget.playerList.scrollToHead()

    def refreshTabHintText(self):
        if not self.widget:
            return
        isEmpty = not bool(self.curData)
        self.widget.emptyHintTf.visible = isEmpty
        if not isEmpty:
            return
        if self.showTab == const.GROUP_INVITE_LIST_RECOMMENDATION:
            hintText = gameStrings.INVITE_TAB_EMPTY_DEFAULT_TEXT
        elif self.showTab == const.GROUP_INVITE_LIST_FRIEND:
            hintText = gameStrings.INVITE_TAB_FRIEND_EMPTY_TEXT
        elif self.showTab == const.GROUP_INVITE_LIST_GUILD:
            p = BigWorld.player()
            if p.guild:
                hintText = gameStrings.INVITE_TAB_EMPTY_DEFAULT_TEXT
            else:
                canJoinLv = p.lv >= GCD.data.get('joinLv', const.GUILD_JOIN_LV)
                if canJoinLv:
                    hintText = gameStrings.INVITE_TAB_GUILD_EMPTY_TEXT
                else:
                    hintText = gameStrings.INVITE_TAB_GUILD_EMPTY_LVLIMIT_TEXT % canJoinLv
        elif self.showTab == const.GROUP_INVITE_LIST_INTERACTION:
            hintText = gameStrings.INVITE_TAB_EMPTY_DEFAULT_TEXT
        else:
            hintText = ''
        self.widget.emptyHintTf.htmlText = hintText

    def getCurSortKey(self):
        key = self.curData.keys()
        if self.showTab != const.GROUP_INVITE_LIST_RECOMMENDATION:
            key.sort(key=lambda k: self.curData.get(k, {}).get('restCnt', 0), reverse=True)
        return key

    def itemLabelFunc(self, *args):
        gbId = long(args[3][0].GetString())
        item = ASObject(args[3][1])
        itemInfo = self.curData.get(gbId, {})
        self.updateItemIcon(item, itemInfo)
        self.updateItemText(item, itemInfo)
        self.updateItemLabel(item, gbId)
        self.updateItemFuncBtn(item, gbId, itemInfo)
        self.registerEvent(item, gbId, itemInfo)

    def updateItemIcon(self, item, info):
        school = info.get('school', const.SCHOOL_SHENTANG)
        schoolFrameName = uiConst.SCHOOL_FRAME_DESC.get(school)
        item.jobIcon.gotoAndStop(schoolFrameName)
        p = BigWorld.player()
        photo = info.get('photo')
        item.playerIcon.setContentUnSee()
        item.playerIcon.fitSize = True
        if not photo:
            sex = info.get('sex', const.SEX_MALE)
            photo = p.friend.getDefaultPhoto(school, sex)
            item.playerIcon.loadImage(photo)
        else:
            item.playerIcon.imgType = uiConst.IMG_TYPE_NOS_FILE
            item.playerIcon.url = photo

    def updateItemText(self, item, info):
        item.lvTf.text = 'Lv.%d' % info.get('level', 0)
        item.nameTf.text = info.get('roleName')
        item.mapTf.text = self.getMapName(info)
        item.stateTf.visible = info.get('restCnt', 0) == 0 and TeamGoalMenuHelper.hasGoal()

    def updateItemLabel(self, item, gbId):
        labelFrameNames = relationLabelUtils.getValidLabelsName(gbId)
        labelCnt = len(labelFrameNames)
        for i in xrange(uiConst.PLAYER_ITEM_MAX_LABEL):
            label = getattr(item.labelMc, 'label%d' % i)
            if i < labelCnt:
                label.gotoAndStop(labelFrameNames[i])
                label.visible = True
            else:
                label.visible = False

    def updateItemFuncBtn(self, item, gbId, info):
        funcBtn = item.funcBtn
        if self.isInvited(gbId):
            funcBtn.label = gameStrings.INVITED
            funcBtn.enabled = False
        else:
            funcBtn.label = gameStrings.INVITE
            funcBtn.enabled = self.canInvite(info.get('state', 0))
        funcBtn.mouseEnabled = True

    def registerEvent(self, item, gbId, info):
        menuParam = {'roleName': info.get('roleName'),
         'gbId': gbId}
        MenuManager.getInstance().registerMenuById(item, uiConst.MENU_CHAT, menuParam)
        item.funcBtn.addEventListener(events.BUTTON_CLICK, self.handleClickFuncBtn, False, 0, True)
        item.funcBtn.addEventListener(events.MOUSE_CLICK, self.handleStopEvent, False, 0, True)

    def getMapName(self, info):
        spaceNo = info.get('spaceNo', 0)
        position = tuple(info.get('position', (0, 0, 0)))
        chunckName = BigWorld.ChunkInfoAt(position)
        return formula.whatLocationName(spaceNo, chunckName)

    def canInvite(self, state):
        return state == 0 or not TeamGoalMenuHelper.hasGoal()

    def setInvited(self, gbId):
        self.invitedPlayers.append(gbId)

    def isInvited(self, gbId):
        return gbId in self.invitedPlayers

    def getItemGbId(self, item):
        return long(self.widget.playerList.dataArray[item.index])

    def invitePlayer(self, gbId):
        p = BigWorld.player()
        roleName = self.curData.get(gbId, {}).get('roleName')
        menuTarget = menuManager.getInstance().menuTarget
        menuTarget.apply(roleName=roleName)
        if menuTarget.canInviteTeam(p):
            menuManager.getInstance().inviteTeam()

    def handleGoalChange(self, *args):
        p = BigWorld.player()
        info = self.teamGoalMenu.updateTeamGoalInfo()
        p.setGroupDetails(info)

    def refreshTeamGoal(self):
        goalType = self.teamGoalMenu.getTeamGoalType()
        goal1Idx, goal2Idx, _ = self.teamGoalMenu.getTeamGoalMenuIdx(goalType)
        self.teamGoalMenu.refreshTeamGoal(goalType, goal1Idx, goal2Idx)
        self.widget.playerList.validateNow()

    def handleClickFuncBtn(self, *args):
        e = ASObject(args[3][0])
        funcBtn = e.currentTarget
        funcBtn.enabled = False
        funcBtn.mouseEnabled = True
        funcBtn.label = gameStrings.INVITED
        item = funcBtn.parent
        gbId = self.getItemGbId(item)
        self.invitePlayer(gbId)
        self.setInvited(gbId)

    def handleStopEvent(self, *args):
        e = ASObject(args[3][0])
        e.stopPropagation()

    def handleTabBtnClick(self, *args):
        e = ASObject(args[3][0])
        tabBtnName = e.currentTarget.name
        selTab = int(tabBtnName[-1])
        if self.showTab != selTab:
            self.setTab(selTab)

    def handleTextLink(self, *args):
        p = BigWorld.player()
        if self.showTab == const.GROUP_INVITE_LIST_GUILD:
            if not p.guild:
                gameglobal.rds.ui.guildQuickJoin.show()
        elif self.showTab == const.GROUP_INVITE_LIST_FRIEND:
            gameglobal.rds.ui.recommendSearchFriend.show()

    def onTeamGoalChanged(self):
        if not self.widget:
            return
        if self.teamGoalMenu:
            goalType = self.teamGoalMenu.getTeamGoalType()
            goal1Idx, goal2Idx, _ = self.teamGoalMenu.getTeamGoalMenuIdx(goalType)
            self.teamGoalMenu.refreshTeamGoal(goalType, goal1Idx, goal2Idx)
        self.widget.playerList.validateNow()
        if TeamGoalMenuHelper.hasGoal():
            ret = self.requestInviteListData()
            if not ret:
                BigWorld.player().showGameMsg(GMDD.data.REQUEST_INVITE_DATA_FREQUENT, ())

    def onTeamHeaderChanged(self):
        if not self.widget:
            return
        self.teamGoalMenu.refreshMenuEnable()
