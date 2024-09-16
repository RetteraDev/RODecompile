#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/evaluatePlayProxy.o
import BigWorld
import gameglobal
import gamelog
import clientUtils
import gametypes
import clientcom
import utils
from guis.ui import gbk2unicode
from item import Item
import events
from guis.uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils
from asObject import ASUtils
from guis.asObject import TipManager
from gameStrings import gameStrings
from guis.asObject import ASObject
from callbackHelper import Functor
from helpers import fittingModel
from data import gui_bao_ge_data as GBGD
from data import evaluate_name_data as END
from data import play_recomm_item_data as PRID
from data import evaluate_set_data as ESD
from cdata import evaluate_set_appearance_reverse_data as ESARD
from cdata import game_msg_def_data as GMDD
EVA_RATE_NUM = 4
STAR_NUM = 5
IMPAGE_PATH = 'comment/%s.dds'
ORIGIN_FACTOR = 1
DOUBLE_FACTOR = 2

class EvaluatePlayProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EvaluatePlayProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_EVALUATEPLAY, Functor(self.hide, True, False))

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_EVALUATEPLAY:
            self.widget = widget
            self.initUI()

    def show(self, showId, showType):
        if not showId or not showType:
            return
        if self.widget:
            return
        self.showId = showId
        self.showType = showType
        self.checkType = uiConst.EVALUATE_CHECKTYPE_ITEM if showType == uiConst.EVALUATE_SHOWTYPE_ITEM else self.getData().get('checkType', 0)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EVALUATEPLAY)

    def clearWidget(self):
        self.widget = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EVALUATEPLAY)
        if self.fittingModel:
            self.fittingModel.resetHeadGen()

    def reset(self):
        self.showId = None
        self.curStarSelected = [0,
         0,
         0,
         0]
        self.showType = None
        self.checkType = None
        self.useTime = 0
        self.fittingModel = None

    def initUI(self):
        if self.hasBaseData():
            self.initData()
            self.initState()

    def initData(self):
        self.fittingModel = fittingModel.FittingModel('EvaluatePlayPhotoGen', 470, None, self)
        self.fittingModel.initHeadGeen()
        self.fittingModel.restorePhoto3D()

    def initState(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        eData = self.getData()
        cantClose = eData.get(self.showId, {}).get('cantClose', 0)
        self.widget.closeBtn.visible = not bool(cantClose)
        self.widget.evaBtn.addEventListener(events.BUTTON_CLICK, self.handleClickEvaBtn, False, 0, True)
        self.widget.declaration.addEventListener(events.EVENT_CHANGE, self.handleChangeDelaration, False, 0, True)
        rateType = eData.get(self.showId, {}).get('rateType', 0)
        for x in xrange(0, EVA_RATE_NUM):
            evaStars = getattr(self.widget, 'evaStars' + str(x), None)
            evaTxt = getattr(self.widget, 'evaTxt' + str(x), None)
            evaStars.num = x
            for y in xrange(0, STAR_NUM):
                star = getattr(evaStars, 'star' + str(y), None)
                star.gotoAndStop('empty')
                star.addEventListener(events.MOUSE_CLICK, self.handleClickStarBtn, False, 0, True)
                star.num = y + 1

            if evaTxt:
                rateName = END.data.get(rateType, {}).get('rateName' + str(x + 1), '')
                rateNameTips = END.data.get(rateType, {}).get('rateNameTips' + str(x + 1), '')
                evaTxt.text = rateName
                TipManager.addTip(evaTxt, rateNameTips)

        timeDesc = eData.get(self.showId, {}).get('timeDesc', '')
        self.widget.deadLineTxt.text = timeDesc
        if timeDesc:
            self.widget.noticeIcon.visible = True
        else:
            self.widget.noticeIcon.visible = False
        self.widget.noticeIcon.x = self.widget.deadLineTxt.x + self.widget.deadLineTxt.width - self.widget.deadLineTxt.textWidth - 25
        txtLimit = eData.get(self.showId, {}).get('txtLimit', 0)
        self.widget.declaration.maxChars = txtLimit
        self.widget.strNumTxt.text = gameStrings.EVALUATE_WORDNUM_DESC % (0, txtLimit)
        if not txtLimit:
            self.widget.declaration.visible = False
            self.widget.strNumTxt.visible = False
            self.widget.declarationTitle.visible = False
        else:
            self.widget.declaration.visible = True
            self.widget.strNumTxt.visible = True
            self.widget.declarationTitle.visible = True
        self.widget.preview.rototeFigure = self.onRotateFigure
        self.widget.preview.zoomFigure = self.onZoomFigure
        if self.showType == uiConst.EVALUATE_SHOWTYPE_PALY:
            recommId = eData.get(self.showId, {}).get('recommendId', 0)
            self.widget.titleName.text = PRID.data.get(recommId, {}).get('name', '')
            self.widget.preview.visible = False
            self.widget.picture.visible = True
            pic = eData.get(self.showId, {}).get('picture', None)
            self.widget.picture.fitSize = True
            self.widget.picture.loadImage(IMPAGE_PATH % pic)
            rewardIcon = eData.get(self.showId, {}).get('rewardIcon', None)
            rewardParam = eData.get(self.showId, {}).get('rewardParam', '0')
            self.setRewardSlot(rewardIcon, rewardParam)
        elif self.showType == uiConst.EVALUATE_SHOWTYPE_ITEM:
            self.widget.titleName.text = eData.get(self.showId, {}).get('name', '')
            self.widget.preview.visible = True
            self.widget.picture.visible = False
            self.updateItemPreview()
            BigWorld.callback(1, self.updateItemPreview)
            mainID = eData.get(self.showId, {}).get('ID', 0)
            rewardIcon = ESD.data.get(mainID, {}).get('rewardIcon', None)
            rewardParam = ESD.data.get(mainID, {}).get('rewardParam', '0')
            erData = ESARD.data.get(self.showId, {})
            eID = erData.get('ID', 0)
            p = BigWorld.player()
            aeInfo = p.evaluateInfo.get('appearanceItemCollectEvaluateInfo', {})
            eState = aeInfo.get(eID, 0)
            acSet = getattr(p, 'appearanceItemCollectSet', set([]))
            doubleAmount = False
            if self.isOwnedItem(self.showId) and eState != gametypes.EVALUATE_APPLY_BEFORE:
                doubleAmount = True
            self.setRewardSlot(rewardIcon, rewardParam, doubleAmount)
        self.useTime = utils.getNow()
        self.refreshInfo()

    def isOwnedItem(self, itemId):
        owned = False
        configData = GBGD.data
        associateIds = list(configData.get(itemId, {}).get('associateIds', []))
        associateIds.append(itemId)
        for associateId in associateIds:
            if associateId in getattr(BigWorld.player(), 'appearanceItemCollectSet', set([])):
                owned = True

        return owned

    def refreshInfo(self):
        if self.hasBaseData():
            pass

    def setRewardSlot(self, rewardIcon, rewardParam, doubleAmount = False):
        if rewardIcon:
            fixFactor = DOUBLE_FACTOR if doubleAmount else ORIGIN_FACTOR
            amount = self.getFormulaValue(rewardParam) * fixFactor
            gfxItem = uiUtils.getGfxItemById(rewardIcon, amount)
            self.widget.rewardSlot.setItemSlotData(gfxItem)
            self.widget.rewardTitleIcon.visible = True
            self.widget.rewardTitleTxt.visible = True
            self.widget.rewardSlot.visible = True
        else:
            self.widget.rewardTitleIcon.visible = False
            self.widget.rewardTitleTxt.visible = False
            self.widget.rewardSlot.visible = False

    def getFormulaValue(self, expformula):
        p = BigWorld.player()
        expformula = expformula.replace('lv', str(p.lv))
        val = 0
        try:
            val = eval(expformula)
        except:
            val = 0

        return val

    def hasBaseData(self):
        if self.widget and self.showId and self.showType:
            return True
        else:
            return False

    def handleClickEvaBtn(self, *arg):
        t = ASObject(arg[3][0])
        p = BigWorld.player()
        _str = self.widget.declaration.text
        if 0 in self.curStarSelected:
            p.showGameMsg(GMDD.data.EVALUATE_NEED_CONTENT, ())
            return
        else:
            evaId = None
            if self.showType == uiConst.EVALUATE_SHOWTYPE_PALY:
                evaId = self.showId
            elif self.showType == uiConst.EVALUATE_SHOWTYPE_ITEM:
                evaId = ESARD.data.get(self.showId, {}).get('ID', None)
            eStar1, eStar2, eStar3, eStar4 = self.curStarSelected
            p.base.applyEvaluate(evaId, eStar1, eStar2, eStar3, eStar4, _str, utils.getNow() - self.useTime)
            self.hide(forceClose=True)
            return

    def refreshStarState(self, rate):
        evaStars = getattr(self.widget, 'evaStars' + str(rate), None)
        if evaStars:
            for x in xrange(0, STAR_NUM):
                star = getattr(evaStars, 'star' + str(x), None)
                star.gotoAndStop('empty')

            for x in xrange(0, self.curStarSelected[rate]):
                star = getattr(evaStars, 'star' + str(x), None)
                star.gotoAndStop('full')

    def handleClickStarBtn(self, *arg):
        e = ASObject(arg[3][0])
        num = int(e.currentTarget.num)
        rate = int(e.currentTarget.parent.num)
        self.curStarSelected[rate] = num
        self.refreshStarState(rate)

    def handleChangeDelaration(self, *arg):
        _str = self.widget.declaration.text
        _str = _str.decode(utils.defaultEncoding())
        num = len(_str)
        eData = self.getData()
        txtLimit = eData.get(self.showId, {}).get('txtLimit', 0)
        self.widget.strNumTxt.text = gameStrings.EVALUATE_WORDNUM_DESC % (num, txtLimit)

    def setLoadingMcVisible(self, bVisible):
        if self.widget:
            self.widget.preview.loadingMc.visible = bVisible

    def getData(self):
        if self.showType == uiConst.EVALUATE_SHOWTYPE_PALY:
            return ESD.data
        if self.showType == uiConst.EVALUATE_SHOWTYPE_ITEM:
            return ESARD.data

    def hide(self, destroy = True, forceClose = True):
        if self.hasBaseData():
            eData = self.getData()
            cantClose = eData.get(self.showId, {}).get('cantClose', 0)
            if cantClose and not forceClose:
                return
        super(EvaluatePlayProxy, self).hide(destroy)

    def updateItemPreview(self):
        self.setLoadingMcVisible(False)
        item = Item(self.showId)
        if self.fittingModel:
            self.fittingModel.addItem(item)

    def onRotateFigure(self, *arg):
        index = arg[3][0].GetNumber()
        deltaYaw = -0.02 * index
        headGen = self.fittingModel.headGen if self.fittingModel else None
        if headGen:
            headGen.rotateYaw(deltaYaw)

    def onZoomFigure(self, *arg):
        index = arg[3][0].GetNumber()
        deltaZoom = -0.02 * index
        headGen = self.fittingModel.headGen if self.fittingModel else None
        if headGen:
            headGen.zoom(deltaZoom)
