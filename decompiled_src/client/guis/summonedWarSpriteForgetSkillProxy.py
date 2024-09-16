#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteForgetSkillProxy.o
import BigWorld
import uiConst
import ui
import gametypes
import const
from uiProxy import UIProxy
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD

class SummonedWarSpriteForgetSkillProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteForgetSkillProxy, self).__init__(uiAdapter)
        self.widget = None
        self.selectedIndex = 0
        self.slotIdx = 0
        self.skillName = ''
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_WAR_SPRITE_FORGET_SKILL, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_WAR_SPRITE_FORGET_SKILL:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_FORGET_SKILL)

    def reset(self):
        self.selectedIndex = 0
        self.slotIdx = 0
        self.skillName = ''

    def show(self, selectedIndex, slotIdx, skillName):
        self.selectedIndex = selectedIndex
        self.slotIdx = slotIdx
        self.skillName = skillName
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_FORGET_SKILL, True)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.radioBtn0.selected = True
        self.widget.radioBtn1.selected = False

    def refreshInfo(self):
        if not self.widget:
            return
        forgetSkillDesc = SCD.data.get('forgetSpriteSkillCashDesc', '%s') % self.skillName
        needCash = SCD.data.get('forgetSpriteSkillSpendCash', 0)
        needYunChui = SCD.data.get('forgetSpriteSkillSpendYunchuiScore', 0)
        self.widget.descTF.htmlText = forgetSkillDesc
        self.widget.cashValT.text = needCash
        self.widget.expValT.text = needYunChui

    @ui.checkInventoryLock()
    def _onConfirmBtnClick(self, e):
        if not self.widget:
            return
        p = BigWorld.player()
        payType = 0
        if self.widget.radioBtn0.selected:
            needCash = SCD.data.get('forgetSpriteSkillSpendCash', 0)
            if needCash > p.bindCash + p.cash:
                p.showGameMsg(GMDD.data.NOT_ENOUGH_CASH, ())
                return
            payType = gametypes.SPRITE_COST_TYPE_BIND_CASH
        elif self.widget.radioBtn1.selected:
            needYunChui = SCD.data.get('forgetSpriteSkillSpendYunchuiScore', 0)
            myYunChui = p.getFame(const.YUN_CHUI_JI_FEN_FAME_ID)
            if needYunChui > myYunChui:
                p.showGameMsg(GMDD.data.NOT_ENOUGH_YUNCHUI_SCORE, ())
                return
            payType = gametypes.SPRITE_COST_TYPE_YUNCHUI_SCORE
        p.base.forgetSpriteLearn(self.selectedIndex, self.slotIdx, p.cipherOfPerson, payType)
        self.hide()

    def _onCancelBtnClick(self, e):
        self.hide()
