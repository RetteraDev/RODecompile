#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/memberDetailsV2Proxy.o
import BigWorld
import gameglobal
import events
import const
import utils
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis import uiConst
from guis import uiUtils
from guis import menuManager
from guis.asObject import MenuManager
from guis.asObject import ASUtils
from guis.asObject import ASObject
from guis.asObject import TipManager
from guis import groupDetailFactory
from guis.teamGoalMenuHelper import TeamGoalMenuHelper
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD
MENU_OFFSET_X = 15
MENU_OFFSET_Y = 2
ASSIGN_RULES = [{'label': gameStrings.ASSIGN_RULE_FREE},
 {'label': gameStrings.ASSIGN_RULE_DICE_JOB},
 {'label': gameStrings.ASSIGN_RULE_DICE},
 {'label': gameStrings.ASSIGN_RULE_HEADER},
 {'label': gameStrings.ASSIGN_RULE_AUCTION}]
ASSIGNRULES_MENUIDX = (0, 2, 3, 4, 1)
ASSIGN_RULE_TIPS = [gameStrings.ASSIGN_RULE_FREE_TIPS,
 gameStrings.ASSIGN_RULE_DICE_JOB_TIPS,
 gameStrings.ASSIGN_RULE_DICE_TIPS,
 gameStrings.ASSIGN_RULE_HEADER_TIPS,
 gameStrings.ASSIGN_RULE_AUCTION_TIPS]
ASSIGN_QUALITYS = [{'label': gameStrings.ASSIGN_QUALITY_6},
 {'label': gameStrings.ASSIGN_QUALITY_5},
 {'label': gameStrings.ASSIGN_QUALITY_4},
 {'label': gameStrings.ASSIGN_QUALITY_3},
 {'label': gameStrings.ASSIGN_QUALITY_2},
 {'label': gameStrings.ASSIGN_QUALITY_1},
 {'label': gameStrings.ASSIGN_QUALITY_0}]
DEFAULT_FONT_SIZE = 14
MAP_TF_MAX_WIDTH = 165

