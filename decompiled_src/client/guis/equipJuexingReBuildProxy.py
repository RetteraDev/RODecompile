#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/equipJuexingReBuildProxy.o
import copy
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
import utils
from guis import uiConst
from guis import uiUtils
from ui import gbk2unicode
from uiProxy import SlotDataProxy
from item import Item
from guis import ui
from callbackHelper import Functor
from data import item_data as ID
from cdata import font_config_data as FCD
from cdata import equip_juexing_reforge_data as EJRD
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from data import sys_config_data as SCD

class EquipJuexingReBuildProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(EquipJuexingReBuildProxy, self).__init__(uiAdapter)
        self.modelMap = {'checkEquipDiKou': self.onCheckEquipDiKou,
         'refreshContent': self.refreshContent,
         'confirmRebuild': self.confirmRebuild,
         'confirmRebuildNext': self.confirmRebuildNext,
         'gotoWeb': self.onGotoWeb,
         'getTips': self.onGetTips,
         'clickYunchuiBtn': self.onClickYunchuiBtn}
        self.mediator = None
        self.type = 'equipJuexingReBuild'
        self.bindType = 'equipJuexingReBuild'
        self.isShow = False
        self.npcID = 0
        self.itemPage = const.CONT_NO_PAGE
        self.itemPos = const.CONT_NO_POS
        self.nowStage = 0
        self.currentItem = None
        self.contentList = None
        self.selectedPos = 0
        self.itemPage2 = const.CONT_NO_PAGE
        self.itemPos2 = const.CONT_NO_POS
        self.jxData = None
        self.itemUUID = None
        self.wupinID = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_EQUIP_JUEXING_REBUILD, self.clearWidgetByEsc)

    def clearWidgetByEsc(self):
        self.changeStage(0)
        self.clearWidget()

    @ui.callFilter(1)
    def clearWidget(self):
        if self.nowStage == 0:
            self.mediator = None
            self.isShow = False
            self.nowStage = 0
            self.itemPage = const.CONT_NO_PAGE
            self.itemPos = const.CONT_NO_POS
            self.contentList = None
            self.currentItem = None
            self.itemPage2 = const.CONT_NO_PAGE
            self.itemPos2 = const.CONT_NO_POS
            self.jxData = None
            self.itemUUID = None
            self.wupinID = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EQUIP_JUEXING_REBUILD)
            if gameglobal.rds.ui.funcNpc.isOnFuncState():
                gameglobal.rds.ui.funcNpc.close()
            gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
        else:
            txt = uiUtils.getTextFromGMD(GMDD.data.NEW_JUEXING_MISS_CONFIRM)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(txt, Functor(self.trueClear, self.itemPage2, self.itemPos2))

    def onCheckEquipDiKou(self, *args):
        return GfxValue(gameglobal.rds.configData.get('enableEquipDiKou', False))

    def trueClear(self, page, pos):
        if not self.isShow:
            return
        if page == const.CONT_NO_PAGE or pos == const.CONT_NO_POS:
            return
        BigWorld.player().cell.confirmReforgeEquipJuexingAll(False, page, pos, self.itemUUID)
        self.changeStage(0)

    def changeStage(self, stage):
        self.nowStage = stage
        if self.mediator:
            self.mediator.Invoke('setNowStage', GfxValue(stage))

    def showConfirmContent(self, page, pos, jxData, itemUUID):
        self.itemPage2 = page
        self.itemPos2 = pos
        self.jxData = jxData
        self.itemUUID = itemUUID
        self.currentItem2 = BigWorld.player().inv.getQuickVal(page, pos)
        if self.mediator:
            self.refreshContentStage2()
        else:
            self.show(self.npcID, 1)

    def refreshContentStage2(self):
        if not self.currentItem2:
            return
        contentList = uiUtils.buildJuexingContentList(self.currentItem2)
        key = self._getKey(1, 0)
        self.bindingData[key] = self.currentItem2
        key2 = self._getKey(1, 1)
        nowItem = copy.deepcopy(self.currentItem2)
        for value in self.jxData:
            nowItem.enhJuexingData[value[0]] = value[1]

        self.bindingData[key2] = nowItem
        iconPath = uiUtils.getItemIconFile64(self.currentItem2.id)
        data = {'iconPath': iconPath}
        self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data))
        self.binding[key2][1].InvokeSelf(uiUtils.dict2GfxDict(data))
        if hasattr(self.currentItem2, 'quality'):
            quality = self.currentItem2.quality
        else:
            quality = ID.data.get(self.currentItem2.id, {}).get('quality', 1)
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

        self.mediator.Invoke('setContentInfoStage2', (uiUtils.array2GfxAarry(fromTextList, True), uiUtils.array2GfxAarry(toTextList, True)))
        juexingDataList = getattr(self.currentItem2, 'enhJuexingData', {})
        maxJuexingLv = 0
        for key in juexingDataList:
            if juexingDataList[key]:
                if key > maxJuexingLv:
                    maxJuexingLv = key

        rd = EJRD.data.get(maxJuexingLv)
        itemNeed = rd.get('itemNeed', [])
        pos = 0
        ok = True
        materialItemId, needNum = itemNeed[0]
        key = self._getKey(1, 2)
        count = BigWorld.player().inv.countItemInPages(materialItemId, enableParentCheck=True)
        data = uiUtils.getGfxItemById(materialItemId, count)
        self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data))
        if count < needNum:
            useStr = "<font color =\'#FB0000\'>%d</font>/%d" % (count, needNum)
        else:
            useStr = '%d/%d' % (count, needNum)
        if gameglobal.rds.configData.get('enableEquipDiKou', False):
            itemDict = {materialItemId: needNum}
            self.refreshDiKouInfo(itemDict)
            if not uiUtils.checkEquipMaterialDiKou(itemDict):
                ok = False
        elif count < needNum:
            ok = False
        self.mediator.Invoke('setIndexValue2', (GfxValue(pos), GfxValue(gbk2unicode(useStr))))
        if ok == True:
            self.mediator.Invoke('setHint', (GfxValue(gbk2unicode('')), GfxValue(1)))
            self.mediator.Invoke('enableConfirm', (GfxValue(True), GfxValue(1)))
        else:
            self.mediator.Invoke('setHint', (GfxValue(gbk2unicode('材料不足')), GfxValue(1)))
            self.mediator.Invoke('enableConfirm', (GfxValue(False), GfxValue(1)))
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def show(self, npcID, nowStage = 0):
        self.npcID = npcID
        self.nowStage = nowStage
        if not self.isShow:
            self.isShow = True
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EQUIP_JUEXING_REBUILD)

    def checkTempJXData(self):
        p = BigWorld.player()
        for i, j, _ in p.inv.xItems():
            item = p.inv.getQuickVal(i, j)
            if item and hasattr(item, 'tempJXAlldata'):
                return (item, i, j)

        return (None, -1, -1)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_EQUIP_JUEXING_REBUILD:
            self.mediator = mediator
        BigWorld.callback(0.1, gameglobal.rds.ui.inventory.updateCurrentPageSlotState)

    def setItem(self, nPageSrc, nItemSrc, srcIt):
        if not self.mediator or not self.binding or self.nowStage == 1:
            return
        self.itemPage = nPageSrc
        self.itemPos = nItemSrc
        key = self._getKey(0, 0)
        self.bindingData[key] = srcIt
        self.currentItem = copy.deepcopy(BigWorld.player().inv.getQuickVal(nPageSrc, nItemSrc))
        data = uiUtils.getGfxItem(self.currentItem, location=const.ITEM_IN_BAG)
        self.wupinID = data['id']
        self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data))
        if self.mediator:
            self.mediator.Invoke('showItemType', (GfxValue(0), GfxValue(False)))
        contentList = uiUtils.buildJuexingContentList(srcIt)
        self.contentList = contentList
        txtList = []
        for item in contentList:
            txtList.append([item[1],
             item[3],
             item[2],
             item[4]])

        if self.mediator != None:
            self.mediator.Invoke('setContentInfo', uiUtils.array2GfxAarry(txtList, True))
        self.trueSelect(0)
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def onGotoWeb(self, *args):
        if self.wupinID:
            url = SCD.data.get('WEB_WUPIN_SEARCH', uiConst.WEB_WUPIN_SEARCH)
            url = url % self.wupinID
        else:
            url = SCD.data.get('WEB_INDEX_SEARCH', uiConst.WEB_INDEX_SEARCH)
        BigWorld.openUrl(url)

    def refreshSelect(self):
        self.trueSelect(self.selectedPos)

    def trueSelect(self, index):
        if not self.mediator:
            return
        self.selectedPos = index
        key = self._getKey(0, 0)
        srcIt = self.bindingData[key]
        juexingDataList = getattr(srcIt, 'enhJuexingData', {})
        maxJuexingLv = 0
        for key in juexingDataList:
            if juexingDataList[key]:
                if key > maxJuexingLv:
                    maxJuexingLv = key

        rd = EJRD.data.get(maxJuexingLv)
        if not rd:
            self.mediator.Invoke('setHint', (GfxValue(gbk2unicode('觉醒等级不匹配,当前装备不能重铸')), GfxValue(0)))
            self.mediator.Invoke('enableConfirm', (GfxValue(False), GfxValue(0)))
            return
        itemNeed = rd.get('itemNeed', [])
        if not itemNeed:
            self.mediator.Invoke('setHint', (GfxValue(gbk2unicode('觉醒等级不匹配,当前装备不能重铸')), GfxValue(0)))
            self.mediator.Invoke('enableConfirm', (GfxValue(False), GfxValue(0)))
            return
        pos = 0
        ok = True
        for i in xrange(1, 2):
            key = self._getKey(0, i)
            self.bindingData[key] = None
            data = GfxValue(0)
            data.SetNull()
            self.binding[key][1].InvokeSelf(data)
            self.binding[key][0].Invoke('setSlotColor', GfxValue('nothing'))
            if i != 0:
                self.mediator.Invoke('setIndexValue', (GfxValue(i), GfxValue(gbk2unicode(''))))
                self.mediator.Invoke('showItemType', (GfxValue(i), GfxValue(True)))

        materialItemId, needNum = itemNeed[0]
        result = BigWorld.player().inv.countItemChild(materialItemId)
        if result[0] > 0:
            materialItem = Item(result[1][0])
        else:
            materialItem = Item(materialItemId)
        key = self._getKey(0, pos + 1)
        self.bindingData[key] = materialItem
        count = BigWorld.player().inv.countItemInPages(materialItemId, enableParentCheck=True)
        data = uiUtils.getGfxItemById(materialItemId, count)
        self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data))
        if count < needNum:
            useStr = "<font color =\'#FB0000\'>%d</font>/%d" % (count, needNum)
        else:
            useStr = '%d/%d' % (count, needNum)
        if gameglobal.rds.configData.get('enableEquipDiKou', False):
            itemDict = {materialItemId: needNum}
            self.refreshDiKouInfo(itemDict)
            if not uiUtils.checkEquipMaterialDiKou(itemDict):
                ok = False
        elif count < needNum:
            ok = False
        self.mediator.Invoke('showItemType', (GfxValue(pos), GfxValue(False)))
        self.mediator.Invoke('setIndexValue', (GfxValue(pos), GfxValue(gbk2unicode(useStr))))
        if ok == True:
            self.mediator.Invoke('setHint', (GfxValue(gbk2unicode('')), GfxValue(0)))
            self.mediator.Invoke('enableConfirm', (GfxValue(True), GfxValue(0)))
        else:
            self.mediator.Invoke('setHint', (GfxValue(gbk2unicode('材料不足')), GfxValue(0)))
            self.mediator.Invoke('enableConfirm', (GfxValue(False), GfxValue(0)))
        self.mediator.Invoke('refreshSlotItem', ())

    def removeItem(self):
        self.itemPage = const.CONT_NO_PAGE
        self.itemPos = const.CONT_NO_POS
        self.currentItem = None
        for i in xrange(0, 2):
            key = self._getKey(0, i)
            self.bindingData[key] = None
            data = GfxValue(0)
            data.SetNull()
            self.binding[key][1].InvokeSelf(data)
            self.binding[key][0].Invoke('setSlotColor', GfxValue('nothing'))
            if i != 0:
                self.mediator.Invoke('setIndexValue', (GfxValue(i), GfxValue(gbk2unicode(''))))
            self.mediator.Invoke('showItemType', (GfxValue(i), GfxValue(True)))

        txtList = []
        if self.mediator != None:
            self.mediator.Invoke('setContentInfo', uiUtils.array2GfxAarry(txtList, True))
        self.contentList = None
        self.mediator.Invoke('setHint', (GfxValue(gbk2unicode('请放入带觉醒效果的装备')), GfxValue(0)))
        self.mediator.Invoke('enableConfirm', (GfxValue(False), GfxValue(0)))
        self.refreshDiKouInfo({})
        self.refreshContent()
        self.wupinID = None

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[19:]), int(idItem[4:]))

    def _getKey(self, bar, slot):
        return 'equipJuexingReBuild%d.slot%d' % (bar, slot)

    def refreshContent(self, *args):
        if self.nowStage == 0:
            if self.currentItem == None:
                self.mediator.Invoke('setHint', (GfxValue(gbk2unicode('请放入带觉醒效果的装备')), GfxValue(0)))
                gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
            else:
                srcIt = BigWorld.player().inv.getQuickVal(self.itemPage, self.itemPos)
                if srcIt:
                    self.setItem(self.itemPage, self.itemPos, srcIt)
        else:
            self.refreshContentStage2()

    def refreshDiKouInfo(self, itemDict):
        if not gameglobal.rds.configData.get('enableEquipDiKou', False):
            return
        if self.mediator:
            info = {}
            if itemDict != {}:
                p = BigWorld.player()
                _, yunchuiNeed, _, _ = utils.calcEquipMaterialDiKou(p, itemDict)
                yunchuiOwn = p.getFame(const.YUN_CHUI_JI_FEN_FAME_ID)
                if yunchuiNeed > yunchuiOwn:
                    info['yunchui'] = '%s/%s' % (uiUtils.toHtml(format(yunchuiOwn, ','), '#FB0000'), format(yunchuiNeed, ','))
                    info['yunchuiEnabled'] = True
                else:
                    info['yunchui'] = '%s/%s' % (format(yunchuiOwn, ','), format(yunchuiNeed, ','))
                    info['yunchuiEnabled'] = False
                info['visible'] = True
            else:
                info['visible'] = False
            self.mediator.Invoke('refreshDiKouInfo', uiUtils.dict2GfxDict(info, True))

    @ui.callFilter(1)
    def confirmRebuildNext(self, *args):
        txt = uiUtils.getTextFromGMD(GMDD.data.NEW_JUEXING_MISS_CONFIRM)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(txt, Functor(self.confrimRebuildStage0, 0))

    def confrimRebuildStage0(self, index):
        enhLv = self.contentList[index][0]
        if gameglobal.rds.configData.get('enableEquipDiKou', False):
            key = self._getKey(0, 0)
            srcIt = self.bindingData[key]
            if not srcIt:
                key = self._getKey(1, 0)
                srcIt = self.bindingData[key]
            if not srcIt:
                return
            juexingDataList = getattr(srcIt, 'enhJuexingData', {})
            maxJuexingLv = 0
            for key in juexingDataList:
                if juexingDataList[key]:
                    if key > maxJuexingLv:
                        maxJuexingLv = key

            rd = EJRD.data.get(maxJuexingLv)
            itemNeed = rd.get('itemNeed', [])
            materialItemId, needNum = itemNeed[0]
            itemDict = {materialItemId: needNum}
            _, yunchuiNeed, _, _ = utils.calcEquipMaterialDiKou(BigWorld.player(), itemDict)
            if yunchuiNeed > 0 and not self.currentItem.isForeverBind():
                msg = uiUtils.getTextFromGMD(GMDD.data.ENHANCE_BIND_CONFIRM)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.trueConfirm, enhLv))
                return
        if self.isMaterialBinded():
            if not self.currentItem.isForeverBind():
                msg = uiUtils.getTextFromGMD(GMDD.data.ENHANCE_BIND_CONFIRM)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.trueConfirm, enhLv))
            else:
                self.trueConfirm(enhLv)
        else:
            self.trueConfirm(enhLv)

    @ui.callFilter(1)
    def confirmRebuild(self, *args):
        if self.nowStage == 0:
            index = int(args[3][0].GetNumber())
            self.confrimRebuildStage0(index)
        else:
            txt = uiUtils.getTextFromGMD(GMDD.data.OLD_JUEXING_MISS_CONFIRM)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(txt, Functor(self.trueConfirm2, self.itemPage2, self.itemPos2))

    def trueConfirm2(self, page, pos):
        if page == const.CONT_NO_PAGE or pos == const.CONT_NO_POS:
            return
        BigWorld.player().cell.confirmReforgeEquipJuexingAll(True, page, pos, self.itemUUID)
        self.changeStage(0)

    def trueConfirm(self, enhLv):
        npcEnt = BigWorld.entities.get(self.npcID)
        npcEnt and npcEnt.cell.reforgeEquipJuexingAll(self.itemPage, self.itemPos)

    def isMaterialBinded(self):
        target = self.contentList[self.selectedPos]
        rd = EJRD.data.get(target[0])
        if not rd:
            return
        itemNeed = rd.get('itemNeed', [])
        if not itemNeed:
            return
        for item in itemNeed:
            materialItemId = item[0]
            mItem = Item(materialItemId)
            ret = BigWorld.player().inv.countItemBind(mItem.getParentId(), enableParentCheck=True)
            if ret:
                return ret

        return False

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        if self.bindingData.has_key(key):
            return gameglobal.rds.ui.inventory.GfxToolTip(self.bindingData[key])
        else:
            return GfxValue('')

    def onNotifySlotUse(self, *args):
        nPage, nItem = self.getSlotID(args[3][0].GetString())
        if nItem == 0:
            self.removeItem()

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator and kind == const.RES_KIND_INV:
            if item:
                if not item.isItemCanRebuild() or self.nowStage == 1:
                    return True
                if self.itemPage == page and self.itemPos == pos:
                    return True
        return False

    def onGetTips(self, *args):
        tips = GMD.data.get(GMDD.data.EQUIP_JUEXING_TIPS, {}).get('text', '可携带的精炼觉醒属性查询')
        self.gameOnOff()
        return GfxValue(gbk2unicode(tips))

    def gameOnOff(self):
        if gameglobal.rds.configData.get('enableEquipGotoWeb', False) and self.mediator:
            self.mediator.Invoke('gotoWebBtnVisible', GfxValue(True))
        else:
            self.mediator.Invoke('gotoWebBtnVisible', GfxValue(False))

    def onClickYunchuiBtn(self, *args):
        mall = gameglobal.rds.ui.tianyuMall
        if mall.mallMediator:
            mall.hide()
        mall.show(keyWord='云垂积分')
