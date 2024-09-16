#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteUpProxy.o
import BigWorld
import uiConst
import gameglobal
import gametypes
import events
from guis import uiUtils
from uiProxy import UIProxy
from callbackHelper import Functor
from gameStrings import gameStrings
from data import sys_config_data as SCD
from data import summon_sprite_info_data as SSID
from data import item_data as ID
from cdata import game_msg_def_data as GMDD

class SummonedWarSpriteUpProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteUpProxy, self).__init__(uiAdapter)
        self.widget = None
        self.spriteInfo = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_SPRITE_UP, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_SPRITE_UP:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_SPRITE_UP)

    def reset(self):
        self.spriteInfo = None

    def show(self):
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_SPRITE_UP)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.help.helpKey = SCD.data.get('spriteUpMarrowHelpKey', 0)

    def refreshInfo(self):
        if not self.widget:
            return
        self.spriteInfo = gameglobal.rds.ui.summonedWarSpriteMine.getCurSelectSpriteInfo()
        spriteId = self.spriteInfo.get('spriteId', 0)
        props = self.spriteInfo.get('props', {})
        baseGrowthRatio = props.get('baseGrowthRatio', 0)
        juexing = props.get('juexing', 0)
        boneLv = props.get('boneLv', 0)
        SSIData = SSID.data.get(spriteId, {})
        spriteBoneGrowth = SSIData.get('spriteBoneGrowth', 0)
        growthRatio, boneRatio = self.getSpriteGrowthRatio(baseGrowthRatio, juexing, boneLv, spriteBoneGrowth)
        desc1 = SCD.data.get('spriteBoneDesc1', '%.2f(%.2f)')
        self.widget.descT1.htmlText = desc1 % (growthRatio, boneRatio)
        boneMaxLv = SSIData.get('spriteBoneTimes', 0)
        desc2 = SCD.data.get('spriteBoneDesc2', '%d/%d')
        self.widget.descT2.htmlText = desc2 % (boneLv, boneMaxLv)
        self.widget.backBtn.visible = False
        self.widget.consumeMc.visible = True if boneLv < boneMaxLv else False
        self.widget.descT4.visible = True if boneLv >= boneMaxLv else False
        self.widget.confirmBtn.enabled = False if boneLv >= boneMaxLv else True
        if boneLv >= boneMaxLv:
            return
        boneNeed = SSIData.get('spriteBoneNeed', ())
        boneCash = SSIData.get('spriteBoneCash', ())
        needNum = boneNeed[boneLv]
        needCash = boneCash[boneLv]
        itemId = self.getBoneItemId()
        itemName = ID.data.get(itemId, {}).get('name', '')
        self.widget.consumeMc.descT3.text = gameStrings.SPRITE_CONSUME_ITEM_DESC % itemName
        slot = self.widget.consumeMc.itemMc.slot
        p = BigWorld.player()
        ownNum = p.inv.countItemInPages(uiUtils.getParentId(itemId), enableParentCheck=True)
        if ownNum < needNum:
            strNum = uiUtils.toHtml(ownNum, '#FF0000')
            slot.setSlotState(uiConst.COMPLETE_ITEM_LEAKED)
            slot.addEventListener(events.MOUSE_CLICK, self.handleItemMcClick, False, 0, True)
        else:
            strNum = uiUtils.toHtml(ownNum, '#FFFFE6')
            slot.setSlotState(uiConst.ITEM_NORMAL)
            slot.removeEventListener(events.MOUSE_CLICK, self.handleItemMcClick)
        count = str('%s/%d' % (strNum, needNum))
        slot.fitSize = True
        slot.dragable = False
        slot.setItemSlotData(uiUtils.getGfxItemById(itemId, count=count))
        self.widget.consumeMc.cashIcon.bonusType = 'bindCash'
        self.widget.consumeMc.cashValT.text = needCash
        if ownNum >= needNum and p.bindCash + p.cash >= needCash:
            self.widget.confirmBtn.enabled = True
        else:
            self.widget.confirmBtn.enabled = False

    def handleItemMcClick(self, *args):
        self.uiAdapter.itemSourceInfor.openPanel()

    def getBoneItemId(self):
        itemIds = SCD.data.get('spriteBoneItemId', (50235, 0))
        if self.spriteInfo.get('rareLv', 0) == gametypes.SPRITE_RARE_TYPE_SPECIAL:
            return itemIds[1]
        else:
            return itemIds[0]

    def getSpriteGrowthRatio(self, baseRatio, isJuexing, boneLv, boneBonusRatio):
        juexingBonusRatio = SCD.data.get('juexingBonusRatio', 0.1) if isJuexing else 0
        return (round(baseRatio * (1 + juexingBonusRatio), 3), round(boneLv * boneBonusRatio, 3))

    def _onBackBtnClick(self, e):
        if not self.spriteInfo:
            return
        spriteIndex = self.spriteInfo.get('index', 0)
        spriteId = self.spriteInfo.get('spriteId', 0)
        props = self.spriteInfo.get('props', {})
        boneLv = props.get('boneLv', 0)
        cashList = SSID.data.get(spriteId, {}).get('spriteBoneWithdrawCash', ())
        boneMaxLv = SSID.data.get(spriteId, {}).get('spriteBoneTimes', 0)
        if boneLv <= 0 or boneLv > boneMaxLv:
            return
        p = BigWorld.player()
        msg = gameStrings.SPRITE_CONSUME_BINDCASH_BACK_BONE % cashList[boneLv - 1]
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(p.base.applyWithdrawBones, spriteIndex))

    def _onConfirmBtnClick(self, e):
        if not self.spriteInfo:
            return
        spriteIndex = self.spriteInfo.get('index', 0)
        spriteId = self.spriteInfo.get('spriteId', 0)
        props = self.spriteInfo.get('props', {})
        boneLv = props.get('boneLv', 0)
        ssidData = SSID.data.get(spriteId, {})
        boneMaxLv = ssidData.get('spriteBoneTimes', 0)
        if boneLv >= boneMaxLv:
            return
        boneCash = ssidData.get('spriteBoneCash', ())
        needCash = boneCash[boneLv]
        p = BigWorld.player()
        toBoneLv = boneLv + 1
        if p.bindCash < needCash:
            msg = uiUtils.getTextFromGMD(GMDD.data.BINDCASH_IS_NOT_ENOUGH, '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(p.base.applyUseBoneSprite, spriteIndex, toBoneLv), msgType='bindCash', isShowCheckBox=True)
        else:
            p.base.applyUseBoneSprite(spriteIndex, toBoneLv)

    def _onCancelBtnClick(self, e):
        self.hide()
