#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/zmjBigBossPanelProxy.o
import BigWorld
import const
import zmjCommon
import events
import formula
import utils
import ui
import uiUtils
import clientUtils
import gametypes
import uiConst
from asObject import ASObject
from asObject import TipManager
from asObject import ASUtils
from helpers import cgPlayer
from guis import rankCommonUtils
from gamestrings import gameStrings
import gameglobal
from uiProxy import UIProxy
from data import rank_common_data as RCD
from data import fame_data as FD
from data import zmj_fuben_config_data as ZFCD
from cdata import game_msg_def_data as GMDD
REWARD_PROGRESS_VALUE = [0,
 20,
 45,
 75,
 100,
 100,
 100]

class ZmjBigBossPanelProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ZmjBigBossPanelProxy, self).__init__(uiAdapter)
        self.widget = None
        self.showRewardEffect = True
        self.cacheRank = ()
        self.reset()
        self.addEvent(events.EVENT_FAME_UPDATE, self.handleFameUpdate)

    def clearData(self):
        self.cacheRank = ()

    def reset(self):
        self.cgPlayer = None

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def unRegisterPanel(self):
        self.widget = None
        self.onMovieEnd()
        self.reset()

    def initUI(self):
        if self.showRewardEffect:
            self.widget.mainMc.rewardEffect.visible = True
            self.showRewardEffect = False
        else:
            self.widget.mainMc.rewardEffect.visible = False
        self.widget.zhanmoFameIcon.bonusType = 'zhanmo'
        self.widget.mainMc.zhanmoIcon.bonusType = 'zhanmo'
        self.widget.mainMc.topRankBtn.addEventListener(events.BUTTON_CLICK, self.handleTopRankBtnClick, False, 0, True)
        self.widget.mainMc.allServerTopRankBtn.addEventListener(events.BUTTON_CLICK, self.handleAllServerTopRankBtnClick, False, 0, True)
        self.widget.mainMc.previewRewardBtn.addEventListener(events.BUTTON_CLICK, self.handlePreviewRewardBtnClick, False, 0, True)
        self.widget.mainMc.getRewardBtn.addEventListener(events.BUTTON_CLICK, self.handleGetRewardBtnClick, False, 0, True)
        self.widget.mainMc.entryBtn.addEventListener(events.BUTTON_CLICK, self.handleEntryBtnClick, False, 0, True)
        self.widget.chargeBtn.addEventListener(events.BUTTON_CLICK, self.handleChargeBtnClick, False, 0, True)
        self.refreshRankTxt()
        zhanmoFameData = FD.data.get(const.ZMJ_ZHANMO_FAME_ID, {})
        zhanmoAutoIncLimit = zhanmoFameData.get('autoIncLimit', 200)
        autoIncIntervalMinute = zhanmoFameData.get('autoIncIntervalMinute', 1)
        incVal = zhanmoFameData.get('incVal', 1)
        zhanmoFameTips = ''
        if autoIncIntervalMinute == 1:
            zhanmoFameTips = gameStrings.ZMJ_FAME_INC_TXT % (incVal,)
        else:
            zhanmoFameTips = gameStrings.ZMJ_FAME_INC_TXT_1 % (autoIncIntervalMinute, incVal)
        self.widget.zhanmoFameProgress.maxValue = zhanmoAutoIncLimit
        TipManager.addTip(self.widget.zhanmoFameProgress, zhanmoFameTips)
        self.playMovie('zmjbigboss')

    def refreshInfo(self):
        if not self.hasBaseData():
            return
        else:
            p = BigWorld.player()
            zhanmoAutoIncLimit = FD.data.get(const.ZMJ_ZHANMO_FAME_ID, {}).get('autoIncLimit', 200)
            curZhanmo = p.fame.get(const.ZMJ_ZHANMO_FAME_ID, 0)
            self.widget.zhanmoFameProgress.currentValue = curZhanmo
            totalTime = int(p.zmjData.get(const.ZMJ_FB_INFO_TOTAL_DAY_MAX_DMG_TIME, 0))
            todayTopDmg = p.zmjData.get(const.ZMJ_FB_INFO_DAY_MAX_DMG, 0)
            totalTopDmg = p.zmjData.get(const.ZMJ_FB_INFO_TOTAL_DAY_MAX_DMG, 0)
            totalDmg = p.zmjData.get(const.ZMJ_FB_INFO_TOTAL_DMG, 0)
            participateDays = len(p.zmjData.get(const.ZMJ_FB_INFO_PARTICIPATE_DAYS, ()))
            self.widget.mainMc.totalTimeTxt.text = totalTime
            dmg, tip = self.damageNumberStr(todayTopDmg)
            self.widget.mainMc.todayTopDmgTxt.text = dmg
            if tip:
                TipManager.addTip(self.widget.mainMc.todayTopDmgTxt, tip)
            dmg, tip = self.damageNumberStr(totalTopDmg)
            self.widget.mainMc.totalTopDmgTxt.text = dmg
            if tip:
                TipManager.addTip(self.widget.mainMc.totalTopDmgTxt, tip)
            self.widget.mainMc.totalDmgTxt.text = gameStrings.ZMJ_PARTICIPATE_DAYS_SIMPLIFY_TXT % participateDays
            rewardList = p.zmjData.get(const.ZMJ_FB_INFO_TAKE_AWAY_AWARD_IDS, ())
            highFbParticipateDaysRewards = ZFCD.data.get('highFbParticipateDaysRewards', {})
            progressNum = 0
            for i in xrange(len(highFbParticipateDaysRewards)):
                awardId = i + 1
                itemMc = getattr(self.widget.mainMc, 'itemMc' + str(i), None)
                days, bonusId = highFbParticipateDaysRewards.get(awardId, (0, 0))
                itemIds = clientUtils.genItemBonus(bonusId)
                itemId = 0
                if itemIds:
                    itemId, itemNum = itemIds[0]
                itemMc.dmgTxt.text = gameStrings.ZMJ_PARTICIPATE_DAYS_TOTAL_TXT % days
                itemInfo = uiUtils.getGfxItemById(itemId)
                itemMc.slot.dragable = False
                itemMc.slot.setItemSlotData(itemInfo)
                if awardId in rewardList:
                    itemMc.effect.visible = False
                    itemMc.completed.visible = True
                elif participateDays >= days:
                    itemMc.effect.visible = True
                    itemMc.completed.visible = False
                else:
                    itemMc.effect.visible = False
                    itemMc.completed.visible = False
                if participateDays >= days:
                    progressNum += 1

            lastDay, bonusId = highFbParticipateDaysRewards.get(progressNum, (0, 0))
            currDay, bonusId = highFbParticipateDaysRewards.get(progressNum + 1, (0, 0))
            curPhasePercent = max((participateDays - lastDay) * 1.0 / (currDay - lastDay), 0)
            curPhaseValue = REWARD_PROGRESS_VALUE[progressNum + 1] - REWARD_PROGRESS_VALUE[progressNum]
            self.widget.mainMc.dmgProgress.currentValue = REWARD_PROGRESS_VALUE[progressNum] + curPhaseValue * curPhasePercent
            highFubenCost = ZFCD.data.get('highFubenCost', 0)
            self.widget.mainMc.zhanmoTxt.text = highFubenCost
            self.widget.mainMc.getRewardBtn.enabled = self.canGetReward()
            self.requestCommonRankData()
            return

    def hasBaseData(self):
        if not self.widget:
            return False
        return True

    def handleGetRewardBtnClick(self, *arg):
        p = BigWorld.player()
        rewardList = p.zmjData.get(const.ZMJ_FB_INFO_TAKE_AWAY_AWARD_IDS, ())
        highFbParticipateDaysRewards = ZFCD.data.get('highFbParticipateDaysRewards', {})
        participateDays = len(p.zmjData.get(const.ZMJ_FB_INFO_PARTICIPATE_DAYS, ()))
        awardIds = []
        for i in xrange(len(highFbParticipateDaysRewards)):
            awardId = i + 1
            days, bonusId = highFbParticipateDaysRewards.get(awardId, (0, 0))
            if awardId not in rewardList and participateDays >= days:
                awardIds.append(awardId)

        if awardIds:
            p.cell.applyZMJParticipateDaysAward(awardIds)

    def handleEntryBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        p = BigWorld.player()
        highFubenCost = ZFCD.data.get('highFubenCost', 0)
        curZhanmo = p.fame.get(const.ZMJ_ZHANMO_FAME_ID, 0)
        if curZhanmo < highFubenCost:
            p.showGameMsg(GMDD.data.ZMJ_LACK_ZHANMO_FAME_MSG, ())
            return
        if not zmjCommon.checkInZMJFbPermitTime():
            p.showGameMsg(GMDD.data.ZMJ_OPENING_TIME_LIMIT, ())
            return
        p.cell.applyZMJHighFuben()

    def handleFameUpdate(self, e):
        if e.data in (const.ZMJ_ZHANMO_FAME_ID, const.ZMJ_TAOFA_FAME_ID, const.ZMJ_GONGXIAN_FAME_ID):
            self.refreshInfo()

    def handlePreviewRewardBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        self.uiAdapter.zmjRewardPreview.show()

    def handleTopRankBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        self.uiAdapter.rankCommon.showRankCommon(gametypes.TOP_TYPE_ZMJ_FUBEN)

    def handleAllServerTopRankBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        self.uiAdapter.rankCommon.showRankCommon(gametypes.TOP_TYPE_ZMJ_FUBEN_GLOBAL)

    def canGetReward(self):
        p = BigWorld.player()
        rewardList = p.zmjData.get(const.ZMJ_FB_INFO_TAKE_AWAY_AWARD_IDS, ())
        highFbParticipateDaysRewards = ZFCD.data.get('highFbParticipateDaysRewards', {})
        participateDays = len(p.zmjData.get(const.ZMJ_FB_INFO_PARTICIPATE_DAYS, ()))
        awardIds = []
        for i in xrange(len(highFbParticipateDaysRewards)):
            awardId = i + 1
            days, bonusId = highFbParticipateDaysRewards.get(awardId, (0, 0))
            if awardId not in rewardList and participateDays >= days:
                awardIds.append(awardId)

        if awardIds:
            return True
        return False

    @ui.callInCD(2)
    def requestCommonRankData(self):
        p = BigWorld.player()
        p.cell.queryZMJRank()

    def onGetZmjRank(self, inTop, idx):
        self.cacheRank = (inTop, idx)
        self.refreshRankTxt()

    def refreshRankTxt(self):
        if not self.hasBaseData():
            return
        if not self.cacheRank:
            self.widget.mainMc.todayRankTxt.text = ''
            return
        inTop, idx = self.cacheRank
        if inTop:
            self.widget.mainMc.todayRankTxt.text = idx
        else:
            highFbTotalMaxDmgRewardsNotInTop = ZFCD.data.get('highFbTotalMaxDmgRewardsNotInTop', {})
            if idx < len(highFbTotalMaxDmgRewardsNotInTop):
                _, _, _, _, _, rankStr = highFbTotalMaxDmgRewardsNotInTop[idx]
                self.widget.mainMc.todayRankTxt.text = rankStr

    def damageNumberStr(self, num):
        if num > uiConst.ZMJ_DAMAGE_VALUE_THRESHOLD:
            return (gameStrings.ZMJ_DMG_SIMPLIFY_TXT % (num / uiConst.ZMJ_DAMAGE_VALUE_THRESHOLD,), num)
        return (num, '')

    def playMovie(self, movieName):
        w = 228
        h = 228
        config = {'position': (0, 0, 0),
         'w': w,
         'h': h,
         'loop': True,
         'screenRelative': False,
         'verticalAnchor': 'TOP',
         'horizontalAnchor': 'RIGHT',
         'callback': self.onMovieEnd}
        if not self.cgPlayer:
            self.cgPlayer = cgPlayer.UIMoviePlayer('gui/widgets/ZmjBigBossPanel' + self.uiAdapter.getUIExt(), 'ZmjBigBoss_Photo', w, h)
        self.cgPlayer.playMovie(movieName, config)

    def onMovieEnd(self):
        if self.cgPlayer:
            self.cgPlayer.endMovie()
            self.cgPlayer = None

    def handleChargeBtnClick(self, *arg):
        zhanmoFameMallId = ZFCD.data.get('zhanmoFameMallId', 0)
        self.uiAdapter.tianyuMall.mallBuyConfirm(zhanmoFameMallId, 1, 'zhanmo.0')
