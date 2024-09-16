#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/clanWarSkillProxy.o
import BigWorld
from Scaleform import GfxValue
import logicInfo
import const
import uiConst
import events
from callbackHelper import Functor
from gameclass import PSkillInfo
from guis.asObject import ASObject
from guis import uiUtils
from gamestrings import gameStrings
from uiProxy import SlotDataProxy
from data import cross_clan_war_config_data as CCWCD
from data import guild_skill_data as GSD
from data import guild_config_data as GCD
import gameglobal
SKILL_MAX_CNT = 8
CLAN_WAR_P_SKILL = 'clanWarPSkills'
CLAN_WAR_SKILL = 'clanWarSkills'
CLAN_WAR_CROSS_SKILL_QL = 'clanWarCrossSkillsQL'
CLAN_WAR_CROSS_SKILL_BH = 'clanWarCrossSkillsBH'
SCROLL_AREA_BASE_Y = 110
HIT_BASE_HEIGHT = 500

class ClanWarSkillProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(ClanWarSkillProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.bindType = 'clanWarSkill'
        self.type = 'clanWarSkill'
        self.callbackHandler = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_CLAN_WAR_SKILL, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CLAN_WAR_SKILL:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CLAN_WAR_SKILL)
        for value in self.callbackHandler.itervalues():
            BigWorld.cancelCallback(value)

        self.callbackHandler.clear()

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CLAN_WAR_SKILL)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.scrollWndList.itemRenderer = 'ClanWarSkill_ItemRender'
        self.widget.scrollWndList.labelFunction = self.labelFunction
        self.widget.scrollWndList.itemHeightFunction = self.itemHeightFunction

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshZhanHunPoint()
        self.refreshYanwuPoint()
        skillDataArray = [CLAN_WAR_P_SKILL, CLAN_WAR_SKILL]
        if self.getEnableGuildCrossSkill():
            skillDataArray.extend([CLAN_WAR_CROSS_SKILL_QL, CLAN_WAR_CROSS_SKILL_BH])
        self.widget.scrollWndList.dataArray = skillDataArray
        self.widget.scrollWndList.validateNow()
        self.updateSlots()

    def refreshZhanHunPoint(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.widget.progressBar.maxValue = CCWCD.data.get('zhanhunMax', 5000)
        self.widget.progressBar.currentValue = getattr(p, 'zhanHun', 0)
        self.widget.progressBar.lableVisible = False
        self.widget.txtZhanHun.text = '%d/%d' % (getattr(p, 'zhanHun', 0), CCWCD.data.get('zhanhunMax', 5000))

    def refreshYanwuPoint(self):
        if not self.widget:
            return
        scrollAreaY = SCROLL_AREA_BASE_Y
        hitHeight = HIT_BASE_HEIGHT
        if not self.getEnableGuildCrossSkill():
            self.widget.yanwuArea.visible = False
            self.widget.iconArea.y = scrollAreaY
            self.widget.scrollWndList.y = scrollAreaY
            self.widget.hit.height = hitHeight
            return
        p = BigWorld.player()
        scrollAreaY += 70
        hitHeight += 70
        self.widget.yanwuArea.visible = True
        self.widget.iconArea.y = scrollAreaY
        self.widget.scrollWndList.y = scrollAreaY
        self.widget.hit.height = hitHeight
        yanwuQL = getattr(p, 'yanwuQL', 0)
        yanwuBH = getattr(p, 'yanwuBH', 0)
        area = self.widget.yanwuArea
        area.QLProgressBar.maxValue = GCD.data.get('yanWuZhiWeeklyMax', 5000)
        area.QLProgressBar.currentValue = yanwuQL
        area.QLProgressBar.lableVisible = False
        area.yanwuQLText.text = gameStrings.CROSS_TOURNAMENT_YANWU_QL % (yanwuQL, GCD.data.get('yanWuZhiWeeklyMax', 5000))
        area.BHProgressBar.maxValue = GCD.data.get('yanWuZhiWeeklyMax', 5000)
        area.BHProgressBar.currentValue = yanwuBH
        area.BHProgressBar.lableVisible = False
        area.yanwuBHText.text = gameStrings.CROSS_TOURNAMENT_YANWU_BH % (yanwuBH, GCD.data.get('yanWuZhiWeeklyMax', 5000))

    def itemHeightFunction(self, *args):
        key = args[3][0].GetString()
        skills = CCWCD.data.get(key, [])
        return GfxValue(76 if len(skills) <= 4 else 141)

    def getSlotID(self, key):
        if key.find(CLAN_WAR_P_SKILL) >= 0:
            return (CLAN_WAR_P_SKILL, int(key[len('clanWarskill.clanWarPSkills'):]))
        if key.find(CLAN_WAR_SKILL) >= 0:
            return (CLAN_WAR_SKILL, int(key[len('clanWarskill.clanWarSkills'):]))
        if key.find(CLAN_WAR_CROSS_SKILL_QL) >= 0:
            return (CLAN_WAR_CROSS_SKILL_QL, int(key[len('clanWarskill.%s' % CLAN_WAR_CROSS_SKILL_QL):]))
        if key.find(CLAN_WAR_CROSS_SKILL_BH) >= 0:
            return (CLAN_WAR_CROSS_SKILL_BH, int(key[len('clanWarskill.%s' % CLAN_WAR_CROSS_SKILL_BH):]))
        return (CLAN_WAR_P_SKILL, int(key[len('clanWarskill.clanWarPSkills'):]))

    def getSlotValue(self, movie, idItem, idCon):
        if GSD.data.get(idItem, {}).get('clientSkill', 0):
            idItem = GSD.data.get(idItem, {}).get('clientSkill', 0)
        if idCon:
            icon = self.uiAdapter.actionbar._getSkillIcon(idItem)
            data = {'iconPath': icon}
            return uiUtils.dict2GfxDict(data, True)

    def labelFunction(self, *args):
        key = args[3][0].GetString()
        skillList = []
        itemMc = ASObject(args[3][1])
        if key == CLAN_WAR_P_SKILL:
            itemMc.txtTitle.text = gameStrings.CROSS_CLAN_WAR_PSKILL
            skillList = CCWCD.data.get(key, [])
        elif key == CLAN_WAR_SKILL:
            itemMc.txtTitle.text = gameStrings.CROSS_CLAN_WAR_SKILL
            skillList = CCWCD.data.get(key, [])
        elif key == CLAN_WAR_CROSS_SKILL_QL:
            itemMc.txtTitle.text = gameStrings.CROSS_TOURNAMENT_SKILL_QL
            skillList = GCD.data.get(key, [])
        elif key == CLAN_WAR_CROSS_SKILL_BH:
            itemMc.txtTitle.text = gameStrings.CROSS_TOURNAMENT_SKILL_BH
            skillList = GCD.data.get(key, [])
        for i in xrange(SKILL_MAX_CNT):
            slot = itemMc.getChildByName('skill%d' % i)
            if i < len(skillList):
                slot.visible = True
                slot.validateNow()
                slot.binding = 'clanWarSkill.%s%d' % (key, skillList[i])
                slot.addEventListener(events.MOUSE_CLICK, self.handleSlotClick, False, 0, True)
            else:
                slot.visible = False

    def onGetTooltip(self, *args):
        key = args[3][0].GetString()
        _, skillId = self.getSlotID(key)
        if GSD.data.get(skillId, {}).get('clientSkill', 0):
            skillId = GSD.data.get(skillId, {}).get('clientSkill', 0)
        return self.uiAdapter.skill.formatTooltip(skillId)

    def handleSlotClick(self, *args):
        e = ASObject(args[3][0])
        skillType, skillId = self.getSlotID(e.currentTarget.binding)
        if skillId:
            BigWorld.player().useGuildSkill(skillId)

    def updateSlots(self, *args):
        if not self.widget:
            return
        for key, v in self.binding.iteritems():
            _, skillId = self.getSlotID(key)
            remain = 0
            total = 0
            if logicInfo.cooldownClanWarSkill.has_key(skillId):
                end, total = logicInfo.cooldownClanWarSkill[skillId]
                remain = end - BigWorld.time()
            if self.callbackHandler.has_key(key):
                BigWorld.cancelCallback(self.callbackHandler[key])
            if remain > 0:
                v[0].Invoke('setShowNumber', GfxValue(True))
                v[0].Invoke('playCooldown', (GfxValue(total * 1000), GfxValue((total - remain) * 1000)))
                self.callbackHandler[key] = BigWorld.callback(remain, Functor(self.afterSkillEndCooldown, v[0], skillId))
            else:
                v[0].Invoke('setShowNumber', GfxValue(False))
                v[0].Invoke('stopCooldown')

    def afterSkillEndCooldown(self, slot, skillId):
        if not self.widget:
            return
        else:
            logicInfo.cooldownClanWarSkill.pop(skillId, None)
            slot.Invoke('endCooldown')
            return

    def getEnableGuildCrossSkill(self):
        return gameglobal.rds.configData.get('enableGuildCrossSkill', False)
