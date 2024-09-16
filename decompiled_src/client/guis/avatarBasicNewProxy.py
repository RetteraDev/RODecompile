#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/avatarBasicNewProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from asObject import ASObject
from uiProxy import UIProxy

class AvatarBasicNewProxy(UIProxy):
    RIGHT_TAB_MAP = {'zhengti': (),
     'faxing': (),
     'body': ('fuse', 'shangshen', 'xiashen', 'quti'),
     'wuguan': ('mianbu', 'mei', 'yanxing', 'yanzhuang', 'zui', 'lunkuo')}

    def __init__(self, uiAdapter):
        super(AvatarBasicNewProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_AVATAR_BASIC_NEW, self.hide)
        self.selectItem = None

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_AVATAR_BASIC_NEW:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_AVATAR_BASIC_NEW)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_AVATAR_BASIC_NEW)

    def initUI(self):
        self.widget.all.zhengti.addEventListener(events.BUTTON_CLICK, self.handleMenuBtnClick, False, 0, True)
        self.widget.all.faxing.addEventListener(events.BUTTON_CLICK, self.handleMenuBtnClick, False, 0, True)
        self.widget.all.wuguan.addEventListener(events.BUTTON_CLICK, self.handleMenuBtnClick, False, 0, True)
        self.widget.all.body.addEventListener(events.BUTTON_CLICK, self.handleMenuBtnClick, False, 0, True)
        self.widget.all.zhengti.selected = True
        self.selectItem = self.widget.all.zhengti
        gameglobal.rds.ui.avatarBasicNewRightTab.refreshTabs(self.RIGHT_TAB_MAP.get('yushe', ()), 0)

    def refreshInfo(self):
        if not self.widget:
            return

    def _onConfirmBtnClick(self, e):
        print 'onConfirmBtnClick:', e.target, e.type

    def handleMenuBtnClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        if target.name not in self.RIGHT_TAB_MAP:
            return
        if self.selectItem:
            self.selectItem.selected = False
        target.selected = True
        self.selectItem = target
        tabArr = self.RIGHT_TAB_MAP[target.name]
        gameglobal.rds.ui.avatarBasicNewRightTab.refreshTabs(tabArr)
        if len(tabArr) == 0:
            gameglobal.rds.ui.characterDetailAdjust.clickItemAdjust(target.name)
        else:
            gameglobal.rds.ui.characterDetailAdjust.clickItemAdjust(tabArr[0])
