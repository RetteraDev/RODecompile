#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteFightProxy.o
import BigWorld
import uiConst
import const
import utils
import events
import gameglobal
import formula
from uiProxy import UIProxy
from guis import uiUtils
from guis import tipUtils
from guis.asObject import TipManager
from guis.asObject import ASObject
from guis.asObject import ASUtils
from gamestrings import gameStrings
from data import sys_config_data as SCD
from data import summon_sprite_info_data as SSID
from data import map_config_data as MCD
from cdata import game_msg_def_data as GMDD
SPRITE_ICON_PATH = 'summonedSprite/icon/%s.dds'

class SummonedWarSpriteFightProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteFightProxy, self).__init__(uiAdapter)
        self.widget = None
        self.selSpriteItem = None
        self.selSpriteIndex = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_WAR_SPRITE_FIGHT, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_WAR_SPRITE_FIGHT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_FIGHT)

    def reset(self):
        self.selSpriteItem = None
        self.selSpriteIndex = 0

    def show(self):
        if not gameglobal.rds.configData.get('enableSpriteAutoCallOut', False):
            return
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_FIGHT)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            pendingList = p.spriteExtraDict['pendingList']
            lvLimit1 = SCD.data.get('spriteAutoCallOutLvLimit1', 0)
            lvLimit2 = SCD.data.get('spriteAutoCallOutLvLimit2', 69)
            mapId = formula.getMapId(p.spaceNo)
            size = MCD.data.get(mapId, {}).get('spritePendingListSize', ())
            for pos, info in enumerate(pendingList):
                spriteItem = self.widget.getChildByName('spriteItem%d' % pos)
                ASUtils.setHitTestDisable(spriteItem.lockIcon, True)
                ASUtils.setHitTestDisable(spriteItem.unlockText, True)
                TipManager.removeTip(spriteItem.selectBtn)
                spriteIndex = info.get('spriteIndex', 0)
                status = info.get('status', 0)
                spriteItem.spriteIndex = spriteIndex
                spriteItem.pos = pos
                if status == const.SPRITE_PENDING_SLOT_DISABLE:
                    spriteItem.lockIcon.visible = True
                    spriteItem.unlockText.visible = True
                    spriteItem.selectBtn.visible = False
                    spriteItem.removeBtn.visible = False
                    spriteItem.selectIcon.visible = False
                    spriteItem.spriteState.visible = False
                    spriteItem.slot.setItemSlotData(None)
                    ASUtils.setHitTestDisable(spriteItem.slot, True)
                    if pos in (0, 1):
                        spriteItem.unlockText.text = gameStrings.SPRITE_FIGHT_LV_DESC % lvLimit1
                    elif pos == 2:
                        spriteItem.unlockText.text = gameStrings.SPRITE_FIGHT_LV_DESC % lvLimit2
                    elif pos == 3:
                        spriteItem.unlockText.text = gameStrings.SPRITE_FIGHT_ADD_PACKAGE_DESC
                        spriteItem.selectBtn.visible = True
                        spriteItem.selectBtn.label = gameStrings.SPRITE_FIGHT_BUY_DESC
                        spriteItem.selectBtn.addEventListener(events.BUTTON_CLICK, self.handleSelectBtnClick, False, 0, True)
                elif status == const.SPRITE_PENDING_SLOT_EMPTY:
                    spriteItem.lockIcon.visible = False
                    spriteItem.unlockText.visible = False
                    spriteItem.selectBtn.visible = True
                    spriteItem.removeBtn.visible = False
                    spriteItem.selectIcon.visible = False
                    spriteItem.spriteState.visible = False
                    spriteItem.slot.setItemSlotData(None)
                    ASUtils.setHitTestDisable(spriteItem.slot, True)
                    if getattr(p, 'inCombat', False):
                        spriteItem.selectBtn.label = gameStrings.SPRITE_FIGHT_OUT_OF_WAR_DESC
                        spriteItem.selectBtn.disabled = True
                    else:
                        spriteItem.selectBtn.label = gameStrings.SPRITE_FIGHT_SELECT_DESC
                        spriteItem.selectBtn.disabled = False
                    spriteItem.selectBtn.addEventListener(events.BUTTON_CLICK, self.handleSelectBtnClick, False, 0, True)
                elif status == const.SPRITE_PENDING_SLOT_FULL:
                    spriteItem.lockIcon.visible = False
                    spriteItem.unlockText.visible = False
                    spriteItem.removeBtn.visible = True
                    ASUtils.setHitTestDisable(spriteItem.slot, False)
                    if self.selSpriteItem and self.selSpriteItem.pos == pos:
                        spriteItem.selectIcon.visible = True
                    else:
                        spriteItem.selectIcon.visible = False
                    self.updateSpriteHeadItem(spriteItem, spriteIndex)
                if pos >= size:
                    spriteItem.selectBtn.visible = True
                    spriteItem.selectBtn.label = gameStrings.SPRITE_FIGHT_UNAVAILABLE_DESC
                    spriteItem.selectBtn.disabled = True
                    tipMsg = uiUtils.getTextFromGMD(GMDD.data.SPRITE_FIGHT_UNAVILABEL_TIP, '')
                    TipManager.addTip(spriteItem.selectBtn, tipMsg)

            fightDesc = uiUtils.getTextFromGMD(GMDD.data.SPRITE_READY_FIGTH_MSG_DESC, '')
            self.widget.desc.text = fightDesc
            self.updateReplaceAndOutBtn()
            return

    def updateReplaceAndOutBtn(self):
        p = BigWorld.player()
        if not self.selSpriteIndex or getattr(p, 'inCombat', False):
            self.widget.replaceBtn.enabled = False
        else:
            self.widget.replaceBtn.enabled = True
        if not self.selSpriteIndex:
            self.widget.outBtn.enabled = False
        else:
            self.widget.outBtn.enabled = True

    def _onReplaceBtnClick(self, e):
        if not self.selSpriteItem:
            return
        pos = self.selSpriteItem.pos
        spriteIndex = self.selSpriteItem.spriteIndex
        gameglobal.rds.ui.summonedWarSpriteFightSelect.show(spriteIndex, pos)

    def _onOutBtnClick(self, e):
        gameglobal.rds.ui.summonedWarSpriteMine.callOutSprite(self.selSpriteIndex)
        self.hide()

    def handleRemoveBtnClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        spriteItem = target.parent
        p = BigWorld.player()
        p.base.removePendingSprite(spriteItem.spriteIndex, spriteItem.pos)

    def handleSelectBtnClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        spriteItem = target.parent
        if target.label == gameStrings.SPRITE_FIGHT_BUY_DESC:
            gameglobal.rds.ui.tianyuMall.showMallTab(10001, 0)
        elif target.label == gameStrings.SPRITE_FIGHT_SELECT_DESC:
            gameglobal.rds.ui.summonedWarSpriteFightSelect.show(spriteItem.spriteIndex, spriteItem.pos)

    def handleSelSpriteClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        spriteItem = target.parent
        if spriteItem.selectIcon.visible:
            return
        if self.selSpriteItem and self.selSpriteItem.selectIcon.visible:
            self.selSpriteItem.selectIcon.visible = False
        spriteItem.selectIcon.visible = True
        self.selSpriteIndex = spriteItem.spriteIndex
        self.selSpriteItem = spriteItem
        self.updateReplaceAndOutBtn()

    def updateSpriteHeadItem(self, spriteItem, spriteIndex):
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(spriteIndex, {})
        spriteId = spriteInfo.get('spriteId', 0)
        iconId = SSID.data.get(spriteId, {}).get('spriteIcon', '000')
        iconPath = SPRITE_ICON_PATH % str(iconId)
        spriteItem.slot.setItemSlotData({'iconPath': iconPath})
        spriteItem.slot.dragable = False
        if utils.getSpriteBattleState(spriteIndex) and utils.getSpriteAccessoryState(spriteIndex):
            spriteItem.spriteState.visible = True
            spriteItem.spriteState.gotoAndStop('zhanAndfu')
        elif utils.getSpriteBattleState(spriteIndex):
            spriteItem.spriteState.visible = True
            spriteItem.spriteState.gotoAndStop('zhan')
        elif utils.getSpriteAccessoryState(spriteIndex):
            spriteItem.spriteState.visible = True
            spriteItem.spriteState.gotoAndStop('fu')
        else:
            spriteItem.spriteState.visible = False
        if getattr(p, 'inCombat', False) and (spriteIndex in p.summonedSpriteLifeList or spriteIndex in p.spriteBattleCallBackList):
            spriteItem.selectBtn.label = gameStrings.SPRITE_FIGHT_OUT_OF_WAR_DESC
            spriteItem.selectBtn.disabled = True
            spriteItem.selectBtn.visible = True
            spriteItem.slot.setSlotState(uiConst.ITEM_GRAY)
            spriteItem.slot.removeEventListener(events.MOUSE_CLICK, self.handleSelSpriteClick)
            spriteItem.removeBtn.enabled = False
            spriteItem.removeBtn.removeEventListener(events.BUTTON_CLICK, self.handleRemoveBtnClick)
        else:
            spriteItem.selectBtn.visible = False
            spriteItem.slot.setSlotState(uiConst.ITEM_NORMAL)
            spriteItem.slot.addEventListener(events.MOUSE_CLICK, self.handleSelSpriteClick, False, 0, True)
            spriteItem.removeBtn.enabled = True
            spriteItem.removeBtn.addEventListener(events.BUTTON_CLICK, self.handleRemoveBtnClick, False, 0, True)
        spriteItem.slot.validateNow()
        TipManager.addTipByType(spriteItem.slot, tipUtils.TYPE_SPRITE_HEAD_TIP, (spriteIndex,), False, 'upLeft')

    def checkSpriteReadyFightState(self, index):
        if not index:
            return
        p = BigWorld.player()
        pendingList = p.spriteExtraDict['pendingList']
        for pos, info in enumerate(pendingList):
            spriteIndex = info.get('spriteIndex', 0)
            status = info.get('status', 0)
            if spriteIndex == index and status == const.SPRITE_PENDING_SLOT_FULL:
                return True

        return False

    def insertSpriteSuccess(self, index, pos):
        p = BigWorld.player()
        p.showGameMsg(GMDD.data.SPRITE_INSERT_PENDING_SUCCESS, ())
        gameglobal.rds.ui.summonedWarSpriteFightSelect.hide()
        self.refreshInfo()

    def removeSpriteSuccess(self, index, pos):
        if self.selSpriteItem and self.selSpriteItem.pos == pos:
            self.selSpriteIndex = 0
            self.selSpriteItem = None
        self.refreshInfo()
