#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/schoolTransferSelectProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import const
import utils
import uiUtils
import gameconfigCommon
from uiProxy import UIProxy
from asObject import ASObject
from gamestrings import gameStrings
from callbackHelper import Functor
from guis.asObject import TipManager
from cdata import game_msg_def_data as GMDD
from data import school_transfer_config_data as STCD
TAB_ITEM_HORIZONTAL_OFFSET = 162
TAB_ITEM_WIDTH = 261
TAB_ITEM_POS_Y = 197

class SchoolTransferSelectProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SchoolTransferSelectProxy, self).__init__(uiAdapter)
        self.widget = None
        self.transferInfo = {}
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SCHOOL_TRANSFER_SELECT, self.hideNpcPanel)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SCHOOL_TRANSFER_SELECT:
            self.widget = widget
            self.initUI()
            self.queryInfo()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SCHOOL_TRANSFER_SELECT)

    def reset(self):
        self.selectedSchool = const.SCHOOL_DEFAULT
        self.isLowLvFree = False

    def clearAll(self):
        self.transferInfo = {}

    def hideNpcPanel(self):
        self.hide()
        if self.uiAdapter.funcNpc.isOnFuncState():
            self.uiAdapter.funcNpc.close()

    def show(self, selectedSchool, isLowLvFree):
        if not gameglobal.rds.configData.get('enableSchoolTransfer', False):
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.SCHOOL_TRANSFER_DISABLED, ())
            return
        if isLowLvFree and not gameglobal.rds.configData.get('enableLowLvFreeSchoolTransfer', False):
            return
        self.selectedSchool = selectedSchool
        self.isLowLvFree = isLowLvFree
        if self.widget:
            self.refreshInfo()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SCHOOL_TRANSFER_SELECT)

    def initUI(self):
        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.handleClickCloseBtn, False, 0, True)
        schoolCount = len(const.SCHOOL_SET)
        allTabItemWidth = TAB_ITEM_WIDTH * (schoolCount - 1) - (TAB_ITEM_WIDTH - TAB_ITEM_HORIZONTAL_OFFSET) * (schoolCount - 2)
        tabItemStartPosX = self.widget.title.x + self.widget.title.width / 2.0 - allTabItemWidth / 2.0
        for i in xrange(schoolCount - 1):
            itemMc = self.widget.getChildByName('item%d' % i)
            if not itemMc:
                itemMc = self.widget.getInstByClsName('SchoolTransferSelect_TabButton')
                itemMc.name = 'item%d' % i
                itemMc.x = tabItemStartPosX + TAB_ITEM_HORIZONTAL_OFFSET * i
                itemMc.y = TAB_ITEM_POS_Y
                self.widget.addChild(itemMc)
            itemMc.groupName = 'school'
            itemMc.data = {'school': 0,
             'schoolName': '',
             'hint': ''}
            itemMc.addEventListener(events.BUTTON_CLICK, self.handleClickItem, False, 0, True)
            itemMc.addEventListener(events.COMPONENT_STATE_CHANGE, self.handleStateChange, False, 0, True)

        self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleClickConfirmBtn, False, 0, True)
        self.widget.addEventListener(events.EVENT_RESIZE, self.handleResize, False, 0, True)
        self.handleResize()

    def handleResize(self, *args):
        self.widget.bg.x = (1280 - int(self.widget.stage.stageWidth)) / 2 - 1
        self.widget.bg.width = self.widget.stage.stageWidth + 2

    def queryInfo(self):
        BigWorld.player().cell.querySchoolTransferCondtion()

    def refreshInfo(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            freeLv = STCD.data.get('freeLv', 49)
            lvFreeCnt = STCD.data.get('lvFreeCnt', 4)
            if self.isLowLvFree:
                self.widget.title.gotoAndStop('lowLvlFree')
                self.widget.freeTime.visible = True
                if p.lv > freeLv:
                    self.widget.freeTime.textField.text = gameStrings.SCHOOL_TRANSFER_SELECT_PROXY_FREE_LV_INVALID
                else:
                    self.widget.freeTime.textField.text = gameStrings.SCHOOL_TRANSFER_SELECT_PROXY_FREE_LV_LEFT_TIME % (lvFreeCnt - p.freeSchoolTransferCnt)
            else:
                self.widget.title.gotoAndStop('normal')
                self.widget.freeTime.visible = False
            self.widget.nowSchoolIcon.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(p.school, ''))
            self.widget.nowSchoolName.text = const.SCHOOL_DICT.get(p.school, '')
            oldSchool = self.transferInfo.get('school', 0)
            newSchool = self.transferInfo.get('tSchool', 0)
            lastTime = self.transferInfo.get('tTransfer', 0)
            hasReverted = self.transferInfo.get('hasReverted', 0)
            if gameconfigCommon.enableSchoolTransferConditionItemCost():
                schoolTransferCD = STCD.data.get('schoolTransferNewCD', 1)
            else:
                schoolTransferCD = STCD.data.get('schoolTransferCD', 7)
            schoolTransferBackCD = STCD.data.get('schoolTransferBackCD', 7)
            now = utils.getNow()
            if now - lastTime < schoolTransferCD * const.SECONDS_PER_DAY:
                hasTransfer = True
                lastSchool = newSchool if hasReverted else oldSchool
            else:
                hasTransfer = False
                lastSchool = p.school
            firstSelectedItemMc = None
            schoolList = list(const.SCHOOL_SET)
            if p.school in schoolList:
                schoolList.remove(p.school)
            for i, school in enumerate(schoolList):
                itemMc = self.widget.getChildByName('item%d' % i)
                if not itemMc:
                    continue
                itemMc.schoolImage.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(school, ''))
                if self.isLowLvFree:
                    hint = gameStrings.SCHOOL_TRANSFER_SELECT_PROXY_FREE_HINT % freeLv
                    if p.lv > freeLv:
                        itemMc.enabled = False
                    else:
                        itemMc.enabled = True
                        if not firstSelectedItemMc and self.selectedSchool in (const.SCHOOL_DEFAULT, school):
                            firstSelectedItemMc = itemMc
                elif hasTransfer:
                    leftBackTime = lastTime + schoolTransferBackCD * const.SECONDS_PER_DAY - now
                    if hasReverted or school != lastSchool or leftBackTime <= 0:
                        itemMc.enabled = False
                        hint = gameStrings.SCHOOL_TRANSFER_SELECT_PROXY_AGAIN_HINT % schoolTransferCD
                        leftAgainTime = lastTime + schoolTransferCD * const.SECONDS_PER_DAY - now
                        if leftAgainTime < 0:
                            leftAgainTime = 0
                        tips = gameStrings.SCHOOL_TRANSFER_SELECT_PROXY_AGAIN_TIME_TIPS % utils.formatDuration(leftAgainTime)
                        TipManager.addTip(itemMc, tips, 5, 'over', 'mouse')
                    else:
                        itemMc.enabled = True
                        hint = gameStrings.SCHOOL_TRANSFER_SELECT_PROXY_BACK_HINT_NEW
                        tips = gameStrings.SCHOOL_TRANSFER_SELECT_PROXY_BACK_TIME_TIPS % utils.formatDuration(leftBackTime)
                        TipManager.addTip(itemMc, tips, 5, 'over', 'mouse')
                        if not firstSelectedItemMc and self.selectedSchool in (const.SCHOOL_DEFAULT, school):
                            firstSelectedItemMc = itemMc
                else:
                    itemMc.enabled = True
                    if gameconfigCommon.enableSchoolTransferConditionItemCost():
                        hint = ''
                    else:
                        hint = gameStrings.SCHOOL_TRANSFER_SELECT_PROXY_CD_HINT % schoolTransferBackCD
                    if not firstSelectedItemMc and self.selectedSchool in (const.SCHOOL_DEFAULT, school):
                        firstSelectedItemMc = itemMc
                leftBackTime = lastTime + schoolTransferBackCD * const.SECONDS_PER_DAY - now
                if hasReverted == 0 and school == oldSchool and leftBackTime > 0 and not self.isLowLvFree:
                    hint = gameStrings.SCHOOL_TRANSFER_SELECT_PROXY_BACK_HINT_NEW
                if school == const.SCHOOL_TIANZHAO:
                    itemMc.newFlag.visible = True
                    openYechaTransferTime = STCD.data.get('openYechaTransferTime', '2016.10.20.00.00.00')
                    openYechaTransferTime = utils.getTimeSecondFromStr(openYechaTransferTime)
                    if openYechaTransferTime > utils.getNow():
                        itemMc.enabled = False
                        hint = STCD.data.get('openYechaTransferHint', '')
                else:
                    itemMc.newFlag.visible = False
                itemMc.hint.htmlText = hint
                itemData = {}
                itemData['school'] = school
                itemData['schoolName'] = const.SCHOOL_DICT.get(school, '')
                itemData['hint'] = hint
                itemMc.data = itemData

            if firstSelectedItemMc:
                firstSelectedItemMc.selected = True
                self.refreshSelectedInfo(int(firstSelectedItemMc.data.school))
            else:
                self.refreshSelectedInfo(const.SCHOOL_DEFAULT)
                self.widget.confirmBtn.enabled = False
            return

    def refreshSelectedInfo(self, selectedSchool):
        if not self.widget:
            return
        self.selectedSchool = selectedSchool
        self.widget.nextSchoolIcon.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(self.selectedSchool, ''))
        self.widget.nextSchoolName.text = const.SCHOOL_DICT.get(self.selectedSchool, '')
        if self.isLowLvFree and BigWorld.player().freeSchoolTransferCnt >= STCD.data.get('lvFreeCnt', 4):
            self.widget.confirmBtn.enabled = False
        else:
            self.widget.confirmBtn.enabled = True

    def handleClickItem(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if itemMc.selected:
            return
        itemMc.selected = True
        self.refreshSelectedInfo(int(itemMc.data.school))

    def handleStateChange(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        itemMc.schoolName.text = itemMc.data.schoolName
        itemMc.hint.htmlText = itemMc.data.hint

    def handleClickCloseBtn(self, *args):
        self.hideNpcPanel()

    def handleClickConfirmBtn(self, *args):
        schoolTransferBackCD = STCD.data.get('schoolTransferBackCD', 7)
        if self.isLowLvFree:
            isFree = True
        else:
            isFree = utils.getNow() - self.transferInfo.get('tTransfer', 0) < schoolTransferBackCD * const.SECONDS_PER_DAY
        self.uiAdapter.schoolTransferCondition.show(self.selectedSchool, self.isLowLvFree, isFree)
        self.hide()

    def updateTransferInfo(self, transferInfo):
        self.transferInfo = transferInfo

    def addLowLvFreePush(self):
        if not gameglobal.rds.configData.get('enableLowLvFreeSchoolTransfer', False):
            return
        self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_LOW_LV_FREE_SCHOOL_TRANSFER)

    def clickLowLvFreePush(self):
        self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_LOW_LV_FREE_SCHOOL_TRANSFER)
        title = STCD.data.get('lowLvFreeSchoolTransferPushTitle', '')
        msg = STCD.data.get('lowLvFreeSchoolTransferPushDesc', '')
        seekId = STCD.data.get('lowLvFreeSchoolTransferPushSeekId', 0)
        yesBtnText = gameStrings.SCHOOL_TRANSFER_SELECT_PUSH_YES_BTN_LABEL
        self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(uiUtils.findPosWithAlert, seekId), yesBtnText=yesBtnText, title=title)
