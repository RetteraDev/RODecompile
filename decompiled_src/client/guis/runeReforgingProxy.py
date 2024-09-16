#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/runeReforgingProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gametypes
import const
from guis import uiConst
from guis import uiUtils
from guis import events
from ui import gbk2unicode
from uiProxy import SlotDataProxy
from item import Item
from guis import ui
from gameclass import PSkillInfo
from data import item_data as ID
from cdata import font_config_data as FCD
from data import rune_data as RD
from data import rune_qifu_data as RQD
from data import rune_qifu_effect_data as RQED

class RuneReforgingProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(RuneReforgingProxy, self).__init__(uiAdapter)
        self.modelMap = {'closePanel': self.onClosePanel,
         'confirm': self.onConfirm,
         'openInventory': self.onOpenInventory,
         'removeItem': self.onRemoveItem}
        self.mediator = None
        self.type = 'runeReforging'
        self.bindType = 'runeReforging'
        self.source = uiConst.RUNE_SOURCE_INV
        self.runePage = const.CONT_NO_PAGE
        self.runePart = const.CONT_NO_POS
        self.invPage = const.CONT_NO_PAGE
        self.invPos = const.CONT_NO_POS
        self.qiFuLv = uiConst.RUNE_FORGING_LOW_LV
        self.npcId = 0
        self.itemMap = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_RUNE_REFORGING, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_RUNE_REFORGING:
            self.mediator = mediator

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_RUNE_REFORGING)

    def reset(self):
        super(self.__class__, self).reset()
        self.itemMap = {}
        self.source = uiConst.RUNE_SOURCE_INV
        self.runePage = const.CONT_NO_PAGE
        self.runePart = const.CONT_NO_POS
        self.invPage = const.CONT_NO_PAGE
        self.invPos = const.CONT_NO_POS
        self.qiFuLv = uiConst.RUNE_FORGING_LOW_LV
        self.npcId = 0
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
        gameglobal.rds.ui.roleInfo.updateRuneSlotState()

    def show(self, npcId):
        if not self.mediator:
            self.npcId = npcId
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_RUNE_REFORGING)

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[13:]), int(idItem[4:]))

    def _getKey(self, bar, slot):
        return 'runeReforging%d.slot%d' % (bar, slot)

    def onClosePanel(self, *arg):
        self.hide()

    def onConfirm(self, *arg):
        npc = BigWorld.entities.get(self.npcId)
        if npc:
            p = BigWorld.player()
            idList = set(self.itemMap.values())
            posList = []
            for id in idList:
                pg, pos = p.inv.findItemByAttr({'id': id})
                if pg != const.CONT_NO_PAGE:
                    posList.append((pg, pos))

            if posList:
                if self.source == uiConst.RUNE_SOURCE_INV:
                    npc.cell.reforgingRuneInInv(self.invPage, self.invPos, gametypes.RUNE_QIFU_OP_TYPE_REFORGING, self.qiFuLv, posList)
                else:
                    npc.cell.reforgingRuneInRuneBoard(self.runePage, self.runePart, gametypes.RUNE_QIFU_OP_TYPE_REFORGING, self.qiFuLv, posList)

    def onOpenInventory(self, *arg):
        if not gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.show()

    def onRemoveItem(self, *arg):
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        self.removeItem(bar, slot)

    def addReforgingItem(self, item):
        if item.id in self.itemMap.values():
            return
        for i in range(5):
            if i not in self.itemMap:
                self.addItem(item, uiConst.RUNE_REFORGING_ITEM, i)
                return

    def updateItemNum(self, item):
        if self.mediator and item.id in self.itemMap.values():
            for id in self.itemMap:
                if item.id == self.itemMap[id]:
                    self.addItem(item, uiConst.RUNE_REFORGING_ITEM, id)

    def addItem(self, item, page, pos):
        if item is not None:
            if page == uiConst.RUNE_REFORGING_ITEM:
                self.itemMap[pos] = item.id
                self.refreshConfirmBtn()
            if page == uiConst.RUNE_REFORGING_EQUIP and not pos:
                self.refreshRuneEquip()
            key = self._getKey(page, pos)
            if self.binding.get(key, None) is not None:
                data = self.uiAdapter.movie.CreateObject()
                icon = uiUtils.getItemIconFile40(item.id)
                idNum = GfxValue(item.id)
                name = GfxValue('item')
                iconPath = GfxValue(icon)
                if page == uiConst.RUNE_REFORGING_ITEM:
                    count = GfxValue(BigWorld.player().inv.countItemInPages(item.id))
                    data.SetMember('count', count)
                data.SetMember('id', idNum)
                data.SetMember('name', name)
                data.SetMember('iconPath', iconPath)
                if hasattr(item, 'quality'):
                    quality = item.quality
                else:
                    quality = ID.data.get(item.id, {}).get('quality', 1)
                color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                self.binding[key][0].Invoke('setSlotColor', GfxValue(color))
                self.binding[key][1].InvokeSelf(data)

    def removeItem(self, page, pos):
        if page == uiConst.RUNE_REFORGING_EQUIP and not pos:
            if self.source == uiConst.RUNE_SOURCE_INV:
                self.invPage = const.CONT_NO_PAGE
                self.invPos = const.CONT_NO_POS
            else:
                self.runePage = const.CONT_NO_PAGE
                self.runePart = const.CONT_NO_POS
            self.refreshRuneEquip()
        key = self._getKey(page, pos)
        if page == uiConst.RUNE_REFORGING_ITEM and pos in self.itemMap:
            del self.itemMap[pos]
            self.refreshConfirmBtn()
        if self.binding.get(key, None) is not None:
            data = GfxValue(1)
            data.SetNull()
            self.binding[key][0].Invoke('setSlotColor', GfxValue('nothing'))
            self.binding[key][1].InvokeSelf(data)

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        if bar == uiConst.RUNE_REFORGING_ITEM:
            if slot in self.itemMap:
                return gameglobal.rds.ui.inventory.GfxToolTip(Item(self.itemMap[slot]))
        elif not slot:
            i = self.getRuneEquip()
            if i:
                return gameglobal.rds.ui.inventory.GfxToolTip(i)
        return GfxValue('')

    def getEffectText(self, isPreview = False):
        runeText = ''
        i = self.getRuneEquip()
        if i:
            runeText = "<font color = \'#BF7FFF\'>"
            if i.id in RD.data and 'pskillList' in RD.data[i.id] and RD.data[i.id]['pskillList']:
                for skillId, skillLv in RD.data[i.id]['pskillList']:
                    runeText += gameglobal.rds.ui.runeView.generateDesc(skillId, PSkillInfo(skillId, skillLv, {}), skillLv) + '\n'

            runeText += "</font><font color = \'#FFFFE5\'>"
            rData = RD.data.get(i.id)
            if uiConst.RUNE_FORGING_LOW_LV in rData.get('qiFuLvList', []):
                runeText += gameStrings.TEXT_RUNEFORGINGPROXY_203
                if uiConst.RUNE_FORGING_LOW_LV in i.runeQiFuData:
                    runeText += '\n'
                    if isPreview and self.qiFuLv == uiConst.RUNE_FORGING_LOW_LV:
                        runeText += gameStrings.TEXT_RUNEREFORGINGPROXY_207
                    else:
                        for skillId in i.runeQiFuData[uiConst.RUNE_FORGING_LOW_LV][1]:
                            skillLv = i.runeQiFuData[uiConst.RUNE_FORGING_LOW_LV][1][skillId]
                            runeText += gameglobal.rds.ui.runeView.generateDesc(skillId, PSkillInfo(skillId, skillLv, {}), skillLv) + '\n'

                        qiFuId = i.runeQiFuData[uiConst.RUNE_FORGING_LOW_LV][0]
                        effects = RQED.data.get(qiFuId, {}).get('effects', [])
                        for effect in effects:
                            if effect[0] == gametypes.RUNE_QIFU_EFFECT_TYPE_SHENLI:
                                runeText += const.RUNE_POWER_DESC[effect[1]] + '*' + str(effect[2]) + '\n'

                else:
                    runeText += gameStrings.TEXT_RUNEFORGINGPROXY_218
            if uiConst.RUNE_FORGING_LHIGH_LV in rData.get('qiFuLvList', []):
                runeText += gameStrings.TEXT_RUNEFORGINGPROXY_221
                if uiConst.RUNE_FORGING_LHIGH_LV in i.runeQiFuData:
                    runeText += '\n'
                    if isPreview and self.qiFuLv == uiConst.RUNE_FORGING_LHIGH_LV:
                        runeText += gameStrings.TEXT_RUNEREFORGINGPROXY_207
                    else:
                        for skillId in i.runeQiFuData[uiConst.RUNE_FORGING_LHIGH_LV][1]:
                            skillLv = i.runeQiFuData[uiConst.RUNE_FORGING_LHIGH_LV][1][skillId]
                            runeText += gameglobal.rds.ui.runeView.generateDesc(skillId, PSkillInfo(skillId, skillLv, {}), skillLv) + '\n'

                        qiFuId = i.runeQiFuData[uiConst.RUNE_FORGING_LHIGH_LV][0]
                        effects = RQED.data.get(qiFuId, {}).get('effects', [])
                        for effect in effects:
                            if effect[0] == gametypes.RUNE_QIFU_EFFECT_TYPE_SHENLI:
                                runeText += const.RUNE_POWER_DESC[effect[1]] + '*' + str(effect[2]) + '\n'

                else:
                    runeText += gameStrings.TEXT_RUNEFORGINGPROXY_218
            runeText += '</font>'
        return runeText

    def refreshRuneEquip(self):
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
        gameglobal.rds.ui.roleInfo.updateRuneSlotState()
        self.refreshConfirmBtn()
        effectText = self.getEffectText()
        i = self.getRuneEquip()
        desc = ''
        if i:
            desc = RQD.data.get((uiConst.RUNE_FORGING_LOW_LV, gametypes.RUNE_QIFU_OP_TYPE_REFORGING), {}).get('desc', '')
        self.mediator.Invoke('refreshRuneEquip', (GfxValue(gbk2unicode(effectText)), GfxValue(gbk2unicode(desc))))

    def refreshConfirmBtn(self):
        if self.mediator:
            i = self.getRuneEquip()
            if i:
                canRuneReforgingLvList = i.getCanRuneReforgingLv()
                if i.isRune() and canRuneReforgingLvList:
                    if uiConst.RUNE_FORGING_LOW_LV in canRuneReforgingLvList and self.checkQiFuLv(uiConst.RUNE_FORGING_LOW_LV):
                        self.setQiFuLv(uiConst.RUNE_FORGING_LOW_LV)
                        return
                    if uiConst.RUNE_FORGING_LHIGH_LV in canRuneReforgingLvList and self.checkQiFuLv(uiConst.RUNE_FORGING_LHIGH_LV):
                        self.setQiFuLv(uiConst.RUNE_FORGING_LHIGH_LV)
                        return
            self.mediator.Invoke('refreshConfirmBtn', GfxValue(False))
            self.removeItem(uiConst.RUNE_REFORGING_EQUIP, 1)
            self.refreshPreview('')

    def checkQiFuLv(self, qiFuLv):
        p = BigWorld.player()
        qiFuData = RQD.data.get((qiFuLv, gametypes.RUNE_QIFU_OP_TYPE_REFORGING), {}).get('qiFuData', [])
        if qiFuData:
            for itemNeed in qiFuData:
                isCanReforging = True
                idSet = set(self.itemMap.values())
                if len(itemNeed) == len(idSet):
                    tDict = dict(itemNeed)
                    for id in idSet:
                        if id not in tDict or tDict[id] > p.inv.countItemInPages(id):
                            isCanReforging = False
                            break

                    if isCanReforging:
                        return True

        return False

    def setQiFuLv(self, qiFuLv):
        self.qiFuLv = qiFuLv
        self.mediator.Invoke('refreshConfirmBtn', GfxValue(True))
        i = self.getRuneEquip()
        self.addItem(i, uiConst.RUNE_FORGING_EQUIP, 1)
        self.refreshPreview(self.getEffectText(True))

    def refreshPreview(self, previewText):
        if self.mediator:
            self.mediator.Invoke('refreshPreview', GfxValue(gbk2unicode(previewText)))

    def getRuneEquip(self):
        i = None
        p = BigWorld.player()
        if self.source == uiConst.RUNE_SOURCE_INV and self.invPage != const.CONT_NO_PAGE:
            i = p.inv.getQuickVal(self.invPage, self.invPos)
        elif self.source == uiConst.RUNE_SOURCE_ROLE and self.runePage != const.CONT_NO_PAGE:
            for runeDataVal in p.runeBoard.runeEquip.runeData:
                if runeDataVal.runeSlotsType == self.runePage and runeDataVal.part == self.runePart:
                    i = runeDataVal.item
                    break

        return i

    def isItemDisabled(self, kind, page, pos, item):
        if kind == const.RES_KIND_INV:
            return self.mediator and page == self.invPage and pos == self.invPos

    @ui.uiEvent(uiConst.WIDGET_RUNE_REFORGING, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onInventoryRightClick(self, event):
        event.stop()
        i = event.data['item']
        nPage = event.data['page']
        nItem = event.data['pos']
        if i == None:
            return
        else:
            self.setInventoryItem(nPage, nItem, uiConst.RUNE_REFORGING_EQUIP, 0)
            return

    def setInventoryItem(self, nPageSrc, nItemSrc, nPageDes, nItemDes):
        p = BigWorld.player()
        srcItem = p.inv.getQuickVal(nPageSrc, nItemSrc)
        if not srcItem:
            return
        if srcItem.isRunReforging() and nPageDes == uiConst.RUNE_FORGING_ITEM:
            self.addItem(srcItem, nPageDes, nItemDes)
        elif srcItem.isRune() and nPageDes == uiConst.RUNE_REFORGING_EQUIP and srcItem.canRuneReforging() and not nItemDes:
            self.invPage = nPageSrc
            self.invPos = nItemSrc
            self.source = uiConst.RUNE_SOURCE_INV
            self.runePage = const.CONT_NO_PAGE
            self.runePart = const.CONT_NO_POS
            self.addItem(srcItem, nPageDes, nItemDes)
