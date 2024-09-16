#Embedded file name: I:/bag/tmp/tw2/res/entities\common/flowback.o
import BigWorld
import gametypes
from userSoleType import UserSoleType
if BigWorld.component in ('base', 'cell'):
    import gameconfig
    import Netease
    import mail
    import serverlog
    import logconst
    import math
    import serverProgress
    from data import log_src_def_data as LSDD
    from cdata import game_msg_def_data as GMDD
    from data import vp_level_data as VLD
    from data import coin_charge_vip_grade_privilege_data as CCVGPD
    from data import formula_server_data as FFD
elif BigWorld.component == 'client' and not getattr(BigWorld, 'isBot', False):
    from data import formula_client_data as FFD
if BigWorld.component in ('base', 'cell', 'client'):
    import utils
    import const
    import formula
    from data import sys_config_data as SCD
    from data import flowback_bonus_type_data as FBTD
    flowbackBonusTypeToProp = {gametypes.FLOWBACK_BONUS_TYPE_JIULI: 'jiuliBonus',
     gametypes.FLOWBACK_BONUS_TYPE_YAOLI: 'yaoliBonus',
     gametypes.FLOWBACK_BONUS_TYPE_VP: 'vpBonus'}
    FLOWBACK_BONUS_SET_LIMITS = frozenset(flowbackBonusTypeToProp.keys())

    def getLostType(lostTime):
        lostDays = lostTime / const.SECONDS_PER_DAY
        for k, v in FBTD.data.iteritems():
            if v['days'][0] <= lostDays <= v['days'][1]:
                return k

        return 0


