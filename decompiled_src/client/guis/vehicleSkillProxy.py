#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/vehicleSkillProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import events
import gametypes
from uiProxy import UIProxy
from guis import hotkeyProxy
from guis.asObject import ASUtils
from guis.asObject import ASObject
from data import zaiju_data as ZD
from data import duel_config_data as DCD
OFFSET_SKILL_BG = 1
OFFSET_TIP_MC = -84
SKILL_MAX_COUNT = 3

class VehicleSkillProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(VehicleSkillProxy, self).__init__(uiAdapter)
        self._resetData()

    def _resetData(self):
        self.widget = None
        self.trapState = uiConst.TRAP_STATE_NORMAL
        self.zaijuId = None
        self.skillMcList = []
        self.skillDataList = []
        self.skillTrapId = DCD.data.get('skillTrapId', 0)
        self.keyArr = []
        self.useSelfSkill = False
        self.trapDisappearTime = DCD.data.get('trapDisappearTime', 5)
        self.trapTimer = 0
        self.trapShowTime = DCD.data.get('TRAP_EFF_SHOW_TIME', 60)
        self.trapShowTimer = 0

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self._initUI()
        self.refreshFrame()

    def show(self, trapState = 0):
        self.trapState = trapState
        self.uiAdapter.loadWidget(uiConst.WIDGET_VEHICLE_SKILL)

    def hideOtherWidget(self):
        if gameglobal.rds.ui.actionbar.mc:
            gameglobal.rds.ui.actionbar.mc.Invoke('setVisible', GfxValue(False))
        if gameglobal.rds.ui.actionbar.wsMc:
            gameglobal.rds.ui.actionbar.wsMc.Invoke('setVisible', GfxValue(False))
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_ACTION_BARS, False)
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_WUSHUANG_BARS, False)
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_ITEMBAR, False)
        gameglobal.rds.ui.bullet.setVisible(False)
        if gameglobal.rds.ui.qinggongBar.thisMc:
            gameglobal.rds.ui.qinggongBar.thisMc.SetVisible(False)

    def clearWidget(self):
        self.clearTimer()
        self._resetData()
        self.uiAdapter.zaiju.binding = {}
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_VEHICLE_SKILL)

    def _getFrameInfo(self):
        p = BigWorld.player()
        bianshen = p.bianshen
        if not bianshen:
            return
        if bianshen[0] == gametypes.BIANSHEN_ZAIJU:
            self.zaijuId = bianshen[1]
            zaijuData = ZD.data.get(self.zaijuId, {})
            self.skillDataList = []
            skills = zaijuData.get('skills', [])
            for skillId, skillLv in skills:
                skillData = {}
                skillData['id'] = skillId
                skillData['lv'] = skillLv
                self.skillDataList.append(skillData)

        self.keyArr = hotkeyProxy.getInstance().shortKey.getKeyDescArray()[0:SKILL_MAX_COUNT]

    def refreshFrame(self, trapState = None):
        if not self.widget:
            return
        self.hideOtherWidget()
        if trapState:
            self.trapState = trapState
        for item in self.skillMcList:
            item.visible = False

        self._getFrameInfo()
        self.widget.tipMc.visible = False
        self.widget.skillItemBg.visible = False
        for i in range(len(self.skillDataList)):
            if i >= SKILL_MAX_COUNT:
                break
            skillData = self.skillDataList[i]
            mc = self.skillMcList[i]
            self.showTrapState(mc, skillData)

        for i in xrange(SKILL_MAX_COUNT):
            self.skillMcList[i].visible = True
            self.skillMcList[i].binding = ''
            self.skillMcList[i].binding = 'zaiju.slot%d' % i
            self.skillMcList[i].keyBind.text = self.keyArr[i]
            self.skillMcList[i].validateNow()

    def clearTimer(self):
        if self.trapTimer:
            BigWorld.cancelCallback(self.trapTimer)
            self.trapTimer = 0
        if self.trapShowTimer:
            BigWorld.cancelCallback(self.trapShowTimer)
            self.trapShowTimer = 0

    def showTrapState(self, skillMc, skillData):
        if skillData['id'] != self.skillTrapId:
            return
        if self.trapState == uiConst.TRAP_STATE_NORMAL:
            self.widget.tipMc.visible = False
            self.widget.skillItemBg.visible = False
            self.clearTimer()
        elif self.trapState == uiConst.TRAP_STATE_TRIGGER:
            self.widget.tipMc.visible = True
            self.widget.skillItemBg.visible = True
            self.widget.tipMc.gotoAndPlay('trapCatch')
            self.widget.tipMc.x = skillMc.x + OFFSET_TIP_MC
            self.widget.skillItemBg.x = skillMc.x + OFFSET_SKILL_BG
            self.clearTimer()
            self.trapShowTimer = BigWorld.callback(self.trapShowTime, self.delayDisapperaTrap)
        elif self.trapState == uiConst.TRAP_STATE_BROKEN:
            self.widget.tipMc.visible = True
            self.widget.skillItemBg.visible = True
            self.widget.tipMc.gotoAndPlay('trapBroken')
            self.widget.tipMc.x = skillMc.x + OFFSET_TIP_MC
            self.widget.skillItemBg.x = skillMc.x + OFFSET_SKILL_BG
            self.clearTimer()
            self.trapTimer = BigWorld.callback(self.trapDisappearTime, self.delayDisapperaTrap)

    def delayDisapperaTrap(self):
        self.widget.tipMc.visible = False
        self.widget.skillItemBg.visible = False
        self.trapTimer = 0

    def _initUI(self):
        for i in range(SKILL_MAX_COUNT):
            skillItem = self.widget.getChildByName('skill%d' % i)
            ASUtils.setMcData(skillItem, 'skillId', 0)
            skillItem.addEventListener(events.MOUSE_CLICK, self.onSkillClick, False, 0, True)
            self.skillMcList.append(skillItem)
            skillItem.visible = False

        self.widget.tipMc.visible = False
        self.widget.skillItemBg.visible = False

    def onSkillClick(self, *args):
        e = ASObject(args[3][0])
        binding = e.currentTarget.binding
        idCon, idItem = binding.split('.')
        slot = idItem[4:]
        slotIndex = int(slot)
        if slotIndex >= len(self.skillDataList):
            return
        self.uiAdapter.zaiju.useSkill(0, slotIndex, True)

    def onCloseClick(self, *args):
        self.hide()

    def _getSkillInfo(self, skillId):
        curLv = 1
        sVal = BigWorld.player().getSkills().get(skillId, None)
        if sVal:
            curLv = sVal.level
        skillInfo = BigWorld.player().getSkillInfo(skillId, curLv)
        return skillInfo
