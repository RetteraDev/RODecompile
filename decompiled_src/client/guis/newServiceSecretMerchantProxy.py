#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/newServiceSecretMerchantProxy.o
import BigWorld
import gameglobal
import utils
import events
import ui
import clientUtils
import time
import appSetting
import keys
from guis.asObject import ASObject
from uiProxy import UIProxy
from guis import uiUtils
from guis import uiConst
from guis.asObject import TipManager
from gamestrings import gameStrings
from data import new_server_activity_data as NSAD
from cdata import game_msg_def_data as GMDD
from data import mall_item_data as MID
from data import item_data as ITEMD
SECOND_PER_DAY = 86400

class NewServiceSecretMerchantProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NewServiceSecretMerchantProxy, self).__init__(uiAdapter)
        self.widget = None

    def reset(self):
        pass

    def initPanel(self, widget):
        self.day = utils.getServerOpenDays()
        self.rewardData = {}
        self.widget = widget
        self.initUI()
        self.giftSelected = 0
        p = BigWorld.player()
        p.base.queryNSDailyGiftData()
        dailyGifts = NSAD.data.get('dailyGiftRewards', [])
        todayGift = None
        if dailyGifts != []:
            todayGift = dailyGifts[self.day]
        self.mallId = todayGift[0]
        self.gitfId_1 = todayGift[1][0]
        self.gitfId_2 = todayGift[1][1]
        self.mallItem = MID.data.get(self.mallId, {})
        self.mallItemId = self.mallItem.get('itemId', 0)
        self.mallItemNumber = self.mallItem.get('many')
        self.mallItemPrice = self.mallItem.get('priceVal')
        self.buyWay = 0
        self.buyNumber = 1
        self.discountInfo = clientUtils.getMallItemDiscountInfo([self.mallId])
        self.widget.bg.mallItem.setItemSlotData(uiUtils.getGfxItemById(self.mallItemId, self.mallItemNumber))
        self.widget.bg.rewardItem_1.setItemSlotData(uiUtils.getGfxItemById(self.gitfId_1, 1))
        self.widget.bg.rewardItem_2.setItemSlotData(uiUtils.getGfxItemById(self.gitfId_2, 1))
        self.widget.bg.price.realPrice.text = str(self.mallItemPrice)
        self.widget.bg.rewardItem_1.tag = 1
        self.widget.bg.rewardItem_2.tag = 2
        if self.rewardData.has_key(self.day):
            self.widget.bg.confirmBtn.disabled = True
            self.widget.bg.broughtIcon.visible = True
            TipManager.addTip(self.widget.bg.confirmBtn, gameStrings.NEW_SERVER_DAILY_GIFT_BOUGHT)
            index = todayGift[1].index(self.rewardData[self.day])
            if index == 0:
                self.widget.bg.rewardItem_1.setSlotState(uiConst.ITEM_SELECTED)
                self.widget.bg.rewardItem_2.setSlotState(uiConst.ITEM_GRAY)
            else:
                self.widget.bg.rewardItem_1.setSlotState(uiConst.ITEM_GRAY)
                self.widget.bg.rewardItem_2.setSlotState(uiConst.ITEM_SELECTED)
        else:
            self.widget.bg.rewardItem_1.addEventListener(events.MOUSE_CLICK, self.onSelect, False, 0, True)
            self.widget.bg.rewardItem_2.addEventListener(events.MOUSE_CLICK, self.onSelect, False, 0, True)
        dailyGiftEndTime = utils.getServerOpenTime() + NSAD.data.get('dailyGiftOpenDay', 7) * SECOND_PER_DAY
        timeString = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(dailyGiftEndTime))
        self.widget.bg.mailText.text = gameStrings.NEW_SERVER_DAILY_GIFT_MAIL_TEXT % (int(timeString.split('-')[1]), int(timeString.split('-')[2].split(' ')[0]))
        self.widget.bg.mallItem.dragable = False
        self.widget.bg.rewardItem_1.dragable = False
        self.widget.bg.rewardItem_2.dragable = False
        self.widget.bg.rewardSlot.slot_1.dragable = False
        self.widget.bg.rewardSlot.slot_2.dragable = False
        self.widget.bg.rewardSlot.slot_3.dragable = False
        self.widget.bg.rewardSlot.slot_4.dragable = False
        self.widget.bg.rewardSlot.slot_5.dragable = False
        self.widget.bg.rewardSlot.slot_6.dragable = False
        self.widget.bg.rewardSlot.slot_7.dragable = False
        self.widget.bg.rewardSlot.slot_1.visible = False
        self.widget.bg.rewardSlot.slot_2.visible = False
        self.widget.bg.rewardSlot.slot_3.visible = False
        self.widget.bg.rewardSlot.slot_4.visible = False
        self.widget.bg.rewardSlot.slot_5.visible = False
        self.widget.bg.rewardSlot.slot_6.visible = False
        self.widget.bg.rewardSlot.slot_7.visible = False
        self.widget.bg.broughtIcon.visible = False

    def refreshInfo(self):
        if self.widget:
            self.showRewards()
        appSetting.Obj[keys.SET_NEW_SERVICE_AVTIVITY_DAILY_GIFT_PUSH % BigWorld.player().gbId] = utils.getNow()
        gameglobal.rds.ui.newServiceActivities.updateActiviesTabGiftRedPot()
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()

    def unRegisterPanel(self):
        self.widget = None

    def initUI(self):
        pass

    def showRewards(self):
        if not self.widget:
            return
        else:
            self.refreshReward()
            if self.rewardData.has_key(self.day):
                self.widget.bg.confirmBtn.disabled = True
                TipManager.addTip(self.widget.bg.confirmBtn, gameStrings.NEW_SERVER_DAILY_GIFT_BOUGHT)
                self.widget.bg.confirmBtn.removeEventListener(events.MOUSE_CLICK, self.onConfirm)
                self.widget.bg.broughtIcon.visible = True
                dailyGifts = NSAD.data.get('dailyGiftRewards', [])
                todayGift = None
                if dailyGifts != []:
                    todayGift = dailyGifts[self.day]
                index = todayGift[1].index(self.rewardData[self.day])
                if index == 0:
                    self.widget.bg.rewardItem_1.setSlotState(uiConst.ITEM_SELECTED)
                    self.widget.bg.rewardItem_2.setSlotState(uiConst.ITEM_GRAY)
                else:
                    self.widget.bg.rewardItem_1.setSlotState(uiConst.ITEM_GRAY)
                    self.widget.bg.rewardItem_2.setSlotState(uiConst.ITEM_SELECTED)
                self.widget.bg.rewardItem_1.removeEventListener(events.MOUSE_CLICK, self.onSelect)
                self.widget.bg.rewardItem_2.removeEventListener(events.MOUSE_CLICK, self.onSelect)
            if self.widget.bg.confirmBtn.disabled == False:
                self.widget.bg.confirmBtn.addEventListener(events.MOUSE_CLICK, self.onConfirm, False, 0, True)
            return

    def refreshReward(self):
        if self.widget != None:
            self.widget.bg.rewardHint.visible = False
            if self.rewardData == {}:
                self.widget.bg.rewardHint.visible = True
            else:
                rewardItems = self.rewardData.items()
                cnt = 1
                for rewardItem in rewardItems:
                    slot = 'slot_' + str(cnt)
                    if hasattr(self.widget.bg.rewardSlot, slot):
                        setSlot = getattr(self.widget.bg.rewardSlot, slot)
                        setSlot.visible = True
                        setSlot.setItemSlotData(uiUtils.getGfxItemById(rewardItem[1], 1))
                    cnt = cnt + 1

    def selectedDisable(self):
        self.widget.bg.rewardItem_1.setSlotState(uiConst.ITEM_NORMAL)
        self.widget.bg.rewardItem_2.setSlotState(uiConst.ITEM_NORMAL)

    def onSelect(self, *args):
        self.selectedDisable()
        e = ASObject(args[3][0])
        e.currentTarget.setSlotState(uiConst.ITEM_SELECTED)
        self.giftSelected = e.currentTarget.tag

    def onConfirm(self, *args):
        p = BigWorld.player()
        if self.giftSelected == 0:
            p.showGameMsg(GMDD.data.NEW_SERVER_DAILY_GIFT_BUY_FAIL_SELECTED_NOTHING, ())
            return
        else:
            rewardGiftId = None
            if self.giftSelected == self.widget.bg.rewardItem_1.tag:
                rewardGiftId = self.gitfId_1
            else:
                rewardGiftId = self.gitfId_2
            msg = gameStrings.NEW_SERVER_DAILY_GIFT_CONFIRM.format(self.mallItemPrice, ITEMD.data.get(rewardGiftId)['name'])
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self.yesCallback, noCallback=self.noCallback)
            return

    @ui.checkInventoryLock()
    def yesCallback(self):
        rewardGiftId = None
        if self.giftSelected == self.widget.bg.rewardItem_1.tag:
            rewardGiftId = self.gitfId_1
        else:
            rewardGiftId = self.gitfId_2
        p = BigWorld.player()
        p.base.buyNSDailyGift(self.mallId, self.buyNumber, p.cipherOfPerson, self.buyWay, self.discountInfo[0], rewardGiftId)

    def noCallback(self):
        pass

    def canOpenTab(self):
        return utils.getServerOpenDays() < NSAD.data.get('dailyGiftOpenDay', 7)
