#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/activitySaleWeekActivationProxy.o
import BigWorld
import events
import uiConst
import gameglobal
import gametypes
import utils
from callbackHelper import Functor
from uiProxy import UIProxy
from asObject import ASObject
from guis import uiUtils
from guis.asObject import TipManager
from gamestrings import gameStrings
from guis.asObject import ASUtils
from data import sys_config_data as SCD
from data import week_activation_privilege_prob_data as WAPPD
from data import week_activation_privilege_item_data as WAPID
from data import play_recomm_operation_activity_data as PROAD
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
MAX_CARD_NUM = 3
MAX_WEEK_ACT_STAGE_NUM = 3

class ActivitySaleWeekActivationProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivitySaleWeekActivationProxy, self).__init__(uiAdapter)
        self.widget = None

    def reset(self):
        pass

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()
        self.refreshInfo()

    def initUI(self):
        self.widget.weekActMc.txtDesc.text = gameStrings.PLAY_RECOMM_WEEK_ACTIVATION_DESC
        TipManager.addTip(self.widget.weekActMc.bonusIcon, gameStrings.PLAY_RECOMM_WEEK_ACTIVATION_DESC)

    def handleMoreWeekActClick(self, *args):
        e = ASObject(args[3][0])
        gameglobal.rds.ui.playRecomm.show(tabIdx=uiConst.PLAY_RECOMMV2_TAB_ACTIVITY_IDX, subTabIdx=uiConst.PLAY_RECOMMV2_TAB_DAILY_ACTIVITY_SUB_TAB)

    def handleCardBackBtnClick(self, *args):
        e = ASObject(args[3][0])
        cardMc = e.currentTarget.parent
        if e.currentTarget.disabled:
            BigWorld.player().showGameMsg(GMDD.data.WEEK_PRIVILEGE_BUY_FAIL_WEEK_ACTIVITION_LIMIT, ())
            return
        if cardMc.groupId:
            p = BigWorld.player()
            p.base.randomWeekPrivilegeBuyInfo(cardMc.groupId)

    def handleBuyBtnClick(self, *args):
        e = ASObject(args[3][0])
        buyBtn = e.currentTarget
        if buyBtn.groupId:
            p = BigWorld.player()
            fun = Functor(p.base.weekPrivilegeBuy, buyBtn.groupId)
            groupId = buyBtn.groupId
            privilegeId = p.weekPrivilegeBuyInfo[groupId].privilegeId
            info = WAPID.data.get(privilegeId, {})
            privilegeType = info.get('privilegeType', gametypes.WEEK_PRIVILEGE_BUY_TYPE_COIN)
            if privilegeType == gametypes.WEEK_PRIVILEGE_BUY_TYPE_COIN:
                msg = GMD.data.get(GMDD.data.WEEK_PRIVILEGE_BUY_CONFIRM, {}).get('text', '%d') % info.get('nowPrice', 0)
                self.uiAdapter.messageBox.showYesNoMsgBox(msg, fun)
            else:
                fun()

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.titleText.text = SCD.data.get('welfareWeekActTitleText', '')
        self.widget.moreWeekActText.text = SCD.data.get('welfareGetMoreWeekActText', '')
        self.widget.moreWeekActText.htmlText = '<u>%s</u>' % self.widget.moreWeekActText.text
        self.widget.moreWeekActText.addEventListener(events.MOUSE_CLICK, self.handleMoreWeekActClick, False, 0, True)
        self.updateCardBtnMc()
        self.updateWeekActivationMc()

    def updateCardBtnMc(self):
        p = BigWorld.player()
        for i in range(1, MAX_CARD_NUM + 1):
            cardMc = self.widget.getChildByName('card%d' % i)
            cardMc.groupId = i
            activationNeed = WAPPD.data.get(i, {}).get('activationNeed', 0)
            cardMc.cardBack.removeEventListener(events.BUTTON_CLICK, self.handleCardBackBtnClick)
            cardMc.cardBack.removeEventListener(events.MOUSE_CLICK, self.handleCardBackBtnClick)
            if p.weekActivation < activationNeed:
                cardMc.gotoAndStop('back')
                cardMc.cardBack.disabled = True
                cardMc.cardBack.addEventListener(events.MOUSE_CLICK, self.handleCardBackBtnClick, False, 0, True)
            elif i in p.weekPrivilegeBuyInfo and p.weekPrivilegeBuyInfo[i].privilegeId and p.weekPrivilegeBuyInfo[i].privilegeId in WAPID.data:
                cardMc.gotoAndStop('front')
                cardMc.cardFront.gotoAndStop(cardMc.cardFront.totalFrames)
                self.updateBasicBoxInfoMc(i)
            else:
                cardMc.gotoAndStop('back')
                cardMc.cardBack.disabled = False
                cardMc.cardBack.enabled = True
                cardMc.cardBack.addEventListener(events.BUTTON_CLICK, self.handleCardBackBtnClick, False, 0, True)

    def updateBasicBoxInfoMc(self, groupId):
        if not self.widget:
            return
        cardMc = self.widget.getChildByName('card%d' % groupId)
        basicBox = cardMc.cardFront.item0.basicBox
        basicBox.groupId = groupId
        p = BigWorld.player()
        privilegeId = p.weekPrivilegeBuyInfo[groupId].privilegeId
        buyStates = p.weekPrivilegeBuyInfo[groupId].privilegeStatus
        info = WAPID.data.get(privilegeId, {})
        privilegeType = info.get('privilegeType', gametypes.WEEK_PRIVILEGE_BUY_TYPE_COIN)
        if privilegeType != gametypes.WEEK_PRIVILEGE_BUY_TYPE_ITEM:
            basicBox.priceType.bonusType = uiConst.MONEY_TYPE_MAP[privilegeType]
            basicBox.priceType.visible = True
            basicBox.itemIcon.visible = False
            nowPrice = info.get('nowPrice', 0)
            sourcePrice = info.get('sourcePrice', 1)
        else:
            basicBox.priceType.visible = False
            basicBox.itemIcon.visible = True
            basicBox.itemIcon.fitSize = True
            needItemId = info.get('needItemId', 0)
            basicBox.itemIcon.loadImage(uiUtils.getItemIconPath(needItemId))
            TipManager.addItemTipById(basicBox.itemIcon, needItemId)
            nowPrice = info.get('needItemNowCount', 1)
            sourcePrice = info.get('needItemSourceCount', 1)
        discountRate = nowPrice * 1.0 / sourcePrice
        if discountRate < 1.0:
            basicBox.itemLabel.gotoAndStop('discount')
            basicBox.itemLabel.valueText.visible = True
            basicBox.itemLabel.visible = True
            basicBox.discountLabel.visible = True
            intPart = int(discountRate * 10.0)
            floatPart = int((discountRate * 10.0 - intPart) * 10.0)
            if floatPart:
                subText = '.%d%s' % (floatPart, gameStrings.ACTIVITY_SHOP_PROXY_DISCOUNT)
            else:
                subText = gameStrings.ACTIVITY_SHOP_PROXY_DISCOUNT
            basicBox.discountLabel.mainText.text = str(intPart)
            basicBox.discountLabel.subText.text = subText
        else:
            basicBox.discountLabel.visible = False
            basicBox.itemLabel.visible = True
        basicBox.priceValue.textField.text = nowPrice
        itemCnt = info.get('privilegeItemCount', 1)
        basicBox.itemName.nameText.htmlText = uiUtils.getItemColorName(info.get('privilegeItemId', 0), itemCnt)
        slotData = uiUtils.getGfxItemById(info.get('privilegeItemId', 0))
        basicBox.itemSlot.setItemSlotData(slotData)
        basicBox.itemSlot.validateNow()
        basicBox.itemSlot.setValueAmountTxt(itemCnt)
        basicBox.itemSlot.valueAmount.x = -45
        basicBox.itemSlot.valueAmount.y = 50
        basicBox.itemSlot.dragable = False
        ASUtils.setHitTestDisable(basicBox.discountLabel, True)
        cardMc.cardFront.item0.buyBtn.groupId = groupId
        if buyStates == gametypes.WEEK_PRIVILEGE_BUY_STATE_HAS_BUY:
            cardMc.cardFront.item0.buyBtn.enabled = False
            cardMc.cardFront.item0.buyBtn.label = gameStrings.PLAY_RECOMM_WEEK_ACTIVATION_HAD_BUY
        else:
            cardMc.cardFront.item0.buyBtn.enabled = True
            cardMc.cardFront.item0.buyBtn.label = gameStrings.PLAY_RECOMM_WEEK_ACTIVATION_BUY
        cardMc.cardFront.item0.buyBtn.addEventListener(events.BUTTON_CLICK, self.handleBuyBtnClick, False, 0, True)

    def updateWeekActivationMc(self):
        p = BigWorld.player()
        self.widget.weekActMc.valueText.text = str(p.weekActivation / 1000)
        for i in range(1, MAX_WEEK_ACT_STAGE_NUM + 1):
            stageVT = self.widget.weekActStageMc.getChildByName('stageVT%d' % i)
            stagePic = self.widget.weekActStageMc.getChildByName('stagePic%d' % i)
            activationNeed = WAPPD.data.get(i, {}).get('activationNeed', 0)
            stageVT.text = activationNeed / 1000
            if p.weekActivation < activationNeed:
                stagePic.gotoAndStop('grey')
            else:
                stagePic.gotoAndStop('bright')

    def sfxAtFrameAfter(self, *args):
        groupId = int(ASObject(args[3][0])[0])
        self.updateBasicBoxInfoMc(groupId)

    def updateAfterTrunCardMc(self):
        if not self.widget:
            return
        p = BigWorld.player()
        for i in range(1, MAX_CARD_NUM + 1):
            cardMc = self.widget.getChildByName('card%d' % i)
            if i in p.weekPrivilegeBuyInfo and p.weekPrivilegeBuyInfo[i].privilegeId and p.weekPrivilegeBuyInfo[i].privilegeId in WAPID.data:
                cardMc.gotoAndStop('front')
                ASUtils.callbackAtFrame(cardMc.cardFront, 10, self.sfxAtFrameAfter, i)

    def isRedFlagVisible(self):
        p = BigWorld.player()
        for i in range(1, MAX_CARD_NUM + 1):
            activationNeed = WAPPD.data.get(i, {}).get('activationNeed', 0)
            if p.weekActivation >= activationNeed and i not in p.weekPrivilegeBuyInfo:
                return True

        return False

    def isShowWeekActTabBtn(self):
        for key, value in PROAD.data.iteritems():
            conditionType = value.get('conditionType', gametypes.OPERATION_ACTIVITY_CONDITION_TYPE_WEEK_PRIVILEGE_BUY)
            if conditionType == gametypes.OPERATION_ACTIVITY_CONDITION_TYPE_WEEK_PRIVILEGE_BUY:
                return True

        return False
