#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/worldBossCardGetProxy.o
import BigWorld
import gameglobal
import uiConst
from guis import events
from uiProxy import UIProxy
from guis import worldBossHelper

class WorldBossCardGetProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WorldBossCardGetProxy, self).__init__(uiAdapter)
        self.widget = None
        self.currentBossId = 0
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WORLD_CARD_GET, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WORLD_CARD_GET:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WORLD_CARD_GET)

    def show(self, bossId):
        self.currentBossId = bossId
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WORLD_CARD_GET)

    def initUI(self):
        self.widget.bottomMc.confirmBtn.addEventListener(events.BUTTON_CLICK, self.onConfirmBtnClick)

    def onConfirmBtnClick(self, *args):
        self.hide()

    def refreshInfo(self):
        if not self.widget:
            return
        self.removeAllChild(self.widget.loadMc)
        bossInfo = worldBossHelper.getInstance().getBossBaseInfoByBossId(self.currentBossId)
        if not bossInfo.get('isRare', False):
            self.widget.title.gotoAndPlay('normal')
            mc = self.widget.getInstByClsName('WorldBossCardGet_normalCard')
            self.widget.loadMc.addChild(mc)
            self.setNormalCardInfo(mc.cardMc, bossInfo)
        else:
            mc = self.widget.getInstByClsName('WorldBossCardGet_rareCard')
            self.widget.loadMc.addChild(mc)
            self.widget.title.gotoAndPlay('rare')
            self.setRareCardInfo(mc.cardMc, bossInfo)

    def removeAllChild(self, mc):
        while mc.numChildren > 0:
            mc.removeChildAt(0)

    def setNormalCardInfo(self, cardMc, info):
        cardMc.content.icon.fitSize = True
        cardMc.content.icon.loadImage(info['bossIcon'])
        cardMc.content.textInfo.bossName.text = info['bossName']
        cardMc.content.textInfo.detail.text = info.get('desc', '...')

    def setRareCardInfo(self, cardMc, info):
        cardMc.content.icon.fitSize = True
        cardMc.content.icon.loadImage(info['bossIcon'])
        cardMc.content.textInfo.bossName.text = info['bossName']
        cardMc.content.textInfo.detail.text = info.get('desc', '...')
