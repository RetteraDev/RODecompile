#Embedded file name: /WORKSPACE/data/entities/client/guis/runeorderupproxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
from guis import uiConst
from guis import uiUtils
from ui import gbk2unicode
from uiProxy import SlotDataProxy
from item import Item
from gameclass import PSkillInfo
from data import item_data as ID
from cdata import font_config_data as FCD
from data import rune_equip_data as REQD
from cdata import rune_equip_order_up_data as REOUD

class RuneOrderUpProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(RuneOrderUpProxy, self).__init__(uiAdapter)
        self.modelMap = {'closePanel': self.onClosePanel,
         'confirm': self.onConfirm,
         'openInventory': self.onOpenInventory,
         'removeItem': self.onRemoveItem,
         'getData': self.onGetData}
        self.mediator = None
        self.type = 'runeOrder'
        self.bindType = 'runeOrder'
        self.itemMap = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_RUNE_ORDERUP, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_RUNE_ORDERUP:
            self.mediator = mediator

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_RUNE_ORDERUP)

    def reset(self):
        super(self.__class__, self).reset()
        self.itemMap = {}

    def show(self):
        if not self.mediator and BigWorld.player().runeBoard.runeEquip:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_RUNE_ORDERUP)

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[9:]), int(idItem[4:]))

    def _getKey(self, bar, slot):
        return 'runeOrder%d.slot%d' % (bar, slot)

    def onGetData(self, *arg):
        p = BigWorld.player()
        if not p.runeBoard.runeEquip:
            self.hide()
            return
        self.addItem(p.runeBoard.runeEquip, uiConst.RUNE_ORDERUP_EQUIP, 0)

    def onClosePanel(self, *arg):
        self.hide()

    def onConfirm(self, *arg):
        p = BigWorld.player()
        idList = set(self.itemMap.values())
        posList = []
        for id in idList:
            pg, pos = p.inv.findItemByAttr({'id': id})
            if pg != const.CONT_NO_PAGE:
                posList.append((pg, pos))

        if posList:
            p.cell.runeEquipOrderUp(posList)

    def onOpenInventory(self, *arg):
        if not gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.show()

    def onRemoveItem(self, *arg):
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        self.removeItem(bar, slot)

    def addOrderUpItem(self, item):
        if item.id in self.itemMap.values():
            return
        for i in range(5):
            if i not in self.itemMap:
                self.addItem(item, uiConst.RUNE_ORDERUP_ITEM, i)
                return

    def updateItemNum(self, item):
        gameglobal.rds.ui.runeForging.updateItemNum(item)
        gameglobal.rds.ui.runeReforging.updateItemNum(item)
        gameglobal.rds.ui.runeChongXi.updateItemNum(item)
        if self.mediator and item.id in self.itemMap.values():
            for id in self.itemMap:
                if item.id == self.itemMap[id]:
                    self.addItem(item, uiConst.RUNE_ORDERUP_ITEM, id)

    def addItem(self, item, page, pos):
        if item is not None:
            if page == uiConst.RUNE_ORDERUP_ITEM:
                self.itemMap[pos] = item.id
            if page == uiConst.RUNE_ORDERUP_EQUIP and not pos:
                self.refreshRuneEquip()
            if not (page == uiConst.RUNE_ORDERUP_EQUIP and pos):
                self.refreshConfirmBtn()
            key = self._getKey(page, pos)
            if self.binding.get(key, None) is not None:
                data = self.uiAdapter.movie.CreateObject()
                icon = uiUtils.getItemIconFile40(item.id)
                idNum = GfxValue(item.id)
                name = GfxValue('item')
                iconPath = GfxValue(icon)
                if page == uiConst.RUNE_ORDERUP_ITEM:
                    count = GfxValue(BigWorld.player().inv.countItemInPages(item.id))
                else:
                    count = GfxValue(item.cwrap)
                data.SetMember('id', idNum)
                data.SetMember('name', name)
                data.SetMember('iconPath', iconPath)
                data.SetMember('count', count)
                if hasattr(item, 'quality'):
                    quality = item.quality
                else:
                    quality = ID.data.get(item.id, {}).get('quality', 1)
                color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                self.binding[key][0].Invoke('setSlotColor', GfxValue(color))
                self.binding[key][1].InvokeSelf(data)

    def removeItem(self, page, pos):
        key = self._getKey(page, pos)
        if page == uiConst.RUNE_ORDERUP_ITEM and pos in self.itemMap:
            del self.itemMap[pos]
            self.refreshConfirmBtn()
        if self.binding.get(key, None) is not None:
            data = GfxValue(1)
            data.SetNull()
            self.binding[key][0].Invoke('setSlotColor', GfxValue('nothing'))
            self.binding[key][1].InvokeSelf(data)

    def onGetToolTip(self, *arg):
        p = BigWorld.player()
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        if bar == uiConst.RUNE_ORDERUP_ITEM:
            return GfxValue('')
            if slot in self.itemMap:
                return gameglobal.rds.ui.inventory.GfxToolTip(Item(self.itemMap[slot]))
        elif slot:
            if p.runeBoard.runeEquip and REOUD.data.get(p.runeBoard.runeEquip.id, {}).get('runeEquipId', 0):
                return gameglobal.rds.ui.inventory.GfxToolTip(Item(REOUD.data.get(p.runeBoard.runeEquip.id, {}).get('runeEquipId', 0)))
        elif p.runeBoard.runeEquip:
            return gameglobal.rds.ui.inventory.GfxToolTip(p.runeBoard.runeEquip)
        return GfxValue('')

    def refreshRuneEquip(self):
        p = BigWorld.player()
        if p.runeBoard.runeEquip and self.mediator:
            i = p.runeBoard.runeEquip
            runeEquipText = '资质：%d\n' % i.runeEquipAptitude
            runeEquipText += '等级：%d\n' % i.runeEquipLv
            runeEquipText += '品阶：%d\n' % i.runeEquipOrder
            runeEquipText += '天轮觉醒：\n'
            tianLunAwakeNeed = REQD.data[i.id]['tianLunAwakeNeed']
            for tianLunEffect in range(len(tianLunAwakeNeed)):
                if tianLunAwakeNeed[tianLunEffect]:
                    runeEquipText += const.RUNE_POWER_DESC[tianLunEffect] + '*%d  ' % tianLunAwakeNeed[tianLunEffect]

            runeEquipText += '\n'
            tianLunPSkillList = REQD.data.get(i.id, {}).get('tianLunPSkillList', ())
            if tianLunPSkillList:
                pskId = tianLunPSkillList[0]
                runeEquipText += gameglobal.rds.ui.runeView.generateDesc(pskId, PSkillInfo(pskId, i.runeEquipLv, {}), i.runeEquipLv) + '\n'
            runeEquipText += '地轮觉醒：\n'
            diLunAwakeNeed = REQD.data[i.id]['diLunAwakeNeed']
            for diLunEffect in range(len(diLunAwakeNeed)):
                if diLunAwakeNeed[diLunEffect]:
                    runeEquipText += const.RUNE_POWER_DESC[diLunEffect] + '*%d  ' % diLunAwakeNeed[diLunEffect]

            runeEquipText += '\n'
            diLunPSkillList = REQD.data.get(i.id, {}).get('diLunPSkillList', ())
            if diLunPSkillList:
                pskId = diLunPSkillList[0]
                runeEquipText += gameglobal.rds.ui.runeView.generateDesc(pskId, PSkillInfo(pskId, i.runeEquipLv, {}), i.runeEquipLv) + '\n'
            self.mediator.Invoke('refreshRuneEquip', GfxValue(gbk2unicode(runeEquipText)))

    def updatePreviewText(self, id):
        if self.mediator:
            previewText = ''
            if id in REQD.data:
                previewText = '资质：随机\n'
                previewText += '等级：1\n'
                previewText += '品阶：%d\n' % REQD.data[id]['order']
                previewText += '天轮觉醒：\n'
                tianLunAwakeNeed = REQD.data[id]['tianLunAwakeNeed']
                for tianLunEffect in range(len(tianLunAwakeNeed)):
                    if tianLunAwakeNeed[tianLunEffect]:
                        previewText += const.RUNE_POWER_DESC[tianLunEffect] + '*%d  ' % tianLunAwakeNeed[tianLunEffect]

                previewText += '\n'
                tianLunPSkillList = REQD.data.get(id, {}).get('tianLunPSkillList', ())
                if tianLunPSkillList:
                    pskId = tianLunPSkillList[0]
                    previewText += gameglobal.rds.ui.runeView.generateDesc(pskId, PSkillInfo(pskId, 1, {}), 1) + '\n'
                previewText += '地轮觉醒：\n'
                diLunAwakeNeed = REQD.data[id]['diLunAwakeNeed']
                for diLunEffect in range(len(diLunAwakeNeed)):
                    if diLunAwakeNeed[diLunEffect]:
                        previewText += const.RUNE_POWER_DESC[diLunEffect] + '*%d  ' % diLunAwakeNeed[diLunEffect]

                previewText += '\n'
                diLunPSkillList = REQD.data.get(id, {}).get('diLunPSkillList', ())
                if diLunPSkillList:
                    pskId = diLunPSkillList[0]
                    previewText += gameglobal.rds.ui.runeView.generateDesc(pskId, PSkillInfo(pskId, 1, {}), 1) + '\n'
            self.mediator.Invoke('updatePreviewText', GfxValue(gbk2unicode(previewText)))

    def refreshConfirmBtn(self):
        if self.mediator:
            p = BigWorld.player()
            oData = REOUD.data.get(p.runeBoard.runeEquip.id, {})
            noticeText = '不能再升阶'
            if oData:
                noticeText = '请放入' + p.runeBoard.runeEquip.name + '进行升阶'
                itemGroups = oData.get('orderUpData', [])
                idList = tuple(self.itemMap.values())
                newItemId = oData.get('runeEquipId', 0)
                for val in itemGroups:
                    itemNeed, _, _ = val
                    if len(idList) != len(itemNeed):
                        continue
                    tDict = dict(itemNeed)
                    flag = True
                    for itemId, itemNum in tDict.items():
                        if itemId not in idList or p.inv.countItemInPages(itemId) < itemNum:
                            flag = False
                            break

                    if flag:
                        self.mediator.Invoke('refreshConfirmBtn', (GfxValue(True), GfxValue(gbk2unicode(noticeText))))
                        self.updatePreviewText(newItemId)
                        self.addItem(Item(newItemId), uiConst.RUNE_ORDERUP_EQUIP, 1)
                        return

            self.mediator.Invoke('refreshConfirmBtn', (GfxValue(False), GfxValue(gbk2unicode(noticeText))))
            self.mediator.Invoke('updatePreviewText', GfxValue(''))
            self.removeItem(uiConst.RUNE_ORDERUP_EQUIP, 1)
