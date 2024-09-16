#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pvpBattleFieldV2Proxy.o
import BigWorld
import math
import utils
import const
import events
import copy
import uiConst
import formula
import gamelog
import gametypes
import gameglobal
from uiProxy import UIProxy
from guis.asObject import ASObject
from gamestrings import gameStrings
from data import battle_field_mode_data as BFMD
from data import battle_field_data as BFD
from data import battle_field_history_data as BFHD
from data import sys_config_data as SCD
from data import duel_config_data as DCD
from cdata import game_msg_def_data as GMDD
from cdata import battlefield_region_config_data as BRCD
from cdata import new_battlefield_region_config_data as NBRCD
OVERVIEW_BF_DATA = 0
INIT_APPLY_PERSON_BTN_X = 456
INIT_APPLY_DOUBLE_BTN_X = 593
INIT_APPLY_BTN_OFFSET = 137
RADER_DESCS = [gameStrings.PVP_PARTICIPATE_BEAT,
 gameStrings.PVP_DEMAGE_ABILITY,
 gameStrings.PVP_CURE_ABILITY,
 gameStrings.PVP_SUFFER_ABILITY,
 gameStrings.PVP_BF_CONTRIBUTION]
radius = [12,
 24,
 40,
 57,
 75]
defaultLimit = (300, 1000, 2000, 100000)
ICON_PATH = 'pvpPanel/%d.dds'

