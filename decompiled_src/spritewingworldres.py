#Embedded file name: /WORKSPACE/data/entities/common/spritewingworldres.o
import BigWorld
if BigWorld.component in ('base', 'cell'):
    import gameengine
import random
import math
import gamelog
import copy
import const
import utils
import time
import gametypes
import wingWorldUtils
from userSoleType import UserSoleType
from userDictType import UserDictType
from data import wing_world_resource_sprite_slot_data as WWRSSD
from data import wing_world_config_data as WWCD
from data import wing_world_resource_speed_data as WWRSD
from cdata import game_msg_def_data as GMDD
if BigWorld.component in ('base', 'cell'):
    import gameconfig
    from data import log_src_def_data as LSDD
    from data import wing_world_resource_sprite_random_event_reverse_data as WWRSRERD
    from data import wing_world_resource_sprite_random_special_reverse_data as WWRSRSRD
    from data import wing_world_resource_sprite_slot_unlock_type_reverse_data as WWRSSUTRD
    import serverlog
    import gameconst
    import riskControl
if BigWorld.component in ('base', 'cell'):
    slotUnlockProcMap = {}
    gLocals = locals()

    def registerSlotUnlockProc(unlockType):

        def _handleSLotUnlock(srcFunc):
            if slotUnlockProcMap.has_key(unlockType) and slotUnlockProcMap[unlockType] != srcFunc.__name__:
                raise ValueError('registerSlotUnlockProc duplicate key: ', unlockType)
            slotUnlockProcMap[unlockType] = srcFunc.__name__

            def func(self, owner, param, sendClient = True):
                slotIndexes = WWRSSUTRD.data.get(unlockType, [])
                return srcFunc(self, owner, param, slotIndexes, sendClient)

            return func

        return _handleSLotUnlock


    @registerSlotUnlockProc(const.WING_WORLD_SPRITE_COLLECT_RES_UNLOCK_TYPE_DEFAULT)
    def _slot_unlock_default_proc(self, owner, param, slotIndexes, sendClient):
        for slotIndex in slotIndexes:
            self.unlockedSlots.add(slotIndex)

        sendClient and owner.soulClient.onSpriteWingWorldResSlotUnlockChange(self.unlockedSlots)


    @registerSlotUnlockProc(const.WING_WORLD_SPRITE_COLLECT_RES_UNLOCK_TYPE_GUILD_LV)
    def _slot_unlock_guildLv_proc(self, owner, param, slotIndexes, sendClient):
        for slotIndex in slotIndexes:
            unlockArg = WWRSSD.data.get(slotIndex, {}).get('unlockArg', None)
            if unlockArg is not None and param >= unlockArg:
                self.unlockedSlots.add(slotIndex)
            else:
                self.unlockedSlots.discard(slotIndex)
                self.rmSprite(owner, slotIndex, sendClient)

        sendClient and owner.soulClient.onSpriteWingWorldResSlotUnlockChange(self.unlockedSlots)


class SpriteWingWorldResVal(UserSoleType):

    def __init__(self):
        self.spriteIndex = 0
        self.lastCalcTime = 0
        self.timerId = 0
        self.remainCalcCnt = 0


