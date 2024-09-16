#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/yaoPeiReforgeProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import uiUtils
import events
import ui
import const
from uiProxy import SlotDataProxy
from data import prop_ref_data as PRD
from cdata import game_msg_def_data as GMDD
from cdata import yao_pei_reforge_data as YPRD
REFORGE_READY = 1
REFORGE_WAITING = 2
REFORGE_FINISH = 3

class YaoPeiReforgeProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(YaoPeiReforgeProxy, self).__init__(uiAdapter)
        self.bindType = 'yaoPeiReforge'
        self.type = 'yaoPeiReforge'
        self.modelMap = {'getExtraInfo': self.onGetExtraInfo,
         'confirm': self.onConfirm,
         'removeItem': self.onRemoveItem}
        self.mediator = None
        self.resPos = None
        self.reforgeState = REFORGE_READY
        self.oldVal = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_YAOPEI_REFORGE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_YAOPEI_REFORGE:
            self.mediator = mediator
            self.refreshInfo()
        BigWorld.callback(0.1, gameglobal.rds.ui.inventory.updateCurrentPageSlotState)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_YAOPEI_REFORGE)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def reset(self):
        self.reforgeState = REFORGE_READY
        self.removeItem(False)

    def show(self):
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_YAOPEI_REFORGE)

    def refreshInfo(self, selectedIdx = -1):
        if self.mediator:
            self.reforgeState = REFORGE_READY
            p = BigWorld.player()
            info = {}
            defaultIdx = selectedIdx
            extraPropList = []
            if self.resPos:
                srcItem = p.inv.getQuickVal(self.resPos[0], self.resPos[1])
                info['itemInfo'] = uiUtils.getGfxItem(srcItem)
                maxActivatedLv = srcItem.calcMaxYaoPeiLv()
                yaoPeiLv = srcItem.getYaoPeiLv()
                idx = 0
                perfectIdx = -1
                for prop in srcItem.yaoPeiExtraProps:
                    propInfo = {}
                    propText = self.createPropText(prop[0], prop[1], prop[2], prop[3], prop[4], prop[5] <= maxActivatedLv)
                    if prop[5] <= yaoPeiLv:
                        propInfo['enabled'] = True
                        if prop[2] < prop[4]:
                            propText = uiUtils.toHtml(propText, '#FFFFE7')
                            if defaultIdx == -1:
                                defaultIdx = idx
                        else:
                            propText = uiUtils.toHtml(propText, '#79C725')
                            if perfectIdx == -1:
                                perfectIdx = idx
                    else:
                        propInfo['enabled'] = False
                        propText = uiUtils.toHtml(propText, '#808080')
                    propInfo['propText'] = propText
                    extraPropList.append(propInfo)
                    idx += 1

                if defaultIdx == -1:
                    defaultIdx = perfectIdx
                hint = uiUtils.getTextFromGMD(GMDD.data.YAOPEI_REFORGE_NO_ACTIVATE_HINT, gameStrings.TEXT_YAOPEIREFORGEPROXY_97)
            else:
                hint = uiUtils.getTextFromGMD(GMDD.data.YAOPEI_REFORGE_HINT, gameStrings.TEXT_YAOPEIREFORGEPROXY_99)
            info['defaultIdx'] = defaultIdx
            info['extraPropList'] = extraPropList
            info['hint'] = hint
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def createPropText(self, pId, pType, pVal, minVal, maxVal, activated):
        prd = PRD.data.get(pId, {})
        propName = prd.get('name', '')
        showType = prd.get('showType', 0)
        if activated:
            pVal = uiUtils.formatProp(pVal, pType, showType)
            text = '%s +%s' % (propName, pVal)
        else:
            minVal = uiUtils.formatProp(minVal, pType, showType)
            maxVal = uiUtils.formatProp(maxVal, pType, showType)
            text = '%s +(%s-%s)' % (propName, minVal, maxVal)
        return text

    def onGetExtraInfo(self, *arg):
        idx = int(arg[3][0].GetNumber())
        if self.mediator:
            p = BigWorld.player()
            info = {}
            srcItem = p.inv.getQuickVal(self.resPos[0], self.resPos[1])
            if idx >= len(srcItem.yaoPeiExtraProps):
                return
            _, _, pVal, _, maxVal, lv = srcItem.yaoPeiExtraProps[idx]
            rData = YPRD.data.get(lv, None)
            if pVal < maxVal and rData:
                info['extraVisible'] = True
                btnEnabled = True
                itemNeed = rData.get('itemNeed')
                if itemNeed:
                    itemId, needNum = itemNeed
                    info['itemInfo'] = uiUtils.getGfxItemById(itemId)
                    ownNum = p.inv.countItemInPages(itemId, enableParentCheck=True)
                    if ownNum < needNum:
                        info['num'] = "<font color = \'#F43804\'>%d/%d</font>" % (ownNum, needNum)
                        btnEnabled = False
                    else:
                        info['num'] = '%d/%d' % (ownNum, needNum)
                cash = rData.get('cash', 0)
                if p.cash < cash:
                    extraCash = uiUtils.toHtml(format(cash, ','), '#F43804')
                    btnEnabled = False
                else:
                    extraCash = format(cash, ',')
                info['extraCash'] = extraCash
                info['btnEnabled'] = btnEnabled
            else:
                info['extraVisible'] = False
                info['hint'] = uiUtils.getTextFromGMD(GMDD.data.YAOPEI_REFORGE_MAX_VALUE_HINT, gameStrings.TEXT_YAOPEIREFORGEPROXY_160)
            self.mediator.Invoke('refreshExtraInfo', uiUtils.dict2GfxDict(info, True))

    def reforgeFinish(self, ok, page, pos, idx, nVal):
        if ok:
            item = BigWorld.player().inv.getQuickVal(page, pos)
            gameglobal.rds.ui.yaoPeiReforgeResult.show(item, idx, self.oldVal, nVal)
        self.refreshInfo(idx)

    def onConfirm(self, *arg):
        idx = int(arg[3][0].GetNumber())
        self.reforgeState = REFORGE_WAITING
        p = BigWorld.player()
        item = p.inv.getQuickVal(self.resPos[0], self.resPos[1])
        if idx >= len(item.yaoPeiExtraProps):
            return
        self.oldVal = item.yaoPeiExtraProps[idx][2]
        p.cell.reforgeYaoPei(self.resPos[0], self.resPos[1], idx)

    def onRemoveItem(self, *arg):
        if self.reforgeState != REFORGE_READY:
            return
        self.removeItem(True)

    def getSlotID(self, key):
        return (0, 0)

    def setItem(self, srcBar, srcSlot):
        if self.reforgeState != REFORGE_READY:
            return
        p = BigWorld.player()
        srcItem = p.inv.getQuickVal(srcBar, srcSlot)
        if srcItem.hasLatch():
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        if len(srcItem.yaoPeiExtraProps) <= 0:
            p.showGameMsg(GMDD.data.YAOPEI_REFORGE_NO_EXTRA_PROPS, ())
            return
        self.removeItem(False)
        self.resPos = (srcBar, srcSlot)
        gameglobal.rds.ui.inventory.updateSlotState(srcBar, srcSlot)
        self.refreshInfo()

    def removeItem(self, needRefresh):
        if self.resPos:
            page, pos = self.resPos
            self.resPos = None
            gameglobal.rds.ui.inventory.updateSlotState(page, pos)
        if needRefresh:
            self.refreshInfo()

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator and kind == const.RES_KIND_INV:
            if item.isYaoPei():
                return (page, pos) == self.resPos
            else:
                return True
        else:
            return False

    @ui.uiEvent(uiConst.WIDGET_YAOPEI_REFORGE, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onInventoryRightClick(self, event):
        event.stop()
        i = event.data['item']
        nPage = event.data['page']
        nItem = event.data['pos']
        if i == None:
            return
        else:
            self.setInventoryItem(nPage, nItem)
            return

    def setInventoryItem(self, nPageSrc, nItemSrc):
        p = BigWorld.player()
        srcItem = p.inv.getQuickVal(nPageSrc, nItemSrc)
        if srcItem:
            if srcItem.isYaoPei():
                self.setItem(nPageSrc, nItemSrc)

    def onGetToolTip(self, *arg):
        item = BigWorld.player().inv.getQuickVal(self.resPos[0], self.resPos[1]) if self.resPos else None
        return gameglobal.rds.ui.inventory.GfxToolTip(item)
