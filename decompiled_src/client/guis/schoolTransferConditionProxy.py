#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/schoolTransferConditionProxy.o
from gamestrings import gameStrings
import BigWorld
import utils
import gameglobal
import uiConst
import events
import const
import uiUtils
import gameconfigCommon
from uiProxy import UIProxy
from guis.asObject import ASUtils
from data import school_transfer_config_data as STCD
from data import school_transfer_condition_show_data as STCSD
from cdata import game_msg_def_data as GMDD
CTYPE_NORMAL = 1
CTYPE_ITEM = 2
CTYPE_CASH = 3
CTYPE_EXP = 4
MODE_NORMAL = 1
MODE_LOW_LV_FREE = 2

class SchoolTransferConditionProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SchoolTransferConditionProxy, self).__init__(uiAdapter)
        self.widget = None
        self.conditionDict = {}
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SCHOOL_TRANSFER_CONDITION, self.hideNpcPanel)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SCHOOL_TRANSFER_CONDITION:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SCHOOL_TRANSFER_CONDITION)

    def reset(self):
        self.selectedSchool = const.SCHOOL_DEFAULT
        self.isLowLvFree = False
        self.isFree = False

    def clearAll(self):
        self.conditionDict = {}

    def hideNpcPanel(self):
        self.hide()
        if self.uiAdapter.funcNpc.isOnFuncState():
            self.uiAdapter.funcNpc.close()

    def show(self, selectedSchool, isLowLvFree, isFree):
        if not gameglobal.rds.configData.get('enableSchoolTransfer', False):
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.SCHOOL_TRANSFER_DISABLED, ())
            return
        if isLowLvFree and not gameglobal.rds.configData.get('enableLowLvFreeSchoolTransfer', False):
            return
        self.selectedSchool = selectedSchool
        self.isLowLvFree = isLowLvFree
        self.isFree = isFree
        if self.widget:
            self.refreshInfo()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SCHOOL_TRANSFER_CONDITION)

    def initUI(self):
        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.handleClickCloseBtn, False, 0, True)
        self.widget.backBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBackBtn, False, 0, True)
        self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleClickConfirmBtn, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            btnEnabled = True
            firstList = []
            secondList = []
            for key, value in STCSD.data.iteritems():
                showMode = value.get('showMode', 0)
                if showMode == MODE_NORMAL and self.isLowLvFree:
                    continue
                elif showMode == MODE_LOW_LV_FREE and not self.isLowLvFree:
                    continue
                ctype = value.get('ctype', 0)
                conditionList = value.get('conditionList', ())
                itemId = value.get('itemId', 0)
                if ctype == CTYPE_NORMAL:
                    state = 'normal'
                    if self.checkCondition(conditionList):
                        desc = value.get('rightDesc', '')
                        flag = 'complete'
                    else:
                        desc = value.get('errorDesc', '')
                        flag = 'fail'
                elif ctype == CTYPE_ITEM and not self.isFree:
                    if gameconfigCommon.enableSchoolTransferConditionItemCost():
                        continue
                    state = 'item'
                    own = p.inv.countItemInPages(itemId, enableParentCheck=True)
                    need = self.getItemCostNum(itemId)
                    if need <= 0:
                        continue
                    if own >= need:
                        desc = '%s/%s' % (format(own, ','), format(need, ','))
                        flag = 'complete'
                    else:
                        desc = '%s/%s' % (uiUtils.toHtml(format(own, ','), '#F43804'), format(need, ','))
                        flag = 'fail'
                elif ctype == CTYPE_CASH and not self.isFree:
                    state = 'cash'
                    need = STCD.data.get('cash', 0)
                    if self.checkCondition(conditionList):
                        desc = gameStrings.TEXT_SCHOOLTRANSFERCONDITIONPROXY_132 % format(need, ',')
                        flag = 'complete'
                    else:
                        desc = gameStrings.TEXT_SCHOOLTRANSFERCONDITIONPROXY_132 % uiUtils.toHtml(format(need, ','), '#F43804')
                        flag = 'fail'
                elif ctype == CTYPE_EXP and not self.isFree:
                    state = 'cash'
                    need = STCD.data.get('expXiuWei', 0)
                    if self.checkCondition(conditionList):
                        desc = gameStrings.TEXT_SCHOOLTRANSFERCONDITIONPROXY_142 % format(need, ',')
                        flag = 'complete'
                    else:
                        desc = gameStrings.TEXT_SCHOOLTRANSFERCONDITIONPROXY_142 % uiUtils.toHtml(format(need, ','), '#F43804')
                        flag = 'fail'
                else:
                    continue
                itemInfo = {}
                itemInfo['sortIdx'] = key
                itemInfo['state'] = state
                itemInfo['desc'] = desc
                itemInfo['itemId'] = itemId
                itemInfo['flag'] = flag
                if flag == 'fail':
                    btnEnabled = False
                if value.get('isPrecondition', 0):
                    firstList.append(itemInfo)
                else:
                    secondList.append(itemInfo)

            if gameconfigCommon.enableSchoolTransferConditionItemCost():
                info = []
                info.append(gameglobal.rds.ui.schoolTransferSelect.transferInfo.get('school', 0))
                info.append(gameglobal.rds.ui.schoolTransferSelect.transferInfo.get('tSchool', 0))
                info.append(gameglobal.rds.ui.schoolTransferSelect.transferInfo.get('tTransfer', 0))
                info.append(gameglobal.rds.ui.schoolTransferSelect.transferInfo.get('hasReverted', -1))
                if not (info[0] or info[1] or info[2] or info[3]):
                    info = None
                needList = utils.genSchoolTransferItemCost(self.selectedSchool, info)
                if gameglobal.rds.ui.schoolTransferSelect.transferInfo.get('school', 0) == self.selectedSchool and gameglobal.rds.ui.schoolTransferSelect.transferInfo.get('hasReverted', -1) == 0:
                    now = utils.getNow()
                    lastTransferTime = gameglobal.rds.ui.schoolTransferSelect.transferInfo.get('tTransfer', 0)
                    lastDay = (now - lastTransferTime) / const.SECONDS_PER_DAY
                    if lastDay < 7:
                        needList = ()
                if self.isLowLvFree:
                    needList = ()
                sortIdx = 0
                for key in needList:
                    state = 'item'
                    itemId = key[0]
                    need = key[1]
                    own = p.inv.countItemInPages(itemId, enableParentCheck=True)
                    if own >= need:
                        desc = '%s/%s' % (format(own, ','), format(need, ','))
                        flag = 'complete'
                    else:
                        desc = '%s/%s' % (uiUtils.toHtml(format(own, ','), '#F43804'), format(need, ','))
                        flag = 'fail'
                    itemInfo = {}
                    itemInfo['sortIdx'] = sortIdx
                    itemInfo['state'] = state
                    itemInfo['desc'] = desc
                    itemInfo['itemId'] = itemId
                    itemInfo['flag'] = flag
                    if flag == 'fail':
                        btnEnabled = False
                    secondList.append(itemInfo)
                    sortIdx += 1

            firstList.sort(key=lambda x: x['sortIdx'])
            secondList.sort(key=lambda x: x['sortIdx'])
            self.updateDetail(self.widget.scrollWnd.canvas.firstCondition, firstList)
            if len(secondList) > 0:
                self.widget.scrollWnd.canvas.secondCondition.visible = True
                self.widget.scrollWnd.canvas.secondCondition.y = self.widget.scrollWnd.canvas.firstCondition.height + 1
            else:
                self.widget.scrollWnd.canvas.secondCondition.visible = False
                self.widget.scrollWnd.canvas.secondCondition.y = 0
            self.updateDetail(self.widget.scrollWnd.canvas.secondCondition, secondList)
            self.widget.scrollWnd.refreshHeight()
            if not gameglobal.rds.configData.get('enableSchoolTransferConditionCheck', False):
                btnEnabled = True
            self.widget.confirmBtn.enabled = btnEnabled
            return

    def checkCondition(self, conditionList):
        for condition in conditionList:
            if not self.conditionDict.get(condition, False):
                return False

        return True

    def getItemCostNum(self, itemId):
        itemCost = STCD.data.get('schoolTransferItemCost', {}).get(self.selectedSchool, None)
        if itemCost:
            for itemCostId, itemCnt in itemCost:
                if itemCostId == itemId:
                    return itemCnt

        return 0

    def updateDetail(self, mainMc, itemList):
        self.widget.removeAllInst(mainMc.condition)
        posX = 0
        posY = 0
        for i, itemInfo in enumerate(itemList):
            itemMc = self.widget.getInstByClsName('SchoolTransferCondition_DetailItem')
            state = itemInfo.get('state', '')
            desc = itemInfo.get('desc', '')
            itemMc.gotoAndStop(state)
            if state == 'normal':
                itemMc.shortDesc.htmlText = desc
                if itemMc.shortDesc.textWidth > 260:
                    itemMc.shortDesc.visible = False
                    itemMc.longDesc.visible = True
                    itemMc.longDesc.htmlText = desc
                else:
                    itemMc.shortDesc.visible = True
                    itemMc.longDesc.visible = False
            elif state == 'item':
                itemMc.desc.htmlText = desc
                itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(itemInfo.get('itemId', 0)))
                itemMc.slot.dragable = False
            elif state == 'cash':
                itemMc.desc.htmlText = desc
                ASUtils.autoSizeWithFont(itemMc.desc, 15, 270, 8)
                itemMc.desc.y = 19 + (15 - int(itemMc.desc.getTextFormat().size))
            else:
                continue
            itemMc.flag.gotoAndStop(itemInfo.get('flag', ''))
            itemMc.x = posX
            itemMc.y = posY
            if i % 2:
                posX = 0
                posY += 60
            else:
                posX += 321
            mainMc.condition.addChild(itemMc)

        mainMc.bg1.height = mainMc.condition.height + 11

    def updateConditionDict(self, conditionDict):
        self.conditionDict = conditionDict
        self.refreshInfo()

    def handleClickCloseBtn(self, *args):
        self.hideNpcPanel()

    def handleClickBackBtn(self, *args):
        self.uiAdapter.schoolTransferSelect.show(self.selectedSchool, self.isLowLvFree)
        self.hide()

    def handleClickConfirmBtn(self, *args):
        if self.isFree:
            self.trueConfirm()
            return
        p = BigWorld.player()
        lackBindCash = STCD.data.get('cash', 0) > p.bindCash
        lackExpXiuWei = STCD.data.get('expXiuWei', 0) > p.expXiuWei
        if not lackBindCash and not lackExpXiuWei:
            self.trueConfirm()
            return
        if lackBindCash and lackExpXiuWei:
            msg = uiUtils.getTextFromGMD(GMDD.data.SCHOOLTRANSFER_LACK_BINDCASH_EXPXIUWEI, '')
        elif lackBindCash:
            msg = uiUtils.getTextFromGMD(GMDD.data.SCHOOLTRANSFER_LACK_BINDCASH, '')
        elif lackExpXiuWei:
            msg = uiUtils.getTextFromGMD(GMDD.data.SCHOOLTRANSFER_LACK_EXPXIUWEI, '')
        else:
            msg = ''
        self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.trueConfirm)

    def trueConfirm(self):
        self.uiAdapter.schoolTransferHint.show(self.selectedSchool, self.isLowLvFree)
        self.hide()
