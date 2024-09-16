#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/skillAppearanceConfirmProxy.o
import BigWorld
import gameglobal
import math
import uiConst
import const
import events
import utils
from uiProxy import SlotDataProxy
from item import Item
from gamestrings import gameStrings
from callbackHelper import Functor
from helpers import skillAppearancesUtils
from guis import uiUtils
from data import consumable_item_data as CID
from data import skill_appearance_data as SAD
from cdata import game_msg_def_data as GMDD
SLOT_STATE_EMPTY = 0
SLOT_STATE_FIRST = 1
SLOT_STATE_SECOND = 2
SLOT_STATE_HELP = 99
SLOT_STATE_SELECTED = 100

class SkillAppearanceConfirmProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(SkillAppearanceConfirmProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.bindType = 'skillAppearanceConfirm'
        self.type = 'skillAppearanceConfirm'
        uiAdapter.registerEscFunc(uiConst.WIDGET_SKILL_APPEARANCE_CONFIRM, self.hide)

    def reset(self):
        self.itemId = -1
        self.itemUUID = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SKILL_APPEARANCE_CONFIRM:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SKILL_APPEARANCE_CONFIRM)
        self.reset()
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def getSlotID(self, key):
        return (0, 0)

    def show(self, itemId, itemUUID):
        tmpItem = Item(itemId)
        if not tmpItem or not tmpItem.isSkillAppearanceItem():
            return
        self.itemId = itemId
        self.itemUUID = itemUUID
        self._realShow()
        if not gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.show()

    def _realShow(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SKILL_APPEARANCE_CONFIRM)
        else:
            self.refreshInfo()

    def isShow(self):
        return not not self.widget

    def onItemDrag(self, item):
        if not item or not item.isSkillAppearanceItem():
            return
        if not skillAppearancesUtils.checkItemCanUse(item):
            BigWorld.player().showGameMsg(GMDD.data.COMMON_MSG, gameStrings.SKILL_APPEARANCE_ITEM_CANNOT_USE)
            return
        self.show(item.id, item.uuid)

    def onUseItem(self, item):
        if not item or not item.isSkillAppearanceItem():
            return
        if not skillAppearancesUtils.checkItemCanUse(item):
            BigWorld.player().showGameMsg(GMDD.data.COMMON_MSG, gameStrings.SKILL_APPEARANCE_ITEM_CANNOT_USE)
            return
        self.show(item.id, item.uuid)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.desc.text = ''
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)
        self.widget.cancelBtn.addEventListener(events.BUTTON_CLICK, self.handleCancelBtnClick, False, 0, True)
        self.widget.item.binding = 'skillAppearanceConfirm0.slot0'
        self.widget.item.dragable = False

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.widget.item.enabled = True
        allNum = p.inv.countItemInPages(self.itemId)
        needNum = 1
        itemInfo = uiUtils.getGfxItemById(self.itemId, uiUtils.convertNumStr(allNum, needNum))
        if allNum < needNum:
            itemInfo['state'] = uiConst.COMPLETE_ITEM_LEAKED
        else:
            itemInfo['state'] = uiConst.ITEM_NORMAL
        self.widget.item.setItemSlotData(itemInfo)
        self.widget.confirmBtn.enabled = allNum >= needNum
        itemConfig = CID.data.get(self.itemId, {})
        expireTime = itemConfig.get('expireTime', -1)
        appearanceId = itemConfig.get('appearanceId', 0)
        skillName = SAD.data.get(appearanceId, {}).get('nName', '')
        if skillName:
            self.widget.desc.text = gameStrings.SKILL_APPEARANCE_CONFIRM_DESC % (skillName, self._getCurrentLeftTime(expireTime))
        else:
            self.widget.desc.text = ''
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def handleConfirmBtnClick(self, *args):
        p = BigWorld.player()
        item, page, idx = p.inv.findItemByUUID(self.itemUUID)
        if not item or not item.isSkillAppearanceItem():
            return
        if not skillAppearancesUtils.checkItemCanUse(item):
            BigWorld.player().showGameMsg(GMDD.data.COMMON_MSG, gameStrings.SKILL_APPEARANCE_ITEM_CANNOT_USE)
            return
        aid = CID.data.get(item.id, {}).get('appearanceId', -1)
        expire = skillAppearancesUtils.getAppearanceExpire(aid)
        if expire == 0 or expire > 0 and expire > utils.getNow():
            import gamelog
            gamelog.debug('ypc@ expire', expire, gameglobal.rds.ui.skillAppearance.getDeadlineTextPure(expire))
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.SKILL_APPEARANCE_CONTINUE_USE % gameglobal.rds.ui.skillAppearance.getDeadlineTextPure(expire), Functor(self._realUseSkillAppearanceItem, page, idx))
            return
        self._realUseSkillAppearanceItem(page, idx)

    def handleCancelBtnClick(self, *args):
        self.hide()

    def isItemDisabled(self, kind, page, pos, item):
        p = BigWorld.player()
        _, pg, i = p.inv.findItemByUUID(self.itemUUID)
        if self.widget and kind == const.RES_KIND_INV:
            if (page, pos) == (pg, i):
                return True
            if not item.isSkillAppearanceItem():
                return True
            if skillAppearancesUtils.checkItemCanUse(item):
                return False
            return True
        else:
            return False

    def _getCurrentLeftTime(self, leftTime):
        if leftTime == 0:
            return gameStrings.COMMON_INFINITE_TIME
        elif leftTime > const.TIME_INTERVAL_DAY:
            return str(int(math.ceil(float(leftTime) / const.TIME_INTERVAL_DAY))) + gameStrings.COMMON_DAY
        elif leftTime > const.TIME_INTERVAL_HOUR:
            return str(int(math.ceil(float(leftTime) / const.TIME_INTERVAL_HOUR))) + gameStrings.COMMON_HOUR
        elif leftTime > const.TIME_INTERVAL_MINUTE:
            return str(int(math.ceil(float(leftTime) / const.TIME_INTERVAL_MINUTE))) + gameStrings.COMMON_MINUTE
        else:
            return gameStrings.COMMON_LESSTHAN_ONE_MINUTE

    def _getSkillIdAndAppearanceId(self, itemId):
        appearanceId = CID.data.get(itemId, {}).get('appearanceId', -1)
        skillId = SAD.data.get(appearanceId, {}).get('skillId', -1)[0]
        return (appearanceId, skillId)

    def _realUseSkillAppearanceItem(self, page, idx):
        p = BigWorld.player()
        p.useBagItem(page, idx)
        self.hide()
