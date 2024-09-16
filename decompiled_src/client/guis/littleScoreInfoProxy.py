#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/littleScoreInfoProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import uiUtils
import utils
import uiConst
import events
import gameglobal
import const
from uiProxy import UIProxy
from guis.asObject import TipManager
from guis.asObject import ASUtils
from data import duel_config_data as DCD
from data import sys_config_data as SCD
from data import battle_field_data as BFD

class LittleScoreInfoProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(LittleScoreInfoProxy, self).__init__(uiAdapter)
        self._resetData()

    def _resetData(self):
        self.widget = None
        self.protecterScoreAdd = False
        self.oldProtecterScore = 0
        self.protecterScore = 0
        self.spriteScoreAdd = False
        self.oldSpriteScore = 0
        self.spriteScore = 0
        self.candyAdd = False
        self.oldCandyCount = 0
        self.candyCount = 0
        self.timer = None
        self.quitTime = None
        self.spriteWinScore = 0

    def _registerASWidget(self, widgetId, widget):
        self.setOtherWidgetVisible(False)
        self.widget = widget
        self._initUI()
        self.refreshFrame()

    def setOtherWidgetVisible(self, visible):
        if gameglobal.rds.ui.actionbar.mc:
            gameglobal.rds.ui.actionbar.mc.Invoke('setVisible', GfxValue(visible))
        if gameglobal.rds.ui.actionbar.wsMc:
            gameglobal.rds.ui.actionbar.wsMc.Invoke('setVisible', GfxValue(visible))
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_ACTION_BARS, visible)
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_WUSHUANG_BARS, visible)
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_ITEMBAR, visible)
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_ITEMBAR2, visible)
        gameglobal.rds.ui.bullet.setVisible(visible)
        if gameglobal.rds.ui.qinggongBar.thisMc:
            gameglobal.rds.ui.qinggongBar.thisMc.SetVisible(visible)
        if visible:
            self.uiAdapter.actionbar.setSchoolCenter()

    def _getFrameInfo(self):
        p = BigWorld.player()
        self.protecterScore, self.spriteScore = self.getTotalScore()
        self.protecterScoreAdd = self.oldProtecterScore < self.protecterScore
        self.spriteScoreAdd = self.oldSpriteScore < self.spriteScore
        self.candyCount = getattr(p, 'currentCandyCnt', 0)
        self.candyAdd = self.oldCandyCount < self.candyCount
        self.oldProtecterScore = self.protecterScore
        self.oldSpriteScore = self.spriteScore
        self.oldCandyCount = self.candyCount
        winResLimit = BFD.data.get(p.mapID, {}).get('winResLimit', 0)
        self.protecterWinScore = winResLimit
        self.spriteWinScore = winResLimit

    def getTotalScore(self):
        p = BigWorld.player()
        if p.bfSideIndex == const.BATTLE_FIELD_HUNT_PROTECT_SIDE_INDEX:
            protecterScore = p.getMyRes()
            spriteScore = p.getEnemyRes()
        else:
            protecterScore = p.getEnemyRes()
            spriteScore = p.getMyRes()
        return (protecterScore, spriteScore)

    def show(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_LITTLE_SCORE_INFO)

    def clearWidget(self):
        self.setOtherWidgetVisible(True)
        self._resetData()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_LITTLE_SCORE_INFO)

    def _addTick(self):
        if not self.timer:
            self._updateTick()

    def _updateTick(self):
        p = BigWorld.player()
        if not self.widget:
            if self.timer:
                BigWorld.cancelCallback(self.timer)
                self.timer = None
            return
        else:
            if self.quitTime == None:
                tReady = p.bfTimeRec.get('tReady', 0)
                duration = BFD.data.get(p.getBattleFieldFbNo(), {}).get('durationTime', 1800)
                self.quitTime = tReady + duration
            left = self.quitTime - utils.getNow()
            left = max(0, left)
            self.checkRange()
            self.widget.countDown.text = utils.formatTimeStr(left, 'm:s', sNum=2, mNum=2, zeroShow=True)
            self.timer = BigWorld.callback(1, self._updateTick)
            return

    def setQuitTime(self, quitTime):
        self.quitTime = quitTime

    def refreshFrame(self):
        if not self.widget:
            return
        self._getFrameInfo()
        self.widget.candyCnt.text = str(self.candyCount)
        self.widget.sprite.currentValue = self.spriteScore
        self.widget.sprite.maxValue = self.spriteWinScore
        self.widget.protecter.currentValue = self.protecterScore
        self.widget.protecter.maxValue = self.protecterWinScore
        self.widget.protecterScore.text = '%d/%d' % (self.protecterScore, self.protecterWinScore)
        self.widget.spriteScore.text = '%d/%d' % (self.spriteScore, self.spriteWinScore)
        self.refreshEff()
        self._addTick()

    def refreshEff(self):
        p = BigWorld.player()
        if self.protecterScoreAdd and p.bfSideIndex == const.BATTLE_FIELD_HUNT_PROTECT_SIDE_INDEX:
            self.widget.addScoreEff0.visible = True
            self.widget.addScoreEff0.gotoAndPlay(1)
        if self.spriteScoreAdd and p.bfSideIndex != const.BATTLE_FIELD_HUNT_PROTECT_SIDE_INDEX:
            self.widget.addScoreEff1.visible = True
            self.widget.addScoreEff1.gotoAndPlay(1)
        if self.candyAdd:
            self.widget.addCandyEff.visible = True
            self.widget.addCandyEff.gotoAndPlay(1)
            soundId = SCD.data.get('HUNT_SOUND_CANDY_ADD', 5110)
            gameglobal.rds.sound.playSound(soundId, position=p.position)

    def scoreChange(self, spriteScore, protecterScore):
        self.spriteScore = spriteScore
        self.protecterScore = protecterScore
        self.refreshFrame()

    def _initUI(self):
        self.chooseVehicleRange = DCD.data.get('huntChooseVehicleRange', {}).get(BigWorld.player().bfSideIndex, ())
        self.widget.addScoreEff0.visible = False
        self.widget.addScoreEff1.visible = False
        self.widget.addCandyEff.visible = False
        if BigWorld.player().bfSideIndex == const.BATTLE_FIELD_HUNT_PROTECT_SIDE_INDEX:
            self.widget.item.gotoAndStop('vs')
            TipManager.removeTip(self.widget.item)
            self.widget.candyCnt.visible = False
        else:
            self.widget.item.gotoAndStop('item')
            giftId = DCD.data.get('itemCandyId', 0)
            TipManager.addItemTipById(self.widget.item, giftId)
            self.widget.candyCnt.visible = True
        ASUtils.setHitTestDisable(self.widget.addScoreEff0, True)
        ASUtils.setHitTestDisable(self.widget.addScoreEff1, True)
        ASUtils.setHitTestDisable(self.widget.addCandyEff, True)
        ASUtils.setHitTestDisable(self.widget.candyCnt, True)
        ASUtils.setHitTestDisable(self.widget.spriteScore, True)
        ASUtils.setHitTestDisable(self.widget.protecterScore, True)
        TipManager.addTip(self.widget.spriteIcon, DCD.data.get('side_tips', {}).get(1, gameStrings.TEXT_LITTLESCOREINFOPROXY_182))
        TipManager.addTip(self.widget.protecterIcon, DCD.data.get('side_tips', {}).get(0, gameStrings.TEXT_LITTLESCOREINFOPROXY_183))
        self.widget.detailBtn.addEventListener(events.MOUSE_CLICK, self.onDetailClick, False, 0, True)
        self.widget.changeSkillBtn.addEventListener(events.MOUSE_CLICK, self.onChangeSkillClick, False, 0, True)

    def onChangeSkillClick(self, *args):
        self.uiAdapter.vehicleChoose.show(False)

    def onDetailClick(self, *args):
        self.uiAdapter.scoreInfo.show()

    def onCloseClick(self, *args):
        self.hide()

    def checkRange(self):
        if not self.chooseVehicleRange:
            return
        pos = BigWorld.player().position
        if pos[0] > self.chooseVehicleRange[0][0] and pos[0] < self.chooseVehicleRange[1][0] and pos[2] > self.chooseVehicleRange[0][1] and pos[2] < self.chooseVehicleRange[1][1]:
            self.widget.changeSkillBtn.enabled = True
            self.uiAdapter.vehicleChoose.tryOpen()
        else:
            self.widget.changeSkillBtn.enabled = False
