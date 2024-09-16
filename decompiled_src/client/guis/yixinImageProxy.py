#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/yixinImageProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gamelog
import const
import gametypes
from guis import uiConst
from guis.ui import gbk2unicode
from guis.uiProxy import UIProxy

class YixinImageProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(YixinImageProxy, self).__init__(uiAdapter)
        self.modelMap = {'refreshPanel': self.onRefreshPanel}
        self.mediator = None
        self.isShow = False
        self.imagePath = ''
        self.isLoading = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_YIXIN_IMAGE, self.closeWidget)

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator

    def hide(self, *args):
        self.closeWidget()

    def closeWidget(self):
        if self.isShow:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_YIXIN_IMAGE)
        self.isShow = False
        self.mediator = None
        self.isLoading = False

    def show(self, imagePath):
        self.imagePath = imagePath
        if not gameglobal.rds.configData.get('enableYixinImage', False):
            return
        if not self.isShow:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_YIXIN_IMAGE)
        if self.mediator:
            self.startLoadImage()
        self.isShow = True

    def startLoadImage(self):
        self.isLoading = True
        imagePath = self.sepImageUrl()
        if len(imagePath) >= 3:
            account = imagePath[1]
            path1 = imagePath[2]
            path = path1 + '?imageView&pixel=200000'
            path1 = path.replace('?', '')
            BigWorld.player().downloadYixinFile(account, path, self.downLoadedImage, (account, path1))
        else:
            return

    def downLoadedImage(self, result, account, path):
        gamelog.debug('jinjj--downLoadedImage-------', account, path, result)
        self.isLoading = False
        if result == gametypes.YIXIN_DOWNLOAD_SUC:
            if self.mediator:
                src = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + path
                gamelog.debug('jinjj-------download path ', src)
                self.mediator.Invoke('loadImage', GfxValue(gbk2unicode(src)))

    def onRefreshPanel(self, *args):
        self.startLoadImage()

    def sepImageUrl(self):
        if self.imagePath != '':
            if self.imagePath[:8] == 'https://':
                self.imagePath = self.imagePath[8:]
            elif self.imagePath[:7] == 'http://':
                self.imagePath = self.imagePath[8:]
            return self.imagePath.split('/')
        return []
