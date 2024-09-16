#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldArmySkillProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gamelog
import utils
import uiUtils
import uiConst
import events
import math
import wingWorldUtils
from uiProxy import UIProxy
from uiProxy import SlotDataProxy
from guis.asObject import TipManager
from gameclass import PSkillInfo
from data import wing_world_army_data as WWAD
from data import wing_world_camp_army_data as WWCAD
from cdata import game_msg_def_data as GMDD
from data import wing_world_config_data as WWCD
from data import wing_world_data as WWD
from data import region_server_config_data as RSCD
from gamestrings import gameStrings
WW_SKILL_BINDING = 'skill'
WW_PS_SKILL_BINDING = 'psSkill'

class WingWorldArmySkillProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(WingWorldArmySkillProxy, self).__init__(uiAdapter)
        self.widget = None
        self.bindType = 'wingWorld'
        self.type = 'wingWorld'
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_WORLD_ARMY_SKILL, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_WORLD_ARMY_SKILL:
            self.widget = widget
            self.skillData = None
            self.initUI()
            self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.tipMc.visible = False
        p = BigWorld.player()
        if p.isWingWorldCampMode():
            self.widget.mpTitle.text = gameStrings.WING_WORLD_CAMP_MP
            self.widget.tipMc.textField.text = gameStrings.WING_WORLD_CAMP_MP
        else:
            self.widget.mpTitle.text = gameStrings.WING_WORLD_COUNTRY_MP
            self.widget.tipMc.textField.text = gameStrings.WING_WORLD_COUNTRY_MP

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_ARMY_SKILL)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_WORLD_ARMY_SKILL)

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshView()

    def getWingWorldArmySkillData(self):
        p = BigWorld.player()
        if p.isWingWorldCampMode():
            ArmyData = WWCAD.data
            camp = p.wingWorld.country.getCamp(p.wingWorldCamp)
            groupId = p.getWingWorldGroupId()
            initData = {'maxMp': WWD.data.get(groupId, {}).get('campMaxmp', 0),
             'curMp': camp.mp}
            skillIds = WWCD.data.get('campArmySkills', ())
            psSkillIds = WWCD.data.get('campArmyPsSkills', ())
        else:
            ArmyData = WWAD.data
            hostId = utils.getHostId()
            groupId = RSCD.data.get(hostId, {}).get('wingWorldGroupId', 0)
            country = p.wingWorld.country.getCountry(hostId)
            initData = {'maxMp': WWD.data.get(groupId, {}).get('maxmp', 0),
             'curMp': country.mp}
            skillIds = WWCD.data.get('armySkills', ())
            psSkillIds = WWCD.data.get('armyPsSkills', ())
        initData['skillNum'] = len(skillIds)
        initData['psSkillNum'] = len(psSkillIds)
        usedMp = 0
        usedList = []
        for postId in sorted(ArmyData.keys()):
            val = ArmyData.get(postId)
            if val.get('skills'):
                postVal = p.wingWorld.getArmyByPostId(postId)
                mpUsed = postVal.mpUsed if postVal else 0
                usedMp += mpUsed
                usedList.append({'label': gameStrings.TEXT_WINGWORLDARMYSKILLPROXY_97 % (val.get('name', ''), postVal.name if postVal else gameStrings.TEXT_ROLEINFOPROXY_2565),
                 'val': mpUsed})

        initData['usedMp'] = usedMp
        initData['labels'] = usedList
        return initData

    def refreshView(self):
        posY = 35
        posX = 25
        slotY = posY
        self.skillData = self.getWingWorldArmySkillData()
        self.widget.bar.maxValue = self.skillData.get('maxMp', 0)
        self.widget.bar.currentValue = self.skillData.get('curMp', 0)
        skillCanvas = self.widget.skillList.canvas
        for i in xrange(self.skillData.get('psSkillNum', 0)):
            slot = self.widget.getInstByClsName('M12_SkillSlot40x40_Bg')
            slot.binding = 'wingWorld.psSkill%d' % i
            slot.dragable = False
            skillCanvas.addChild(slot)
            slot.x = posX + i % 4 * 56
            slot.y = posY + int(i / 4) * 56
            slot.addEventListener(events.MOUSE_CLICK, self.handleClickSkill, False, 0, True)
            slotY = slot.y

        skillCanvas.skillTitle2.y = slotY + 56
        posY = slotY + 88
        for i in xrange(self.skillData.get('skillNum', 0)):
            slot = self.widget.getInstByClsName('M12_SkillSlot40x40_Bg')
            slot.binding = 'wingWorld.skill%d' % i
            skillCanvas.addChild(slot)
            slot.x = posX + i % 4 * 56
            slot.y = posY + int(i / 4) * 56
            slot.addEventListener(events.MOUSE_CLICK, self.handleClickSkill, False, 0, True)

        self.widget.skillList.refreshHeight()
        TipManager.addTipByFunc(self.widget.bar, self.getWWArmySkillTip, None, False)

    def handleClickSkill(self, *args):
        BigWorld.player().showGameMsg(GMDD.data.USE_WW_ARMY_SKILL_MSG, ())

    def getWWArmySkillTip(self, *args):
        self.widget.tipMc.visible = True
        self.widget.tipMc.mp.text = '%d/%d' % (self.skillData.get('curMp', 0), self.skillData.get('maxMp', 0))
        self.widget.tipMc.usedMp.text = self.skillData.get('usedMp', 0)
        for i in xrange(6):
            label = self.widget.tipMc.getChildByName('label%d' % i)
            val = self.widget.tipMc.getChildByName('val%d' % i)
            if self.skillData.get('labels', 0)[i]:
                label.visible = True
                val.visible = True
                label.text = self.skillData.get('labels', [])[i].get('label', '')
                label.width = label.textWidth + 4
                val.x = label.x + label.width
                val.text = self.skillData.get('labels', [])[i].get('val', '')
            else:
                label.visible = False
                val.visible = False

        TipManager.showImediateTip(self.widget.bar, self.widget.tipMc)
        return self.widget.tipMc

    def onGetTooltip(self, *args):
        key = args[3][0].GetString()
        _, skillId = self.getSkillIDByBinding(key)
        if key.find(WW_SKILL_BINDING) >= 0:
            return self.uiAdapter.skill.formatTooltip(skillId)
        else:
            return self.uiAdapter.skill.formatPSkillTooltip(skillId)

    def getSkillIDByBinding(self, key):
        skills = []
        idx = 0
        skillType = ''
        if key.find(WW_PS_SKILL_BINDING) >= 0:
            idx = int(key[len('wingWorld.' + WW_PS_SKILL_BINDING):])
            skills = WWCD.data.get('armyPsSkills', ())
            skillType = WW_PS_SKILL_BINDING
        elif key.find(WW_SKILL_BINDING) >= 0:
            idx = int(key[len('wingWorld.' + WW_SKILL_BINDING):])
            skills = WWCD.data.get('armySkills', ())
            skillType = WW_SKILL_BINDING
        if idx < len(skills):
            return (skillType, skills[idx])
        return ('', 0)

    def getSlotID(self, key):
        return self.getSkillIDByBinding(key)

    def getSlotValue(self, movie, idItem, idCon):
        if idCon:
            if idCon == WW_PS_SKILL_BINDING:
                skillData = PSkillInfo(idItem, 1)
                icon = 'skill/icon/%d.dds' % skillData.getSkillData('icon', 0)
            else:
                icon = self.uiAdapter.actionbar._getSkillIcon(idItem)
            data = {'iconPath': icon}
            return uiUtils.dict2GfxDict(data, True)
