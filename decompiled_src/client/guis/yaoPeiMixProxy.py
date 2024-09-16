#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/yaoPeiMixProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import uiUtils
import events
import ui
import const
from uiProxy import SlotDataProxy
from ui import unicode2gbk
from data import yaopei_mix_data as YMD
from cdata import game_msg_def_data as GMDD
MIX_READY = 1
MIX_WAITING = 2
MIX_FINISH = 3

class YaoPeiMixProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(YaoPeiMixProxy, self).__init__(uiAdapter)
        self.bindType = 'yaoPeiMix'
        self.type = 'yaoPeiMix'
        self.modelMap = {'confirm': self.onConfirm,
         'removeItem': self.onRemoveItem}
        self.mediator = None
        self.resPos = None
        self.mixState = MIX_READY
        self.realItem = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_YAOPEI_MIX, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_YAOPEI_MIX:
            self.mediator = mediator
            self.refreshInfo()
        BigWorld.callback(0.1, gameglobal.rds.ui.inventory.updateCurrentPageSlotState)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_YAOPEI_MIX)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def reset(self):
        self.mixState = MIX_READY
        self.realItem = None
        self.removeItem(False)

    def show(self):
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_YAOPEI_MIX)

    def refreshInfo(self):
        if self.mediator:
            self.mixState = MIX_READY
            p = BigWorld.player()
            info = {}
            btnEnabled = True
            if self.resPos:
                info['hasRes'] = True
                srcItem = p.inv.getQuickVal(self.resPos[0], self.resPos[1])
                info['itemInfo'] = uiUtils.getGfxItemById(srcItem.id)
                cash = YMD.data.get(srcItem.id, {}).get('cash', 0)
                if p.cash < cash:
                    extraCash = uiUtils.toHtml(format(cash, ','), '#F43804')
                    btnEnabled = False
                else:
                    extraCash = format(cash, ',')
                info['extraCash'] = extraCash
            else:
                info['hasRes'] = False
                btnEnabled = False
                info['hint'] = uiUtils.getTextFromGMD(GMDD.data.YAOPEI_MIX_HINT, '')
            info['btnLabel'] = gameStrings.TEXT_YAOPEIMIXPROXY_80
            info['btnEnabled'] = btnEnabled
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def mixFinish(self, ok, page, pos):
        if ok:
            self.mixSuccess(page, pos)
        else:
            self.refreshInfo()

    def mixSuccess(self, page, pos):
        self.removeItem(False)
        if self.mediator:
            self.mixState = MIX_FINISH
            info = {}
            self.realItem = BigWorld.player().inv.getQuickVal(page, pos)
            info['itemInfo'] = uiUtils.getGfxItem(self.realItem)
            info['hint'] = gameStrings.TEXT_YAOPEIMIXPROXY_99 % uiUtils.getItemColorNameByItem(self.realItem)
            info['btnLabel'] = gameStrings.TEXT_YAOPEIMIXPROXY_100
            self.mediator.Invoke('mixSuccess', uiUtils.dict2GfxDict(info, True))

    def onConfirm(self, *arg):
        label = unicode2gbk(arg[3][0].GetString())
        if label == gameStrings.TEXT_YAOPEIMIXPROXY_100:
            self.removeItem(True)
        elif self.resPos:
            self.mixState = MIX_WAITING
            BigWorld.player().cell.yaoPeiMix(self.resPos[0], self.resPos[1])

    def onRemoveItem(self, *arg):
        if self.mixState != MIX_READY:
            return
        self.removeItem(True)

    def getSlotID(self, key):
        return (0, 0)

    def setItem(self, srcBar, srcSlot):
        if self.mixState != MIX_READY:
            return
        p = BigWorld.player()
        if p.inv.getQuickVal(srcBar, srcSlot).hasLatch():
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
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
            if item.isYaoPeiMixMaterial():
                return (page, pos) == self.resPos
            else:
                return True
        else:
            return False

    @ui.uiEvent(uiConst.WIDGET_YAOPEI_MIX, events.EVENT_INVENTORY_ITEM_CLICKED)
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
            if srcItem.isYaoPeiMixMaterial():
                self.setItem(nPageSrc, nItemSrc)

    def onGetToolTip(self, *arg):
        return gameglobal.rds.ui.inventory.GfxToolTip(self.realItem)
