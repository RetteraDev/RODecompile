#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/runeChongXiProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gametypes
import const
from guis import uiConst
from guis import uiUtils
from ui import gbk2unicode
from uiProxy import SlotDataProxy
from item import Item
from gameclass import PSkillInfo
from data import item_data as ID
from cdata import font_config_data as FCD
from data import rune_equip_xilian_effect_data as REXED
from cdata import rune_equip_chongxi_data as RECD

class RuneChongXiProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(RuneChongXiProxy, self).__init__(uiAdapter)
        self.modelMap = {'closePanel': self.onClosePanel,
         'confirm': self.onConfirm,
         'openInventory': self.onOpenInventory,
         'removeItem': self.onRemoveItem,
         'getData': self.onGetData}
        self.mediator = None
        self.type = 'runeChongXi'
        self.bindType = 'runeChongXi'
        self.itemMap = {}
        self.runeSlotsType = None
        self.part = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_RUNE_CHONGXI, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_RUNE_CHONGXI:
            self.mediator = mediator

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_RUNE_CHONGXI)

    def reset(self):
        super(self.__class__, self).reset()
        self.itemMap = {}
        self.runeSlotsType = None
        self.part = None

    def show(self, runeSlotsType, part):
        if not self.mediator and BigWorld.player().runeBoard.runeEquip:
            self.runeSlotsType = runeSlotsType
            self.part = part
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_RUNE_CHONGXI)

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[11:]), int(idItem[4:]))

    def _getKey(self, bar, slot):
        return 'runeChongXi%d.slot%d' % (bar, slot)

    def onGetData(self, *arg):
        p = BigWorld.player()
        if not p.runeBoard.runeEquip:
            self.hide()
            return
        self.addXiLianSlot()

    def onClosePanel(self, *arg):
        self.hide()

    def onConfirm(self, *arg):
        p = BigWorld.player()
        idList = set(self.itemMap.values())
        posList = []
        for item in idList:
            pg, pos = p.inv.findItemByAttr({'id': item[0]})
            if pg != const.CONT_NO_PAGE:
                posList.append((pg, pos))

        if posList and self.runeSlotsType != None:
            p.cell.runeEquipChongXi(self.runeSlotsType, self.part, posList)

    def onOpenInventory(self, *arg):
        if not gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.show()

    def onRemoveItem(self, *arg):
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        self.removeItem(bar, slot)

    def updateItemNum(self, item):
        self.refreshConfirmBtn()
        for i in self.itemMap:
            if self.itemMap[i][0] == item.id:
                self.addItem(self.itemMap[i][0], uiConst.RUNE_CHONGXI_ITEM, i)

    def addXiLianSlot(self):
        if self.runeSlotsType == None:
            self.hide()
            return
        else:
            self.refreshRuneEquip()
            key = self._getKey(uiConst.RUNE_CHONGXI_EQUIP, 0)
            runeEquip = BigWorld.player().runeBoard.runeEquip
            if runeEquip.runeEquipXiLianData.has_key((self.runeSlotsType, self.part)):
                xiLianId = runeEquip.runeEquipXiLianData[self.runeSlotsType, self.part][0]
            else:
                xiLianId = 0
            if self.binding.get(key, None) is not None:
                data = self.uiAdapter.movie.CreateObject()
                iconPath = uiConst.ITEM_ICON_IMAGE_RES_40 + str(REXED.data[xiLianId].get('tipsIcon', 'notFound')) + '.dds'
                data.SetMember('iconPath', GfxValue(iconPath))
                self.binding[key][1].InvokeSelf(data)
            p = BigWorld.player()
            chongXiData = RECD.data.get(p.runeBoard.runeEquip.runeEquipOrder, {}).get('chongXiData')
            self.setSlotNum(len(chongXiData[0]))
            self.refreshPreview(gameStrings.TEXT_RUNECHONGXIPROXY_128)
            for i, value in enumerate(chongXiData[0]):
                self.itemMap[i] = value
                self.addItem(value[0], uiConst.RUNE_CHONGXI_ITEM, i)

            self.refreshConfirmBtn()
            return

    def addItem(self, id, page, pos):
        key = self._getKey(page, pos)
        if self.binding.get(key, None) is not None:
            data = self.uiAdapter.movie.CreateObject()
            icon = uiUtils.getItemIconFile40(id)
            idNum = GfxValue(id)
            name = GfxValue('item')
            iconPath = GfxValue(icon)
            count = GfxValue(str(BigWorld.player().inv.countItemInPages(id)) + '/' + str(self.itemMap[pos][1]))
            data.SetMember('id', idNum)
            data.SetMember('name', name)
            data.SetMember('iconPath', iconPath)
            data.SetMember('count', count)
            quality = ID.data.get(id, {}).get('quality', 1)
            color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
            self.binding[key][0].Invoke('setSlotColor', GfxValue(color))
            self.binding[key][1].InvokeSelf(data)

    def removeItem(self, page, pos):
        key = self._getKey(page, pos)
        if self.binding.get(key, None) is not None:
            data = GfxValue(1)
            data.SetNull()
            self.binding[key][0].Invoke('setSlotColor', GfxValue('nothing'))
            self.binding[key][1].InvokeSelf(data)

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        if bar == uiConst.RUNE_CHONGXI_ITEM:
            if slot in self.itemMap:
                return gameglobal.rds.ui.inventory.GfxToolTip(Item(self.itemMap[slot][0]))
        elif not slot:
            return gameglobal.rds.ui.roleInfo.formatRuneChongXiTooltip(self.runeSlotsType, self.part)
        return GfxValue('')

    def refreshRuneEquip(self):
        p = BigWorld.player()
        if p.runeBoard.runeEquip and self.mediator:
            runeEquipText = "<font color = \'#FFB91C\'>"
            for key, value in p.runeBoard.runeEquip.runeEquipXiLianData.iteritems():
                runeSlotsType, part = key
                xiLianId, pskData = value
                if self.runeSlotsType == runeSlotsType and self.part == part:
                    runeEquipText += gameStrings.TEXT_ROLEINFOPROXY_1669
                    for rTypeNeed, rLvNeed in REXED.data[xiLianId].get('activateCondition', []):
                        runeEquipText += gameStrings.TEXT_ROLEINFOPROXY_1671 + str(rLvNeed) + gameStrings.TEXT_ROLEINFOPROXY_1671_1 + const.RUNE_POWER_DESC[rTypeNeed] + '\n'

                    runeEquipText += gameStrings.TEXT_ROLEINFOPROXY_1672
                    for skillId in pskData:
                        skillLv = pskData[skillId]
                        runeEquipText += gameglobal.rds.ui.runeView.generateDesc(skillId, PSkillInfo(skillId, skillLv, {}), skillLv) + '\n'

                    for effect in REXED.data[xiLianId].get('effects', []):
                        if effect[0] == gametypes.RUNE_EQUIP_XILIAN_EFFECT_TYPE_SHENLI:
                            runeEquipText += const.RUNE_POWER_DESC[effect[1]] + '*' + str(effect[2]) + '\n'

            runeEquipText += '</font>'
            self.mediator.Invoke('refreshRuneEquip', GfxValue(gbk2unicode(runeEquipText)))

    def refreshConfirmBtn(self):
        if self.mediator:
            isCanChongXi = self.checkChongXi()
            self.mediator.Invoke('refreshConfirmBtn', GfxValue(isCanChongXi))

    def checkChongXi(self):
        for pos in self.itemMap:
            if self.itemMap[pos][1] > BigWorld.player().inv.countItemInPages(self.itemMap[pos][0]):
                return False

        return True

    def refreshPreview(self, previewText):
        if self.mediator:
            self.mediator.Invoke('refreshPreview', GfxValue(gbk2unicode(previewText)))

    def setSlotNum(self, num):
        if self.mediator:
            self.mediator.Invoke('setSlotNum', GfxValue(num))