class PvpBattleFieldV2Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PvpBattleFieldV2Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.cFlag = 0
        self.tabData = {const.BATTLE_FIELD_MODE_RES: {},
         const.BATTLE_FIELD_MODE_FLAG: {},
         const.BATTLE_FIELD_MODE_FORT: {},
         const.BATTLE_FIELD_MODE_NEW_FLAG: {},
         const.BATTLE_FIELD_MODE_PUBG: {},
         OVERVIEW_BF_DATA: {}}
        self.isTodayActivity = False
        self.isSelectUpRegion = False

    def reset(self):
        pass

    def initPanel(self, widget):
        self.widget = widget
        self.refreshActivity()
        self.myBfId = -1
        self.bfStage = 0
        self.buildHistoryItem()
        self.initData()
        p = BigWorld.player()
        p.cell.queryBattleFieldHistoryDataCell(p.bfHistoryVers[0], p.bfHistoryVers[1], p.bfHistoryVers[2], p.bfHistoryVers[3], p.bfHistoryVers[4], p.bfHistoryVers[5], [], const.BATTLE_FIELD_HISTORY_LEIDA)

    def unRegisterPanel(self):
        self.widget = None

    def initUI(self):
        isSelectFrame = False
        self.initBFButtonList()
        self.widget.data = self.onGetBFButtonList()
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.descPanel.barAlwaysVisible = True
        for i in xrange(min(len(self.widget.data), 3)):
            mc = self.widget.getChildByName('activity%d' % i)
            mc.data = self.widget.data[i]
            mc.visible = mc.data['visible']
            mc.enabled = mc.data['isOpen']
            if mc.enabled:
                mc.unlockFrame.visible = False
            mc.nameTxt.text = mc.data['name']
            mc.toggle = True
            mc.selected = mc.data['selected'] if mc.data.has_key('selected') else False
            mc.vsNumTxt.text = mc.data['numberDesc']
            mc.startLvTxt.text = mc.data['openLvDesc']
            mc.startDayTxt.text = mc.data['timeShortDesc']
            if mc.data['icon']:
                mc.pictrue.loadImage(ICON_PATH % mc.data['icon'])
            mc.startTimeTxt.visible = False
            mc.turn.visible = not i
            mc.checkBox.visible = not i
            mc.checkBox.addEventListener(events.BUTTON_CLICK, self.handleCheckBoxClick, False, 0, True)
            if not isSelectFrame and mc.selected:
                mc.selectFrame.visible = True
                isSelectFrame = not isSelectFrame
            if mc.selected or mc.data['isInfoNeedShow'] and self.myBfId < 0:
                self.selectBF(mc.data)

        self.target = self.widget.activity0
        self.refreshBF()
        self.setRaderInfo()
        self.setMedal()

    def updateUpRegionSelectBtn(self):
        fbNo = self.getBattleFieldFbNo(self.myBfId)
        lvRange = BFD.data.get(fbNo, {}).get('lv', ())
        hostId = utils.getHostId()
        if (hostId, lvRange, fbNo) in NBRCD.data:
            regionConfigData = NBRCD.data
        else:
            regionConfigData = BRCD.data
        upConfigData = regionConfigData.get((hostId, lvRange), {}).get('upRegionConfig', ())
        isVisabel = True if upConfigData else False
        self.widget.upRegionSelectBtn.visible = gameglobal.rds.configData.get('enableUpBFRegion', False) and isVisabel
        self.widget.warHelpIcon.visible = gameglobal.rds.configData.get('enableUpBFRegion', False) and isVisabel
        self.widget.warHelpIcon.helpKey = 405

    def buildHistoryItem(self):
        self.gloryDataKey = []
        self.commonDataKey = []
        for id, item in BFHD.data.iteritems():
            if item.get('isGloryData', 0):
                self.gloryDataKey.append(item)
            else:
                self.commonDataKey.append(item)

    def normalizeTabData(self):
        for k, data in self.tabData.iteritems():
            if isinstance(data, dict):
                for key, item in data.iteritems():
                    if item < 0:
                        data[key] = 0

    def getValueList(self, key):
        p = BigWorld.player()
        valueList = [self.tabData[const.BATTLE_FIELD_MODE_RES].get(key, 0), self.tabData[const.BATTLE_FIELD_MODE_FLAG].get(key, 0), self.tabData[const.BATTLE_FIELD_MODE_FORT].get(key, 0)]
        if gameglobal.rds.configData.get('enableNewFlagBF', False):
            valueList.append(self.tabData[const.BATTLE_FIELD_MODE_NEW_FLAG].get(key, 0))
        if gameglobal.rds.configData.get('enableCqzzBf', False):
            valueList.append(self.tabData[const.BATTLE_FIELD_MODE_CQZZ].get(key, 0))
        if p.isCanJoinPUBG():
            valueList.append(self.tabData[const.BATTLE_FIELD_MODE_PUBG].get(key, 0))
        return valueList

    def initData(self):
        p = BigWorld.player()
        if p.bfHistoryInfo.get('battleFieldFortHistory', {}):
            self.tabData[const.BATTLE_FIELD_MODE_RES] = copy.deepcopy(p.bfHistoryInfo.get('battleFieldResHistory', {}))
            self.tabData[const.BATTLE_FIELD_MODE_FLAG] = copy.deepcopy(p.bfHistoryInfo.get('battleFieldFlagHistory', {}))
            self.tabData[const.BATTLE_FIELD_MODE_FORT] = copy.deepcopy(p.bfHistoryInfo.get('battleFieldFortHistory', {}))
            self.tabData[const.BATTLE_FIELD_MODE_NEW_FLAG] = copy.deepcopy(p.bfHistoryInfo.get('battleFieldNewFlagHistory', {}))
            self.tabData[const.BATTLE_FIELD_MODE_CQZZ] = copy.deepcopy(p.bfHistoryInfo.get('battleFieldCqzzHistory', {}))
            self.tabData[const.BATTLE_FIELD_MODE_PUBG] = copy.deepcopy(p.bfHistoryInfo.get('battleFieldPUBGHistory', {}))
            self.normalizeTabData()
            for item in self.gloryDataKey:
                key = item.get('key', 0)
                self.tabData[OVERVIEW_BF_DATA][key] = sum(self.getValueList(key))

            for item in self.commonDataKey:
                key = item.get('key', 0)
                if not item.get('type', 0):
                    self.tabData[OVERVIEW_BF_DATA][key] = sum(self.getValueList(key))

        self.initUI()

    def setMedal(self):
        medal = [self.tabData[OVERVIEW_BF_DATA].get('mvp', 0),
         self.tabData[OVERVIEW_BF_DATA].get('firstCnt', 0),
         self.tabData[OVERVIEW_BF_DATA].get('secondCnt', 0),
         self.tabData[OVERVIEW_BF_DATA].get('thirdCnt', 0)]
        medal_text = [self.widget.mvpNum,
         self.widget.longjiangNum,
         self.widget.huweiNum,
         self.widget.baoqiNum]
        for i in xrange(len(medal)):
            medal_text[i].text = medal[i]

    def convertNum(self, num):
        if type(num) == str:
            return num
        elif num > 100000000:
            return gameStrings.BF_HISTORY_YI % ('%.2f' % (num / 100000000))
        elif num > 10000:
            return gameStrings.BF_HISTORY_WAN % int(num / 10000)
        else:
            return str(int(num))

    def setRaderInfo(self):
        for i in xrange(5):
            raderDesc = self.widget.getChildByName('desc%d' % i)
            raderDesc.text = RADER_DESCS[i]

        tabData = self.tabData.get(OVERVIEW_BF_DATA, {})
        for idx in xrange(0, len(self.commonDataKey)):
            if self.commonDataKey[idx].get('type', 0):
                if self.commonDataKey[idx].get('type', 0) != OVERVIEW_BF_DATA:
                    continue
            key = self.commonDataKey[idx].get('key', '')
            if self.commonDataKey[idx].get('isAverage', 0):
                divide = self.commonDataKey[idx].get('divide', [])
                if not tabData.get(divide[1], 0):
                    tabData[key] = 0
                elif self.commonDataKey[idx].get('isPercentForm', 0):
                    tabData[key] = '%d%%' % int(tabData.get(divide[0], 0) * 1.0 / tabData.get(divide[1], 0) * 100)
                else:
                    tabData[key] = int(tabData.get(divide[0], 0) / tabData.get(divide[1], 0))

        data = [self.tabData[OVERVIEW_BF_DATA].get('averJibai', 0),
         self.tabData[OVERVIEW_BF_DATA].get('averDamage', 0),
         self.tabData[OVERVIEW_BF_DATA].get('averCure', 0),
         self.tabData[OVERVIEW_BF_DATA].get('averBeDamage', 0),
         self.tabData[OVERVIEW_BF_DATA].get('averDonateScore', 0)]
        for i in xrange(len(data)):
            radertext = self.widget.getChildByName('radar%d' % i)
            radertext.text = self.convertNum(data[i])

        mc = self.widget.socialRadar.inner
        limit = []
        limit.append(list(DCD.data.get('averJibaiLimit', defaultLimit)))
        limit.append(list(DCD.data.get('averDamageLimit', defaultLimit)))
        limit.append(list(DCD.data.get('averCureLimit', defaultLimit)))
        limit.append(list(DCD.data.get('averBeDamageLimit', defaultLimit)))
        limit.append(list(DCD.data.get('averDonateScoreLimit', defaultLimit)))
        centerPointX = mc.width / 2 + 0.5
        centerPointY = mc.height / 2 + 4
        mc.graphics.clear()
        mc.graphics.moveTo(centerPointX, centerPointY - self.getRadius(limit[0], data[0], radius))
        angle = 360 / len(data)
        mc.graphics.beginFill(26316, 0.6)
        for i in xrange(len(data) - 1):
            pointX, pointY = self.getVertex(centerPointX, centerPointY, angle * i + (angle - 90), self.getRadius(limit[i + 1], data[i + 1], radius))
            mc.graphics.lineTo(pointX, pointY)

        mc.graphics.lineTo(centerPointX, centerPointY - self.getRadius(limit[0], data[0], radius))
        mc.graphics.endFill()

    def getRadius(self, limit, data, radius):
        for i in xrange(len(limit)):
            if data < limit[i]:
                return radius[i]

        return radius[len(limit)]

    def getVertex(self, centerPointX, centerPointY, angle, radius):
        dx = radius * math.cos(math.pi * angle / 180)
        dy = radius * math.sin(math.pi * angle / 180)
        return (centerPointX + dx, centerPointY + dy)

    def handleCheckBoxClick(self, *args):
        gameglobal.rds.ui.pvpBattleRotationV2.show()

    def refreshActivity(self):
        for i in xrange(3):
            mc = self.widget.getChildByName('activity%d' % i)
            mc.unlockFrame.visible = True
            mc.selectFrame.visible = False

    def initBFButtonList(self):
        self.widget.applyOfPersonBtn.addEventListener(events.BUTTON_CLICK, self.handleApplyClick, False, 0, True)
        self.widget.applyOfDoubleBtn.addEventListener(events.BUTTON_CLICK, self.handleApplyOfDoubleBtnClick, False, 0, True)
        self.widget.applyOfTeamBtn.addEventListener(events.BUTTON_CLICK, self.handleApplyOfTeamClick, False, 0, True)
        self.widget.applyCommander.addEventListener(events.EVENT_SELECT, self.handleApplyCommanderSelect, False, 0, True)
        self.widget.bfDotaHeros.addEventListener(events.BUTTON_CLICK, self.handleShowBfDotaHeros, False, 0, True)
        self.widget.battleFieldDataBtn.addEventListener(events.BUTTON_CLICK, self.handleBattleFieldDataClick, False, 0, True)
        self.widget.activity0.addEventListener(events.MOUSE_CLICK, self.handleChooseBfClick, False, 0, True)
        self.widget.activity1.addEventListener(events.MOUSE_CLICK, self.handleChooseBfClick, False, 0, True)
        self.widget.activity2.addEventListener(events.MOUSE_CLICK, self.handleChooseBfClick, False, 0, True)
        self.widget.upRegionSelectBtn.addEventListener(events.EVENT_SELECT, self.handleUpRegionSelect, False, 0, True)
        self.widget.bfGradingBtn.addEventListener(events.BUTTON_CLICK, self.handleBfGradingBtnClick, False, 0, True)
        self.widget.bfRewardBtn.addEventListener(events.BUTTON_CLICK, self.handleBfRewardBtnClick, False, 0, True)
        self.refreshApplyCommander()

    def handleBfGradingBtnClick(self, *args):
        if self.myBfId == const.BATTLE_FIELD_MODE_PUBG:
            gameglobal.rds.ui.rankCommon.showRankCommon(gametypes.TOP_TYPE_PUBG_GRADING_RANK)

    def handleBfRewardBtnClick(self, *args):
        if self.myBfId == const.BATTLE_FIELD_MODE_PUBG:
            gameglobal.rds.ui.generalReward.show(gametypes.GENERAL_REWARD_PUBG)

    def handleUpRegionSelect(self, *args):
        self.isSelectUpRegion = self.widget.upRegionSelectBtn.selected

    def handleBattleFieldDataClick(self, *args):
        p = BigWorld.player()
        gameglobal.rds.ui.battleFieldHistory.isNeedShow = True
        p.cell.queryBattleFieldHistoryDataCell(p.bfHistoryVers[0], p.bfHistoryVers[1], p.bfHistoryVers[2], p.bfHistoryVers[3], p.bfHistoryVers[4], p.bfHistoryVers[5], [], const.BATTLE_FIELD_HISTORY_SHENGYA)
        if p.bfHistoryInfo.get('battleFieldFortHistory', {}):
            gameglobal.rds.ui.battleFieldHistory.show()

    def handleShowBfDotaHeros(self, *args):
        gameglobal.rds.ui.bfDotaHeros.show()

    def handleChooseBfClick(self, *args):
        preTarget = self.target
        self.target = ASObject(args[3][0]).currentTarget
        if self.target.unlockFrame.visible or not self.target.enabled:
            return
        for i in xrange(3):
            mc = self.widget.getChildByName('activity%d' % i)
            mc.selectFrame.visible = False

        preTarget.selectFrame.visible = False
        self.target.selected = True
        self.setMcDataByName(self.target, 'selected', True)
        self.target.selectFrame.visible = True
        self.selectBFByIndex(self.target.data['idx'])

    def selectBFByIndex(self, fbMode):
        if fbMode < 0:
            return
        else:
            p = BigWorld.player()
            curTargetMc = None
            stage = getattr(p, 'battleFieldStage', 1)
            if stage != 1:
                value = BFMD.data.get(fbMode)
                if p.battleFieldFbNo in value.get('fbs', []) and self.isBattleNeedShow(fbMode):
                    if self.widget:
                        curTargetMc = self.getSelectTargetMcByIndex(fbMode, setSelectedData=True)
            elif self.widget and self.isBattleNeedShow(fbMode):
                curTargetMc = self.getSelectTargetMcByIndex(fbMode, setSelectedData=True)
            if curTargetMc:
                self.selectBF(curTargetMc.data)
            return

    def getSelectTargetMcByIndex(self, idx, setSelectedData = False):
        curTarget = None
        for i in xrange(min(len(self.widget.data), 3)):
            mc = self.widget.getChildByName('activity%d' % i)
            if mc.data['idx'] == idx:
                curTarget = mc
            if setSelectedData:
                if mc.data['idx'] != idx:
                    mc.selected = False
                    self.setMcDataByName(mc, 'selected', False)
                else:
                    mc.selected = True
                    self.setMcDataByName(mc, 'selected', True)

        return curTarget

    def setMcDataByName(self, mc, name, value):
        if mc.data:
            tempdata = mc.data
            tempdata[name] = value
            mc.data = tempdata

    def selectBF(self, data):
        self.myBfId = data['idx']
        textMc = self.widget.descPanel.canvas.text
        textMc.htmlText = ''
        if data['desc']:
            textMc.htmlText += data['desc'] + '\n\n'
        if data['timeDesc']:
            textMc.htmlText += data['timeDesc'] + '\n\n'
        if data['winStandard']:
            textMc.htmlText += data['winStandard'] + '\n\n'
        if data['priceDesc']:
            textMc.htmlText += data['priceDesc']
        textMc.height = textMc.textHeight + 20
        self.widget.descPanel.validateNow()
        self.widget.descPanel.refreshHeight()
        self.isOpenDouble = data['isOpenDouble']
        self.isModeHunt = data['modeHunt']
        self.isTeamBtnShow = data['teamApplyBtnNeedShow']
        self.isBFButtonSelected = data['selected'] if data.has_key('selected') else False
        self.widget.applyOfPersonBtn.visible = not self.isModeHunt
        self.widget.applyOfDoubleBtn.visible = self.isOpenDouble and not self.isModeHunt
        self.widget.applyOfTeamBtn.visible = not self.isModeHunt
        self.widget.applyCommander.visible = not self.isModeHunt
        self.updateUpRegionSelectBtn()
        self.refreshOtherUI(data)
        self.setBfStage(self.bfStage)

    def refreshOtherUI(self, data):
        p = BigWorld.player()
        self.widget.bfGradingTxt.visible = False
        self.widget.bfGradingBtn.visible = False
        self.widget.bfRewardBtn.visible = False
        self.widget.bfHelpIcon.visible = False
        self.widget.bfDotaHeros.visible = False
        if data['id'] == const.BATTLE_FIELD_MODE_PUBG:
            self.widget.bfGradingTxt.visible = True
            self.widget.bfGradingBtn.visible = True
            self.widget.bfRewardBtn.visible = True
            self.widget.bfHelpIcon.visible = True
            self.widget.applyCommander.visible = False
            self.widget.bfHelpIcon.helpKey = DCD.data.get('pubgBattleFieldHelpKey', 0)
            self.widget.bfGradingTxt.htmlText = DCD.data.get('pubgPVPBattleFieldRankTxt', gameStrings.PUBG_PVP_BATTLE_FIELD_V2_RANK_TXT) % (p.getCurRankNameInPUBG(), p.pubgRankPoints)
        elif data['id'] == const.BATTLE_FIELD_MODE_DOTA and gameglobal.rds.configData.get('enableBfDotaHeros', False) and p.lv >= SCD.data.get('bfDotaOpenLv', 40):
            self.widget.applyCommander.visible = False
            self.widget.bfDotaHeros.visible = True

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
        self.setBFBtnVisibleWithSelected()

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
        self.updateUpRegionBtnEnabled()

    def setStage2Info(self):
        self.widget.applyOfPersonBtn.visible = False
        self.widget.applyOfDoubleBtn.visible = False
        self.widget.applyOfTeamBtn.label = gameStrings.PVP_QUIT_QUEUE
        self.widget.applyOfTeamBtn.visible = True
        self.refreshApplyCommander()
        self.updateUpRegionBtnEnabled()

    def setStage3Info(self):
        self.widget.applyOfPersonBtn.visible = False
        self.widget.applyOfDoubleBtn.visible = False
        self.widget.applyOfTeamBtn.visible = False
        self.refreshApplyCommander()
        self.updateUpRegionBtnEnabled()

    def setStage4Info(self):
        self.widget.applyOfPersonBtn.visible = False
        self.widget.applyOfDoubleBtn.visible = False
        self.widget.applyOfTeamBtn.label = gameStrings.PVP_QUIT_GAME
        self.widget.applyOfTeamBtn.visible = False
        self.refreshApplyCommander()
        self.updateUpRegionBtnEnabled()

    def setBFBtnVisibleWithSelected(self):
        if not self.isBFButtonSelected:
            self.widget.applyOfTeamBtn.visible = False
            self.widget.applyOfDoubleBtn.visible = False
            self.widget.applyOfPersonBtn.visible = False
            self.widget.applyCommander.visible = False

    def refreshApplyCommander(self):
        checkboxEnable = getattr(BigWorld.player(), 'battleFieldStage', 1) == uiConst.BF_PANEL_STAGE_INIT
        self.widget.applyCommander.enabled = checkboxEnable
        self.widget.applyCommander.selected = self.cFlag

    def updateUpRegionBtnEnabled(self):
        if not self.widget.upRegionSelectBtn.visible:
            return
        checkboxEnable = getattr(BigWorld.player(), 'battleFieldStage', 1) == uiConst.BF_PANEL_STAGE_INIT
        self.widget.upRegionSelectBtn.enabled = checkboxEnable
        self.widget.upRegionSelectBtn.selected = self.isSelectUpRegion

    def handleApplyCommanderSelect(self, *args):
        if self.widget.applyCommander:
            self.cFlag = self.widget.applyCommander.selected

    def handleApplyClick(self, *args):
        self.apply(self.myBfStage, self.myBfId)

    def apply(self, stage, bfId):
        p = BigWorld.player()
        if stage == uiConst.BF_PANEL_STAGE_INIT:
            if not self.personCheck(bfId):
                return
            p.cell.applyBattleField(self.getBattleFieldFbNo(bfId), self.getGroupHeaderCandidateFlag(), self.isSelectUpRegion)
        self.refreshBF()

    def handleApplyOfDoubleBtnClick(self, *args):
        stage = self.myBfStage
        bfId = self.myBfId
        p = BigWorld.player()
        if stage == uiConst.BF_PANEL_STAGE_INIT:
            if not self.teamCheck(bfId):
                return
            p.cell.applyBattleFieldOfTeam(self.getBattleFieldFbNo(bfId), gametypes.BATTLE_FIELD_APPLY_GROUP_OF_DOUBLE, self.getGroupHeaderCandidateFlag(), self.isSelectUpRegion)

    def handleApplyOfTeamClick(self, *args):
        stage = self.myBfStage
        idx = self.myBfId
        p = BigWorld.player()
        if stage == uiConst.BF_PANEL_STAGE_INIT:
            bfMode = BFMD.data.get(idx, {}).get('mode', 0)
            if bfMode == const.BATTLE_FIELD_MODE_HUNT:
                self.apply(stage, idx)
            else:
                if not self.teamCheck(idx):
                    return
                p.cell.applyBattleFieldOfTeam(self.getBattleFieldFbNo(idx), gametypes.BATTLE_FIELD_APPLY_GROUP_OF_TEAM, self.getGroupHeaderCandidateFlag(), self.isSelectUpRegion)
        elif stage == uiConst.BF_PANEL_STAGE_APPLYED:
            p.cancelApplyBattleField()
        elif stage == uiConst.BF_PANEL_STAGE_IN_GAME:
            p.cell.quitBattleField()

    def teamCheck(self, bfId):
        p = BigWorld.player()
        if not self.bfConditionCheck(bfId):
            return False
        if not p.isInTeamOrGroup():
            p.showGameMsg(GMDD.data.DUEL_APPLY_FAILED_NOT_IN_GROUP, ())
            return False
        if p.groupHeader != p.id:
            p.showGameMsg(GMDD.data.DUEL_APPLY_FAILED_NOT_HEADER, ())
            return False
        return True

    def personCheck(self, bfId):
        p = BigWorld.player()
        if not self.bfConditionCheck(bfId):
            return False
        if p.isInTeamOrGroup():
            p.showGameMsg(GMDD.data.APPLY_FAILED_IN_GROUP, ())
            return False
        return True

    def getGroupHeaderCandidateFlag(self):
        return self.cFlag

    def getBattleFieldFbNo(self, bfIdx):
        p = BigWorld.player()
        if p.battleFieldFbNo != 0:
            return p.battleFieldFbNo
        else:
            enableCrossServerBF = gameglobal.rds.configData.get('enableCrossServerBF', False)
            fbNo = formula.genBattleFieldFbNoByLv(p.lv, bfIdx, False, self.isTodayActivity)
            if enableCrossServerBF and utils.getBattleFieldRegionInfo(fbNo, self.isSelectUpRegion, utils.getHostId()) != (0, 0, 0):
                fbNo = formula.genBattleFieldFbNoByLv(p.lv, bfIdx, True, self.isTodayActivity)
            if fbNo:
                return fbNo
            gamelog.info('@hjx getBattleFieldFbNo:', p.lv)
            return 0

    def bfConditionCheck(self, fbId):
        minLv, maxLv = formula.getBattleFieldLvReq(fbId)
        p = BigWorld.player()
        if not utils.canEnterPvP():
            return False
        if p.lv < minLv or p.lv > maxLv:
            p.showGameMsg(GMDD.data.BATTLE_FIELD_APPLY_FAILED_LV, (minLv, maxLv))
            return False
        return True

    def refreshBF(self):
        if not self.widget:
            return
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
        for i in xrange(min(len(self.widget.data), 3)):
            mc = self.widget.getChildByName('activity%d' % i)
            applyTabIdx = gameglobal.rds.ui.pvPPanel.getApply()
            if applyTabIdx != uiConst.APPLY_TABIDX_NONE and applyTabIdx != uiConst.APPLY_TABIDX_BATTLEFIELDV2:
                mc.enabled = False
                mc.unlockFrame.visible = True
                mc.selectFrame.visible = False
            elif not mc.data['isOpen']:
                mc.enabled = False
                mc.unlockFrame.visible = True
            else:
                mc.enabled = isEnable
                mc.unlockFrame.visible = not isEnable

    def bfCmp(self, val0, val1):
        priority0 = val0.get('priority', 0)
        priority1 = val1.get('priority', 0)
        if priority0 == priority1:
            id0 = val0.get('id', 0)
            id1 = val1.get('id', 0)
            return id0 - id1
        return priority1 - priority0

    def onGetBFButtonList(self):
        p = BigWorld.player()
        ret = []
        sel = False
        self.isTodayActivity = False
        for key, val in BFMD.data.items():
            if not self.isBFAvaliable(val):
                continue
            obj = {}
            self.getBasicBfInfo(obj, val, key)
            self.getBFDesc(obj, val)
            self.getBFOpenLvDesc(obj, val)
            obj['isOpen'] = self.isBattleNeedShow(key)
            obj['isInfoNeedShow'] = True
            if p.battleFieldFbNo in val.get('fbs', []) or p.battleFieldFbNo in val.get('crossServerFbs', []):
                obj['selected'] = True
                sel = True
            ret.append(obj)

        isSelected = False
        ret.sort(cmp=self.bfCmp)
        if len(ret) > 0 and not sel:
            for i in xrange(0, len(ret)):
                if ret[i]['isOpen'] and not isSelected:
                    ret[i]['selected'] = True
                    isSelected = True
                else:
                    ret[i]['selected'] = False

        return ret

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

    def getBFDesc(self, obj, bfItem):
        obj['desc'] = bfItem.get('desc', '')
        obj['numberDesc'] = bfItem.get('numberDesc', '')
        obj['timeDesc'] = bfItem.get('timeDesc', '')
        obj['timeShortDesc'] = bfItem.get('timeShortDesc', '')
        obj['priceDesc'] = bfItem.get('priceDesc', '')
        obj['openLvDesc'] = bfItem.get('openLvDesc', '%d~~%d')
        obj['winStandard'] = bfItem.get('winStandard', '')

    def getBasicBfInfo(self, obj, bfItem, key):
        p = BigWorld.player()
        mode = bfItem.get('mode', const.BATTLE_FIELD_MODE_FLAG)
        obj['idx'] = key
        obj['id'] = mode
        obj['name'] = bfItem.get('name', '')
        obj['priority'] = bfItem.get('priority', 0)
        obj['isOpenDouble'] = bfItem.get('isOpenDouble', False)
        obj['modeHunt'] = mode == const.BATTLE_FIELD_MODE_HUNT
        obj['bg'] = 'pvpPanel/%s.dds' % bfItem.get('bg', 'default')
        obj['visible'] = 1
        obj['teamApplyBtnNeedShow'] = self.teamApplyBtnNeedShow(key)
        obj['icon'] = bfItem.get('icon', 0)

    def teamApplyBtnNeedShow(self, key):
        p = BigWorld.player()
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

    def isBFAvaliable(self, bfItem):
        p = BigWorld.player()
        timeWrap = utils.localtimeEx(utils.getNow(), False)
        weekday = timeWrap.tm_wday
        openTimeDay = []
        if len(bfItem.get('openStartTimes', ())) != 0:
            openTimeDay = bfItem.get('openStartTimes', ())[0][-1]
        mode = bfItem.get('mode', const.BATTLE_FIELD_MODE_FLAG)
        if mode == const.BATTLE_FIELD_MODE_RES and weekday not in openTimeDay:
            return False
        if mode == const.BATTLE_FIELD_MODE_FLAG and weekday not in openTimeDay:
            return False
        isEnableFortBf = utils.isEnableFortBf()
        if mode == const.BATTLE_FIELD_MODE_FORT and not isEnableFortBf:
            return False
        if mode == const.BATTLE_FIELD_MODE_HOOK or mode == const.BATTLE_FIELD_MODE_HUNT:
            return False
        if gameglobal.rds.configData.get('enableDuelTimeCheck', True) and not bfItem.get('isPvpPanelShow', False):
            return False
        if mode == const.BATTLE_FIELD_MODE_CQZZ and (not gameglobal.rds.configData.get('enableCqzzBf', False) or weekday not in openTimeDay):
            return False
        if mode == const.BATTLE_FIELD_MODE_RACE and (not gameglobal.rds.configData.get('enableRaceBattleField', False) or weekday not in openTimeDay):
            return False
        if mode == const.BATTLE_FIELD_MODE_PUBG and (not p.isCanJoinPUBG() or weekday not in openTimeDay or gameglobal.rds.configData.get('enablePVPPUBGProxy', False)):
            return False
        if mode == const.BATTLE_FIELD_MODE_TIMING_PUBG:
            return False
        return True
