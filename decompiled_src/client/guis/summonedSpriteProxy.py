#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/summonedSpriteProxy.o
import BigWorld
import gameglobal
import uiConst
from uiProxy import UIProxy
from asObject import ASObject
from cdata import game_msg_def_data as GMDD
PROFILE_PATH = 'widgets/SummonedSpriteProfileWidget.swf'

class SummonedSpriteProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedSpriteProxy, self).__init__(uiAdapter)
        self.widget = None
        self.tabMap = {uiConst.SUMMONED_SPRITE_TAB_PROFILE: 'summonedSpriteProfile'}
        self.tabIdx = uiConst.SUMMONED_SPRITE_TAB_PROFILE
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_SPRITE, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_SPRITE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.unRegisterPanel()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_SPRITE)

    def reset(self):
        self.tabIdx = uiConst.SUMMONED_SPRITE_TAB_PROFILE

    def show(self):
        enableSummonedSprite = gameglobal.rds.configData.get('enableSummonedSprite', False)
        if not enableSummonedSprite:
            return
        p = BigWorld.player()
        if not BigWorld.player().summonSpriteList:
            p.showGameMsg(GMDD.data.NO_SUMMONED_SPRITE_TO_SHOW, ())
            if not BigWorld.isPublishedVersion():
                gameglobal.rds.ui.summonedSpriteGM.show()
            return
        gameglobal.rds.ui.summonedWarSprite.show()
        if self.widget:
            self.refreshInfo()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_SPRITE)
        if not BigWorld.isPublishedVersion():
            gameglobal.rds.ui.summonedSpriteGM.show()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.tabButtons = [self.widget.profileBtn]
        self.widget.tabViewPaths = [PROFILE_PATH]
        self.widget.onTabChanged = self.onTabChanged

    def getCurrentProxy(self):
        return getattr(self.uiAdapter, self.tabMap.get(self.tabIdx, ''), None)

    def onTabChanged(self, *args):
        currentTabIndex = int(args[3][0].GetNumber())
        currentView = ASObject(args[3][1])
        self.unRegisterPanel()
        self.tabIdx = currentTabIndex
        proxy = self.getCurrentProxy()
        if proxy and hasattr(proxy, 'initPanel'):
            proxy.initPanel(currentView)

    def unRegisterPanel(self):
        proxy = self.getCurrentProxy()
        if proxy and hasattr(proxy, 'unRegisterPanel'):
            proxy.unRegisterPanel()

    def refreshInfo(self):
        if not self.widget:
            return
        proxy = self.getCurrentProxy()
        if proxy and hasattr(proxy, 'refreshInfo'):
            proxy.refreshInfo()
