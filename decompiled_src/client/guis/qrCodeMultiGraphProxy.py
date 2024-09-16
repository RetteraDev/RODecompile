#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/qrCodeMultiGraphProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import events
import urllib
import clientcom
from helpers import PNGEncode
from uiProxy import UIProxy
from asObject import ASObject
from guis.asObject import TipManager
from cdata import game_msg_def_data as GMDD
UPLOAD_TEMP_IMGS = 'upload_temp1.jpg'
APP_URL = 'http://hd.tianyu.163.com/gamePhoto/photoShare?bucket=%s&key=%s'
COLUMN_NUMBER = 4
INITIAL_PHOTO_X = 6
INITIAL_PHOTO_Y = 6
ITEM_WIDTH = 135
ITEM_HEIGHT = 135
PHOTO_CONTENT_WIDTH = 118
PHOTO_CONTENT_HEIGHT = 118

class QrCodeMultiGraphProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(QrCodeMultiGraphProxy, self).__init__(uiAdapter)
        self.widget = None
        self.infoList = []
        self.photoPathList = []
        self.selectedPathList = []
        self.onUpLoadSuccessList = []
        self.onUpLoadFailList = []
        self.photoPath = ''
        self.selectedNumber = 0
        self.photoNumber = 0
        self.totalNumber = 0
        self.uploadState = False
        self.upLoadSuccessDict = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_MULTI_GRAPH, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MULTI_GRAPH:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def reset(self):
        super(self.__class__, self).reset()
        self.mediator = None
        self.selectedNumber = 0
        self.selectedPathList = []

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MULTI_GRAPH)

    def show(self, imgPath = '', imgPathList = None):
        self.photoPathList = imgPathList
        self.photoPath = imgPath
        if self.widget:
            self.refreshInfo()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_MULTI_GRAPH)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.photoMc.photoList.itemRenderer = 'QRCodeMultiGraph_Item'
        self.widget.photoMc.photoList.itemWidth = ITEM_WIDTH
        self.widget.photoMc.photoList.itemHeight = ITEM_HEIGHT
        self.widget.photoMc.photoList.column = COLUMN_NUMBER
        self.widget.photoMc.photoList.dataArray = []
        self.widget.photoMc.photoList.lableFunction = self.itemFunction
        self.widget.chooseTxt.htmlText = gameStrings.TEXT_QRCODEMULTIGRAPHPROXY_85 % (0, self.photoNumber, self.totalNumber)
        self.widget.saveBtn.addEventListener(events.MOUSE_CLICK, self.handleClickSaveBtn, False, 0, True)
        self.widget.installBtn.addEventListener(events.MOUSE_CLICK, self.handleClickInstallBtn, False, 0, True)
        p = BigWorld.player()
        p.base.fetchAppAlbumVolLimit()

    def handleClickSaveBtn(self, *args):
        p = BigWorld.player()
        if self.selectedPathList:
            self.widget.saveBtn.enabled = False
            self.loadCount = len(self.selectedPathList)
            paths = []
            for i, path in enumerate(self.selectedPathList):
                if path not in self.onUpLoadSuccessList:
                    upLoadPath = gameglobal.rds.ui.qrCode.createUploadImg(path, i)
                    if gameglobal.rds.ui.qrCode.checkMd5(path):
                        paths.append((upLoadPath, path))
                    else:
                        self.onUpLoadSuccess(None, path)

            if paths:
                if not p.checkCameraSharePicNum(num=len(paths)):
                    return
                allFileKeys = [None] * len(paths)
            for i, (upLoadPath, path) in enumerate(paths):
                p.uploadCameraSharePic(upLoadPath, self.onUpLoadSuccess, (path,), idx=i, allFileKeys=allFileKeys)

    def singleUpLoadSuccess(self, status, path):
        if status:
            if path not in self.onUpLoadSuccessList:
                self.onUpLoadSuccessList.append(path)
                if path in self.onUpLoadFailList:
                    self.onUpLoadFailList.remove(path)
            codeUrl = gameglobal.rds.ui.qrCode.genUploadSuccessUrl(status, path)
            self.upLoadSuccessDict[path] = codeUrl
        elif path not in self.onUpLoadFailList:
            self.onUpLoadFailList.append(path)
        self.refreshInfo()

    def onUpLoadSuccess(self, status, path):
        self.loadCount -= 1
        if status:
            if path not in self.onUpLoadSuccessList:
                self.onUpLoadSuccessList.append(path)
            codeUrl = gameglobal.rds.ui.qrCode.genUploadSuccessUrl(status, path)
            self.upLoadSuccessDict[path] = codeUrl
        elif path not in self.onUpLoadFailList:
            self.onUpLoadFailList.append(path)
        if not self.loadCount:
            self.uploadState = False
            self.selectedPathList = []
            self.refreshInfo()
            if self.widget:
                self.widget.saveBtn.enabled = True
        else:
            self.uploadState = True

    def handleClickInstallBtn(self, *args):
        gameglobal.rds.ui.qrCodeInstallAPP.show()

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemTip = ''
        if itemData.uploadSuccess or itemData.uploadFail:
            if itemData.uploadSuccess == True:
                itemMc.gotoAndStop('success')
                itemTip = gameStrings.TEXT_QRCODEMULTIGRAPHPROXY_163
                TipManager.addTip(itemMc.selected, itemTip)
            if itemData.uploadFail == True:
                itemMc.gotoAndStop('fail')
                itemTip = gameStrings.TEXT_QRCODEMULTIGRAPHPROXY_169
                TipManager.addTip(itemMc.unselected, itemTip)
        photo = itemData.path
        itemMc.photoMc.fixedSize = True
        itemMc.photoMc.data = photo
        itemMc.photoMc.photo.loadImage(photo)
        itemMc.photoMc.photo.x = INITIAL_PHOTO_X
        itemMc.photoMc.photo.y = INITIAL_PHOTO_Y
        itemMc.photoMc.photo.addEventListener(events.EVENT_COMPLETE, self.handleComplete)
        itemMc.photoMc.addEventListener(events.MOUSE_CLICK, self.onPhotoClick, False, 0, True)
        itemMc.photoCheckBox.removeEventListener(events.EVENT_SELECT, self.handleSelect)
        itemMc.photoCheckBox.selected = False
        itemMc.photoMc.selected = False
        itemMc.photoCheckBox.addEventListener(events.EVENT_SELECT, self.handleSelect, False, 0, True)

    def handleComplete(self, *args):
        target = ASObject(args[3][0]).currentTarget
        content = target.getContent()
        width = content.width
        height = content.height
        x = target.x
        y = target.y
        if content.width >= content.height:
            content.width = PHOTO_CONTENT_WIDTH
            scaleX = width / content.width
            content.height = content.height / scaleX
            target.y = y + PHOTO_CONTENT_WIDTH / 2 - content.height / 2
        else:
            content.height = PHOTO_CONTENT_HEIGHT
            scaleY = height / content.height
            content.width = content.width / scaleY
            target.x = x + PHOTO_CONTENT_HEIGHT / 2 - content.width / 2

    def onPhotoClick(self, *args):
        target = ASObject(args[3][0]).currentTarget
        Path = target.data[3:]
        target.selected = not target.selected
        if Path in self.onUpLoadSuccessList:
            gameglobal.rds.ui.qrCode.showSucessPhoto(self.upLoadSuccessDict, imgPath=Path, content=gameStrings.TEXT_QRCODEMULTIGRAPHPROXY_214)
        elif Path in self.onUpLoadFailList:
            gameglobal.rds.ui.qrCode.show(imgPath=Path, content=gameStrings.TEXT_QRCODEMULTIGRAPHPROXY_218)
        else:
            gameglobal.rds.ui.qrCode.show(imgPath=Path, content=gameStrings.TEXT_QRCODEMULTIGRAPHPROXY_218)

    def handleSelect(self, *args):
        target = ASObject(args[3][0]).currentTarget
        path = target.parent.photoMc.data[3:]
        if target.selected == True:
            self.selectedNumber += 1
            self.selectedPathList.append(path)
            target.parent.photoMc.selected = True
        elif target.selected == False:
            self.selectedNumber -= 1
            target.parent.photoMc.selected = False
            self.selectedPathList.remove(path)
        if self.selectedNumber > self.photoNumber:
            target.selected = False
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.CAN_NOT_CHOOSE_MORE_PHOTO, ())
        if self.uploadState == True:
            target.selected = False
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.CAN_NOT_CHOOSE_WHEN_UPLOAD, ())
        self.refreshChooseTxt()

    def refreshInfo(self):
        self.photoNumber = 9
        self.infoList = []
        if not gameglobal.rds.configData.get('enableNewCamera', False):
            gameglobal.rds.ui.camera.refreshNewTakenPhotoList(self.photoPathList)
        else:
            gameglobal.rds.ui.cameraV2.refreshNewTakenPhotoList(self.photoPathList)
        self.photoPathList = filter(clientcom.isFileExist, self.photoPathList)
        for i in xrange(len(self.photoPathList)):
            photoInfo = {}
            photoInfo['path'] = '../' + self.photoPathList[i]
            photoInfo['uploadSuccess'] = False
            photoInfo['uploadFail'] = False
            if self.photoPathList[i] in self.onUpLoadSuccessList:
                photoInfo['uploadSuccess'] = True
            if self.photoPathList[i] in self.onUpLoadFailList:
                photoInfo['uploadFail'] = True
            self.infoList.append(photoInfo)

        if not self.widget:
            return
        self.widget.photoMc.photoList.dataArray = self.infoList[::-1]
        self.selectedNumber = 0
        self.totalNumber = len(self.photoPathList)
        self.refreshChooseTxt()

    def refreshChooseTxt(self):
        self.widget.chooseTxt.htmlText = gameStrings.TEXT_QRCODEMULTIGRAPHPROXY_85 % (self.selectedNumber, self.photoNumber, self.totalNumber)
