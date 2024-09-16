#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bfDotaChooseHeroRightProxy.o
import BigWorld
import uiUtils
import uiConst
import events
import ui
import math
from gameStrings import gameStrings
import utils
import skillDataInfo
import gamelog
import gametypes
import gameglobal
import gameconfigCommon
import copy
from uiProxy import UIProxy
from guis import events
from guis.asObject import ASObject
from guis.asObject import TipManager
from guis.asObject import ASUtils
from guis import tipUtils
from data import zaiju_data as ZD
from data import duel_config_data as DCD
from cdata import game_msg_def_data as GMDD
ITEM_RENDER_MAX_CNT = 5
PAGE_MAX_CNT = 2

class BfDotaChooseHeroRightProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BfDotaChooseHeroRightProxy, self).__init__(uiAdapter)
        self.exitTime = 0
        self._resetData()

    def _resetData(self):
        self.widget = None
        self.callbackHelper = {}
        self.heroInfoList = []
        self.chooseHeroId = 0
        self.chooseSkillIdx = -1
        self.lastSelectedMc = None
        self.lastSelectedSkillMc = None
        self.tickTimer = 0
        self.lastRemindTime = 0
        self.tickIntTime = 0
        self.firstRemind = True
        self.timeLimitedHeroSet = set()

    def _registerASWidget(self, widgetId, widget):
        self.checkExitTime()
        self.widget = widget
        self.getHeroInfoList()
        self._initUI()
        if not self.chooseHeroId and len(self.heroInfoList) > 0:
            self.chooseHeroId = self.heroInfoList[0]['id']
        self.refreshFrame()
        self.updateTick()

    def checkExitTime(self):
        p = BigWorld.player()
        if p.battleFieldPhase == gametypes.DUEL_PHASE_RUNNING:
            readyTime = uiUtils.getDuelCountTime('readyTime', p.mapID)
            if getattr(p, 'isJumpQueue', False):
                self.exitTime = int(self.uiAdapter.battleField.tipsTimeStamp + readyTime)
            else:
                self.exitTime = int(p.battleFieldReEnterTimestamp + readyTime)

    def show(self):
        if self.widget:
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_DOTA_CHOOSE_HERO_RIGHT)
        if gameconfigCommon.enableDotaFreeRandomRole():
            BigWorld.player().base.queryDotaFreeRandomRoleList()

    def getFreeRoleList(self):
        p = BigWorld.player()
        if gameconfigCommon.enableDotaFreeRandomRole():
            weeklyFreeList = list(getattr(p, 'bfDotaFreeRoleList', []))
            weeklyFreeList.extend(DCD.data.get('BATTLE_FIELD_ROLE_ZAIJU_SET', []))
        else:
            weeklyFreeList = list(DCD.data.get('BATTLE_FIELD_ROLE_ZAIJU_SET', []))
        return weeklyFreeList

    def getHeroInfoList(self):
        p = BigWorld.player()
        self.heroInfoList = []
        self.timeLimitedHeroSet = set()
        weeklyFreeList = self.getFreeRoleList()
        availableRoleZaijuList = copy.deepcopy(getattr(p, 'availableRoleZaijuSet', set()))
        for id in weeklyFreeList:
            if id not in availableRoleZaijuList:
                self.timeLimitedHeroSet.add(id)
            availableRoleZaijuList.add(id)

        startTimeList = DCD.data.get('BATTLE_FIELD_DOTA_ROLE_OPEN_START_TIME', ())
        endTimeList = DCD.data.get('BATTLE_FIELD_DOTA_ROLE_OPEN_END_TIME', ())
        openHeroList = DCD.data.get('BATTLE_FIELD_DOTA_ROLE_OPEN_LIST', ())
        if len(startTimeList) == len(endTimeList) == len(openHeroList):
            for index, startTime in enumerate(startTimeList):
                endTime = endTimeList[index]
                herolist = list(openHeroList[index])
                if utils.inCrontabRangeWithYear(startTime, endTime):
                    for id in herolist:
                        if id not in availableRoleZaijuList:
                            self.timeLimitedHeroSet.add(id)
                        availableRoleZaijuList.add(id)

        blackStrList = gameglobal.rds.configData.get('bfDotaRoleBlackList', '').split(',')
        if blackStrList:
            try:
                for str in blackStrList:
                    if int(str) in availableRoleZaijuList:
                        availableRoleZaijuList.remove(int(str))

            except:
                gamelog.error('@jbx:bfDotaRoleBlackList Error', blackStrList)

        availableRoleZaijuList = list(availableRoleZaijuList)
        for id in availableRoleZaijuList:
            zjd = ZD.data.get(id, {})
            if zjd and zjd.has_key('sortOrder'):
                info = {}
                info['id'] = id
                info['name'] = zjd.get('desc', '')
                info['sortOrder'] = zjd.get('sortOrder')
                info['headIcon'] = zjd.get('littleHeadIcon')
                self.heroInfoList.append(info)

        self.heroInfoList.sort(cmp=self.cmpHero)

    def cmpHero(self, info0, info1):
        mainType0, subType0 = info0['sortOrder']
        mainType1, subType1 = info1['sortOrder']
        if mainType0 != mainType1:
            return mainType0 - mainType1
        if subType0 != subType1:
            return subType0 - subType1
        return 0

    def updateTick(self):
        if not self.widget:
            return
        if not self.widget.mainMc:
            return
        p = BigWorld.player()
        leftTime = max(0, self.exitTime - utils.getNow())
        if leftTime == 0 and utils.getNow() - self.lastRemindTime >= 5:
            if utils.getNow() - self.lastRemindTime <= 10:
                p.showGameMsg(GMDD.data.CHOOSE_HERO_OVER_TIME, ())
            self.lastRemindTime = utils.getNow()
        if leftTime > 5:
            self.widget.mainMc.countDown.txtCountDown.text = utils.formatTimeStr(leftTime, 'm:s', sNum=2, mNum=2, zeroShow=True)
            self.widget.mainMc.countDown.visible = True
            self.widget.mainMc.countDownEff.visible = False
        else:
            self.widget.mainMc.countDown.visible = False
            if not self.widget.mainMc.countDownEff.visible:
                self.widget.mainMc.countDownEff.visible = True
            frameName = 'time%d' % leftTime
            if self.tickIntTime != leftTime:
                self.widget.mainMc.countDownEff.gotoAndPlay(frameName)
                if leftTime:
                    self.widget.mainMc.countDownEff.lightEff.gotoAndPlay(1)
        self.tickIntTime = leftTime
        self.tickTimer = BigWorld.callback(0.2, self.updateTick)

    def clearWidget(self):
        BigWorld.cancelCallback(self.tickTimer)
        self._resetData()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_DOTA_CHOOSE_HERO_RIGHT)

    def refreshFrame(self):
        if not self.widget:
            return
        self.getHeroInfoList()
        self.refreshHeadIconList()

    def refreshHeadIconList(self):
        self.widget.mainMc.scrollList.dataArray = range(int(math.ceil(len(self.heroInfoList) / 5.0)))
        self.widget.mainMc.scrollList.validateNow()
        if self.chooseHeroId:
            self.uiAdapter.bfDotaChooseHeroBottom.refreshFrame()
            self.widget.mainMc.lockBtn.enabled = True

    def _initUI(self):
        ASUtils.setHitTestDisable(self.widget.mainMc.countDownEff, True)
        self.widget.mainMc.countDownEff.visible = False
        ASUtils.setHitTestDisable(self.widget.mainMc.unLockStateEff, True)
        ASUtils.setHitTestDisable(self.widget.mainMc.lockBtn.lockState, True)
        self.widget.mainMc.scrollList.itemRenderer = 'BfDotaChooseHeroRight_HertListItemRender'
        self.widget.mainMc.scrollList.lableFunction = self.lableFunction
        self.widget.mainMc.scrollList.itemHeight = 92
        self.widget.mainMc.skill0.addEventListener(events.MOUSE_CLICK, self.handleSkillClick, False, 0, True)
        self.widget.mainMc.skill1.addEventListener(events.MOUSE_CLICK, self.handleSkillClick, False, 0, True)
        self.widget.mainMc.lockBtn.addEventListener(events.MOUSE_CLICK, self.handleChooseHeroClick, False, 0, True)
        self.widget.removeAllInst(self.widget.mainMc.scrollList.canvas)
        self.widget.mainMc.scrollList.validateNow()
        self.refreshLockBtn()
        self.refreshTalentSkillIcons()

    def handleSkillClick(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.name == 'skill0':
            self.chooseSkillIdx = 0
            self.widget.mainMc.skill1.gotoAndStop('weixuan')
        elif e.currentTarget.name == 'skill1':
            self.chooseSkillIdx = 1
            self.widget.mainMc.skill0.gotoAndStop('weixuan')
        else:
            return
        if self.lastSelectedSkillMc:
            self.lastSelectedSkillMc.selected = False
        e.currentTarget.skill.selected = True
        self.lastSelectedSkillMc = e.currentTarget.skill
        if e.currentTarget.currentFrameLabel == 'weixuan':
            gameglobal.rds.sound.playSound(5616)
            e.currentTarget.gotoAndStop('xuanze')
            self.initExpandTalenSkills(e.currentTarget.skillList)
        else:
            gameglobal.rds.sound.playSound(5617)
            e.currentTarget.gotoAndStop('weixuan')

    def initExpandTalenSkills(self, skillList):
        talentSkillList = DCD.data.get('BATTLE_FIELD_DOTA_TALENT_SKILL_LIST', [])
        pageCnt = int(math.ceil(len(talentSkillList) / 5.0))
        availableSkillIds = BigWorld.player().availableTalenSkillIds
        for page in xrange(PAGE_MAX_CNT):
            pageMc = skillList.getChildByName('list%d' % page)
            if page >= pageCnt:
                pageMc.visible = False
                continue
            else:
                pageMc.visible = True
            for i in xrange(ITEM_RENDER_MAX_CNT):
                itemMc = pageMc.getChildByName('skill%d' % i)
                index = i + page * ITEM_RENDER_MAX_CNT
                itemMc.idx = index
                if index >= len(talentSkillList):
                    itemMc.visible = False
                    continue
                else:
                    itemMc.visible = True
                    skillId = talentSkillList[index]
                    if skillId in availableSkillIds:
                        ASUtils.setMcEffect(itemMc.skillIcon, '')
                    else:
                        ASUtils.setMcEffect(itemMc.skillIcon, 'gray')
                    skillInfo = skillDataInfo.ClientSkillInfo(skillId, 1)
                    path = uiUtils.getSkillIconPath(skillInfo, uiConst.ICON_SIZE64)
                    itemMc.txtSkillName.text = skillInfo.getSkillData('sname', '')
                    mcWidth = itemMc.txtSkillName.width
                    ASUtils.autoSizeWithFont(itemMc.txtSkillName, 14, mcWidth, 5)
                    itemMc.skillIcon.icon.loadImage(path)
                    TipManager.addTipByType(itemMc, tipUtils.TYPE_SKILL, talentSkillList[index])
                    itemMc.addEventListener(events.MOUSE_CLICK, self.handleChangeTalentSkill, False, 0, True)

    def handleChangeTalentSkill(self, *args):
        p = BigWorld.player()
        if not p:
            return
        e = ASObject(args[3][0])
        idx = int(e.currentTarget.idx)
        skillId, _ = utils.getTalentSkillByIndex(idx)
        if skillId not in p.availableTalenSkillIds:
            p.showGameMsg(GMDD.data.CHOOSE_LOCK_TALENT_SKILL, ())
            return
        skills = list(p.bfDotaTalentSkillRecord.get(p.gbId, (10100, 10101)))
        if skillId in skills:
            p.showGameMsg(GMDD.data.CHOOSE_OWNED_TALENT_SKILL, ())
            return
        cfgSkills = DCD.data.get('BATTLE_FIELD_DOTA_TALENT_SKILL_LIST', [])
        if self.chooseSkillIdx in range(0, 2):
            skills[self.chooseSkillIdx] = cfgSkills[idx]
            p.cell.changeMyTalentSkills(skills)

    def handleChooseHeroClick(self, *args):
        gameglobal.rds.sound.playSound(5614)
        p = BigWorld.player()
        if not p:
            return
        if not self.chooseHeroId:
            return
        if p.bfDotaZaijuRecord.get(p.gbId, 0):
            p.cell.cancelMyRoleInPrepareStatus(p.bfDotaZaijuRecord[p.gbId])
        elif p.battleFieldPhase == gametypes.DUEL_PHASE_RUNNING:
            p.cell.rechooseHeroAfterLogon(self.chooseHeroId)
        else:
            p.cell.confirmMyRoleInPrepareStatus(self.chooseHeroId)

    @ui.uiEvent(uiConst.WIDGET_DOTA_CHOOSE_HERO_RIGHT, events.EVENT_BF_DOTA_ZAIJU_CHANGE)
    def refreshLockBtn(self, event = None):
        p = BigWorld.player()
        if p.bfDotaZaijuRecord.get(p.gbId, 0):
            self.widget.mainMc.lockBtn.label = gameStrings.BF_DOTA_CANCEL_CHOOSE_HERO
            self.widget.mainMc.unLockStateEff.visible = False
            self.widget.mainMc.lockBtn.lockState.gotoAndStop('suoding')
        else:
            self.widget.mainMc.lockBtn.label = gameStrings.BF_DOTA_CHOOSE_HERO
            self.widget.mainMc.unLockStateEff.visible = True
            self.widget.mainMc.lockBtn.lockState.gotoAndStop('zhengchang')

    def lableFunction(self, *args):
        numList = int(args[3][0].GetNumber())
        mc = ASObject(args[3][1])
        for i in xrange(ITEM_RENDER_MAX_CNT):
            index = i + numList * ITEM_RENDER_MAX_CNT
            itemMc = mc.getChildByName('item%d' % i)
            itemMc.idx = index
            itemMc.selected = False
            itemMc.removeEventListener(events.MOUSE_CLICK, self.handleHeadIconClick)
            if index >= len(self.heroInfoList):
                itemMc.visible = False
            else:
                info = self.heroInfoList[index]
                if info['id'] == self.chooseHeroId:
                    if self.lastSelectedMc:
                        self.lastSelectedMc.selected = False
                    itemMc.selected = True
                    self.lastSelectedMc = itemMc
                itemMc.visible = True
                itemMc.timeLimited.visible = info['id'] in self.timeLimitedHeroSet
                itemMc.icon.fitSize = True
                itemMc.icon.loadImage(uiUtils.getZaijuLittleHeadIconPath(info['headIcon']))
                itemMc.addEventListener(events.MOUSE_CLICK, self.handleHeadIconClick, False, 0, True)
                TipManager.addTip(itemMc, info['name'], tipUtils.TYPE_DEFAULT_BLACK)

    def handleHeadIconClick(self, *args):
        gameglobal.rds.sound.playSound(5613)
        p = BigWorld.player()
        if not p:
            return
        if self.isLocked():
            return
        e = ASObject(args[3][0])
        idx = int(e.currentTarget.idx)
        if idx >= len(self.heroInfoList):
            return
        id = self.heroInfoList[idx]['id']
        if id == self.chooseHeroId:
            return
        self.chooseHeroId = id
        if self.lastSelectedMc:
            self.lastSelectedMc.selected = False
        self.lastSelectedMc = e.currentTarget
        self.lastSelectedMc.selected = True
        self.widget.mainMc.lockBtn.enabled = True
        self.uiAdapter.bfDotaChooseHeroBottom.refreshFrame()

    def isLocked(self):
        p = BigWorld.player()
        if self.chooseHeroId and self.chooseHeroId == p.bfDotaZaijuRecord.get(p.gbId, 0):
            return True
        return False

    @ui.uiEvent(uiConst.WIDGET_DOTA_CHOOSE_HERO_RIGHT, events.EVENT_TALENT_SKILL_CHANGE)
    def refreshTalentSkillIcons(self, event = None):
        p = BigWorld.player()
        if not p:
            return
        self.widget.mainMc.skill0.gotoAndStop('weixuan')
        self.widget.mainMc.skill1.gotoAndStop('weixuan')
        self.widget.mainMc.skill0.skill.selected = False
        self.widget.mainMc.skill1.skill.selected = False
        skill0, skill1 = p.bfDotaTalentSkillRecord.get(p.gbId, (10100, 10101))
        sd0 = skillDataInfo.ClientSkillInfo(skill0, 1)
        path0 = uiUtils.getSkillIconPath(sd0, uiConst.ICON_SIZE64)
        sd1 = skillDataInfo.ClientSkillInfo(skill1, 1)
        path1 = uiUtils.getSkillIconPath(sd1, uiConst.ICON_SIZE64)
        self.widget.mainMc.skill0.skill.icon.loadImage(path0)
        self.widget.mainMc.skill1.skill.icon.loadImage(path1)
        TipManager.addTipByType(self.widget.mainMc.skill0.skill, tipUtils.TYPE_SKILL, skill0)
        TipManager.addTipByType(self.widget.mainMc.skill1.skill, tipUtils.TYPE_SKILL, skill1)
