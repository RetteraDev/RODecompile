#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/reliveMsgBoxProxy.o
from Scaleform import GfxValue
import gameglobal
import gamelog
from guis import uiConst
from guis.ui import gbk2unicode
from guis.uiProxy import UIProxy

class ReliveMsgBoxProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ReliveMsgBoxProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerReliveMsgBox': self.onRegisterReliveMsgBox,
         'getReliveMsgData': self.onGetReliveMsgData,
         'clickBtn': self.onClickBtn,
         'completeCountDown': self.onCompleteCountDown}
        self.title = ''
        self.content = ''
        self.buttons = []
        self.repeat = 0
        self.freeze = False
        self.mc = None

    def onRegisterReliveMsgBox(self, *arg):
        gamelog.debug('wy:onRegisterReliveMsgBox')
        self.mc = arg[3][0]

    def onGetReliveMsgData(self, *arg):
        gamelog.debug('wy:onGetReliveMsgData')
        movie = arg[0]
        messageBox = movie.CreateObject()
        messageBoxBtns = movie.CreateArray()
        buttonEnbales = movie.CreateArray()
        interval = 1000.0
        repeat = 3 if self.freeze else self.repeat
        if repeat != 0:
            timer = movie.CreateArray()
            timer.SetElement(0, GfxValue(interval))
            timer.SetElement(1, GfxValue(repeat))
            messageBox.SetMember('timer', timer)
        for i, btn in enumerate(self.buttons):
            messageBoxBtns.SetElement(i, GfxValue(gbk2unicode(btn.title)))
            buttonEnbales.SetElement(i, GfxValue(btn.enable))

        messageBox.SetMember('title', GfxValue(gbk2unicode(self.title)))
        messageBox.SetMember('contenttext', GfxValue(gbk2unicode(self.content)))
        messageBox.SetMember('btnList', messageBoxBtns)
        messageBox.SetMember('btnEnable', buttonEnbales)
        return messageBox

    def onCompleteCountDown(self, *arg):
        self.dismiss()
        gameglobal.rds.ui.messageBox.mediator.SetVisible(True)

    def onClickBtn(self, *args):
        idx = int(args[3][0].GetString())
        button = self.buttons[idx]
        gamelog.debug('zt: click button***', button.title, button.dismissOnClick)
        if button.enable and callable(button.onClickCallback):
            button.onClickCallback()
        else:
            gamelog.debug('zt: can not response to click, enable=', button.enable, 'callable=', callable(button.onClickCallback))
        gamelog.debug('zt: click button---', button.title, button.dismissOnClick)
        if button.dismissOnClick:
            self.dismiss()
        gamelog.debug('zt: click button+++', button.title, button.dismissOnClick)

    def dismiss(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_RELIVE_MSG_BOX)
        self.buttons = []
        self.repeat = 0
        self.freeze = False

    def show(self, isModal, title, content, buttonList, freeze = False, repeat = 0):
        gamelog.debug('wy:relive show')
        self.title = title
        self.content = content
        self.buttons = buttonList
        self.freeze = freeze
        self.repeat = repeat
        self.uiAdapter.loadWidget(uiConst.WIDGET_RELIVE_MSG_BOX, isModal)
