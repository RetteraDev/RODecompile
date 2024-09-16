#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildBillBoardProxy.o
from gamestrings import gameStrings
import os
import BigWorld
from Scaleform import GfxValue
import gameglobal
import C_ui
import const
from PIL import Image
from guis import uiConst
from uiProxy import UIProxy
from guis import uiUtils
from ui import gbk2unicode

class GuildBillBoardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildBillBoardProxy, self).__init__(uiAdapter)
        self.modelMap = {'report': self.onReport,
         'help': self.onHelp,
         'select': self.onSelect,
         'confirm': self.onConfirm,
         'refresh': self.onRefresh,
         'getError': self.onGetError,
         'closeHelp': self.onCloseHelp,
         'isReportBtnVisible': self.onIsReportBtnVisible}
        self.mainMediator = None
        self.helpMediator = None
        self.filePath = ''
        self.srcResPath = ''
        self.imagePath = ''
        self.fortId = 0
        self.status = 0
        self.entity = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_BILL_BOARD, self.hide)
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_BILL_BOARD_HELP, self.hideHelp)

    def reset(self):
        self.filePath = ''
        self.srcResPath = ''
        self.imagePath = ''
        self.fortId = 0
        self.status = 0
        self.entity = None

    def show(self, fortId, entity):
        self.fortId = fortId
        self.entity = entity
        self.entity.downloadAdvertise()
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_BILL_BOARD)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_BILL_BOARD:
            self.mainMediator = mediator
            self.updateAuthorization()
        elif widgetId == uiConst.WIDGET_GUILD_BILL_BOARD_HELP:
            self.helpMediator = mediator

    def clearWidget(self):
        self.mainMediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_BILL_BOARD)
        self.hideHelp()

    def onHelp(self, *arg):
        if self.helpMediator:
            self.hideHelp()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_BILL_BOARD_HELP)

    def hideHelp(self):
        self.helpMediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_BILL_BOARD_HELP)

    def onCloseHelp(self, *arg):
        self.hideHelp()

    def onSelect(self, *arg):
        if hasattr(C_ui, 'ayncOpenFileDialog'):
            workPath = os.getcwd()
            C_ui.ayncOpenFileDialog(gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_1174, gameStrings.TEXT_CUSTOMERSERVICEVIPPROXY_179, workPath, self.onSelectFile)

    def onSelectFile(self, path):
        if not path or not (path.endswith('.jpg') or path.endswith('.png')):
            return
        self.filePath = path
        i = path.rfind('\\')
        i = path.rfind('/') if i == -1 else i
        fileName = path if i == -1 else path[i + 1:]
        i = fileName.find('.')
        extension = fileName[i:]
        fileName = fileName if i == -1 else fileName[:i]
        self.srcResPath = const.IMAGES_DOWNLOAD_DIR + '/' + fileName + extension
        self.imagePath = const.IMAGES_DOWNLOAD_DIR + '/' + fileName + '.dds'
        uiUtils.copyToImagePath(self.filePath)
        im = Image.open(self.srcResPath)
        im = im.resize((512, 256))
        im.save(self.srcResPath)
        BigWorld.convert2DXT5(self.srcResPath, const.IMAGES_DOWNLOAD_DIR)
        if self.mainMediator:
            self.mainMediator.Invoke('setFilePath', (GfxValue(gbk2unicode(fileName) + extension), GfxValue('../' + self.imagePath)))

    def onGetError(self, *arg):
        self.setError(self.status)

    def setError(self, status):
        self.status = status
        if self.mainMediator:
            errorFlag = False
            refreshBtnVisible = False
            text = ''
            if status == 1:
                errorFlag = True
                refreshBtnVisible = True
                text = gameStrings.TEXT_GUILDBILLBOARDPROXY_122
            elif status == 2:
                errorFlag = True
                text = gameStrings.TEXT_GUILDBILLBOARDPROXY_125
            elif status == 3:
                errorFlag = True
                text = gameStrings.TEXT_GUILDBILLBOARDPROXY_128
            info = {}
            info['errorFlag'] = errorFlag
            info['refreshBtnVisible'] = refreshBtnVisible
            info['text'] = text
            self.mainMediator.Invoke('setError', uiUtils.dict2GfxDict(info, True))

    def onConfirm(self, *arg):
        if self.entity:
            self.entity.uploadAdvertise(self.imagePath)

    def onRefresh(self, *arg):
        if self.entity:
            BigWorld.callback(10, self.updateAuthorization)
            self.entity.refreshAdvertise()

    def updateAuthorization(self):
        if self.mainMediator and self.entity:
            canUse = self.entity.checkClickPermission()
            self.mainMediator.Invoke('updateAuthorization', GfxValue(canUse))

    def onReport(self, *arg):
        p = BigWorld.player()
        srcId = uiConst.MENU_GUILD_BILLBOARD_PICTURE
        fort = p.clanWar.fort.get(self.fortId, {})
        if fort:
            guildName = fort.ownerGuildName
            gameglobal.rds.ui.prosecute.show(guildName, srcId)

    def onIsReportBtnVisible(self, *args):
        p = BigWorld.player()
        fort = p.clanWar.fort.get(self.fortId, {})
        if fort:
            ownerGuildNUID = fort.ownerGuildNUID
            if ownerGuildNUID:
                return GfxValue(True)
        return GfxValue(False)
