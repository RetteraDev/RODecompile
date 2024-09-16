#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/rankPanelUtils.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import const
import events
from gamestrings import gameStrings
import gameglobal
import clientcom
from guis import uiConst
from guis import uiUtils
from guis.asObject import ASObject
from guis.asObject import TipManager
from guis.asObject import ASUtils

class BaseRankUtil(object):

    def reset(self):
        pass

    def unRegister(self):
        self.reset()

    def register(self, *args):
        pass


class BaseRankClickGroupUtil(BaseRankUtil):

    def __init__(self):
        self.widget = None
        self.dataMap = {}
        self.clickCalBack = None
        self.currentData = None
        self.selectedMc = None

    def handleClick(self, *args):
        if not self.widget:
            return
        else:
            mc = ASObject(args[3][0]).currentTarget
            data = self.dataMap.get(mc.name, None)
            if data != None:
                mc.selected = True
                self.selectedMc = mc
                self.currentData = data
                if self.clickCalBack:
                    self.clickCalBack()
            return

    def unRegister(self):
        if self.dataMap:
            for mcName, data in self.dataMap.iteritems():
                mc = getattr(self.widget, mcName, None)
                if mc:
                    mc.removeEventListener(events.BUTTON_CLICK, self.handleClick)

        self.reset()


class SchoolBtnsUtil(BaseRankClickGroupUtil):

    def __init__(self):
        super(SchoolBtnsUtil, self).__init__()
        self.defaultMcMap = {'allBtn': const.SCHOOL_DEFAULT,
         'shengtangBtn': const.SCHOOL_SHENTANG,
         'yuxuBtn': const.SCHOOL_YUXU,
         'guangrenBtn': const.SCHOOL_GUANGREN,
         'yantianBtn': const.SCHOOL_YANTIAN,
         'linglongBtn': const.SCHOOL_LINGLONG,
         'liuguangBtn': const.SCHOOL_LIUGUANG,
         'yechaBtn': const.SCHOOL_YECHA,
         'tianzhaoBtn': const.SCHOOL_TIANZHAO}

    def reset(self):
        self.widget = None
        self.dataMap = {}
        self.clickCalBack = None
        self.currentData = None
        self.selectedMc = None

    def register(self, widget, selectedMc, clickCalBack, mcMap = None, needTip = False):
        self.clickCalBack = clickCalBack
        self.widget = widget
        self.selectedMc = selectedMc
        if mcMap:
            self.dataMap = mcMap
        else:
            self.dataMap = self.defaultMcMap
        if self.selectedMc:
            self.selectedMc.selected = True
            self.currentData = self.dataMap.get(selectedMc.name, '')
        for mcName, data in self.dataMap.iteritems():
            btnMc = getattr(self.widget, mcName, None)
            if btnMc:
                if needTip:
                    name = uiUtils.getSchoolNameById(data)
                    if not name and data == const.SCHOOL_DEFAULT:
                        name = gameStrings.RANK_ALL_SCHOOL
                    TipManager.addTip(btnMc, name)
                btnMc.groupName = 'schoolGroup'
                btnMc.addEventListener(events.BUTTON_CLICK, self.handleClick, False, 0, True)


class LvButtonsUtil(BaseRankClickGroupUtil):

    def __init__(self):
        super(LvButtonsUtil, self).__init__()

    def register(self, widget, selectedMc, mcMap, clickCalBack):
        self.widget = widget
        self.clickCalBack = clickCalBack
        self.dataMap = mcMap
        self.selectedMc = selectedMc
        if self.selectedMc:
            self.selectedMc.selected = True
            self.currentData = self.dataMap.get(self.selectedMc.name, '')
        for mcName, data in self.dataMap.iteritems():
            btnMc = getattr(self.widget, mcName, None)
            if btnMc:
                btnMc.groupName = 'lvBtnGroup'
                btnMc.addEventListener(events.BUTTON_CLICK, self.handleClick, False, 0, True)

    def reset(self):
        self.dataMap = {}
        self.currentData = ''
        self.widget = None
        self.selectedMc = None
        self.clickCalBack = None


class RankListUtil(BaseRankUtil):

    def __init__(self):
        self.mc = None
        self.listItemCalBack = None
        self.selectedItem = None
        self.clickedMc = None
        self.listItemCalBack = None
        self.clickListItemCalBack = None
        self.dataMap = {}

    def register(self, mc, itemHeight, itemRenderer, itemDataMap, listItemCalBack = None, clickListItemCalBack = None):
        self.mc = mc
        self.listItemCalBack = listItemCalBack
        self.dataMap = itemDataMap
        self.clickListItemCalBack = clickListItemCalBack
        mc.itemHeight = itemHeight
        mc.itemRenderer = itemRenderer
        mc.lableFunction = self.listItemFunc

    def listItemFunc(self, *args):
        if not self.mc:
            return
        else:
            itemData = ASObject(args[3][0])
            itemMc = ASObject(args[3][1])
            roleName = getattr(itemData, 'roleName', '')
            isSelf = getattr(itemData, 'gbid', 0) == BigWorld.player().gbId or roleName == BigWorld.player().roleName
            for k, value in self.dataMap.iteritems():
                mc = getattr(itemMc, k, None)
                text = getattr(itemData, value, '')
                if mc:
                    mc.htmlText = uiUtils.toHtml(text, color='#a65b11') if isSelf else text

            itemMc.data = itemData
            if self.listItemCalBack:
                self.listItemCalBack(itemMc)
            itemMc.addEventListener(events.MOUSE_CLICK, self.handleClickListItem, False, 0, True)
            return

    def unRegister(self):
        self.reset()

    def handleClickListItem(self, *args):
        if not self.mc:
            return
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if self.selectedItem:
            self.selectedItem.gotoAndStop('up')
        self.selectedItem = itemMc
        self.selectedItem.gotoAndStop('down')
        if self.clickListItemCalBack:
            self.clickListItemCalBack(e)

    def setItemBg(self, index, itemMc):
        bg = getattr(itemMc, 'bg', None)
        if bg:
            state = 'bai' if index % 2 == 1 else 'wu'
            bg.gotoAndStop(state)

    def scrollToMyRank(self, myRank):
        if self.mc:
            myRankPos = (myRank - 1) * self.itemHeight
            self.mc.scrollTo(myRankPos)

    def reset(self):
        self.mc = None
        self.listItemCalBack = None
        self.selectedItem = None
        self.listItemCalBack = None
        self.clickListItemCalBack = None
        self.dataMap = {}