class MemberDetailsV2Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MemberDetailsV2Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.groupDetailFactory = groupDetailFactory.getInstance()
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MEMBERDETAILS_V2, self.hide)

    def reset(self):
        self.hoverItem = None
        self.teamGoalMenu = None
        self.defaultGoal = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MEMBERDETAILS_V2:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MEMBERDETAILS_V2)

    def show(self, defaultGoal = None):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_MEMBERDETAILS_V2)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.teamName.text = utils.getTeamName()
        self.addEvent(events.EVENT_TEAM_GOAL_CHANGED, self.onTeamGoalChanged)
        self.addEvent(events.EVENT_CHANGE_GROUP_HEADER, self.onTeamHeaderChanged)
        self.initTeamGoal()
        self.initAssignMode()
        self.refreshAssignMode()
        self.refreshMembers()
        self.refreshHelpInfo()
        self.refreshButtonShow()
        self.registerMenu()

    def initTeamGoal(self):
        self.teamGoalMenu = TeamGoalMenuHelper(self.widget.goalTypeMenu, self.widget.goal1Menu, self.widget.goal2Menu)
        self.teamGoalMenu.initTeamGoal()
        self.defaultGoal and self.setDefaultTeamGoal(self.defaultGoal)
        self.widget.goalTypeMenu.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handleGoalChange, False, 0, True)
        self.widget.goal1Menu.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handleGoalChange, False, 0, True)
        self.widget.goal2Menu.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handleGoalChange, False, 0, True)

    def initAssignMode(self):
        assignRuleMc = self.widget.assignRule
        assignQuality = self.widget.assignQuality
        ASUtils.setDropdownMenuData(assignRuleMc, ASSIGN_RULES)
        ASUtils.setDropdownMenuData(assignQuality, ASSIGN_QUALITYS)
        assignRuleMc.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handleAssignChange, False, 0, True)
        assignQuality.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handleAssignChange, False, 0, True)
        self.refreshAssignEnable()
        self.refreshAssignMode()

    def refreshAssignEnable(self):
        if not self.widget:
            return
        isLeader = BigWorld.player().isTeamLeader()
        self.widget.assignRule.enabled = isLeader
        self.widget.assignQuality.enabled = isLeader

    def refreshAssignMode(self):
        if not self.widget:
            return
        assignRuleMc = self.widget.assignRule
        assignQuality = self.widget.assignQuality
        p = BigWorld.player()
        if p.groupAssignWay in const.GROUP_ASSIGN_WAY:
            ruleMenuIdx = ASSIGNRULES_MENUIDX[p.groupAssignWay]
        else:
            ruleMenuIdx = 0
        TipManager.addTip(assignRuleMc, ASSIGN_RULE_TIPS[ruleMenuIdx])
        assignRuleMc.selectedIndex = ruleMenuIdx
        assignQuality.selectedIndex = const.GROUP_ASSIGN_QUALITY[p.groupAssignQuality]
        assignRuleMc.validateNow()
        assignQuality.validateNow()

    def refreshMembers(self):
        if not self.widget:
            return
        p = BigWorld.player()
        memberCanvas = self.widget.memberCanvas
        memberIdx = 0
        for gbId, info in p._getSortedMembers():
            school = info.get('school')
            if not p._checkValidSchool(school):
                continue
            if memberIdx >= const.TEAM_MAX_NUMBER:
                return
            item = getattr(memberCanvas, 'i%d' % memberIdx)
            item.gbId = gbId
            item.roleName = info.get('roleName')
            if info['isOn']:
                item.gotoAndStop('online')
                item.mapName.text = gameglobal.rds.ui.team._getMapNameByGbId(gbId)
            else:
                item.gotoAndStop('offline')
                item.mapName.text = gameStrings.TEAM_MEMBER_OFFLINE
            ASUtils.autoSizeWithFont(item.mapName, DEFAULT_FONT_SIZE, MAP_TF_MAX_WIDTH)
            item.jobIcon.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(school))
            item.playerName.text = info.get('roleName')
            item.playerLv.text = gameStrings.TEAM_MEMBER_LV % info.get('level', 1)
            item.leaderIcon.visible = p.headerGbId == gbId
            item.changeLeaderBtn.visible = self.hoverItem == item and self.checkCanChangeLeader(gbId)
            item.delMemberBtn.visible = self.hoverItem == item and self.checkCanDelMember(gbId)
            item.overBg.visible = self.hoverItem == item
            item.visible = True
            memberIdx += 1
            item.addEventListener(events.MOUSE_ROLL_OVER, self.handleRollOver, False, 0, True)
            item.addEventListener(events.MOUSE_ROLL_OUT, self.handleRollOut, False, 0, True)
            item.changeLeaderBtn.addEventListener(events.BUTTON_CLICK, self.handleChangeLeader, False, 0, True)
            item.delMemberBtn.addEventListener(events.BUTTON_CLICK, self.handleDeleteItem, False, 0, True)

        for idx in xrange(memberIdx, const.TEAM_MAX_NUMBER):
            item = getattr(memberCanvas, 'i%d' % idx)
            item.visible = False

        self.widget.invitePlayerBtn.enabled = self.checkCanInvitePlayers()
        self.widget.leaveBtn.enabled = self.checkCanLeaveTeam()

    def checkCanInvitePlayers(self):
        p = BigWorld.player()
        if p.isInFullTeam():
            return False
        if p.isInPUBG():
            return False
        return True

    def checkCanLeaveTeam(self):
        p = BigWorld.player()
        if p.isInPUBG():
            return False
        return True

    def checkCanDelMember(self, gbId):
        p = BigWorld.player()
        if p.isInPUBG():
            return False
        if not p.isTeamLeader():
            return False
        if gbId == p.headerGbId:
            return False
        return True

    def checkCanChangeLeader(self, gbId):
        p = BigWorld.player()
        if p.isInPUBG():
            return False
        if not p.isTeamLeader():
            return False
        if gbId == p.headerGbId:
            return False
        return True

    def checkCanUseShareMenu(self, shareMenuBtnMc):
        p = BigWorld.player()
        isCloseTeamGoal = TeamGoalMenuHelper.isNeedCloseTeamGoal()
        if isCloseTeamGoal:
            return False
        if p.isInPUBG():
            return False
        if not uiUtils.checkShareTeamLvLimit():
            shareMenuBtnMc.mouseEnabled = True
            tipStr = uiUtils.getTextFromGMD(GMDD.data.TEAM_INFO_LV_LIMIT) % SCD.data.get('teamInfoUseLv', 20)
            TipManager.addTip(shareMenuBtnMc, tipStr)
            return False
        return True

    def checkCanChangeTeamInfo(self):
        p = BigWorld.player()
        isCloseTeamGoal = TeamGoalMenuHelper.isNeedCloseTeamGoal()
        if isCloseTeamGoal:
            return False
        if p.isInPUBG():
            return False
        return True

    def checkUseLeaderMenu(self):
        p = BigWorld.player()
        if p.isInPUBG():
            return False
        return True

    def refreshHelpInfo(self):
        self.widget.helpMc.visible = False

    def refreshButtonShow(self):
        if not self.widget:
            return
        isLeader = BigWorld.player().isTeamLeader()
        self.widget.changeTeamInfoBtn.visible = isLeader
        self.widget.leaderMenuBtn.visible = isLeader
        self.widget.shareMenuBtn.visible = isLeader
        self.widget.changeTeamInfoBtn.enabled = self.checkCanChangeTeamInfo()
        self.widget.leaderMenuBtn.enabled = self.checkUseLeaderMenu()
        self.widget.shareMenuBtn.enabled = self.checkCanUseShareMenu(self.widget.shareMenuBtn)

    def registerMenu(self):
        leaderMenuOffsetPos = [MENU_OFFSET_X, self.widget.leaderMenuBtn.height + MENU_OFFSET_Y]
        MenuManager.getInstance().registerMenuById(self.widget.leaderMenuBtn, uiConst.MENU_LEADER_CMD, {}, events.LEFT_BUTTON, leaderMenuOffsetPos)
        shareMenuOffsetPos = [MENU_OFFSET_X, self.widget.shareMenuBtn.height + MENU_OFFSET_Y]
        MenuManager.getInstance().registerMenuById(self.widget.shareMenuBtn, uiConst.MENU_LEADER_SHARETEAM, {}, events.LEFT_BUTTON, shareMenuOffsetPos)

    def setDefaultTeamGoal(self, defaultGoal):
        if not self.widget:
            self.defaultGoal = defaultGoal
            return
        goalType = const.GROUP_GOAL_RELAXATION
        defaultLabelId = defaultGoal.get('labelId', 0)
        goal1Idx = const.GROUP_GOAL_DEFAULT
        goal2Idx = const.GROUP_GOAL_DEFAULT
        for type, data in groupDetailFactory.getActAvlData().items():
            for idx, labelId in enumerate(data):
                if labelId == defaultLabelId:
                    goal1Idx = type
                    goal2Idx = idx + 1

        self.teamGoalMenu.refreshTeamGoal(goalType, goal1Idx, goal2Idx)
        info = self.teamGoalMenu.updateTeamGoalInfo()
        p = BigWorld.player()
        if p.isInTeamOrGroup():
            p.setGroupDetails(info)

    def handleGoalChange(self, *args):
        info = self.teamGoalMenu.updateTeamGoalInfo()
        BigWorld.player().setGroupDetails(info)

    def handleRollOver(self, *args):
        e = ASObject(args[3][0])
        item = e.currentTarget
        p = BigWorld.player()
        item.overBg.visible = True
        item.changeLeaderBtn.visible = self.checkCanChangeLeader(long(item.gbId))
        item.delMemberBtn.visible = self.checkCanDelMember(long(item.gbId))
        self.hoverItem = item

    def handleRollOut(self, *args):
        e = ASObject(args[3][0])
        item = e.currentTarget
        item.overBg.visible = False
        item.changeLeaderBtn.visible = False
        item.delMemberBtn.visible = False
        self.hoverItem = None

    def handleChangeLeader(self, *args):
        e = ASObject(args[3][0])
        item = e.currentTarget.parent
        menuManager.getInstance().menuTarget.apply(gbId=long(item.gbId))
        menuManager.getInstance().changeTeamLeader()

    def handleDeleteItem(self, *args):
        e = ASObject(args[3][0])
        item = e.currentTarget.parent
        menuManager.getInstance().menuTarget.apply(item.roleName, gbId=long(item.gbId))
        menuManager.getInstance().kickTeam()

    def handleAssignChange(self, *args):
        selRuleMenuIdx = self.widget.assignRule.selectedIndex
        selAssignRule = ASSIGNRULES_MENUIDX.index(selRuleMenuIdx)
        selQualityMenuIdx = self.widget.assignQuality.selectedIndex
        selQualityRule = const.GROUP_ASSIGN_QUALITY.index(selQualityMenuIdx)
        BigWorld.player().cell.setGroupAssign(selAssignRule, selQualityRule)

    def _onChangeTeamInfoBtnClick(self, e):
        gameglobal.rds.ui.createTeamV2.show()

    def _onLeaveBtnClick(self, e):
        menuManager.getInstance().leaveTeam()

    def _onInvitePlayerBtnClick(self, e):
        gameglobal.rds.ui.invitePlayer.show()

    def onTeamGoalChanged(self):
        if not self.widget:
            return
        else:
            if self.teamGoalMenu:
                goalType = self.teamGoalMenu.getTeamGoalType()
                goal1Idx, goal2Idx, _ = self.teamGoalMenu.getTeamGoalMenuIdx(goalType)
                self.teamGoalMenu.refreshTeamGoal(goalType, goal1Idx, goal2Idx)
            self.widget.teamName.text = utils.getTeamName()
            if self.defaultGoal:
                msg = gameglobal.rds.ui.team.getShareTeamInfoMsg()
                BigWorld.player().cell.chatToGroupInfo(msg)
                self.defaultGoal = None
            return

    def onTeamHeaderChanged(self):
        if not self.widget:
            return
        self.teamGoalMenu.refreshMenuEnable()
        self.refreshButtonShow()
        self.refreshAssignEnable()

    def isShow(self):
        return bool(self.widget)

    def changeUIVisible(self):
        if self.isShow():
            self.hide()
        else:
            self.show()
