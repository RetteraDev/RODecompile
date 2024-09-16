#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/equipJuexingConfirmProxy.o
import copy
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
from guis import uiConst
from guis import uiUtils
from uiProxy import SlotDataProxy
from guis import ui
from callbackHelper import Functor
from data import item_data as ID
from cdata import font_config_data as FCD
from cdata import game_msg_def_data as GMDD

class EquipJuexingConfirmProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(EquipJuexingConfirmProxy, self).__init__(uiAdapter)
        self.modelMap = {'refreshContent': self.refreshContent,
         'confirmRebuild': self.confirmRebuild}
        self.mediator = None
        self.type = 'equipJuexingConfirm'
        self.bindType = 'equipJuexingConfirm'
        self.isShow = False
        self.itemPage = const.CONT_NO_PAGE
        self.itemPos = const.CONT_NO_POS
        self.currentItem = None
        self.afterItem = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_EQUIP_JUEXING_CONFIRM, self.clearWidget)

    def confirmRebuild(self, *args):
        txt = uiUtils.getTextFromGMD(GMDD.data.OLD_JUEXING_MISS_CONFIRM)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(txt, Functor(self.trueConfirm, self.itemPage, self.itemPos))

    def trueConfirm(self, page, pos):
        if page == const.CONT_NO_PAGE or pos == const.CONT_NO_POS:
            return
        BigWorld.player().cell.confirmReforgeEquipJuexingAll(True, page, pos, self.itemUUID)
        self.closeThis()

    def closeThis(self):
        self.mediator = None
        self.isShow = False
        self.itemPage = const.CONT_NO_PAGE
        self.itemPos = const.CONT_NO_POS
        self.currentItem = None
        self.afterItem = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EQUIP_JUEXING_CONFIRM)
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    @ui.callFilter(1)
    def clearWidget(self):
        txt = uiUtils.getTextFromGMD(GMDD.data.NEW_JUEXING_MISS_CONFIRM)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(txt, Functor(self.trueClear, self.itemPage, self.itemPos))

    def trueClear(self, page, pos):
        if not self.isShow:
            return
        if page == const.CONT_NO_PAGE or pos == const.CONT_NO_POS:
            return
        BigWorld.player().cell.confirmReforgeEquipJuexingAll(False, page, pos, self.itemUUID)
        self.closeThis()

    def show(self, page, pos, jxData, itemUUID):
        self.itemPage = page
        self.itemPos = pos
        self.jxData = jxData
        self.itemUUID = itemUUID
        self.currentItem = BigWorld.player().inv.getQuickVal(page, pos)
        self.selectedPos = gameglobal.rds.ui.equipJuexingReBuild.selectedPos
        if not self.isShow:
            self.isShow = True
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EQUIP_JUEXING_CONFIRM, True)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_EQUIP_JUEXING_CONFIRM:
            self.mediator = mediator

    def refreshContent(self, *args):
        if not self.currentItem:
            return
        contentList = uiUtils.buildJuexingContentList(self.currentItem)
        key = self._getKey(0, 0)
        self.bindingData[key] = self.currentItem
        key2 = self._getKey(0, 1)
        nowItem = copy.deepcopy(self.currentItem)
        for value in self.jxData:
            nowItem.enhJuexingData[value[0]] = value[1]

        self.bindingData[key2] = nowItem
        iconPath = uiUtils.getItemIconFile64(self.currentItem.id)
        data = {'iconPath': iconPath}
        self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data))
        self.binding[key2][1].InvokeSelf(uiUtils.dict2GfxDict(data))
        if hasattr(self.currentItem, 'quality'):
            quality = self.currentItem.quality
        else:
            quality = ID.data.get(self.currentItem.id, {}).get('quality', 1)
        color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
        self.binding[key][0].Invoke('setSlotColor', GfxValue(color))
        self.binding[key2][0].Invoke('setSlotColor', GfxValue(color))
        contentList2 = uiUtils.buildJuexingContentList(nowItem)
        fromTextList = []
        for item in contentList:
            if True in item[2]:
                fromTextList.append([uiUtils.toHtml(item[1], '#808080'), item[3]])
            else:
                fromTextList.append([uiUtils.toHtml(item[1], '#CEBC8A'), item[3]])

        toTextList = []
        for item in contentList2:
            if True in item[2]:
                toTextList.append([uiUtils.toHtml(item[1], '#808080'), item[3]])
            else:
                toTextList.append([uiUtils.toHtml(item[1], '#CEBC8A'), item[3]])

        self.mediator.Invoke('setContentInfo', (uiUtils.array2GfxAarry(fromTextList, True), uiUtils.array2GfxAarry(toTextList, True)))
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[19:]), int(idItem[4:]))

    def _getKey(self, bar, slot):
        return 'equipJuexingConfirm%d.slot%d' % (bar, slot)

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        if self.bindingData.has_key(key):
            return gameglobal.rds.ui.inventory.GfxToolTip(self.bindingData[key])
        else:
            return GfxValue('')

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator and kind == const.RES_KIND_INV:
            return True
        else:
            return False
