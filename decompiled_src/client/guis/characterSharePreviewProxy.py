#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/characterSharePreviewProxy.o
import gameglobal
import uiConst
import events
import ResMgr
from uiProxy import UIProxy
from asObject import ASObject
LEFT_UP_PICTURE = '../game/character1.jpg'
LEFT_DOWN_PICTURE = '../game/character5.jpg'
CENTER_PICTURE = '../game/character0.jpg'
RIGHT_UP_PICTURE = '../game/character3.jpg'
RIGHT_DOWN_PICTURE = '../game/character4.jpg'

class CharacterSharePreviewProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CharacterSharePreviewProxy, self).__init__(uiAdapter)
        self.widget = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_CHARACTER_SHARE_PREVIEW, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CHARACTER_SHARE_PREVIEW:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def reset(self):
        super(self.__class__, self).reset()
        self.mediator = None
        gameglobal.rds.ui.characterDetailAdjust.setUploadEnable(True)

    def clearWidget(self):
        self.clearImage()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CHARACTER_SHARE_PREVIEW)

    def show(self):
        if self.widget:
            self.refreshInfo()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CHARACTER_SHARE_PREVIEW)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleClickConfirmBtn, False, 0, True)
        self.widget.reScreenshotBtn.addEventListener(events.MOUSE_CLICK, self.handleClickReScreenshotBtn, False, 0, True)
        self.widget.leftUpPic.addEventListener(events.MOUSE_CLICK, self.onPhotoClick, False, 0, True)
        self.widget.leftDownPic.addEventListener(events.MOUSE_CLICK, self.onPhotoClick, False, 0, True)
        self.widget.rightUpPic.addEventListener(events.MOUSE_CLICK, self.onPhotoClick, False, 0, True)
        self.widget.rightDownPic.addEventListener(events.MOUSE_CLICK, self.onPhotoClick, False, 0, True)
        self.widget.centerPic.addEventListener(events.MOUSE_CLICK, self.onPhotoClick, False, 0, True)
        self.widget.previewPanel.visible = False
        self.widget.previewPanel.previewCloseBtn.addEventListener(events.MOUSE_CLICK, self.handleClickpreviewCloseBtn, False, 0, True)
        self.widget.previewPanel.perspective.htmlText = ' '

    def handleClickConfirmBtn(self, *args):
        gameglobal.rds.ui.characterDetailAdjust.uploadCharacterPhoto()
        self.hide(False)

    def handleClickReScreenshotBtn(self, *args):
        self.widget.previewPanel.visible = False
        gameglobal.rds.ui.characterDetailAdjust.reScreenshot()
        self.hide(False)

    def handleClickpreviewCloseBtn(self, *args):
        self.widget.previewPanel.visible = False

    def onPhotoClick(self, *args):
        target = ASObject(args[3][0]).currentTarget
        Path = target.data
        target.selected = not target.selected
        self.widget.previewPanel.visible = True
        self.widget.previewPanel.previewPic.fitSize = True
        self.widget.previewPanel.previewPic.loadImage('../' + Path)
        self.widget.previewPanel.perspective.htmlText = target.label

    def clearImage(self):
        if self.widget:
            self.widget.leftUpPic.photoMC.photo.clear()
            self.widget.leftDownPic.photoMC.photo.clear()
            self.widget.rightUpPic.photoMC.photo.clear()
            self.widget.rightDownPic.photoMC.photo.clear()
            self.widget.centerPic.photoMC.photo.clear()
        ResMgr.purge(LEFT_UP_PICTURE)
        ResMgr.purge(LEFT_DOWN_PICTURE)
        ResMgr.purge(CENTER_PICTURE)
        ResMgr.purge(RIGHT_UP_PICTURE)
        ResMgr.purge(RIGHT_DOWN_PICTURE)

    def refreshInfo(self):
        self.clearImage()
        self.widget.leftUpPic.photoMC.photo.fitSize = True
        self.widget.leftUpPic.photoMC.photo.loadImage('../' + LEFT_UP_PICTURE)
        self.widget.leftUpPic.data = LEFT_UP_PICTURE
        self.widget.leftDownPic.photoMC.photo.fitSize = True
        self.widget.leftDownPic.photoMC.photo.loadImage('../' + LEFT_DOWN_PICTURE)
        self.widget.leftDownPic.data = LEFT_DOWN_PICTURE
        self.widget.centerPic.photoMC.photo.fitSize = True
        self.widget.centerPic.photoMC.photo.loadImage('../' + CENTER_PICTURE)
        self.widget.centerPic.data = CENTER_PICTURE
        self.widget.rightUpPic.photoMC.photo.fitSize = True
        self.widget.rightUpPic.photoMC.photo.loadImage('../' + RIGHT_UP_PICTURE)
        self.widget.rightUpPic.data = RIGHT_UP_PICTURE
        self.widget.rightDownPic.photoMC.photo.fitSize = True
        self.widget.rightDownPic.photoMC.photo.loadImage('../' + RIGHT_DOWN_PICTURE)
        self.widget.rightDownPic.data = RIGHT_DOWN_PICTURE
