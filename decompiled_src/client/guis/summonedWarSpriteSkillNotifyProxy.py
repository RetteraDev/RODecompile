#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteSkillNotifyProxy.o
import BigWorld
import uiConst
import skillDataInfo
import tipUtils
import ui
import gametypes
import gameglobal
from callbackHelper import Functor
from guis import uiUtils
from uiProxy import UIProxy
from guis.asObject import TipManager
from data import skill_general_data as SGD
from data import sys_config_data as SCD
from data import summon_sprite_skill_data as SSSD

class SummonedWarSpriteSkillNotifyProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteSkillNotifyProxy, self).__init__(uiAdapter)
        self.reset()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SPRITE_GET_SKILL_NOTIFY:
            skillData = self.skillDataList.pop(0)
            self.initUI(widget.multiID, widget, skillData)

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SPRITE_GET_SKILL_NOTIFY)

    def reset(self):
        self.skillDataList = []
        self.skillWidDict = {}

    def show(self, spriteIndex, skillId):
        self.skillDataList.insert(0, (spriteIndex, skillId))
        self.uiAdapter.loadWidget(uiConst.WIDGET_SPRITE_GET_SKILL_NOTIFY)

    def initUI(self, widgetId, widget, skillData):
        p = BigWorld.player()
        spriteIdx, spriteSkillId = skillData
        spriteInfo = p.summonSpriteList.get(spriteIdx)
        if not spriteInfo:
            self.hideNotify(widgetId)
        self.skillWidDict[skillData] = widgetId
        widget.defaultCloseBtn = widget.closeBtn
        widget.title.textField.htmlText = SCD.data.get('spriteSkillNotifyTitle', '%s') % spriteInfo.get('name', '')
        skillId = SSSD.data.get(spriteSkillId, {}).get('virtualSkill', 0)
        widget.detailBtn.data = widget.forgetBtn.data = (spriteIdx, spriteSkillId, skillId)
        skillInfo = skillDataInfo.ClientSkillInfo(skillId)
        iconPath = uiUtils.getSkillIconPath(skillInfo, uiConst.ICON_SIZE64)
        widget.skillSlot.fitSize = True
        widget.skillSlot.dragable = False
        widget.skillSlot.setItemSlotData({'iconPath': iconPath})
        widget.skillDesc.skillName.htmlText = skillInfo.getSkillData('qualityName', '')
        widget.skillDesc.skillType.text = skillInfo.getSkillData('skillShortDesc', 'skillShortDesc')
        widget.skillSlot.validateNow()
        TipManager.addTipByType(widget.skillSlot, tipUtils.TYPE_SKILL, skillId)

    def _asWidgetClose(self, widgetId, multiID):
        self.hideNotify(multiID)

    def hideNotify(self, wid):
        self.uiAdapter.unLoadWidget(wid)

    def _onForgetBtnClick(self, e):
        spriteIdx, spriteSkillId, skillId = e.target.data
        wid = self.skillWidDict.get((spriteIdx, spriteSkillId), 0)
        self.hideNotify(wid)
        skillInfo = skillDataInfo.ClientSkillInfo(skillId)
        skillName = skillInfo.getSkillData('sname', '')
        slotIdx = self.getSlotIdx(spriteIdx, spriteSkillId)
        if slotIdx == -1:
            return
        gameglobal.rds.ui.summonedWarSpriteForgetSkill.show(spriteIdx, slotIdx, skillName)

    def _onDetailBtnClick(self, e):
        spriteIdx, spriteSkillId, skillId = e.target.data
        wid = self.skillWidDict.get((spriteIdx, spriteSkillId), 0)
        self.hideNotify(wid)
        self.uiAdapter.summonedWarSprite.show(0)
        self.showSpriteSkill(spriteIdx, skillId)

    def getSlotIdx(self, spriteIdx, spriteSkillId):
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(spriteIdx, {})
        learnSkills = spriteInfo.get('skills', {}).get('learns', [])
        for info in learnSkills:
            if info.get('id') == spriteSkillId:
                return info.get('part', 0)

        return -1

    @ui.checkWidgetLoaded(uiConst.WIDGET_SUMMONED_WAR_SPRITE)
    @ui.callAfterTime(0.1)
    def showSpriteSkill(self, spriteIdx, skillId):
        self.uiAdapter.summonedWarSpriteMine.setSpriteSelected(spriteIdx, 'skillTabBtn')
        self.uiAdapter.summonedWarSpriteMine.skillProxy.setSkillSelected(skillId)
