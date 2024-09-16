#Embedded file name: I:/bag/tmp/tw2/res/entities\common/newServerSignIn.o
import utils
import BigWorld
from userSoleType import UserSoleType
from userDictType import UserDictType
from data import item_data as ID
if BigWorld.component in ('base', 'cell'):
    import gamebonus
    import Netease
    import gameconst
    import serverlog
    import logconst
    import gameconfig
    import mail
    from data import log_src_def_data as LSDD
    from cdata import activity_resignin_config_data as ARCD
    from cdata import mail_template_def_data as MTDD
from data import activity_signin_type_data as ASTD
from data import activity_signin_bonus_data as ASBD
from cdata import game_msg_def_data as GMDD

class NewServerSignInVal(UserSoleType):

    def __init__(self, signId):
        self.id = signId
        self.dates = []
        self.resignCnt = 0
        self.exactDayBonus = []

    def getData(self):
        return ASTD.data[self.id]

    @staticmethod
    def getStartDayByData(d):
        if d.get('isOpenServer'):
            start = utils.getYearMonthDayInt(utils.getServerOpenTime())
        else:
            start = d.get('startDay', 0)
        return start

    def getStartDay(self):
        return NewServerSignInVal.getStartDayByData(self.getData())

    def getTotalSignCnt(self):
        return len(self.dates)

    def getExactSignDay(self):
        startDay = self.getStartDay()
        return utils.diffYearMonthDayInt(utils.getYearMonthDayInt(), startDay) + 1

    def checkCanSignToDay(self):
        if not self.isRunning():
            return False
        if self.hasSignedToday():
            return False
        return True

    def hasSignedToday(self):
        today = utils.getYearMonthDayInt()
        return today in self.dates

    def signInToday(self, owner):
        if not self.checkCanSignToDay():
            return False
        bonusId = ASBD.data[self.id, self.getTotalSignCnt() + 1].get('bonusId', 0)
        rewardItems = gamebonus.genItemBonus(bonusId)
        exactBonusId = ASBD.data[self.id, self.getExactSignDay()].get('exactDayBonus', 0)
        if exactBonusId:
            exactBonus = gamebonus.genItemBonus(exactBonusId)
            rewardItems += exactBonus
        rewardItemDict = {}
        for itemId, itemNum in rewardItems:
            rewardItemDict[itemId] = rewardItemDict.setdefault(itemId, 0) + itemNum

        if owner.inv.isRefuse():
            owner.client.showGameMsg(GMDD.data.ITEM_INV_LOCKED, ())
            return False
        if not owner.inv.canInsertItems(owner, rewardItemDict, True):
            return False
        today = utils.getYearMonthDayInt()
        self.dates.append(today)
        opNUID = Netease.getNUID()
        detail = '%d,%d' % (self.id, self.getTotalSignCnt())
        owner._placeInvItemsWithMwrapCheck(rewardItemDict, opNUID, LSDD.data.LOG_SRC_SIGN_IN_AWARD, opCode=gameconst.WEALTH_OP_SIGN_IN, detail=detail)
        serverlog.genActivitySignInLog(owner, logconst.SIGN_IN_LOG_SIGN_IN, today, self.getTotalSignCnt(), self.id)
        return True

    def getUnSignInDays(self):
        """
        \xbc\xc6\xcb\xe3\xb4\xd3\xc7\xa9\xb5\xbd\xbf\xaa\xca\xbc\xb5\xbd\xb5\xb1\xc7\xb0\xc8\xd5\xc6\xda\xb5\xc4\xc2\xa9\xc7\xa9\xb4\xce\xca\xfd
        :return: \xc2\xa9\xc7\xa9\xb4\xce\xca\xfd
        """
        if self.isOutdated():
            return self.getData().get('duration') - len(self.dates)
        startDay = self.getStartDay()
        prevDay = utils.shiftYearMonthDayInt(utils.getYearMonthDayInt(), -1)
        totalCnt = self.getTotalSignCnt()
        if self.hasSignedToday():
            totalCnt -= 1
        return utils.diffYearMonthDayInt(prevDay, startDay) + 1 - totalCnt

    def getFirstUnsignInDay(self):
        """
        \xbc\xc6\xcb\xe3\xb5\xda\xd2\xbb\xb8\xf6\xc2\xa9\xc7\xa9\xb5\xc4\xc8\xd5\xc6\xda
        :return: \xc2\xa9\xc7\xa9\xc8\xd5\xc6\xda\xa3\xacNone\xd4\xf2\xc3\xbb\xd3\xd0\xc2\xa9\xc7\xa9
        """
        signData = self.getData()
        startDay = self.getStartDay()
        prevDay = utils.shiftYearMonthDayInt(utils.getYearMonthDayInt(), -1)
        for day in range(0, signData.get('duration', 0)):
            thisDay = utils.shiftYearMonthDayInt(startDay, day)
            if day > prevDay:
                return None
            if thisDay not in self.dates:
                return thisDay

    def reSignIn(self, owner):
        if not self.isRunning():
            return False
        resignDays = self.getUnSignInDays()
        if resignDays <= 0:
            owner.client.showGameMsg(GMDD.data.RE_SIGN_IN_FAILED_NO_RESIGN_IN_CNT, ())
            return False
        resignData = ARCD.data.get(self.id)
        if not resignData:
            return
        maxAllowReSignCnt = resignData.get('reSignInCnt', 0)
        if self.resignCnt >= maxAllowReSignCnt:
            owner.client.showGameMsg(GMDD.data.RE_SIGN_IN_MAX_LIMIT, ())
            return False
        curResignDay = None
        curResignDay = self.getFirstUnsignInDay()
        if not curResignDay:
            return False
        reSignInCostItemId = resignData.get('reSignInItemId', 0)
        reSignInCostitemNum = resignData.get('reSignInItemCnt', {}).get(self.resignCnt + 1, 0)
        if not reSignInCostItemId or not reSignInCostitemNum:
            return False
        if owner.inv.isRefuse():
            owner.client.showGameMsg(GMDD.data.ITEM_INV_LOCKED, ())
            return False
        if not owner.inv.canRemoveItems({reSignInCostItemId: reSignInCostitemNum}, enableParentCheck=True):
            itemName = ID.data.get(reSignInCostItemId, {}).get('name', '')
            owner.client.showGameMsg(GMDD.data.RE_SIGN_IN_FAILED_NO_SUCH_ITEM, (reSignInCostitemNum, itemName))
            return False
        opNUID = Netease.getNUID()
        bonusId = ASBD.data[self.id, self.getTotalSignCnt() + 1].get('bonusId', 0)
        rewardItems = gamebonus.genItemBonus(bonusId)
        exactBonusId = ASBD.data[self.id, utils.diffYearMonthDayInt(curResignDay, self.getStartDay()) + 1].get('exactDayBonus', 0)
        if exactBonusId:
            exactBonus = gamebonus.genItemBonus(exactBonusId)
            rewardItems += exactBonus
        rewardItemsDict = {}
        for itemId, itemNum in rewardItems:
            rewardItemsDict[itemId] = rewardItemsDict.get(itemId, 0) + itemNum

        if not owner.inv.canInsertItems(owner, rewardItemsDict, True):
            return False
        ret = owner.inv.autoConsumeItems(owner, reSignInCostItemId, reSignInCostitemNum, opNUID, logSrc=LSDD.data.LOG_SRC_RE_SIGN_IN, enableParentCheck=True)
        if not ret:
            return False
        self.resignCnt += 1
        self.dates.append(curResignDay)
        opNUID = Netease.getNUID()
        detail = '%d,%d' % (self.id, self.getTotalSignCnt())
        owner._placeInvItemsWithMwrapCheck(rewardItemsDict, opNUID, LSDD.data.LOG_SRC_SIGN_IN_AWARD, opCode=gameconst.WEALTH_OP_SIGN_IN, detail=detail)
        serverlog.genActivitySignInLog(owner, logconst.SIGN_IN_LOG_RE_SIGN_IN, curResignDay, self.getTotalSignCnt(), self.id)
        return True

    def getLastDay(self):
        startDay = self.getStartDay()
        signData = self.getData()
        return utils.shiftYearMonthDayInt(startDay, signData.get('duration', 0) - 1)

    def isOutdated(self):
        return utils.getYearMonthDayInt() > self.getLastDay()

    def isStart(self):
        return utils.getYearMonthDayInt() >= self.getStartDay()

    def isRunning(self):
        return self.isStart() and not self.isOutdated()

    def isOpenServerSignIn(self):
        return self.getData().get('isOpenServer', False)

    @property
    def randomBonusId(self):
        """\xd6\xb8\xb6\xa8\xc8\xd5\xc6\xda\xb5\xc4\xcb\xe6\xbb\xfa\xbd\xb1\xc0\xf8"""
        return ASBD.data.get((self.id, self.getExactSignDay()), {}).get('randomBonus', 0)

    @property
    def exactBonusId(self):
        """\xd6\xb8\xb6\xa8\xc8\xd5\xc6\xda\xb5\xc4\xbd\xb1\xc0\xf8"""
        return ASBD.data.get((self.id, self.getExactSignDay()), {}).get('exactDayBonus', 0)

    @property
    def accuBonusId(self):
        """\xc0\xdb\xbc\xc6\xc7\xa9\xb5\xbd\xbd\xb1\xc0\xf8"""
        return ASTD.data.get(self.id, {}).get('accuBonus', {}).get(self.signedDays, 0)

    @property
    def uniqueBonusId(self):
        """\xd2\xbb\xb4\xce\xd0\xd4\xbd\xb1\xc0\xf8"""
        uniqueBonus = ASTD.data.get(self.id, {}).get('uniqueBonus', (0, 0))
        if self.signedDays == uniqueBonus[0]:
            return uniqueBonus[1]

    @property
    def signedDays(self):
        """\xc0\xdb\xbc\xc6\xc7\xa9\xb5\xbd\xb5\xc4\xcc\xec\xca\xfd"""
        return len(self.dates)

    def signIn(self, owner):
        """\xd0\xc2\xb0\xe6\xbb\xee\xb6\xaf\xc7\xa9\xb5\xbd"""
        if not self.checkCanSignToDay():
            return False
        today = utils.getYearMonthDayInt()
        self.dates.append(today)
        if self.exactBonusId:
            self.exactDayBonus.append(self.getExactSignDay())
        logSrc = LSDD.data.LOG_SRC_ACTIVITY_SIGN_IN
        rewardItems = []
        if self.randomBonusId:
            gamebonus.genBonusEx(owner, logSrc, self.randomBonusId, owner.lv, owner.onGetSignInRandomBonusItem, self.id)
        if self.accuBonusId:
            rewardItems += gamebonus.genItemBonus(self.accuBonusId)
        if self.uniqueBonusId:
            rewardItems += gamebonus.genItemBonus(self.uniqueBonusId)
        if self.exactBonusId:
            rewardItems += gamebonus.genItemBonus(self.exactBonusId)
        rewardItemDict = {}
        items = []
        for itemId, itemNum in rewardItems:
            rewardItemDict[itemId] = rewardItemDict.setdefault(itemId, 0) + itemNum
            items.append((itemId, itemNum))

        if owner.inv.isRefuse() or not owner.inv.canInsertItems(owner, rewardItemDict, False):
            templateId = MTDD.data.GM_ITEM2408
            mail.sendSysMailEx(owner.gbId, '', templateId, logSrc=logSrc, itemBonus=items)
        else:
            opNUID = Netease.getNUID()
            detail = '%d,%d' % (self.id, self.getTotalSignCnt())
            owner._placeInvItemsWithMwrapCheck(rewardItemDict, opNUID, logSrc, opCode=gameconst.WEALTH_OP_SIGN_IN, detail=detail)
        serverlog.genActivitySignInLog(owner, logconst.SIGN_IN_LOG_SIGN_IN, today, self.getTotalSignCnt(), self.id)
        return True

    def reSignInEx(self, owner):
        """\xd0\xc2\xb0\xe6\xbb\xee\xb6\xaf\xb2\xb9\xc7\xa9"""
        if not self.isRunning():
            return False
        resignDays = self.getUnSignInDays()
        if resignDays <= 0:
            owner.client.showGameMsg(GMDD.data.RE_SIGN_IN_FAILED_NO_RESIGN_IN_CNT, ())
            return False
        resignData = ARCD.data.get(self.id)
        if not resignData:
            return
        maxAllowReSignCnt = resignData.get('reSignInCnt', 0)
        if self.resignCnt >= maxAllowReSignCnt:
            owner.client.showGameMsg(GMDD.data.RE_SIGN_IN_MAX_LIMIT, ())
            return False
        curResignDay = self.getFirstUnsignInDay()
        if not curResignDay:
            return False
        reSignInCostItemId = resignData.get('reSignInItemId', 0)
        reSignInCostitemNum = resignData.get('reSignInItemCnt', {}).get(self.resignCnt + 1, 0)
        if not reSignInCostItemId or not reSignInCostitemNum:
            return False
        if owner.inv.isRefuse():
            owner.client.showGameMsg(GMDD.data.ITEM_INV_LOCKED, ())
            return False
        if not owner.inv.canRemoveItems({reSignInCostItemId: reSignInCostitemNum}, enableParentCheck=True):
            itemName = ID.data.get(reSignInCostItemId, {}).get('name', '')
            owner.client.showGameMsg(GMDD.data.RE_SIGN_IN_FAILED_NO_SUCH_ITEM, (reSignInCostitemNum, itemName))
            return False
        self.resignCnt += 1
        self.dates.append(curResignDay)
        opNUID = Netease.getNUID()
        owner.inv.autoConsumeItems(owner, reSignInCostItemId, reSignInCostitemNum, opNUID, logSrc=LSDD.data.LOG_SRC_ACTIVITY_RESIGN_IN, enableParentCheck=True)
        logSrc = LSDD.data.LOG_SRC_ACTIVITY_RESIGN_IN
        rewardItems = []
        if self.accuBonusId:
            rewardItems += gamebonus.genItemBonus(self.accuBonusId)
        if self.uniqueBonusId:
            rewardItems += gamebonus.genItemBonus(self.uniqueBonusId)
        rewardItemDict = {}
        items = []
        for itemId, itemNum in rewardItems:
            rewardItemDict[itemId] = rewardItemDict.setdefault(itemId, 0) + itemNum
            items.append((itemId, itemNum))

        if owner.inv.isRefuse() or not owner.inv.canInsertItems(owner, rewardItemDict, False):
            templateId = MTDD.data.GM_ITEM2408
            mail.sendSysMailEx(owner.gbId, '', templateId, logSrc=logSrc, itemBonus=items)
        else:
            opNUID = Netease.getNUID()
            detail = '%d,%d' % (self.id, self.getTotalSignCnt())
            owner._placeInvItemsWithMwrapCheck(rewardItemDict, opNUID, logSrc, opCode=gameconst.WEALTH_OP_SIGN_IN, detail=detail)
        serverlog.genActivitySignInLog(owner, logconst.SIGN_IN_LOG_RE_SIGN_IN, curResignDay, self.getTotalSignCnt(), self.id)
        return True


