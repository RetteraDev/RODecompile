#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/tianZhaoSummonedSpriteSkillSetProxy.o
import BigWorld
import gamelog
import uiConst
import const
import utils
import events
import gameglobal
from uiProxy import UIProxy
from guis import tipUtils
from guis.asObject import TipManager
from guis.asObject import ASObject
from guis.asObject import ASUtils
from gamestrings import gameStrings
from data import summon_sprite_info_data as SSID
from cdata import game_msg_def_data as GMDD
SPRITE_ICON_PATH = 'summonedSprite/icon/%s.dds'
UNLOCK_CNT = 2
SLOT_CNT = 4

class TianZhaoSummonedSpriteSkillSetProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(TianZhaoSummonedSpriteSkillSetProxy, self).__init__(uiAdapter)
        self.widget = None
        self.selSpriteItem = None
        self.selSpriteIndex = 0
        self.cacheSpriteDic = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_TIANZHAO_SUMMONED_SPRITE_SKILL_SET, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_TIANZHAO_SUMMONED_SPRITE_SKILL_SET:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.cacheSpriteDic = {}
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_TIANZHAO_SUMMONED_SPRITE_SKILL_SET)

    def reset(self):
        self.selSpriteItem = None
        self.selSpriteIndex = 0

    def show(self):
        BigWorld.player().base.querySpriteSEOrder()
        self.cacheSpriteDic = {}
        self.cacheSpriteDic.update(BigWorld.player().summonSpriteSEOrder)
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_TIANZHAO_SUMMONED_SPRITE_SKILL_SET)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def onSpriteChange(self):
        self.cacheSpriteDic = {}
        self.cacheSpriteDic.update(BigWorld.player().summonSpriteSEOrder)
        self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            summonSpriteSEOrder = self.cacheSpriteDic
            for pos in xrange(SLOT_CNT):
                spriteItem = self.widget.getChildByName('spriteItem%d' % pos)
                ASUtils.setHitTestDisable(spriteItem.lockIcon, True)
                ASUtils.setHitTestDisable(spriteItem.unlockText, True)
                TipManager.removeTip(spriteItem.selectBtn)
                spriteItem.pos = pos + 1
                spriteItem.spriteIndex = 0
                spriteItem.unlockText.text = ''
                spriteIndex = summonSpriteSEOrder.get(pos + 1, 0)
                spriteInfo = p.summonSpriteList.get(spriteIndex, {})
                if pos >= UNLOCK_CNT:
                    spriteItem.lockIcon.visible = True
                    spriteItem.unlockText.visible = True
                    spriteItem.selectBtn.visible = False
                    spriteItem.removeBtn.visible = False
                    spriteItem.selectIcon.visible = False
                    spriteItem.spriteState.visible = False
                    spriteItem.slot.setItemSlotData(None)
                    ASUtils.setHitTestDisable(spriteItem.slot, True)
                    spriteItem.selectBtn.enabled = False
                elif not summonSpriteSEOrder.get(pos + 1, 0) or not spriteInfo:
                    spriteItem.lockIcon.visible = False
                    spriteItem.unlockText.visible = False
                    spriteItem.selectBtn.visible = True
                    spriteItem.removeBtn.visible = False
                    spriteItem.selectIcon.visible = False
                    spriteItem.spriteState.visible = False
                    spriteItem.slot.setItemSlotData(None)
                    ASUtils.setHitTestDisable(spriteItem.slot, True)
                    spriteItem.selectBtn.label = gameStrings.SPRITE_FIGHT_SELECT_DESC
                    spriteItem.selectBtn.enabled = True
                    spriteItem.selectBtn.addEventListener(events.BUTTON_CLICK, self.handleSelectBtnClick, False, 0, True)
                else:
                    spriteItem.lockIcon.visible = False
                    spriteItem.unlockText.visible = False
                    spriteItem.removeBtn.visible = True
                    ASUtils.setHitTestDisable(spriteItem.slot, False)
                    if self.selSpriteItem and self.selSpriteItem.pos == pos:
                        spriteItem.selectIcon.visible = True
                    else:
                        spriteItem.selectIcon.visible = False
                    spriteItem.spriteIndex = spriteIndex
                    self.updateSpriteHeadItem(spriteItem, spriteIndex)

            self.updateReplaceAndsureBtn()
            return

    def updateReplaceAndsureBtn(self):
        summonSpriteSEOrder = BigWorld.player().summonSpriteSEOrder
        hasChange = False
        for k, v in self.cacheSpriteDic.iteritems():
            if not summonSpriteSEOrder.has_key(k) or summonSpriteSEOrder[k] != v:
                hasChange = True
                break

        self.widget.sureBtn.enabled = hasChange

    def _onSureBtnClick(self, e):
        orderList = self.cacheSpriteDic.keys()
        indexList = [ self.cacheSpriteDic[k] for k in orderList ]
        gamelog.info('jbx:setSpriteSEOrder', orderList, indexList)
        BigWorld.player().base.setSpriteSEOrder(orderList, indexList)
        self.hide()

    def handleRemoveBtnClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        spriteItem = target.parent
        self.cacheSpriteDic[spriteItem.pos] = 0
        self.refreshInfo()

    def handleSelectBtnClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        spriteItem = target.parent
        gameglobal.rds.ui.summonedWarSpriteFightSelect.show(spriteItem.spriteIndex, spriteItem.pos, self.onSeledtedSprite)

    def onSeledtedSprite(self, spriteIndex, pos):
        gamelog.info('jbx:onSeledtedSprite', pos, spriteIndex)
        if spriteIndex in self.cacheSpriteDic.values():
            BigWorld.player().showGameMsg(GMDD.data.SELECTED_SUMMONED_SPRITE_REPEAT, ())
            return
        self.cacheSpriteDic[pos] = spriteIndex
        self.uiAdapter.summonedWarSpriteFightSelect.hide()
        self.refreshInfo()

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
        self.updateReplaceAndsureBtn()

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
