#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/skillGuideProxy.o
import BigWorld
import gameglobal
import skillInfoManager
from guis import uiUtils
from guis import uiConst
from uiProxy import SlotDataProxy
from data import skill_guide_data as SGD
from data import skill_panel_data as SPD
from data import skill_general_template_data as SGTD

class SkillGuideProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(SkillGuideProxy, self).__init__(uiAdapter)
        self.modelMap = {'getCurrnetSkillInfo': self.onGetCurrnetSkillInfo,
         'getNormalSkills': self.onGetNormalSkills,
         'getSkillInfo': self.onGetSkillInfo,
         'getInitInfo': self.onGetInitInfo}
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SKILL_GUIDE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SKILL_GUIDE:
            self.mediator = mediator

    def show(self, skillId = 0, type = 1):
        p = BigWorld.player()
        if getattr(p, 'isStraightLvUp', False):
            return
        if skillId != 0:
            if SGTD.data.get(skillId, {}).get('unShowPush', 0):
                return
            self.skillId = skillId
        self.type = type
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SKILL_GUIDE)

    def close(self):
        self.clearWidget()

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SKILL_GUIDE)

    def reset(self):
        self.mediator = None
        self.skillList = []
        self.currentSkillId = None
        self.binding = {}
        self.bindType = 'skills'
        self.skillId = 0
        self.type = 0
        self.firstIndex = 0
        self.skillInfoManager = skillInfoManager.getInstance()

    def onGetInitInfo(self, *args):
        ret = {}
        ret['skillId'] = self.skillId
        ret['firstIndex'] = self.firstIndex
        return uiUtils.dict2GfxDict(ret, True)

    def onGetCurrnetSkillInfo(self, *args):
        ret = {}
        self.currentSkillId = int(args[3][0].GetNumber())
        skillData = SGD.data.get(self.currentSkillId, {})
        tab0 = {'content': []}
        tab1 = {'content': []}
        tab2 = {'content': []}
        tab0['name'] = skillData.get('tabName1', '')
        tab1['name'] = skillData.get('tabName2', '')
        tab2['name'] = skillData.get('tabName3', '')
        for i in xrange(10):
            keys = skillData.keys()
            key1 = 'skillPoint' + str(i)
            if key1 in keys:
                tab0['content'].append(skillData.get(key1, ''))
            key2 = 'seriesSkillLabel' + str(i)
            key3 = 'seriesSkillDesc' + str(i)
            key4 = 'seriesSkillIcons' + str(i)
            if key2 in keys and key3 in keys:
                if key4 in keys:
                    tab1['content'].append({'seriesSkillLabel': skillData.get(key2, ''),
                     'seriesSkillDesc': skillData.get(key3, ''),
                     'icons': skillData.get(key4, [])})
                else:
                    tab1['content'].append({'seriesSkillLabel': skillData.get(key2, ''),
                     'seriesSkillDesc': skillData.get(key3, '')})
            key5 = 'coreSkillIcon' + str(i)
            key6 = 'coreSkillDesc' + str(i)
            if key5 in keys and key6 in keys:
                tab2['content'].append({'coreSkillIcon': skillData.get(key5, ''),
                 'coreSkillDesc': skillData.get(key6, '')})
            key7 = 'coreSkillWsTitle' + str(i)
            key8 = 'coreSkillWsDesc' + str(i)
            if key7 in keys and key8 in keys:
                tab2['content'].append({'coreSkillWsTitle': skillData.get(key7, ''),
                 'coreSkillWsDesc': skillData.get(key8, '')})

        ret['tab0'] = tab0
        ret['tab1'] = tab1
        ret['tab2'] = tab2
        return uiUtils.dict2GfxDict(ret, True)

    def onGetNormalSkills(self, *arg):
        skillInfo = []
        p = BigWorld.player()
        commonSkillList = SPD.data.get(p.school, {}).get('wsType1Skills', []) + SPD.data.get(p.school, {}).get('wsType2Skills', [])
        WSSkillList = SPD.data.get(p.school, {}).get('wsType1SpecialSkills', []) + SPD.data.get(p.school, {}).get('wsType2SpecialSkills', [])
        self.skillList = commonSkillList + WSSkillList
        for index, skillId in enumerate(self.skillList):
            item = self.skillInfoManager.commonSkillIns.getSkillItemInfo(skillId)
            item['type'] = SGD.data.get(skillId, {}).get('type', 1)
            item['index'] = index
            skillInfo.append(item)

        if self.type == 1:
            self.firstIndex = 0
        else:
            self.firstIndex = len(commonSkillList)
        return uiUtils.array2GfxAarry(skillInfo, True)

    def onGetSkillInfo(self, *args):
        skillId = int(args[3][0].GetNumber())
        info = self.skillInfoManager.commonSkillIns.getSkillItemInfo(skillId)
        info['type'] = SGD.data.get(skillId, {}).get('type', 1)
        return uiUtils.dict2GfxDict(info, True)
