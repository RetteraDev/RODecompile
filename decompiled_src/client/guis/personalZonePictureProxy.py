#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/personalZonePictureProxy.o
import BigWorld
import gametypes
import gameglobal
import C_ui
import os
import utils
import const
import gamelog
from uiProxy import UIProxy
from guis import events
from guis import uiUtils
from guis import uiConst
from PIL import Image
from guis.asObject import ASObject
from guis.asObject import ASUtils
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
MAX_PICTURE_NUM = 3

class PersonalZonePictureProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PersonalZonePictureProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_PERSONAL_ZONE_PICTURE, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PERSONAL_ZONE_PICTURE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PERSONAL_ZONE_PICTURE)

    def reset(self):
        self.pictures = []
        self.curIndex = 0

    def show(self, pictures, idx):
        self.curIndex = idx
        self.pictures = pictures
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_PERSONAL_ZONE_PICTURE)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.nextBtn.addEventListener(events.MOUSE_CLICK, self.handleNextBtnClick, False, 0, True)
        self.widget.preBtn.addEventListener(events.MOUSE_CLICK, self.handlePreBtnClick, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        self.updatePicture()

    def handlePreBtnClick(self, *args):
        if self.curIndex > 0:
            self.curIndex = self.curIndex - 1
            self.updatePicture()

    def handleNextBtnClick(self, *args):
        if self.curIndex < len(self.pictures):
            self.curIndex = self.curIndex + 1
            self.updatePicture()

    def updatePicture(self):
        if len(self.pictures) == 1:
            self.widget.preBtn.enabled = False
            self.widget.nextBtn.enabled = False
        elif self.curIndex == len(self.pictures) - 1:
            self.widget.preBtn.enabled = True
            self.widget.nextBtn.enabled = False
        elif self.curIndex == 0:
            self.widget.preBtn.enabled = False
            self.widget.nextBtn.enabled = True
        else:
            self.widget.preBtn.enabled = True
            self.widget.nextBtn.enabled = True
        if self.curIndex < len(self.pictures):
            path = self.pictures[self.curIndex]['filePath']
            self.widget.icon.scaleType = uiConst.SCALE_TYPE_FIT_GEOMETRIC_SCALING
            self.widget.icon.imgType = uiConst.IMG_TYPE_NOS_FILE
            if utils.isDownloadImage(path):
                self.widget.icon.url = path
            else:
                self.widget.icon.loadImage(path)
