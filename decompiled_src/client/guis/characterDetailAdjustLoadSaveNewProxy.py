#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/characterDetailAdjustLoadSaveNewProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from asObject import ASObject
from uiProxy import UIProxy
import gamelog

class CharacterDetailAdjustLoadSaveNewProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CharacterDetailAdjustLoadSaveNewProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_NEW_CHARACTER_DETAIL_ADJUST_LOADSAVENEW_TOP, self.hide)
        uiAdapter.registerEscFunc(uiConst.WIDGET_NEW_CHARACTER_DETAIL_ADJUST_LOADSAVENEW_BOTTOM, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_NEW_CHARACTER_DETAIL_ADJUST_LOADSAVENEW_TOP:
            self.widget = widget
            self.initUITop()
        elif widgetId == uiConst.WIDGET_NEW_CHARACTER_DETAIL_ADJUST_LOADSAVENEW_BOTTOM:
            self.widget = widget
            self.initUIBottom()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_NEW_CHARACTER_DETAIL_ADJUST_LOADSAVENEW_TOP)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_NEW_CHARACTER_DETAIL_ADJUST_LOADSAVENEW_TOP)

    def initUITop(self):
        self.widget.top.resetBtn.addEventListener(events.BUTTON_CLICK, self.clickBtn, False, 0, True)
        self.widget.top.randomBtn.addEventListener(events.BUTTON_CLICK, self.clickBtn, False, 0, True)
        self.widget.top.recoverBtn.addEventListener(events.BUTTON_CLICK, self.clickBtn, False, 0, True)

    def initUIBottom(self):
        self.widget.bottom.saveBtn.addEventListener(events.BUTTON_CLICK, self.clickBtn, False, 0, True)
        self.widget.bottom.loadBtn.addEventListener(events.BUTTON_CLICK, self.clickBtn, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return

    def _onConfirmBtnClick(self, e):
        print 'onConfirmBtnClick:', e.target, e.type

    def clickBtn(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        gamelog.debug('ypc@ button clicked ! ', target.name)
        if target.name == 'saveBtn':
            gameglobal.rds.ui.characterDetailAdjust.saveNpcConfig('manual_save')
        elif e.target.name == 'loadBtn':
            gameglobal.rds.ui.characterDetailAdjust.readAvatarConfig()
        elif e.target.name == 'resetBtn':
            gameglobal.rds.ui.characterDetailAdjust.resetAvatarConfig()
        elif e.target.name == 'randomBtn':
            gameglobal.rds.ui.characterDetailAdjust.clickRandom()
        elif e.target.name == 'recoverBtn':
            gameglobal.rds.ui.characterDetailAdjust.clickRecover()
