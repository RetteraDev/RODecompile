#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/marryPlanPreviewProxy.o
import BigWorld
import gametypes
import gameglobal
import uiConst
import uiUtils
import physique
import const
import clientUtils
from item import Item
from uiProxy import UIProxy
from helpers import fittingModel
from helpers import charRes
from data import consumable_item_data as CID
from data import marriage_package_data as MPD
from data import marriage_theme_data as MTD
from data import marriage_fenwei_data as MFD
from data import marriage_chedui_data as MCD
from data import item_data as ID
MARRY_PLAN_PREVIEW_TYPE_PIC = 1
MARRY_PLAN_PREVIEW_TYPE_PHOTO = 2

class MarryPlanPreviewProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MarryPlanPreviewProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MARRY_PLAN_PREVIEW, self.hide)

    def reset(self):
        self.showType = 0
        self.fittingModel1 = None
        self.fittingModel2 = None
        self.curData = None
        self.dataArray = []
        self.curIndex = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MARRY_PLAN_PREVIEW:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.resetFittingModel()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MARRY_PLAN_PREVIEW)

    def resetFittingModel(self):
        if self.fittingModel1:
            self.fittingModel1.resetHeadGen()
        if self.fittingModel2:
            self.fittingModel2.resetHeadGen()

    def show(self, dataType, dataArray, selIndex):
        self.dataType = dataType
        self.dataArray = dataArray
        self.curIndex = selIndex
        self.genPreviewData()
        if self.widget:
            self.refreshInfo()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_MARRY_PLAN_PREVIEW)

    def genPreviewData(self):
        dataId = self.dataArray[self.curIndex].data
        if self.dataType == gametypes.MARRIAGE_PACKAGE_INDEX_ZHUTI:
            self.showType = MARRY_PLAN_PREVIEW_TYPE_PIC
            self.curData = MTD.data.get(dataId, {})
        elif self.dataType == gametypes.MARRIAGE_PACKAGE_INDEX_CHEDUI:
            self.showType = MARRY_PLAN_PREVIEW_TYPE_PIC
            self.curData = MCD.data.get(dataId, {})
        elif self.dataType == gametypes.MARRIAGE_PACKAGE_INDEX_FENWEI:
            self.showType = MARRY_PLAN_PREVIEW_TYPE_PIC
            self.curData = MFD.data.get(dataId, {})
        elif self.dataType == gametypes.MARRIAGE_PACKAGE_INDEX_XL_YIFU:
            self.showType = MARRY_PLAN_PREVIEW_TYPE_PHOTO
            self.curData = dataId
        elif self.dataType == gametypes.MARRIAGE_PACKAGE_INDEX_XN_YIFU:
            self.showType = MARRY_PLAN_PREVIEW_TYPE_PHOTO
            self.curData = dataId
        elif self.dataType == gametypes.MARRIAGE_PACKAGE_INDEX_BL_YIFU:
            self.showType = MARRY_PLAN_PREVIEW_TYPE_PHOTO
            self.curData = dataId
        elif self.dataType == gametypes.MARRIAGE_PACKAGE_INDEX_BN_YIFU:
            self.showType = MARRY_PLAN_PREVIEW_TYPE_PHOTO
            self.curData = dataId

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        self.fittingModel1 = fittingModel.MarryPreviewFittingModel('MarryPreviewPhotoGen', 380, None, self)
        self.fittingModel1.initHeadGeen()
        self.fittingModel2 = fittingModel.FittingModel('MarryPlayerPreviewPhotoGen', 380, None, self)
        self.fittingModel2.initHeadGeen()

    def initState(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.photoMc.photo1.rototeFigure = self.onRotateFigure1
        self.widget.photoMc.photo1.zoomFigure = self.onZoomFigure1
        self.widget.photoMc.photo2.rototeFigure = self.onRotateFigure2
        self.widget.photoMc.photo2.zoomFigure = self.onZoomFigure2

    def refreshInfo(self):
        if self.hasBaseData():
            if self.showType == MARRY_PLAN_PREVIEW_TYPE_PIC:
                self.widget.photoMc.visible = False
                self.widget.picMc.visible = True
                icon1 = self.curData.get('icon1', '')
                icon2 = self.curData.get('icon2', '')
                self.widget.picMc.picture0.fitSize = True
                self.widget.picMc.picture0.loadImage(uiConst.MARRY_RES_DIR + icon1 + '.dds')
                self.widget.picMc.picture1.fitSize = True
                self.widget.picMc.picture1.loadImage(uiConst.MARRY_RES_DIR + icon2 + '.dds')
                self.widget.picMc.desc.htmlText = self.curData.get('desc', '')
                self.widget.rBtn.visible = False
                self.widget.lBtn.visible = False
                self.updateItemPreview()
            elif self.showType == MARRY_PLAN_PREVIEW_TYPE_PHOTO:
                self.widget.photoMc.visible = True
                self.widget.picMc.visible = False
                gfxItem = uiUtils.getGfxItemById(self.curData)
                self.widget.photoMc.itemSlot.setItemSlotData(gfxItem)
                self.widget.photoMc.itemSlot.dragable = False
                itemData = ID.data.get(self.curData, {})
                self.widget.photoMc.itemName.htmlText = itemData.get('name', '')
                self.widget.photoMc.desc.htmlText = itemData.get('funcDesc', '')
                self.updateItemPreview()
                self.widget.rBtn.visible = True
                self.widget.lBtn.visible = True

    def hasBaseData(self):
        if self.widget and self.showType:
            return True
        else:
            return False

    def updateItemPreview(self):
        _physique = None
        p = BigWorld.player()
        intimacyTgtGbId = p.friend.intimacyTgt
        marriageTgtEquipment = getattr(p, 'marriageTgtEquipment', {}).get(intimacyTgtGbId, {})
        if self.dataType == gametypes.MARRIAGE_PACKAGE_INDEX_XL_YIFU:
            if p.physique.sex != const.SEX_MALE:
                if marriageTgtEquipment:
                    _physique = marriageTgtEquipment.get('physique', None)
                else:
                    _physique = physique.Physique({'sex': const.SEX_MALE,
                     'bodyType': 3,
                     'school': 3,
                     'hair': 42})
        elif self.dataType == gametypes.MARRIAGE_PACKAGE_INDEX_XN_YIFU:
            if p.physique.sex != const.SEX_FEMALE:
                if marriageTgtEquipment:
                    _physique = marriageTgtEquipment.get('physique', None)
                else:
                    _physique = physique.Physique({'sex': const.SEX_FEMALE,
                     'bodyType': 3,
                     'school': 3,
                     'hair': 12005})
        elif self.dataType == gametypes.MARRIAGE_PACKAGE_INDEX_BL_YIFU:
            if p.physique.sex != const.SEX_MALE:
                if marriageTgtEquipment:
                    _physique = marriageTgtEquipment.get('physique', None)
                else:
                    _physique = physique.Physique({'sex': const.SEX_MALE,
                     'bodyType': 3,
                     'school': 3,
                     'hair': 42})
        elif self.dataType == gametypes.MARRIAGE_PACKAGE_INDEX_BN_YIFU:
            if p.physique.sex != const.SEX_FEMALE:
                if marriageTgtEquipment:
                    _physique = marriageTgtEquipment.get('physique', None)
                else:
                    _physique = physique.Physique({'sex': const.SEX_FEMALE,
                     'bodyType': 3,
                     'school': 3,
                     'hair': 12005})
        bonusId = 0
        if not isinstance(self.curData, dict):
            bonusId = CID.data.get(self.curData, {}).get('bonusId', 0)
        itemIds = clientUtils.genItemBonus(bonusId)
        items = [ Item(itemId) for itemId, num in itemIds ]
        if self.fittingModel1 and self.fittingModel2:
            if _physique:
                self.widget.photoMc.photo1.visible = True
                self.widget.photoMc.photo2.visible = False
                self.fittingModel1.figureInfo = {}
                self.fittingModel1.figureInfo['physique'] = _physique
                self.fittingModel1.figureInfo['avatarConfig'] = marriageTgtEquipment.get('avatarConfig', '')
                self.fittingModel1.figureInfo['aspect'] = marriageTgtEquipment.get('aspect', None)
                self.fittingModel1.addItems(items)
                self.fittingModel2.addItems([])
            else:
                self.widget.photoMc.photo1.visible = False
                self.widget.photoMc.photo2.visible = True
                self.fittingModel1.figureInfo = {}
                self.fittingModel1.figureInfo['sex'] = 2
                self.fittingModel1.figureInfo['bodyType'] = 3
                self.fittingModel1.figureInfo['hair'] = 12005
                self.fittingModel1.figureInfo['avatarConfig'] = ''
                self.fittingModel1.addItems([])
                self.fittingModel2.addItems(items)

    def onRotateFigure1(self, *arg):
        index = arg[3][0].GetNumber()
        deltaYaw = -0.02 * index
        headGen = self.fittingModel1.headGen if self.fittingModel1 else None
        if headGen:
            headGen.rotateYaw(deltaYaw)

    def onZoomFigure1(self, *arg):
        index = arg[3][0].GetNumber()
        deltaZoom = -0.02 * index
        headGen = self.fittingModel1.headGen if self.fittingModel1 else None
        if headGen:
            headGen.zoom(deltaZoom)

    def onRotateFigure2(self, *arg):
        index = arg[3][0].GetNumber()
        deltaYaw = -0.02 * index
        headGen = self.fittingModel2.headGen if self.fittingModel2 else None
        if headGen:
            headGen.rotateYaw(deltaYaw)

    def onZoomFigure2(self, *arg):
        index = arg[3][0].GetNumber()
        deltaZoom = -0.02 * index
        headGen = self.fittingModel2.headGen if self.fittingModel2 else None
        if headGen:
            headGen.zoom(deltaZoom)

    def setLoadingMcVisible(self, visble):
        if self.hasBaseData():
            self.widget.photoMc.loadingMc.visible = visble

    def _onLBtnClick(self, e):
        if self.hasBaseData():
            self.curIndex -= 1
            self.fixDataIndex()
            self.genPreviewData()
            self.refreshInfo()
            if gameglobal.rds.ui.marryPlanOrder.widget:
                gameglobal.rds.ui.marryPlanOrder.setMenuIndex(self.dataType, self.curIndex)
            if gameglobal.rds.ui.marryPlanSetting.widget:
                gameglobal.rds.ui.marryPlanSetting.setMenuIndex(self.dataType, self.curIndex)

    def _onRBtnClick(self, e):
        if self.hasBaseData():
            self.curIndex += 1
            self.fixDataIndex()
            self.genPreviewData()
            self.refreshInfo()
            if gameglobal.rds.ui.marryPlanOrder.widget:
                gameglobal.rds.ui.marryPlanOrder.setMenuIndex(self.dataType, self.curIndex)
            if gameglobal.rds.ui.marryPlanSetting.widget:
                gameglobal.rds.ui.marryPlanSetting.setMenuIndex(self.dataType, self.curIndex)

    def fixDataIndex(self):
        if self.curIndex < 0:
            self.curIndex = len(self.dataArray) - 1
        if self.curIndex >= len(self.dataArray):
            self.curIndex = 0
