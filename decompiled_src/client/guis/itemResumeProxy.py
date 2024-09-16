#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/itemResumeProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import math
import gameglobal
import const
import utils
from guis import uiConst
from guis.ui import gbk2unicode
from guis.uiProxy import UIProxy
from guis import uiUtils
from cdata import game_msg_def_data as GMDD
from data import item_data as ID

class ItemResumeProxy(UIProxy):
    RESUME_PAGE_START = 0
    RESUME_PAGE_ENOUGH = 1
    RESUME_PAGE_NOT_ENOUGH = 2
    RESUME_MONTH = 0
    RESUME_FOREVER = 1

    def __init__(self, uiAdapter):
        super(ItemResumeProxy, self).__init__(uiAdapter)
        self.modelMap = {'refreshPageOne': self.onRefreshPageOne,
         'closeWidget': self.dismiss,
         'confirm': self.onConfirm,
         'refreshPageTwo': self.onRefreshPageTwo,
         'buyCard': self.onBuyCard}
        self.mediator = None
        self.isShow = False
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ITEM_RESUME, self.clearWidget)

    def reset(self):
        self.nowType = 0
        self.resumeItem = None
        self.page = const.CONT_NO_PAGE
        self.pos = const.CONT_NO_POS
        self.bagType = const.RES_KIND_INV

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator
        if BigWorld.player():
            BigWorld.player().registerEvent(const.EVENT_UPDATE_COIN, self.onCoinChange)
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def onCoinChange(self, unbindCoin, bindCoin, freeCoin):
        if self.mediator:
            self.setNowView(self.nowType, True)

    def onRefreshPageOne(self, *args):
        self.setItemIcon()
        if self.resumeItem:
            if self.resumeItem.isExpireTTLEC() and not self.resumeItem.isExpireTTL():
                self.mediator.Invoke('setHitVisible', GfxValue(True))
            else:
                self.mediator.Invoke('setHitVisible', GfxValue(False))
        labelConfirm = uiUtils.getTextFromGMD(GMDD.data.COFIRM_TEXT, gameStrings.TEXT_DOUBLECHECKWITHINPUTPROXY_87)
        labelCancel = uiUtils.getTextFromGMD(GMDD.data.CANCEL_TEXT, gameStrings.TEXT_ITEMRESUMEPROXY_73)
        self.setButtonState(0, labelConfirm, labelCancel)
        label1 = self.getCostText(0)
        label2 = self.getCostText(1)
        self.mediator.Invoke('setShowLabel', (GfxValue(gbk2unicode(label1)), GfxValue(gbk2unicode(label2))))

    def setButtonState(self, type, labelConfirm, labelCancel, stateConfirm = True, stateCancel = True):
        info = {}
        info['confirmLabel'] = labelConfirm
        info['confirmData'] = type
        info['confirmState'] = stateConfirm
        info['cancelLabel'] = labelCancel
        info['cancelData'] = type
        info['cancelState'] = stateCancel
        self.mediator.Invoke('setButtonState', uiUtils.dict2GfxDict(info, True))

    def getSelectTypeEnough(self, type):
        return BigWorld.player().getCoinAll() >= self.getTypeCost(type)

    def getTypeCost(self, type):
        if type == self.RESUME_MONTH:
            searchName = 'mallRenewal30Days'
        else:
            searchName = 'mallRenewalForever'
        cost = ID.data.get(self.resumeItem.id, {}).get(searchName, 0)
        if type == self.RESUME_FOREVER:
            cost = math.ceil((const.ITEM_OWNERSHIP_MAX - getattr(self.resumeItem, 'ownershipPercent', 0)) * 1.0 / 100 * cost)
        return cost

    def getCostText(self, type):
        cost = self.getTypeCost(type)
        label = uiUtils.getTextFromGMD(GMDD.data.NEED_COST_TEXT, gameStrings.TEXT_ITEMRESUMEPROXY_110) % cost
        return label

    def setItemIcon(self):
        if self.resumeItem:
            itemData = uiUtils.getGfxItem(self.resumeItem)
            itemData['srcType'] = 'itemResume'
            itemData['itemId'] = self.resumeItem.id
            self.mediator.Invoke('setNowItem', uiUtils.dict2GfxDict(itemData, True))

    def onRefreshPageTwo(self, *args):
        self.setItemIcon()
        type = int(args[3][0].GetNumber())
        self.setNowView(type)

    def setNowView(self, type, needRefresh = False):
        self.nowType = type
        if self.getSelectTypeEnough(type) and needRefresh == False:
            labelConfirm = uiUtils.getTextFromGMD(GMDD.data.COFIRM_TEXT, gameStrings.TEXT_DOUBLECHECKWITHINPUTPROXY_87)
            labelCancel = uiUtils.getTextFromGMD(GMDD.data.CANCEL_TEXT, gameStrings.TEXT_ITEMRESUMEPROXY_73)
            self.setButtonState(1, labelConfirm, labelCancel)
        else:
            labelConfirm = uiUtils.getTextFromGMD(GMDD.data.BUY_CARD, gameStrings.TEXT_ITEMRESUMEPROXY_134)
            labelCancel = uiUtils.getTextFromGMD(GMDD.data.PAY_CONFIRM, gameStrings.TEXT_ITEMRESUMEPROXY_135)
            if needRefresh == True and self.getSelectTypeEnough(type):
                self.setButtonState(self.RESUME_PAGE_NOT_ENOUGH, labelConfirm, labelCancel, True, True)
            else:
                self.setButtonState(self.RESUME_PAGE_NOT_ENOUGH, labelConfirm, labelCancel, False, True)
        if type == self.RESUME_PAGE_START:
            expireTime = const.TIME_INTERVAL_MONTH
            itemData = ID.data.get(self.resumeItem.id, {})
            ownershipAdd = itemData.get('mallRenewalOwnership', 0)
            ownershipPercent = min(self.resumeItem.ownershipPercent + ownershipAdd, const.ITEM_OWNERSHIP_MAX)
            expireTime = max(utils.getNow(), self.resumeItem.expireTime) + expireTime - utils.getNow()
            ownerShip = '%d%%' % ownershipPercent
            if ownershipAdd == 100:
                timeName = uiUtils.getTextFromGMD(GMDD.data.FOREVER_TEXT, gameStrings.TEXT_SELFADAPTIONSHOPPROXY_38)
            else:
                timeName = utils.formatDurationShortVersion(expireTime)
        else:
            timeName = uiUtils.getTextFromGMD(GMDD.data.FOREVER_TEXT, gameStrings.TEXT_SELFADAPTIONSHOPPROXY_38)
            ownerShip = '100%'
        label1 = uiUtils.getTextFromGMD(GMDD.data.EXPIRE_TIME_ADD, gameStrings.TEXT_ITEMRESUMEPROXY_154) % timeName
        label2 = uiUtils.getTextFromGMD(GMDD.data.PAY_CONFIRM, gameStrings.TEXT_ITEMRESUMEPROXY_155 % ownerShip)
        self.mediator.Invoke('setShowLabelForPage2', (GfxValue(gbk2unicode(label1)), GfxValue(gbk2unicode(label2))))
        cost = self.getTypeCost(type)
        enough = self.getSelectTypeEnough(type)
        self.mediator.Invoke('setCostText', (GfxValue(cost), GfxValue(enough)))

    def dismiss(self, *arg):
        self.clearWidget()

    def clearWidget(self):
        self.reset()
        if BigWorld.player():
            if BigWorld.player().__class__.__name__ == 'PlayerAvatar':
                BigWorld.player().unRegisterEvent(const.EVENT_UPDATE_COIN, self.onCoinChange)
        if self.mediator:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ITEM_RESUME)
        self.mediator = None
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def show(self, item, page, index, types = const.RES_KIND_INV):
        self.resumeItem = item
        self.page = page
        self.pos = index
        self.bagType = types
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ITEM_RESUME)

    def onConfirm(self, *args):
        if self.pos != const.CONT_NO_POS:
            BigWorld.player().cell.renewalItemUsingCoin(self.bagType, self.page, self.pos, self.nowType + 1)
        self.clearWidget()

    def onBuyCard(self, *args):
        gameglobal.rds.ui.tianyuMall.onOpenChargeWindow()

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator and kind == const.RES_KIND_INV:
            if page == self.page and pos == self.pos:
                return True
        return False
