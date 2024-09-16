#Embedded file name: I:/bag/tmp/tw2/res/entities\common/wingWorldYabiao.o
import const
import gametypes
import utils
import wingWorldUtils
import gamelog
from data import wing_world_config_data as WWCD
from cdata import game_msg_def_data as GMDD
from userDictType import UserDictType

class WingWorldYabiaoData(UserDictType):

    def __init__(self, yabiaoZaijuOwnerGbId = 0, yabiaoGuildNUID = 0, yabiaoNUID = 0, yabiaoCurrHostId = 0, yabiaoBeginTime = 0, yabiaoBrokenBeginTime = 0, yabiaoRemainTime = 0, yabiaoDakaSeq = None, yabiaoBrokenDakaFlag = False, yabiaoLastUpgradeTime = 0, yabiaoPostion = None, yabiaoSpaceNo = 0, yabiaoZaijuHp = 0, yabiaoZaijuMaxHp = 0, zaijuInvincibleEndTime = 0, yabiaoDestination = 0, yabiaoEntId = 0):
        self.yabiaoZaijuOwnerGbId = yabiaoZaijuOwnerGbId
        self.yabiaoGuildNUID = yabiaoGuildNUID
        self.yabiaoNUID = yabiaoNUID
        self.yabiaoCurrHostId = yabiaoCurrHostId
        self.yabiaoBeginTime = yabiaoBeginTime
        self.yabiaoBrokenBeginTime = yabiaoBrokenBeginTime
        self.yabiaoRemainTime = yabiaoRemainTime
        if yabiaoDakaSeq is None:
            yabiaoDakaSeq = [0] * const.WING_WORLD_YABIAO_DAKA_TOTAL_COUNT
        self.yabiaoDakaSeq = yabiaoDakaSeq
        self.yabiaoBrokenDakaFlag = yabiaoBrokenDakaFlag
        self.yabiaoLastUpgradeTime = yabiaoLastUpgradeTime
        self.yabiaoPostion = yabiaoPostion
        self.yabiaoSpaceNo = yabiaoSpaceNo
        self.yabiaoZaijuHp = yabiaoZaijuHp
        self.yabiaoZaijuMaxHp = yabiaoZaijuMaxHp
        self.zaijuInvincibleEndTime = zaijuInvincibleEndTime
        self.yabiaoDestination = yabiaoDestination
        self.yabiaoEntId = yabiaoEntId
        super(WingWorldYabiaoData, self).__init__()

    def resetAll(self):
        gamelog.debug('cgy#wingWorldYabiaoData resetAll')
        self.yabiaoZaijuOwnerGbId = 0
        self.yabiaoGuildNUID = 0
        self.yabiaoNUID = 0
        self.yabiaoCurrHostId = 0
        self.yabiaoBeginTime = 0
        self.yabiaoBrokenBeginTime = 0
        self.yabiaoRemainTime = 0
        self.yabiaoDakaSeq = [0] * const.WING_WORLD_YABIAO_DAKA_TOTAL_COUNT
        self.yabiaoBrokenDakaFlag = False
        self.yabiaoLastUpgradeTime = 0
        self.yabiaoPostion = None
        self.yabiaoSpaceNo = 0
        self.yabiaoZaijuHp = 0
        self.yabiaoZaijuMaxHp = 0
        self.zaijuInvincibleEndTime = 0
        self.yabiaoDestination = 0
        self.yabiaoEntId = 0
        self.clear()

    def carryRes(self, item2Num):
        self.update(item2Num)

    def getCarryRes(self):
        res = [0] * gametypes.WING_RESOURCE_TYPE_COUNT
        for i, v in enumerate(range(gametypes.WING_RESOURCE_TYPE_COUNT)):
            res[i] = self.get(i, 0)

        return res

    def getUpgradeLevel(self):
        level = 0
        for v in self.yabiaoDakaSeq:
            if v:
                level += 1

        return level

    def isYabiaoRunning(self):
        return bool(self.yabiaoNUID)

    def setYabiaoZaijuBroken(self):
        if self.yabiaoBrokenBeginTime:
            gamelog.error('cgy#setYabiaoZaijuBroken again: ', self.yabiaoBrokenBeginTime, self.yabiaoGuildNUID)
            return 0
        self.yabiaoBrokenBeginTime = utils.getNow()
        lossResPercent = WWCD.data.get('yabiaoBorkenLossResPercent', 0.1)
        res = self.getCarryRes()
        realUnit = wingWorldUtils.getRealUnitViaYabiaoResValue(res[0])
        lostUnit = int(round(realUnit * lossResPercent))
        remainUnit = realUnit - lostUnit
        gamelog.info('cgy#setYabiaoZaijuBroken: ', self.yabiaoGuildNUID, self.yabiaoNUID, self.yabiaoCurrHostId, res[0], realUnit, lostUnit, remainUnit)
        for i, v in enumerate(range(gametypes.WING_RESOURCE_TYPE_COUNT)):
            self[i] = wingWorldUtils.getYabiaoResValueViaRealUnit(remainUnit)

        return lostUnit

    def isBroken(self):
        return bool(self.yabiaoBrokenBeginTime)

    def getWingWorldYabiaoRemainTime(self):
        if self.yabiaoBrokenBeginTime:
            beginTime = self.yabiaoBrokenBeginTime
            dura = self.getWingWorldYabiaoBrokenDura()
        else:
            beginTime = self.yabiaoBeginTime
            dura = self.getWingWorldYabiaoDura()
        goneTime = utils.getNow() - beginTime
        return max(0, dura - goneTime)

    def getWingWorldYabiaoDura(self):
        return WWCD.data.get('wingWorldYabiaoDura', 1200)

    def getWingWorldYabiaoBrokenDura(self):
        return WWCD.data.get('yabiaoZaijuInvincibleDura', 600)

    def getYabiaoZaijuNo(self):
        return wingWorldUtils.getYabiaoZaijuNo(self.yabiaoBrokenBeginTime)

    def __repr__(self):
        return 'gbId:{}, gnuid:{}, nuid: {} begin:{}, brokenFlag:{}, brokenBegin:{}, upgradeseq:{}, carryRes{}, pos:{}, spaceNo:{}, hostId: {}, dest: {}'.format(self.yabiaoZaijuOwnerGbId, self.yabiaoGuildNUID, self.yabiaoNUID, self.yabiaoBeginTime, self.yabiaoBrokenDakaFlag, self.yabiaoBrokenBeginTime, self.yabiaoDakaSeq, self.items(), self.yabiaoPostion, self.yabiaoSpaceNo, self.yabiaoCurrHostId, self.yabiaoDestination)

    __str__ = __repr__
