#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/roleInformationJunjieProxy.o
import BigWorld
import gameglobal
import gametypes
import uiConst
import uiUtils
import const
import utils
import events
import clientUtils
import skillDataInfo
import math
import formula
from guis.asObject import TipManager
from guis.asObject import MenuManager
from guis.asObject import ASObject
from guis.asObject import ASUtils
from gameclass import PSkillInfo
from uiProxy import UIProxy
from guis import activityFactory
from gameStrings import gameStrings
from data import junjie_config_data as JCD
from data import famous_general_lv_data as FGLD
from data import famous_general_config_data as FGCD
from data import quest_data as QD
from data import sys_config_data as SCD
from data import seeker_data as SEEKD
from data import npc_data as ND
from data import activity_state_config_data as ASCD
from data import activity_basic_data as ABD
from data import world_war_config_data as WWCD
from data import stats_target_data as STD
from cdata import game_msg_def_data as GMDD
from data import famous_general_zhanxun_rank_data as FGZRD
JUN_JIE_ACTIVITY_ITEM = 'RoleInformationJunjieV1_JunjieItem'
SKILL_SLOT_MAX_NUM = 6
STAR_NUM = 3
TIP_MAX_WIDTH = 200
MAX_JUN_JIE_LV = 10
INIT_FAMOUS_LV = 1
MAX_NEXT_JUNJIE_ITEMS = 4
PROGRESS_X = 193
PROGRESS_WIDTH = 399
MING_JIANG_PROGRESS_X = 243
MING_JIANG_PROGRESS_WIDTH = 350
ABANDOND_LVS = (99, 100)
FAMOUS_TIP_Y = 47
JUNJIE_TIP_Y = 39
MOST_HIGH_FAMOUS_LV = 19
SKILL_TIP_LINES = 3
SKILL_TIP_BG_WIDTH = 170

class RoleInformationJunjieProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RoleInformationJunjieProxy, self).__init__(uiAdapter)
        self.widget = None
        self.junziWeekVal = 0
        self.nowLevelData = {}
        self.nextLevelData = {}
        self.curZhanXunFame = 0
        self.zhanXunRequire = False
        self.lvRequire = False
        self.questRequire = False
        self.zhanXunRequire = False
        self.maxLvNum = 0
        self.awardInfo = {}
        self.selectedSkillId = 0
        self.selectedLv = 0
        self.skillPanel = None
        self.lvUpRewardPanel = None
        self.maxLvNextReward = None
        self.nextReward = None
        self.extraExp = 0
        self.stage = -1
        self.famousSeasonNum = -1
        self.actFactory = activityFactory.getInstance()
        self.sortedAct = sorted(ABD.data.iteritems(), key=lambda d: d[1]['sortedId'])

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()
        self.initStage()

    def unRegisterPanel(self):
        self.widget = None
        self.selectedSkillId = 0
        self.selectedLv = 0
        self.skillPanel = None
        self.lvUpRewardPanel = None
        self.maxLvNextReward = None
        self.nextReward = None
        self.famousSeasonNum = -1

    def initStage(self):
        BigWorld.player().cell.queryFamousGeneralSeasonStage()

    def initUI(self):
        if not self.widget:
            return
        p = BigWorld.player()
        lv = p.junJieLv
        famousGeneralLv = p.famousGeneralLv
        self.nowLevelData = JCD.data.get(lv, {})
        self.nextLevelData = JCD.data.get(lv + 1, {})
        self.curZhanXunFame = p.getFame(const.ZHAN_XUN_FAME_ID)
        self.weekZhanxunFame = p.fameWeek.get(const.ZHAN_XUN_FAME_ID, (0, 0))
        self.nowFamousLevelData = FGLD.data.get(famousGeneralLv, {})
        self.widget.questPanel.visible = False
        self.widget.panel.saveTempBtn.visible = False
        if p.famousGeneralLv:
            self.widget.panel.gotoAndStop('mingjiang')
            self.refreshExtraExp()
            self.initFamousInfo()
            self.initFamousSkillArea()
            self.setFamousGeneralVal()
            self.queryForFamousVal()
            self.refreshMingJiangVisible(not p.isUsingTemp())
        else:
            self.widget.panel.gotoAndStop('junjie')
            self.initJunJieInfo()
            self.widget.panel.nextReward.visible = False
            self.widget.panel.maxLvNextReward.visible = False
            self.nextReward = self.widget.panel.nextReward
            self.maxLvNextReward = self.widget.panel.maxLvNextReward
            if p.junJieLv >= MAX_JUN_JIE_LV:
                p.cell.queryFullJunjieCnt()
                self.initNextJunjieInfoMax()
            else:
                self.initNextJunjieInfo()
        self.initJunzi()
        self.initWeekReward()
        self.initActivityPanel()

    def refreshMingJiangVisible(self, visible):
        self.widget.panel.famousMaxVal.visible = visible
        self.widget.panel.zhanxunRankBtn.visible = visible
        self.widget.panel.famousInfo.visible = visible
        self.widget.panel.lvUpBtn.visible = visible
        self.widget.panel.lvUpRewardBtn.visible = visible
        self.widget.panel.famousRankBtn.visible = visible
        self.widget.panel.famousIntro.visible = visible
        self.widget.panel.weekJunjieActivity.visible = visible
        self.widget.panel.saveTempBtn.visible = not visible
        self.widget.panel.getBtn.visible = visible
        self.widget.panel.getExtraBtn.visible = visible
        self.widget.panel.findNpc.visible = visible
        self.widget.panel.nulinScoreNpc.visible = visible
        self.widget.panel.saveTempBtn.addEventListener(events.BUTTON_CLICK, self.onSaveTempBtnClick)

    def onSaveTempBtnClick(self, *args):
        p = BigWorld.player()
        if p.isInPUBG():
            p.cell.saveCharTempFGSkillScheme(gametypes.CHAR_TEMP_TYPE_PUBG, 1)
        else:
            p.cell.saveCharTempFGSkillScheme(gametypes.CHAR_TEMP_TYPE_ARENA, 1)

    def initJunJieInfo(self):
        p = BigWorld.player()
        self.widget.panel.junjieName.text = self.nowLevelData.get('name', '')
        maxJunJieLimit = self.nowLevelData.get('maxJunJieLimit', 0)
        if p.junJieLv >= MAX_JUN_JIE_LV:
            needJunJie = FGCD.data.get('needZhanxun2Promote', 0)
        else:
            needJunJie = self.getLvUpNeedZhanXun()
        self.widget.panel.progress.currentValue = self.curZhanXunFame * 100.0 / needJunJie
        tipStr = gameStrings.JUNJIE_PROGRESS_TIP % (self.curZhanXunFame, needJunJie)
        self.widget.panel.tip.tiptext.text = tipStr
        self.widget.panel.tip.tiptext.width = self.widget.panel.tip.tiptext.textWidth + 5
        self.widget.panel.tip.tipbg.width = self.widget.panel.tip.tiptext.textWidth + 10
        maxProgressX = PROGRESS_WIDTH - self.widget.panel.tip.tipbg.width + PROGRESS_X
        tipX = PROGRESS_X + PROGRESS_WIDTH * self.curZhanXunFame * 1.0 / needJunJie
        self.widget.panel.tip.x = tipX if tipX < maxProgressX else maxProgressX
        self.widget.panel.tip.y = JUNJIE_TIP_Y
        self.widget.panel.junjieLvUpBtn.addEventListener(events.MOUSE_CLICK, self.handleClickJunjieLvUpBtn)
        self.widget.panel.bigIcon.loadImage('junjie/%d.dds' % self.nowLevelData.get('icon', 0))

    def initFamousInfo(self):
        p = BigWorld.player()
        self.widget.panel.famousName.text = self.nowFamousLevelData.get('name', '')
        needFamousGeneralVal = self.nowFamousLevelData.get('needFamousGeneralVal', 1)
        tipStr = gameStrings.FAMOUS_PROGRESS_TIP % (p.famousGeneralVal, needFamousGeneralVal)
        self.widget.panel.progress.currentValue = p.famousGeneralVal * 100.0 / needFamousGeneralVal
        self.widget.panel.tip.tiptext.text = tipStr
        self.widget.panel.tip.tiptext.width = self.widget.panel.tip.tiptext.textWidth + 5
        self.widget.panel.tip.tipbg.width = self.widget.panel.tip.tiptext.textWidth + 10
        tipX = MING_JIANG_PROGRESS_X + MING_JIANG_PROGRESS_WIDTH * p.famousGeneralVal * 1.0 / needFamousGeneralVal
        maxProgressX = MING_JIANG_PROGRESS_WIDTH - self.widget.panel.tip.tipbg.width + MING_JIANG_PROGRESS_X
        self.widget.panel.tip.x = tipX if tipX < maxProgressX else maxProgressX
        self.widget.panel.tip.y = FAMOUS_TIP_Y
        self.widget.panel.lvUpRewardBtn.addEventListener(events.MOUSE_CLICK, self.handleClickLvUpRewardBtn)
        self.widget.panel.famousRankBtn.addEventListener(events.MOUSE_CLICK, self.handleClickRank)
        self.widget.panel.zhanxunRankBtn.addEventListener(events.MOUSE_CLICK, self.handleClickRank)
        self.widget.panel.famousIntro.addEventListener(events.MOUSE_CLICK, self.handleClickFamousIntro)
        self.widget.panel.famousInfo.addEventListener(events.MOUSE_CLICK, self.handleClickFamousInfo)
        self.widget.panel.lvUpBtn.addEventListener(events.MOUSE_CLICK, self.handleClickLvUpBtn)
        self.widget.panel.lvUpRewardPanel.visible = False
        self.lvUpRewardPanel = self.widget.panel.lvUpRewardPanel
        starNum = p.famousGeneralLv % STAR_NUM if p.famousGeneralLv % STAR_NUM else STAR_NUM
        if p.famousGeneralLv >= MOST_HIGH_FAMOUS_LV:
            self.widget.panel.starNumArea.starNums.text = 'x%d' % (p.famousGeneralLv - MOST_HIGH_FAMOUS_LV + 1)
            self.widget.panel.starArea.visible = False
            self.widget.panel.starNumArea.visible = True
        else:
            for i in xrange(0, STAR_NUM):
                if i < starNum:
                    self.widget.panel.starArea.getChildByName('star%d' % i).gotoAndStop('you')
                else:
                    self.widget.panel.starArea.getChildByName('star%d' % i).gotoAndStop('wu')

            self.widget.panel.starNumArea.visible = False
            self.widget.panel.starArea.visible = True
        lvState = p.famousGeneralLv / STAR_NUM if starNum < STAR_NUM else p.famousGeneralLv / STAR_NUM - 1
        if lvState >= SKILL_SLOT_MAX_NUM:
            lvState = SKILL_SLOT_MAX_NUM - 1
        self.widget.panel.bigIcon.gotoAndStop('lv%d' % lvState)
        if p.famousGeneralVal < needFamousGeneralVal:
            self.widget.panel.lvUpBtn.enabled = False
        self.initSeasonTime()

    def initSeasonTime(self):
        if self.widget and self.widget.panel.seasonNum and self.widget.panel.startTime:
            if self.famousSeasonNum < 0:
                famousSeasonNum = FGCD.data.get('famousSeasonNum', 0)
            else:
                famousSeasonNum = self.famousSeasonNum
            seasonTimes = FGCD.data.get('seasonTimes', [])[famousSeasonNum - 1]
            seasonInfo = seasonTimes.split(' ')
            self.widget.panel.seasonNum.text = seasonInfo[0]
            self.widget.panel.startTime.text = gameStrings.FAMOUS_SEASON_TIME % seasonInfo[1].split('-')[0]
            self.widget.panel.startTime.visible = False

    def refreshExtraExp(self):
        p = BigWorld.player()
        if not self.widget or not p.famousGeneralLv:
            return
        self.extraExp = utils.calcFamousGeneralWeekRatio()
        if self.extraExp > 1:
            self.widget.panel.exp.visible = True
            self.widget.panel.exp.times.text = 'x%.1f' % self.extraExp
            self.widget.panel.exp.icon.gotoAndStop('exp')
        else:
            self.widget.panel.exp.visible = False

    def refreshFamousLvUpReward(self):
        p = BigWorld.player()
        famousGeneralLv = p.famousGeneralLv
        bonusId = FGLD.data.get(famousGeneralLv, {}).get('bonusId', 0)
        if not bonusId:
            return
        itemInfo = self.getItemInfoFromBonusId(bonusId)
        self.widget.panel.lvUpRewardPanel.slot.setItemSlotData(itemInfo)

    def getItemInfoFromBonusId(self, bonusId):
        itemBonus = clientUtils.genItemBonus(bonusId)
        return uiUtils.getGfxItemById(itemBonus[0][0], itemBonus[0][1])

    def initFamousSkillArea(self):
        if not self.widget:
            return
        p = BigWorld.player()
        if not p.famousGeneralLv:
            return
        self.widget.panel.skillPanel.visible = False
        self.skillPanel = self.widget.panel.skillPanel
        for i in xrange(0, SKILL_SLOT_MAX_NUM):
            skillItem = self.widget.panel.getChildByName('skill%d' % i)
            skillItem.item.gotoAndStop('state%d' % i)
            skillItem.gotoAndStop('you')
            ASUtils.setHitTestDisable(skillItem.item.slot.word, True)
            skillItem.item.slot.addEventListener(events.MOUSE_CLICK, self.handleClickSkill)
            skillItem.item.slot.word.txt.text = gameStrings.FAMOUS_SKILL_AVALIABLE
            for i in xrange(0, STAR_NUM):
                skillItem.item.getChildByName('star%d' % i).gotoAndStop('you')

            skillItem.item.slot.slot.keyBind.visible = False

        maxFamousGeneralLv = SKILL_SLOT_MAX_NUM * STAR_NUM
        famousGeneralLv = p.famousGeneralLv if p.famousGeneralLv <= maxFamousGeneralLv else maxFamousGeneralLv
        skillItemNum = int(famousGeneralLv / STAR_NUM)
        starNum = famousGeneralLv % STAR_NUM
        if starNum:
            skillItem = self.widget.panel.getChildByName('skill%d' % skillItemNum)
            for i in xrange(starNum, STAR_NUM):
                skillItem.item.getChildByName('star%d' % i).gotoAndStop('wu')

        if starNum:
            greySkillNum = skillItemNum + 1
        else:
            greySkillNum = skillItemNum
        for i in xrange(greySkillNum, SKILL_SLOT_MAX_NUM):
            skillItem = self.widget.panel.getChildByName('skill%d' % i)
            for j in xrange(0, STAR_NUM):
                skillItem.item.getChildByName('star%d' % j).gotoAndStop('wu')

            skillItem.gotoAndStop('bukexuan')
            skillItem.item.slot.word.txt.text = gameStrings.FAMOUS_SKILL_NOT_AVALIABLE

        for lv, skillInfo in self.awardInfo.iteritems():
            skillItem = self.widget.panel.getChildByName('skill%d' % lv)
            if not skillItem:
                continue
            skillId = skillInfo.get('pskillId', 0)
            tWhen = skillInfo.get('tWhen', 0)
            skillItem.item.slot.word.visible = False
            skillItem.item.slot.bg.visible = False
            skillItem.item.slot.slot.binding = 'famousSkill.%d' % skillId
            pSkillInfo = PSkillInfo(skillId, 1)
            icon = pSkillInfo.getSkillData('icon', 'notFound')
            iconPath = 'skill/icon/' + str(icon) + '.dds'
            skillItem.item.slot.slot.data = {'skillId': skillId,
             'famousLv': lv,
             'iconPath': iconPath,
             'tWhen': tWhen}

        ASUtils.setHitTestDisable(self.widget.panel.extraSlot.word, True)
        self.widget.panel.extraSlot.word.visible = True
        self.widget.panel.extraSlot.slot.keyBind.visible = False
        self.widget.panel.extraSlot.slot.addEventListener(events.MOUSE_CLICK, self.handleExtraSlotClick, False, 0, True)
        extraInfo = self.awardInfo.get(gametypes.FAMOUS_GENERAL_LV_DEFAULT_2_KEY_LV / 3, {})
        if extraInfo:
            skillId = extraInfo.get('pskillId', 0)
            tWhen = extraInfo.get('tWhen', 0)
            self.widget.panel.extraSlot.slot.binding = 'famousSkill.%d' % skillId
            pSkillInfo = PSkillInfo(skillId, 1)
            icon = pSkillInfo.getSkillData('icon', 'notFound')
            iconPath = 'skill/icon/' + str(icon) + '.dds'
            self.widget.panel.extraSlot.slot.data = {'skillId': skillId,
             'iconPath': iconPath,
             'tWhen': tWhen}
            self.widget.panel.extraSlot.word.visible = False

    def initJunzi(self):
        if not self.widget:
            return
        p = BigWorld.player()
        nowJunzi = p.getFame(const.JUN_ZI_FAME_ID)
        thisWeekJunzi = self.nowLevelData.get('maxJunZi', 0) * p.getMaxJunziRate()
        extraJunzi = self.nowLevelData.get('extraJunZi', 0)
        curMaxJunZi = self.getCurMaxJunZi() if self.getCurMaxJunZi() > 0 else thisWeekJunzi + extraJunzi
        self.widget.panel.junziScore.text = nowJunzi
        self.widget.panel.weekJunzi.text = gameStrings.WEEK_JUNZI % self.junziWeekVal
        self.widget.panel.weekJunziLimit.text = gameStrings.WEEK_JUNZI_MAX % curMaxJunZi
        TipManager.addTip(self.widget.panel.junziScore, gameStrings.JUN_ZI_TIP)
        TipManager.addTip(self.widget.panel.junziIcon, gameStrings.JUN_ZI_TIP)
        seekNpcId = FGCD.data.get('junziNpcId', 0)
        npcId = SEEKD.data.get(seekNpcId, {}).get('npcId', 0)
        budNpcLink = ''
        npcName = ''
        if npcId == 0:
            npcName = SEEKD.data.get(seekNpcId, {}).get('name', gameStrings.OTHER)
        else:
            npcName = ND.data.get(npcId, {}).get('name', gameStrings.OTHER)
            budNpcLink = 'seek:%d' % seekNpcId
        self.widget.panel.nulinScoreNpc.htmlText = gameStrings.NUL_IN_SCORE_NPC % (budNpcLink, npcName)
        self.widget.panel.findNpc.data = seekNpcId
        self.widget.panel.findNpc.x = self.widget.panel.nulinScoreNpc.x + self.widget.panel.nulinScoreNpc.textWidth + 5
        self.widget.panel.findNpc.addEventListener(events.MOUSE_CLICK, self.handleClickFindNpc)

    def initNextJunjieInfoMax(self):
        if not self.widget:
            return
        maxLvNumReach = False
        zhanXunReach = False
        if not self.isCloseToNextSeason():
            self.widget.panel.lvRequire.text = gameStrings.MAX_JUN_JIE_NUM_REQUIRE % FGCD.data.get('needFullJunjieLvCnt', 0)
            if self.maxLvNum >= FGCD.data.get('needFullJunjieLvCnt', 0):
                self.widget.panel.isLvReach.gotoAndStop('lvgou')
                maxLvNumReach = True
            else:
                self.widget.panel.isLvReach.gotoAndStop('wenzi')
                self.widget.panel.isLvReach.txt.text = '(%d/%d)' % (self.maxLvNum, FGCD.data.get('needFullJunjieLvCnt', 0))
                maxLvNumReach = False
        else:
            self.widget.panel.isLvReach.visible = False
            self.widget.panel.lvRequire.text = gameStrings.FAMOUS_CLOSE_TO_NEXT_SEASON_REQUIRE
            maxLvNumReach = False
        self.widget.panel.activityRequire.text = gameStrings.MAX_JUN_JIE_ZHAN_XUN_REQUIRE % FGCD.data.get('needZhanxun2Promote', 0)
        if self.curZhanXunFame >= FGCD.data.get('needZhanxun2Promote', 0):
            zhanXunReach = True
            self.widget.panel.isActivityReach.gotoAndStop('lvgou')
        else:
            zhanXunReach = False
            self.widget.panel.isActivityReach.gotoAndStop('wenzi')
            self.widget.panel.isActivityReach.txt.text = '(%d/%d)' % (self.curZhanXunFame, FGCD.data.get('needZhanxun2Promote', 0))
        self.widget.panel.zhanxunRequire.visible = False
        self.widget.panel.zhanxunRequireDot.visible = False
        self.widget.panel.isZhanxunReach.visible = False
        self.widget.panel.nextJunjieName.text = FGLD.data.get(INIT_FAMOUS_LV, {}).get('name', '')
        self.widget.panel.nextRewardBtn.addEventListener(events.MOUSE_CLICK, self.handleClickNextRewardBtn)
        if maxLvNumReach and zhanXunReach:
            self.widget.panel.junjieLvUpBtn.enabled = True
        else:
            self.widget.panel.junjieLvUpBtn.enabled = False

    def refreshMaxLvNextReward(self):
        bonusId = FGCD.data.get('promoteBonusId', 0)
        itemInfo = self.getItemInfoFromBonusId(bonusId)
        self.widget.panel.maxLvNextReward.slot.setItemSlotData(itemInfo)

    def initNextJunjieInfo(self):
        p = BigWorld.player()
        self.widget.panel.nextJunjieName.text = self.nextLevelData.get('name', '')
        firstQid = self.nowLevelData.get('questIds', ())[0]
        if self.nowLevelData.get('questDesc', ''):
            self.widget.panel.activityRequire.htmlText = self.nowLevelData.get('questDesc', '')
        else:
            questText = QD.data.get(firstQid, {}).get('shortDesc', '')
            self.widget.panel.activityRequire.htmlText = questText
        isQuestCom = False
        questComNum = 0
        totalQuestNum = len(self.nowLevelData.get('questIds', ()))
        for qid in self.nowLevelData.get('questIds', ()):
            if p.isQuestCompleted(qid) or p.isQuestComplete(qid):
                questComNum += 1

        if questComNum == totalQuestNum:
            isQuestCom = True
        if isQuestCom:
            self.widget.panel.isActivityReach.gotoAndStop('lvgou')
            self.widget.panel.activityRequire.text = gameStrings.JUN_JIE_ACT_REQUIRED
            self.questRequire = True
        else:
            self.questRequire = False
            self.widget.panel.isActivityReach.gotoAndStop('wenzi')
            self.widget.panel.isActivityReach.txt.text = '(%d/%d)' % (questComNum, totalQuestNum)
        lvRequire = QD.data.get(firstQid, {}).get('comMinLv', 0)
        if p.lv >= lvRequire:
            self.lvRequire = True
            self.widget.panel.isLvReach.gotoAndStop('lvgou')
            self.widget.panel.lvRequire.text = gameStrings.JUN_JIE_LV_REQUIRED
        else:
            self.lvRequire = False
            self.widget.panel.isLvReach.gotoAndStop('wenzi')
            self.widget.panel.lvRequire.text = gameStrings.JUN_JIE_LV_NOT_REQUIRE
            self.widget.panel.isLvReach.txt.text = '(%d/%d)' % (p.lv, lvRequire)
        curWeeksZhanxunRequire = self.getLvUpNeedZhanXun()
        if self.curZhanXunFame >= curWeeksZhanxunRequire:
            self.zhanXunRequire = True
            self.widget.panel.zhanxunRequire.text = gameStrings.JUN_JIE_ZHAN_XUN_REQUIRED
            self.widget.panel.isZhanxunReach.gotoAndStop('lvgou')
        else:
            self.zhanXunRequire = False
            self.widget.panel.isZhanxunReach.gotoAndStop('wenzi')
            self.widget.panel.zhanxunRequire.text = gameStrings.JUN_JIE_ZHAN_XUN_NOT_REQUIRE
            self.widget.panel.isZhanxunReach.txt.text = '(%d/%d)' % (self.curZhanXunFame, curWeeksZhanxunRequire)
        self.widget.panel.nextRewardBtn.addEventListener(events.MOUSE_CLICK, self.handleClickNextRewardBtn)
        if self.zhanXunRequire and self.lvRequire and self.questRequire:
            self.widget.panel.junjieLvUpBtn.enabled = True
        else:
            self.widget.panel.junjieLvUpBtn.enabled = False

    def refreshNextReward(self):
        self.widget.panel.nextReward.nowLevelYunChui.text = self.nowLevelData.get('weekYunChuiScore', 0)
        self.widget.panel.nextReward.nextLevelYunChui.text = self.nextLevelData.get('weekYunChuiScore', 0)
        itemIds = self.nowLevelData.get('itemBuyAvaliable', ())
        for i in xrange(0, len(itemIds)):
            self.widget.panel.nextReward.getChildByName('item%d' % i).setItemSlotData(uiUtils.getGfxItemById(itemIds[i]))
            self.widget.panel.nextReward.getChildByName('item%d' % i).visible = True

        if len(itemIds) < MAX_NEXT_JUNJIE_ITEMS:
            for i in xrange(len(itemIds), MAX_NEXT_JUNJIE_ITEMS):
                self.widget.panel.nextReward.getChildByName('item%d' % i).visible = False

        questIds = self.nowLevelData.get('questIds', ())
        rewardItemId = 0
        for questId in questIds:
            rewardItems = QD.data.get(questId, {}).get('rewardItems', ())
            if rewardItems:
                rewardItemId = rewardItems[0][0]

        self.widget.panel.nextReward.reward.setItemSlotData(uiUtils.getGfxItemById(rewardItemId))

    def initWeekReward(self):
        p = BigWorld.player()
        if not self.widget:
            return
        self.widget.panel.getBtn.addEventListener(events.MOUSE_CLICK, self.handleClickGetBtn)
        getEnabled = False
        if gameglobal.rds.configData.get('enableWingWorld', False):
            rewardZXBonusList = self.nowLevelData.get('wingWorldRewardZXBonusList', [])
            rewardZXScores = self.nowLevelData.get('wingWorldRewardZXScores', [])
        else:
            rewardZXBonusList = self.nowLevelData.get('rewardZXBonusList', [])
            rewardZXScores = self.nowLevelData.get('rewardZXScores', [])
        if len(rewardZXBonusList) == 3:
            self.widget.panel.rewardMC.gotoAndStop('normal')
        elif len(rewardZXBonusList) == 5:
            self.widget.panel.rewardMC.gotoAndStop('wingworld')
        if len(rewardZXScores) == len(rewardZXBonusList):
            for i in xrange(len(rewardZXScores)):
                itemBonus = clientUtils.genItemBonus(rewardZXBonusList[i])
                if len(itemBonus) <= 0:
                    continue
                itemInfo = uiUtils.getGfxItemById(itemBonus[0][0], itemBonus[0][1])
                itemInfo['state'] = uiConst.ITEM_GRAY
                state = rewardZXScores[i]
                arrowState = 'dislight'
                if self.weekZhanxunFame[0] >= rewardZXScores[i]:
                    itemInfo['state'] = uiConst.ITEM_NORMAL
                    if i != 0:
                        arrowState = 'light'
                    getEnabled = True
                    for key, value in p.zhanXunReward.iteritems():
                        if key[1] == i:
                            if value:
                                getEnabled = False

                    if not getEnabled:
                        state = gameStrings.WEEK_REWARD_GETTED
                elif i > 0 and self.weekZhanxunFame[0] > rewardZXScores[i - 1]:
                    arrowState = 'half'
                if i != 0:
                    arrow = self.widget.panel.rewardMC.getChildByName('arrow%d' % i)
                    if arrow:
                        arrow.gotoAndStop(arrowState)
                reward = self.widget.panel.rewardMC.getChildByName('reward%d' % i)
                if reward:
                    reward.slot.setItemSlotData(itemInfo)
                    reward.slotEx.visible = False
                    reward.state.text = state

        self.widget.panel.getBtn.enabled = getEnabled
        self.setExtraReward()
        self.widget.panel.weekRewardYunChui.text = self.nowLevelData.get('weekYunChuiScore', 0)
        if p.zhanXunExtraBonus:
            self.widget.panel.weekZhanxun.text = gameStrings.WEEK_ZHAN_XUN_POINT_WITH_BONUS % (self.weekZhanxunFame[0] - p.zhanXunExtraBonus, p.zhanXunExtraBonus)
        else:
            self.widget.panel.weekZhanxun.text = gameStrings.WEEK_ZHAN_XUN_POINT % self.weekZhanxunFame[0]
        self.widget.panel.weekZhanxun.width = self.widget.panel.weekZhanxun.textWidth + 30
        TipManager.addTip(self.widget.panel.weekRewardYunChui, gameStrings.WEEK_YUN_CHUI_SCORE_TIP)

    def initActivityPanel(self):
        self.widget.panel.weekJunjieActivity.addEventListener(events.MOUSE_CLICK, self.handleClickActivityBtn)

    def getJunjieActList(self, levelReq):
        p = BigWorld.player()
        ret = []
        for key, activityData in self.sortedAct:
            actIns = self.actFactory.actIns.get(key, None)
            if actIns.getShowInJunzi() == 0 and actIns.getShowInZhanxun() == 0:
                continue
            if not hasattr(actIns, 'erefId'):
                continue
            if levelReq and (p.realLv < actIns.getMinLv() or p.realLv > actIns.getMaxLv()):
                continue
            zhanxunActivityBlackList = WWCD.data.get('zhanxunActivityBlackList', None)
            enableWorldWar = gameglobal.rds.configData.get('enableWorldWar', False)
            if enableWorldWar and p.worldWar.state != gametypes.WORLD_WAR_STATE_CLOSE and zhanxunActivityBlackList and key in zhanxunActivityBlackList:
                continue
            weekSet = activityData.get('weekSet', 0)
            if utils.isInvalidWeek(weekSet):
                continue
            nowErefId = actIns.erefId[0]
            item = STD.data.get(nowErefId, {})
            actItem = {}
            actItem['actId'] = actIns.id
            actItem['actName'] = actIns.getDesc()
            actItem['sortedId'] = actIns.getSortedId()
            actItem['zhanXunValue'] = item.get('rewardZhanXun', 0)
            actItem['junziValue'] = item.get('rewardJunZi', 0)
            actItem['playRecommPage'] = item.get('playRecommPage', 0)
            actItem['playRecommItemId'] = item.get('playRecommItemId', 0)
            actItem['playRecommLocateType'] = item.get('playRecommLocateType', 0)
            actItem['process'] = [actIns.getStatsInfoValue(item.get('property', '')), item.get('finishNum', 0)]
            ret.append(actItem)

        ret.sort(key=lambda x: x['sortedId'])
        return ret

    def refreshActivityPanel(self):
        self.widget.questPanel.actCloseBtn.addEventListener(events.MOUSE_CLICK, self.handleClickActClose)
        lvReq = self.widget.questPanel.lvCheckBox.selected
        junJieActList = self.getJunjieActList(lvReq)
        questPanel = self.widget.questPanel
        posY = 0
        length = len(junJieActList)
        for i in xrange(0, length):
            item = questPanel.scroll.canvas.getChildByName('item%d' % i)
            if not item:
                item = self.widget.getInstByClsName(JUN_JIE_ACTIVITY_ITEM)
                questPanel.scroll.canvas.addChild(item)
                item.y = posY
            item.check.addEventListener(events.MOUSE_CLICK, self.handleClickCheck)
            item.actName.text = junJieActList[i].get('actName', '')
            item.junZiNum.text = junJieActList[i].get('junziValue', '')
            item.zhanXunNum.text = junJieActList[i].get('zhanXunValue', '')
            if junJieActList[i].get('process', (0, 0))[0] >= junJieActList[i].get('process', (0, 0))[1]:
                item.progress.gotoAndStop('lvgou')
            else:
                item.progress.gotoAndStop('wenzi')
                item.progress.txt.text = '%d/%d' % (junJieActList[i].get('process', (0, 0))[0], junJieActList[i].get('process', (0, 0))[1])
            item.check.data = {'playRecommPage': junJieActList[i].get('playRecommPage', ''),
             'playRecommItemId': junJieActList[i].get('playRecommItemId', ''),
             'playRecommLocateType': junJieActList[i].get('playRecommLocateType', '')}
            posY += item.height

        while length < questPanel.scroll.canvas.numChildren:
            questPanel.scroll.canvas.removeChildAt(length)

    def setExtraReward(self):
        zxActivityId = self.getZxActivityId()
        getExtraBtn = self.widget.panel.getExtraBtn
        p = BigWorld.player()
        canGetZxBonus = False
        itemMc = None
        isGetedZxBouns = False
        if zxActivityId:
            zxActivityTips = SCD.data.get('ZX_ACTIVITY_TIPS', '7.30~8.10 ')
            zxData = ASCD.data.get(zxActivityId, {}).get('rewardZXInfo', {}).get(p.junJieLv, None)
            if zxData:
                needPoint = zxData[0]
                bonusId = zxData[1]
                itemList = clientUtils.genItemBonus(bonusId)
                rewardZXScores = []
                if gameglobal.rds.configData.get('enableWingWorld', False):
                    rewardZXScores = self.nowLevelData.get('wingWorldRewardZXScores', [])
                extraIndex = -1
                for i in xrange(len(rewardZXScores)):
                    if needPoint >= rewardZXScores[i]:
                        extraIndex = i
                    else:
                        break

                if itemList:
                    itemId, cnt = itemList[0]
                    if extraIndex > 0 and self.widget.panel.rewardMC.currentFrameLabel == 'wingworld':
                        rewardItem = self.widget.panel.rewardMC.getChildByName('reward%d' % extraIndex)
                        itemMc = rewardItem.slotEx
                        itemMc.visible = True
                        itemMc.effect.visible = False
                        itemMc.slot.dragable = False
                        itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(itemId, cnt))
                isGetedZxBouns = p.zhanXunActivityBonusApplied
                if self.weekZhanxunFame[0] >= needPoint:
                    if not isGetedZxBouns:
                        canGetZxBonus = True
            else:
                zxActivityTips = SCD.data.get('ZX_ACTIVITY_NO_TIPS', 'aa')
                canGetZxBonus = False
        else:
            zxActivityTips = SCD.data.get('ZX_ACTIVITY_NO_TIPS', 'aa')
            canGetZxBonus = False
        getExtraBtn.enabled = canGetZxBonus
        getExtraBtn.label = gameStrings.WEEK_REWARD_GETTED if isGetedZxBouns else gameStrings.WEEK_EXTRA_REWARD
        if itemMc:
            itemMc.effect.visible = canGetZxBonus
            state = uiConst.ITEM_NORMAL if canGetZxBonus or isGetedZxBouns else uiConst.ITEM_GRAY
            itemMc.slot.setSlotState(state)
        TipManager.addTip(getExtraBtn, zxActivityTips)
        getExtraBtn.addEventListener(events.MOUSE_CLICK, self.handleClickGetExtraBtn)

    def getZxActivityId(self):
        p = BigWorld.player()
        if not hasattr(p, 'zxActivityId'):
            return 0
        else:
            return p.zxActivityId

    def setJunZiWeekVal(self, weekVal):
        self.junziWeekVal = weekVal

    def getCurMaxJunZi(self):
        p = BigWorld.player()
        if not hasattr(p, 'fameWeek'):
            return 0
        if not p.fameWeek.has_key(const.JUN_ZI_FAME_ID):
            return 0
        return p.fameWeek[const.JUN_ZI_FAME_ID][1]

    def onGetToolTip(self, *args):
        key = args[3][0].GetString()
        tipType, skillId = key.split('.')
        tip = gameglobal.rds.ui.skill.formatPSkillTooltip(int(skillId), sLv=1)
        return tip

    def handleClickActClose(self, *args):
        self.widget.questPanel.visible = False

    def handleClickCheck(self, *args):
        target = ASObject(args[3][0]).currentTarget
        gameglobal.rds.ui.playRecomm.showInPage(page=target.data.playRecommPage, selectedId=target.data.playRecommItemId, locateType=target.data.playRecommLocateType)

    def handleClickGetBtn(self, *args):
        BigWorld.player().cell.applyZXBonus()

    def handleClickGetExtraBtn(self, *args):
        BigWorld.player().cell.applyZXBonusFromActivity()

    def handleClickNextRewardBtn(self, *args):
        target = ASObject(args[3][0]).currentTarget
        if BigWorld.player().junJieLv >= MAX_JUN_JIE_LV:
            MenuManager.getInstance().showMenu(target, self.maxLvNextReward, None, False)
            self.refreshMaxLvNextReward()
        else:
            MenuManager.getInstance().showMenu(target, self.nextReward, None, False)
            self.refreshNextReward()

    def handleClickActivityBtn(self, *args):
        self.widget.questPanel.visible = not self.widget.questPanel.visible
        self.refreshActivityPanel()

    def handleClickJunjieLvUpBtn(self, *args):
        p = BigWorld.player()
        if p.junJieLv >= MAX_JUN_JIE_LV:
            gameglobal.rds.ui.famousLvupIntro.show()
            return
        p.cell.junJieLvUp()

    def handleClickLvUpRewardBtn(self, *args):
        target = ASObject(args[3][0]).currentTarget
        MenuManager.getInstance().showMenu(target, self.lvUpRewardPanel, None, False)
        self.refreshFamousLvUpReward()

    def handleClickLvUpBtn(self, *args):
        BigWorld.player().cell.updateFamousGeneralLv()

    def handleClickRank(self, *args):
        gameglobal.rds.ui.famousRankList.show()

    def handleClickFamousIntro(self, *args):
        p = BigWorld.player()
        if self.stage == gametypes.FAMOUS_GENERAL_STAGE_RUNNING:
            timeGap = self.getNowFromNextSeasonTimeGap()
            if timeGap > 0 and timeGap < FGCD.data.get('famousGeneralSeasonStartGap', 0):
                gameglobal.rds.ui.famousSeasonAnnounce.show()
            else:
                gameglobal.rds.ui.famousSeasonIntro.show()

    def handleClickFindNpc(self, *args):
        target = ASObject(args[3][0]).currentTarget
        seekId = int(target.data)
        uiUtils.gotoTrack(seekId)
        gameglobal.rds.uiLog.addFlyLog(seekId)

    def handleExtraSlotClick(self, *args):
        target = ASObject(args[3][0]).currentTarget
        data = target.data
        p = BigWorld.player()
        skills = FGCD.data.get('famousGeneralDefaultPskills', {}).get(p.school, ())
        if not skills:
            MenuManager.getInstance().hideMenu()
            return
        else:
            MenuManager.getInstance().showMenu(target, self.skillPanel, None, False)
            self.widget.panel.skillPanel.cdTip.visible = False
            self.widget.panel.skillPanel.equipBtn.visible = True
            self.widget.panel.skillPanel.equipBtn.removeEventListener(events.MOUSE_CLICK, self.handleClickEquipSkill)
            self.widget.panel.skillPanel.equipBtn.addEventListener(events.MOUSE_CLICK, self.handleExtraEquipSkillClick, False, 0, True)
            column = int(math.ceil(len(skills) * 1.0 / SKILL_TIP_LINES))
            self.widget.panel.skillPanel.tipBg.width = SKILL_TIP_BG_WIDTH * column
            self.widget.panel.skillPanel.equipBtn.x = self.widget.panel.skillPanel.tipBg.width / 2 - self.widget.panel.skillPanel.equipBtn.width / 2
            self.widget.panel.skillPanel.cdTip.x = self.widget.panel.skillPanel.tipBg.width / 2 - self.widget.panel.skillPanel.cdTip.width / 2
            isInCd = False
            if data and data.tWhen:
                now = utils.getNow()
                switchPkillCD = FGCD.data.get('switchPkillCD', 604800)
                interval = now - data.tWhen
                if interval < switchPkillCD:
                    deltaVal = switchPkillCD - interval
                    self.widget.panel.skillPanel.cdTip.visible = True
                    self.widget.panel.skillPanel.equipBtn.visible = False
                    self.widget.panel.skillPanel.cdTip.wordWrap = True
                    if deltaVal <= 59:
                        self.widget.panel.skillPanel.cdTip.text = gameStrings.FAMOUS_SKILL_CD_TIP % utils.formatTimeStr(deltaVal)
                    else:
                        self.widget.panel.skillPanel.cdTip.text = gameStrings.FAMOUS_SKILL_CD_TIP % utils.formatTimeStr(deltaVal, gameStrings.FAMOUS_SKILL_CD_TIME_FORMAT)
                    self.widget.panel.skillPanel.cdTip.height = self.widget.panel.skillPanel.cdTip.textHeight + 10
                    isInCd = True
            skillCanvas = self.widget.panel.skillPanel.skillCanvas
            self.widget.removeAllInst(skillCanvas)
            for j in xrange(column):
                itemY = 0
                itemX = j * 153
                for i in xrange(SKILL_TIP_LINES):
                    index = j * SKILL_TIP_LINES + i
                    if index >= len(skills):
                        break
                    skillItem = self.widget.getInstByClsName('RoleInformationJunjieV1_jinengxuanze')
                    skillCanvas.addChild(skillItem)
                    skillItem.groupName = 'empty'
                    skillItem.groupName = 'skillItem'
                    skillId = skills[index]
                    skillItem.mouseChildren = True
                    skillItem.slot.binding = 'famousSkill.%d' % skillId
                    skillInfo = PSkillInfo(skillId, 1)
                    skillName = skillInfo.getSkillData('sname', '')
                    skillItem.skillName.text = skillName
                    icon = skillInfo.getSkillData('icon', 'notFound')
                    iconPath = 'skill/icon/' + str(icon) + '.dds'
                    skillItem.slot.data = {'skillId': skillId,
                     'iconPath': iconPath,
                     'famousLv': 1}
                    skillItem.selected = False
                    skillItem.addEventListener(events.MOUSE_DOWN, self.handleClickSkillChoose, False, 0, True)
                    skillItem.visible = True
                    skillItem.slot.lock.visible = False
                    skillItem.slot.keyBind.visible = False
                    skillItem.data = {'avaliable': True,
                     'isInCd': isInCd}
                    skillItem.x = itemX
                    skillItem.y = itemY
                    itemY = itemY + skillItem.height

            return

    def handleExtraEquipSkillClick(self, *args):
        if not self.selectedSkillId:
            return
        p = BigWorld.player()
        p.cell.selectFamousGeneralRewardPskill(gametypes.FAMOUS_GENERAL_LV_DEFAULT, self.selectedSkillId)
        self.widget.panel.skillPanel.visible = False

    def handleClickSkill(self, *args):
        p = BigWorld.player()
        target = ASObject(args[3][0]).currentTarget
        data = target.slot.data
        rootName = target.parent.parent.name
        idx = int(rootName.replace('skill', ''))
        starNum = self.getStarNumFromSkillIdx(idx)
        MenuManager.getInstance().showMenu(target, self.skillPanel, None, False)
        self.selectedSkillId = 0
        self.selectedLv = 0
        self.widget.panel.skillPanel.cdTip.visible = False
        self.widget.panel.skillPanel.equipBtn.visible = True
        self.widget.panel.skillPanel.equipBtn.removeEventListener(events.MOUSE_CLICK, self.handleExtraEquipSkillClick)
        self.widget.panel.skillPanel.equipBtn.addEventListener(events.MOUSE_CLICK, self.handleClickEquipSkill, False, 0, True)
        isInCd = False
        if data and data.tWhen:
            now = utils.getNow()
            switchPkillCD = FGCD.data.get('switchPkillCD', 604800)
            interval = now - data.tWhen
            if interval < switchPkillCD:
                deltaVal = switchPkillCD - interval
                self.widget.panel.skillPanel.cdTip.visible = True
                self.widget.panel.skillPanel.equipBtn.visible = False
                self.widget.panel.skillPanel.cdTip.wordWrap = True
                if deltaVal <= 59:
                    self.widget.panel.skillPanel.cdTip.text = gameStrings.FAMOUS_SKILL_CD_TIP % utils.formatTimeStr(deltaVal)
                else:
                    self.widget.panel.skillPanel.cdTip.text = gameStrings.FAMOUS_SKILL_CD_TIP % utils.formatTimeStr(deltaVal, gameStrings.FAMOUS_SKILL_CD_TIME_FORMAT)
                self.widget.panel.skillPanel.cdTip.height = self.widget.panel.skillPanel.cdTip.textHeight + 10
                isInCd = True
        skillMaxLv = idx * STAR_NUM + starNum + 1
        maxLv = skillMaxLv if p.famousGeneralLv + 1 >= skillMaxLv else p.famousGeneralLv + 1
        minLv = idx * STAR_NUM + 1
        self.widget.panel.skillPanel.tipBg.width = SKILL_TIP_BG_WIDTH
        self.widget.panel.skillPanel.equipBtn.x = self.widget.panel.skillPanel.tipBg.width / 2 - self.widget.panel.skillPanel.equipBtn.width / 2
        self.widget.panel.skillPanel.cdTip.x = self.widget.panel.skillPanel.tipBg.width / 2 - self.widget.panel.skillPanel.cdTip.width / 2
        skillCanvas = self.widget.panel.skillPanel.skillCanvas
        self.widget.removeAllInst(skillCanvas)
        itemY = 0
        for lv in xrange(minLv, minLv + 3):
            skillId = FGLD.data.get(lv, {}).get('pskills', {}).get(p.school, 0)
            skillItem = self.widget.getInstByClsName('RoleInformationJunjieV1_jinengxuanze')
            skillCanvas.addChild(skillItem)
            skillItem.groupName = 'empty'
            skillItem.groupName = 'skillItem'
            skillItem.mouseChildren = True
            skillItem.slot.binding = 'famousSkill.%d' % skillId
            skillInfo = PSkillInfo(skillId, 1)
            skillName = skillInfo.getSkillData('sname', '')
            skillItem.skillName.text = skillName
            icon = skillInfo.getSkillData('icon', 'notFound')
            iconPath = 'skill/icon/' + str(icon) + '.dds'
            skillItem.slot.data = {'skillId': skillId,
             'famousLv': lv,
             'iconPath': iconPath}
            skillItem.selected = False
            skillItem.addEventListener(events.MOUSE_DOWN, self.handleClickSkillChoose)
            skillItem.visible = True
            skillItem.slot.lock.visible = False
            skillItem.slot.keyBind.visible = False
            if lv < maxLv:
                skillItem.data = {'lv': lv,
                 'avaliable': True,
                 'isInCd': isInCd}
            else:
                skillItem.data = {'lv': lv,
                 'avaliable': False,
                 'isInCd': isInCd}
            skillItem.y = itemY
            itemY = itemY + skillItem.height

        if minLv >= maxLv and not isInCd:
            self.widget.panel.skillPanel.cdTip.text = gameStrings.FAMOUS_ALL_SKILL_AVALIABLE_TIP
            self.widget.panel.skillPanel.cdTip.visible = True
            self.widget.panel.skillPanel.equipBtn.visible = False

    def handleClickSkillChoose(self, *args):
        target = ASObject(args[3][0]).currentTarget
        if target.data.get('isInCd', False):
            return
        if not target.data.get('avaliable', False):
            lv = target.data.get('lv', 1)
            famousName = FGLD.data.get(lv, {}).get('name', '')
            self.widget.panel.skillPanel.cdTip.text = gameStrings.FAMOUS_SKILL_AVALIABLE_TIP % famousName
            self.widget.panel.skillPanel.cdTip.visible = True
            self.widget.panel.skillPanel.equipBtn.visible = False
        else:
            self.selectedSkillId = int(target.slot.data.skillId)
            self.selectedLv = int(target.slot.data.famousLv)
            self.widget.panel.skillPanel.cdTip.visible = False
            self.widget.panel.skillPanel.equipBtn.visible = True

    def handleClickEquipSkill(self, *args):
        if not self.selectedSkillId:
            return
        p = BigWorld.player()
        p.cell.selectFamousGeneralRewardPskill(self.selectedLv, self.selectedSkillId)
        self.widget.panel.skillPanel.visible = False

    def handleClickFamousInfo(self, *args):
        BigWorld.player().cell.queryFamousRecordInfo()

    def getLvUpNeedZhanXun(self):
        if gameglobal.rds.configData.get('enablePursueJunJie', False):
            needZhanxunFormulaId = self.nowLevelData.get('needZhanxunFormulaId', 0)
            curWeeksZhanxunRequire = formula.calcFormulaById(needZhanxunFormulaId, {'week': float(utils.getServerOpenWeeks())})
        else:
            curWeeksZhanxunRequire = self.nowLevelData.get('needZhanxun', 0)
        return curWeeksZhanxunRequire

    def getStarNumFromSkillIdx(self, idx):
        p = BigWorld.player()
        famousGeneralLv = p.famousGeneralLv
        num = famousGeneralLv / STAR_NUM
        if idx < num:
            return STAR_NUM
        else:
            return famousGeneralLv % STAR_NUM

    def queryForFamousVal(self):
        p = BigWorld.player()
        key = 'allLv'
        p.base.getFamousGeneralTop(gametypes.TOP_TYPE_ZHAN_XUN, -1, key)
        self.setFamousGeneralVal()

    def setFamousGeneralVal(self, data = {}):
        if not self.widget:
            return
        if data.get('key', '') != 'allLv':
            return
        rank = data.get('myRank', -1) + 1
        famousMaxVal = 0
        if gameglobal.rds.configData.get('enableWingWorld', False):
            zhanXunRequireList = FGCD.data.get('wingZhanxunRewardFamousGeneralValList', [])
        else:
            zhanXunRequireList = FGCD.data.get('zhanxunRewardFamousGeneralValList', [])
        for zhanXunRequire in zhanXunRequireList:
            if self.weekZhanxunFame[0] >= zhanXunRequire[0] and self.weekZhanxunFame[0] <= zhanXunRequire[1]:
                famousMaxVal = zhanXunRequire[2]

        if rank:
            for key, value in FGZRD.data.iteritems():
                if rank >= key[0] and rank <= key[1]:
                    famousMaxVal += value.get('rewardFamousGeneralVal', 0)

        if self.widget:
            if self.extraExp:
                famousMaxVal = int(famousMaxVal * self.extraExp)
            if self.widget.panel.famousMaxVal:
                self.widget.panel.famousMaxVal.text = gameStrings.FAMOUS_GENERAL_VAL_TEXT % famousMaxVal
                TipManager.addTip(self.widget.panel.famousMaxVal, FGCD.data.get('famousWeekValTip', ''))

    def getNowFromNextSeasonTimeGap(self):
        now = utils.getNow()
        seasonStartTime = FGCD.data.get('famousGenralSeasonEndCrontab', '')
        seasonStartSeconds = utils.getNextCrontabTime(seasonStartTime)
        return seasonStartSeconds - now

    def isCloseToNextSeason(self):
        if self.stage in gametypes.FAMOUS_GENERAL_STAGE_IN_RUN:
            return False
        timeGap = self.getNowFromNextSeasonTimeGap()
        openLimitDays = FGCD.data.get('openLimitDays', 0)
        return timeGap <= openLimitDays * 60 * 60 * 24

    def isReadyForFamous(self):
        p = BigWorld.player()
        return not p.famousGeneralLv and p.junJieLv >= MAX_JUN_JIE_LV

    def checkFamousGeneralLvUp(self):
        p = BigWorld.player()
        if p.famousGeneralLv:
            famousGeneralLv = p.famousGeneralLv
            nowFamousLevelData = FGLD.data.get(famousGeneralLv, {})
            needFamousGeneralVal = nowFamousLevelData.get('needFamousGeneralVal', 999)
            if p.famousGeneralVal >= needFamousGeneralVal:
                return True
        return False

    def pushFamousGeneralLvUpMsg(self):
        pushId = FGCD.data.get('famousGeneralLvUpPushId', 0)
        if pushId:
            self.setFamousGeneralLvUpMsgCallBack(pushId)
            gameglobal.rds.ui.pushMessage.addPushMsg(pushId)

    def removeFamousGeneralLvUpMsg(self):
        pushId = FGCD.data.get('famousGeneralLvUpPushId', 0)
        if pushId:
            gameglobal.rds.ui.pushMessage.removePushMsg(pushId)

    def setFamousGeneralLvUpMsgCallBack(self, pushId):
        gameglobal.rds.ui.pushMessage.setCallBack(pushId, {'click': self.pushToShowJunjiePanel})

    def pushToShowJunjiePanel(self):
        self.removeFamousGeneralLvUpMsg()
        gameglobal.rds.ui.roleInfo.show(uiConst.ROLEINFO_TAB_JUNJIE)
