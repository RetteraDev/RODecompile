#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildBusinessBagProxy.o
import BigWorld
import gameglobal
import uiUtils
import uiConst
import const
import commQuest
from uiProxy import UIProxy
from data import business_config_data as BCD
from data import quest_data as QD
from cdata import business_lv_config_data as BLCD

class GuildBusinessBagProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildBusinessBagProxy, self).__init__(uiAdapter)
        self.modelMap = {}
        self.mediator = None
        self.bagSlotCount = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_BUSINESS_BAG, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_BUSINESS_BAG:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_BUSINESS_BAG)

    def show(self):
        if self.mediator:
            self.mediator.Invoke('swapPanelToFront')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_BUSINESS_BAG)

    def setBagSlotCount(self, bagSlotCount):
        self.bagSlotCount = bagSlotCount

    def refreshInfo(self):
        if self.mediator:
            p = BigWorld.player()
            info = {}
            info['maxNum'] = self.bagSlotCount
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))
            for pos in xrange(self.bagSlotCount):
                item = p.zaijuBag.getQuickVal(0, pos)
                self.updateItem(item, 0, pos)

            self.updateOtherInfo()

    def updateItem(self, item, page, pos):
        if self.mediator:
            info = {}
            info['itemInfo'] = uiUtils.getGfxItem(item, location=const.ITEM_IN_BUSINESS_BAG) if item else None
            info['isBlack'] = item != None and hasattr(item, 'ownerGbId') and item.ownerGbId != BigWorld.player().gbId
            info['pos'] = pos
            self.mediator.Invoke('updateItem', uiUtils.dict2GfxDict(info, True))
        gameglobal.rds.ui.guildBusinessShop.refreshPackageInfo()

    def updateOtherInfo(self):
        if self.mediator:
            p = BigWorld.player()
            info = {}
            businessLv = 0
            for questId in p.quests:
                qd = QD.data[questId]
                if commQuest.isQuestDisable(questId):
                    continue
                if qd.has_key('businessLv'):
                    businessLv = qd['businessLv']
                    break

            info['condition'] = format(BLCD.data.get(businessLv, {}).get('maxFame', 0), ',')
            info['own'] = format(p.getFame(BCD.data.get('businessFameId', 0)), ',')
            info['bagSpace'] = '%d/%d' % (p.zaijuBag.countZaijuBagNum(), self.bagSlotCount)
            self.mediator.Invoke('updateOtherInfo', uiUtils.dict2GfxDict(info, True))

    def canPickUp(self, itemLen):
        return itemLen + BigWorld.player().zaijuBag.countZaijuBagNum() <= self.bagSlotCount
