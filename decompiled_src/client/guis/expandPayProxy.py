#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/expandPayProxy.o
import BigWorld
from uiProxy import UIProxy
import gameglobal
import const
import gamelog
from guis import uiConst
from guis import uiUtils
from callbackHelper import Functor
from gameStrings import gameStrings
from item import Item
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
from cdata import item_fame_score_cost_data as IFSCD
from cdata import item_parentId_data as IPD
from cdata import item_coin_dikou_cost_data as ICDCD

class ExpandPayProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ExpandPayProxy, self).__init__(uiAdapter)
        self.modelMap = {'getViewInfo': self.onGetViewInfo,
         'enlargeBag': self.onEnlargeBag}
        self.expandType = -1
        self.slotIdx = -1
        self.npcId = 0
        self.bindCash = 0
        self.costItemId = 0
        self.mediator = None
        self.data = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_EXPAND_PAY, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_EXPAND_PAY:
            self.mediator = mediator

    def show(self, expandType, slotIdx, data = {}):
        self.expandType = int(expandType)
        self.slotIdx = int(slotIdx)
        self.data = data
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EXPAND_PAY)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.expandType = -1
        self.slotIdx = -1
        self.npcId = 0
        self.bindCash = 0
        self.costItemId = 0
        self.mediator = None
        self.data = {}
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EXPAND_PAY)

    def onGetViewInfo(self, *arg):
        ret = {}
        config = []
        helpKey = 30
        if self.expandType == uiConst.EXPAND_INVENTORY_EXPAND:
            config = SCD.data.get('invEnlargeCost', [])
        elif self.expandType == uiConst.EXPAND_STORAGE_EXPAND:
            config = SCD.data.get('storageEnlargeCost', [])
        elif self.expandType == uiConst.EXPAND_MATERIAL_BAG_ACTIVE:
            config = SCD.data.get('materialActiveCost', [])
            helpKey = 44
        elif self.expandType == uiConst.EXPAND_RIDE_WING_BAG_EXPAND:
            config = SCD.data.get('rideWingBagEnlargeCost', [])
        elif self.expandType == uiConst.EXPAND_MATERIAL_BAG_EXPAND:
            config = SCD.data.get('materialBagEnlargeCost', [])
            helpKey = 44
        elif self.expandType == uiConst.EXPAND_SPRITE_MATERIAL_BAG_EXPAND:
            config = SCD.data.get('spriteMaterialBagEnlargeCost', [])
        elif self.expandType == uiConst.EXPAND_WARDROBE_DYE_EXPAND:
            config = SCD.data.get('wardrobeDyeListEnlargeCost', ((0, (310009, 5)),))
        elif self.expandType == uiConst.EXPAND_RUNE_INV_EXPAND:
            config = SCD.data.get('hierogramBagEnlargeCost')
        if len(config) > self.slotIdx and self.slotIdx != -1:
            data = config[self.slotIdx]
            if data != None and data[1] != 0:
                p = BigWorld.player()
                self.bindCash = data[0]
                ret['money'] = self.bindCash
                ret['playerCash'] = p.bindCash
                ret['moneyType'] = 'bindCash'
                ret['requireText'] = ''
                ret['currentCount'] = p.inv.countItemInPages(int(data[1][0]), enableParentCheck=True)
                ret['itemCount'] = data[1][1]
                count = uiUtils.convertNumStr(ret['currentCount'], data[1][1])
                self.costItemId = data[1][0]
                ret['item'] = uiUtils.getGfxItemById(data[1][0], count)
                deltaCount = ret['itemCount'] - ret['currentCount']
                ret['itemFameTxt'] = {}
                if deltaCount > 0 and self.expandType == uiConst.EXPAND_WARDROBE_DYE_EXPAND:
                    itemCost = SCD.data.get('wardrobeDyeListExpandItemCost', 0)
                    totalCost = deltaCount * itemCost
                    ret['moneyType'] = 'tianbi'
                    ret['requireText'] = gameStrings.EXPAND_PAY_REQIRE_TEXT % Item(self.costItemId).name
                    ret['itemFameTxt']['line1'] = gameStrings.ITEM_FAME_INSTANTLY_PURCHASE_1
                    ret['itemFameTxt']['line2'] = gameStrings.ITEM_YUNBI_INSTANTLY_PURCHASE_3 % totalCost
                elif deltaCount > 0 and gameglobal.rds.configData.get('enableYunChuiScoreDikou', False) and self.expandType != uiConst.EXPAND_MATERIAL_BAG_ACTIVE:
                    itemIds = IPD.data.get(self.costItemId, [])
                    itemCost = 0
                    for id in itemIds:
                        if IFSCD.data.has_key(id):
                            itemFameData = IFSCD.data.get(id, {})
                            itemCost = itemFameData.get(const.YUN_CHUI_JI_FEN_FAME_ID, 0)

                    totalCost = deltaCount * itemCost
                    ret['itemFameTxt']['line1'] = gameStrings.ITEM_FAME_INSTANTLY_PURCHASE_1
                    ret['itemFameTxt']['line2'] = gameStrings.ITEM_FAME_INSTANTLY_PURCHASE_2 % totalCost
                else:
                    ret['itemFameTxt'] = None
        ret['helpKey'] = helpKey
        return uiUtils.dict2GfxDict(ret, True)

    def onEnlargeBag(self, *arg):
        p = BigWorld.player()
        if uiUtils.checkBindCashEnough(self.bindCash, p.bindCash, p.cash, Functor(self.confirmEnlarge)):
            self.confirmEnlarge()

    def confirmEnlarge(self):
        p = BigWorld.player()
        if self.expandType == uiConst.EXPAND_INVENTORY_EXPAND:
            p.cell.toEnlargeInvPackSlot()
        elif self.expandType == uiConst.EXPAND_STORAGE_EXPAND:
            ent = BigWorld.entities.get(self.npcId)
            if ent:
                ent.cell.enlargeStorageSlot()
        elif self.expandType == uiConst.EXPAND_MATERIAL_BAG_ACTIVE:
            page, pos = p.inv.findItemById(self.costItemId)
            if page != const.CONT_NO_PAGE and pos != const.CONT_NO_POS:
                item = p.inv.getQuickVal(page, pos)
                if item:
                    p.useBagItem(page, pos)
            else:
                p.showGameMsg(GMDD.data.NO_ITEM_TO_ACTIVE_MATERIAL_BAG, ())
        elif self.expandType == uiConst.EXPAND_RIDE_WING_BAG_EXPAND:
            p.base.enlargeRideWingBagSlot(self.data.get('page', 0))
        elif self.expandType == uiConst.EXPAND_MATERIAL_BAG_EXPAND:
            p.base.toEnlargeMaterialBagSlot()
        elif self.expandType == uiConst.EXPAND_SPRITE_MATERIAL_BAG_EXPAND:
            p.base.toEnlargeSpriteMaterialBagSlot()
        elif self.expandType == uiConst.EXPAND_WARDROBE_DYE_EXPAND:
            uuid = self.data.get('uuid', '')
            if uuid:
                p.base.requireAddDyeScheme(uuid, self.slotIdx + 3)
        elif self.expandType == uiConst.EXPAND_RUNE_INV_EXPAND:
            gamelog.info('jbx:enlargeHierogramBagSlot')
            p.base.enlargeHierogramBagSlot()
        self.hide()

    def updateNpcId(self, npcId):
        self.npcId = npcId
