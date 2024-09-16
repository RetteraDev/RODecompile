#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/crossServerSXYSetProxy.o
import BigWorld
import uiConst
import gamelog
import const
import gametypes
import copy
from asObject import TipManager
from uiProxy import UIProxy
from guis import ui
from asObject import ASUtils
from gameStrings import gameStrings
from guis import events
from guis.asObject import ASObject
from guis import rankPanelUtils
from data import sys_config_data as SCD
from data import digong_clanwar_config_data as DCCD
from cdata import game_msg_def_data as GMDD

def sort_by_level(a, b):
    return a.level - b.level


def sort_by_school(a, b):
    return a.school - b.school


def sort_by_roleId(a, b):
    pa = gametypes.GUILD_PRIVILEGES.get(a.roleId, {}).get('sortv', 0)
    pb = gametypes.GUILD_PRIVILEGES.get(b.roleId, {}).get('sortv', 0)
    return cmp(pa, pb)


def sort_by_time(a, b):
    if a.online != b.online:
        return a.online - b.online
    if a.online:
        return a.level - b.level
    return a.tLastOnline - b.tLastOnline


def sort_by_combat(a, b):
    return a.combatScore - b.combatScore


SORT_TYPE_LV = 1
SORT_TYPE_SCHOOL = 2
SORT_TYPE_POST = 3
SORT_TYPE_TIME = 4
SORT_TYPE_COMBAT = 5
SORT_MAP = {SORT_TYPE_LV: (sort_by_level, False),
 SORT_TYPE_SCHOOL: (sort_by_school, False),
 SORT_TYPE_POST: (sort_by_roleId, True),
 SORT_TYPE_TIME: (sort_by_time, True),
 SORT_TYPE_COMBAT: (sort_by_combat, False)}
SORT_BTN_MAP = {'lvMc': SORT_TYPE_LV,
 'postMc': SORT_TYPE_POST,
 'onlineMc': SORT_TYPE_TIME,
 'combatMc': SORT_TYPE_COMBAT}
BTN_MC_MAP = {1: 'lvMc',
 3: 'postMc',
 4: 'onlineMc',
 5: 'combatMc'}

class CrossServerSXYSetProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CrossServerSXYSetProxy, self).__init__(uiAdapter)
        self.widget = None
        self.ascendSorted = True
        self.allMembers = []
        self.onlineMembers = []
        self.memberList = []
        self.sortType = SORT_TYPE_TIME
        self.selectedGbIds = []
        uiAdapter.registerEscFunc(uiConst.WIDGET_CROSS_SERVER_SXY_SET, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CROSS_SERVER_SXY_SET:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CROSS_SERVER_SXY_SET)

    def reset(self):
        self.allMembers = []
        self.onlineMembers = []
        self.memberList = []
        self.sortType = SORT_TYPE_TIME
        self.selectedGbIds = []

    def show(self):
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_CROSS_SERVER_SXY_SET)
        gamelog.info('jbx:queryGuildMemberGSXY')
        BigWorld.player().cell.queryGuildMemberGSXY()

    @ui.callAfterTime(0.2)
    def updateMembers(self):
        if not self.widget:
            return
        self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.revokeBtn.addEventListener(events.BUTTON_CLICK, self.handleRevokeBtnClick, False, 0, True)
        self.widget.refreshBtn.addEventListener(events.BUTTON_CLICK, self.handleRefreshBtnClick, False, 0, True)
        self.widget.sureBtn.addEventListener(events.BUTTON_CLICK, self.handleSureBtnClick, False, 0, True)
        self.widget.postMc.addEventListener(events.MOUSE_CLICK, self.handleSortClick, False, 0, True)
        self.widget.lvMc.addEventListener(events.MOUSE_CLICK, self.handleSortClick, False, 0, True)
        self.widget.combatMc.addEventListener(events.MOUSE_CLICK, self.handleSortClick, False, 0, True)
        self.widget.onlineMc.addEventListener(events.MOUSE_CLICK, self.handleSortClick, False, 0, True)
        self.widget.searchInput.addEventListener(events.EVENT_CHANGE, self.handleInputChanged, False, 0, True)
        self.widget.searchInput.addEventListener(events.KEYBOARD_EVENT_KEY_UP, self.handleSearchKeyEvent, False, 0, True)
        self.widget.searchBtn.addEventListener(events.BUTTON_CLICK, self.handleSearchBtnClick, False, 0, True)
        self.widget.schoolDrop.addEventListener(events.INDEX_CHANGE, self.handleSchoolSelect, False, 0, True)
        self.widget.searchInput.defaultText = gameStrings.CROSS_SERVER_SXY_SEARCH_DEFAULT
        ASUtils.setDropdownMenuData(self.widget.schoolDrop, rankPanelUtils.getCompleteMenuData())
        if self.widget.schoolDrop.selectedIndex == -1:
            self.widget.schoolDrop.selectedIndex = 0
        self.widget.membersList.itemRenderer = 'CrossServerSXYSet_MemberItem'
        self.widget.membersList.barAlwaysVisible = True
        self.widget.membersList.dataArray = []
        self.widget.membersList.lableFunction = self.itemFunction
        p = BigWorld.player()
        self.selectedGbIds = copy.deepcopy(getattr(p, 'crossServerSXYGbIds', []))

    def checkMember(self, member):
        return member.level >= DCCD.data.get('gsxyLvLimit', 69)

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        guild = p.guild
        if not guild:
            return
        self.updateGuildPowerBtn()
        self.updateTitleBtnMcSortIcon()
        self.allMembers = [ gMember for gMember in guild.member.values() if self.checkMember(gMember) ]
        self.onlineMembers = [ member for member in self.allMembers if member.online ]
        members = sorted(self.allMembers, cmp=SORT_MAP[self.sortType][0], reverse=SORT_MAP[self.sortType][1] if self.ascendSorted else not SORT_MAP[self.sortType][1])
        self.memberList = []
        memberLen = len(members)
        for i in xrange(memberLen):
            memberInfo = self.createMemberInfo(members[i])
            self.memberList.append(memberInfo)

        self.widget.totalMember.text = '%d/%d' % (len(self.onlineMembers), len(self.allMembers))
        self.widget.membersList.dataArray = self.memberList
        self.widget.membersList.validateNow()
        self.updateSelectedMemberNum()

    def createMemberInfo(self, member):
        p = BigWorld.player()
        memberInfo = {}
        memberInfo['gbId'] = int(member.gbId)
        memberInfo['nameText'] = member.role
        memberInfo['lvText'] = member.level
        memberInfo['schoolId'] = member.school
        memberInfo['schoolText'] = const.SCHOOL_DICT[member.school]
        memberInfo['postText'] = gametypes.GUILD_ROLE_DICT[member.roleId]
        memberInfo['combatText'] = member.combatScore
        memberInfo['online'] = bool(member.online)
        memberInfo['onlineText'] = gameStrings.CROSS_SERVER_SXY_ONLINE if member.online else gameStrings.CROSS_SERVER_SXY_OFFLINE
        memberInfo['isSelected'] = member.gbId in self.selectedGbIds
        memberInfo['isDisableCheckBox'] = p.guild.memberMe.roleId in DCCD.data.get('qualifyPostList', [1, 2])
        return memberInfo

    def updateGuildPowerBtn(self):
        p = BigWorld.player()
        roleId = p.guild.memberMe.roleId
        if roleId in DCCD.data.get('qualifyPostList', [1, 2]):
            self.widget.revokeBtn.disabled = False
            self.widget.sureBtn.disabled = False
        else:
            self.widget.revokeBtn.disabled = True
            self.widget.sureBtn.disabled = True
            TipManager.addTip(self.widget.revokeBtn, gameStrings.ONLY_HAS_GUILD_POWER_TIP)
            TipManager.addTip(self.widget.sureBtn, gameStrings.ONLY_HAS_GUILD_POWER_TIP)

    def updateTitleBtnMcSortIcon(self):
        for i in BTN_MC_MAP.keys():
            btnMc = self.widget.getChildByName(BTN_MC_MAP[i])
            if self.sortType == i:
                btnMc.sortIcon.visible = True
                if self.ascendSorted:
                    btnMc.sortIcon.gotoAndStop('up')
                else:
                    btnMc.sortIcon.gotoAndStop('down')
            else:
                btnMc.sortIcon.visible = False

    def handleRevokeBtnClick(self, *args):
        p = BigWorld.player()
        p.cell.removeGuildMemberGSXY()

    def handleRefreshBtnClick(self, *args):
        p = BigWorld.player()
        gamelog.info('jbx:queryGuildMemberGSXY')
        p.cell.queryGuildMemberGSXY()

    def handleSureBtnClick(self, *args):
        p = BigWorld.player()
        gamelog.info('jbx:selectedGbIds', self.selectedGbIds)
        p.cell.setGuildMemberGSXY(self.selectedGbIds)

    def handleSortClick(self, *args):
        target = ASObject(args[3][0]).currentTarget
        sortType = SORT_BTN_MAP[target.name]
        self.sortType = sortType
        if target.sortIcon.visible and target.sortIcon.currentLabel == 'up':
            self.ascendSorted = False
        else:
            self.ascendSorted = True
        self.refreshInfo()

    def handleInputChanged(self, *args):
        if self.widget.searchInput == '':
            return

    def handleSearchKeyEvent(self, *args):
        e = ASObject(args[3][0])
        if int(e.keyCode) == uiConst.AS_KEY_CODE_ENTER:
            self.updateSearchedName()

    def handleSearchBtnClick(self, *args):
        if self.widget.searchInput == '':
            return
        self.updateSearchedName()

    def handleSchoolSelect(self, *args):
        schoolId = rankPanelUtils.getCompleteMenuData()[self.widget.schoolDrop.selectedIndex]['schoolId']
        self.updateSchoolSort(schoolId)

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.checkBox.removeEventListener(events.EVENT_SELECT, self.handleSelectCheckBox)
        itemMc.memberData = itemData
        if itemData.online:
            color = '0xE5D4A1'
        else:
            color = '0x808080'
        itemMc.nameText.text = itemData.nameText
        itemMc.postText.text = itemData.postText
        itemMc.lvText.text = itemData.lvText
        itemMc.schoolText.text = itemData.schoolText
        itemMc.combatText.text = itemData.combatText
        itemMc.onlineText.text = itemData.onlineText
        itemMc.nameText.textColor = color
        itemMc.postText.textColor = color
        itemMc.lvText.textColor = color
        itemMc.schoolText.textColor = color
        itemMc.combatText.textColor = color
        itemMc.onlineText.textColor = color
        itemMc.checkBox.selected = itemData.isSelected
        if itemData.isDisableCheckBox:
            itemMc.checkBox.disabled = False
            TipManager.removeTip(itemMc.checkBox)
            itemMc.checkBox.addEventListener(events.EVENT_SELECT, self.handleSelectCheckBox, False, 0, True)
        else:
            itemMc.checkBox.disabled = True
            TipManager.addTip(itemMc.checkBox, DCCD.data.get('qualifyPostTip', gameStrings.ONLY_HAS_GUILD_POWER_TIP))

    def handleSelectCheckBox(self, *args):
        target = ASObject(args[3][0]).currentTarget
        itemMc = target.parent
        gbId = int(itemMc.memberData.gbId)
        if target.selected:
            if len(self.selectedGbIds) == DCCD.data.get('gsxyMaxMemberNum', 50):
                BigWorld.player().showGameMsg(GMDD.data.GSXY_SET_MEMBER_FAIL_MEMBER_CNT_LIMIT, ())
                target.removeEventListener(events.EVENT_SELECT, self.handleSelectCheckBox)
                target.selected = False
                target.addEventListener(events.EVENT_SELECT, self.handleSelectCheckBox, False, 0, True)
                return
            self.selectedGbIds.append(gbId)
        elif gbId in self.selectedGbIds:
            self.selectedGbIds.remove(gbId)
        self.updateSelectedMemberNum()

    def updateSelectedMemberNum(self):
        self.widget.selectedMember.text = '%d/%d' % (len(self.selectedGbIds), len(self.allMembers))

    def updateSearchedName(self):
        playerName = self.widget.searchInput
        number = 0
        for itemInfo in self.memberList:
            if playerName == itemInfo.get('nameText', ''):
                return number
            number += 1

        pos = self.widget.membersList.getIndexPosY(number)
        self.widget.membersList.scrollTo(pos)

    def updateSchoolSort(self, schoolId):
        schoolList = []
        for itemInfo in self.memberList:
            if itemInfo.get('schoolId', 0) == schoolId:
                schoolList.append(itemInfo)

        if schoolId == 0:
            schoolList = self.memberList
        self.widget.membersList.dataArray = schoolList
        self.widget.membersList.validateNow()

    def updateFbEliteMembersList(self, gbIds):
        self.selectedGbIds = copy.deepcopy(gbIds)
        self.refreshInfo()
