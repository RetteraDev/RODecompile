#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/teamGoalMenuHelper.o
import BigWorld
import events
import const
import uiConst
import utils
from guis import groupDetailFactory
from guis.asObject import ASUtils
from guis.asObject import ASObject
from cdata import group_fb_menu_data as GFMD
from data import fb_data as FD
from data import group_label_data as GLD
groupDetailIns = groupDetailFactory.getInstance()

class TeamGoalMenuHelper(object):
    hotTagList = groupDetailIns.goalIns[const.GROUP_HOT_TAGS].hotTagItems

    def __init__(self, goalTypeMenu, goal1Menu, goal2Menu):
        self.goalTypeMenu = goalTypeMenu
        self.goal1Menu = goal1Menu
        self.goal2Menu = goal2Menu

    def destroy(self):
        self.goalTypeMenu = None
        self.goal1Menu = None
        self.goal2Menu = None

    def initTeamGoal(self):
        self.refreshMenuEnable()
        ASUtils.setDropdownMenuData(self.goalTypeMenu, uiConst.TEAMGOAL_TYPE)
        self.goalTypeMenu.menuRowCount = len(uiConst.TEAMGOAL_TYPE)
        self.goalTypeMenu.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handleGoalChange, False, 0, True)
        self.goal1Menu.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handleGoalChange, False, 0, True)
        self.goal2Menu.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handleGoalChange, False, 0, True)
        goalType = self.getTeamGoalType()
        if self.isNeedCloseTeamGoal():
            self.goalTypeMenu.selectedIndex = 0
            self.resetGoalMenu(self.goal1Menu)
            self.resetGoalMenu(self.goal2Menu)
        else:
            goal1Idx, goal2Idx, _ = self.getTeamGoalMenuIdx(goalType)
            self.refreshTeamGoal(goalType, goal1Idx, goal2Idx)

    @staticmethod
    def isNeedCloseTeamGoal():
        p = BigWorld.player()
        if p.inFubenTypes(const.FB_TYPE_ARENA):
            return True
        elif p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            return True
        elif p._isSoul():
            return True
        elif not getattr(p, 'detailInfo', {}):
            return True
        else:
            return False

    def refreshMenuEnable(self):
        p = BigWorld.player()
        isLeader = p.isTeamLeader()
        extra = self.isNeedCloseTeamGoal()
        self.goalTypeMenu.enabled = isLeader and not extra
        self.goal1Menu.enabled = isLeader and not extra
        self.goal2Menu.enabled = isLeader and not extra

    def refreshTeamGoal(self, goalType, goal1Idx, goal2Idx):
        dropDownMenuInfo = groupDetailIns.getDropDownMenuInfoV2(goalType)
        self.goalTypeMenu.selectedIndex = self.getMenuIdxByGoalType(goalType)
        if goalType == const.GROUP_GOAL_DEFAULT:
            self.resetGoalMenu(self.goal1Menu)
            self.resetGoalMenu(self.goal2Menu)
            return
        goal1MenuData = self.genGoal1MenuData(dropDownMenuInfo)
        self.refreshGoal1Menu(goal1Idx, goal1MenuData)
        goal2MenuData = self.genGoal2MenuDataByGoal1(dropDownMenuInfo, goal1Idx)
        self.refreshGoal2Menu(goal2Idx, goal2MenuData)

    @staticmethod
    def getTeamGoalType():
        p = BigWorld.player()
        if hasattr(p, 'detailInfo') and p.groupNUID > 0:
            ret = p.detailInfo.get('goal', 0)
        else:
            ret = const.GROUP_GOAL_DEFAULT
        if ret not in uiConst.MENU_GOAL_TYPE_LIST:
            ret = const.GROUP_GOAL_DEFAULT
        return ret

    @staticmethod
    def getMenuIdxByGoalType(goalType):
        if goalType == const.GROUP_HOT_TAGS:
            goalType = const.GROUP_GOAL_RELAXATION
        if goalType in uiConst.MENU_GOAL_TYPE_LIST:
            return uiConst.MENU_GOAL_TYPE_LIST.index(goalType)
        return 0

    @staticmethod
    def getGoalTypeByMenuIdx(menuIdx):
        return uiConst.MENU_GOAL_TYPE_LIST[menuIdx]

    def resetGoalMenu(self, goalMenuMc):
        goalMenuMc.selectedIndex = 0
        goalMenuMc.visible = False

    def getTeamGoalMenuIdx(self, goalType):
        return groupDetailIns.dropMenuVal2Index(goalType)

    def genGoal1MenuData(self, dropDownMenuInfo):
        return [ {'label': goal.get('keyName')} for goal in dropDownMenuInfo ]

    def genGoal2MenuDataByGoal1(self, dropDownMenuInfo, goal1):
        goal2DetailsData = dropDownMenuInfo[goal1]['data'] if goal1 < len(dropDownMenuInfo) else {}
        goal2MenuData = [ {'label': goal.get('keyName', '')} for goal in goal2DetailsData ]
        return goal2MenuData

    def getMenuFbLvLimit(self, fIndex, sIndex, tIndex = const.GROUP_GOAL_DEFAULT):
        if fIndex == 0 or sIndex == 0:
            return (const.MIN_CURRENT_LEVEL, const.MAX_CURRENT_LEVEL)
        dropDownMenuInfo = groupDetailIns.getDropDownMenuInfoV2(const.GROUP_GOAL_FB)
        fData = dropDownMenuInfo[fIndex]
        fKey = fData['key']
        sData = fData['data'][sIndex]
        sKey = sData['key']
        tData = sData['data'][tIndex]
        tKey = tData['key']
        fbNo = GFMD.data.get(fKey, {}).get(sKey, {}).get(tKey, {}).get('fbNo', 0)
        if fbNo:
            lvMin = FD.data.get(fbNo, {}).get('lvMin', 1)
            lvMax = FD.data.get(fbNo, {}).get('lvMax', const.MAX_CURRENT_LEVEL)
        else:
            lvMin = const.MIN_CURRENT_LEVEL
            lvMax = const.MAX_CURRENT_LEVEL
        return (lvMin, lvMax)

    def refreshGoal1Menu(self, goal1Idx, goal1MenuData):
        if len(goal1MenuData) == 0:
            self.resetGoalMenu(self.goal1Menu)
            self.resetGoalMenu(self.goal2Menu)
            return
        ASUtils.setDropdownMenuData(self.goal1Menu, goal1MenuData)
        self.goal1Menu.menuRowCount = len(goal1MenuData)
        self.goal1Menu.selectedIndex = goal1Idx
        self.goal1Menu.visible = True

    def refreshGoal2Menu(self, goal2Idx, goal2MenuData):
        if len(goal2MenuData) == 0:
            self.resetGoalMenu(self.goal2Menu)
            return
        ASUtils.setDropdownMenuData(self.goal2Menu, goal2MenuData)
        self.goal2Menu.menuRowCount = len(goal2MenuData)
        self.goal2Menu.selectedIndex = goal2Idx
        self.goal2Menu.visible = True

    def updateTeamGoalInfo(self, extraInfo = {}):
        p = BigWorld.player()
        lvMinDefault, lvMaxDefault = self.getGoalLvLimit()
        if not extraInfo and hasattr(p, 'detailInfo'):
            extraInfo = p.detailInfo
            extraInfo['lvMin'] = lvMinDefault
            extraInfo['lvMax'] = lvMaxDefault
        teamName = extraInfo.get('teamName', utils.getTeamName())
        lvMin = extraInfo.get('lvMin', lvMinDefault)
        lvMax = extraInfo.get('lvMax', lvMaxDefault)
        schoolReqs = extraInfo.get('schoolReq', const.SCHOOL_DICT.keys())
        isPublic = True
        goalType = self.getGoalTypeByMenuIdx(self.goalTypeMenu.selectedIndex)
        self.updateCurrentTeamGoalMenuIdx()
        fKey, sKey, tKey = self.getCurrentTeamGoalKey()
        return (teamName,
         goalType,
         lvMin,
         lvMax,
         schoolReqs,
         isPublic,
         fKey,
         sKey,
         tKey)

    def updateCurrentTeamGoalMenuIdx(self):
        goalIdx = self.goalTypeMenu.selectedIndex
        goalType = self.getGoalTypeByMenuIdx(goalIdx)
        fIndex = self.goal1Menu.selectedIndex
        sIndex = self.goal2Menu.selectedIndex
        tIndex = const.GROUP_GOAL_DEFAULT
        groupDetailIns.goalIns[goalType].setDropDownMenuIndex(fIndex, sIndex, tIndex)

    def getCurrentTeamGoalKey(self):
        goalIdx = self.goalTypeMenu.selectedIndex
        goalType = self.getGoalTypeByMenuIdx(goalIdx)
        fIndex = self.goal1Menu.selectedIndex
        sIndex = self.goal2Menu.selectedIndex
        tIndex = const.GROUP_GOAL_DEFAULT
        return groupDetailIns.goalIns[goalType].getCreateTeamKeys(fIndex, sIndex, tIndex)

    def handleGoalChange(self, *args):
        e = ASObject(args[3][0])
        menu = e.currentTarget
        if menu == self.goalTypeMenu:
            self.resetGoalMenu(self.goal1Menu)
            self.resetGoalMenu(self.goal2Menu)
        elif menu == self.goal1Menu:
            self.resetGoalMenu(self.goal2Menu)
        goalType = self.getGoalTypeByMenuIdx(self.goalTypeMenu.selectedIndex)
        goal1Idx = self.goal1Menu.selectedIndex
        goal2Idx = self.goal2Menu.selectedIndex
        self.refreshTeamGoal(goalType, goal1Idx, goal2Idx)

    @staticmethod
    def hasGoal():
        p = BigWorld.player()
        if not getattr(p, 'detailInfo', {}):
            return False
        goalType = TeamGoalMenuHelper.getTeamGoalType()
        goal1Idx, goal2Idx, _ = groupDetailIns.dropMenuVal2Index(goalType)
        if goalType != const.GROUP_GOAL_DEFAULT and goal1Idx != 0 and goal2Idx != 0:
            return True
        return False

    def getGoalLvLimit(self):
        goalType = self.getGoalTypeByMenuIdx(self.goalTypeMenu.selectedIndex)
        goal1Idx = self.goal1Menu.selectedIndex
        goal2Idx = self.goal2Menu.selectedIndex
        lvMin = const.MIN_CURRENT_LEVEL
        lvMax = const.MAX_CURRENT_LEVEL
        actAvlData = groupDetailFactory.getActAvlData()
        if goalType == const.GROUP_GOAL_RELAXATION:
            if goal1Idx != 0 and goal2Idx != 0:
                key = actAvlData.get(goal1Idx)[goal2Idx - 1]
                item = GLD.data.get(key, {})
                if item.get('recommendLv'):
                    lvMin, lvMax = item['recommendLv']
                elif item.get('lv'):
                    lvMin, lvMax = item['lv']
        elif goalType == const.GROUP_GOAL_FB:
            lvMin, lvMax = self.getMenuFbLvLimit(goal1Idx, goal2Idx)
        return (lvMin, lvMax)
