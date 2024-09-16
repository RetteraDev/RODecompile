#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/runeFeedProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
from guis import uiConst
from guis import uiUtils
from ui import gbk2unicode
from gameclass import PSkillInfo
from uiProxy import SlotDataProxy
from item import Item
from data import item_data as ID
from data import rune_equip_data as REQD
from cdata import game_msg_def_data as GMDD
from cdata import rune_equip_exp_data as REED
from cdata import font_config_data as FCD

class RuneFeedProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(RuneFeedProxy, self).__init__(uiAdapter)
        self.modelMap = {'closePanel': self.onClosePanel,
         'feedRune': self.onFeedRune,
         'removeItem': self.onRemoveItem,
         'getData': self.onGetData}
        self.type = 'runeFeed'
        self.bindType = 'runeFeed'
        self.mediator = None
        self.feedId = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_RUNE_FEED, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_RUNE_FEED:
            self.mediator = mediator

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_RUNE_FEED)

    def reset(self):
        super(self.__class__, self).reset()
        self.feedId = None

    def show(self):
        if not self.mediator and BigWorld.player().runeBoard.runeEquip:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_RUNE_FEED)

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[8:]), int(idItem[4:]))

    def _getKey(self, bar, slot):
        return 'runeFeed%d.slot%d' % (bar, slot)

    def addItem(self, item, page, pos):
        if item is not None:
            if pos == uiConst.RUNE_FEED_ITEM:
                if self.feedId != item.id:
                    self.updateFeedItem(True)
                self.feedId = item.id
            elif pos == uiConst.RUNE_FEED_EQUIP:
                self.updateEquip()
            key = self._getKey(page, pos)
            if self.binding.get(key, None) is not None:
                data = self.uiAdapter.movie.CreateObject()
                icon = uiUtils.getItemIconFile40(item.id)
                idNum = GfxValue(item.id)
                name = GfxValue('item')
                iconPath = GfxValue(icon)
                if pos == uiConst.RUNE_FEED_ITEM:
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
        if pos == uiConst.RUNE_FEED_ITEM:
            self.updateFeedItem(False)
            self.feedId = None
        if self.binding.get(key, None) is not None:
            data = GfxValue(1)
            data.SetNull()
            self.binding[key][0].Invoke('setSlotColor', GfxValue('nothing'))
            self.binding[key][1].InvokeSelf(data)

    def onGetToolTip(self, *arg):
        p = BigWorld.player()
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        if slot == uiConst.RUNE_FEED_ITEM:
            if self.feedId:
                return gameglobal.rds.ui.inventory.GfxToolTip(Item(self.feedId))
            else:
                return GfxValue('')
        elif slot == uiConst.RUNE_FEED_EQUIP:
            if p.runeBoard.runeEquip:
                return gameglobal.rds.ui.inventory.GfxToolTip(p.runeBoard.runeEquip)
            else:
                return GfxValue('')

    def onGetData(self, *arg):
        p = BigWorld.player()
        if not p.runeBoard.runeEquip:
            self.hide()
            return
        self.addItem(p.runeBoard.runeEquip, 0, uiConst.RUNE_FEED_EQUIP)

    def updateFeedItem(self, isBtnEnable):
        if self.mediator:
            self.mediator.Invoke('updateFeedItem', GfxValue(isBtnEnable))

    def refreshRuneEquip(self):
        p = BigWorld.player()
        if p.runeBoard.runeEquip and self.mediator:
            i = p.runeBoard.runeEquip
            runeEquipText = '资质：%d\n' % i.runeEquipAptitude
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

    def updateEquip(self):
        if self.mediator:
            p = BigWorld.player()
            feedArray = self.movie.CreateArray()
            feedArray.SetElement(0, GfxValue(gbk2unicode(p.runeBoard.runeEquip.name)))
            feedArray.SetElement(1, GfxValue(p.runeBoard.runeEquip.runeEquipOrder))
            feedArray.SetElement(2, GfxValue(p.runeBoard.runeEquip.runeEquipLv))
            if const.RUNE_EQUIP_MAX_LV <= p.runeBoard.runeEquip.runeEquipLv:
                eData = REED.data.get((const.RUNE_EQUIP_MAX_LV - 1, p.runeBoard.runeEquip.runeEquipOrder))
                feedArray.SetElement(3, GfxValue(eData['upExp']))
                feedArray.SetElement(4, GfxValue(eData['upExp']))
            else:
                feedArray.SetElement(3, GfxValue(p.runeBoard.runeEquip.runeEquipExp))
                eData = REED.data.get((p.runeBoard.runeEquip.runeEquipLv, p.runeBoard.runeEquip.runeEquipOrder))
                feedArray.SetElement(4, GfxValue(eData['upExp']))
            self.mediator.Invoke('updateEquip', feedArray)
            self.refreshRuneEquip()

    def onClosePanel(self, *arg):
        self.hide()

    def onFeedRune(self, *arg):
        key = arg[3][0].GetString()
        p = BigWorld.player()
        if const.RUNE_EQUIP_MAX_LV <= p.runeBoard.runeEquip.runeEquipLv:
            p.showGameMsg(GMDD.data.RUNE_FEED_LV_ENOUGH, ())
            return
        if self.feedId:
            if not key:
                p.showGameMsg(GMDD.data.RUNE_FEED_NONE, ())
                return
            amount = int(key)
            count = BigWorld.player().inv.countItemInPages(self.feedId)
            if amount > 0 and amount <= count:
                p.cell.addRuneEquipExp(self.feedId, amount)
            else:
                p.showGameMsg(GMDD.data.RUNE_FEED_LESS, ())

    def onRemoveItem(self, *arg):
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        if slot == uiConst.RUNE_FEED_ITEM:
            self.removeItem(bar, slot)