class FlowbackSingleBonus(UserSoleType):

    def __init__(self, lastApplyTime = 0, totalCount = 0, availCount = 0, fixedAmount = 0, lostType = 0, extraAmount = 0, consumeFameVal = 0, firstExtra = 0, roFirstExtra = 0):
        super(UserSoleType, self).__init__()
        self.lastApplyTime = lastApplyTime
        self.totalCount = totalCount
        self.availCount = availCount
        self.fixedAmount = fixedAmount
        self.extraAmount = extraAmount
        self.lostType = lostType
        self.consumeFameVal = consumeFameVal
        self.firstExtra = firstExtra
        self.roFirstExtra = roFirstExtra

    def clearCD(self):
        self.lastApplyTime = 0

    def getData(self):
        return FBTD.data.get(self.lostType, {})

    def checkCanApplyBonus(self, owner, useExtra, bMsg = True):
        if not self.lostType:
            return False
        _, _, _, applyInterval, consumeFameId, _, _ = type(self).getDataSpecification(self.lostType, owner)
        if utils.getNow() - self.lastApplyTime < applyInterval:
            bMsg and owner.client.showGameMsg(GMDD.data.FLOWBACK_BONUS_APPLY_IN_CD, ())
            return False
        if self.availCount <= 0:
            bMsg and owner.client.showGameMsg(GMDD.data.FLOWBACK_BONUS_APPLY_OUT_OF_LIMIT, ())
            return False
        if useExtra and self.extraAmount > 0:
            if not owner.fame.enoughFame([(consumeFameId, self.consumeFameVal)], owner):
                bMsg and owner.client.showGameMsg(GMDD.data.FLOWBACK_BONUS_APPLY_FAME_NOT_ENOUGH, ())
                return False
        return True

    def consumeFame(self, owner, useExtra):
        if not useExtra:
            return True
        _, _, _, _, consumeFameId, _, _ = type(self).getDataSpecification(self.lostType, owner)
        if self.extraAmount > 0:
            owner.reduceFame(consumeFameId, self.consumeFameVal, srcType=LSDD.data.LOG_SRC_FLOWBACK_BONUS)
        return True

    def applyBonus(self, owner, useExtra):
        if not self.checkCanApplyBonus(owner, useExtra, True):
            return
        if not self.consumeFame(owner, useExtra):
            return
        if self.applyBonusInternal(owner, useExtra):
            self.onBonusApplied(owner)

    def onBonusApplied(self, owner):
        self.availCount -= 1
        self.lastApplyTime = utils.getNow()

    def applyBonusInternal(self, owner, useExtra):
        raise Exception('You must implement this!(2)')

    @classmethod
    def calcLostHours(cls, lostTime, owner):
        fId = SCD.data.get('calcVpBasedLostHoursFid', 10006)
        funcRet = formula.calcFormulaById(fId, {'lv': owner.lv})
        vpBasedLostHours = int(owner.overflowExp / funcRet / 5.0 / 60)
        return max(vpBasedLostHours, (int(math.ceil(lostTime * 1.0 / const.SECONDS_PER_DAY)) - 2) * (min(max(owner.lv - 44, 0), 1) + min(max(owner.lv - 34, 0), 1) * 0.5 + min(max(owner.lv - 19, 0), 1) * 3.5))

    @classmethod
    def calcAmountBase(cls, lostTime, owner):
        raise Exception('You must implement this!')

    @classmethod
    def getDataSpecification(cls, lostType, owner):
        raise Exception('You must implement this!')

    @classmethod
    def createBonusObj(cls, lostTime, owner):
        obj = cls()
        obj.lostType = getLostType(lostTime)
        obj.lastApplyTime = 0
        discountFactor, countFormula, extraKey, applyInterval, _, fameFactor, firstPercent = cls.getDataSpecification(obj.lostType, owner)
        totalAmount = int(round(cls.calcAmountBase(lostTime, owner) * discountFactor))
        ctx = {'lostTime': lostTime,
         'lostLv': owner.lv}
        obj.totalCount = countFormula(ctx)
        obj.firstExtra = 0
        obj.roFirstExtra = 0
        if obj.totalCount == 0:
            obj.fixedAmount = 0
        elif firstPercent > 0 and obj.totalCount > 1:
            obj.firstExtra = int(round(totalAmount * firstPercent))
            obj.fixedAmount = (totalAmount - obj.firstExtra) // (obj.totalCount - 1)
            obj.firstExtra -= obj.fixedAmount
            obj.roFirstExtra = obj.firstExtra
        else:
            obj.fixedAmount = totalAmount // obj.totalCount
        obj.availCount = obj.totalCount
        vipGrade = utils.getVipGrade(owner)
        if vipGrade:
            obj.extraAmount = int(CCVGPD.data[vipGrade].get(extraKey, 0) * obj.fixedAmount)
        else:
            obj.extraAmount = 0
        obj.consumeFameVal = int(fameFactor * obj.extraAmount)
        return obj

    def fromDTO(self, d):
        if 'lastApplyTime' in d:
            self.lastApplyTime = d['lastApplyTime']
        if 'totalCount' in d:
            self.totalCount = d['totalCount']
        if 'availCount' in d:
            self.availCount = d['availCount']
        if 'fixedAmount' in d:
            self.fixedAmount = d['fixedAmount']
        if 'lostType' in d:
            self.lostType = d['lostType']
        if 'extraAmount' in d:
            self.extraAmount = d['extraAmount']
        if 'consumeFameVal' in d:
            self.consumeFameVal = d['consumeFameVal']
        if 'firstExtra' in d:
            self.firstExtra = d['firstExtra']
        if 'roFirstExtra' in d:
            self.roFirstExtra = d['roFirstExtra']

    def getDTO(self):
        return {'lastApplyTime': self.lastApplyTime,
         'totalCount': self.totalCount,
         'availCount': self.availCount,
         'fixedAmount': self.fixedAmount,
         'lostType': self.lostType,
         'extraAmount': self.extraAmount,
         'consumeFameVal': self.consumeFameVal,
         'firstExtra': self.firstExtra,
         'roFirstExtra': self.roFirstExtra}

    def __cmp__(self, other):
        return cmp(other.availCount * (other.fixedAmount, other.extraAmount) + other.firstExtra, self.availCount * (self.fixedAmount + self.extraAmount) + self.firstExtra)


