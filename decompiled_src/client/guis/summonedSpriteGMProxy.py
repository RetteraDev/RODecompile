#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedSpriteGMProxy.o
import BigWorld
import gameglobal
from uiProxy import UIProxy
from guis import uiConst
from guis import events
from guis.asObject import ASObject
from guis.asObject import ASUtils
from data import sys_config_data as SCD
from data import item_data as ID
SPRITTE_HEIGHT = 24

class SummonedSpriteGMProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedSpriteGMProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_SPRITE_GM, self.onClose)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_SPRITE_GM:
            self.widget = widget
            self.initUI()

    def onClose(self, *arg):
        self.hide()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_SPRITE_GM)
        self.reset()

    def show(self):
        enableSummonedSprite = gameglobal.rds.configData.get('enableSummonedSprite', False)
        if not enableSummonedSprite:
            return
        self.reset()
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_SPRITE_GM)
        else:
            self.initUI()

    def initUI(self):
        if not self.widget:
            return
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.initSpriteList()

    def initSpriteList(self):
        self.widget.spriteList.itemRenderer = 'SummonedSpriteGM_ListItemRenderer'
        self.widget.spriteList.lableFunction = self.itemFunction
        self.widget.spriteList.itemHeight = SPRITTE_HEIGHT
        self.widget.spriteList.scrollbar.addEventListener(events.MOUSE_WHEEL, self.handleWheel, False, 1, True)
        self.widget.showActionBtn.addEventListener(events.MOUSE_CLICK, self.handleShowAction, False, 0, True)
        self.refreshInfo()

    def setStateText(self, text):
        if not self.widget:
            return
        self.widget.statusTF.htmlText = text

    def handleShowAction(self, *args):
        sprite = BigWorld.player().summonedSpriteInWorld
        if sprite:
            BigWorld.debugAQ(sprite.model)
        else:
            BigWorld.debugAQ(None)

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        info = ID.data.get(itemData.itemId, {})
        itemMc.nameTF.text = info.get('name', '')
        itemMc.IDTF.text = itemData.itemId
        itemMc.getSpriteBtn.addEventListener(events.MOUSE_CLICK, self.handleGetSprite, False, 0, True)
        ASUtils.setMcData(itemMc.getSpriteBtn, 'data', itemData)

    def handleGetSprite(self, *args):
        e = ASObject(args[3][0])
        data = e.currentTarget.data
        msg = '$getitem 0 %s 1' % str(int(data.itemId))
        BigWorld.player().cell.adminOnCell(msg)

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.refreshSpriteList()

    def refreshSpriteList(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.spriteInfoList = []
        spriteList = SCD.data.get('zhanlingGMindex', ())
        for spriteItemId in spriteList:
            info = ID.data.get(spriteItemId, {})
            spriteInfo = {}
            spriteInfo['name'] = info.get('name', '')
            spriteInfo['itemId'] = spriteItemId
            self.spriteInfoList.append(spriteInfo)

        self.widget.spriteList.dataArray = self.spriteInfoList

    def handleWheel(self, *args):
        e = ASObject(args[3][0])

    def reset(self):
        pass
