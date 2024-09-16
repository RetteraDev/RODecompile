#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/shengSiChangProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import gamelog
import const
import gametypes
from uiProxy import DataProxy
from ui import gbk2unicode
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from data import sheng_si_chang_data as SSCD
from gamestrings import gameStrings

class ShengSiChangProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(ShengSiChangProxy, self).__init__(uiAdapter)
        self.modelMap = {'getTipsInfo': self.onGetTipsInfo,
         'okClick': self.onOkClick,
         'cancelClick': self.onCancelClick,
         'miniClick': self.onMiniClick,
         'getStatsInfo': self.onGetStatsInfo,
         'confirmTimeOut': self.onConfirmTimeOut,
         'startSSC': self.onStartSSC}
        self.bindType = 'shengSiChang'
        self.sscTipMed = None
        self.sscStatsMed = None
        self.uiAdapter = uiAdapter
        self.reset()

    def reset(self):
        self.tipsTimeStamp = 0
        self.stage = uiConst.SSC_TIPS_STAGE_START
        self.statsStage = uiConst.SSC_STATS_IN_SSC
        self.isClickDone = False
        self.createDelayId = None
        if self.uiAdapter:
            self.uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_SHENG_SI_CHANG_START, {'click': self.clickPushIcon})

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.sscTipMed = None
        self.sscStatsMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SHENG_SI_CHANG_TIPS)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SHENG_SI_CHANG_STATS)

    def _asWidgetClose(self, widgetId, multiID):
        pass

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SHENG_SI_CHANG_TIPS:
            self.sscTipMed = mediator
        elif widgetId == uiConst.WIDGET_SHENG_SI_CHANG_STATS:
            self.sscStatsMed = mediator

    def showTips(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SHENG_SI_CHANG_TIPS, False)

    def closeTips(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SHENG_SI_CHANG_TIPS)
        self.sscTipMed = None
        self.isClickDone = False
        self.stage = uiConst.SSC_TIPS_STAGE_START
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_SHENG_SI_CHANG_START)

    def setDesc(self, msg):
        if self.sscTipMed:
            self.sscTipMed.Invoke('setDesc', GfxValue(gbk2unicode(msg)))

    def showConfirmTip(self, stage):
        self.stage = stage
        self.refreshSSCTip()

    def onGetTipsInfo(self, *arg):
        p = BigWorld.player()
        sscData = SSCD.data.get(p.getShengSiChangFbNo(), {})
        if self.stage in (uiConst.SSC_TIPS_STAGE_END, uiConst.SSC_TIPS_STAGE_FINAL_END):
            timeInterval = sscData.get('quitTime', 45)
        else:
            timeInterval = const.DUEL_PREPARE_DELAY
        ret = self.movie.CreateObject()
        ret.SetMember('stage', GfxValue(self.stage))
        ret.SetMember('timerMaxValue', GfxValue(timeInterval))
        ret.SetMember('timerCurValue', GfxValue(int(timeInterval - (p.getServerTime() - self.tipsTimeStamp)) - 1))
        return ret

    def refreshSSCTip(self):
        if self.sscTipMed:
            self.sscTipMed.Invoke('refreshPanel')
        else:
            self.showTips()

    def clickPushIcon(self):
        self.refreshSSCTip()

    def onOkClick(self, *arg):
        p = BigWorld.player()
        if self.stage == uiConst.SSC_TIPS_STAGE_START:
            self.isClickDone = True
            p.cell.confirmEnterShengSiChang(p.getShengSiChangFbNo())
        elif self.stage in (uiConst.SSC_TIPS_STAGE_END, uiConst.SSC_TIPS_STAGE_FINAL_END):
            p.cell.leaveShengSiChang()

    def onCancelClick(self, *arg):
        if self.stage == uiConst.SSC_TIPS_STAGE_START:
            self.isClickDone = True
            p = BigWorld.player()
            p.cell.cancelEnterShengSiChang(p.getShengSiChangFbNo())
        self.closeTips()

    def onConfirmTimeOut(self, *arg):
        p = BigWorld.player()
        if not self.isClickDone and self.stage == uiConst.SSC_TIPS_STAGE_START:
            self.onOkClick()
        elif not self.isClickDone and self.stage == uiConst.SSC_TIPS_STAGE_WAITING:
            p.showGameMsg(GMDD.data.SHENG_SI_CHANG_CONFIRM_TIME_OUT, ())
        elif self.isClickDone and self.stage == uiConst.SSC_TIPS_STAGE_WAITING:
            self.createSSCDelayNotify()
        self.closeTips()

    def createSSCDelayNotify(self):
        msg = GMD.data.get(GMDD.data.SSC_DELAY_NOTIFY, {}).get('text', gameStrings.TEXT_SHENGSICHANGPROXY_137)
        self.createDelayId = gameglobal.rds.ui.messageBox.showAlertBox(msg)

    def closeSSCDelayNotify(self):
        if self.createDelayId is None:
            return
        else:
            gameglobal.rds.ui.messageBox.dismiss(self.createDelayId)
            self.createDelayId = None
            return

    def onStartSSC(self, *arg):
        self.closeSSCStats()
        p = BigWorld.player()
        if p.shengSiChangStatus == gametypes.SHENG_SI_CHANG_STATUS_WIN_STANDBY:
            self.createSSCDelayNotify()

    def onMiniClick(self, *arg):
        p = BigWorld.player()
        if p.shengSiChangStatus == gametypes.SHENG_SI_CHANG_STATUS_TIMEOUT or self.stage == uiConst.SSC_TIPS_STAGE_WAITING:
            self.closeTips()
        else:
            self.sscTipMed = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SHENG_SI_CHANG_TIPS)

    def onGetRoundInfo(self):
        if self.sscStatsMed:
            self.sscStatsMed.Invoke('refreshPanel')

    def getNewRuleStatsInfo(self):
        p = BigWorld.player()
        ret = self.movie.CreateObject()
        state = p.shengSiChangStatus
        if state in [gametypes.SHENG_SI_CHANG_STATUS_IN_SSC, gametypes.SHENG_SI_CHANG_STATUS_START]:
            ret.SetMember('stage', GfxValue(uiConst.SSC_STATS_IN_SSC))
            ret.SetMember('aliveMenNum', GfxValue(p.sscStatsInfo.get('aliveMen', 0)))
            ret.SetMember('winNum', GfxValue(p.sscStatsInfo.get('winNum', 0)))
        elif state in [gametypes.SHENG_SI_CHANG_STATUS_WIN_STANDBY, gametypes.SHENG_SI_CHANG_STATUS_NEW_RULE_SPECIAL]:
            ret.SetMember('stage', GfxValue(uiConst.SSC_STATS_STANDBY))
            ret.SetMember('curTeamNum', GfxValue(p.roundCurNotFinishedCnt))
            standByTitle = gameStrings.SSC_STAND_BY_TITLE
            if getattr(p, 'sscStageLv', 0):
                currRankLv = getattr(p, 'sscRankLv', '1')
                standByTitle = gameStrings.SSC_STAND_BY_LV_TITLE % (currRankLv, p.sscStageLv)
            ret.SetMember('standbyTitle', GfxValue(gbk2unicode(standByTitle)))
        elif state in [gametypes.SHENG_SI_CHANG_STATUS_CONFIRMING, gametypes.SHENG_SI_CHANG_STATUS_CONFIRMED]:
            ret.SetMember('stage', GfxValue(uiConst.SSC_STATS_START_COUNTING))
            ret.SetMember('count', GfxValue(const.DUEL_PREPARE_DELAY - int(p.getServerTime() - self.sscTimeStamp)))
        return ret

    def onGetStatsInfo(self, *arg):
        ret = self.movie.CreateObject()
        p = BigWorld.player()
        ret.SetMember('stage', GfxValue(self.statsStage))
        if self.statsStage == uiConst.SSC_STATS_IN_SSC:
            ret.SetMember('aliveMenNum', GfxValue(p.sscStatsInfo.get('aliveMen', 0)))
            ret.SetMember('winNum', GfxValue(p.sscStatsInfo.get('winNum', 0)))
        elif self.statsStage == uiConst.SSC_STATS_STANDBY:
            if gameglobal.rds.configData.get('enableNewMatchRuleSSC', False) and self.isInCounting():
                ret.SetMember('stage', GfxValue(uiConst.SSC_STATS_START_COUNTING))
                ret.SetMember('count', GfxValue(const.DUEL_PREPARE_DELAY - int(p.getServerTime() - self.sscTimeStamp)))
            else:
                ret.SetMember('curTeamNum', GfxValue(p.roundCurNotFinishedCnt))
                standByTitle = gameStrings.SSC_STAND_BY_TITLE
                if getattr(p, 'sscStageLv', 0):
                    currRankLv = getattr(p, 'sscRankLv', '1')
                    standByTitle = gameStrings.SSC_STAND_BY_LV_TITLE % (currRankLv, p.sscStageLv)
                ret.SetMember('standbyTitle', GfxValue(gbk2unicode(standByTitle)))
        elif self.statsStage == uiConst.SSC_STATS_START_COUNTING:
            ret.SetMember('count', GfxValue(const.DUEL_PREPARE_DELAY - int(p.getServerTime() - self.sscTimeStamp)))
        return ret

    def isInCounting(self):
        if not getattr(self, 'sscTimeStamp', 0):
            return False
        p = BigWorld.player()
        return const.DUEL_PREPARE_DELAY - int(p.getServerTime() - self.sscTimeStamp) > 0

    def refreshSSCStats(self, statsStage, sscTimeStamp = None):
        gamelog.debug('@hjx ssc#refreshSSCStats:', self.sscStatsMed, statsStage, sscTimeStamp)
        self.statsStage = statsStage
        if sscTimeStamp:
            self.sscTimeStamp = sscTimeStamp
        if self.sscStatsMed:
            self.sscStatsMed.Invoke('refreshPanel')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SHENG_SI_CHANG_STATS, False)

    def closeSSCStats(self):
        self.sscStatsMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SHENG_SI_CHANG_STATS)