class NewServerSignIn(UserDictType):

    def __init__(self, **kwargs):
        super(NewServerSignIn, self).__init__(**kwargs)
        self.lastCalcDay = 0
        self.currentIds = []

    def initNewServerSignIn(self, signInId):
        if signInId not in self:
            self[signInId] = NewServerSignInVal(signInId)

    def clearOutDatedSignInInfo(self):
        if len(self) < 3:
            return
        its = self.items()
        its.sort(key=lambda x: x[1].getLastDay())
        toClearIds = its[:2]
        for k, _ in toClearIds:
            if not self[k].isOutdated():
                continue
            del self[k]

    def recalcCurrentIds(self):
        """
        \xd6\xd8\xd0\xc2\xbc\xc6\xcb\xe3\xb5\xb1\xc7\xb0\xc7\xa9\xb5\xbdID\xa3\xac\xd0\xc2\xb7\xfe\xc7\xa9\xb5\xbd\xd3\xc5\xcf\xc8\xd3\xda\xbb\xee\xb6\xaf\xc7\xa9\xb5\xbd
        :return:
        """
        now = utils.getYearMonthDayInt()
        if now == self.lastCalcDay:
            return
        myHostId = int(gameconfig.getHostId())
        candidates = []
        for k, v in ASTD.data.iteritems():
            startDay = NewServerSignInVal.getStartDayByData(v)
            endDay = utils.shiftYearMonthDayInt(startDay, v.get('duration', 0))
            if not startDay <= now < endDay:
                continue
            includeHosts = v.get('includeHosts', None)
            if includeHosts is not None and myHostId not in includeHosts:
                continue
            excludeHosts = v.get('excludeHosts', None)
            if excludeHosts is not None and myHostId in excludeHosts:
                continue
            candidates.append(k)

        self.lastCalcDay = now
        self.currentIds = candidates

    def getWorkingSignInIds(self):
        self.recalcCurrentIds()
        for currentId in self.currentIds:
            if currentId not in self:
                self.initNewServerSignIn(currentId)

        return self.currentIds

    def hasNewServerSignIn(self):
        ids = self.getWorkingSignInIds()
        for signInId in ids:
            signInInfo = self[signInId]
            if signInInfo.isOpenServerSignIn():
                return True

        return False

    def _lateReload(self):
        for v in self.itervalues():
            if hasattr(v, 'reloadScript'):
                v.reloadScript()