class RefreshBtnUtil(BaseRankUtil):

    def __init__(self):
        self.mc = None
        self.cdTime = 0
        self.clickCalBack = None
        self.updateTimer = None
        self.updateCountDown = None

    def register(self, btnMc, clickCalBack, cdTime = 0):
        self.mc = btnMc
        self.cdTime = cdTime
        self.clickCalBack = clickCalBack
        if cdTime == 0:
            self.mc.addEventListener(events.MOUSE_CLICK, self.handleClickRefreshBtn, False, 0, True)
        elif cdTime > 0:
            self.mc.addEventListener(events.MOUSE_CLICK, self.handleClickCDRefreshBtn, False, 0, True)
        self.clickCalBack = clickCalBack
        if self.updateTimer == None:
            self.mc.label = gameStrings.REFRESH_BTN_LABEL
            self.mc.enabled = True
        else:
            self.mc.enabled = False
            self.mc.label = gameStrings.REFRESH_BTN_LABEL_CD % self.updateCountDown

    def handleClickRefreshBtn(self, *args):
        if not self.mc:
            return
        self.clickCalBack()

    def handleClickCDRefreshBtn(self, *args):
        if not self.mc:
            return
        else:
            if self.updateTimer == None:
                self.mc.enabled = False
                self.updateCountDown = self.cdTime + 1
                self.updateTimer = BigWorld.callback(0, self.updateRefreshCD)
                self.clickCalBack()
            return

    def updateRefreshCD(self):
        self.updateCountDown -= 1
        if self.updateCountDown > 0 and self.updateTimer:
            if self.mc:
                self.mc.label = gameStrings.REFRESH_BTN_LABEL_CD % self.updateCountDown
            self.updateTimer = BigWorld.callback(1, self.updateRefreshCD)
        else:
            self.updateTimer = None
            self.updateCountDown = 0
            if self.mc:
                self.mc.label = gameStrings.REFRESH_BTN_LABEL
                self.mc.enabled = True

    def reset(self):
        self.mc = None
        self.cdTime = 0
        self.clickCalBack = None

    def resetAll(self):
        self.mc = None
        self.cdTime = 0
        self.clickCalBack = None
        self.updateTimer = None
        self.updateCountDown = None

    def unRegister(self):
        if not self.mc:
            return
        if self.cdTime == 0:
            self.mc.removeEventListener(events.MOUSE_CLICK, self.handleClickRefreshBtn)
        elif self.cdTime > 0:
            self.mc.removeEventListener(events.MOUSE_CLICK, self.handleClickCDRefreshBtn)
        self.reset()


def getDefaultSchoolMenuData():
    menuData = []
    for school in const.SCHOOL_SET:
        if school == const.SCHOOL_TIANZHAO and not clientcom.enableNewSchoolTianZhao():
            continue
        menuData.append({'label': const.SCHOOL_DICT[school],
         'schoolId': school})

    return menuData


def getCompleteMenuData():
    menuData = getDefaultSchoolMenuData()
    menuData.insert(0, {'label': gameStrings.TEXT_RANKPANELUTILS_296,
     'schoolId': 0})
    return menuData


class SchoolMenuUtil(BaseRankUtil):

    def __init__(self):
        self.reset()
        super(SchoolMenuUtil, self).__init__()

    def register(self, menuMc, changeCallback, menuData = None, selectIdx = 0):
        if menuData == None:
            menuData = getDefaultSchoolMenuData()
        self.menuMc = menuMc
        self.menuData = menuData
        self.changeCallback = changeCallback
        ASUtils.setDropdownMenuData(self.menuMc, menuData)
        self.menuMc.menuRowCount = len(menuData)
        self.menuMc.selectedIndex = selectIdx
        self.schoolId = self.menuData[selectIdx]['schoolId']
        self.menuMc.jobIcon.gotoAndStop(uiConst.SCHOOL_FRAME_DESC[self.schoolId])
        self.menuMc.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.onChangeCallback, False, 0, True)

    def onChangeCallback(self, *args):
        schoolId = self.menuData[self.menuMc.selectedIndex]['schoolId']
        frameName = uiConst.SCHOOL_FRAME_DESC[schoolId]
        self.menuMc.jobIcon.gotoAndStop(frameName)
        self.schoolId = schoolId
        self.changeCallback()

    def reset(self):
        self.menuMc = None
        self.menuData = {}
        self.schoolId = 0
        self.changeCallback = None

    def unregister(self):
        if self.menuMc:
            self.menuMc.removeEventListener(events.LIST_EVENT_INDEX_CHANGE, self.onChangeCallback)
        self.reset()
