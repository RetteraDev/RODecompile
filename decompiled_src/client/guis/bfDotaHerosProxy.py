#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bfDotaHerosProxy.o
import BigWorld
CEFModule = None
try:
    import CEFManager as CEFModule
except:
    CEFModule = None

import gameglobal
import gamelog
import utils
import formula
from helpers import CEFControl
from guis import events
from guis import uiConst
from uiProxy import UIProxy
from cdata import game_msg_def_data as GMDD
URL_TYPE_DEVELOPER = 1
URL_TYPE_QC_TEST = 2
URL_TYPE_RELEASE = 3
URL_DEVELOPER = 'http://sq.tianyu.163.com:3000/2017/kingoflegend/tygamec/inner'
URL_QC_TEST = 'http://hd-test-qc.tianyu.163.com/2017/kingoflegend/tygamec/inner'
URL_RELEASE = 'https://hd.tianyu.163.com/2017/kingoflegend/tygamec/inner'

class BfDotaHerosProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BfDotaHerosProxy, self).__init__(uiAdapter)
        self.widget = None
        self.width = 1107
        self.height = 620
        self.textureCreated = False
        self.swfPath = 'gui/widgets/BfDotaHerosWidget' + uiAdapter.getUIExt()
        self.insName = 'BfDotaHeros_Content'
        self.oldX = 0
        self.oldY = 0
        self.tokenUrl = ''
        if BigWorld.isPublishedVersion():
            self.urlMode = URL_TYPE_RELEASE
        else:
            self.urlMode = URL_TYPE_QC_TEST
        uiAdapter.registerEscFunc(uiConst.WIDGET_BF_DOTA_HEROS, self.onClose)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BF_DOTA_HEROS:
            self.widget = widget
            self.initUI()

    def refreshDrawToFlash(self):
        CEFModule.drawToFlash(self.swfPath, self.insName, 0, 0, self.width, self.height)

    def textureChangeCallback(self, width, height):
        self.refreshDrawToFlash()

    def connectionBindedCallback(self, bind):
        CEFControl.logMsg('jbx:connectionBindedCallback')
        CEFModule.loadURL(self.tokenUrl)
        CEFModule.resize(self.width, self.height)
        self.refreshDrawToFlash()

    def onClose(self, *arg):
        self.hide()

    def clearWidget(self):
        self.reset()
        self.widget = None
        CEFModule.setVisible(False)
        CEFModule.setPosition(0, 0)
        CEFModule.loadURL('about:blank')
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BF_DOTA_HEROS)

    def show(self):
        if formula.inBattleField(BigWorld.player().mapID):
            BigWorld.player().showGameMsg(GMDD.data.CAN_NOT_OPEN_IN_BF, ())
            return
        if not CEFModule:
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BF_DOTA_HEROS)

    def getTokenCallBack(self, tokenStr):
        CEFControl.logMsg('jbx:getTokenCallback')
        if self.urlMode == URL_TYPE_DEVELOPER:
            url = URL_DEVELOPER
        elif self.urlMode == URL_TYPE_QC_TEST:
            url = URL_QC_TEST
        else:
            url = URL_RELEASE
        self.tokenUrl = '%s%s' % (url, CEFControl.getUrlExtendParamsStr(('tyGameCredential', tokenStr)))
        CEFModule.setConnBindedCallback(self.connectionBindedCallback)
        CEFModule.setTextureChangeCallback(self.textureChangeCallback)
        if not CEFModule.isCefProcessRunning():
            swShow = gameglobal.SW_HIDE if BigWorld.isPublishedVersion() else gameglobal.SW_SHOW
            CEFModule.openCefProcess(gameglobal.CEF_PROCESS_NAME, self.width, self.height, swShow)
        else:
            self.connectionBindedCallback(True)
        CEFModule.resize(self.width, self.height)

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
        CEFModule.loadURL('about:blank')
        CEFControl.logMsg('jbx:initUI')
        if hasattr(CEFModule, 'setCefRequestCallback'):
            CEFModule.setCefRequestCallback(CEFControl.handleCEFRequest)
        BigWorld.player().base.queryBattleFieldDotaTokenBase()

    def onEnterFrame(self, *args):
        x = int(self.widget.x + self.widget.photo.x * self.widget.scaleX)
        y = int(self.widget.y + self.widget.photo.y * self.widget.scaleY)
        if self.oldX != x or self.oldY != y:
            CEFModule.setPosition(x, y)
            self.oldX = x
            self.oldY = y
            scale = CEFControl.getDPIScale()
            CEFModule.setScale(self.widget.scaleX / scale, self.widget.scaleY / scale)

    def reset(self):
        self.textureCreated = False
        self.tokenUrl = ''
