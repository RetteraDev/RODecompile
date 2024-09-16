#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/yaoPeiLvUpProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import uiUtils
import const
from uiProxy import SlotDataProxy
from data import prop_ref_data as PRD
from data import skill_general_template_data as SGTD

class YaoPeiLvUpProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(YaoPeiLvUpProxy, self).__init__(uiAdapter)
        self.bindType = 'yaoPeiLvUp'
        self.type = 'yaoPeiLvUp'
        self.modelMap = {}
        self.mediator = None
        self.oldLv = 0
        self.lvUpItem = None
        self.location = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_YAOPEI_LVUP, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_YAOPEI_LVUP:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_YAOPEI_LVUP)

    def reset(self):
        self.oldLv = 0
        self.lvUpItem = None
        self.location = None

    def show(self, oldLv, lvUpItem, lvUpItemInBag):
        if not lvUpItem:
            return
        self.oldLv = oldLv
        self.lvUpItem = lvUpItem
        self.location = const.ITEM_IN_BAG if lvUpItemInBag else const.ITEM_IN_EQUIPMENT
        if self.mediator:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_YAOPEI_LVUP, isModal=True)

    def refreshInfo(self):
        if self.mediator:
            info = {}
            info['itemInfo'] = uiUtils.getGfxItem(self.lvUpItem, location=self.location)
            info['oldLv'] = 'Lv.%d' % self.oldLv
            oldBasicAdd, oldExtraAdd, oldSkillLv = self.lvUpItem.getYaoPeiPropsAdd(self.oldLv)
            newLv = self.lvUpItem.getYaoPeiLv()
            info['newLv'] = 'Lv.%d' % newLv
            newBasicAdd, newExtraAdd, newSkillLv = self.lvUpItem.getYaoPeiPropsAdd(newLv)
            propList = []
            propActivateList = []
            if hasattr(self.lvUpItem, 'yaoPeiProps'):
                for prop in self.lvUpItem.yaoPeiProps:
                    propInfo = self.createPropInfo(prop[0], prop[1], prop[2], oldBasicAdd, newBasicAdd)
                    propList.append(propInfo)

            if hasattr(self.lvUpItem, 'rprops'):
                for prop in self.lvUpItem.rprops:
                    propInfo = self.createPropInfo(prop[0], prop[1], prop[2], oldExtraAdd, newExtraAdd)
                    propList.append(propInfo)

            if hasattr(self.lvUpItem, 'yaoPeiExtraProps'):
                for prop in self.lvUpItem.yaoPeiExtraProps:
                    if prop[5] <= self.oldLv:
                        propInfo = self.createPropInfo(prop[0], prop[1], prop[2], oldExtraAdd, newExtraAdd)
                        propList.append(propInfo)
                    elif prop[5] <= newLv:
                        propActivateInfo = self.createPropActivateInfo(prop[0], prop[1], prop[2], prop[3], prop[4], True)
                        propActivateList.append(propActivateInfo)

            yaoPeiSkillId = getattr(self.lvUpItem, 'yaoPeiSkillId', 0)
            if yaoPeiSkillId and oldSkillLv < newSkillLv:
                if oldSkillLv > 0:
                    skillInfo = {}
                    skillInfo['isProp'] = False
                    skillInfo['skillDesc'] = gameStrings.TEXT_YAOPEILVUPPROXY_89 % (newSkillLv - oldSkillLv)
                    propList.append(skillInfo)
                elif newSkillLv > 0:
                    skillInfo = {}
                    skillInfo['isProp'] = False
                    skillInfo['skillDesc'] = self.createSkillDesc(yaoPeiSkillId)
                    propActivateList.append(skillInfo)
            info['propList'] = propList
            info['propActivateList'] = propActivateList
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def createPropInfo(self, pId, pType, pVal, oldBasicAdd, newBasicAdd):
        info = {}
        info['isProp'] = True
        prd = PRD.data.get(pId, {})
        info['propName'] = prd.get('name', '')
        showType = prd.get('showType', 0)
        info['oldValue'] = uiUtils.formatProp(pVal * oldBasicAdd, pType, showType)
        info['newValue'] = uiUtils.formatProp(pVal * newBasicAdd, pType, showType)
        return info

    def createPropActivateInfo(self, pId, pType, pVal, minVal, maxVal, activated):
        info = {}
        info['isProp'] = True
        prd = PRD.data.get(pId, {})
        info['propName'] = prd.get('name', '')
        showType = prd.get('showType', 0)
        pVal = uiUtils.formatProp(pVal, pType, showType)
        minVal = uiUtils.formatProp(minVal, pType, showType)
        maxVal = uiUtils.formatProp(maxVal, pType, showType)
        if activated:
            info['value'] = '+%s ( %s - %s )' % (pVal, minVal, maxVal)
        else:
            info['value'] = '+ ( %s - %s )' % (minVal, maxVal)
        return info

    def createSkillDesc(self, skillId):
        skillInfo = BigWorld.player().getSkillTipsInfo(skillId, 1)
        mainEff = skillInfo.getSkillData('mainEff', '')
        equipSkillDesc = skillInfo.getSkillData('shortMainEff', mainEff)
        return '[%s]<br>%s' % (SGTD.data.get(skillId, {}).get('name', ''), equipSkillDesc)