class FlowbackYaoliBonus(FlowbackSingleBonus):

    @classmethod
    def getDataSpecification(cls, lostType, owner):
        d = FBTD.data[lostType]
        return (d.get('yaoliFactor', 0),
         d.get('yaoliCountFormula', lambda c: 0),
         d.get('yaoliExtraVipFactorKey', lambda d: 0),
         d.get('yaoliApplyInterval', const.SECONDS_PER_DAY),
         d.get('yaoliExtraFameId', 0),
         d.get('yaoliExtraFameFactor', 0),
         0)

    def applyBonusInternal(self, owner, useExtra):
        amount = self.fixedAmount
        if useExtra:
            amount += self.extraAmount
        owner.yaoliPoint = max(owner.yaoliPoint - amount, 0)
        serverlog.markFlowbackPlayerApplyBonusLog(owner, self.lostType, gametypes.FLOWBACK_BONUS_TYPE_YAOLI, useExtra, self.fixedAmount, self.extraAmount, 0)
        return True

    @classmethod
    def calcAmountBase(cls, lostTime, owner):
        return cls.calcLostHours(lostTime, owner)


class FlowbackJiuliBonus(FlowbackSingleBonus):

    @classmethod
    def getDataSpecification(cls, lostType, owner):
        d = FBTD.data[lostType]
        return (d.get('jiuliFactor', 0),
         d.get('jiuliCountFormula', lambda c: 0),
         d.get('jiuliExtraVipFactorKey', lambda d: 0),
         d.get('jiuliApplyInterval', const.SECONDS_PER_DAY),
         d.get('jiuliExtraFameId', 0),
         d.get('jiuliExtraFameFactor', 0),
         0)

    def applyBonusInternal(self, owner, useExtra):
        amount = self.fixedAmount
        if useExtra:
            amount += self.extraAmount
        owner.addFame(const.FAME_ID_JIULI, amount, LSDD.data.LOG_SRC_FLOWBACK_BONUS)
        serverlog.markFlowbackPlayerApplyBonusLog(owner, self.lostType, gametypes.FLOWBACK_BONUS_TYPE_JIULI, useExtra, self.fixedAmount, self.extraAmount, 0)
        return True

    @classmethod
    def calcAmountBase(cls, lostTime, owner):
        return cls.calcLostHours(lostTime, owner)


