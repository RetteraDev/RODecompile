#Embedded file name: /WORKSPACE/data/entities/common/rolesaledata.o
import BigWorld
import utils
import gamelog
import gametypes
import const
import time
from userSoleType import UserSoleType
from data import cbg_config_data as CCD
from cdata import game_msg_def_data as GMDD
if BigWorld.component in ('base', 'cell'):
    import mail
    import gameconfig
    import math
    import gameengine
    import gameconst
    import serverlog
    from data import log_src_def_data as LSDD

class RoleSaleData(UserSoleType):

    def __init__(self):
        self.saleStatus = 0
        self.saleStatusTime = 0
        self.salePrice = 0
        self.saleDays = 0
        self.vendeeGbId = 0
        self.lastSaleDoneTime = 0
        self.newSaleFlag = 0
        self.newSaleFlagStartTime = 0
        self.ip = 0
        self.inSaleOperating = False
        self.unbindCoinCost = 0
        self.bindCoinCost = 0
        self.extra = {}
        self.newSaleFlagTimer = 0
        self.autoUnRegisterTimer = 0
        self.canPutOnSaleTimer = 0

    def __getstate__(self):
        return (self.saleStatus,
         self.saleStatusTime,
         self.salePrice,
         self.saleDays,
         self.vendeeGbId,
         self.lastSaleDoneTime)

    def __setstate__(self, state):
        self.saleStatus, self.saleStatusTime, self.salePrice, self.saleDays, self.vendeeGbId, self.lastSaleDoneTime = state

    def reset(self):
        self.saleStatus = 0
        self.saleStatusTime = 0
        self.salePrice = 0
        self.saleDays = 0
        self.vendeeGbId = 0
        self.extra = {}

    if BigWorld.component in ('base', 'cell'):

        def transfer(self, owner):
            if not gameconfig.enableCBGRole():
                return
            owner.client.onGetRoleSaleData(self)

        def onLogin(self, owner):
            if not gameconfig.enableCBGRole():
                return
            if not owner._isRaw():
                return
            if owner.lastLogoffTime and self.lastSaleDoneTime and owner.lastLogoffTime < self.lastSaleDoneTime:
                self._doOnFirstLogonAfterTrade(owner)
            self._doOnLogon(owner)

        def checkStatusCanTo(self, tStatus):
            if tStatus not in gametypes.ROLE_SALE_ALL_STATUS:
                return False
            if tStatus == gametypes.ROLE_SALE_STATUS_REGISTER:
                return self.saleStatus == gametypes.ROLE_SALE_STATUS_DEFAULT
            if tStatus == gametypes.ROLE_SALE_STATUS_ONSALE:
                return self.saleStatus == gametypes.ROLE_SALE_STATUS_REGISTER and utils.getNow() - self.saleStatusTime > CCD.data.get('roleSaleRegisterDays', 0) * const.SECONDS_PER_DAY
            return True

        def changeToStatus(self, tStatus):
            self.saleStatus = tStatus
            self.saleStatusTime = utils.getNow()

        def setIp(self, ip):
            self.ip = ip

        def getCoinCost(self):
            return self.unbindCoinCost + self.bindCoinCost

        def _doOnFirstLogonAfterTrade(self, owner):
            owner.cipherOfBase = ''
            owner.cell.onModifyCipherSuccess(owner.cipherOfBase)
            owner.soulClient.onCipherModified('')
            msgId = CCD.data.get('roleSaleDoneLogonFriendMsgId', 0)
            if msgId and gameconfig.enableCBGRoleMsg():
                owner.showGameMsgToAllFriends(msgId, (owner.roleName,))
            if owner._checkBindYixin():
                owner.cell.unBindYixin()
            owner.cell.onSetPhoneNum(owner.account.bindPhoneNum, 0)
            if gameconfig.enableCBGRoleAward():
                sTimeStr = CCD.data.get('roleSaleActivityBonusStartTime', '')
                eTimeStr = CCD.data.get('roleSaleActivityBonusEndTime', '')
                sTimeStamp = utils.getTimeSecondFromStr(sTimeStr)
                eTimeStamp = utils.getTimeSecondFromStr(eTimeStr)
                if sTimeStamp <= self.lastSaleDoneTime <= eTimeStamp:
                    self.newSaleFlag = 1
                    self.newSaleFlagStartTime = utils.getNow()
                    lastTime = CCD.data.get('roleSaleMarkFlagTime', 0)
                    self.newSaleFlagTimer = owner._callback(lastTime, '_onNewSaleRoleFlagTTL', ())
                    bonusList = CCD.data.get('roleSaleActivityBonusList', {})
                    if bonusList:
                        chooseBonusId = 0
                        for priceRange, bId in bonusList:
                            lPrice, rPrice = priceRange
                            if lPrice <= float(self.salePrice) / 100 <= rPrice:
                                chooseBonusId = bId
                                break

                        if chooseBonusId:
                            mailId = CCD.data.get('roleSaleActivityBonusMailId', 0)
                            if mailId:
                                mail.sendSysMailEx(owner.gbID, owner.roleName, mailId, logSrc=LSDD.data.LOG_SRC_CBG_ROLE, bonusId=chooseBonusId)
                    if gameconfig.enableCBGRoleMsg():
                        gameengine.broadcastBaseApp('broadcastClient', ('showSysNotification', (GMDD.data.NOVICE_SERVER_PLAYER_FIRST_LOGON_AFTER_CBG_TRADE,
                          (owner.roleName,),
                          1,
                          0)))
            if gameconfig.enableFTB():
                owner.ftbFirstLogonAfterTrade()
            if gameconfig.enableNewPlayerTreasureBox():
                from data import sys_config_data as SCD
                owner.cell.tryToSignNewPlayerFlag(gametypes.NT_FLAG_CBG, SCD.data.get('ntRatios', {}).get('ntCBGRatio', 0))

        def _doOnLogon(self, owner):
            if self.saleStatus == gametypes.ROLE_SALE_STATUS_REGISTER:
                totalRemainSecs = const.SECONDS_PER_DAY * (CCD.data.get('roleSaleRegisterDays', 0) + CCD.data.get('roleSaleCanPutOnSaleDays', 0)) - (utils.getNow() - self.saleStatusTime)
                registerRemainSecs = const.SECONDS_PER_DAY * CCD.data.get('roleSaleRegisterDays', 0) - (utils.getNow() - self.saleStatusTime)
                if totalRemainSecs <= 0:
                    self.unRegister(owner, bySys=True)
                else:
                    self._setUnRegisterTimer(owner)
                    if registerRemainSecs <= 0:
                        owner._callback(12, '_delaySendCbgMsg', (GMDD.data.CBG_ROLE_CAN_PUT_ON_SALE, ()))
                    else:
                        remainSeconds = max(0, self.saleStatusTime + CCD.data.get('roleSaleRegisterDays', 0) * const.SECONDS_PER_DAY - utils.getNow() - 12)
                        remainDays = int(remainSeconds // const.SECONDS_PER_DAY)
                        remainHours = int(remainSeconds % const.SECONDS_PER_DAY / const.SECONDS_PER_HOUR)
                        remainMins = int(remainSeconds % const.SECONDS_PER_HOUR / const.SECONDS_PER_MIN)
                        remainSecs = int(remainSeconds % const.SECONDS_PER_MIN)
                        owner._callback(12, '_delaySendCbgMsg', (GMDD.data.CBG_ROLE_REGISTER_COUNT_DOWN, (remainDays,
                          remainHours,
                          remainMins,
                          remainSecs)))
                        self._setCanPutOnSaleTimer(owner)
            if self.newSaleFlag:
                lastTime = max(0, CCD.data.get('roleSaleMarkFlagTime', 0) - (utils.getNow() - self.newSaleFlagStartTime))
                if lastTime <= 0:
                    self.newSaleFlag = 0
                    self.newSaleFlagStartTime = 0
                else:
                    self.newSaleFlagTimer = owner._callback(lastTime, '_onNewSaleRoleFlagTTL', ())
                    if gameconfig.enableCBGRoleAward():
                        if self.salePrice and self.salePrice >= CCD.data.get('roleSaleAuraPriceThresholdYuan', const.MAX_UINT32) * 100:
                            owner.cell.addAuraByNewSaleRole(self.newSaleFlagStartTime)
                            stId = CCD.data.get('roleSaleMarkFlagStateId', 0)
                            stId and owner.cell.addState(stId, 1, -1, gametypes.ADD_STATE_FROM_CBG, 0, 0)

        def onNewSaleFlagTTL(self, owner):
            self.newSaleFlag = 0
            self.newSaleFlagStartTime = 0
            self.newSaleFlagTimer = 0
            owner.cell.removeAuraByNewSaleRole()
            stId = CCD.data.get('roleSaleMarkFlagStateId', 0)
            owner.cell.removeState(stId, gametypes.REMOVE_STATE_BY_NORMAL)

        def register(self, owner):
            self.changeToStatus(gametypes.ROLE_SALE_STATUS_REGISTER)
            self.setIp(owner.account.realIp)
            self.transfer(owner)
            serverlog.genCBGRoleRegisterLog(owner, gameconst.CBG_REGISTER)
            self._setUnRegisterTimer(owner)

        def _setUnRegisterTimer(self, owner):
            self._cancelUnRegisterTimer(owner)
            if self.saleStatus == gametypes.ROLE_SALE_STATUS_REGISTER:
                totalRemainSecs = const.SECONDS_PER_DAY * (CCD.data.get('roleSaleRegisterDays', 0) + CCD.data.get('roleSaleCanPutOnSaleDays', 0)) - (utils.getNow() - self.saleStatusTime)
                if totalRemainSecs >= 0:
                    self.autoUnRegisterTimer = owner._callback(totalRemainSecs, '_autoUnRegisterSaleRole', ())

        def _cancelUnRegisterTimer(self, owner):
            owner._cancelCallback(self.autoUnRegisterTimer)
            self.autoUnRegisterTimer = 0

        def _setCanPutOnSaleTimer(self, owner):
            self._cancelCanPutOnSaleTimer(owner)
            if self.saleStatus == gametypes.ROLE_SALE_STATUS_REGISTER:
                remainSeconds = max(0, self.saleStatusTime + CCD.data.get('roleSaleRegisterDays', 0) * const.SECONDS_PER_DAY - utils.getNow())
                if remainSeconds >= 0:
                    self.canPutOnSaleTimer = owner._callback(remainSeconds, '_onCanPutOnSale', ())

        def _cancelCanPutOnSaleTimer(self, owner):
            owner._cancelCallback(self.canPutOnSaleTimer)
            self.canPutOnSaleTimer = 0

        def _onCanPutOnSale(self, owner):
            owner.client.showGameMsg(GMDD.data.CBG_ROLE_CAN_PUT_ON_SALE, ())
            self._cancelCanPutOnSaleTimer(owner)

        def unRegister(self, owner, bySys = False):
            if self.saleStatus != gametypes.ROLE_SALE_STATUS_REGISTER:
                self._cancelUnRegisterTimer(owner)
                self._cancelCanPutOnSaleTimer(owner)
                gameengine.reportCritical('unRegister saleStatus %d %d', self.saleStatus, owner.gbID)
                return
            self.changeToStatus(gametypes.ROLE_SALE_STATUS_DEFAULT)
            self.transfer(owner)
            owner.client.onApplyUnRegisterSaleRole(True)
            serverlog.genCBGRoleRegisterLog(owner, gameconst.CBG_UNREGISTER if not bySys else gameconst.CBG_UNREGISTER_BY_SYS)
            self._cancelUnRegisterTimer(owner)
            self._cancelCanPutOnSaleTimer(owner)

        def putOnSale(self, owner, price, tLong, vendeeGbId, orderSn):
            self.changeToStatus(gametypes.ROLE_SALE_STATUS_ONSALE)
            serverlog.genCBGRolePutOnSaleLog(owner, price, tLong, vendeeGbId, orderSn)
            self._cancelUnRegisterTimer(owner)
            self._cancelCanPutOnSaleTimer(owner)
