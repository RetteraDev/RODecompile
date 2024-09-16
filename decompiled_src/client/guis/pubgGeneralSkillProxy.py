#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pubgGeneralSkillProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import gamelog
import logicInfo
from guis import tipUtils
from uiProxy import UIProxy
from guis import skillInfoManager
from guis.asObject import ASObject
from Scaleform import GfxValue
from guis.asObject import TipManager
from data import sys_config_data as SCD

class PubgGeneralSkillProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PubgGeneralSkillProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_PUBG_GENERAL_SKILL_WIDGET, self.hide)

    def reset(self):
        self.widget = None
        self.skillInfoManager = skillInfoManager.getInstance()
        self.binding = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PUBG_GENERAL_SKILL_WIDGET:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PUBG_GENERAL_SKILL_WIDGET)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_PUBG_GENERAL_SKILL_WIDGET)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        if not p.pubgSkills:
            return
        maxSkillNum = SCD.data.get('pubgMaxLearnSkillNum', 10)
        i = 0
        for skillId in p.pubgSkills.iterkeys():
            if i < maxSkillNum - 1:
                skillItemInfo = self.skillInfoManager.commonSkillIns.getSkillItemInfo(skillId)
                skillItem = self.widget.getChildByName('skill%d' % i)
                skillItem.setItemSlotData(skillItemInfo.get('icon'))
                skillItem.binding = 'skills22.%d' % skillId
                TipManager.addTipByType(skillItem, tipUtils.TYPE_SKILL, {'skillId': skillId,
                 'lv': skillItemInfo.get('skillLv')})
                self.binding[skillId] = skillItem
                i += 1
                self.refreshSkillSlot(skillId)

    def handleSlotClick(self, *args):
        e = ASObject(args[3][0])
        key = e.currentTarget.binding
        _, skillId = key.split('.')
        p = BigWorld.player()
        if p.checkCanUsePubgSkill(int(skillId)):
            tgtId = p.targetLocked.id if p.targetLocked and p.targetLocked.id else p.id
            p.cell.usePubgSkill(int(skillId), tgtId)

    def refreshSkillSlot(self, skillId):
        if not self.widget:
            return
        skillSlot = self.binding[skillId]
        total = remain = 0
        if skillId in logicInfo.cooldownSkill:
            end, total = logicInfo.cooldownSkill[skillId]
            remain = end - BigWorld.time()
        skillSlot.playCooldown(GfxValue(total * 1000), GfxValue((total - remain) * 1000))