class FlowbackVpBonus(FlowbackSingleBonus):

    @classmethod
    def getDataSpecification(cls, lostType, owner):
        d = FBTD.data[lostType]
        return (d.get('vpFactor', 0) * CCVGPD.data.get(utils.getVipGrade(owner), {}).get('vpVipFactor', 1),
         d.get('vpCountFormula', lambda c: 0),
         lambda d: 0,
         d.get('vpApplyInterval', const.SECONDS_PER_DAY),
         0,
         0,
         d.get('firstVpPercent') * CCVGPD.data.get(utils.getVipGrade(owner), {}).get('firstVpPercentFactor', 1))

    def checkCanApplyBonus(self, owner, useExtra, bMsg = True):
        if not super(FlowbackVpBonus, self).checkCanApplyBonus(owner, useExtra, bMsg):
            return False
        fixedAmount = self.fixedAmount + self.firstExtra
        amount = min(fixedAmount, owner.overflowExp)
        if amount <= 0 or not owner._doGetBackflowVp(amount, bCostFame=False):
            owner.client.showGameMsg(GMDD.data.APPLY_FLOWBACK_VP_NOT_ENOUGH, ())
            return False
        if owner.exp >= serverProgress.getMaxExp(owner.lv) and owner.expXiuWei >= owner.getMaxXiuWeiVal():
            owner.client.showGameMsg(GMDD.data.FLOWBACK_BONUS_EXP_XIUWEI_FULL, ())
            return
        if amount < fixedAmount:
            owner.client.showGameMsg(GMDD.data.FLOWBACK_BONUS_NOT_ENOUGH_VP, (amount,))
        return True

    def applyBonusInternal(self, owner, useExtra):
        amount = min(self.fixedAmount + self.firstExtra, owner.overflowExp)
        self.firstExtra = 0
        vld = VLD.data.get(owner.lv)
        vpDefaultLower = vld.get('vpDefaultLower')
        vpDefaultUpper = vld.get('vpDefaultUpper')
        exp = int(amount)
        owner.overflowExp -= exp
        owner.addExp(exp, {'logSrc': LSDD.data.LOG_SRC_FLOWBACK_BONUS})
        serverlog.markFlowbackPlayerApplyBonusLog(owner, self.lostType, gametypes.FLOWBACK_BONUS_TYPE_VP, useExtra, amount, 0, 0)
        return True

    @classmethod
    def calcAmountBase(cls, lostTime, owner):
        return int(round(owner.overflowExp))

    def checkCanClearApplyCD(self, owner):
        _, _, _, applyInterval, consumeFameId, _, _ = type(self).getDataSpecification(self.lostType, owner)
        if utils.getNow() - self.lastApplyTime >= applyInterval:
            return False
        if self.availCount <= 0:
            return False
        return True

    def clearVPApplyCD(self, owner):
        itemInfo = FBTD.data[self.lostType].get('vpClearCDItem', (240000, 1))
        if not itemInfo:
            return
        if not self.checkCanClearApplyCD(owner):
            owner.client.showGameMsg(GMDD.data.FLOWBACK_VP_APPLY_CD_NO_NEED, ())
            return
        itemDict = {itemInfo[0]: itemInfo[1]}
        if owner.inv.isRefuse():
            owner.client.showGameMsg(GMDD.data.ITEM_INV_LOCKED, ())
            return
        if not owner.inv.canRemoveItems(itemDict, enableParentCheck=True):
            owner.client.showGameMsg(GMDD.data.ITEM_NOT_ENOUGH_CLEAR_FLOWBACK_CD, ())
            return
        opNUID = Netease.getNUID()
        for itemId, itemNum in itemDict.iteritems():
            owner.inv.autoConsumeItems(owner, itemId, itemNum, opNUID, LSDD.data.LOG_SRC_FLOWBACK_BONUS, enableParentCheck=True)

        self.lastApplyTime = 0
        owner.syncFlowbackBonusToClient()


