#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/achvmentStageAwardProxy.o
from gamestrings import gameStrings
import gameglobal
import uiConst
import clientUtils
from uiProxy import UIProxy
from guis.asObject import ASObject
from gamestrings import gameStrings
from guis import events
from guis import uiUtils
from guis.asObject import ASUtils
from item import Item
from data import achievement_point_lv_data as APLD
from data import achievement_class_data as ACD
from data import title_data as TD
from data import item_data as ID
from data import achievement_data as AD
MAIN_CLASS_ID = 0
FIRST_STAGE = 1
DETAIL_COLUMN_MAINCLASS = 4
DETAIL_COLUMN = 5
TITLE_ICON_PATH = 'achvment/76/%d.dds'
MAIN_ITEM_H = 166
MAIN_ITEM_W = 118
ITEM_H = 128
ITEM_W = 95
KEYCODE_CTRL = 17

class AchvmentStageAwardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(AchvmentStageAwardProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ACHVMENT_STAGE_AWARD, self.hide)

    def reset(self):
        self.achieves = {}
        self.achievePointData = {}
        self.maxPointData = {}
        self.subClassInfo = {}
        self.achieveFilterData = {}
        self.classData = []
        self.detailData = {}
        self.classProgress = {}
        self.lastSelClassId = 0
        self.lastSelClassItem = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ACHVMENT_STAGE_AWARD:
            self.widget = widget
            self.initData()
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ACHVMENT_STAGE_AWARD)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ACHVMENT_STAGE_AWARD)

    def initData(self):
        self.achieves = gameglobal.rds.ui.achvment.achieves
        self.achievePoint = gameglobal.rds.ui.achvment.achievePoint
        self.achieveFilterData = AD.data
        self.subClassInfo = gameglobal.rds.ui.achvment.subClassInfo
        self.classProgress = gameglobal.rds.ui.achvment.classProgress
        self.classData = self.genClassData()
        self.detailData = self.genDetailData()
        self.achievePointData, self.maxPointData = self.genClassAchievePointData()

    def genClassAchievePointData(self):
        if not self.subClassInfo:
            self.subClassInfo = gameglobal.rds.ui.achvment.genSubClassInfo()
        achievedRet = {}
        maxRet = {}
        for k, v in self.achieveFilterData.iteritems():
            val = v.get('rewardPoint', 0)
            subClassId = v.get('class', 0)
            classId = self.subClassInfo.get(subClassId, ('', 0))[1]
            if classId not in achievedRet:
                achievedRet[classId] = 0
            if k in self.achieves:
                achievedRet[classId] += val
            if classId not in maxRet:
                maxRet[classId] = 0
            maxRet[classId] += val

        achievedRet[MAIN_CLASS_ID] = sum(achievedRet.itervalues())
        maxRet[MAIN_CLASS_ID] = sum(maxRet.itervalues())
        return (achievedRet, maxRet)

    def genClassData(self):
        classIds = set([ classId for classId, stageIdx in APLD.data.iterkeys() ])
        return sorted(list(classIds))

    def genDetailData(self):
        ret = {}
        for k, v in APLD.data.iteritems():
            classId, stageIndex = k
            if classId not in ret:
                ret[classId] = {}
            ret[classId][stageIndex] = v

        del ret[MAIN_CLASS_ID][FIRST_STAGE]
        sortedRet = {}
        for classId, classInfo in ret.iteritems():
            sortkey = sorted(classInfo.iterkeys())
            sortedRet[classId] = [ ret[classId][stageIndex] for stageIndex in sortkey ]

        return sortedRet

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.isCtrlPressed = False
        self.widget.stage.addEventListener(events.KEYBOARD_EVENT_KEY_DOWN, self.handleKeyEvent, False, 0, True)
        self.widget.stage.addEventListener(events.KEYBOARD_EVENT_KEY_UP, self.handleKeyEvent, False, 0, True)
        self.refreshInfo()

    def handleKeyEvent(self, *args):
        e = ASObject(args[3][0])
        if e.keyCode == KEYCODE_CTRL:
            self.isCtrlPressed = e.type == events.KEYBOARD_EVENT_KEY_DOWN

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshClassList()
        self.refreshDetailList()
        self.refreshTopInfo()

    def refreshTopInfo(self):
        if self.lastSelClassId == MAIN_CLASS_ID:
            achievePoint = self.achievePoint
            achievedCnt = len(self.achieves)
            maxAchieveCnt = len(self.achieveFilterData)
        else:
            achievePoint = self.achievePointData[self.lastSelClassId]
            achievedCnt, maxAchieveCnt = self.classProgress.get(self.lastSelClassId, (0, 1))
        self.widget.achievePointTf.text = achievePoint
        self.widget.achieveTf.text = gameStrings.ACHIEVEMENT_ACHIEVED_TEXT % achievedCnt
        self.widget.achieveProgressTf.text = gameStrings.ACHIEVEMENT_ACHIEVED_PROGRESS_TEXT % (100.0 * achievedCnt / maxAchieveCnt)

    def refreshClassList(self):
        self.widget.classList.itemRenderer = 'AchvmentStageAward_ClassItem'
        self.widget.classList.labelFunction = self.classItemFunction
        self.widget.classList.dataArray = self.classData
        self.widget.classList.validateNow()

    def classItemFunction(self, *args):
        classId = int(args[3][0].GetNumber())
        item = ASObject(args[3][1])
        item.classId = classId
        item.label = ACD.data.get(classId, {}).get('name', gameStrings.TEXT_ACHVMENTSTAGEAWARDPROXY_164)
        isSel = bool(self.lastSelClassId == classId)
        item.selected = isSel
        if isSel:
            self.lastSelClassItem = item
        item.addEventListener(events.MOUSE_CLICK, self.onClassItemClick, False, 0, True)

    def refreshDetailList(self, needReset = False):
        if self.lastSelClassId == MAIN_CLASS_ID:
            self.widget.detailList.itemRenderer = 'AchvmentStageAward_MainClassDetailItem'
            self.widget.detailList.labelFunction = self.mainDetailItemFunction
            self.widget.detailList.itemHeight = MAIN_ITEM_H
            self.widget.detailList.itemWidth = MAIN_ITEM_W
            self.widget.detailList.column = DETAIL_COLUMN_MAINCLASS
        else:
            self.widget.detailList.itemRenderer = 'AchvmentStageAward_DetailItem'
            self.widget.detailList.labelFunction = self.detailItemFunction
            self.widget.detailList.column = DETAIL_COLUMN
            self.widget.detailList.itemHeight = ITEM_H
            self.widget.detailList.itemWidth = ITEM_W
        self.widget.detailList.dataArray = self.detailData.get(self.lastSelClassId, ())
        self.widget.detailList.validateNow()
        needReset and self.widget.detailList.scrollToHead()

    def mainDetailItemFunction(self, *args):
        data = ASObject(args[3][0])
        item = ASObject(args[3][1])
        rangeFloor = data.achievePointRange
        item.achievePointTf.text = rangeFloor
        titleIconId = data.rewardTitleIcon
        item.titleIcon.visible = titleIconId
        item.titleIcon.fitSize = True
        titleIconId and item.titleIcon.loadImage(TITLE_ICON_PATH % titleIconId)
        item.titleTf.text = TD.data.get(data.rewardTitle, {}).get('name')
        isAchieved = self.isAchievedRangeFloor(self.lastSelClassId, rangeFloor)
        item.getIcon.visible = isAchieved
        ASUtils.setHitTestDisable(item.getIcon, True)
        bonusId = data.rewardBonusId
        rewardItems = clientUtils.genItemBonus(bonusId)
        if len(rewardItems) == 1:
            itemId, cnt = rewardItems[0]
            state = uiConst.ITEM_GRAY if isAchieved else uiConst.ITEM_NORMAL
            item.slot.setItemSlotData(uiUtils.getGfxItemById(itemId, cnt, appendInfo={'state': state,
             'srcType': 'achevment'}))
            item.slot.itemId = itemId
            item.slot.addEventListener(events.MOUSE_CLICK, self.onItemClick, False, 0, True)
            item.slot.dragable = False

    def onItemClick(self, *args):
        itemId = ASObject(args[3][0]).currentTarget.itemId
        if self.isCtrlPressed:
            item = Item(itemId)
            if item.isEquip():
                gameglobal.rds.ui.fittingRoom.addItem(item)

    def detailItemFunction(self, *args):
        data = ASObject(args[3][0])
        item = ASObject(args[3][1])
        rangeFloor = data.achievePointRange
        item.achievePointTf.text = rangeFloor
        isAchieved = self.isAchievedRangeFloor(self.lastSelClassId, rangeFloor)
        item.getIcon.visible = isAchieved
        ASUtils.setHitTestDisable(item.getIcon, True)
        bonusId = data.rewardBonusId
        rewardItems = clientUtils.genItemBonus(bonusId)
        if len(rewardItems) == 1:
            itemId, cnt = rewardItems[0]
            item.nameTf.text = ID.data.get(itemId, {}).get('name')
            state = uiConst.ITEM_GRAY if isAchieved else uiConst.ITEM_NORMAL
            item.slot.itemId = itemId
            item.slot.addEventListener(events.MOUSE_CLICK, self.onItemClick, False, 0, True)
            item.slot.setItemSlotData(uiUtils.getGfxItemById(itemId, cnt, appendInfo={'state': state,
             'srcType': 'achevment'}))
            item.slot.dragable = False

    def isAchievedRangeFloor(self, classId, rangeFloor):
        if not rangeFloor:
            rangeFloor = 0
        classAchievedPoint = self.achievePointData.get(classId, 0)
        return classAchievedPoint >= int(rangeFloor)

    def onClassItemClick(self, *args):
        e = ASObject(args[3][0])
        item = e.currentTarget
        classId = item.classId
        if classId == self.lastSelClassId:
            return
        item.selected = True
        if self.lastSelClassItem:
            self.lastSelClassItem.selected = False
        self.lastSelClassItem = item
        self.lastSelClassId = classId
        self.refreshDetailList(needReset=True)
        self.refreshTopInfo()
