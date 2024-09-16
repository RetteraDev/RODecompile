#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/qrCodeAppScanShareProxy.o
from PIL import Image
import time
import os
import re
import BigWorld
import urllib
import gameglobal
import uiUtils
import uiConst
import utils
from gameStrings import gameStrings
from uiProxy import UIProxy
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
UPLOAD_TEMP_IMG = 'upload_app_temp'
APP_URL = 'hd.tianyu.163.com/appScanCode/photoShare?bucket=%s&key=%s&qrShareId=%d&gbid=%d&gsid=%d'
PIC_MAX_WIDTH = 744
DAILY_SHARE_ID = 0

class QrCodeAppScanShareProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(QrCodeAppScanShareProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.lastUploadedInfo = None
        self.lastShowMsgBoxId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_QRCODE_APPSCAN, self.hide)

    def reset(self):
        self.qrContent = None
        self.lastPhotoRequest = None
        self.lastUploadRequest = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_QRCODE_APPSCAN:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_QRCODE_APPSCAN)

    def show(self, shareInfo):
        if isinstance(shareInfo, QrShareInfo) and shareInfo.qrCodeId != -1 and not self.widget and gameglobal.rds.configData.get('enableQRCode', False):
            if shareInfo.imgPath:
                if self.lastUploadedInfo and shareInfo.imgPath == self.lastUploadedInfo.imgPath:
                    self.qrContent = self.lastUploadedInfo.qrContent
                    self.uiAdapter.loadWidget(uiConst.WIDGET_QRCODE_APPSCAN, isModal=True)
                    return
                if gameglobal.rds.ui.qrCode.checkMd5(shareInfo.imgPath):
                    self.lastUploadRequest = shareInfo
                    upLoadPath = self.createUploadTmpImg(shareInfo)
                    BigWorld.player().uploadQRCodeSharePic(upLoadPath, self.onUploadFinished)
                    self.uiAdapter.loadWidget(uiConst.WIDGET_QRCODE_APPSCAN, isModal=True)
                else:
                    self.shareFeedBack(False)
            else:
                self.takeScreenShot(shareInfo)

    def createUploadTmpImg(self, shareInfo):
        if not isinstance(shareInfo, QrShareInfo) or not shareInfo.imgPath:
            return
        try:
            imgPath = shareInfo.imgPath
            img = Image.open(imgPath)
            index = imgPath.rfind('/')
            if index != -1:
                upLoadPath = '%s%s.jpg' % (imgPath[:index + 1], UPLOAD_TEMP_IMG)
                w, h = img.size
                if shareInfo.qrCodeId == 0 and w > PIC_MAX_WIDTH:
                    h = h * PIC_MAX_WIDTH / w
                    newImg = img.resize((PIC_MAX_WIDTH, h), Image.ANTIALIAS)
                    newImg.save(upLoadPath)
                else:
                    img.save(upLoadPath)
        except:
            upLoadPath = imgPath

        return upLoadPath

    def onUploadFinished(self, status):
        if status and self.lastUploadRequest:
            self.lastUploadRequest.status = status
            codeUrl = self.getQRCodeUrl(self.lastUploadRequest)
            self.qrContent = self.lastUploadRequest.qrContent = uiUtils.getQRCodeBuff(codeUrl)
            self.refreshInfo()
            self.lastUploadedInfo = self.lastUploadRequest

    def getQRCodeUrl(self, shareInfo):
        if isinstance(shareInfo, QrShareInfo):
            bucket = gameglobal.rds.configSect.readString('nos/account')
            codeUrl = APP_URL % (bucket,
             urllib.quote(shareInfo.status),
             shareInfo.qrCodeId,
             BigWorld.player().gbId,
             utils.getHostId())
            return codeUrl

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.mainMC.closeBtn

    def refreshInfo(self):
        if not self.widget:
            return
        if self.qrContent:
            self.widget.mainMC.pic.fitSize = True
            self.widget.mainMC.pic.loadImageByBase64(self.qrContent)
            self.widget.mainMC.descText.text = gameStrings.QRCODE_APP_SCAN_WINDOW_LOADED

    def shareFeedBack(self, success):
        if not self.widget:
            return
        if success:
            msgId = gameglobal.rds.ui.messageBox.showMsgBox(SCD.data.get('qrCodeAppShareSuccess', ''), callback=self.shareFeedBackCallBack)
        else:
            msgId = BigWorld.player().showGameMsg(GMDD.data.CAMERA_PIC_UPLOAD_FAIL_BY_TYPE, ())
        if self.lastShowMsgBoxId != 0:
            gameglobal.rds.ui.messageBox.dismiss(self.lastShowMsgBoxId, needDissMissCallBack=False)
        self.lastShowMsgBoxId = msgId

    def shareFeedBackCallBack(self):
        self.lastShowMsgBoxId = 0
        self.hide()

    def onScreenShotFinished(self, imgPath):
        if self.lastPhotoRequest:
            pattern = re.compile(self.lastPhotoRequest.imgPath)
            match = pattern.search(os.path.basename(imgPath))
            if match:
                self.lastPhotoRequest.imgPath = imgPath
                self.show(self.lastPhotoRequest)

    def takeScreenShot(self, shareInfo):
        if isinstance(shareInfo, QrShareInfo):
            self.uiAdapter.hideWaterMark()
            self.lastPhotoRequest = shareInfo
            self.lastPhotoRequest.imgPath = time.strftime('%Y%m%d-%H%M%S', time.localtime())
            uiRange = self.lastPhotoRequest.uiRange
            if not uiRange:
                self.uiAdapter.screenShot(self.lastPhotoRequest.imgPath)
            else:
                if not isinstance(uiRange, list):
                    uiRange = list(uiRange)
                for i, item in enumerate(uiRange):
                    uiRange[i] = [ int(round(ele)) for ele in item ]

                self.uiAdapter.screenShot(self.lastPhotoRequest.imgPath, uiRange[0], uiRange[1])

    def setLogoWaterMarkByRange(self, uiRange, posType):
        if posType == uiConst.WATERMARK_BOTTOM_LEFT:
            pos = (uiRange[0][0], uiRange[1][1])
        elif posType == uiConst.WATERMARK_BOTTOM_RIGHT:
            pos = uiRange[1]
        elif posType == uiConst.WATERMARK_TOP_LEFT:
            pos = uiRange[0]
        elif posType == uiConst.WATERMARK_TOP_RIGHT:
            pos = (uiRange[1][0], uiRange[0][1])
        self.uiAdapter.setWaterMarkPos(pos, posType)

    def createShareInfoInstance(self, dailyShare = False):
        info = QrShareInfo()
        if dailyShare:
            info.qrCodeId = DAILY_SHARE_ID
        return info


class QrShareInfo(object):

    def __init__(self):
        super(QrShareInfo, self).__init__()
        self.qrCodeId = -1
        self.imgPath = ''
        self.uiRange = []
        self.status = None
        self.qrContent = None
