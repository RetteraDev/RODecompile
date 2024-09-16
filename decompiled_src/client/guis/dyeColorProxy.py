#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/dyeColorProxy.o
import BigWorld
from Scaleform import GfxValue
import uiConst
import uiUtils
import gameglobal
import const
from uiProxy import UIProxy
from ui import gbk2unicode
from item import Item
from helpers import capturePhoto

class DyeColorProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(DyeColorProxy, self).__init__(uiAdapter)
        self.modelMap = {'chooseColor': self.onChooseColor,
         'chooseColor1': self.onChooseColor1,
         'reSetFigure': self.onReSetFigure,
         'zoomFigure': self.onZoomFigure,
         'rotateFigure': self.onRotateFigure,
         'clickConfirm': self.onClickConfirm,
         'clickClose': self.onClickClose,
         'setDyeMethod': self.onSetDyeMethod,
         'getInitData': self.onGetInitData}
        self.color = []
        self.color1 = []
        self.mediator = None
        self.headGen = None
        self.isDye = True
        self.pageScr = const.CONT_NO_PAGE
        self.posScr = const.CONT_NO_POS
        self.pageDes = const.CONT_NO_PAGE
        self.posDes = const.CONT_NO_POS
        self.dyeMethod = const.DYE_COPY
        self.res = None
        self.extraInfo = {}
        self.itemName = None
        self.itemColor = None

    def onChooseColor(self, *arg):
        r = int(arg[3][1].GetNumber())
        g = int(arg[3][2].GetNumber())
        b = int(arg[3][3].GetNumber())
        alpha = int(arg[3][4].GetNumber())
        if alpha == 0:
            alpha = 255
        self.color = [r,
         g,
         b,
         alpha]
        self.showPhoto3D()

    def onChooseColor1(self, *arg):
        r = int(arg[3][1].GetNumber())
        g = int(arg[3][2].GetNumber())
        b = int(arg[3][3].GetNumber())
        alpha = int(arg[3][4].GetNumber())
        if alpha == 0:
            alpha = 255
        self.color1 = [r,
         g,
         b,
         alpha]
        self.showPhoto3D()

    def clearWidget(self):
        self.mediator = None
        self.resetHeadGen()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_DYE_COLOR)

    def reset(self):
        self.color = []
        self.color1 = []
        self.isDye = True
        self.pageScr = const.CONT_NO_PAGE
        self.posScr = const.CONT_NO_POS
        self.pageDes = const.CONT_NO_PAGE
        self.posDes = const.CONT_NO_POS
        self.dyeMethod = const.DYE_COPY
        self.res = None
        self.extraInfo = {}
        self.itemName = None
        self.itemColor = None

    def show(self, isDye, pageScr, posScr, pageDes, posDes):
        p = BigWorld.player()
        equip = None
        if pageDes == const.INV_PAGE_EQUIP:
            equip = p.equipment.get(posDes)
        elif pageDes == const.INV_PAGE_WARDROBE:
            equip = p.wardrobeBag.getDrobeItem(posDes)
        else:
            equip = p.inv.getQuickVal(pageDes, posDes)
        if not self.uiAdapter.fittingRoom.checkItemPreview(equip, True):
            return
        else:
            self.isDye = isDye
            self.pageScr = pageScr
            self.posScr = posScr
            self.pageDes = pageDes
            self.posDes = posDes
            if self.mediator:
                self.showPhoto3D()
            else:
                self.uiAdapter.loadWidget(uiConst.WIDGET_DYE_COLOR, True)
            return

    def getDyeColor(self):
        if self.color and self.color1:
            return '%d,%d,%d,%d' % tuple(self.color) + ':' + '%d,%d,%d,%d' % tuple(self.color1)
        return ''

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_DYE_COLOR:
            self.mediator = mediator
            self.showPhoto3D()

    def onClickClose(self, *arg):
        self.hide()

    def onClickConfirm(self, *arg):
        if self.isDye:
            self.uiAdapter.inventory.dyeEquipment(self.pageDes, self.posDes, self.dyeMethod)
        else:
            self.uiAdapter.inventory.rongGuangEquipment(self.pageDes, self.posDes)
        self.hide()

    def onSetDyeMethod(self, *arg):
        self.dyeMethod = int(arg[3][0].GetNumber()) + 1
        if self.res:
            gameglobal.rds.ui.dyePlane.setDyeMethod(self.dyeMethod)
            return
        self.showPhoto3D()

    def onRotateFigure(self, *arg):
        index = arg[3][0].GetNumber()
        deltaYaw = -0.02 * index
        if self.headGen:
            self.headGen.rotateYaw(deltaYaw)

    def onZoomFigure(self, *arg):
        index = arg[3][0].GetNumber()
        deltaZoom = -0.02 * index
        if self.headGen:
            self.headGen.zoom(deltaZoom)

    def onReSetFigure(self, *arg):
        if self.headGen:
            self.headGen.resetYaw()

    def showPhoto3D(self):
        if self.mediator:
            p = BigWorld.player()
            extraInfo = {}
            if self.res:
                res = self.res
                self.setDyePanVisible(False)
                self.setDyeBtnVisible(False)
                extraInfo = self.extraInfo
            elif self.isDye:
                dyeItem = p.inv.getQuickVal(self.pageScr, self.posScr)
                if not dyeItem or not dyeItem.isDye():
                    return
                dyeType = dyeItem.getDyeType()
                if dyeType == Item.CONSUME_DYE_SUPER:
                    self.setDyePanVisible(True)
                else:
                    self.setDyePanVisible(False)
                mpr, aspect, showFashion = uiUtils.getDyeModel(self.pageScr, self.posScr, self.pageDes, self.posDes, self.dyeMethod)
                res = mpr.getPrerequisites()
            else:
                self.setDyePanVisible(False)
                mpr, aspect, showFashion = uiUtils.getRongGuangModel(self.pageScr, self.posScr, self.pageDes, self.posDes)
                res = mpr.getPrerequisites()
                extraInfo = {'aspect': aspect,
                 'showFashion': showFashion}
            self.initHeadGen()
            self.takePhoto3D(res, extraInfo)

    def setDyePanVisible(self, isVisible):
        if self.mediator:
            self.mediator.Invoke('setDyePanVisible', GfxValue(isVisible))

    def setDyeBtnVisible(self, isVisible):
        if self.mediator:
            self.mediator.Invoke('setDyeBtnVisible', GfxValue(isVisible))

    def updatePhoto3D(self):
        if self.mediator and self.isDye:
            model = self.headGen.adaptor.attachment
            uiUtils.preDyeModel(model, self.pageScr, self.posScr, self.pageDes, self.posDes)

    def takePhoto3D(self, res, extraInfo = {}):
        if self.mediator:
            if not self.headGen:
                self.headGen = capturePhoto.DyePhotoGen.getInstance('gui/taskmask.tga', 542)
            self.headGen.startCaptureEntAndRes(BigWorld.player(), res, False, extraInfo)

    def resetHeadGen(self):
        if self.headGen:
            self.headGen.endCapture()

    def initHeadGen(self):
        if not self.headGen:
            self.headGen = capturePhoto.DyePhotoGen.getInstance('gui/taskmask.tga', 542)
        self.headGen.initFlashMesh()

    def showByRes(self, res, extraInfo):
        self.res = res
        self.extraInfo = extraInfo
        if self.mediator:
            self.showPhoto3D()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_DYE_COLOR, False)

    def setItemInfo(self, itemName, color):
        self.itemName = itemName
        self.itemColor = color
        if self.mediator:
            self.mediator.Invoke('setItemInfo', (GfxValue(gbk2unicode(itemName)), GfxValue(color)))

    def onGetInitData(self, *arg):
        return uiUtils.dict2GfxDict({'itemName': self.itemName,
         'color': self.itemColor,
         'dyeMethod': self.dyeMethod - 1}, True)

    def setDyeMethod(self, value):
        self.dyeMethod = value
        if self.mediator:
            self.mediator.Invoke('setDyeMethod', GfxValue(self.dyeMethod - 1))
