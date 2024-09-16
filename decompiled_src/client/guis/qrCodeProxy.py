#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/qrCodeProxy.o
from gamestrings import gameStrings
from PIL import Image
import BigWorld
from Scaleform import GfxValue
import urllib
import gameglobal
import uiUtils
import clientcom
from guis import uiConst
from guis.ui import gbk2unicode
from guis.uiProxy import UIProxy
from helpers import PNGEncode
from data import sys_config_data as SCD
UPLOAD_TEMP_IMG = 'upload_temp'
APP_URL = 'http://hd.tianyu.163.com/gamePhoto/photoShare?bucket=%s&key=%s'

class QrCodeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(QrCodeProxy, self).__init__(uiAdapter)
        self.modelMap = {'uploadImage': self.onUploadImage,
         'shareImage': self.onShareImage,
         'downloadApp': self.onDownloadApp,
         'getPhotoState': self.onGetPhotoState}
        self.reset()
        self.upLoadDict = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_QRCODE_PANEL, self.clearWidget)

    def reset(self):
        self.mediator = None
        self.title = None
        self.content = None
        self.qrContent = False
        self.previewChartPath = ''
        self.originalPath = ''
        self.photoState = ''

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_QRCODE_PANEL:
            self.mediator = mediator
            self.refreshContent()

    def refreshContent(self):
        if self.mediator:
            if self.photoState == 'NotUpload':
                self.qrContent = False
                self.setUploadBtnVisible(True)
            elif self.photoState == 'Success':
                self.setUploadBtnVisible(False)
            elif self.photoState == 'AppScanShare':
                self.setUploadBtnVisible(False)
                self.setQRCodeVisible(False)
            imgPath = ''
            if self.originalPath:
                imgPath = '../' + self.originalPath
            self.mediator.Invoke('setContent', (GfxValue(gbk2unicode(self.title)), GfxValue(gbk2unicode(self.content)), GfxValue(gbk2unicode(imgPath))))
        if self.photoState != 'AppScanShare':
            self.refreshLoading()

    def refreshLoading(self):
        if self.mediator:
            if not self.qrContent:
                self.mediator.Invoke('setIsLoading', GfxValue(True))
            else:
                self.mediator.Invoke('setIsLoading', GfxValue(False))
                self.mediator.Invoke('setQRCode', GfxValue(uiUtils.getQRCodeBuff(self.qrContent)))

    def setContent(self, content):
        self.content = content
        self.refreshContent()

    def setQRCode(self, qrContent):
        self.qrContent = qrContent
        self.refreshLoading()

    def createUploadImg(self, imgPath, loadCount = 0):
        try:
            img = Image.open(imgPath)
            index = imgPath.rfind('/')
            if index != -1:
                previewChartPath = '%s%s%d.jpg' % (imgPath[:index + 1], UPLOAD_TEMP_IMG, loadCount)
            else:
                previewChartPath = '%s%d.jpg' % (UPLOAD_TEMP_IMG, loadCount)
            w, h = img.size
            maxL = w if w > h else h
            if maxL > gameglobal.MAX_PHOTO_SIZE:
                w = w * gameglobal.MAX_PHOTO_SIZE / maxL
                h = h * gameglobal.MAX_PHOTO_SIZE / maxL
                newImg = img.resize((w, h), Image.ANTIALIAS)
                newImg.save(previewChartPath)
            else:
                img.save(previewChartPath)
        except:
            previewChartPath = imgPath

        return previewChartPath

    def show(self, title = gameStrings.TEXT_QRCODEPROXY_109, content = gameStrings.TEXT_QRCODEPROXY_109_1, imgPath = None):
        self.title = title
        self.content = content
        self.photoState = 'NotUpload'
        if self.upLoadDict.has_key(imgPath):
            self.qrContent = self.upLoadDict[imgPath]
        self.originalPath = imgPath
        self.previewChartPath = self.createUploadImg(imgPath)
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_QRCODE_PANEL)
        else:
            self.refreshContent()
            self.setUploadBtnVisible(True)

    def showAppScanSharePhoto(self, imgPath):
        self.photoState = 'AppScanShare'
        self.originalPath = imgPath
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_QRCODE_PANEL)

    def showSucessPhoto(self, upLoadSuccessDict, imgPath = None, title = gameStrings.TEXT_QRCODEPROXY_109, content = gameStrings.TEXT_QRCODEPROXY_109_1):
        self.title = title
        self.content = content
        self.photoState = 'Success'
        if upLoadSuccessDict.has_key(imgPath):
            self.qrContent = upLoadSuccessDict[imgPath]
        self.originalPath = imgPath
        self.previewChartPath = self.createUploadImg(imgPath)
        self.setQRCode(self.qrContent)
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_QRCODE_PANEL)
        else:
            self.onUploadImage()
            self.refreshContent()

    def clearWidget(self):
        self.reset()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_QRCODE_PANEL)

    def onUploadImage(self, *arg):
        p = BigWorld.player()
        if self.qrContent:
            self.refreshLoading()
            self.setQRCodeVisible(True)
            return
        else:
            if self.previewChartPath:
                if not p.checkCameraSharePicNum():
                    return
                if self.checkMd5(self.originalPath):
                    p.uploadCameraSharePic(self.previewChartPath, self.onUpLoadSuccess, (self.originalPath,))
                    self.refreshLoading()
                    self.setQRCodeVisible(True)
                else:
                    self.onUpLoadSuccess(None, self.originalPath)
            return

    def onShareImage(self, *arg):
        if self.originalPath:
            shareInfo = gameglobal.rds.ui.qrCodeAppScanShare.createShareInfoInstance(dailyShare=True)
            shareInfo.imgPath = self.originalPath
            gameglobal.rds.ui.qrCodeAppScanShare.show(shareInfo)

    def onDownloadApp(self, *arg):
        clientcom.openFeedbackUrl(SCD.data.get('TIANYU_APP_URL', 'http://tianyu.163.com/download/app/'))

    def uploadFailed(self):
        self.setContent(gameStrings.TEXT_QRCODEPROXY_176)

    def checkMd5(self, picPath):
        pngEncode = PNGEncode.PNGEncode()
        pngEncode.open(picPath)
        hasMd5 = pngEncode.hasMd5()
        pngEncode.save()
        return hasMd5

    def onUpLoadSuccess(self, status, path):
        gameglobal.rds.ui.qrCodeMultiGraph.singleUpLoadSuccess(status, path)
        if status:
            codeUrl = self.genUploadSuccessUrl(status, path)
            self.setQRCode(codeUrl)
            self.upLoadDict[path] = codeUrl
            self.photoState = 'Success'
            self.setUploadBtnVisible(False)
        else:
            self.uploadFailed()

    def setQRCodeVisible(self, visible):
        if self.mediator:
            self.mediator.Invoke('setQRCodeVisible', GfxValue(visible))

    def setUploadBtnVisible(self, visible):
        if self.mediator:
            self.mediator.Invoke('setUploadBtnVisible', GfxValue(visible))

    def onGetPhotoState(self, *args):
        return GfxValue(self.photoState)

    def genUploadSuccessUrl(self, status, path):
        if gameglobal.rds.configData.get('enableQRCode', False):
            shareInfo = gameglobal.rds.ui.qrCodeAppScanShare.createShareInfoInstance(dailyShare=True)
            shareInfo.imgPath = path
            shareInfo.status = status
            codeUrl = gameglobal.rds.ui.qrCodeAppScanShare.getQRCodeUrl(shareInfo)
        elif gameglobal.rds.configData.get('enableCameraNewURL', False):
            bucket = gameglobal.rds.configSect.readString('nos/account')
            codeUrl = APP_URL % (bucket, urllib.quote(status))
        else:
            host, url = clientcom.genCameraShareUrl(status)
            codeUrl = 'http://' + host + url
        return codeUrl
