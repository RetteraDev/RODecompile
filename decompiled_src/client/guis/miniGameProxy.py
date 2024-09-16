#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/miniGameProxy.o
from gamestrings import gameStrings
import BigWorld
CEFModule = None
try:
    import CEFManager as CEFModule
except:
    CEFModule = None

import gameglobal
import gamelog
from guis import events
from guis import uiConst
from uiProxy import UIProxy
from data import sys_config_data as SYSCD

class MiniGameProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MiniGameProxy, self).__init__(uiAdapter)
        self.widget = None
        self.width = 1105
        self.height = 623
        self.textureCreated = False
        self.closeMsgId = None
        self.swfPath = 'gui/widgets/MiniGameWidget' + uiAdapter.getUIExt()
        self.insName = 'MiniGameWebUnit'
        self.oldX = 0
        self.oldY = 0
        self.url = None
        self.interactiveObjId = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_MINI_GAME, self.onClose)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MINI_GAME:
            self.widget = widget
            self.initUI()

    def refreshDrawToFlash(self):
        CEFModule.drawToFlash(self.swfPath, self.insName, 0, 0, self.width, self.height)

    def textureChangeCallback(self, width, height):
        gamelog.debug('m.l@MiniGameProxy.textureChangeCallback', width, height)
        self.refreshDrawToFlash()

    def connectionBindedCallback(self, bind):
        gamelog.debug('m.l@MiniGameProxy.connectionBindedCallback', bind)
        CEFModule.loadURL(self.url)
        CEFModule.resize(self.width, self.height)
        self.refreshDrawToFlash()

    def onClose(self, *arg):
        msg = SYSCD.data.get('confirmQuitMiniGameMsg', gameStrings.TEXT_MINIGAMEPROXY_57)
        if self.closeMsgId:
            gameglobal.rds.ui.messageBox.dismiss(self.closeMsgId)
            self.cancelSexBoxId = None
        self.closeMsgId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.leaveMiniGame, yesBtnText=gameStrings.TEXT_IMPPLAYERTEAM_644, noBtnText=gameStrings.TEXT_AVATAR_2876_1, isModal=False, msgType='pushLoop', textAlign='center')

    def leaveMiniGame(self):
        self.closeMsgId = None
        BigWorld.player().quitInteractiveObj()
        self.hide()

    def clearWidget(self):
        self.widget = None
        CEFModule.setVisible(False)
        CEFModule.setPosition(0, 0)
        CEFModule.loadURL('about:blank')
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MINI_GAME)
        self.reset()

    def show(self, interactiveObjId, url):
        if not CEFModule:
            return
        self.interactiveObjId = interactiveObjId
        self.url = url
        CEFModule.setConnBindedCallback(self.connectionBindedCallback)
        CEFModule.setTextureChangeCallback(self.textureChangeCallback)
        if not CEFModule.isCefProcessRunning():
            swShow = gameglobal.SW_HIDE if BigWorld.isPublishedVersion() else gameglobal.SW_SHOW
            CEFModule.openCefProcess(gameglobal.CEF_PROCESS_NAME, self.width, self.height, swShow)
        CEFModule.resize(self.width, self.height)
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_MINI_GAME)
        else:
            self.initUI()

    def initUI(self):
        if not self.widget:
            return
        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.onClose, False, 1, True)
        self.refreshDrawToFlash()
        self.oldX = int(self.widget.x + self.widget.photo.x)
        self.oldY = int(self.widget.y + self.widget.photo.y)
        self.widget.addEventListener(events.EVENT_ENTER_FRAME, self.onEnterFrame, False, 0, True)
        if hasattr(CEFModule, 'initImgBuff'):
            CEFModule.initImgBuff()
        CEFModule.setPosition(self.oldX, self.oldY)
        CEFModule.resize(self.width, self.height)
        CEFModule.setVisible(True)
        CEFModule.loadURL(self.url)
        CEFModule.setCefRequestCallback(self.handleCEFRequest)

    def handleCEFRequest(self, request, requestLen):
        pass

    def getDPIScale(self):
        if 'win10' in BigWorld.getOSDesc().lower() or 'win8' in BigWorld.getOSDesc().lower():
            return BigWorld.getScreenDPI()[0] / 96.0
        return 1.0

    def onEnterFrame(self, *args):
        x = int(self.widget.x + self.widget.photo.x * self.widget.scaleX)
        y = int(self.widget.y + self.widget.photo.y * self.widget.scaleY)
        if self.oldX != x or self.oldY != y:
            CEFModule.setPosition(x, y)
            self.oldX = x
            self.oldY = y
            scale = self.getDPIScale()
            CEFModule.setScale(self.widget.scaleX / scale, self.widget.scaleY / scale)

    def reset(self):
        self.url = None
        self.closeMsgId = None
        self.textureCreated = False
        self.interactiveObjId = None
