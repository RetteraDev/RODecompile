#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedSpriteUnitFrameProxy.o
import BigWorld
import gametypes
import gameglobal
import gamelog
from uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils
from guis import events
from guis.asObject import ASObject
from guis.asObject import Tweener
from data import summon_sprite_data as SSD

class SummonedSpriteUnitFrameProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedSpriteUnitFrameProxy, self).__init__(uiAdapter)
        self.widget = None
        self.actionBarWidget = None
        self.summonedSprite = None
        self.reset()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_SPRITE_UNIT_FRAME:
            self.widget = widget
            self.initUI()
        elif widgetId == uiConst.WIDGET_SUMMONED_SPRITE_ACTION_BAR:
            self.actionBarWidget = widget
            self.initActionBar()

    def showActionBar(self):
        if not self.actionBarWidget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_SPRITE_ACTION_BAR)

    def initActionBar(self):
        skillInfo = BigWorld.player().getClientSkillInfo(1101, 1)
        skillData = uiUtils.getGfxSkill(skillInfo)
        self.actionBarWidget.mainMC.slot.setItemSlotData(skillData)
        self.actionBarWidget.mainMC.slot.addEventListener(events.MOUSE_CLICK, self.onClickUseSkill, False, 0, True)

    def onClickUseSkill(self, *args):
        self.actionBarWidget.mainMC.gotoAndPlay('down')

    def closeActionBar(self):
        self.actionBarWidget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_SPRITE_ACTION_BAR)

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_SPRITE_UNIT_FRAME)
        self.reset()

    def show(self):
        enableSummonedSprite = gameglobal.rds.configData.get('enableSummonedSprite', False)
        if not enableSummonedSprite:
            return
        if not BigWorld.player().summonSpriteList:
            return
        self.reset()
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_SPRITE_UNIT_FRAME)
        else:
            self.initUI()

    def initUI(self):
        if not self.widget:
            return
        self.resetZhaoHuan(False)

    def updateSummonedSpriteInfo(self, summonedSprite):
        if not self.widget:
            return
        if self.summonedSprite != summonedSprite:
            return
        if not self.widget.mainMC.lvMC:
            return
        self.widget.mainMC.lvMC.lvTF.text = summonedSprite.lv
        self.widget.mainMC.HPBar.currentValue = summonedSprite.hp * 100.0 / summonedSprite.mhp

    def updateSummonedSpriteLV(self, summonedSprite):
        if not self.widget:
            return
        if self.summonedSprite != summonedSprite:
            return
        if not self.widget.mainMC.lvMC:
            return
        self.widget.mainMC.lvMC.lvTF.text = summonedSprite.lv

    def updateSummonedSpriteHP(self, summonedSprite):
        if not self.widget:
            return
        if self.summonedSprite != summonedSprite:
            return
        if not self.widget.mainMC.HPBar:
            return
        self.widget.mainMC.HPBar.currentValue = summonedSprite.hp * 100.0 / summonedSprite.mhp

    def updateSummonedSpriteMP(self, summonedSprite):
        if not self.widget:
            return
        if self.summonedSprite != summonedSprite:
            return
        if not self.widget.mainMC.MPBar:
            return
        self.widget.mainMC.MPBar.currentValue = summonedSprite.mp * 100.0 / summonedSprite.mmp

    def resetZhaoHuan(self, zhaoHuan, summonedSprite = None):
        if not self.widget:
            return
        self.summonedSprite = summonedSprite
        self.widget.mainMC.addEventListener(events.MOUSE_CLICK, self.summonSprite, False, 0, True)
        if zhaoHuan:
            self.widget.mainMC.gotoAndPlay('zhaohuan')
            self.widget.mainMC.addEventListener(events.MOUSE_ROLL_OVER, self.handleMenuOver, False, 0, True)
            self.widget.mainMC.addEventListener(events.MOUSE_ROLL_OUT, self.handleMenuOut, False, 0, True)
            self.widget.mainMC.func1MC.zhuDongAttackBtn.showMC.gotoAndPlay('zhudong')
            self.widget.mainMC.func1MC.genShuiAttackBtn.showMC.gotoAndPlay('baohu')
            self.widget.mainMC.func1MC.protectMasterBtn.showMC.gotoAndPlay('gensui')
            self.widget.mainMC.func1MC.idleBtn.showMC.gotoAndPlay('daiji')
            self.widget.mainMC.func1MC.zhuDongAttackBtn.addEventListener(events.MOUSE_CLICK, self.onFuncBtnClick, False, 0, True)
            self.widget.mainMC.func1MC.genShuiAttackBtn.addEventListener(events.MOUSE_CLICK, self.onFuncBtnClick, False, 0, True)
            self.widget.mainMC.func1MC.protectMasterBtn.addEventListener(events.MOUSE_CLICK, self.onFuncBtnClick, False, 0, True)
            self.widget.mainMC.func1MC.idleBtn.addEventListener(events.MOUSE_CLICK, self.onFuncBtnClick, False, 0, True)
            self.widget.mainMC.func2MC.teleportToMeBtn.addEventListener(events.MOUSE_CLICK, self.onFuncBtnClick, False, 0, True)
            self.widget.mainMC.func2MC.goBackBtn.addEventListener(events.MOUSE_CLICK, self.onFuncBtnClick, False, 0, True)
            iconId = SSD.data.get(summonedSprite.spriteId, {}).get('icon', '000')
            iconPath = 'summonedSprite/icon/%s.dds' % str(iconId)
            self.widget.mainMC.headMC.headIcon.loadImage(iconPath)
            self.widget.mainMC.HPBar.thumb.visible = False
            self.widget.mainMC.MPBar.validateNow()
            self.widget.mainMC.MPBar.thumb.visible = False
            self.updateSummonedSpriteInfo(summonedSprite)
            self.changeState(summonedSprite.mode)
        else:
            self.widget.mainMC.removeEventListener(events.MOUSE_ROLL_OVER, self.handleMenuOver)
            self.widget.mainMC.removeEventListener(events.MOUSE_ROLL_OUT, self.handleMenuOut)
            if self.widget.mainMC.func1MC:
                if self.widget.mainMC.func1MC.zhuDongAttackBtn:
                    self.widget.mainMC.func1MC.zhuDongAttackBtn.removeEventListener(events.MOUSE_CLICK, self.onFuncBtnClick)
                if self.widget.mainMC.func1MC.genShuiAttackBtn:
                    self.widget.mainMC.func1MC.genShuiAttackBtn.removeEventListener(events.MOUSE_CLICK, self.onFuncBtnClick)
                if self.widget.mainMC.func1MC.protectMasterBtn:
                    self.widget.mainMC.func1MC.protectMasterBtn.removeEventListener(events.MOUSE_CLICK, self.onFuncBtnClick)
                if self.widget.mainMC.func1MC.idleBtn:
                    self.widget.mainMC.func1MC.idleBtn.removeEventListener(events.MOUSE_CLICK, self.onFuncBtnClick)
                if self.widget.mainMC.func2MC.teleportToMeBtn:
                    self.widget.mainMC.func2MC.teleportToMeBtn.removeEventListener(events.MOUSE_CLICK, self.onFuncBtnClick)
                if self.widget.mainMC.func2MC.goBackBtn:
                    self.widget.mainMC.func2MC.goBackBtn.removeEventListener(events.MOUSE_CLICK, self.onFuncBtnClick)
            self.widget.mainMC.gotoAndPlay('weizhaohuan')

    def summonSprite(self, *args):
        if not self.summonedSprite:
            BigWorld.player().base.applySummonPreSprite()
            gamelog.debug('m.l@SummonedSpriteUnitFrameProxy.summonSprite')
        else:
            BigWorld.player().lockTarget(self.summonedSprite)

    def onFuncBtnClick(self, *args):
        e = ASObject(args[3][0])
        name = e.currentTarget.name
        p = BigWorld.player()
        if name == 'zhuDongAttackBtn':
            p.base.setSpriteMode(gametypes.SP_MODE_COVER)
        elif name == 'genShuiAttackBtn':
            p.base.setSpriteMode(gametypes.SP_MODE_ASSIST)
        elif name == 'protectMasterBtn':
            p.base.setSpriteMode(gametypes.SP_MODE_NOATK)
        elif name == 'idleBtn':
            p.base.setSpriteMode(gametypes.SP_MODE_NOATK)
        elif name == 'teleportToMeBtn':
            p.suggestSpriteTeleportToMe()
        elif name == 'goBackBtn':
            p.base.applyDismissSprite()
        self.showFuncMC(False)

    def handleMenuOver(self, *args):
        Tweener.removeTweens(self.widget.mainMC.func1MC)
        Tweener.removeTweens(self.widget.mainMC.func2MC)
        self.showFuncMC(True)

    def hideFuncMC1(self, *args):
        if self.widget.mainMC.func1MC:
            self.widget.mainMC.func1MC.visible = False

    def hideFuncMC2(self, *args):
        if self.widget.mainMC.func2MC:
            self.widget.mainMC.func2MC.visible = False

    def handleMenuOut(self, *args):
        Tweener.addTween(self.widget.mainMC.func1MC, {'time': 0.5,
         'alpha': 0.0,
         'transition': 'linear',
         'onComplete': self.hideFuncMC1})
        Tweener.addTween(self.widget.mainMC.func2MC, {'time': 0.5,
         'alpha': 0.0,
         'transition': 'linear',
         'onComplete': self.hideFuncMC2})

    def changeState(self, state):
        if not self.widget:
            return
        if state == gametypes.SP_MODE_COVER:
            self.widget.mainMC.HPBar.stateMC.gotoAndPlay('zhudong')
            self.widget.mainMC.diwenMC.gotoAndPlay('zhudong')
        elif state == gametypes.SP_MODE_ASSIST:
            self.widget.mainMC.HPBar.stateMC.gotoAndPlay('baohu')
            self.widget.mainMC.diwenMC.gotoAndPlay('baohu')
        elif state == gametypes.SP_MODE_NOATK:
            self.widget.mainMC.HPBar.stateMC.gotoAndPlay('gensui')
            self.widget.mainMC.diwenMC.gotoAndPlay('gensui')
        elif state == gametypes.SP_MODE_ATK:
            self.widget.mainMC.HPBar.stateMC.gotoAndPlay('daiji')
            self.widget.mainMC.diwenMC.gotoAndPlay('daiji')

    def showFuncMC(self, show):
        self.widget.mainMC.func1MC.alpha = 1.0
        self.widget.mainMC.func1MC.visible = show
        self.widget.mainMC.func2MC.alpha = 1.0
        self.widget.mainMC.func2MC.visible = show

    def reset(self):
        self.summonedSprite = None
