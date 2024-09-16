#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedSpriteUnitFrameV2Proxy.o
from gamestrings import gameStrings
import BigWorld
import const
import gametypes
import gameglobal
import gamelog
import logicInfo
import utils
import tipUtils
import skillDataInfo
import ui
from uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils
from guis import events
from guis import hotkeyProxy
from guis import hotkey as HK
from guis.asObject import ASUtils
from guis.asObject import ASObject
from guis.asObject import TipManager
from guis.asObject import MenuManager
from gamestrings import gameStrings
from data import summon_sprite_info_data as SSID
from data import summon_sprite_data as SSD
from data import sys_config_data as SYSCD
from data import skill_general_data as SGD
from cdata import game_msg_def_data as GMDD

class SummonedSpriteUnitFrameV2Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedSpriteUnitFrameV2Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.summonedSprite = None
        self.awakeSkillCB = None
        self.teleportCB = None
        self.reset()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_SPRITE_UNIT_FRAMEV2:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_SPRITE_UNIT_FRAMEV2)
        self.reset()

    def show(self):
        enableSummonedSprite = gameglobal.rds.configData.get('enableSummonedSprite', False)
        if not enableSummonedSprite:
            return
        if not BigWorld.player().summonSpriteList:
            return
        self.reset()
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_SPRITE_UNIT_FRAMEV2)
        else:
            self.initUI()

    def initUI(self):
        if not self.widget:
            return
        p = BigWorld.player()
        if p.summonedSpriteInWorld:
            self.resetZhaoHuan(True, p.summonedSpriteInWorld)
        else:
            self.resetZhaoHuan(False)
        MenuManager.getInstance().registerMenuById(self.widget, uiConst.MENU_SUMMON_SPRITE, {})

    def updateSummonedSpriteInfo(self, summonedSprite):
        if not self.widget:
            return
        if self.summonedSprite != summonedSprite:
            return
        if not self.widget.mainMC.zhaoHuanMC.lvMC:
            return
        self.widget.mainMC.zhaoHuanMC.lvMC.lvTF.text = summonedSprite.lv
        if summonedSprite.mhp:
            self.widget.mainMC.zhaoHuanMC.HPBar.currentValue = summonedSprite.hp * 100.0 / summonedSprite.mhp
        if summonedSprite.mmp:
            self.widget.mainMC.zhaoHuanMC.MPBar.currentValue = summonedSprite.mp * 100.0 / summonedSprite.mmp

    def updateSummonedSpriteLV(self, summonedSprite):
        if not self.widget:
            return
        if not summonedSprite:
            return
        if self.summonedSprite != summonedSprite:
            return
        if not self.widget.mainMC.zhaoHuanMC.lvMC:
            return
        self.widget.mainMC.zhaoHuanMC.lvMC.lvTF.text = getattr(summonedSprite, 'lv', 0)

    def updateSummonedSpriteHP(self, summonedSprite):
        if not self.widget:
            return
        if self.summonedSprite != summonedSprite:
            return
        if not self.widget.mainMC.zhaoHuanMC.HPBar:
            return
        if not summonedSprite.mhp:
            return
        self.widget.mainMC.zhaoHuanMC.HPBar.currentValue = summonedSprite.hp * 100.0 / summonedSprite.mhp

    def updateSummonedSpriteMP(self, summonedSprite):
        if not self.widget:
            return
        if self.summonedSprite != summonedSprite:
            return
        if not self.widget.mainMC.zhaoHuanMC.MPBar:
            return
        if not summonedSprite.mmp:
            return
        self.widget.mainMC.zhaoHuanMC.MPBar.currentValue = summonedSprite.mp * 100.0 / summonedSprite.mmp

    def initMPHPBar(self):
        mainMC = self.widget.mainMC
        mainMC.zhaoHuanMC.MPBar.constraintsDisabled = True
        mainMC.zhaoHuanMC.MPBar.clockWise = False
        mainMC.zhaoHuanMC.MPBar.width = 400
        mainMC.zhaoHuanMC.MPBar.isProcessing = False
        mainMC.zhaoHuanMC.MPBar.setAngle(216, 324)
        ASUtils.setHitTestDisable(mainMC.zhaoHuanMC.MPBar, True)
        mainMC.zhaoHuanMC.HPBar.constraintsDisabled = True
        mainMC.zhaoHuanMC.HPBar.width = 400
        mainMC.zhaoHuanMC.HPBar.isProcessing = False
        mainMC.zhaoHuanMC.HPBar.setAngle(216, 327)
        ASUtils.setHitTestDisable(mainMC.zhaoHuanMC.HPBar, True)

    def initAwakeSkill(self):
        if not self.widget:
            return
        if not self.widget.mainMC.zhaoHuanMC:
            return
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(p.lastSpriteBattleIndex, {})
        awakeSkill = utils.getAwakeSkillBySprite()
        manualSkillMC = self.widget.mainMC.zhaoHuanMC.manualSkillMC
        if awakeSkill:
            manualSkillMC.skillMC.gotoAndPlay('normal')
            skillInfo = skillDataInfo.ClientSkillInfo(awakeSkill, lv=10)
            iconPath = uiUtils.getSkillIconPath(skillInfo, uiConst.ICON_SIZE40)
            manualSkillMC.skillMC.skillIcon.loadImage(iconPath)
            lv = utils.getAwakeSkillLvBySpriteIdx(p.lastSpriteBattleIndex)
            TipManager.addTipByType(manualSkillMC, tipUtils.TYPE_SKILL, {'skillId': awakeSkill,
             'lv': lv}, False, 'upLeft')
            manualSkillMC.keyMC.textField.text = BigWorld.player().getSpriteManualSkillHKBriefDesc()
        else:
            manualSkillMC.skillMC.gotoAndPlay('gray')
            TipManager.addTip(manualSkillMC, gameStrings.SPRITE_MANUAL_SKILL_DISABLED)
        props = spriteInfo.get('props', {})
        juexing = props.get('juexing', False)
        manualSkillMC.lockMC.visible = not juexing
        familiar = props.get('familiar', 0)
        spriteId = spriteInfo.get('spriteId', 0)
        sData = SSID.data.get(spriteId, {})
        awakeNeedFamiliarLv = sData.get('awakeNeedFamiliarLv', 0)
        lessFamiIcon = self.widget.mainMC.zhaoHuanMC.lessFamiIcon
        if juexing and familiar < awakeNeedFamiliarLv:
            lessFamiIcon.visible = True
            tip = uiUtils.getTextFromGMD(GMDD.data.SPRITE_AWAKE_NEED_FAMI_TIP, '')
            TipManager.addTip(lessFamiIcon, tip)
        else:
            lessFamiIcon.visible = False

    def setHotKeyText(self):
        mainMC = self.widget.mainMC
        p = BigWorld.player()
        if mainMC and mainMC.zhaoHuanMC:
            tipsMsg = gameStrings.SPRITE_TELEPORT_BACK_TIPS if p.inCombat else gameStrings.SPRITE_TELEPORT_BACK_NO_COMBAT_TIPS
            backTip = tipsMsg + gameStrings.TEXT_SUMMONEDSPRITEUNITFRAMEV2PROXY_183 % BigWorld.player().getSpriteTeleportHKDesc()
            TipManager.addTip(mainMC.zhaoHuanMC.teleportMC, backTip)
            mainMC.zhaoHuanMC.teleportMC.keyMC.textField.text = BigWorld.player().getSpriteTeleportHKBriefDesc()
            mainMC.zhaoHuanMC.manualSkillMC.keyMC.textField.text = BigWorld.player().getSpriteManualSkillHKBriefDesc()

    def resetZhaoHuan(self, zhaoHuan, summonedSprite = None):
        if not self.widget:
            return
        self.summonedSprite = summonedSprite
        if zhaoHuan:
            p = BigWorld.player()
            mainMC = self.widget.mainMC
            mainMC.gotoAndPlay('zhaohuan')
            self.initMPHPBar()
            self.initAwakeSkill()
            mainMC.zhaoHuanMC.modesMC.visible = False
            mainMC.zhaoHuanMC.manualSkillMC.activedMC.visible = False
            mainMC.zhaoHuanMC.teleportMC.activedMC.visible = False
            iconId = SSD.data.get(summonedSprite.spriteId, {}).get('icon', '111')
            iconPath = 'summonedSprite/icon/%s.dds' % str(iconId)
            mainMC.zhaoHuanMC.headMC.headIcon.fitSize = True
            mainMC.zhaoHuanMC.headMC.headIcon.loadImage(iconPath)
            mainMC.zhaoHuanMC.headMC.addEventListener(events.MOUSE_CLICK, self.summonSprite, False, 0, True)
            self.setHotKeyText()
            mainMC.zhaoHuanMC.teleportMC.addEventListener(events.MOUSE_CLICK, self.onTeleportClick, False, 0, True)
            mainMC.zhaoHuanMC.teleportMC.coolDown.textField.text = ''
            mainMC.zhaoHuanMC.manualSkillMC.coolDown.textField.text = ''
            mainMC.zhaoHuanMC.manualSkillMC.addEventListener(events.MOUSE_CLICK, self.onManualClick, False, 0, True)
            TipManager.addTip(mainMC.zhaoHuanMC.selectModeMC, gameStrings.SPRITE_SWITCH_MODE_TIPS)
            mainMC.zhaoHuanMC.selectModeMC.addEventListener(events.MOUSE_CLICK, self.onOpenModeClick, False, 0, True)
            mainMC.zhaoHuanMC.selectModeMC.overMC.visible = False
            self.updateSummonedSpriteInfo(summonedSprite)
            self.changeState(summonedSprite.mode)
            self.updateManualSkillCooldown()
        else:
            self.widget.mainMC.gotoAndPlay('weizhaohuan')
            self.widget.mainMC.weiZhaoHuanMC.addEventListener(events.MOUSE_CLICK, self.summonSprite, False, 0, True)
            self.refreshLastSpriteIcon()

    def refreshLastSpriteIcon(self):
        if not self.widget:
            return
        mc = self.widget.mainMC.weiZhaoHuanMC
        if not mc:
            return
        headIcon = mc.headMc.headIcon
        p = BigWorld.player()
        headIcon.fitSize = True
        headIcon.defaultIcon.visible = not p.lastSpriteBattleIndex
        iconPath = ''
        lastSpriteInfo = p.summonSpriteList.get(p.lastSpriteBattleIndex)
        if lastSpriteInfo:
            iconPath = uiUtils.getSummonSpriteIconPath(lastSpriteInfo.get('spriteId'))
            ASUtils.setMcEffect(mc.headMc, 'gray')
        else:
            ASUtils.setMcEffect(mc.headMc, '')
        headIcon.loadImage(iconPath)

    @ui.callFilter(2)
    def onTeleportClick(self, *args):
        BigWorld.player().spriteTeleportBack(True)

    def playTeleportActived(self):
        if not self.widget:
            return
        if not self.widget.mainMC.zhaoHuanMC:
            return
        self.widget.mainMC.zhaoHuanMC.teleportMC.activedMC.visible = True
        self.widget.mainMC.zhaoHuanMC.teleportMC.activedMC.gotoAndPlay(0)

    def onManualClick(self, *args):
        BigWorld.player().spriteUseManualSkill(True)

    def playManualSkillActived(self):
        if not self.widget:
            return
        if not self.widget.mainMC.zhaoHuanMC:
            return
        self.widget.mainMC.zhaoHuanMC.manualSkillMC.activedMC.visible = True
        self.widget.mainMC.zhaoHuanMC.manualSkillMC.activedMC.gotoAndPlay(0)

    def updateManualSkillCooldown(self):
        if not self.widget:
            return
        if not self.widget.mainMC.zhaoHuanMC:
            return
        nextTime = logicInfo.spriteManualSkillCoolDown
        if not nextTime:
            return
        now = utils.getNow()
        remainTime = nextTime - now
        if remainTime:
            awakeSkill = utils.getAwakeSkillBySprite()
            cd = SGD.data.get((awakeSkill, 10), {}).get('cd', 0)
            self.widget.mainMC.zhaoHuanMC.manualSkillMC.coolDown.playCooldown(cd * 1000, (cd - remainTime) * 1000)
            if self.awakeSkillCB:
                BigWorld.cancelCallback(self.awakeSkillCB)
            self.awakeSkillCB = BigWorld.callback(remainTime, self.clearAwakeCD)

    def clearAwakeCD(self):
        if not self.widget:
            return
        elif not self.widget.mainMC.zhaoHuanMC:
            return
        else:
            self.awakeSkillCB = None
            self.widget.mainMC.zhaoHuanMC.manualSkillMC.coolDown.stopCooldown()
            return

    def updateTeleportCooldown(self):
        if not self.widget:
            return
        if not self.widget.mainMC.zhaoHuanMC:
            return
        nextTime = logicInfo.spriteTeleportSkillCoolDown
        now = utils.getNow()
        remainTime = nextTime - now
        if nextTime and remainTime:
            cd = SGD.data.get((const.SSPRITE_BACK_SKILL_ID, const.DEFAULT_SKILL_LV_SPRITE), {}).get('cd', 0)
            self.widget.mainMC.zhaoHuanMC.teleportMC.coolDown.playCooldown(cd * 1000, (cd - remainTime) * 1000)
            if self.teleportCB:
                BigWorld.cancelCallback(self.teleportCB)
            self.teleportCB = BigWorld.callback(remainTime, self.clearTeleportCD)

    def clearTeleportCD(self):
        if not self.widget:
            return
        elif not self.widget.mainMC.zhaoHuanMC:
            return
        else:
            self.teleportCB = None
            self.widget.mainMC.zhaoHuanMC.teleportMC.coolDown.stopCooldown()
            return

    def summonSprite(self, *args):
        e = ASObject(args[3][0])
        if e.buttonIdx == uiConst.RIGHT_BUTTON:
            return
        if not gameglobal.rds.ui.summonedWarSprite.widget:
            gameglobal.rds.ui.summonedWarSprite.show(uiConst.WAR_SPRITE_TAB_INDEX0)

    def reset(self):
        self.summonedSprite = None

    def changeState(self, state):
        if not self.widget:
            return
        zhaoHuanMC = self.widget.mainMC.zhaoHuanMC
        if not zhaoHuanMC:
            return
        if state == gametypes.SP_MODE_COVER:
            zhaoHuanMC.selectModeMC.stateMC.innerMC.gotoAndPlay('zhudong')
            zhaoHuanMC.manualSkillMC.grayMC.visible = False
            zhaoHuanMC.teleportMC.huhuan.visible = True
        elif state == gametypes.SP_MODE_ASSIST:
            zhaoHuanMC.selectModeMC.stateMC.innerMC.gotoAndPlay('xiezuo')
            zhaoHuanMC.manualSkillMC.grayMC.visible = False
            zhaoHuanMC.teleportMC.huhuan.visible = True
        elif state == gametypes.SP_MODE_NOATK:
            zhaoHuanMC.selectModeMC.stateMC.innerMC.gotoAndPlay('beidong')
            zhaoHuanMC.manualSkillMC.grayMC.visible = True
            zhaoHuanMC.teleportMC.huhuan.visible = True

    def onOpenModeClick(self, *args):
        e = ASObject(args[3][0])
        e.stopImmediatePropagation()
        if not self.widget:
            return
        zhaoHuanMC = self.widget.mainMC.zhaoHuanMC
        if zhaoHuanMC:
            if zhaoHuanMC.modesMC.visible:
                self.onHideSelectMode()
                return
            zhaoHuanMC.modesMC.visible = True
            zhaoHuanMC.modesMC.zhuDongMC.stateMC.innerMC.gotoAndPlay('zhudong')
            zhaoHuanMC.modesMC.shouHuMC.stateMC.innerMC.gotoAndPlay('xiezuo')
            zhaoHuanMC.modesMC.beiDongMC.stateMC.innerMC.gotoAndPlay('beidong')
            zhaoHuanMC.modesMC.zhuDongMC.overMC.visible = False
            zhaoHuanMC.modesMC.shouHuMC.overMC.visible = False
            zhaoHuanMC.modesMC.beiDongMC.overMC.visible = False
            zhaoHuanMC.modesMC.zhuDongMC.addEventListener(events.MOUSE_CLICK, self.onSelectModeClick, False, 0, True)
            zhaoHuanMC.modesMC.shouHuMC.addEventListener(events.MOUSE_CLICK, self.onSelectModeClick, False, 0, True)
            zhaoHuanMC.modesMC.beiDongMC.addEventListener(events.MOUSE_CLICK, self.onSelectModeClick, False, 0, True)
            self.widget.stage.addEventListener(events.MOUSE_CLICK, self.onHideSelectMode)
            zhaoHuanMC.modesMC.zhuDongMC.addEventListener(events.MOUSE_OVER, self.onModeOver, False, 0, True)
            zhaoHuanMC.modesMC.shouHuMC.addEventListener(events.MOUSE_OVER, self.onModeOver, False, 0, True)
            zhaoHuanMC.modesMC.beiDongMC.addEventListener(events.MOUSE_OVER, self.onModeOver, False, 0, True)
            zhaoHuanMC.modesMC.zhuDongMC.addEventListener(events.MOUSE_OUT, self.onModeOut, False, 0, True)
            zhaoHuanMC.modesMC.shouHuMC.addEventListener(events.MOUSE_OUT, self.onModeOut, False, 0, True)
            zhaoHuanMC.modesMC.beiDongMC.addEventListener(events.MOUSE_OUT, self.onModeOut, False, 0, True)
            TipManager.addTip(zhaoHuanMC.modesMC.zhuDongMC, uiUtils.getTextFromGMD(GMDD.data.SPRITE_MODE_ZHU_DONG, gameStrings.SPRITE_MODE_ZHU_DONG))
            TipManager.addTip(zhaoHuanMC.modesMC.shouHuMC, uiUtils.getTextFromGMD(GMDD.data.SPRITE_MODE_SHOUHU, gameStrings.SPRITE_MODE_SHOUHU))
            TipManager.addTip(zhaoHuanMC.modesMC.beiDongMC, uiUtils.getTextFromGMD(GMDD.data.SPRITE_MODE_BEIDONG, gameStrings.SPRITE_MODE_BEIDONG))

    def onHideSelectMode(self, *args):
        self.widget.stage.removeEventListener(events.MOUSE_CLICK, self.onHideSelectMode)
        if self.widget.mainMC.zhaoHuanMC:
            self.widget.mainMC.zhaoHuanMC.modesMC.visible = False

    def onSelectModeClick(self, *args):
        e = ASObject(args[3][0])
        if not self.widget:
            return
        p = BigWorld.player()
        if e.currentTarget.name == 'zhuDongMC':
            p.base.setSpriteMode(gametypes.SP_MODE_COVER)
        elif e.currentTarget.name == 'shouHuMC':
            p.base.setSpriteMode(gametypes.SP_MODE_ASSIST)
        elif e.currentTarget.name == 'beiDongMC':
            p.base.setSpriteMode(gametypes.SP_MODE_NOATK)
        if self.widget.mainMC.zhaoHuanMC:
            self.widget.mainMC.zhaoHuanMC.modesMC.visible = False

    def onModeOver(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.overMC.visible = True

    def onModeOut(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.overMC.visible = False

    def updateCombat(self, inCombat):
        if not self.widget:
            return
        zhaoHuanMC = self.widget.mainMC.zhaoHuanMC
        if not zhaoHuanMC:
            return
        zhaoHuanMC.teleportMC.huhuan.visible = not inCombat
        p = BigWorld.player()
        tipsMsg = gameStrings.SPRITE_TELEPORT_BACK_TIPS if p.inCombat else gameStrings.SPRITE_TELEPORT_BACK_NO_COMBAT_TIPS
        backTip = tipsMsg + gameStrings.TEXT_SUMMONEDSPRITEUNITFRAMEV2PROXY_183 % BigWorld.player().getSpriteTeleportHKDesc()
        TipManager.addTip(zhaoHuanMC.teleportMC, backTip)
