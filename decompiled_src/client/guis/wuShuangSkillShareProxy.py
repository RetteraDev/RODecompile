#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wuShuangSkillShareProxy.o
import BigWorld
import gameglobal
import utils
import copy
import uiConst
import const
import events
import skillDataInfo
import cPickle
import zlib
import tipUtils
import gametypes
from uiProxy import UIProxy
from guis.asObject import ASUtils
from guis.asObject import TipManager
from guis.asObject import ASObject
from gameStrings import gameStrings
from data import skill_panel_data as SPD
from data import skill_general_data as SGD
from data import skill_general_template_data as SGTD
from data import sys_config_data as SCD
SCHEME_KEY = ['schemeDefault',
 'schemeExtra_1',
 'schemeExtra_2',
 'schemeSpecial']
SCHEME_NAME_KEY = ['nameDefault',
 'nameExtra1',
 'nameExtra2',
 'nameSpecial']
HOT_KEY_DICT = {(0, 0): 'F1',
 (0, 1): 'F2',
 (0, 2): 'F3',
 (1, 0): 'F4',
 (1, 1): 'F5',
 (1, 2): 'F6'}
TITLE_NAMES = {const.SCHOOL_SHENTANG: ('TianFa', 'ShenYou'),
 const.SCHOOL_YUXU: ('WanXiang', 'XingLuo'),
 const.SCHOOL_GUANGREN: ('WenQing', 'WenDao'),
 const.SCHOOL_YANTIAN: ('YanSha', 'TianShu'),
 const.SCHOOL_LINGLONG: ('QiaoYu', 'HuaYan'),
 const.SCHOOL_LIUGUANG: ('JiMie', 'YanGuang'),
 const.SCHOOL_YECHA: ('YeSha1', 'YeSha2'),
 const.SCHOOL_TIANZHAO: ('tianzhao1', 'tianzhao2')}
DAO_HANG_NUM_TO_FAME = {1: 'one',
 2: 'two',
 3: 'three',
 4: 'four',
 5: 'five'}
TITLE_NUM = 2
MAX_BG_LEVEL = 4
MAX_SPECIAL_SKILL_NUM = 8
LEFT_OFFSET = 12
RIGHT_OFFSET = 15
EQUIP_NUM = 3

class WuShuangSkillShareProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WuShuangSkillShareProxy, self).__init__(uiAdapter)
        self.widget = None
        self.sharedSkillData = None
        self.currentMode = 0
        self.wsSkillDict = {}
        self.filterMode = []
        self.wuShuangHotKeys = {}
        self.selectTypes = []
        self.wsData = {}

    def initPanel(self, widget):
        self.widget = widget
        self.initData()
        self.initUI()

    def initData(self):
        p = BigWorld.player()
        self.sharedSkillData = {}
        self.wsData = p.sharedSkillData.get('wsSkill', {})
        defaultPlanIdx = 1
        for i in xrange(0, len(SCHEME_KEY)):
            if self.wsData.get(SCHEME_KEY[i], []):
                scheme = copy.deepcopy(self.wsData.get(SCHEME_KEY[i], []))
                learnedSkills = []
                for k, v in scheme.iteritems():
                    skillId = k
                    learnedSkills.append(skillId)

                self.sharedSkillData[i] = {}
                self.sharedSkillData[i]['scheme'] = scheme
                schemeName = self.wsData.get(SCHEME_NAME_KEY[i], '')
                self.sharedSkillData[i]['schemeName'] = schemeName if schemeName else gameStrings.DEFAULT_SKILL_PLAN % defaultPlanIdx
                if not schemeName:
                    defaultPlanIdx += 1
                self.sharedSkillData[i]['learnedSkills'] = learnedSkills
                self.filterMode.append({'label': self.sharedSkillData[i]['schemeName'],
                 'mode': i})

        self.school = p.sharedSkillData.get('school', 0)
        self.wsSkillDict[uiConst.SKILL_PANEL_SPECIAL_LEFT] = SPD.data.get(self.school, {}).get('wsType%dSpecialSkills' % uiConst.SKILL_PANEL_SPECIAL_LEFT, [])
        self.wsSkillDict[uiConst.SKILL_PANEL_SPECIAL_RIGHT] = SPD.data.get(self.school, {}).get('wsType%dSpecialSkills' % uiConst.SKILL_PANEL_SPECIAL_RIGHT, [])
        hotKeyData = self.wsData.get('wushuangHotKeys', {})
        for k, v in hotKeyData.iteritems():
            self.wuShuangHotKeys[k] = cPickle.loads(zlib.decompress(v))

        self.selectTypes = []
        self.selectTypes.append(self.wsData.get('selectType1', []))
        self.selectTypes.append(self.wsData.get('selectType2', []))

    def initUI(self):
        self.initFilter()
        self.initTitle()
        self.initWuShuangSlot()
        self.initEquipSlot()
        self.initWsHud(uiConst.SKILL_PANEL_SPECIAL_LEFT)
        self.initWsHud(uiConst.SKILL_PANEL_SPECIAL_RIGHT)

    def initWsHud(self, direction):
        p = BigWorld.player()
        idx = direction - 1
        hud = self.widget.specialPanel.getChildByName('wsHud%d' % idx)
        wsCeil = self.wsData.get('mws', [0, 0])[idx] / 100
        maxCeil = int(SCD.data.get('wsMaxLimit%d' % idx, 10000) / 100)
        hud.notice.text = gameStrings.WS_MAX_TXT % wsCeil
        hud.progress.maxValue = maxCeil
        hud.progress.currentValue = wsCeil
        hud.progress.lableVisible = False
        TipManager.addTip(hud, gameStrings.WS_VALUE_TIP)

    def initWuShuangSlot(self):
        self.setWuShuangSlot(True)
        self.setWuShuangSlot(False)

    def initEquipSlot(self):
        keys = []
        if self.wuShuangHotKeys:
            currentWSHotKey = self.wuShuangHotKeys.get(self.currentMode, {})
            for k, v in currentWSHotKey.iteritems():
                preId = 0
                idx = 0
                if k[1] >= RIGHT_OFFSET:
                    preId = uiConst.SKILL_PANEL_SPECIAL_RIGHT - 1
                    idx = k[1] - RIGHT_OFFSET
                else:
                    preId = uiConst.SKILL_PANEL_SPECIAL_LEFT - 1
                    idx = k[1] - LEFT_OFFSET
                skillId = v[1]
                slot = self.widget.specialPanel.getChildByName('equSkill%d_%d' % (preId, idx))
                slot.slot.keyBind.text = HOT_KEY_DICT[preId, idx]
                self.setEquipSlotBySkillId(slot, skillId)
                self.setDaoHang(skillId, preId, idx)
                keys.append((preId, idx))

            for i in xrange(0, 2):
                for j in xrange(0, EQUIP_NUM):
                    if (i, j) not in keys:
                        slot = self.widget.specialPanel.getChildByName('equSkill%d_%d' % (i, j))
                        slot.slot.dragable = False
                        slot.slot.keyBind.text = HOT_KEY_DICT[i, j]
                        slot.skillName.visible = False
                        slot.slot.data = None
                        self.initDaoHang(i, j)

        elif self.selectTypes:
            for i in xrange(0, len(self.selectTypes)):
                selectType = self.selectTypes[i]
                for j in xrange(0, len(selectType)):
                    skillId = selectType[j]
                    slot = self.widget.specialPanel.getChildByName('equSkill%d_%d' % (i, j))
                    slot.slot.keyBind.text = HOT_KEY_DICT[i, j]
                    self.setEquipSlotBySkillId(slot, skillId)
                    self.setDaoHang(skillId, i, j)

        else:
            for i in xrange(0, 2):
                for j in xrange(0, EQUIP_NUM):
                    slot = self.widget.specialPanel.getChildByName('equSkill%d_%d' % (i, j))
                    slot.slot.keyBind.text = HOT_KEY_DICT[i, j]
                    slot.slot.dragable = False
                    slot.slot.data = None
                    slot.skillName.visible = False
                    self.initDaoHang(i, j)

    def getDaoHangData(self, skillId):
        scheme = self.sharedSkillData.get(self.currentMode, {}).get('scheme', {})
        daoHangData = scheme.get(skillId, {})
        return daoHangData

    def setDaoHang(self, skillId, preIdx, idx):
        self.initDaoHang(preIdx, idx)
        daoHangMc = self.widget.specialPanel.getChildByName('daoHangMc%d_%d' % (preIdx, idx))
        daoHangData = self.getDaoHangData(skillId)
        for daoHangIdx, daoHangNum in daoHangData.iteritems():
            realIdx = uiConst.WUSHUANG_IDX[daoHangIdx - 1]
            daoHang = daoHangMc.getChildByName('daoHang%d' % realIdx)
            daoHang.gotoAndStop('activation')
            daoHang.num.gotoAndStop(DAO_HANG_NUM_TO_FAME[daoHangNum])

    def initDaoHang(self, preIdx, idx):
        daoHangMc = self.widget.specialPanel.getChildByName('daoHangMc%d_%d' % (preIdx, idx))
        for i in xrange(0, len(uiConst.WUSHUANG_IDX)):
            daoHang = daoHangMc.getChildByName('daoHang%d' % i)
            daoHang.gotoAndStop('normal')
            daoHang.num.gotoAndStop('one')

    def getDaoHangDict(self, skillId):
        daoHangData = self.getDaoHangData(skillId)
        extraInfo = {'windCnt': 0,
         'forestCnt': 0,
         'hillCnt': 0,
         'fireCnt': 0}
        for daoHangIdx, daoHangNum in daoHangData.iteritems():
            daoHangType = uiConst.WUSHUANG_IDX[daoHangIdx - 1]
            if daoHangType == uiConst.WIND_TYPE:
                extraInfo['windCnt'] = daoHangNum
            elif daoHangType == uiConst.WOOD_TYPE:
                extraInfo['forestCnt'] = daoHangNum
            elif daoHangType == uiConst.HILL_TYPE:
                extraInfo['hillCnt'] = daoHangNum
            elif daoHangType == uiConst.FIRE_TYPE:
                extraInfo['fireCnt'] = daoHangNum

        return extraInfo

    def setEquipSlotBySkillId(self, slot, skillId):
        if not skillId:
            slot.skillName.visible = False
            slot.slot.data = None
            return
        else:
            data, skillName = self.getSkillInfoById(skillId)
            slot.slot.setItemSlotData(data)
            slot.slot.dragable = False
            slot.slot.validateNow()
            skillLv = self.wsData.get('skillInfo', {}).get(skillId, 0)
            extraInfo = self.getDaoHangDict(skillId)
            extraInfo['isOnlyDetail'] = True
            TipManager.addTipByType(slot.slot, tipUtils.TYPE_WS_SKILL, {'skillId': skillId,
             'lv': skillLv,
             'extraInfo': extraInfo})
            ASUtils.setHitTestDisable(slot.slotBox, True)
            slot.skillName.textField.text = skillName
            slot.skillName.visible = True
            return

    def initFilter(self):
        panel = self.widget.specialPanel
        panel.filter.menuRowCount = len(self.filterMode)
        panel.filter.addEventListener(events.INDEX_CHANGE, self.handleFilterIndexChange)
        ASUtils.setDropdownMenuData(panel.filter, self.filterMode)
        panel.filter.selectedIndex = 0

    def handleFilterIndexChange(self, *args):
        panel = self.widget.specialPanel
        self.currentMode = self.filterMode[panel.filter.selectedIndex]['mode']
        self.initWuShuangSlot()
        self.initEquipSlot()

    def getSkillInfoById(self, skillId):
        sd = skillDataInfo.ClientSkillInfo(skillId)
        icon = sd.getSkillData('icon', None)
        data = {'iconPath': 'skill/icon64/%s.dds' % icon}
        skillName = SGTD.data.get(skillId, {}).get('name', '')
        return (data, skillName)

    def setWuShuangSlot(self, isLeft):
        idx = 0
        direction = 1
        if isLeft:
            idx = uiConst.SKILL_PANEL_SPECIAL_LEFT - 1
            direction = uiConst.SKILL_PANEL_SPECIAL_LEFT
        else:
            idx = uiConst.SKILL_PANEL_SPECIAL_RIGHT - 1
            direction = uiConst.SKILL_PANEL_SPECIAL_RIGHT
        for i in xrange(0, MAX_SPECIAL_SKILL_NUM):
            slot = self.widget.specialPanel.getChildByName('slot%d_%d' % (idx, i))
            if i >= len(self.wsSkillDict[direction]):
                slot.gotoAndStop('close')
                continue
            skillId = self.wsSkillDict[direction][i]
            slot.gotoAndStop('open')
            ASUtils.setHitTestDisable(slot.icon.slotBox, True)
            slot.icon.addBtn.visible = False
            slot.icon.practiceBtn.visible = False
            data, skillName = self.getSkillInfoById(skillId)
            slot.icon.slot.setItemSlotData(data)
            slot.icon.slot.validateNow()
            slot.icon.skillName.text = skillName
            slot.icon.slot.dragable = False
            skillLv = 0
            learnedSkills = self.sharedSkillData.get(self.currentMode, {}).get('learnedSkills', {})
            if learnedSkills and skillId in learnedSkills:
                slot.icon.slot.enabled = True
                skillLv = self.wsData.get('skillInfo', {}).get(skillId, 0)
                slot.icon.valueAmount.text = '%d/%d' % (skillLv, gametypes.WUSHUANG_LV_MAX)
            else:
                slot.icon.slot.enabled = False
                wsStar = SGD.data.get((skillId, 1), {}).get('wsStar', 1)
                if wsStar == 3:
                    slot.icon.valueAmount.text = gameStrings.WU_SHUANG_NOT_LEARNED
                else:
                    autoNeedLv = SGD.data.get((skillId, 1), {}).get('learnLv', 1)
                    slot.icon.valueAmount.text = gameStrings.WU_SHUANG_LV_REQUIRE % autoNeedLv
            TipManager.addTipByType(slot.icon.slot, tipUtils.TYPE_WS_SKILL, {'skillId': skillId,
             'lv': skillLv,
             'extraInfo': {'isOnlyDetail': True}})

    def initTitle(self):
        for i in xrange(0, TITLE_NUM):
            self.widget.specialPanel.getChildByName('wushuang%d' % i).gotoAndStop(TITLE_NAMES[self.school][i])

    def initBG(self):
        leftWushuangBg = self.widget.specialPanel.getChildByName('wushuangBg%d' % (uiConst.SKILL_PANEL_SPECIAL_LEFT - 1))
        rightWushuangBg = self.widget.specialPanel.getChildByName('wushuangBg%d' % (uiConst.SKILL_PANEL_SPECIAL_RIGHT - 1))
        for i in xrange(0, MAX_BG_LEVEL):
            visible = False
            if i == MAX_BG_LEVEL - 1:
                visible = True
            leftBg = leftWushuangBg.getChildByName('level%d' % i)
            rightBg = rightWushuangBg.getChildByName('level%d' % i)
            leftBg.visible = visible
            rightBg.visible = visible
            leftBg.gotoAndStop(1)
            rightBg.gotoAndStop(1)

    def unRegisterPanel(self):
        self.widget = None
        self.sharedSkillData = None
        self.currentMode = 0
        self.wsSkillDict = {}
        self.filterMode = []
        self.wuShuangHotKeys = {}
        self.selectTypes = []
        self.wsData = {}
