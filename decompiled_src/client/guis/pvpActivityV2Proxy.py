#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pvpActivityV2Proxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import utils
import const
import events
import uiConst
import formula
import gamelog
import gametypes
import gameconfigCommon
from uiProxy import UIProxy
from guis.asObject import ASObject
from gamestrings import gameStrings
from data import battle_field_mode_data as BFMD
from data import battle_field_data as BFD
from data import sys_config_data as SCD
from data import duel_config_data as DCD
from cdata import game_msg_def_data as GMDD
INIT_APPLY_PERSON_BTN_X = 456
INIT_APPLY_DOUBLE_BTN_X = 593
INIT_APPLY_BTN_OFFSET = 137
MAX_ACTIVITY_NUM = 5
ICON_PATH = 'pvpPanel/%d.dds'

class PvpActivityV2Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PvpActivityV2Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.cFlag = 0

    def reset(self):
        pass

    def initPanel(self, widget):
        self.widget = widget
        self.myBfId = -1
        self.bfStage = 0
        self.myMode = -1
        self.target = None
        self.isBFButtonSelected = False
        self.refreshActivity()
        self.initUI()

    def unRegisterPanel(self):
        self.widget = None

    def setVisible(self, mc, active):
        mc.turn.visible = active
        mc.checkBox.visible = active
        mc.nameTxt.visible = active
        mc.chaosTxt.visible = active
        mc.startLvTxt.visible = active
        mc.startDayTxt.visible = active
        mc.startTimeTxt.visible = False
        mc.unlockFrame.visible = active
        mc.vsNumTxt.visible = active
        mc.bottomBorder.visible = active

    def setActivityName(self, mc, name):
        nameList = name.split(gameStrings.TEXT_HELPPROXY_512, 1)
        if len(nameList) == 1:
            mc.chaosTxt.visible = False
            mc.nameTxt.visible = True
            mc.nameTxt.text = nameList[0]
        else:
            mc.chaosTxt.visible = True
            mc.chaosTxt.nameTxt.text = nameList[0]
            mc.chaosTxt.modeTxt.text = nameList[1]
            mc.nameTxt.visible = False

    def initUI(self):
        self.initBFButtonList()
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.data = self.onGetTodayBFButtonList()
        curSelectMc = None
        for i in xrange(MAX_ACTIVITY_NUM):
            mc = self.widget.getChildByName('activity%d' % i)
            if i >= len(self.widget.data):
                self.setVisible(mc, False)
            else:
                self.setVisible(mc, True)
                mc.data = self.widget.data[i]
                mc.enabled = mc.data['isOpen']
                if mc.enabled:
                    mc.unlockFrame.visible = False
                self.setActivityName(mc, mc.data['name'])
                mc.toggle = True
                mc.selected = mc.data['selected']
                mc.vsNumTxt.text = mc.data['numberDesc']
                mc.startLvTxt.text = mc.data['openLvDesc']
                mc.startDayTxt.text = mc.data['timeShortDesc']
                if mc.data['icon']:
                    mc.pitctrue.loadImage(ICON_PATH % mc.data['icon'])
                mc.turn.visible = False
                mc.checkBox.visible = False
                mc.checkBox.addEventListener(events.BUTTON_CLICK, self.handleCheckBoxClick, False, 0, True)
                if mc.selected:
                    curSelectMc = mc
                mc.addEventListener(events.MOUSE_CLICK, self.handleChooseBfClick, False, 0, True)

        if len(self.widget.data) >= 1:
            if curSelectMc:
                self.isBFButtonSelected = True
            else:
                curSelectMc = self.widget.getChildByName('activity0')
                curSelectMc.selected = True
                curSelectMc.data['selected'] = True
                self.isBFButtonSelected = False
            curSelectMc.selectFrame.visible = True
            self.target = curSelectMc
            self.selectBF(curSelectMc.data)
            self.refreshBF()

    def handleCheckBoxClick(self, *args):
        gameglobal.rds.ui.pvpBattleRotationV2.show()

    def refreshBF(self):
        p = BigWorld.player()
        stage = getattr(p, 'battleFieldStage', 1)
        self.refreshBtnEnabled()
        self.setBfStage(stage)

    def refreshBtnEnabled(self):
        p = BigWorld.player()
        stage = getattr(p, 'battleFieldStage', 1)
        if stage == uiConst.BF_PANEL_STAGE_INIT:
            self.isEnableBtnWithoutSelected(True)
        elif stage == uiConst.BF_PANEL_STAGE_APPLYED:
            self.isEnableBtnWithoutSelected(False)

    def isEnableBtnWithoutSelected(self, isEnable):
        for i in xrange(len(self.widget.data)):
            if i >= MAX_ACTIVITY_NUM:
                break
            mc = self.widget.getChildByName('activity%d' % i)
            applyTabIdx = gameglobal.rds.ui.pvPPanel.getApply()
            if applyTabIdx != uiConst.APPLY_TABIDX_NONE and applyTabIdx != uiConst.APPLY_TABIDX_ACTIVITYV2:
                mc.enabled = False
                mc.unlockFrame.visible = True
                mc.selectFrame.visible = False
            elif not mc.data['isOpen']:
                mc.enabled = False
                mc.unlockFrame.visible = True
            else:
                mc.enabled = isEnable
                mc.unlockFrame.visible = not isEnable

    def refreshActivity(self):
        for i in xrange(5):
            mc = self.widget.getChildByName('activity%d' % i)
            mc.unlockFrame.visible = True
            mc.selectFrame.visible = False

    def selectBF(self, data):
        self.myBfId = data['idx']
        self.myMode = data['id']
        textMc = self.widget.descPanel.canvas.text
        textMc.htmlText = ''
        if data['desc']:
            textMc.htmlText += data['desc'] + '\n\n'
        if data['timeDesc']:
            textMc.htmlText += data['timeDesc'] + '\n'
        if data['winStandard']:
            textMc.htmlText += data['winStandard'] + '\n'
        if data['priceDesc']:
            textMc.htmlText += data['priceDesc']
        textMc.height = textMc.textHeight + 20
        self.widget.descPanel.validateNow()
        self.widget.descPanel.refreshHeight()
        self.isOpenDouble = data['isOpenDouble']
        self.isModeHunt = data['modeHunt']
        self.isTeamBtnShow = data['teamApplyBtnNeedShow']
        isShow = self.isBattleNeedShow(self.myBfId)
        self.widget.applyOfPersonBtn.visible = not self.isModeHunt and isShow
        self.widget.applyOfDoubleBtn.visible = self.isOpenDouble and not self.isModeHunt and isShow
        self.widget.applyCommander.visible = not self.isModeHunt and isShow
        self.widget.applyOfTeamBtn.visible = not self.isModeHunt and isShow
        self.setBfStage(self.bfStage)

    def refreshOtherUI(self, data):
        p = BigWorld.player()
        self.widget.bfGradingTxt.visible = False
        self.widget.bfGradingBtn.visible = False
        self.widget.bfRewardBtn.visible = False
        self.widget.bfHelpIcon.visible = False
        self.widget.chaosTime.visible = False
        self.widget.signUpBtn.visible = False
        if data and data['id'] == const.BATTLE_FIELD_MODE_PUBG:
            self.widget.bfGradingTxt.visible = True
            self.widget.bfGradingBtn.visible = True
            self.widget.bfRewardBtn.visible = True
            self.widget.bfHelpIcon.visible = True
            self.widget.applyCommander.visible = False
            self.widget.bfHelpIcon.helpKey = DCD.data.get('pubgBattleFieldHelpKey', 0)
            self.widget.bfGradingTxt.htmlText = DCD.data.get('pubgPVPBattleFieldRankTxt', gameStrings.PUBG_PVP_BATTLE_FIELD_V2_RANK_TXT) % (p.getCurRankNameInPUBG(), p.pubgRankPoints)
        if data and data['chaosMode']:
            self.widget.chaosTime.visible = True
            self.widget.chaosTime.text = data['chaosTimeDesc']
        if data and data['isShowNewFlagBF']:
            self.widget.applyOfTeamBtn.visible = False
            self.widget.applyOfDoubleBtn.visible = False
            self.widget.applyOfPersonBtn.visible = False
            self.widget.applyCommander.visible = False
            self.widget.signUpBtn.visible = True
        self.setBFBtnVisibleWithSelected()

    def handleSignUpBtnClick(self, *args):
        gameglobal.rds.ui.battleOfFortSignUp.show(self.myBfId)
        self.hide()

    def setBfStage(self, stage):
        self.bfStage = stage
        if stage == uiConst.BF_PANEL_STAGE_INIT:
            self.setStage1Info()
        elif stage == uiConst.BF_PANEL_STAGE_APPLYED:
            self.setStage2Info()
        elif stage == uiConst.BF_PANEL_STAGE_MATCHED:
            self.setStage3Info()
        elif stage == uiConst.BF_PANEL_STAGE_IN_GAME:
            self.setStage4Info()
        else:
            self.setStage1Info()
        self.myBfStage = stage
        self.target and self.refreshOtherUI(self.target.data)

    def setStage1Info(self):
        if not self.isModeHunt:
            self.widget.applyOfTeamBtn.visible = self.isTeamBtnShow
            if not self.isTeamBtnShow:
                self.widget.applyOfPersonBtn.x = self.widget.applyOfDoubleBtn.x
                self.widget.applyOfDoubleBtn.x = self.widget.applyOfTeamBtn.x
            else:
                self.widget.applyOfPersonBtn.x = INIT_APPLY_PERSON_BTN_X
                self.widget.applyOfDoubleBtn.x = INIT_APPLY_DOUBLE_BTN_X
        else:
            self.widget.applyOfTeamBtn.visible = True
            self.widget.applyOfPersonBtn.x = INIT_APPLY_PERSON_BTN_X
            self.widget.applyOfDoubleBtn.x = INIT_APPLY_DOUBLE_BTN_X
        self.widget.applyOfPersonBtn.label = gameStrings.PVP_APPLY_OF_PERSON
        self.widget.applyOfPersonBtn.visible = not self.isModeHunt
        self.widget.applyOfDoubleBtn.visible = self.isOpenDouble and not self.isModeHunt
        self.widget.applyOfDoubleBtn.label = gameStrings.PVP_APPLY_OF_DOUBLE
        if self.widget.applyOfDoubleBtn.visible:
            self.widget.applyOfPersonBtn.x = self.widget.applyOfDoubleBtn.x - INIT_APPLY_BTN_OFFSET
        else:
            self.widget.applyOfPersonBtn.x = self.widget.applyOfDoubleBtn.x
        if self.isModeHunt:
            self.widget.applyOfTeamBtn.label = gameStrings.PVP_APPLY_OF_PERSON
        else:
            self.widget.applyOfTeamBtn.label = gameStrings.PVP_APPLY_OF_TEAM
        self.refreshApplyCommander()

    def setStage2Info(self):
        self.widget.applyOfPersonBtn.visible = False
        self.widget.applyOfDoubleBtn.visible = False
        self.widget.applyOfTeamBtn.label = gameStrings.PVP_QUIT_QUEUE
        self.widget.applyOfTeamBtn.visible = True
        self.refreshApplyCommander()

    def setStage3Info(self):
        self.widget.applyOfPersonBtn.visible = False
        self.widget.applyOfDoubleBtn.visible = False
        self.widget.applyOfTeamBtn.visible = False
        self.refreshApplyCommander()

    def setStage4Info(self):
        self.widget.applyOfPersonBtn.visible = False
        self.widget.applyOfDoubleBtn.visible = False
        self.widget.applyOfTeamBtn.label = gameStrings.PVP_QUIT_GAME
        self.widget.applyOfTeamBtn.visible = False
        self.refreshApplyCommander()

    def setBFBtnVisibleWithSelected(self):
        if not self.isBFButtonSelected:
            self.widget.applyOfTeamBtn.visible = False
            self.widget.applyOfDoubleBtn.visible = False
            self.widget.applyOfPersonBtn.visible = False
            self.widget.applyCommander.visible = False
            self.widget.signUpBtn.visible = False

    def refreshApplyCommander(self):
        checkboxEnable = getattr(BigWorld.player(), 'battleFieldStage', 1) == uiConst.BF_PANEL_STAGE_INIT
        self.widget.applyCommander.enabled = checkboxEnable
        self.widget.applyCommander.selected = self.cFlag

    def initBFButtonList(self):
        self.widget.applyOfPersonBtn.addEventListener(events.BUTTON_CLICK, self.handleApplyClick, False, 0, True)
        self.widget.applyOfDoubleBtn.addEventListener(events.BUTTON_CLICK, self.handleApplyOfDoubleBtnClick, False, 0, True)
        self.widget.applyOfTeamBtn.addEventListener(events.BUTTON_CLICK, self.handleApplyOfTeamClick, False, 0, True)
        self.widget.applyCommander.addEventListener(events.EVENT_SELECT, self.handleApplyCommanderSelect, False, 0, True)
        self.widget.signUpBtn.addEventListener(events.BUTTON_CLICK, self.handleSignUpBtnClick, False, 0, True)
        self.widget.bfGradingBtn.addEventListener(events.BUTTON_CLICK, self.handleBfGradingBtnClick, False, 0, True)
        self.widget.bfRewardBtn.addEventListener(events.BUTTON_CLICK, self.handleBfRewardBtnClick, False, 0, True)
        self.refreshApplyCommander()

    def handleBfGradingBtnClick(self, *args):
        if self.myMode == const.BATTLE_FIELD_MODE_PUBG:
            gameglobal.rds.ui.rankCommon.showRankCommon(gametypes.TOP_TYPE_PUBG_GRADING_RANK)

    def handleBfRewardBtnClick(self, *args):
        if self.myMode == const.BATTLE_FIELD_MODE_PUBG:
            gameglobal.rds.ui.generalReward.show(gametypes.GENERAL_REWARD_PUBG)

    def isBattleNeedShow(self, key):
        if not gameglobal.rds.configData.get('enableDuelTimeCheck', True):
            return True
        isOpen = False
        openStartTimes = BFMD.data.get(key, {}).get('openStartTimes', ())
        openEndTimes = BFMD.data.get(key, {}).get('openEndTimes', ())
        current = utils.getNow()
        if not BFMD.data.get(key, {}).get('isOpen', 0):
            return False
        if len(openStartTimes) == 0:
            isOpen = True
        else:
            for index in xrange(len(openStartTimes)):
                if utils.inTimeTupleRange(openStartTimes[index], openEndTimes[index], current):
                    isOpen = True
                    break

        return isOpen

    def handleChooseBfClick(self, *args):
        p = BigWorld.player()
        stage = getattr(p, 'battleFieldStage', 1)
        if stage != uiConst.BF_PANEL_STAGE_INIT:
            return
        preTarget = self.target
        self.target = ASObject(args[3][0]).currentTarget
        preTarget.selectFrame.visible = False
        self.target.selectFrame.visible = True
        self.isBFButtonSelected = not (self.target.unlockFrame.visible or not self.target.enabled)
        self.selectBFByIndex(self.target.data['idx'])

    def selectBFByIndex(self, fbMode):
        if fbMode < 0:
            return
        p = BigWorld.player()
        stage = getattr(p, 'battleFieldStage', 1)
        if stage != 1:
            value = BFMD.data.get(fbMode)
            if p.battleFieldFbNo in value.get('fbs', []):
                if self.widget:
                    self._selectBFByIndex(fbMode)
        elif self.widget:
            self._selectBFByIndex(fbMode)

    def _selectBFByIndex(self, idx):
        curTarget = None
        for i in xrange(len(self.widget.data)):
            if i >= MAX_ACTIVITY_NUM:
                break
            mc = self.widget.getChildByName('activity%d' % i)
            if mc.data['idx'] != idx:
                mc.selected = False
                tempdata = mc.data
                tempdata['selected'] = False
                mc.data = tempdata
            else:
                mc.selected = True
                tempdata = mc.data
                tempdata['selected'] = True
                mc.data = tempdata
                curTarget = mc

        if curTarget:
            self.selectBF(curTarget.data)

    def handleApplyOfTeamClick(self, *args):
        stage = self.myBfStage
        idx = self.myBfId
        p = BigWorld.player()
        if stage == uiConst.BF_PANEL_STAGE_INIT:
            bfMode = BFMD.data.get(idx, {}).get('mode', 0)
            if self.isModeHunt:
                self.apply(stage, idx)
            else:
                if not self.teamCheck(idx):
                    return
                p.cell.applyBattleFieldOfTeam(self.getBattleFieldFbNo(idx), gametypes.BATTLE_FIELD_APPLY_GROUP_OF_TEAM, self.getGroupHeaderCandidateFlag(), False)
        elif stage == uiConst.BF_PANEL_STAGE_APPLYED:
            p.cancelApplyBattleField()
        elif stage == uiConst.BF_PANEL_STAGE_IN_GAME:
            p.cell.quitBattleField()

    def handleApplyCommanderSelect(self, *args):
        if self.widget.applyCommander:
            self.cFlag = self.widget.applyCommander.selected

    def teamCheck(self, bfId):
        p = BigWorld.player()
        if not self._bfConditionCheck(bfId):
            return False
        if not p.isInTeamOrGroup():
            p.showGameMsg(GMDD.data.DUEL_APPLY_FAILED_NOT_IN_GROUP, ())
            return False
        if p.groupHeader != p.id:
            p.showGameMsg(GMDD.data.DUEL_APPLY_FAILED_NOT_HEADER, ())
            return False
        return True

    def handleApplyClick(self, *args):
        self.apply(self.myBfStage, self.myBfId)

    def apply(self, stage, bfId):
        p = BigWorld.player()
        if stage == uiConst.BF_PANEL_STAGE_INIT:
            if not self._bfConditionCheck(bfId):
                return
            if p.isInTeamOrGroup():
                p.showGameMsg(GMDD.data.APPLY_FAILED_IN_GROUP, ())
                return
            p.cell.applyBattleField(self.getBattleFieldFbNo(bfId), self.getGroupHeaderCandidateFlag(), False)
        self.refreshBF()

    def handleApplyOfDoubleBtnClick(self, *args):
        stage = self.myBfStage
        bfId = self.myBfId
        p = BigWorld.player()
        if stage == uiConst.BF_PANEL_STAGE_INIT:
            if not self.teamCheck(bfId):
                return
            p.cell.applyBattleFieldOfTeam(self.getBattleFieldFbNo(bfId), gametypes.BATTLE_FIELD_APPLY_GROUP_OF_DOUBLE, self.getGroupHeaderCandidateFlag(), False)

    def getGroupHeaderCandidateFlag(self):
        return self.cFlag

    def getBattleFieldFbNo(self, bfIdx):
        p = BigWorld.player()
        if p.battleFieldFbNo != 0:
            return p.battleFieldFbNo
        else:
            enableCrossServerBF = gameglobal.rds.configData.get('enableCrossServerBF', False)
            mode = BFMD.data.get(bfIdx, {}).get('mode', 1)
            fbNo = formula.genBattleFieldFbNoByLv(p.lv, bfIdx, False, self.isTodayActivity)
            if enableCrossServerBF and utils.getBattleFieldRegionInfo(fbNo) != (0, 0, 0):
                fbNo = formula.genBattleFieldFbNoByLv(p.lv, bfIdx, True, self.isTodayActivity)
            if fbNo:
                return fbNo
            gamelog.info('@hjx getBattleFieldFbNo:', p.lv)
            return 0

    def _bfConditionCheck(self, fbId):
        if not utils.canEnterPvP():
            return False
        minLv, maxLv = formula.getBattleFieldLvReq(fbId)
        p = BigWorld.player()
        if p.lv < minLv or p.lv > maxLv:
            p.showGameMsg(GMDD.data.BATTLE_FIELD_APPLY_FAILED_LV, (minLv, maxLv))
            return False
        return True

    def onGetTodayBFButtonList(self):
        p = BigWorld.player()
        ret = []
        self.isTodayActivity = True
        isActivitySelected = False
        for key, val in BFMD.data.items():
            if not self.isBFAvaliable(val):
                continue
            if not self.isInTodayActivity(val):
                continue
            weekSet = val.get('weekSet', 0)
            if weekSet and utils.isInvalidWeek(weekSet):
                continue
            obj = {}
            self.getBasicBfInfo(obj, val, key)
            self.getBFTodayDesc(obj, val)
            self.getBFOpenLvDesc(obj, val)
            obj['isOpen'] = self.isTodayActivityAvaliable(val)
            obj['selected'] = False
            obj['chaosMode'] = val.get('isChaos', 0) and gameconfigCommon.enableBattleFieldChaosMode()
            obj['chaosTimeDesc'] = val.get('chaosTimeDesc', '')
            obj['isShowNewFlagBF'] = val.get('isShowNewFlagBF', 0)
            if self.isTodayActivityAvaliable(val) and (p.battleFieldFbNo in val.get('fbs', []) or p.battleFieldFbNo in val.get('crossServerFbs', [])):
                obj['selected'] = True
                isActivitySelected = True
            ret.append(obj)

        if not isActivitySelected:
            for activityData in ret:
                if activityData.get('isOpen', True):
                    activityData['selected'] = True
                    break

        return ret

    def isBFAvaliable(self, bfItem):
        p = BigWorld.player()
        isEnableFlagBf = gameglobal.rds.configData.get('enableFlagBf', False)
        mode = bfItem.get('mode', const.BATTLE_FIELD_MODE_FLAG)
        if mode == const.BATTLE_FIELD_MODE_FLAG and not isEnableFlagBf:
            return False
        isEnableFortBf = utils.isEnableFortBf()
        if mode == const.BATTLE_FIELD_MODE_FORT and not isEnableFortBf:
            return False
        if mode == const.BATTLE_FIELD_MODE_HOOK and not utils.isEnableHookBf():
            return False
        if gameglobal.rds.configData.get('enableDuelTimeCheck', True) and not bfItem.get('isPvpPanelShow', False):
            return False
        isEnalbeHuntBf = gameglobal.rds.configData.get('enableHuntBf', False)
        if mode == const.BATTLE_FIELD_MODE_HUNT and not isEnalbeHuntBf:
            return False
        if mode == const.BATTLE_FIELD_MODE_DOTA and not utils.isDotaBfOpen():
            return False
        if mode == const.BATTLE_FIELD_MODE_NEW_FLAG and not gameglobal.rds.configData.get('enableNewFlagBF', False):
            return False
        if mode == const.BATTLE_FIELD_MODE_RACE and not gameglobal.rds.configData.get('enableRaceBattleField', False):
            return False
        if mode == const.BATTLE_FIELD_MODE_CQZZ and not gameglobal.rds.configData.get('enableCqzzBf', False):
            return False
        if bfItem.get('isChaos') and not gameconfigCommon.enableBattleFieldChaosMode():
            return False
        if mode == const.BATTLE_FIELD_MODE_LZS and not gameglobal.rds.configData.get('enableLZSBattleField', False):
            return False
        if mode == const.BATTLE_FIELD_MODE_PUBG and not p.isCanJoinPUBG():
            return False
        if mode == const.BATTLE_FIELD_MODE_TIMING_PUBG and not p.isCanJoinTimingPUBG():
            return False
        return True

    def isInTodayActivity(self, bfItem):
        if not bfItem.get('isInTodayActivity', 0):
            return False
        todayActivityStartTime = bfItem.get('todayActivityStartTime', ())
        weekDay = utils.localtimeEx(utils.getNow(), False).tm_wday
        for i in xrange(0, len(todayActivityStartTime)):
            if not todayActivityStartTime[i]:
                continue
            weekList = todayActivityStartTime[i][0][4]
            for week in weekList:
                if weekDay == week:
                    return True

        return False

    def getBasicBfInfo(self, obj, bfItem, key):
        p = BigWorld.player()
        mode = bfItem.get('mode', const.BATTLE_FIELD_MODE_FLAG)
        obj['idx'] = key
        obj['id'] = mode
        obj['name'] = bfItem.get('name', '')
        obj['isOpenDouble'] = bfItem.get('isOpenDouble', False)
        obj['modeHunt'] = mode == const.BATTLE_FIELD_MODE_HUNT or mode == const.BATTLE_FIELD_MODE_RACE
        obj['showDotaHeros'] = mode == const.BATTLE_FIELD_MODE_DOTA and gameglobal.rds.configData.get('enableBfDotaHeros', False) and p.lv >= SCD.data.get('bfDotaOpenLv', 40)
        obj['bg'] = 'pvpPanel/%s.dds' % bfItem.get('bg', 'default')
        obj['visible'] = 1
        obj['teamApplyBtnNeedShow'] = self.teamApplyBtnNeedShow(key)
        obj['icon'] = bfItem.get('icon', 0)

    def teamApplyBtnNeedShow(self, key):
        needShow = False
        teamOpenStartTimes = BFMD.data.get(key, {}).get('teamOpenStartTimes', ())
        teamOpenEndTimes = BFMD.data.get(key, {}).get('teamOpenEndTimes', ())
        current = utils.getNow()
        if len(teamOpenStartTimes) == 0:
            needShow = True
        else:
            for index in xrange(len(teamOpenStartTimes)):
                if utils.inTimeTupleRange(teamOpenStartTimes[index], teamOpenEndTimes[index], current):
                    needShow = True
                    break

        return needShow

    def getBFTodayDesc(self, obj, bfItem):
        obj['desc'] = bfItem.get('todayDesc', '')
        obj['numberDesc'] = bfItem.get('todayNumberDesc', '')
        obj['timeDesc'] = bfItem.get('todayTimeDesc', '')
        obj['timeShortDesc'] = bfItem.get('todayTimeShortDesc', '')
        obj['priceDesc'] = bfItem.get('todayPriceDesc', '')
        obj['openLvDesc'] = bfItem.get('todayOpenLvDesc', '%d~~%d')
        obj['winStandard'] = bfItem.get('todaywinStandard', '')

    def getBFOpenLvDesc(self, obj, bfItem):
        p = BigWorld.player()
        lv = getattr(p, 'lv', 99)
        bd = BFD.data
        fbs = bfItem.get('fbs', [])
        minLv = 0
        maxLv = 0
        minLvTemp = 0
        maxLvTemp = 0
        minFbId = 0
        maxFbId = 0
        for fbId in fbs:
            lvRange = bd.get(fbId, {}).get('lv', (1, 99))
            if lv >= lvRange[0] and lv <= lvRange[1]:
                minLv = lvRange[0]
                maxLv = lvRange[1]
                break
            else:
                if minLvTemp == 0 or minLvTemp > lvRange[0]:
                    minLvTemp = lvRange[0]
                    minFbId = fbId
                if maxLvTemp == 0 or maxLvTemp < lvRange[1]:
                    maxLvTemp = lvRange[1]
                    maxFbId = fbId

        if minLv == 0 and maxLv == 0:
            lvRange = (1, 99)
            if lv < minLvTemp:
                lvRange = bd.get(minFbId, {}).get('lv', (1, 99))
            elif lv > maxLvTemp:
                lvRange = bd.get(maxFbId, {}).get('lv', (1, 99))
            minLv = lvRange[0]
            maxLv = lvRange[1]
        if obj['openLvDesc'].count('%d'):
            if obj['openLvDesc'].count('%d') == 1:
                obj['openLvDesc'] = obj['openLvDesc'] % minLv
            else:
                obj['openLvDesc'] = obj['openLvDesc'] % (minLv, maxLv)

    def isTodayActivityAvaliable(self, bfItem):
        if not gameglobal.rds.configData.get('enableDuelTimeCheck', True):
            return True
        mode = bfItem.get('mode', const.BATTLE_FIELD_MODE_FLAG)
        if mode == const.BATTLE_FIELD_MODE_NEW_FLAG:
            openStartTimes = bfItem.get('openStartTimes', ())
            openEndTimes = bfItem.get('openEndTimes', ())
            for index in xrange(len(openStartTimes)):
                if utils.inTimeTupleRange(openStartTimes[index], openEndTimes[index], utils.getNow()):
                    return True

        else:
            todayActivityStartTime = bfItem.get('todayActivityStartTime', ())
            todayActivityEndTime = bfItem.get('todayActivityEndTime', ())
            for i in xrange(0, len(todayActivityStartTime)):
                if not todayActivityStartTime[i]:
                    continue
                if utils.inTimeTupleRange(todayActivityStartTime[i][0], todayActivityEndTime[i][0], utils.getNow()):
                    return True

        return False
