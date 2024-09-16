#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pvpPUBGProxy.o
import BigWorld
import gameglobal
import utils
import copy
import datetime
import uiUtils
import const
import gametypes
import events
import math
import formula
import gamelog
import pubgUtils
import duelUtils
from guis.asObject import ASUtils
from guis import ui
from uiProxy import UIProxy
from guis import pinyinConvert
from guis import uiConst
from guis.asObject import ASObject
from guis.asObject import TipManager
from gamestrings import gameStrings
from callbackHelper import Functor
from guis import menuManager
from guis.asObject import MenuManager
from guis import arenaPlayoffsProxy
from data import duel_config_data as DCD
from cdata import game_msg_def_data as GMDD
from data import battle_field_mode_data as BFMD
from data import fame_data as FD
defaultLimit = (0, 20, 30, 40, 50)
defaultLimit2 = (0, 20000, 30000, 40000, 50000)
radius = [12,
 25,
 40,
 57,
 75]
INIT_APPLY_PERSON_BTN_X = 593

class PvpPUBGProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PvpPUBGProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.allBasicData = dict()
        self.bfStage = uiConst.BF_PANEL_STAGE_INIT

    def unRegisterPanel(self):
        self.widget = None

    def initPanel(self, widget):
        self.widget = widget
        self.reset()
        self.queryAllData()
        self.initAll()

    def initAll(self):
        self.initAllData()
        self.initAllUI()
        self.refreshBF()

    def queryAllData(self):
        BigWorld.player().cell.pubgQueryStatistics()

    def initAllData(self):
        self.allBasicData = self.getPUBGInfo()

    def getPUBGInfo(self):
        p = BigWorld.player()
        pubgModeData = BFMD.data.get(const.BATTLE_FIELD_MODE_PUBG, {})
        obj = dict()
        if not pubgModeData:
            return obj
        obj['idx'] = pubgModeData.get('mode', const.BATTLE_FIELD_MODE_PUBG)
        obj['id'] = const.BATTLE_FIELD_MODE_PUBG
        obj['name'] = pubgModeData.get('name', '')
        obj['isOpenDouble'] = pubgModeData.get('isOpenDouble', False)
        obj['bg'] = 'pvpPanel/%s.dds' % pubgModeData.get('bg', 'default')
        obj['applyBtnNeedShow'] = self.isPUBGApplyBtnNeedShow()
        obj['teamApplyBtnNeedShow'] = self.isPUBGApplyBtnNeedShow()
        obj['icon'] = pubgModeData.get('icon', 0)
        fameData = FD.data[const.PUBG_MONEY_FAME_ID]
        obj['pubgFameNameTxt'] = fameData.get('name', '')
        obj['pubgFameNumLimitTxt'] = '%s' % fameData.get('weekGainLimit', '0')
        obj['pubgAllFameNumTxt'] = str(p.fame.get(const.PUBG_MONEY_FAME_ID, 0))
        obj['rankNameTxt'] = p.getCurRankNameInPUBG()
        obj['rankPointTxt'] = gameStrings.PUBG_PVP_MAIN_PROXY_RANK_POINT_TXT % p.pubgRankPoints
        obj['gameSeasonTxt'] = DCD.data.get('pubgGameSeasonTxt', '')
        obj['gameSeasonTimeTxt'] = DCD.data.get('pubgGameSeasonTimeTxt', '')
        obj['desc'] = pubgModeData.get('desc', '')
        obj['numberDesc'] = pubgModeData.get('numberDesc', '')
        obj['timeDesc'] = pubgModeData.get('timeDesc', '')
        obj['timeShortDesc'] = pubgModeData.get('timeShortDesc', '')
        obj['priceDesc'] = pubgModeData.get('priceDesc', '')
        obj['openLvDesc'] = pubgModeData.get('openLvDesc', '%d~~%d')
        obj['winStandard'] = pubgModeData.get('winStandard', '')
        gameglobal.rds.ui.pvpBattleFieldV2.getBFOpenLvDesc(obj, pubgModeData)
        obj['radarLimit'] = list()
        obj['radarLimit'].append(list(DCD.data.get('pubgRadarKillCntLimit', defaultLimit)))
        obj['radarLimit'].append(list(DCD.data.get('pubgRadarAssistCntLimit', defaultLimit)))
        obj['radarLimit'].append(list(DCD.data.get('pubgRadarDamageLimit', defaultLimit2)))
        obj['radarLimit'].append(list(DCD.data.get('pubgRadarSurvivalLimit', defaultLimit2)))
        obj['radarLimit'].append(list(DCD.data.get('pubgRadarCollectLimit', defaultLimit)))
        return obj

    def isPUBGValid(self):
        p = BigWorld.player()
        if not p.isCanJoinPUBG():
            return False
        if not gameglobal.rds.configData.get('enablePVPPUBGProxy', False):
            return False
        pubgModeData = BFMD.data.get(const.BATTLE_FIELD_MODE_PUBG, {})
        if not pubgModeData:
            return False
        if not pubgModeData.get('isOpen', 0):
            return False
        return True

    def isPUBGApplyBtnNeedShow(self):
        if not gameglobal.rds.configData.get('enableDuelTimeCheck', True):
            return True
        pubgModeData = BFMD.data.get(const.BATTLE_FIELD_MODE_PUBG, {})
        openStartTimes = pubgModeData.get('todayActivityStartTime', ())
        openEndTimes = pubgModeData.get('todayActivityEndTime', ())
        needShow = False
        current = utils.getNow()
        if len(openStartTimes) == 0:
            needShow = True
        else:
            for index in xrange(len(openStartTimes)):
                if not openStartTimes[index]:
                    continue
                if utils.inTimeTupleRange(openStartTimes[index][0], openEndTimes[index][0], current):
                    needShow = True
                    break

        return needShow

    def isPUBGTeamApplyBtnNeedShow(self):
        if not gameglobal.rds.configData.get('enableDuelTimeCheck', True):
            return True
        pubgModeData = BFMD.data.get(const.BATTLE_FIELD_MODE_PUBG, {})
        needShow = False
        teamOpenStartTimes = pubgModeData.get('teamOpenStartTimes', ())
        teamOpenEndTimes = pubgModeData.get('teamOpenEndTimes', ())
        current = utils.getNow()
        if len(teamOpenStartTimes) == 0:
            needShow = True
        else:
            for index in xrange(len(teamOpenStartTimes)):
                if utils.inTimeTupleRange(teamOpenStartTimes[index], teamOpenEndTimes[index], current):
                    needShow = True
                    break

        return needShow

    def initAllUI(self):
        if not self.allBasicData:
            gameglobal.rds.ui.pvPPanel.show(uiConst.PVP_BG_V2_TAB_TODAY_BATTLE_FIELD)
            return
        if not self.widget:
            return
        self.initUI()
        self.initDesc()
        self.initPubgBattleRadar()

    def initUI(self):
        p = BigWorld.player()
        self.widget.gradingTxt.text = self.allBasicData['rankNameTxt']
        self.widget.rankPointTxt.text = self.allBasicData['rankPointTxt']
        self.widget.gameSeasonTxt.text = self.allBasicData['gameSeasonTxt']
        self.widget.gameSeasonTimeTxt.text = self.allBasicData['gameSeasonTimeTxt']
        participateCount = p.playerAllBattleData.get(pubgUtils.PUBG_STATISTICS_PARTICIPATE_CNT_SEASON, 0)
        self.widget.gameSeasonAllRoundsTxt.text = str(participateCount)
        self.widget.gameSeasonSuccessfulRoundsTxt.text = str(p.playerAllBattleData.get(pubgUtils.PUBG_STATISTICS_TOP_RANK_SEASON, 0))
        self.widget.gameSeasonKillNumsTxt.text = str(p.playerAllBattleData.get(pubgUtils.PUBG_STATISTICS_KILL_CNT_SEASON, 0))
        self.widget.gameSeasonRankTxt.text = str(int(round(p.playerAllBattleData.get(pubgUtils.PUBG_STATISTICS_TOTAL_RANK_FOR_AVERAGE_SEASON, 99) / participateCount)) if participateCount > 1 else int(p.playerAllBattleData.get(pubgUtils.PUBG_STATISTICS_TOTAL_RANK_FOR_AVERAGE_SEASON, 99)))
        self.widget.curWeekAllRoundsTxt.text = str(p.playerAllBattleData.get(pubgUtils.PUBG_STATISTICS_PARTICIPATE_CNT_WEEKLY, 0))
        self.widget.curWeekSuccessfulRoundsTxt.text = str(p.playerAllBattleData.get(pubgUtils.PUBG_STATISTICS_TOP_RANK_WEEKLY, 0))
        self.widget.curWeekKillNumsTxt.text = str(p.playerAllBattleData.get(pubgUtils.PUBG_STATISTICS_KILL_CNT_WEEKLY, 0))
        self.widget.curWeekRankTxt.text = str(p.playerAllBattleData.get(pubgUtils.PUBG_EXTRA_MAX_RANK_WEEKLY, 99))
        self.widget.curWeekCoinTxt.text = gameStrings.PUBG_PVP_MAIN_PROXY_FAME_TXT % self.allBasicData['pubgFameNameTxt']
        self.widget.curWeekCoinNums.text = '%s/%s' % (str(p.playerAllBattleData.get(pubgUtils.PUBG_STATISTICS_FAME_WEEKLY, 0)), self.allBasicData['pubgFameNumLimitTxt'])
        self.widget.allCoinTxt.text = gameStrings.PUBG_PVP_MAIN_PROXY_ALL_FAME_TXT % self.allBasicData['pubgFameNameTxt']
        self.widget.allCoinNums.text = self.allBasicData['pubgAllFameNumTxt']
        self.widget.gameplayBtn.addEventListener(events.MOUSE_CLICK, self.handleClickFuncBtn, False, 0, True)
        self.widget.gradingBtn.addEventListener(events.MOUSE_CLICK, self.handleClickFuncBtn, False, 0, True)
        self.widget.gradingRankBtn.addEventListener(events.MOUSE_CLICK, self.handleClickFuncBtn, False, 0, True)
        self.widget.rewardBtn.addEventListener(events.MOUSE_CLICK, self.handleClickFuncBtn, False, 0, True)
        self.widget.storeBtn.addEventListener(events.MOUSE_CLICK, self.handleClickFuncBtn, False, 0, True)
        self.widget.battleFieldAllData.addEventListener(events.MOUSE_CLICK, self.handleClickFuncBtn, False, 0, True)
        self.widget.applyOfPersonBtn.addEventListener(events.MOUSE_CLICK, self.handleClickApplyBtn, False, 0, True)
        self.widget.applyOfTeamBtn.addEventListener(events.MOUSE_CLICK, self.handleClickApplyBtn, False, 0, True)

    def initDesc(self):
        textMc = self.widget.descPanel.canvas.text
        textMc.htmlText = ''
        if self.allBasicData['desc']:
            textMc.htmlText += self.allBasicData['desc'] + '\n\n'
        if self.allBasicData['timeDesc']:
            textMc.htmlText += self.allBasicData['timeDesc'] + '\n\n'
        if self.allBasicData['winStandard']:
            textMc.htmlText += self.allBasicData['winStandard'] + '\n\n'
        if self.allBasicData['priceDesc']:
            textMc.htmlText += self.allBasicData['priceDesc']
        textMc.height = textMc.textHeight + 20
        self.widget.descPanel.validateNow()
        self.widget.descPanel.refreshHeight()

    def initPubgBattleRadar(self):
        p = BigWorld.player()
        radarInnerMc = self.widget.socialRadar.inner
        limit = self.allBasicData['radarLimit']
        data = [p.playerAllBattleData.get(pubgUtils.PUBG_STATISTICS_KILL_CNT_SEASON, 0),
         p.playerAllBattleData.get(pubgUtils.PUBG_STATISTICS_ASSIST_CNT_SEASON, 0),
         p.playerAllBattleData.get(pubgUtils.PUBG_STATISTICS_DAMAGE_SEASON, 0),
         p.playerAllBattleData.get(pubgUtils.PUBG_STATISTICS_DURING_TIME_SEASON, 0),
         p.playerAllBattleData.get(pubgUtils.PUBG_STATISTICS_ACTIVE_SCORE_SEASON, 0)]
        participateCount = p.playerAllBattleData.get(pubgUtils.PUBG_STATISTICS_PARTICIPATE_CNT_SEASON, 0)
        if participateCount > 1:
            for idx, tempData in enumerate(data):
                data[idx] = int(round(tempData / participateCount))

        centerPointX = radarInnerMc.width / 2 + 0.5
        centerPointY = radarInnerMc.height / 2 + 4
        angle = 360 / len(data)
        for i in xrange(len(data) + 1):
            raderDesc = self.widget.getChildByName('desc%d' % i)
            radertext = self.widget.getChildByName('radar%d' % i)
            if raderDesc and radertext:
                raderDesc.text = gameStrings.PUBG_RADER_DESCS[i]
                radertext.text = data[i]
            if i == 0:
                radarInnerMc.graphics.clear()
                radarInnerMc.graphics.moveTo(centerPointX, centerPointY - self.getRadius(limit[0], data[0], radius))
                radarInnerMc.graphics.beginFill(26316, 0.6)
            elif i == len(data):
                radarInnerMc.graphics.lineTo(centerPointX, centerPointY - self.getRadius(limit[0], data[0], radius))
                radarInnerMc.graphics.endFill()
            else:
                pointX, pointY = self.getVertex(centerPointX, centerPointY, 90 - angle * i, self.getRadius(limit[i], data[i], radius))
                radarInnerMc.graphics.lineTo(pointX, pointY)

    def getRadius(self, limit, data, radius):
        for i in xrange(1, len(limit)):
            if limit[i - 1] <= data < limit[i]:
                return radius[i - 1]

        return radius[len(radius) - 1]

    def getVertex(self, centerPointX, centerPointY, angle, radius):
        dx = radius * math.cos(math.pi * angle / 180)
        dy = radius * math.sin(math.pi * angle / 180)
        return (centerPointX + dx, centerPointY - dy)

    def handleClickFuncBtn(self, *args):
        p = BigWorld.player()
        btnMc = ASObject(args[3][0]).currentTarget
        if btnMc.name == 'storeBtn':
            uiUtils.closeCompositeShop()
            shopId = DCD.data.get('pubgCompositeShopId', 0)
            shopId and p.base.openPrivateShop(0, shopId)
        elif btnMc.name == 'gameplayBtn':
            gameglobal.rds.ui.baoDian.show(introType=uiConst.BAODIAN_TYPE_PUBG)
        elif btnMc.name == 'gradingBtn':
            gameglobal.rds.ui.pubgRankingShow.show()
        elif btnMc.name == 'gradingRankBtn':
            gameglobal.rds.ui.rankCommon.showRankCommon(gametypes.TOP_TYPE_PUBG_GRADING_RANK)
        elif btnMc.name == 'rewardBtn':
            gameglobal.rds.ui.generalReward.show(gametypes.GENERAL_REWARD_PUBG)
        elif btnMc.name == 'battleFieldAllData':
            p = BigWorld.player()
            gameglobal.rds.ui.battleFieldHistory.isNeedShow = True
            p.cell.queryBattleFieldHistoryDataCell(p.bfHistoryVers[0], p.bfHistoryVers[1], p.bfHistoryVers[2], p.bfHistoryVers[3], p.bfHistoryVers[4], p.bfHistoryVers[5], [], const.BATTLE_FIELD_HISTORY_SHENGYA)
            if p.bfHistoryInfo.get('battleFieldFortHistory', {}):
                gameglobal.rds.ui.battleFieldHistory.show()

    def handleClickApplyBtn(self, *args):
        p = BigWorld.player()
        btnMc = ASObject(args[3][0]).currentTarget
        pubgModeId = const.BATTLE_FIELD_MODE_PUBG
        if btnMc.name == 'applyOfPersonBtn':
            if self.bfStage == uiConst.BF_PANEL_STAGE_INIT:
                if not gameglobal.rds.ui.pvpBattleFieldV2.personCheck(pubgModeId):
                    return
                p.cell.applyBattleField(self.getBattleFieldFbNo(pubgModeId), False, False)
            self.refreshBF()
        elif btnMc.name == 'applyOfTeamBtn':
            if self.bfStage == uiConst.BF_PANEL_STAGE_INIT:
                if not gameglobal.rds.ui.pvpBattleFieldV2.teamCheck(pubgModeId):
                    return
                p.cell.applyBattleFieldOfTeam(self.getBattleFieldFbNo(pubgModeId), gametypes.BATTLE_FIELD_APPLY_GROUP_OF_TEAM, False, False)
            elif self.bfStage == uiConst.BF_PANEL_STAGE_APPLYED:
                p.cancelApplyBattleField()
            elif self.bfStage == uiConst.BF_PANEL_STAGE_IN_GAME:
                p.cell.quitBattleField()

    def getBattleFieldFbNo(self, bfIdx):
        p = BigWorld.player()
        if p.battleFieldFbNo != 0:
            return p.battleFieldFbNo
        else:
            enableCrossServerBF = gameglobal.rds.configData.get('enableCrossServerBF', False)
            fbNo = formula.genBattleFieldFbNoByLv(p.lv, bfIdx, False, False)
            if enableCrossServerBF and utils.getBattleFieldRegionInfo(fbNo, False, utils.getHostId()) != (0, 0, 0):
                fbNo = formula.genBattleFieldFbNoByLv(p.lv, bfIdx, True, False)
            if fbNo:
                return fbNo
            gamelog.info('@zmk getPUBGBattleFieldFbNo - Error:', p.id)
            return 0

    def refreshBF(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.bfStage = getattr(p, 'battleFieldStage', uiConst.BF_PANEL_STAGE_INIT)
        self.initAllData()
        self.refreshUIInStage()

    def refreshUIInStage(self):
        self.widget.doubleBtn.visible = False
        self.widget.applyOfPersonBtn.visible = self.allBasicData['applyBtnNeedShow']
        self.widget.applyOfTeamBtn.visible = self.allBasicData['teamApplyBtnNeedShow']
        if self.bfStage == uiConst.BF_PANEL_STAGE_INIT:
            if not self.allBasicData['teamApplyBtnNeedShow']:
                self.widget.applyOfPersonBtn.x = self.widget.applyOfTeamBtn.x
            else:
                self.widget.applyOfPersonBtn.x = INIT_APPLY_PERSON_BTN_X
            self.widget.applyOfPersonBtn.label = gameStrings.PVP_APPLY_OF_PERSON
            self.widget.applyOfTeamBtn.label = gameStrings.PVP_APPLY_OF_TEAM
        elif self.bfStage == uiConst.BF_PANEL_STAGE_APPLYED:
            self.widget.applyOfPersonBtn.visible = False
            self.widget.applyOfTeamBtn.visible = True
            self.widget.applyOfTeamBtn.label = gameStrings.PVP_QUIT_QUEUE
        elif self.bfStage == uiConst.BF_PANEL_STAGE_MATCHED:
            self.widget.applyOfPersonBtn.visible = False
            self.widget.applyOfTeamBtn.visible = False
        elif self.bfStage == uiConst.BF_PANEL_STAGE_IN_GAME:
            self.widget.applyOfPersonBtn.visible = False
            self.widget.applyOfTeamBtn.visible = False