class Flowback(UserSoleType):

    def _lateReload(self):
        super(Flowback, self)._lateReload()
        self.yaoliBonus.reloadScript()
        self.jiuliBonus.reloadScript()
        self.vpBonus.reloadScript()

    def __init__(self):
        super(Flowback, self).__init__()
        self.lostType = 0
        self.startTime = 0
        self.itemBonusRefType = 0
        self.lastLostTime = 0
        self.thisLostTime = 0
        self.lastWorldChatTime = 0
        self.worldChatCount = 0
        self.lastTeleportTime = 0
        self.teleportCount = 0
        self.guildGiftCount = 0
        self.friendGiftCount = 0
        self.giftSentFriends = []
        self.yaoliBonus = FlowbackYaoliBonus()
        self.jiuliBonus = FlowbackJiuliBonus()
        self.vpBonus = FlowbackVpBonus()

    def reloadOnLogin(self, owner):
        if not gameconfig.enableFlowbackBonus():
            return
        if not owner.lastLogoffTime:
            return
        if owner.lv < SCD.data.get('FLOWBACK_MIN_LV', 20):
            return
        if SCD.data.has_key('flowbackStartTimes') and SCD.data.has_key('flowbackEndTimes'):
            fbStartTime = SCD.data['flowbackStartTimes']
            fbEndTime = SCD.data['flowbackEndTimes']
            current = utils.getNow()
            if not any([ utils.inTimeTupleRange(fbStartTime[i], fbEndTime[i], current) for i in xrange(len(fbStartTime)) ]):
                self.resetBonusInfo(owner, False)
            else:
                self.resetBonusInfo(owner)
        else:
            self.resetBonusInfo(owner)
        if self.isValid():
            self.addState(owner)
            owner.flowbackTypeOfCell = self.lostType
            owner.base.updateFriendFlowbackType((self.lostType, self.thisLostTime, self.giftSentFriends))
            owner.client.notifyFlowbackBonusAvailableOnLogin()
            remainTime = self.getBonusRemainTime()
            owner._callback(remainTime, 'onFlowbackExpire', ())
            serverlog.markFlowbackPlayerLog(owner)
        owner.syncFlowbackBonusToClient()

    def onExpire(self, owner):
        owner.flowbackTypeOfCell = 0
        owner.base.updateFriendFlowbackType((0, 0, []))

    def resetBonusInfo(self, owner, inFlowbackTime = True):
        lostTime = utils.getNow() - owner.lastLogoffTime
        typ = getLostType(lostTime)
        if typ:
            d = FBTD.data[typ]
            if 'hostId' in d and utils.getHostId() not in d.get('hostId', ()):
                return
            self.recalcFlowbackRights(owner, typ, inFlowbackTime)

    def addState(self, owner):
        if not self.isValid():
            return
        remainTime = self.getBonusRemainTime()
        states = FBTD.data[self.lostType].get('states', ())
        for stateId in states:
            owner.addState(stateId, 1, remainTime, gametypes.ADD_STATE_FROM_FLOWBACK, owner.id, 0)

    def recalcFlowbackRights(self, owner, newDurationType, inFlowbackTime = True):
        thisLostTime = utils.getNow() - owner.lastLogoffTime
        if inFlowbackTime:
            if self.itemBonusRefType and self.isValid():
                self.itemBonusRefType = [self.lostType, newDurationType][self.thisLostTime < thisLostTime]
            else:
                self.itemBonusRefType = newDurationType
        shouldReset = False
        if self.isValid() and self.getBonusRemainTime() > self.getBonusRemainTimeByStartDura(utils.getNow(), thisLostTime):
            pass
        else:
            self.lastLostTime = self.thisLostTime
            self.thisLostTime = utils.getNow() - owner.lastLogoffTime
            self.startTime = utils.getNow()
            shouldReset = True
        if not self.isValid() or shouldReset:
            self.lostType = newDurationType
            self.resetAllAttributes(owner, inFlowbackTime)
            return

    def resetAllAttributes(self, owner, inFlowbackTime = True):
        if inFlowbackTime:
            self.yaoliBonus = FlowbackYaoliBonus.createBonusObj(self.thisLostTime, owner)
            self.jiuliBonus = FlowbackJiuliBonus.createBonusObj(self.thisLostTime, owner)
        self.vpBonus = FlowbackVpBonus.createBonusObj(self.thisLostTime, owner)
        self.lastWorldChatTime = 0
        self.worldChatCount = 0
        self.lastTeleportTime = 0
        self.teleportCount = 0
        self.guildGiftCount = 0
        self.friendGiftCount = 0
        self.giftSentFriends = []

    def checkRightsExpire(self):
        return self.getBonusRemainTime() <= 0

    def getBonusRemainTimeByStartDura(self, startTime, lostTime):
        return FFD.data.get(SCD.data.get('FLOWBACK_BONUS_EXPIRE_TIME')).get('formula')({'lostTime': lostTime}) * const.SECONDS_PER_DAY - (utils.getNow() - startTime)

    def getBonusRemainTime(self):
        return self.getBonusRemainTimeByStartDura(self.startTime, self.thisLostTime)

    def isValidServer(self):
        d = FBTD.data.get(self.lostType, {})
        if 'hostId' in d and utils.getHostId() not in d['hostId']:
            return False
        return True

    def resetDaily(self, owner):
        if not self.isValid():
            return
        self.worldChatCount = 0
        self.teleportCount = 0
        self.friendGiftCount = 0
        self.guildGiftCount = 0
        self.giftSentFriends = []

    def hasFlowbackBonus(self):
        return self.lostType != 0

    def isValid(self):
        return not self.checkRightsExpire() and self.isValidServer() and self.hasFlowbackBonus()

    def getFlowbackType(self):
        if not self.isValid():
            return 0
        else:
            return self.lostType

    def applyBonus(self, owner, typ, useExtra):
        if not self.isValid():
            owner.client.showGameMsg(GMDD.data.FLOWBACK_BONUS_APPLY_NOT_AVAIL, ())
            return
        if typ in FLOWBACK_BONUS_SET_LIMITS:
            getattr(self, flowbackBonusTypeToProp[typ]).applyBonus(owner, useExtra)
        elif typ == gametypes.FLOWBACK_BONUS_TYPE_ITEM:
            self.applyItemBonus(owner)
        owner.syncFlowbackBonusToClient()

    def applyItemBonus(self, owner):
        if not self.itemBonusRefType:
            owner.client.showGameMsg(GMDD.data.FLOWBACK_BONUS_ITEM_ALREADY_APPLIED, ())
            return
        d = FBTD.data.get(self.itemBonusRefType, {})
        if not d:
            return
        if 'bonusId' not in d:
            return
        owner.base.sendFlowbackBonusItemMail(d['bonusId'], d['mailTemplateId'], self.itemBonusRefType)
        serverlog.markFlowbackPlayerApplyBonusLog(owner, self.lostType, gametypes.FLOWBACK_BONUS_TYPE_ITEM, 0, 1, 0, bonusId=d['bonusId'])
        self.itemBonusRefType = 0

    def revertItemBonus(self, owner, formalRef):
        self.itemBonusRefType = formalRef

    def clearVPApplyCD(self, owner):
        if not self.isValid():
            owner.client.showGameMsg(GMDD.data.FLOWBACK_BONUS_APPLY_NOT_AVAIL, ())
            return
        self.vpBonus.clearVPApplyCD(owner)

    def checkCanWorldChat(self, owner, bMsg = True):
        """
        \xbc\xec\xb2\xe9\xca\xc7\xb7\xf1\xc4\xdc\xb7\xa2\xcb\xcd\xca\xc0\xbd\xe7\xcf\xfb\xcf\xa2
        :param owner: Avatar
        :param bMsg: \xca\xc7\xb7\xf1\xd0\xe8\xd2\xaa\xb7\xb4\xc0\xa1
        :return:
        """
        now = utils.getNow()
        if now - self.lastWorldChatTime < SCD.data.get('NOVICE_BOOST_WORLD_CHAT_INTERVAL', 30):
            bMsg and owner.client.showGameMsg(GMDD.data.FLOWBACK_WORLD_CHAT_TOO_FREQUENT, ())
            return False
        if self.worldChatCount >= SCD.data.get('NOVICE_BOOST_WORLD_CHAT_DAILY_COUNT', 10):
            bMsg and owner.client.showGameMsg(GMDD.data.FLOWBACK_WORLD_CHAT_OUT_LIMIT, ())
            return False
        return True

    def checkTeleport(self, owner, bMsg):
        """
        \xbc\xec\xb2\xe9\xc4\xdc\xb7\xf1\xb4\xab\xcb\xcd
        :param owner: Avatar
        :param bMsg: \xca\xc7\xb7\xf1\xcf\xd4\xca\xbe\xcf\xfb\xcf\xa2
        :return:
        """
        now = utils.getNow()
        if now - self.lastTeleportTime < SCD.data.get('NOVICE_BOOST_TELEPORT_INTERVAL', 5):
            bMsg and owner.client.showGameMsg(GMDD.data.FLOWBACK_TELEPORT_TOO_FREQUENT, ())
            return False
        if self.teleportCount >= SCD.data.get('NOVICE_BOOST_TELEPORT_DAILY_CNT', 5):
            bMsg and owner.client.showGameMsg(GMDD.data.FLOWBACK_TELEPORT_OUT_OF_LIMIT, ())
            return False
        return owner.checkTeleportToSeekInternal()

    def _beforeTeleport(self):
        self.lastTeleportTime = utils.getNow()
        self.teleportCount += 1

    def teleportToSeek(self, owner, trackId):
        """
        \xb4\xab\xcb\xcd\xb5\xbd\xc4\xb3\xb8\xf6seek
        :param owner: Avatar 
        :param trackId: \xc4\xbf\xb1\xeaID
        :return:
        """
        return owner.teleportToSeekInternal(trackId, self._beforeTeleport)

    def updateWorldChatStat(self, owner):
        self.worldChatCount += 1
        self.lastWorldChatTime = utils.getNow()

    def checkCanRecvGuildGift(self, owner):
        if not owner.guildBox:
            return
        if not self.isValid():
            return False
        if self.guildGiftCount > 0:
            owner.client.showGameMsg(GMDD.data.FLOWBACK_BONUS_GUILD_COUNT_LIMIT, ())
            return False
        return True

    def applyGuildGift(self, owner):
        if not self.checkCanRecvGuildGift(owner):
            return
        d = FBTD.data[self.lostType]
        bonusId = d.get('guildBonusId', 20000)
        if not bonusId:
            return
        self.guildGiftCount += 1
        templateId = d.get('guildMailTemplateId', 0)
        guildCash = d.get('guildCash', 0)
        owner.client.showGameMsg(GMDD.data.FLOWBACK_GUILD_BONUS_MAILED_SUCC, ())
        mail.sendSysMailEx(owner.gbId, owner.roleName, templateId, logSrc=LSDD.data.LOG_SRC_FLOWBACK_BONUS, bonusId=bonusId)
        if guildCash:
            owner.guildBox.addFlowbackBonus(owner, guildCash)
        serverlog.markFlowbackPlayerGiftLog(owner, self.lostType, logconst.LOG_FLOWBACK_GIFT_GUILD, self.friendGiftCount, self.guildGiftCount, owner.guildNUID, 0)
        owner.syncFlowbackBonusToClient()
        return True

    def checkCanRecvFriendGift(self, owner):
        dailyFriendGiftCount = FBTD.data[self.lostType].get('dailyFriendGiftCount', 10)
        if not self.isValid():
            return False
        if self.friendGiftCount >= dailyFriendGiftCount:
            return False
        return True

    def applyFriendGift(self, owner, otherFriendBox, otherFriendGBID, otherRoleName):
        if not self.checkCanRecvFriendGift(owner):
            otherFriendBox.client.showGameMsg(GMDD.data.FLOWBACK_BONUS_OTHER_FRIEND_OUT_OF_LIMIT, ())
            return
        if otherFriendGBID in self.giftSentFriends:
            otherFriendBox.client.showGameMsg(GMDD.data.FLOWBACK_BONUS_FRIEND_ALREADY_SENT, ())
            return
        d = FBTD.data[self.lostType]
        bonusId = d.get('friendBonusId', 0)
        if not bonusId:
            return
        self.friendGiftCount += 1
        self.giftSentFriends.append(otherFriendGBID)
        templateId = d.get('friendMailTemplateId', 0)
        friendCash = d.get('friendCash', 0)
        owner.client.showGameMsg(GMDD.data.FLOWBACK_FRIEND_BONUS_MAILED_SUCC, (otherRoleName,))
        mail.sendSysMailEx(owner.gbId, owner.roleName, templateId, logSrc=LSDD.data.LOG_SRC_FLOWBACK_BONUS, bonusId=bonusId, subjectArgs=(otherRoleName,), contentArgs=(otherRoleName,))
        otherFriendBox.cell.onSendFriendGiftSucc(owner.gbId, owner.roleName, friendCash)
        serverlog.markFlowbackPlayerGiftLog(owner, self.lostType, logconst.LOG_FLOWBACK_GIFT_FRIEND, self.friendGiftCount, self.guildGiftCount, 0, otherFriendGBID)
        return True
