#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impFishing.o
import random
import BigWorld
import gametypes
import gameglobal
import gamelog
import const
from helpers import fishing
from callbackHelper import Functor
from guis import uiConst
from guis import ui
from guis import uiUtils
from data import fish_data as FD
from data import item_data as ID
from cdata import game_msg_def_data as GMDD
from data import life_skill_config_data as LSCFD
FISH_RARITY_LV = 3

class ImpFishing(object):

    def startFish(self, dist = 6, autoFishing = False):
        dstPos = fishing.checkWater(dist)
        if self.fishingMgr is None:
            self.fishingMgr = fishing.FishingMgr(self)
        self.fishingMgr.autoFishing = autoFishing
        if not self.checkCanFish():
            return
        elif not dstPos:
            self.fashion.stopAction()
            self.cancelWeaponTimerAndHangUpWeapon()
            self.cell.readyFishing(const.ST_READY_FISHING)
            if autoFishing:
                self.fishingMgr.setAutoTimer()
            return
        else:
            self.ap.stopMove()
            gamelog.debug('startFish')
            self.cell.startFishing(dstPos, autoFishing)
            return

    def doStartFish(self):
        gamelog.debug('doStartFish', self.fishingStatus)
        if self.fishingMgr is None:
            self.fishingMgr = fishing.FishingMgr(self)
        self.fishingMgr.isCharging = False
        self.fishingMgr.throwFishRod(self.buoyPos)
        self.cancelWeaponTimerAndHangUpWeapon()
        if self == BigWorld.player():
            gameglobal.rds.ui.actionbar.setRideShine(True, uiConst.FISH_STARTING)
            gameglobal.rds.ui.skill.setRideShine(2, True)
        if self.fishingStatus == const.ST_AUTO_FISHING:
            self.topLogo.setAutoFishingVisible(True)

    def stopFish(self):
        if self == BigWorld.player() and (self.inFishing() or self.inFishingReady()):
            gameglobal.rds.ui.fishing.hide(1)
            if self.fishingMgr:
                self.fishingMgr.stopFish()
            self.fishingStatus = const.ST_NONE_FISHING
            self.cell.stopFishing(False)

    def doStopFish(self):
        if self == BigWorld.player():
            gameglobal.rds.ui.fishing.closeFishing()
            if gameglobal.rds.ui.fishing.restart:
                gameglobal.rds.ui.fishing.showFishing()
                gameglobal.rds.ui.fishing.restart = False
        if self.fishingMgr:
            self.fishingMgr.stopFish()
        self.topLogo.setAutoFishingVisible(False)

    def pullFish(self):
        gamelog.debug('impFishing@pullFish', self.inFishing(), self.fishingMgr.isCharging)
        if self.inFishing() and self.fishingMgr:
            if self.fishingMgr.isCharging:
                self.cell.startCharging()
            else:
                self.cell.pullFish()

    def checkFishEquip(self, bMsg = True):
        equipNeed = (gametypes.FISHING_EQUIP_ROD, gametypes.FISHING_EQUIP_BUOY, gametypes.FISHING_EQUIP_HOOK)
        errorMsg = (GMDD.data.FISHING_NO_ROD, GMDD.data.FISHING_NO_BUOY, GMDD.data.FISHING_NO_HOOK)
        for idx, part in enumerate(equipNeed):
            if self.fishingEquip.isEmpty(part):
                bMsg and self.showGameMsg(errorMsg[idx], ())
                return False
            equip = self.fishingEquip.get(part)
            if getattr(equip, 'initMaxDura', 0) > 0 and equip.cdura < LSCFD.data.get('toolDuraConsume', 5):
                bMsg and self.showGameMsg(GMDD.data.FISHING_EQUIP_DURA, (equip.name,))
                return False

        return True

    def checkCanFish(self, bMsg = True):
        if not self.inWorld:
            return False
        if self.inRealFishing():
            return False
        if not self.stateMachine.checkStatus(const.CT_FISHING):
            return False
        if self.fishingEquip.isEmpty(gametypes.FISHING_EQUIP_BAIT):
            bMsg and self.showGameMsg(GMDD.data.FISHING_NO_BAIT, ())
            return False
        if not self.checkFishEquip(bMsg):
            self.stopFish()
            return False
        bait = self.fishingEquip.get(gametypes.FISHING_EQUIP_BAIT)
        baitPg, baitPos = self.inv.findItemInPages(bait.id, includeExpired=True, includeLatch=True, includeShihun=True)
        if baitPg == const.CONT_NO_PAGE or baitPos == const.CONT_NO_POS:
            bMsg and self.showGameMsg(GMDD.data.FISHING_BAIT_USED_UP, ())
            self.stopFish()
            return False
        emptyPg, emptyPos = self.inv.searchEmptyInPages()
        if emptyPg == const.CONT_NO_PAGE or emptyPos == const.CONT_NO_POS:
            bMsg and self.showGameMsg(GMDD.data.FISHING_INV_FULL, ())
            self.stopFish()
            return False
        return True

    def onFishBite(self, fishId, delay, duration):
        if self.fishingMgr:
            rarity = FD.data.get(fishId, {}).get('rarity', 1)
            isCharging = True if rarity >= FISH_RARITY_LV else False
            if self.fishingStatus == const.ST_AUTO_FISHING:
                isCharging = False
            self.fishingMgr.isCharging = isCharging
            BigWorld.callback(delay, Functor(self.fishingMgr.shakeBuoy, duration, isCharging))
            if self == BigWorld.player():
                if isCharging:
                    gameglobal.rds.ui.fishing.fishId = fishId
                    gameglobal.rds.ui.fishing.upFishingRod(rarity)
                if self.fishingStatus == const.ST_AUTO_FISHING:
                    randTime = random.uniform(delay, delay + duration)
                    BigWorld.callback(randTime, self.pullFish)
                BigWorld.callback(delay, Functor(gameglobal.rds.ui.fishing.setFloatMove, uiConst.FLOAT_MOVE_FAST))

    def onFishGone(self, fishId):
        gameglobal.rds.ui.fishing.showResult(uiConst.FISHING_ESCAPE)

    def onFishMiss(self, fishId):
        gameglobal.rds.ui.fishing.showResult(uiConst.FISHING_DECOUPLE)

    def noFishBite(self):
        gameglobal.rds.ui.fishing.showResult(uiConst.FISHING_NOBITE)

    def restarFishing(self):
        self.fishingStatus = const.ST_READY_FISHING
        self.doPullFish(True)
        if self == BigWorld.player() and not gameglobal.rds.ui.fishing.isAuto:
            BigWorld.callback(1, gameglobal.rds.ui.fishing.restartFishing)

    def doPullFish(self, isRealPull = False):
        gamelog.debug('doPullFish')
        if self.fishingMgr:
            self.fishingMgr.pullFish(isRealPull)

    def inFishing(self):
        fishStatus = self.inRealFishing() or self.inFishingHold()
        if self == BigWorld.player():
            return fishStatus or gameglobal.rds.ui.fishing.isChargingForDist
        else:
            return fishStatus

    def inRealFishing(self):
        if self.fishingStatus in (const.ST_AUTO_FISHING, const.ST_MANUAL_FISHING):
            return True
        return False

    def inFishingReady(self):
        return self.fishingStatus == const.ST_READY_FISHING

    def inFishingHold(self):
        return self.fishingStatus == const.ST_HOLD_FISHING

    def onGenFishBonus(self, fishId, fishBonus, isAutoFishing):
        gameglobal.rds.ui.fishing.showResult(uiConst.FISHING_SUCCESS)
        if self == BigWorld.player():
            gameglobal.rds.sound.playSound(gameglobal.SD_413)
        if not isAutoFishing:
            for itemId, num in fishBonus:
                gameglobal.rds.ui.fishing.fishingResult[0] = itemId
                gameglobal.rds.ui.fishing.fishingResult[1] = num

            BigWorld.callback(1, gameglobal.rds.ui.fishing.showFishing)
            if gameglobal.rds.ui.fishing.restartHandler:
                BigWorld.cancelCallback(gameglobal.rds.ui.fishing.restartHandler)
                gameglobal.rds.ui.fishing.restartHandler = None
        if fishId not in self.fishHistory:
            self.fishHistory.append(fishId)

    def autoFishAgain(self):
        self.readyFish(const.ST_HOLD_FISHING, bMsg=False)
        gameglobal.rds.ui.fishing.hide()
        if self.checkCanFish():
            gameglobal.rds.ui.fishing.showFishing()

    @ui.callFilter(0.5)
    def readyFish(self, step = const.ST_READY_FISHING, bMsg = True):
        if not self.checkCanFish(bMsg=bMsg):
            return
        else:
            if self.fishingMgr is None:
                self.fishingMgr = fishing.FishingMgr(self)
            self.ap.stopMove()
            self.cell.readyFishing(step)
            return

    def doReadyFish(self, step = const.ST_READY_FISHING):
        gamelog.debug('doReadyFish', step, self.fishingStatus)
        if self.fishingMgr is None:
            self.fishingMgr = fishing.FishingMgr(self)
        self.cancelWeaponTimerAndHangUpWeapon()
        self.fishingMgr.start(step)
        if self == BigWorld.player() and (step == const.ST_READY_FISHING and not gameglobal.rds.ui.fishing.isAuto or step == const.ST_HOLD_FISHING and gameglobal.rds.ui.fishing.isAuto):
            gameglobal.rds.ui.fishing.readyFish(step)

    def onFishingInFishGroup(self, fishGroupId):
        BigWorld.callback(0.5, Functor(gameglobal.rds.ui.showFishLabel, 0, uiConst.FISHING_IN_POINT))

    def updateFishingScore(self, questId, fishId, scoreData):
        gamelog.debug('zt: updateFishingScore', questId, fishId, scoreData)
        fishingScore = int(scoreData.get('score', 0))
        ret = {}
        ret['score'] = fishingScore
        ret['icon'] = []
        for i, fish in enumerate(gameglobal.rds.ui.fishingGame.gameFishes):
            if i == len(gameglobal.rds.ui.fishingGame.gameFishes) - 2:
                continue
            if i != len(gameglobal.rds.ui.fishingGame.gameFishes) - 1:
                fishNum = scoreData.get(fish, 0)
            else:
                fishNum = scoreData.get(fish, 0) + scoreData.get(gameglobal.rds.ui.fishingGame.gameFishes[i - 1], 0)
            iconId = ID.data.get(fish, {}).get('icon', fish)
            ret['icon'].append(['item/icon/%d.dds' % iconId, fishNum])

        gameglobal.rds.ui.fishingGame.myVal = ret
        if gameglobal.rds.ui.fishingGame.noticeMediator:
            gameglobal.rds.ui.fishingGame.noticeMediator.Invoke('setMyRankInfo', uiUtils.dict2GfxDict(ret))
