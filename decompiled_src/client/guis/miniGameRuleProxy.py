#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/miniGameRuleProxy.o
import BigWorld
import gameglobal
import uiUtils
from gameStrings import gameStrings
from guis import events
from guis import uiConst
from uiProxy import UIProxy
from data import item_data as ID
from data import mini_game_data as MGD

class MiniGameRuleProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MiniGameRuleProxy, self).__init__(uiAdapter)
        self.widget = None
        self.miniGameId = 0
        self.enoughItem = True
        uiAdapter.registerEscFunc(uiConst.WIDGET_MINI_GAME_RULE, self.onClose)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MINI_GAME_RULE:
            self.widget = widget
            self.initUI()

    def onClose(self, *arg):
        self.hide()

    def onConfirm(self, *args):
        if not self.enoughItem:
            keyWord = MGD.data.get(self.miniGameId, {}).get('keyWord', gameStrings.MINI_GAME_DUUDLE)
            gameglobal.rds.ui.help.show(keyWord)
            return
        if self.confirmCallback:
            self.confirmCallback()
        self.hide()

    def onCancel(self, *args):
        self.hide()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MINI_GAME_RULE)
        self.reset()

    def show(self, miniGameId, confirmCallback):
        self.miniGameId = miniGameId
        self.confirmCallback = confirmCallback
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_MINI_GAME_RULE)
        else:
            self.initUI()

    def initUI(self):
        if not self.widget:
            return
        self.widget.defaultCloseBtn = self.widget.closeBtn
        miniGameInfo = MGD.data.get(self.miniGameId, {})
        consumeItemId = miniGameInfo.get('consumeItemId')
        consumeItemNum = miniGameInfo.get('consumeItemNum')
        itemInfo = uiUtils.getGfxItemById(consumeItemId)
        self.widget.consumeItem.setItemSlotData(itemInfo)
        itemName = ID.data.get(consumeItemId, {}).get('name', '')
        ownCount = BigWorld.player().inv.countItemInPages(consumeItemId)
        self.widget.miniGameRuleTitleTF.text = miniGameInfo.get('descTitle', '')
        self.widget.miniGameRuleDescTF.text = miniGameInfo.get('desc', '')
        self.widget.itemNameTF.text = itemName
        self.widget.itemNumTF.text = '%d/%d' % (ownCount, consumeItemNum)
        self.enoughItem = consumeItemNum <= ownCount
        self.widget.itemNumTF.textColor = '0xFFFFFF' if self.enoughItem else '0xF43804'
        if not self.enoughItem:
            self.widget.confirmBtn.label = gameStrings.MINI_GAME_NO_ENOUGH_ITEM
        self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.onConfirm, False, 1, True)

    def reset(self):
        self.miniGameId = 0
        self.confirmCallback = None
