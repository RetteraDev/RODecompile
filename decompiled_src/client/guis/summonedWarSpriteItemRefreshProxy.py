#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteItemRefreshProxy.o
import BigWorld
import uiConst
import summonSpriteExplore
import gameglobal
from guis import uiUtils
from uiProxy import UIProxy
from gameStrings import gameStrings
from data import sys_config_data as SCD

class SummonedWarSpriteItemRefreshProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteItemRefreshProxy, self).__init__(uiAdapter)
        self.widget = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_WAR_SPRITE_ITEM_REFRESH, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_WAR_SPRITE_ITEM_REFRESH:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_ITEM_REFRESH)

    def reset(self):
        pass

    def show(self):
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_ITEM_REFRESH, True)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        exploreSprite = p.spriteExtraDict['exploreSprite']
        bonusId = exploreSprite.bonusId
        option = exploreSprite.option
        itemId = summonSpriteExplore.getItemIdByBonusId(option, bonusId)
        self.widget.itemSlot.slot.fitSize = True
        self.widget.itemSlot.slot.dragable = False
        itemInfo = uiUtils.getGfxItemById(itemId)
        self.widget.itemSlot.slot.setItemSlotData(itemInfo)
        refreshTimes = exploreSprite.refreshTimes
        refreshTimesLimit = gameglobal.rds.ui.summonedWarSpriteExplore.getSpriteExploreRefreshTimes()
        self.widget.refreshBtn.enabled = refreshTimes < refreshTimesLimit
        self.widget.refreshBtn.label = gameStrings.SPRITE_ITEM_REFRESH_BTN_LABEL % (refreshTimes, refreshTimesLimit)

    def _onRefreshBtnClick(self, e):
        p = BigWorld.player()
        p.base.exploreSpriteRefreshBonus()
