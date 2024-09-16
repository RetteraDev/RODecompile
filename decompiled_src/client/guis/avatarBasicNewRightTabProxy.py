#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/avatarBasicNewRightTabProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from gamestrings import gameStrings
from asObject import ASObject
from uiProxy import UIProxy
import gamelog
TOTAL_TAB_NUM = 6

class AvatarBasicNewRightTabProxy(UIProxy):
    TAB_LABEL_MAP = {'fuse': gameStrings.AVATAR_BASIC_NEW_TAB_SKINCOLOR,
     'shangshen': gameStrings.AVATAR_BASIC_NEW_TAB_UPPERBODY,
     'xiashen': gameStrings.AVATAR_BASIC_NEW_TAB_LOWERBODY,
     'quti': gameStrings.AVATAR_BASIC_NEW_TAB_BODY,
     'mianbu': gameStrings.AVATAR_BASIC_NEW_TAB_FACE,
     'mei': gameStrings.AVATAR_BASIC_NEW_TAB_BROW,
     'yanxing': gameStrings.AVATAR_BASIC_NEW_TAB_EYE,
     'yanzhuang': gameStrings.AVATAR_BASIC_NEW_TAB_EYESHADOW,
     'zui': gameStrings.AVATAR_BASIC_NEW_TAB_MOUTH,
     'lunkuo': gameStrings.AVATAR_BASIC_NEW_TAB_OUTLINE}

    def __init__(self, uiAdapter):
        super(AvatarBasicNewRightTabProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_AVATAR_BASIC_NEW_RIGHT_TAB, self.hide)
        self.selectItem = None

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_AVATAR_BASIC_NEW_RIGHT_TAB:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_AVATAR_BASIC_NEW_RIGHT_TAB)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_AVATAR_BASIC_NEW_RIGHT_TAB)

    def initUI(self):
        for i in xrange(TOTAL_TAB_NUM):
            tab = self.widget.all.getChildByName('tab%d' % i)
            tab.addEventListener(events.BUTTON_CLICK, self.onTabClickBtn, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return

    def refreshTabs(self, tabArr, default = 0):
        if not self.widget or tabArr == None:
            return
        else:
            gamelog.debug('ypc@ refreshTabs!')
            tabNum = len(tabArr)
            for i in xrange(TOTAL_TAB_NUM):
                tab = self.widget.all.getChildByName('tab%d' % i)
                if i < tabNum:
                    tab.visible = True
                    tab.label = self.TAB_LABEL_MAP.get(tabArr[i], '')
                    tab.data = tabArr[i]
                    if default == i:
                        tab.selected = True
                        self.selectItem = tab
                    else:
                        tab.selected = False
                else:
                    tab.visible = False
                    tab.data = ''
                    tab.selected = False

            return

    def onTabClickBtn(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        if self.selectItem:
            self.selectItem.selected = False
        target.selected = True
        self.selectItem = target
        data = target.data
        if data not in self.TAB_LABEL_MAP:
            return
        gameglobal.rds.ui.characterDetailAdjust.clickItemAdjust(data)