class SpriteWingWorldRes(UserSoleType):
    CALC_INTERVAL = 600
    SPRITE_COLLECT_RATE = 3600 / CALC_INTERVAL

    def __init__(self):
        self.spriteInSlots = {}
        self.resDictCurrent = {}
        self.fameCurrent = 0
        self.specialRareLv = 0
        self.specialCntDay = 0
        self.maxSpeed = 0
        self.resTotalDay = 0
        self.resetDailyTime = 0
        self.unlockedSlots = set()
        self.unlockArgs = {}
        self.maxSpeedTemp = 0

    if BigWorld.component in ('base', 'cell'):

        def transfer(self, owner):
            slots = {}
            for slotIndex, sVal in self.spriteInSlots.iteritems():
                slots[slotIndex] = sVal.spriteIndex

            owner.soulClient.onGetSpriteWingWorldRes(slots, self.resDictCurrent, self.unlockedSlots, self.specialRareLv, self.specialCntDay, self.maxSpeed, self.resTotalDay)

    def isValidSlot(self, slotIndex):
        return slotIndex in self.unlockedSlots

    def isEmptySlot(self, slotIndex):
        return self.isValidSlot(slotIndex) and slotIndex not in self.spriteInSlots

    def getStartEndSecs(self):
        shour, smin, ehour, emin = WWCD.data.get('spriteResCollectTimeRange', (12, 30, 18, 30))
        startSecs = shour * 3600 + smin * 60
        endSecs = ehour * 3600 + emin * 60
        return (startSecs, endSecs)

    def getSecs(self, timeStamp):
        stime = time.localtime(timeStamp)
        chour, cmin, csec = stime[const.LOCAL_TIME_INDEX_HOUR], stime[const.LOCAL_TIME_INDEX_MIN], stime[const.LOCAL_TIME_INDEX_SEC]
        secs = chour * 3600 + cmin * 60 + csec
        return secs

    def inValidTime(self, timeStamp = 0):
        timeStamp = timeStamp or utils.getNow()
        startSecs, endSecs = self.getStartEndSecs()
        timeSecs = self.getSecs(timeStamp)
        return startSecs < timeSecs < endSecs

    def getSecsToNextStartTime(self, cur = 0, currentSecs = 0, startSecs = 0):
        if not currentSecs and not startSecs:
            startSecs, endSecs = self.getStartEndSecs()
            currentSecs = self.getSecs(utils.getNow())
        if currentSecs <= startSecs:
            return startSecs - currentSecs
        else:
            return const.SECONDS_PER_DAY - (currentSecs - startSecs)

    def getRemainCalcTime(self):
        startSecs, endSecs = self.getStartEndSecs()
        currentSecs = self.getSecs(utils.getNow())
        if currentSecs < startSecs or currentSecs > endSecs:
            return max(0, endSecs - startSecs)
        else:
            return max(0, endSecs - currentSecs)

    def getRemainCalcCnt(self):
        return max(0, int(self.getRemainCalcTime() / self.CALC_INTERVAL))

    if BigWorld.component in ('base', 'cell'):
        slotUnlockProcMap = {}

        def processSlot(self, owner, unlockType, param, sendClient = True):
            if not owner.vipBase.isValidProp(gametypes.VIP_SERVICE_WING_WORLD_SPRITE_RES):
                self.clearSlot(owner, sendClient)
                return
            funcName = slotUnlockProcMap.get(unlockType)
            if not funcName:
                return
            func = gLocals.get(funcName)
            if not func:
                return
            func(self, owner, param, sendClient)

        def clearSlot(self, owner, sendClient = True):
            needClear = len(self.unlockedSlots) or len(self.spriteInSlots)
            self.unlockedSlots.clear()
            for slotIndex in self.spriteInSlots.keys():
                self.rmSprite(owner, slotIndex, sendClient=False)

            sendClient and needClear and self.transfer(owner)

        def processSlotOnVipChange(self, owner, isAdd):
            if isAdd:
                self.processSlot(owner, const.WING_WORLD_SPRITE_COLLECT_RES_UNLOCK_TYPE_DEFAULT, 0, sendClient=False)
                for unlockType, arg in self.unlockArgs.iteritems():
                    self.processSlot(owner, unlockType, arg, sendClient=False)

                owner.soulClient.onSpriteWingWorldResSlotUnlockChange(self.unlockedSlots)
            else:
                self.clearSlot(owner)

        def processRes(self, owner, sendClient = True):
            if not self.spriteInSlots:
                return
            current = utils.getNow()
            startSecs, endSecs = self.getStartEndSecs()
            currentSecs = self.getSecs(current)
            slotIndexes = self.spriteInSlots.keys()
            for slotIndex in slotIndexes:
                self.processSingleSpriteRes(owner, slotIndex, current, currentSecs, startSecs, endSecs, sendClient=False)

            sendClient and owner.soulClient.onSpriteWingWorldResSyncRes(self.resDictCurrent, self.resTotalDay)

        def resetDaily(self, owner, sendClient = True):
            current = utils.getNow()
            if not utils.isSameDay(current, self.resetDailyTime):
                self.specialCntDay = 0
                self.specialRareLv = 0
                self.resTotalDay = 0
                self.maxSpeed = 0
                self.resetDailyTime = current
            rmSlotIndexes = []
            for slotIndex, sVal in self.spriteInSlots.iteritems():
                if sVal.remainCalcCnt <= 0:
                    rmSlotIndexes.append(slotIndex)

            if rmSlotIndexes:
                for slotIndex in rmSlotIndexes:
                    self.rmSprite(owner, slotIndex, sendClient=False)

            sendClient and self.transfer(owner)

        def _calcCurrentMaxSpeed(self, owner):
            totalSpeed = 0
            for sVal in self.spriteInSlots.itervalues():
                speedDict = self._getSpeed(owner, sVal.spriteIndex)
                totalSpeed += sum(speedDict.itervalues())

            speedPerHour = totalSpeed * self.SPRITE_COLLECT_RATE
            return speedPerHour

        def calcMaxSpeedTemp(self, owner, sendClient = True):
            speedPerHour = self._calcCurrentMaxSpeed(owner)
            if speedPerHour > self.maxSpeedTemp:
                self.maxSpeedTemp = speedPerHour

        def calcMaxSpeed(self, owner, sendClient = True):
            speedPerHour = self._calcCurrentMaxSpeed(owner)
            if speedPerHour > self.maxSpeed:
                self.maxSpeed = speedPerHour
            if speedPerHour > self.maxSpeedTemp:
                self.maxSpeedTemp = speedPerHour
            sendClient and owner.soulClient.onSpriteWingWorldResSyncSpecialRareLvAndSpeed(self.specialRareLv, self.maxSpeed)

        def calcSpecial(self, owner, sendClient = True):
            self.calcMaxSpeed(owner, sendClient=False)
            threshold, cntLimit = WWCD.data.get('spriteResCollectSpecialArgs', (const.MAX_UINT32, 0))
            if self.resTotalDay >= threshold and self.specialCntDay < cntLimit:
                openLevel = wingWorldUtils.getSeasonOpenedLevel(wingWorldUtils.getCurSeasonStep(owner.getWingWorldGroupId()))
                spData = WWCD.data.get('spriteResCollectRareLv', {}).get(openLevel)
                if spData:
                    self.specialRareLv = utils.getValueByRangeKey(spData, self.maxSpeed, 0)
            sendClient and owner.soulClient.onSpriteWingWorldResSyncSpecialRareLvAndSpeed(self.specialRareLv, self.maxSpeed)

        def resetAfterSubmit(self, owner, sendClient = True):
            self.specialRareLv = 0
            sendClient and owner.soulClient.onSpriteWingWorldResSyncSpecialRareLvAndSpeed(self.specialRareLv, self.maxSpeed)

        def processSingleSpriteRes(self, owner, slotIndex, current = 0, currentSecs = 0, startSecs = 0, endSecs = 0, sendClient = True, fromCB = False):
            sVal = self.getSpriteVal(slotIndex)
            if sVal:
                if fromCB:
                    sVal.timeId = 0
                else:
                    self._cancelTimer(owner, sVal)
            if not sVal or not sVal.lastCalcTime or not owner.ownSprites.isValidIndex(sVal.spriteIndex) or sVal.remainCalcCnt <= 0:
                self.rmSprite(owner, slotIndex)
                owner._checkSpriteWingWorldResSysRemoveNotify()
                return
            current = current or utils.getNow()
            if current - sVal.lastCalcTime < self.CALC_INTERVAL:
                self._startTimer(owner, slotIndex, sVal, subOffset=current - sVal.lastCalcTime)
                return
            if not currentSecs:
                current = utils.getNow()
                startSecs, endSecs = self.getStartEndSecs()
                currentSecs = self.getSecs(current)
            lastCaltSecs = self.getSecs(sVal.lastCalcTime)
            setNotInTime = not startSecs < lastCaltSecs < endSecs
            beforeStart = lastCaltSecs <= startSecs
            afterEnd = lastCaltSecs >= endSecs
            isSameDay = utils.isSameDay(current, sVal.lastCalcTime)
            needPendingTimer = False
            needCalc = False
            needCalcToDayEnd = False
            inCalcTime = self.inValidTime(current)
            isTodayRes = False
            if setNotInTime:
                if isSameDay:
                    if inCalcTime:
                        needCalc = True
                    elif currentSecs <= startSecs:
                        needPendingTimer = True
                    elif currentSecs >= endSecs:
                        if beforeStart:
                            needCalc = True
                            needCalcToDayEnd = True
                        elif afterEnd:
                            needPendingTimer = True
                    isTodayRes = True
                elif utils.isSameDay(current, sVal.lastCalcTime + const.SECONDS_PER_DAY):
                    if lastCaltSecs <= endSecs:
                        needCalc = True
                        needCalcToDayEnd = True
                    else:
                        if inCalcTime:
                            needCalc = True
                        elif currentSecs <= startSecs:
                            needPendingTimer = True
                        elif currentSecs >= endSecs:
                            needCalc = True
                            needCalcToDayEnd = True
                        isTodayRes = True
                else:
                    needCalc = True
                    needCalcToDayEnd = True
            else:
                if isSameDay and inCalcTime:
                    needCalc = True
                else:
                    needCalc = True
                    needCalcToDayEnd = True
                isTodayRes = isSameDay
            if needPendingTimer:
                if not owner.spriteWingWorldResTimerId:
                    secs = self.getSecsToNextStartTime(currentSecs=currentSecs, startSecs=startSecs)
                    owner.spriteWingWorldResTimerId = owner._callback(secs, '_onTimeToStartSpriteWingWorldResCollect', ())
            if needCalc:
                if needCalcToDayEnd:
                    calcCnt = max(0, sVal.remainCalcCnt)
                elif not isSameDay and lastCaltSecs >= endSecs:
                    calcCnt = max(0, min(sVal.remainCalcCnt, int(max(0, min(currentSecs, endSecs) - startSecs) / self.CALC_INTERVAL)))
                else:
                    calcCnt = max(0, min(sVal.remainCalcCnt, int(max(0, min(currentSecs, endSecs) - max(startSecs, lastCaltSecs)) / self.CALC_INTERVAL)))
                maxResPerDay = max(0, int(max(self.maxSpeedTemp, self.maxSpeed) * (1.0 * max(0, endSecs - startSecs) / self.CALC_INTERVAL / self.SPRITE_COLLECT_RATE)))
                oldCalcTime = sVal.lastCalcTime
                if calcCnt:
                    sVal.remainCalcCnt = max(0, sVal.remainCalcCnt - calcCnt)
                    sVal.lastCalcTime = utils.getNow() if needCalcToDayEnd else utils.getNow() - max(0, currentSecs - startSecs) % self.CALC_INTERVAL
                    res = self._calcSingleSpriteRes(owner, sVal.spriteIndex, calcCnt)
                    oldTotal = sum(self.resDictCurrent.itervalues())
                    if utils.isSameDay(oldCalcTime, utils.getNow()) and int(self.resTotalDay + sum(res.itervalues())) > maxResPerDay:
                        if riskControl.checkFeature(None, gameconst.F_SPRITE_RES_REPORT):
                            gameengine.reportCritical('@xzh sprite wing res limit! %d %d %d %d' % (owner.gbID,
                             self.resTotalDay,
                             sum(res.itervalues()),
                             maxResPerDay))
                    else:
                        self._addRes(res)
                        newTotal = sum(self.resDictCurrent.itervalues())
                        if isTodayRes:
                            self.resTotalDay += newTotal - oldTotal
                            self.calcMaxSpeed(owner)
                sendClient and owner.soulClient.onSpriteWingWorldResSyncRes(self.resDictCurrent, self.resTotalDay)
                if needCalcToDayEnd or sVal.remainCalcCnt <= 0:
                    self.rmSprite(owner, slotIndex, sendClient=sendClient)
                elif inCalcTime:
                    if setNotInTime:
                        subOffset = max(0, (currentSecs - startSecs) % self.CALC_INTERVAL)
                    else:
                        subOffset = max(0, (current - oldCalcTime) % self.CALC_INTERVAL)
                    self._startTimer(owner, slotIndex, sVal, subOffset=subOffset)

    def unlockSlot(self, slotIndex):
        self.unlockedSlots.add(slotIndex)

    def lockSlot(self, slotIndex):
        self.unlockedSlots.discard(slotIndex)

    if BigWorld.component in ('base', 'cell'):

        def setSprite(self, owner, slotIndex, spriteIndex):
            sVal = SpriteWingWorldResVal()
            sVal.spriteIndex = spriteIndex
            sVal.lastCalcTime = utils.getNow()
            sVal.remainCalcCnt = self.getRemainCalcCnt()
            self.spriteInSlots[slotIndex] = sVal
            if self.inValidTime():
                self._startTimer(owner, slotIndex, sVal)
            else:
                self._startPendingTimer(owner)

        def rmSprite(self, owner, slotIndex, sendClient = True, byPlayer = False):
            sVal = self.spriteInSlots.pop(slotIndex, None)
            if sVal:
                self._cancelTimer(owner, sVal)
                sendClient and self.transfer(owner)
                if not byPlayer:
                    serverlog.genWingWorldSpriteResOpLog(owner, gameconst.WING_WORLD_SPRITE_RES_OP_BACK_BY_SYS, sVal.spriteIndex)
            return sVal

        def refreshAllTimer(self, owner):
            now = utils.getNow()
            for slotIndex, sVal in self.spriteInSlots.iteritems():
                sVal.lastCalcTime = now
                self._startTimer(owner, slotIndex, sVal)

        def _startTimer(self, owner, slotIndex, sVal, subOffset = 0):
            if sVal.timerId and owner._hasITimer(sVal.timerId):
                owner._cancelCallback(sVal.timerId)
            lastCalcTime = sVal.lastCalcTime or utils.getNow()
            srcs = max(0, self.CALC_INTERVAL - subOffset)
            sVal.timerId = owner._callback(srcs, '_calcSpriteWingWorldResSingle', (slotIndex,))

        def _cancelTimer(self, owner, sVal):
            if sVal.timerId and owner._hasITimer(sVal.timerId):
                owner._cancelCallback(sVal.timerId)
            sVal.timerId = 0

        def _startPendingTimer(self, owner):
            if not owner.spriteWingWorldResTimerId:
                secs = self.getSecsToNextStartTime()
                owner.spriteWingWorldResTimerId = owner._callback(secs, '_onTimeToStartSpriteWingWorldResCollect', ())
            shour, smin, _, _ = WWCD.data.get('spriteResCollectTimeRange', (12, 30, 18, 30))
            owner.soulClient.showGameMsg(GMDD.data.WING_WORLD_SPRITE_RES_COLLECT_NOT_IN_TIME, (shour, smin))

        def getSpriteVal(self, slotIndex):
            return self.spriteInSlots.get(slotIndex, None)

        def getSpriteIndex(self, slotIndex):
            sVal = self.getSpriteVal(slotIndex)
            if sVal:
                return sVal.spriteIndex
            return 0

        def getSlotIndexBySpriteIndex(self, spriteIndex):
            for slotIndex, sVal in self.spriteInSlots.iteritems():
                if sVal.spriteIndex == spriteIndex:
                    return slotIndex

            return 0

    else:

        def getSpriteIndex(self, slotIndex):
            return self.spriteInSlots.get(slotIndex, 0)

        def getSlotIndexBySpriteIndex(self, spriteIndex):
            for slotIndex, sSpriteIndex in self.spriteInSlots.iteritems():
                if sSpriteIndex == spriteIndex:
                    return slotIndex

            return 0

    if BigWorld.component in ('base', 'cell'):

        def submitAllRes(self, owner):
            if not self.resDictCurrent:
                return
            guildRatio, countryRatio = WWCD.data.get('spriteResCollectSubmitSplitRatio', (7, 3))
            guildPct = min(1.0, float(guildRatio) / (guildRatio + countryRatio))
            guildRes, countryRes = {}, {}
            for resId, resNum in self.resDictCurrent.iteritems():
                resVal = int(resNum)
                guildRes[resId] = int(resVal * guildPct)
                countryRes[resId] = resVal - guildRes[resId]

            resDictBak = copy.copy(self.resDictCurrent)
            self.resDictCurrent.clear()
            if guildRes and owner.guildBoxOfBase:
                owner.guildBoxOfBase.addWingWorldResourceFromSprite(owner.gbID, guildRes)
            if countryRes:
                gameengine.getGlobalBase('WingWorldStub').addResource(countryRes)
            if self.fameCurrent:
                fameId = WWCD.data.get('spriteResCollectFameId', 0)
                fame = int(self.fameCurrent)
                self.fameCurrent = 0
                owner.cell.addFame(fameId, fame, LSDD.data.LOG_SRC_WING_WORLD_SPRITE_RES_COLLECT, 0, 0)
            owner.soulClient.onSpriteWingWorldResSyncRes(self.resDictCurrent, self.resTotalDay)
            owner.soulClient.showGameMsg(GMDD.data.WING_WORLD_SPRITE_RES_COLLECT_SUBMIT_SUCC, ())
            self._calcRandomEvent(owner, resDictBak, fame)

        def _calcRandomEvent(self, owner, res, fameVal):
            eIds = set()
            rareData = WWRSRSRD.data.get(self.specialRareLv, {})
            if rareData:
                rareType = random.choice(rareData.keys())
                eId = utils.randomByDictUniform(rareData[rareType], 0)
                if eId:
                    eIds.add(eId)
            f = WWCD.data.get('spriteResCollectEventProbFormula', None)
            if f:
                args = {}
                for resType in WWRSD.data.iterkeys():
                    args['r{0}'.format(resType)] = res.get(resType, 0)

                prob = f(args)
                if random.random() <= prob:
                    eTypes = set()
                    eventRatioDict = WWCD.data.get('spriteResCollectEventRatioByType', {})
                    for eType, eProb in eventRatioDict.iteritems():
                        if random.random() > eProb:
                            continue
                        eTypes.add(eType)

                    for eType in eTypes:
                        eIdsByType = WWRSRERD.data.get(eType, {})
                        eId = utils.randomByDictUniform(eIdsByType, 0)
                        if eId:
                            eIds.add(eId)

            if self.specialRareLv:
                self.specialCntDay += 1
            self.resetAfterSubmit(owner)
            if eIds:
                owner.cell.doSpriteWingWorldResRandomEvent(eIds)
                owner.soulClient.onSpriteWingWorldResRandomEvent(eIds)
            serverlog.genWingWorldSpriteResSubmitLog(owner, res, fameVal, eIds)

    if BigWorld.component in ('base', 'cell'):

        def _getSpeed(self, owner, index):
            sprite = owner.ownSprites.getSprite(index)
            if not sprite:
                return {}
            speedDict = {}
            for resType in WWRSD.data.iterkeys():
                pVal = self._getSpritePropValByResId(resType, sprite)
                if pVal:
                    guildPointCnt = wingWorldUtils.getGuildResourcePointCount(owner.guildNUIDOfBase, resType) if owner.guildNUIDOfBase else 0
                    countryPointCnt = wingWorldUtils.getCurHostResourcePointCount(resType)
                    speed = wingWorldUtils.getResourceCollectSpeed(resType, pVal, guildPointCnt, countryPointCnt)
                    speedDict[resType] = speed

            return speedDict

        def _calcSingleSpriteRes(self, owner, index, cnt):
            speedDict = self._getSpeed(owner, index)
            gainDict = {}
            for resType, resVal in speedDict.iteritems():
                gainDict[resType] = resVal * cnt

            resDict = {}
            for resType, resVal in gainDict.iteritems():
                collectCoef = WWRSD.data.get(resType, {}).get('collectCoef', {})
                baseVal = self.resDictCurrent.get(resType, 0)
                realVal = self.calcResReducedByCoef(collectCoef, resVal, baseVal)
                resDict[resType] = realVal

            return resDict

        def calcResReducedByCoef(self, collectCoef, val, baseVal):
            retVal = baseVal
            remainVal = val
            keys = sorted(collectCoef.keys(), cmp=lambda a, b: cmp(a[1], b[1]))
            for rang in keys:
                low, high = rang
                if retVal >= high:
                    continue
                coef = collectCoef.get(rang, 0)
                if not coef:
                    continue
                need = (high - retVal) / coef
                if remainVal >= need:
                    remainVal -= need
                    retVal += need * coef
                else:
                    retVal += remainVal * coef
                    remainVal = 0

            return retVal - baseVal

        def _getSpritePropValByResId(self, resId, sprite):
            if not any(sprite.props.vPropCache):
                sprite._calcSpritePropList()
            maxHp, phyAtk, mgcAtk, phyDef, mgcDef = sprite.props.vPropCache
            if resId == gametypes.WING_RESOURCE_TYPE_OBSIDIAN:
                return max(phyAtk, mgcAtk)
            if resId == gametypes.WING_RESOURCE_TYPE_CATEYE:
                return max(phyDef, mgcDef)
            if resId == gametypes.WING_RESOURCE_TYPE_DIAMOND:
                return maxHp
            return 0

        def _addRes(self, res):
            if not gameconfig.enableWingWorldSpriteResCollect():
                return
            for resType, resNum in res.iteritems():
                self.resDictCurrent[resType] = min(self.resDictCurrent.get(resType, 0) + resNum, WWRSD.data.get(resType, {}).get('collectMax', const.MAX_UINT32))

            self.fameCurrent = wingWorldUtils.getFameByResourceCollectVal(sum(self.resDictCurrent.itervalues()))

        def _resetRes(self):
            self.resDictCurrent.clear()
