#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/skillPushProxy.o
import gameglobal
import skillDataInfo
from guis import uiConst
from guis import uiUtils
from uiProxy import SlotDataProxy
from data import skill_general_template_data as SGTD
from data import sys_config_data as SCD

class SkillPushProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(SkillPushProxy, self).__init__(uiAdapter)
        self.modelMap = {'getPushSkills': self.onGetPushSkills,
         'autoEquip': self.autoEquipSkill}
        self.mediator = None
        self.skillId = 0
        self.cacheSkillId = []

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SKILL_PUSH:
            self.mediator = mediator

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SKILL_PUSH)

    def clearWidget(self):
        self.mediator = None
        self.skillId = 0
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SKILL_PUSH)
        if len(self.cacheSkillId) > 0:
            self.showCacheNewSkill()

    def _getSkillIcon(self, skillId, level = 1):
        sd = skillDataInfo.ClientSkillInfo(skillId, level)
        icon = sd.getSkillData('icon', 'notFound')
        if icon != None:
            return 'skill/icon/' + str(icon) + '.dds'
        else:
            return

    def setSkillData(self, skillId, isWs):
        if gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
            if skillId not in self.cacheSkillId:
                self.cacheSkillId.append(skillId)
            return
        if SGTD.data.get(skillId, {}).get('unShowPush', 0) or isWs:
            return
        oldSkillId = self.skillId
        self.skillId = skillId
        if self.mediator:
            if oldSkillId != 0:
                gameglobal.rds.ui.actionbar.addNewSkill(oldSkillId)
            self.refresh()
        else:
            self.show()

    def refresh(self):
        obj = self._getSkillsObj()
        if self.mediator:
            self.mediator.Invoke('setPushSkill', obj)

    def _getSkillsObj(self):
        if self.skillId == 0:
            return
        data = {}
        path = self._getSkillIcon(self.skillId)
        data['skillId'] = self.skillId
        data['iconPath'] = path
        data['skillPushTime'] = SCD.data.get('skillPushTime', 5)
        obj = uiUtils.dict2GfxDict(data)
        return obj

    def onGetPushSkills(self, *arg):
        obj = self._getSkillsObj()
        return obj

    def autoEquipSkill(self, *arg):
        skillId = int(arg[3][0].GetNumber())
        self.hide()
        if skillId == 0:
            return
        gameglobal.rds.ui.actionbar.addNewSkill(skillId)

    def showCacheNewSkill(self):
        if len(self.cacheSkillId) > 0:
            skillId = self.cacheSkillId.pop(0)
            self.setSkillData(skillId, False)
