#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/commonSkillShareProxy.o
import BigWorld
import gameglobal
import utils
import skillDataInfo
import skillInfoManager
import events
import const
from uiProxy import UIProxy
from gameclass import SkillInfo
from gameclass import PSkillInfo
from guis import tipUtils
from guis import asObject
from guis.asObject import ASObject
from guis.asObject import Tweener
from guis.asObject import TipManager
from guis.asObject import ASUtils
from callbackHelper import Functor
from gameStrings import gameStrings
from skillEnhanceCommon import CSkillEnhanceVal
from data import skill_panel_data as SPD
from data import sys_config_data as SCD
from data import skill_general_data as SGD
from data import skill_general_template_data as SGTD
from data import skill_enhance_data as SED
from data import jingjie_data as JJD
from cdata import skill_enhance_lv_data as SELD
from cdata import pskill_data as PD
from cdata import skill_enhance_jingjie_data as SEJD
from cdata import game_msg_def_data as GMDD
import formula
MAX_SKILL_NUM = 12
SKILL_SLOT_NAME = 'CommonSkill_Button'
SKILL_STATE = 0
XIU_LIAN_STATE = 1
MAX_XIULIAN_COLUMN = 5
MAX_XIULIAN_ROW = 3
SKILL_ITEM_WIDTH = 468
MAX_CANVAS_WIDTH = 1050

class CommonSkillShareProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CommonSkillShareProxy, self).__init__(uiAdapter)
        self.widget = None
        self.sharedSkillData = None
        self.skillIdList = []
        self.psSkillIdList = []
        self.school = 0
        self.maxSkillLevel = 0
        self.skillModeInfo = {}
        self.currentMode = 0
        self.skillManager = None
        self.xiuLianPanel = None
        self.skillPanel = None
        self.lastSelect = None
        self.canvasInitX = 0
        self.moveTimeCnt = 0
        self.oldNextX = 0
        self.oldPrevX = 0
        self.isNextTweenerRunning = False
        self.isPreTweenerRunning = False
        self.currentSkillState = SKILL_STATE
        self.childSkillIdDict = {}
        self.filterMode = []
        self.usedXiulianPoint = 0

    def initPanel(self, widget):
        self.widget = widget
        self.initData()
        self.initUI()

    def initData(self):
        p = BigWorld.player()
        self.sharedSkillData = p.sharedSkillData
        self.school = self.sharedSkillData.get('school', 0)
        self.skillIdList = SPD.data.get(self.school, {}).get('wsType1Skills', []) + SPD.data.get(self.school, {}).get('wsType2Skills', [])
        self.childSkillIdDict = {}
        for skillId in self.skillIdList:
            skillInfo = SkillInfo(skillId, 1)
            childId = skillInfo.getSkillData('childId', [])
            if childId:
                self.childSkillIdDict[skillId] = []
                for subSkillId in childId:
                    self.childSkillIdDict[skillId].append(subSkillId)

        self.psSkillIdList = SPD.data.get(self.school, {}).get('pskills', [])
        self.maxSkillLevel = SCD.data.get('maxSkillLevel', 0)
        self.filterMode = []
        defaultPlanIdx = 1
        for info in self.sharedSkillData.get('skill', []):
            mode = info[0]
            skillInfo = info[1]
            self.preProcessSkillInfo(skillInfo)
            modeName = info[2]
            self.skillModeInfo[mode] = {}
            self.skillModeInfo[mode]['skillInfo'] = skillInfo
            self.skillModeInfo[mode]['modeName'] = modeName if modeName else gameStrings.DEFAULT_SKILL_PLAN % defaultPlanIdx
            if not modeName:
                defaultPlanIdx += 1
            self.filterMode.append({'label': self.skillModeInfo[mode]['modeName'],
             'mode': mode})

        self.skillManager = skillInfoManager.getInstance()

    def getPrePart(self, part):
        row, col = part / 10, part % 10
        prePart = row - 1
        if prePart > 0:
            return prePart * 10 + col
        return 0

    def preProcessSkillInfo(self, skillInfo):
        for skillId in skillInfo:
            enhanceData = skillInfo.get(skillId, {}).get('enhanceData', {})
            for i in xrange(MAX_XIULIAN_ROW):
                for j in xrange(MAX_XIULIAN_COLUMN):
                    part = int('%d%d' % (i + 1, j + 1))
                    if not enhanceData.has_key(part) or not enhanceData[part]:
                        continue
                    enhData = SED.data.get((skillId, part), {})
                    enhanceType = formula.getSkillEnhanceType(part)
                    totalPoint = sum([ data['enhancePoint'] for pt, data in enhanceData.iteritems() if pt % 10 in enhanceType and pt != part ])
                    if enhData.has_key('totalPoint') and totalPoint < enhData['totalPoint']:
                        enhanceData[part] = {'enhancePoint': 0}

    def initUI(self):
        if self.currentSkillState == SKILL_STATE:
            self.widget.skillPanel.gotoAndStop('commonSkill')
            self.initFilter()
            self.setSkillPanel()
        else:
            self.widget.skillPanel.gotoAndStop('xiuLian')
            self.setXiuLianPanel()

    def setXiuLianPanel(self):
        self.xiuLianPanel = self.widget.skillPanel.xiuLianPanel
        self.xiuLianPanel.goBackBtn.addEventListener(events.MOUSE_CLICK, self.handleGoBack)
        self.xiuLianPanel.canvas.addEventListener(events.MOUSE_WHEEL, self.handleWheel)
        self.oldNextX = 0
        self.oldPrevX = 0
        self.isNextTweenerRunning = False
        self.isPrevTweenerRunning = False
        self.setSkillList()
        self.setSkillDetail()
        self.setGotoWeb()
        self.initXiuLianPoint()
        self.setSkillPracticeInfo()
        self.setXiuLianPoint()
        self.setEnhanceLvInfo()

    def setSkillList(self):
        while self.xiuLianPanel.canvas.numChildren > 0:
            self.xiuLianPanel.canvas.removeChildAt(0)

        self.moveTimeCnt = 0
        skillItem = None
        xPos = 0
        skillInfo = []
        skillModeInfo = self.skillModeInfo[self.currentMode]['skillInfo']
        for skillId in self.skillIdList:
            item = self.skillManager.commonSkillIns.getSkillItemInfo(skillId)
            item['skLvStr'] = '%d/%d' % (self.getSkillLvFromId(skillId), self.maxSkillLevel)
            item['skillId'] = skillId
            item['level'] = self.getSkillLvFromId(skillId)
            skillInfo.append(item)

        for i in xrange(0, len(skillInfo)):
            skillItem = self.widget.getInstByClsName('CommonSkill_Button')
            skillItem.label = skillInfo[i]['skillName']
            skillItem.data = skillInfo[i]['skillId']
            skillItem.icon.setItemSlotData(skillInfo[i]['icon'])
            skillItem.icon.dragable = False
            skillItem.validateNow()
            skillItem.mouseChildren = True
            skillItem.changeNum.visible = False
            skillItem.numDesc.visible = True
            skillItem.numDesc.textField.text = skillInfo[i]['skLvStr']
            skillItem.textBg.width = skillItem.textField.textWidth + 5
            skillItem.x = xPos
            xPos += skillItem.width + 3
            self.xiuLianPanel.canvas.addChild(skillItem)
            if not i:
                if self.lastSelect:
                    self.lastSelect.selected = False
                    self.lastSelect = None
                skillItem.selected = True
                self.lastSelect = skillItem
            skillItem.icon.mouseEnabled = True
            skillItem.icon.validateNow()
            TipManager.addTipByType(skillItem.icon, tipUtils.TYPE_SKILL, {'skillId': skillInfo[i]['skillId'],
             'lv': skillInfo[i]['level'],
             'extraInfo': {'isOnlyDetail': True}})
            skillItem.addEventListener(events.MOUSE_CLICK, self.handleClickItem)

        self.canvasInitX = self.xiuLianPanel.canvas.x
        self.xiuLianPanel.prevBtn.addEventListener(events.MOUSE_CLICK, self.handlePrevClick)
        self.xiuLianPanel.nextBtn.addEventListener(events.MOUSE_CLICK, self.handleNextClick)

    def getSkillLvFromId(self, skillId):
        skillModeInfo = self.skillModeInfo.get(self.currentMode, {}).get('skillInfo', {})
        lv = skillModeInfo.get(skillId, {}).get('level', 1)
        return lv

    def setSkillDetail(self):
        skillModeInfo = self.skillModeInfo.get(self.currentMode, {}).get('skillInfo', {})
        skillId = int(self.lastSelect.data)
        lv = self.getSkillLvFromId(skillId)
        skillName = SGTD.data.get(skillId, {}).get('name', '')
        self.xiuLianPanel.skillDescDetail.skillName.text = skillName
        sd = skillDataInfo.ClientSkillInfo(skillId)
        icon = sd.getSkillData('icon', None)
        data = {'iconPath': 'skill/icon/%d.dds' % icon}
        self.xiuLianPanel.icon.setItemSlotData(data)
        self.xiuLianPanel.icon.dragable = False
        self.xiuLianPanel.icon.validateNow()
        TipManager.addTipByType(self.xiuLianPanel.icon, tipUtils.TYPE_SKILL, {'skillId': skillId,
         'lv': lv,
         'extraInfo': {'isOnlyDetail': True}})

    def setGotoWeb(self):
        self.xiuLianPanel.gotoWebBtn.addEventListener(events.MOUSE_CLICK, self.handleClickGotoWeb)
        self.xiuLianPanel.gotoWebText.addEventListener(events.MOUSE_CLICK, self.handleClickGotoWeb)

    def initXiuLianPoint(self):
        for i in xrange(0, MAX_XIULIAN_COLUMN):
            endLine = self.xiuLianPanel.xiuLianPointDetail.getChildByName('lineEnd%d' % i)
            endLine.x = 335
            for j in xrange(0, MAX_XIULIAN_ROW):
                xiuLianMc = self.xiuLianPanel.xiuLianPointDetail.getChildByName('xiuLian%d%d' % (j, i))
                xiuLianMc.visible = True
                xiuLianMc.part = '%d%d' % (j + 1, i + 1)
                if j > 1:
                    continue
                line = self.xiuLianPanel.xiuLianPointDetail.getChildByName('line%d%d%d%d' % (j,
                 i,
                 j + 1,
                 i))

            self.xiuLianPanel.xiuLianPointDetail.xiuLianVal1.text = ''
            self.xiuLianPanel.xiuLianPointDetail.xiuLianVal2.text = ''
            self.xiuLianPanel.xiuLianPointDetail.xiuLianVal3.text = ''
            self.xiuLianPanel.xiuLianPoint.pointText.text = ''

    def getEnhanceData(self, skillId):
        self.enhanceData = []
        skillEnhanceInfo = self.skillModeInfo[self.currentMode].get('skillInfo', {}).get(skillId, {}).get('enhanceData', {})
        for i in xrange(MAX_XIULIAN_ROW):
            rowData = []
            for j in xrange(MAX_XIULIAN_COLUMN):
                index = int('%d%d' % (i + 1, j + 1))
                data = SED.data.get((skillId, index), {})
                if not data:
                    visible = False
                else:
                    visible = True
                prePoint = data.get('prePoint', 0)
                curPoint = skillEnhanceInfo.get(index, {}).get('enhancePoint', 0)
                maxPoint = len(data.get('pskills', ()))
                rowData.append({'prePoint': prePoint,
                 'maxPoint': maxPoint,
                 'curPoint': curPoint,
                 'visible': visible})

            self.enhanceData.append(rowData)

    def getUsedXiuLianPoint(self):
        self.usedXiulianPoint = 0
        for skillId in self.skillIdList:
            skillEnhanceInfo = self.skillModeInfo[self.currentMode].get('skillInfo', {}).get(skillId, {}).get('enhanceData', {})
            for i in xrange(MAX_XIULIAN_ROW):
                for j in xrange(MAX_XIULIAN_COLUMN):
                    index = int('%d%d' % (i + 1, j + 1))
                    data = SED.data.get((skillId, index), {})
                    if not data:
                        continue
                    curPoint = skillEnhanceInfo.get(index, {}).get('enhancePoint', 0)
                    self.usedXiulianPoint += curPoint

    def setSkillPracticeInfo(self):
        skillId = int(self.lastSelect.data)
        leftCount = 0
        middleCount = 0
        rightCount = 0
        self.getEnhanceData(skillId)
        self.relayoutLine()
        for i in xrange(0, MAX_XIULIAN_ROW):
            for j in xrange(0, MAX_XIULIAN_COLUMN):
                xiuLianMc = self.xiuLianPanel.xiuLianPointDetail.getChildByName('xiuLian%d%d' % (i, j))
                xiuLianMc.visible = self.enhanceData[i][j]['visible']
                state = const.SKILL_ENHANCE_STATE_ACTIVE
                if not self.enhanceData[i][j]['curPoint']:
                    xiuLianMc.gotoAndStop('hui')
                    state = const.SKILL_ENHANCE_STATE_INACTIVE
                elif self.enhanceData[i][j]['curPoint'] == self.enhanceData[i][j]['maxPoint']:
                    xiuLianMc.gotoAndStop('redLight')
                    state = const.SKILL_ENHANCE_STATE_ACTIVE
                elif self.enhanceData[i][j]['curPoint'] < self.enhanceData[i][j]['maxPoint']:
                    xiuLianMc.gotoAndStop('redHui')
                    state = const.SKILL_ENHANCE_STATE_ACTIVE
                xiuLianMc.textField.text = '%d/%d' % (self.enhanceData[i][j]['curPoint'], self.enhanceData[i][j]['maxPoint'])
                extraInfo = {}
                skillId = int(self.lastSelect.data)
                extraInfo['skillId'] = skillId
                extraInfo['skillLv'] = self.getSkillLvFromId(skillId)
                extraInfo['canActivate'] = True
                extraInfo['state'] = state
                extraInfo['enhancePoint'] = self.enhanceData[i][j]['curPoint']
                TipManager.addTipByType(xiuLianMc, tipUtils.TYPE_SKILL_ENHANCE, {'part': int(xiuLianMc.part),
                 'extraInfo': extraInfo})
                if j < 2:
                    leftCount += self.enhanceData[i][j]['curPoint']
                if j == 2:
                    middleCount += self.enhanceData[i][j]['curPoint']
                if j > 2 and j < 5:
                    rightCount += self.enhanceData[i][j]['curPoint']
                if i > 0:
                    line = self.xiuLianPanel.xiuLianPointDetail.getChildByName('line%d%d%d%d' % (i - 1,
                     j,
                     i,
                     j))
                    if self.enhanceData[i][j]['prePoint']:
                        if line:
                            line.visible = True
                            if self.enhanceData[i][j]['curPoint']:
                                line.gotoAndStop('liantong_now')
                            else:
                                line.gotoAndStop('liantong_no')
                    elif line:
                        line.gotoAndStop('noActivating')
                        line.visible = True

        branchNames = gameStrings.COMMON_SKILL_SHARE_BRANCH_NAMES.get(self.school, [])
        branchCount = [leftCount, middleCount, rightCount]
        for i in xrange(len(branchNames)):
            valText = self.xiuLianPanel.xiuLianPointDetail.getChildByName('xiuLianVal%d' % (i + 1))
            valText.text = '%s:%d' % (branchNames[i], branchCount[i])

    def relayoutLine(self):
        pos = [201, 268, 335]
        for i in xrange(0, MAX_XIULIAN_COLUMN):
            isHideAll = True
            endLine = self.xiuLianPanel.xiuLianPointDetail.getChildByName('lineEnd%d' % i)
            for j in xrange(0, MAX_XIULIAN_ROW):
                visible = self.enhanceData[j][i]['visible']
                if visible:
                    isHideAll = False
                if visible:
                    endLine.x = pos[j]
                for j in xrange(0, MAX_XIULIAN_ROW):
                    visible = self.enhanceData[j][i]['visible']
                    if visible:
                        break
                    else:
                        line = self.xiuLianPanel.xiuLianPointDetail.getChildByName('line%d%d%d%d' % (j - 1,
                         i,
                         j,
                         i))
                        if line:
                            line.visible = False

                if isHideAll:
                    endLine.x = pos[0]

    def getXiuLianPoint(self):
        info = {}
        self.getUsedXiuLianPoint()
        info['usedEnhPoint'] = self.usedXiulianPoint
        info['curEnhPoint'] = self.sharedSkillData.get('totalSkillEnhancePoint', 0)
        jingjie = self.sharedSkillData.get('jingjie', 0)
        lv = self.sharedSkillData.get('lv', 79)
        info['totalEnhPoint'] = SEJD.data.get((jingjie, lv), {}).get('maxEnhancePoint', 0)
        return info

    def setXiuLianPoint(self):
        info = self.getXiuLianPoint()
        self.xiuLianPanel.xiuLianPoint.pointText.text = gameStrings.XIU_LIAN_POINT_TXT % (info['usedEnhPoint'], info['curEnhPoint'], info['totalEnhPoint'])
        tipsStr = gameStrings.XIU_LIAN_POINT_TIP % (info['usedEnhPoint'], info['curEnhPoint'], info['totalEnhPoint'])
        TipManager.addTip(self.xiuLianPanel.xiuLianPoint, tipsStr)

    def getEnhanceLvInfo(self):
        ret = {}
        totalPoint = self.sharedSkillData.get('totalSkillEnhancePoint', 0)
        enhanceLv = utils.getSkillEnhanceLvByTotalPoint(totalPoint)
        ret['curEnhanceLv'] = enhanceLv
        ret['totalSkillEnhancePoint'] = totalPoint
        info = gameglobal.rds.ui.skill.getEnhanceInfo(self.school, enhanceLv, totalPoint)
        ret['info'] = info
        return ret

    def setEnhanceLvInfo(self):
        enhanceLvInfo = self.getEnhanceLvInfo()
        self.enhanceLvInfo = enhanceLvInfo
        i = 0
        while i < enhanceLvInfo['curEnhanceLv'] - 2:
            processBar = self.xiuLianPanel.getChildByName('p%d' % i)
            if processBar:
                processBar.currentValue = enhanceLvInfo['info'][i]['curVal']
                processBar.maxValue = enhanceLvInfo['info'][i]['maxVal']
                TipManager.addTip(processBar, gameStrings.XIU_LIAN_GOTTEN % enhanceLvInfo['totalSkillEnhancePoint'])
            processBar.lableVisible = False
            icon = self.xiuLianPanel.getChildByName('p%dIcon' % i)
            if icon:
                icon.gotoAndStop('actived')
            i += 1

        if i == 5:
            return
        processBar = self.xiuLianPanel.getChildByName('p%d' % i)
        if processBar:
            processBar.currentValue = enhanceLvInfo['info'][i]['curVal']
            processBar.maxValue = enhanceLvInfo['info'][i]['maxVal']
            processBar.lableVisible = False
            TipManager.addTip(processBar, gameStrings.XIU_LIAN_GOTTEN % enhanceLvInfo['totalSkillEnhancePoint'])
        icon = self.xiuLianPanel.getChildByName('p%dIcon' % i)
        if icon:
            icon.gotoAndStop('actived')
            TipManager.addTip(icon, enhanceLvInfo['info'][i]['desc'])
        i += 1
        icon = self.xiuLianPanel.getChildByName('p%dIcon' % i)
        if icon:
            if enhanceLvInfo['info'][i - 1]['curVal'] == enhanceLvInfo['info'][i - 1]['maxVal']:
                icon.gotoAndStop('actived')
            elif enhanceLvInfo['info'][i - 1]['curVal'] == enhanceLvInfo['info'][i - 1]['activeVal']:
                icon.gotoAndStop('activing')
            else:
                icon.gotoAndStop('needActive')
            TipManager.addTip(icon, enhanceLvInfo['info'][i]['desc'])
        processBar = self.xiuLianPanel.getChildByName('p%d' % i)
        if processBar:
            processBar.currentValue = enhanceLvInfo['info'][i]['curVal']
            processBar.maxValue = enhanceLvInfo['info'][i]['maxVal']
            processBar.lableVisible = False
        i += 1
        for i in xrange(i, 5):
            processBar = self.xiuLianPanel.getChildByName('p%d' % i)
            if processBar:
                processBar.currentValue = enhanceLvInfo['info'][i]['curVal']
                processBar.maxValue = enhanceLvInfo['info'][i]['maxVal']
                processBar.lableVisible = False
            icon = self.xiuLianPanel.getChildByName('p%dIcon' % i)
            if icon:
                icon.gotoAndStop('needActive')
                TipManager.addTip(icon, enhanceLvInfo['info'][i]['desc'])

    def setSkillSlotByData(self, slot, skillId, lv):
        slot.changeNum.visible = False
        avatarLv = self.sharedSkillData.get('level', 1)
        learnLv = SGD.data.get((skillId, 1), {}).get('learnLv', 1)
        if avatarLv < learnLv:
            slot.icon.setSlotState(3)
            slot.numDesc.textField.text = gameStrings.SKILL_LEARN_LV_REQUIRE % learnLv
        else:
            slot.icon.setSlotState(1)
            slot.numDesc.textField.text = '%d/%d' % (lv, self.maxSkillLevel)
        sd = skillDataInfo.ClientSkillInfo(skillId)
        icon = sd.getSkillData('icon', None)
        data = {'iconPath': 'skill/icon/%s.dds' % icon}
        slot.icon.setItemSlotData(data)
        slot.icon.dragable = False
        skillName = SGTD.data.get(skillId, {}).get('name', '')
        slot.label = skillName
        slot.icon.validateNow()
        TipManager.addTipByType(slot, tipUtils.TYPE_SKILL, {'skillId': skillId,
         'lv': lv,
         'extraInfo': {'isOnlyDetail': True}})

    def initFilter(self):
        self.skillPanel = self.widget.skillPanel.skillPanel
        panel = self.skillPanel
        panel.filter.menuRowCount = len(self.filterMode)
        panel.filter.addEventListener(events.INDEX_CHANGE, self.handleFilterIndexChange)
        ASUtils.setDropdownMenuData(panel.filter, self.filterMode)
        panel.filter.selectedIndex = self.currentMode

    def handleFilterIndexChange(self, *args):
        panel = self.skillPanel
        self.currentMode = self.filterMode[panel.filter.selectedIndex]['mode']
        self.setSkillPanel()

    def isAutoLvUp(self, pskId):
        pskInfo = PSkillInfo(pskId, 1)
        return pskInfo.getSkillData('autoLvUp', 0)

    def getPSkillLvStr(self, skillId, skillLv = 0):
        p = BigWorld.player()
        if self.isAutoLvUp(skillId):
            pskillInfo = PSkillInfo(skillId, 1)
        else:
            pskillInfo = PSkillInfo(skillId, min(skillLv + 1, const.MAX_SKILL_LEVEL))
        learnEnhanceLv = pskillInfo.getSkillData('learnEnhanceLv', 0)
        totalSkillEnhancePoint = self.sharedSkillData.get('totalSkillEnhancePoint', 0)
        enhanceLv = utils.getSkillEnhanceLvByTotalPoint(totalSkillEnhancePoint)
        if learnEnhanceLv and enhanceLv < learnEnhanceLv:
            skLvStr = gameStrings.PSKILL_LEARNED_XIU_LIAN_REQUIRE % SELD.data.get(learnEnhanceLv, {}).get('name', '')
        elif skillLv == 0:
            skLvStr = gameStrings.PSKILL_LEARNED_LV_REQUIRE % PD.data.get((skillId, 1), {}).get('learnLv', 1)
        else:
            skLvStr = gameStrings.PSKILL_LEARNED
        return skLvStr

    def getPskillLevel(self, psId):
        pskills = self.sharedSkillData.get('pskill', [])
        level = 0
        for pskillItem in pskills:
            if psId == pskillItem[0]:
                level = pskillItem[1]
                break

        return level

    def isPskillLearned(self, psId):
        pskills = self.sharedSkillData.get('pskill', [])
        isLearned = False
        for pskillItem in pskills:
            if psId == pskillItem[0] and pskillItem[2]:
                isLearned = True
                break

        return isLearned

    def setSkillPanel(self):
        panel = self.skillPanel.panel
        self.usedXiulianPoint = 0
        panel.gotoAndStop('school_%d' % self.school)
        skillInfo = self.skillModeInfo.get(self.currentMode, {}).get('skillInfo', {})
        for i in xrange(0, MAX_SKILL_NUM):
            skillSlot = panel.getChildByName('skill%d' % i)
            skillId = self.skillIdList[i]
            self.setSkillSlotByData(skillSlot, skillId, self.getSkillLvFromId(skillId))
            childIdList = self.childSkillIdDict.get(skillId, [])
            if childIdList:
                for j in xrange(0, len(childIdList)):
                    childSkillId = childIdList[j]
                    childSkillSlot = panel.getChildByName('subSkill%d%d' % (i, j))
                    if not childSkillSlot:
                        continue
                    self.setSkillSlotByData(childSkillSlot, childSkillId, self.getSkillLvFromId(skillId))

        posX = 0
        for i in xrange(0, len(self.psSkillIdList)):
            pskillItem = self.widget.getInstByClsName(SKILL_SLOT_NAME)
            self.skillPanel.pskillCanvas.addChild(pskillItem)
            pskillItem.x = posX
            posX += pskillItem.width + 3
            pskillId = self.psSkillIdList[i]
            psSkillInfo = self.skillManager.pSkillIns.getSkillItemInfo(pskillId)
            name = psSkillInfo.get('skillName', '')
            pskillItem.label = name
            pskillItem.validateNow()
            pskillItem.mouseChildren = True
            data = psSkillInfo.get('icon', {})
            pskillItem.icon.setItemSlotData(data)
            isLearned = self.isPskillLearned(pskillId)
            skillLv = self.getPskillLevel(pskillId)
            psSkillInfo['skLvStr'] = self.getPSkillLvStr(pskillId, skillLv)
            if not isLearned:
                pskillItem.icon.setSlotState(3)
            else:
                pskillItem.icon.setSlotState(1)
            pskillItem.icon.dragable = False
            pskillItem.numDesc.textField.text = psSkillInfo.get('skLvStr', '')
            pskillItem.icon.iconFitSize = True
            pskillItem.changeNum.visible = False
            pskillItem.icon.validateNow()
            TipManager.addTipByType(pskillItem.icon, tipUtils.TYPE_SKILL, {'skillId': pskillId,
             'isPSkill': True,
             'lv': skillLv if skillLv else 1})

        if not self.isXiulianEnabled():
            startJingJie = SCD.data.get('startJingJie', 3)
            jName = JJD.data.get(startJingJie, {}).get('name', '')
            self.skillPanel.xiuLianTips.text = gameStrings.XIU_LIAN_BTN_TIP % jName
        else:
            self.skillPanel.xiuLianTips.visible = False
        self.skillPanel.xiuLianBtn.addEventListener(events.MOUSE_CLICK, self.handleClickXiuLian)
        self.skillPanel.skillPoint.visible = False
        self.skillPanel.pointIcon.visible = False

    def isXiulianEnabled(self):
        jingjie = self.sharedSkillData.get('jingjie', 0)
        if jingjie < SCD.data.get('startJingJie', 3):
            return False
        return True

    def handleClickXiuLian(self, *args):
        if not self.isXiulianEnabled():
            BigWorld.player().showGameMsg(GMDD.data.SKILL_XIU_LIAN_FAILED_LESS_JING_JIE, (JJD.data.get('startJingJie', {}).get('name', ''),))
            return
        self.currentSkillState = XIU_LIAN_STATE
        self.widget.skillPanel.gotoAndStop('xiuLian')
        self.initUI()

    def handleGoBack(self, *args):
        self.currentSkillState = SKILL_STATE
        self.widget.skillPanel.gotoAndStop('commonSkill')
        self.initUI()

    def handleWheel(self, *args):
        e = ASObject(args[3][0])
        if e.delta > 0:
            self.handleNextClick(None)
        elif e.delta < 0:
            self.handlePrevClick(None)

    def handleClickItem(self, *args):
        e = ASObject(args[3][0])
        if self.lastSelect == e.currentTarget:
            return
        index = 0
        self.lastSelect.selected = False
        self.lastSelect = e.currentTarget
        self.lastSelect.selected = True
        self.setSkillDetail()
        self.setSkillPracticeInfo()

    def handlePrevClick(self, *args):
        newX = 0
        if self.isNextTweenerRunning:
            return
        if self.isPreTweenerRunning:
            return
        self.isPreTweenerRunning = True
        self.moveTimeCnt += 1
        newX = min(self.canvasInitX + self.moveTimeCnt * SKILL_ITEM_WIDTH, self.canvasInitX)
        if self.oldPrevX == newX:
            self.moveTimeCnt -= 1
            self.isPreTweenerRunning = False
            return
        self.oldNextX = 0
        Tweener.addTween(self.xiuLianPanel.canvas, {'x': newX,
         'y': self.xiuLianPanel.canvas.y,
         'time': 0.4,
         'transition': 'linear',
         'onComplete': self.setXiuLianPreTweenEnd,
         'onCompleteParams': (newX,)})

    def handleNextClick(self, *args):
        newX = 0
        if self.isPreTweenerRunning:
            return
        if self.isNextTweenerRunning:
            return
        self.isNextTweenerRunning = True
        self.moveTimeCnt -= 1
        newX = max(self.canvasInitX + self.moveTimeCnt * SKILL_ITEM_WIDTH, MAX_CANVAS_WIDTH - self.xiuLianPanel.canvas.width)
        if self.oldNextX == newX:
            self.moveTimeCnt += 1
            self.isNextTweenerRunning = False
            return
        self.oldPrevX = 0
        Tweener.addTween(self.xiuLianPanel.canvas, {'x': newX,
         'y': self.xiuLianPanel.canvas.y,
         'time': 0.4,
         'transition': 'linear',
         'onComplete': self.setXiuLianNextTweenEnd,
         'onCompleteParams': (newX,)})

    def setXiuLianNextTweenEnd(self, *args):
        newX = int(args[3][0].GetNumber())
        self.isNextTweenerRunning = False
        self.oldNextX = newX

    def setXiuLianPreTweenEnd(self, *args):
        newX = int(args[3][0].GetNumber())
        self.isPreTweenerRunning = False
        self.oldPreX = newX

    def handleClickGotoWeb(self, *args):
        skillId = int(self.lastSelect.data)
        gameglobal.rds.ui.skill.gotoWeb(skillId)

    def unRegisterPanel(self):
        self.widget = None
        self.sharedSkillData = None
        self.skillIdList = []
        self.psSkillIdList = []
        self.school = 0
        self.maxSkillLevel = 0
        self.skillModeInfo = {}
        self.currentMode = 0
        self.skillManager = None
        self.xiuLianPanel = None
        self.skillPanel = None
        self.lastSelect = None
        self.canvasInitX = 0
        self.moveTimeCnt = 0
        self.oldNextX = 0
        self.oldPrevX = 0
        self.isNextTweenerRunning = False
        self.isPreTweenerRunning = False
        self.currentSkillState = SKILL_STATE
        self.childSkillIdDict = {}
        self.filterMode = []
        self.usedXiulianPoint = 0
