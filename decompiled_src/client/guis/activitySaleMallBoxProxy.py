#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/activitySaleMallBoxProxy.o
from gamestrings import gameStrings
import BigWorld
import time
import gameglobal
import uiConst
import events
import gametypes
import utils
import const
from item import Item
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis import uiUtils
from guis.asObject import ASObject
from guis.asObject import TipManager
from guis import uiConst
from data import preferential_activities_detail_data as PADD
from data import mall_item_data as MID
from data import item_data as ID
ITEM_START_Y = 189
ITEM_OFFSET_Y = 88
ITEM_COLUMN_CNT = 6
ICON_PATH = 'guitianyuMallBuy/%s.dds'

class ActivitySaleMallBoxProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivitySaleMallBoxProxy, self).__init__(uiAdapter)
        self.widget = None
        self.visibleActivityIdList = []
        self.reset()

    def reset(self):
        self.tabIdx = 0
        self.widget = None
        self.activityId = 0
        self.displayMode = gametypes.PREFERENTIAL_ACTIVITY_SHOW_TIME_TYPE_START_END
        self.mallId = 0
        self.itemRenderMcList = []
        self.timer = None

    def initPanel(self, tabIdx, currentView):
        self.tabIdx = tabIdx
        self.widget = currentView
        self.activityId = self.visibleActivityIdList[tabIdx - uiConst.ACTIVITY_SALE_TAB_MALL_BOX_1]
        self.displayMode = PADD.data.get(self.activityId, {}).get('showTimeType', gametypes.PREFERENTIAL_ACTIVITY_SHOW_TIME_TYPE_START_END)
        self.delTimer()
        self.initUI()
        self.addEvent(events.EVENT_TIANBI_COIN_CHANGED, self.refreshInfo)
        self.addEvent(events.EVENT_CASH_CHANGED, self.refreshInfo)
        self.refreshInfo()

    def unRegisterMallBox(self, tabIdx):
        self.uiAdapter.fittingRoom.hide()
        for itemRenderMc in self.itemRenderMcList:
            self.widget.mainMc.rightWnd.canvas.removeChild(itemRenderMc)

        self.widget = None
        self.delTimer()
        self.tabIdx = 0
        self.reset()
        self.delEvent(events.EVENT_TIANBI_COIN_CHANGED, self.refreshInfo)
        self.delEvent(events.EVENT_CASH_CHANGED, self.refreshInfo)

    def clearWidget(self):
        self.widget = None

    def addTimer(self):
        if not self.timer:
            self.timer = BigWorld.callback(1, self.timerFunc, -1)

    def timerFunc(self):
        if not self.widget:
            self.delTimer()
            return
        openServerTime = utils.getServerOpenTime()
        left = PADD.data.get(self.activityId, {}).get('durationTime', 0) * 24 * 60 * 60 - (utils.getNow() - openServerTime)
        self.widget.mainMc.txtTimeDesc.leftTime.text = gameStrings.ACTIVITY_SALE_MALL_BOX_LEFT_TIME % utils.formatDurationShortVersion(left)

    def delTimer(self):
        self.timer and BigWorld.cancelCallback(self.timer)
        self.timer = None

    def initUI(self):
        self.mallId = PADD.data.get(self.activityId, {}).get('mallId', 0)
        itemId = MID.data.get(self.mallId, {}).get('itemId', 0)
        self.widget.mainMc.rightWnd.canvas.itemIcon.fitSize = True
        self.widget.mainMc.rightWnd.canvas.itemIcon.loadImage(uiUtils.getItemIconFile110(itemId))
        TipManager.addItemTipById(self.widget.mainMc.rightWnd.canvas.itemIcon, itemId)
        posY = ITEM_START_Y
        itemList = PADD.data.get(self.activityId, {}).get('itemList', 0)
        self.widget.mainMc.rightWnd.canvasBg.loadImage(self.getIconPath(PADD.data.get(self.activityId, {}).get('bg', '')))
        self.widget.mainMc.rightWnd.canvas.canvas.loadImage(self.getIconPath(PADD.data.get(self.activityId, {}).get('bg', '')))
        index = 0
        for txtDesc, itemsLines in itemList:
            for items in itemsLines:
                if PADD.data.get(self.activityId, {}).get('canBuyFilter', 0):
                    items = self.filterItems(items)
                if not items:
                    continue
                itemRenderMc = self.widget.getInstByClsName('ActivitySaleMallBox_Item')
                self.widget.mainMc.rightWnd.canvas.addChild(itemRenderMc)
                itemRenderMc.x = 0
                itemRenderMc.y = posY
                self.itemRenderMcList.append(itemRenderMc)
                posY += ITEM_OFFSET_Y
                itemRenderMc.txtDesc.text = txtDesc
                txtDesc = ''
                itemRenderMc.itemBg.loadImage(self.getIconPath(PADD.data.get(self.activityId, {}).get('itemBg', '')))
                itemRenderMc.itemBg.visible = not (index == 0 and PADD.data.get(self.activityId, {}).get('hideFirstBg', 0))
                for i in xrange(ITEM_COLUMN_CNT):
                    itemMc = getattr(itemRenderMc, 'item%d' % i)
                    if i < len(items):
                        itemMc.visible = True
                        itemMc.slot.dragable = False
                        itemMc.slot.itemId = items[i]
                        itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(items[i], srcType='activitySaleMallBox'))
                        itemMc.slot.addEventListener(events.MOUSE_CLICK, self.handleShowFit, False, 0, True)
                    else:
                        itemMc.visible = False

                index += 1

        self.widget.mainMc.rightWnd.refreshHeight(posY)
        if self.displayMode == gametypes.PREFERENTIAL_ACTIVITY_SHOW_TIME_TYPE_START_END:
            endTimeStr = PADD.data.get(self.activityId, {}).get('endTime', '')
            endTime = utils.getTimeSecondFromStr(endTimeStr)
            timeStruct = time.localtime(endTime)
            self.widget.mainMc.txtTimeDesc.leftTime.text = gameStrings.ACTIVITY_SALE_MALL_BOX_END_TIME + gameStrings.TEXT_ACTIVITYSALEMALLBOXPROXY_130 % (timeStruct.tm_year,
             timeStruct.tm_mon,
             timeStruct.tm_mday,
             timeStruct.tm_hour)
        else:
            self.timerFunc()
            self.addTimer()
        self.widget.mainMc.rightWnd.canvas.btns.buyBtn.addEventListener(events.BUTTON_CLICK, self._onBuyBtnClick, False, 0, True)
        self.widget.mainMc.rightWnd.canvas.btns.sendBtn.addEventListener(events.BUTTON_CLICK, self._onSendBtnClick, False, 0, True)
        self.widget.mainMc.chargeButton.addEventListener(events.BUTTON_CLICK, self._onChangeBtnClick, False, 0, True)

    def getIconPath(self, name):
        return ICON_PATH % name

    def filterItems(self, items):
        p = BigWorld.player()
        result = []
        for itemId in items:
            schReq = ID.data.get(itemId, {}).get('schReq', ())
            if schReq and p.realSchool not in schReq:
                continue
            sexReq = ID.data.get(itemId, {}).get('sexReq', None)
            physique = getattr(p, 'physique', None)
            sex = getattr(physique, 'sex', -1)
            if sexReq and sex != sexReq:
                continue
            allowBodyType = ID.data.get(itemId, {}).get('allowBodyType', ())
            if allowBodyType and p.physique.bodyType not in allowBodyType:
                continue
            result.append(itemId)

        return result

    def refreshInfo(self, *args):
        if not self.widget:
            return
        p = BigWorld.player()
        self.widget.mainMc.cashNum.text = format(p.unbindCoin + p.bindCoin + p.freeCoin, ',')

    def _onBuyBtnClick(self, *args):
        self.uiAdapter.tianyuMallBuyV2.show(self.activityId, self.mallId, displayMode=uiConst.TIANYU_MALL_BUY_MODE_BUY)

    def _onSendBtnClick(self, *args):
        self.uiAdapter.tianyuMallBuyV2.show(self.activityId, self.mallId, displayMode=uiConst.TIANYU_MALL_BUY_MODE_SEND)

    def _onChangeBtnClick(self, *args):
        self.uiAdapter.tianyuMall.onOpenChargeWindow(*args)

    def onGetToolTip(self, itemId):
        item = Item(itemId)
        return self.uiAdapter.inventory.GfxToolTip(item, location=const.ITEM_IN_BAG)

    def handleShowFit(self, *args):
        e = ASObject(args[3][0])
        if e.buttonIdx == uiConst.LEFT_BUTTON:
            itemId = int(e.currentTarget.itemId)
            self.uiAdapter.fittingRoom.addItem(Item(itemId))
