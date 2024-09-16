#Embedded file name: /WORKSPACE/data/entities/common/equipment.o
import BigWorld
import random
import const
import copy
import gametypes
import item
import utils
from userListType import UserListType
from data import equip_data as ED
from const import EQUIP_PART_NUM, CONT_EMPTY_VAL
from pickledItem import PickledItem
from formula import calcCombatScoreType
from data import zaiju_data as ZJD
from data import school_switch_general_data as SSGD
from cdata import equip_suits_data as ESD
from data import sys_config_data as SCD
from cdata import yaopei_lv_data as YLD
from cdata import equip_star_factor_data as ESFD
from cdata import equip_quality_factor_data as EQFD
from cdata import equip_order_factor_data as EOFD
from cdata import equip_enhance_prop_data as EEPD
from data import horsewing_upgrade_data as HWUD
from cdata import equip_enhance_juexing_prop_data as EEJPD
from data import equip_gem_data as EGD
if BigWorld.component in ('base', 'cell'):
    import gameconst
    import gameengine
    import gametimer
    import serverlog
    import Netease
    import logconst
    import gameconfig
    import commcalc
    from data import log_src_def_data as LSDD

class Equipment(UserListType):
    FASHION_PARTS_MAP = {'head': gametypes.EQU_PART_FASHION_HEAD,
     'body': gametypes.EQU_PART_FASHION_BODY,
     'shoe': gametypes.EQU_PART_FASHION_SHOE,
     'hand': gametypes.EQU_PART_FASHION_HAND,
     'leg': gametypes.EQU_PART_FASHION_LEG,
     'cape': gametypes.EQU_PART_FASHION_CAPE,
     'head2': gametypes.EQU_PART_FASHION_HEAD,
     'head1': gametypes.EQU_PART_FASHION_HEAD,
     'headdress': gametypes.EQU_PART_HEADWEAR,
     'headdressRight': gametypes.EQU_PART_HEADWEAR_RIGHT,
     'headdressLeft': gametypes.EQU_PART_HEADWEAR_LFET,
     'facewear': gametypes.EQU_PART_FACEWEAR,
     'waistwear': gametypes.EQU_PART_WAISTWEAR,
     'backwear': gametypes.EQU_PART_BACKWEAR,
     'tailwear': gametypes.EQU_PART_TAILWEAR,
     'chestwear': gametypes.EQU_PART_CHESTWEAR,
     'earwear': gametypes.EQU_PART_EARWEAR,
     'neiyi': gametypes.EQU_PART_FASHION_NEIYI,
     'neiku': gametypes.EQU_PART_FASHION_NEIKU,
     'footdust': gametypes.EQU_PART_FOOT_DUST}
    FASHION_PARTS = (gametypes.EQU_PART_FASHION_BODY,
     gametypes.EQU_PART_FASHION_SHOE,
     gametypes.EQU_PART_FASHION_HAND,
     gametypes.EQU_PART_FASHION_LEG,
     gametypes.EQU_PART_FASHION_NEIYI,
     gametypes.EQU_PART_FASHION_NEIKU,
     gametypes.EQU_PART_FOOT_DUST,
     gametypes.EQU_PART_FASHION_CAPE)
    FASHION_WEAPON_PARTS = (gametypes.EQU_PART_FASHION_WEAPON_ZHUSHOU, gametypes.EQU_PART_FASHION_WEAPON_FUSHOU)
    ALL_FASHION_PARTS = FASHION_PARTS
    WEAPON_MUTEX_PARTS = (gametypes.EQU_PART_WAISTWEAR, gametypes.EQU_PART_BACKWEAR)

    def __init__(self):
        super(Equipment, self).__init__()
        self.extend([ CONT_EMPTY_VAL for x in xrange(EQUIP_PART_NUM) ])
        self.version = 0
        self.freeze = 0
        self.suit = {}
        self.opstr = ''
        self.locker = 0
        self.state = 0

    def _lateReload(self):
        super(Equipment, self)._lateReload()
        for part in xrange(len(self)):
            if self.isInvalid(part):
                continue
            if self.isEmpty(part):
                continue
            self[part].reloadScript()

    def _isValidPart(self, part):
        if 0 <= part < EQUIP_PART_NUM:
            return True
        return False

    def consistent(self):
        if not hasattr(self, 'version'):
            return False
        currVer = item.Item.TIMESTAMP
        if self.version == currVer:
            return False
        for part in self.getPartTuple():
            it = self.get(part)
            if it == CONT_EMPTY_VAL:
                continue
            it.consistent()

        self.version = currVer
        return True

    def isInvalid(self, part):
        if 0 <= part < EQUIP_PART_NUM:
            return False
        return True

    def noEquip(self):
        for i in self:
            if i != CONT_EMPTY_VAL:
                return False

        return True

    def isEmpty(self, part):
        return self[part] == CONT_EMPTY_VAL

    def isFill(self, part):
        return not self.isEmpty(part)

    def refuseChangeEquip(self, owner):
        if owner._isOnZaijuOrBianyao():
            zaijuNo = owner._getZaijuOrBianyaoNo()
            return ZJD.data[zaijuNo].get('isEquipLock', 0) > 0
        elif owner._isSchoolSwitch():
            switchNo = owner._getSchoolSwitchNo()
            return SSGD.data[switchNo].get('isEquipLock', 0) > 0
        else:
            return False

    def isRefuse(self, owner):
        if self.refuseChangeEquip(owner):
            return True
        if self.isLock():
            return True
        if self.freeze != 0:
            return True
        return False

    def isLock(self):
        return self.state == 1

    def lock(self, owner, opstr = '', lastout = const.CONT_INTERVAL_LOCK):
        if self.state == 1:
            try:
                gameengine.reportCritical('Verify Equipment lock twice:%d, %s, %s-->%s' % (owner.id,
                 owner.playerName,
                 self.opstr,
                 opstr))
            except:
                pass

        self.state = 1
        self.opstr = opstr
        self.locker = owner.addTimer(lastout, 0, gametimer.TIMER_EQUIPMENT_LOCK)

    def unlock(self, owner, opstr = ''):
        if self.state == 0:
            try:
                gameengine.reportCritical('Verify Equipment unlock twice:%d, %s, %s-->%s' % (owner.id,
                 owner.playerName,
                 self.opstr,
                 opstr))
            except:
                pass

            return
        if self.opstr != opstr:
            if opstr == 'timer':
                pass
            else:
                try:
                    gameengine.reportCritical('Verify Equipment unlock inconsistent:%d, %s, %s-->%s' % (owner.id,
                     owner.playerName,
                     self.opstr,
                     opstr))
                except:
                    pass

        self.state = 0
        self.opstr = ''
        owner.delTimer(self.locker)
        self.locker = 0

    def getPartTuple(self):
        parts = []
        for part in xrange(len(self)):
            if self._isValidPart(part):
                parts.append(part)

        return parts

    def _reportCritical(self, part, obj):
        if BigWorld.component in ('base', 'cell'):
            import gameengine
            gameengine.reportCritical('Verify in Equip(%d):%d(%s,%s),%d(%d)' % (part,
             obj.id,
             obj.name,
             obj.guid(),
             obj.cwrap,
             obj.mwrap))

    def verifyObj(self, part):
        obj = self[part]
        if not obj:
            return
        if obj.cwrap <= 0 or obj.cwrap > obj.mwrap:
            self._reportCritical(part, obj)

    def get(self, part, changeToItem = True):
        try:
            it = self[part]
            if it.__class__ is PickledItem and changeToItem:
                it.changeToItem()
            return it
        except IndexError:
            return CONT_EMPTY_VAL

    def set(self, part, e = CONT_EMPTY_VAL):
        if not self._isValidPart(part):
            return False
        self[part] = e
        self.verifyObj(part)
        return True

    def move(self, srcPart, dstPart):
        if not self._isValidPart(srcPart):
            return False
        if not self.isEmpty(dstPart):
            return False
        self[dstPart] = self[srcPart]
        self[srcPart] = CONT_EMPTY_VAL
        return True

    def isEquip(self, tp, stp):
        equiped = False
        for part in xrange(EQUIP_PART_NUM):
            equ = self[part]
            if equ != CONT_EMPTY_VAL and equ.type == tp and equ.stype == stp:
                equiped = True
                break

        return equiped

    def calcAllEquipScore(self, suitsCache = None):
        sum = 0
        for part in xrange(EQUIP_PART_NUM):
            it = self[part]
            if it == CONT_EMPTY_VAL:
                continue
            if it.isExpireTTL():
                continue
            if hasattr(it, 'score'):
                sum += it.score

        if suitsCache:
            ignoreSuitIds = utils.equipSuitIgnoreSuits(suitsCache)
            for suiteId, suiteNum in suitsCache.iteritems():
                if suiteId in ignoreSuitIds:
                    continue
                suitData = ESD.data.get(suiteId, {})
                for num, sData in suitData.iteritems():
                    if num <= suiteNum:
                        sum += sData.get('suitScore', 0)

        return int(sum)

    def calcAllEquipScoreType(self, suitsCache = None):
        addTypes = []
        for part in xrange(EQUIP_PART_NUM):
            it = self[part]
            if it == CONT_EMPTY_VAL:
                continue
            if it.isExpireTTL():
                continue
            if hasattr(it, 'scoreType'):
                addTypes.append(it.scoreType)

        sumType = calcCombatScoreType([], [], addTypes, 0, const.COMBAT_SCORE_TYPE_OP_ADD)
        if suitsCache:
            ignoreSuitIds = utils.equipSuitIgnoreSuits(suitsCache)
            for suiteId, suiteNum in suitsCache.iteritems():
                if suiteId in ignoreSuitIds:
                    continue
                suitData = ESD.data.get(suiteId, {})
                for num, sData in suitData.iteritems():
                    if num <= suiteNum:
                        sumType = calcCombatScoreType(sumType, sData.get('suitScoreType', []), [], sData.get('suitScore', 0), const.COMBAT_SCORE_TYPE_OP_COEFF)

        return sumType

    def calcAllAttrSum(self, attr):
        sum = 0
        for part in xrange(EQUIP_PART_NUM):
            it = self[part]
            if it == CONT_EMPTY_VAL:
                continue
            if it.isExpireTTL():
                continue
            if hasattr(it, attr):
                sum += getattr(it, attr) * it.cwrap

        return sum

    def calcPanelAttrSum(self, attr):
        sum = 0
        for part in xrange(EQUIP_PART_NUM):
            it = self[part]
            if it == CONT_EMPTY_VAL:
                continue
            if it.isExpireTTL():
                continue
            if hasattr(it, attr):
                sum += getattr(it, attr) * it.cwrap

        return sum

    def countBlank(self):
        cnt = 0
        for part in xrange(len(self)):
            if self.isEmpty(part):
                cnt += 1

        return cnt

    def countAllObj(self):
        cnt = 0
        for part in xrange(len(self)):
            if self.isEmpty(part):
                continue
            cnt += 1

        return cnt

    def countNum(self):
        cnt = 0
        for part in xrange(len(self)):
            if not self.isEmpty(part):
                cnt += 1

        return cnt

    def randomGet(self, good = False):
        items = []
        for part, it in enumerate(self):
            if it:
                if good and it.isWaster():
                    continue
                items.append((part, it))

        if len(items) > 0:
            return random.choice(items)
        else:
            return (const.CONT_NO_POS, CONT_EMPTY_VAL)

    def findItemByAttr(self, attr):
        for part, it in enumerate(self):
            it = self.get(part)
            if it == CONT_EMPTY_VAL:
                continue
            for k, v in attr.iteritems():
                if not hasattr(it, k):
                    break
                if getattr(it, k) != v:
                    break
            else:
                return part

        return const.CONT_NO_POS

    def calcPanelGemAttrSum(self, attr, owner):
        if gameconfig.enableSplitWenYinFromEquip():
            return self._calcPanelGemAttrSumWY(attr, owner)
        else:
            return self._calcPanelGemAttrSum(attr)

    def _calcPanelGemAttrSum(self, attr):
        yinSum = 0
        yangSum = 0
        for part in xrange(EQUIP_PART_NUM):
            it = self[part]
            if it == CONT_EMPTY_VAL:
                continue
            if it.isExpireTTL():
                continue
            yinSlots = getattr(it, 'yinSlots', [])
            for gemSlot in yinSlots:
                if not gemSlot or not gemSlot.gem:
                    continue
                gemData = utils.getEquipGemData(gemSlot.gem.id)
                gemAttr = gemData.get(attr, 0)
                yinSum += gemAttr

            yangSlots = getattr(it, 'yangSlots', [])
            for gemSlot in yangSlots:
                if not gemSlot or not gemSlot.gem:
                    continue
                gemData = utils.getEquipGemData(gemSlot.gem.id)
                gemAttr = gemData.get(attr, 0)
                yangSum += gemAttr

        return (yinSum, yangSum)

    def _calcPanelGemAttrSumWY(self, attr, owner):
        yinSum = 0
        yangSum = 0
        for part in xrange(EQUIP_PART_NUM):
            it = self[part]
            if it == CONT_EMPTY_VAL:
                continue
            if it.isExpireTTL():
                continue
            wyIt = owner.wenYin.getWYSlots(part)
            if not wyIt:
                continue
            yinSlots = getattr(it, 'yinSlots', [])
            for gemSlot in yinSlots:
                if not gemSlot or not gemSlot.isEmpty():
                    continue
                wySlot = wyIt.yinSlots[gemSlot.pos]
                if not wySlot.isFilled():
                    continue
                gemData = utils.getEquipGemData(wySlot.gem.id)
                if it.addedOrder >= gemData.get('orderLimit', 0):
                    yinSum += gemData.get(attr, 0)
                elif gameconfig.enableLessLvWenYin():
                    lessGemId = utils.getLessLvWenYinGemId(it.addedOrder, gemData)
                    if lessGemId:
                        yinSum += EGD.data.get(lessGemId, {}).get(attr, 0)

            yangSlots = getattr(it, 'yangSlots', [])
            for gemSlot in yangSlots:
                if not gemSlot or not gemSlot.isEmpty():
                    continue
                wySlot = wyIt.yangSlots[gemSlot.pos]
                if not wySlot.isFilled():
                    continue
                gemData = utils.getEquipGemData(wySlot.gem.id)
                if it.addedOrder >= gemData.get('orderLimit', 0):
                    yangSum += gemData.get(attr, 0)
                elif gameconfig.enableLessLvWenYin():
                    lessGemId = utils.getLessLvWenYinGemId(it.addedOrder, gemData)
                    if lessGemId:
                        yangSum += EGD.data.get(lessGemId, {}).get(attr, 0)

        return (yinSum, yangSum)

    @staticmethod
    def _applyEquipPropsList(owner, equip, propsName, param):
        if hasattr(equip, propsName):
            propsList = getattr(equip, propsName, [])
            for prop, type, value in propsList:
                owner.combatProp.addPretreatProp(owner, prop, type, value * param)

    @staticmethod
    def applyEquip(owner, equip):
        if not owner._isValidPropSrc(gameconst.AVATAR_PROP_SRC_EQUIP):
            return
        if not gameconfig.enableNewPropCalc():
            return
        if not commcalc.validEquipOnCalcProp(owner, equip):
            return
        if owner.combatProp.effective_equip.has_key(equip.uuid):
            return
        isYaoPei = equip.isYaoPei()
        if isYaoPei and BigWorld.component in ('base', 'cell') and not gameconfig.enableYaoPei():
            return
        starFactor = ESFD.data.get(equip.addedStarLv, {}).get('factor', 1.0)
        qualityFactor = EQFD.data.get(equip.quality, {}).get('factor', 1.0)
        ypLv = 0
        if isYaoPei:
            ypLv = equip.getYaoPeiLv()
            if gameconfig.enableRebalance() and owner.rebalancing:
                methodID, factor = owner.getMethodFactorByModeID(gametypes.REBALANCE_SUBSYS_ID_HSF, owner.rebalanceMode)
                if methodID:
                    ypLv = min(ypLv, factor)
            ypd = YLD.data.get(ypLv, {})
        if isYaoPei:
            basicAdd = ypd.get('basicAdd', 1)
            Equipment._applyEquipPropsList(owner, equip, 'yaoPeiProps', basicAdd)
        else:
            Equipment._applyEquipPropsList(owner, equip, 'props', starFactor * qualityFactor)
        Equipment._applyEquipPropsList(owner, equip, 'fixedProps', starFactor * qualityFactor)
        if isYaoPei:
            extraAdd = ypd.get('extraAdd', 1)
            for prop, type, val, _, _, lv in getattr(equip, 'yaoPeiExtraProps', []):
                if ypLv >= lv:
                    owner.combatProp.addPretreatProp(owner, prop, type, val * extraAdd)

        else:
            Equipment._applyEquipPropsList(owner, equip, 'extraProps', starFactor * qualityFactor)
        if isYaoPei:
            extraAdd = ypd.get('extraAdd', 1)
            Equipment._applyEquipPropsList(owner, equip, 'rprops', extraAdd)
        elif not gameconfig.enableNewLv89():
            Equipment._applyEquipPropsList(owner, equip, 'rprops', starFactor * qualityFactor)
        else:
            param = equip.isSesMaker(owner.gbId)
            Equipment._applyEquipPropsList(owner, equip, 'rprops', (param + starFactor) * qualityFactor)
        orderFactor = EOFD.data.get(equip.addedOrder, {}).get('factor', 1.0)
        _, part = owner.realEquipment.findEquipByUUID(equip.uuid)
        enhCalcData = commcalc.getEquipShareEnhProp(owner, equip, commcalc.getAlternativeEquip(owner, part))
        if commcalc.enableShareEquipProp(owner) and enhCalcData:
            enhLv = enhCalcData['enhLv']
            maxEnhlv = enhCalcData['maxEnhlv']
            enhanceRefining = enhCalcData['enhanceRefining']
            equipType = enhCalcData['equipType']
            equipSType = enhCalcData['equipSType']
            enhanceType = enhCalcData['enhanceType']
        else:
            enhLv = getattr(equip, 'enhLv', 0)
            maxEnhlv = equip.getMaxEnhLv(owner)
            enhanceRefining = getattr(equip, 'enhanceRefining', {})
            equipType = equip.equipType
            equipSType = equip.equipSType
            enhanceType = equip.enhanceType
        if owner.rebalancing and gameconfig.enableRebalance():
            methodID, factor = owner.getMethodFactorByModeID(gametypes.REBALANCE_SUBSYS_ID_QH, owner.rebalanceMode)
            if methodID:
                maxEnhlv = min(maxEnhlv, factor)
        refiningFactor = 0
        tEnhLv = min(maxEnhlv, enhLv)
        if enhanceRefining:
            for elv, enh in enhanceRefining.items():
                if elv <= tEnhLv:
                    refiningFactor += enh

        enhanceData = EEPD.data.get((equipType, equipSType, enhanceType))
        if enhanceData:
            for prop, type, value in enhanceData.get('enhProps', []):
                owner.combatProp.addPretreatProp(owner, prop, type, value * orderFactor * refiningFactor)

        if commcalc.enableShareEquipProp(owner) and enhCalcData:
            enhJuexingNoAddData = enhCalcData['enhJuexingData']
            enhJuexingAddRatio = enhCalcData['enhJuexingAddRatio']
        else:
            enhJuexingNoAddData = getattr(equip, 'enhJuexingData', {})
            enhJuexingAddRatio = getattr(equip, 'enhJuexingAddRatio', {})
        enhJuexingData = commcalc.applyEnhJuexingAddData(enhJuexingNoAddData, enhJuexingAddRatio, maxEnhlv)
        if enhJuexingData:
            refiningStar = equip.getEquipRefiningStar()
            for eLv, jxData in enhJuexingData.items():
                if eLv > tEnhLv:
                    continue
                juexingDataList = utils.getEquipEnhJuexingPropData(equipType, equipSType, eLv, enhanceType)
                for prop, type, value in jxData:
                    if prop not in juexingDataList:
                        continue
                    owner.combatProp.addPretreatProp(owner, prop, type, value * refiningStar)

        Equipment._applyEquipPropsList(owner, equip, 'preprops', starFactor * qualityFactor)
        for prop, type, value in equip.getGemProps(owner):
            if not gameconfig.enableNewLv89():
                owner.combatProp.addPretreatProp(owner, prop, type, value)
            else:
                wenYinEnh = equip.isSesWenYinEnh()
                owner.combatProp.addPretreatProp(owner, prop, type, value * (1 + wenYinEnh))

        if equip.isWingOrRide():
            ridewing_quality = equip.quality
            ridewing_type = equip.getVehicleType()
            ridewing_stage = getattr(equip, 'rideWingStage', None)
            if utils.isRideWingShareEpRegenEnabled():
                if part == gametypes.EQU_PART_RIDE and owner.sharedRideAttr.itemId > 0 and owner.hasSharedRideMaxSpeed():
                    ridewing_quality = owner.sharedRideAttr.quality
                    ridewing_type = owner.sharedRideAttr.equipType
                    ridewing_stage = owner.sharedRideAttr.rideWingStage
                elif part == gametypes.EQU_PART_WINGFLY and owner.sharedWingAttr.itemId > 0 and owner.hasSharedWingMaxSpeed():
                    ridewing_quality = owner.sharedWingAttr.quality
                    ridewing_type = owner.sharedWingAttr.equipType
                    ridewing_stage = owner.sharedWingAttr.rideWingStage
            if ridewing_stage is not None:
                hwud = HWUD.data.get((ridewing_quality, ridewing_type, ridewing_stage))
                if hwud:
                    for prop, type, value in hwud.get('props', []):
                        owner.combatProp.addPretreatProp(owner, prop, type, value)

        owner.combatProp.effective_equip[equip.uuid] = True

    @staticmethod
    def _unApplyEquipPropsList(owner, equip, propsName, param):
        if hasattr(equip, propsName):
            propsList = getattr(equip, propsName, [])
            for prop, type, value in propsList:
                owner.combatProp.removePretreatProp(owner, prop, type, value * param)

    @staticmethod
    def unApplyEquip(owner, equip):
        if not gameconfig.enableNewPropCalc():
            return
        if not owner.combatProp.effective_equip.has_key(equip.uuid):
            return
        starFactor = ESFD.data.get(equip.addedStarLv, {}).get('factor', 1.0)
        qualityFactor = EQFD.data.get(equip.quality, {}).get('factor', 1.0)
        if equip.isYaoPei():
            ypd = YLD.data.get(equip.getYaoPeiLv(), {})
        if equip.isYaoPei():
            basicAdd = ypd.get('basicAdd', 1)
            Equipment._unApplyEquipPropsList(owner, equip, 'yaoPeiProps', basicAdd)
        else:
            Equipment._unApplyEquipPropsList(owner, equip, 'props', starFactor * qualityFactor)
        Equipment._unApplyEquipPropsList(owner, equip, 'fixedProps', starFactor * qualityFactor)
        if equip.isYaoPei():
            extraAdd = ypd.get('extraAdd', 1)
            ypLv = equip.getYaoPeiLv()
            for prop, type, val, _, _, lv in getattr(equip, 'yaoPeiExtraProps', []):
                if ypLv >= lv:
                    owner.combatProp.removePretreatProp(owner, prop, type, val * extraAdd)

        else:
            Equipment._unApplyEquipPropsList(owner, equip, 'extraProps', starFactor * qualityFactor)
        if equip.isYaoPei():
            extraAdd = ypd.get('extraAdd', 1)
            Equipment._unApplyEquipPropsList(owner, equip, 'rprops', extraAdd)
        elif not gameconfig.enableNewLv89():
            Equipment._unApplyEquipPropsList(owner, equip, 'rprops', starFactor * qualityFactor)
        else:
            param = equip.isSesMaker(owner.gbId)
            Equipment._unApplyEquipPropsList(owner, equip, 'rprops', (starFactor + param) * qualityFactor)
        orderFactor = EOFD.data.get(equip.addedOrder, {}).get('factor', 1.0)
        _, part = owner.realEquipment.findEquipByUUID(equip.uuid)
        enhCalcData = commcalc.getEquipShareEnhProp(owner, equip, commcalc.getAlternativeEquip(owner, part))
        if commcalc.enableShareEquipProp(owner) and enhCalcData:
            enhLv = enhCalcData['enhLv']
            maxEnhlv = enhCalcData['maxEnhlv']
            enhanceRefining = enhCalcData['enhanceRefining']
            equipType = enhCalcData['equipType']
            equipSType = enhCalcData['equipSType']
            enhanceType = enhCalcData['enhanceType']
        else:
            enhLv = getattr(equip, 'enhLv', 0)
            maxEnhlv = equip.getMaxEnhLv(owner)
            enhanceRefining = getattr(equip, 'enhanceRefining', {})
            equipType = equip.equipType
            equipSType = equip.equipSType
            enhanceType = equip.enhanceType
        refiningFactor = 0
        tEnhLv = min(maxEnhlv, enhLv)
        if enhanceRefining:
            for elv, enh in enhanceRefining.items():
                if elv <= tEnhLv:
                    refiningFactor += enh

        enhanceData = EEPD.data.get((equipType, equipSType, enhanceType))
        if enhanceData:
            for prop, type, value in enhanceData.get('enhProps', []):
                owner.combatProp.removePretreatProp(owner, prop, type, value * orderFactor * refiningFactor)

        if commcalc.enableShareEquipProp(owner) and enhCalcData:
            enhJuexingNoAddData = enhCalcData['enhJuexingData']
            enhJuexingAddRatio = enhCalcData['enhJuexingAddRatio']
        else:
            enhJuexingNoAddData = getattr(equip, 'enhJuexingData', {})
            enhJuexingAddRatio = getattr(equip, 'enhJuexingAddRatio', {})
        enhJuexingData = commcalc.applyEnhJuexingAddData(enhJuexingNoAddData, enhJuexingAddRatio, maxEnhlv)
        if enhJuexingData:
            refiningStar = equip.getEquipRefiningStar()
            if owner.rebalancing and gameconfig.enableRebalance():
                methodID, factor = owner.getMethodFactorByModeID(gametypes.REBALANCE_SUBSYS_ID_QHJX, owner.rebalanceMode)
                if methodID:
                    tEnhLv = min(tEnhLv, factor)
            for eLv, jxData in enhJuexingData.items():
                if eLv > tEnhLv:
                    continue
                juexingDataList = utils.getEquipEnhJuexingPropData(equipType, equipSType, eLv, enhanceType)
                for prop, type, value in jxData:
                    if prop not in juexingDataList:
                        continue
                    owner.combatProp.removePretreatProp(owner, prop, type, value * refiningStar)

        Equipment._unApplyEquipPropsList(owner, equip, 'preprops', starFactor * qualityFactor)
        for prop, type, value in equip.getGemProps(owner):
            if not gameconfig.enableNewLv89():
                owner.combatProp.removePretreatProp(owner, prop, type, value)
            else:
                wenYinEnh = equip.isSesWenYinEnh()
                owner.combatProp.removePretreatProp(owner, prop, type, value * (1 + wenYinEnh))

        if equip.isWingOrRide():
            ridewing_quality = equip.quality
            ridewing_type = equip.getVehicleType()
            ridewing_stage = getattr(equip, 'rideWingStage', None)
            if utils.isRideWingShareEpRegenEnabled():
                if part == gametypes.EQU_PART_RIDE and owner.sharedRideAttr.itemId > 0 and owner.hasSharedRideMaxSpeed():
                    ridewing_quality = owner.sharedRideAttr.quality
                    ridewing_type = owner.sharedRideAttr.equipType
                    ridewing_stage = owner.sharedRideAttr.rideWingStage
                elif part == gametypes.EQU_PART_WINGFLY and owner.sharedWingAttr.itemId > 0 and owner.hasSharedWingMaxSpeed():
                    ridewing_quality = owner.sharedWingAttr.quality
                    ridewing_type = owner.sharedWingAttr.equipType
                    ridewing_stage = owner.sharedWingAttr.rideWingStage
            if ridewing_stage is not None:
                hwud = HWUD.data.get((ridewing_quality, ridewing_type, ridewing_stage))
                if hwud:
                    for prop, type, value in hwud.get('props', []):
                        owner.combatProp.removePretreatProp(owner, prop, type, value)

        owner.combatProp.effective_equip.pop(equip.uuid)

    def equipItem(self, owner, part, it, strong = True, calcSuit = True, calcPskillCache = True):
        if self.isRefuse(owner):
            return False
        oldEquipIt = copy.deepcopy(self.get(part))
        equipIt = it.deepcopy()
        if it.isEquipBind():
            it.bindItem()
            if BigWorld.component in ('base', 'cell'):
                opNUID = Netease.getNUID()
                serverlog.genItemLog(owner, equipIt, 0, opNUID, LSDD.data.LOG_SRC_EQUIP_ITEM, detail=logconst.ITEM_EQUIP_BIND)
        self.set(part, it)
        owner._calcEquipEnhanceSuitCache()
        if hasattr(it, 'checkDyeMaterialsValidSelf'):
            it.checkDyeMaterialsValidSelf(owner)
        dyeList = getattr(it, 'dyeList', [])
        itemId = it.id
        if hasattr(it, 'rubbing') and it.rubbing:
            itemId = it.rubbing
        enhLv = getattr(it, 'rideWingStage', 0) if it.isWingOrRide() else it.getRealEnhlv(owner)
        owner.setAspect(part, itemId, dyeList, enhLv, getattr(it, 'rongGuang', []), useRealAspect=True)
        if part == gametypes.EQU_PART_WEAPON_ZHUSHOU:
            isSpecial = ED.data.get(it.id, {}).get('isSpecial', False)
            effId = SCD.data.get('wuHunEffect', {}).get(owner.school, 0)
            if isSpecial and effId and it.isPerfertRefined(owner):
                owner.setAspect(gametypes.EQU_PART_WUHUN, effId)
            else:
                owner.setAspect(gametypes.EQU_PART_WUHUN, 0)
        ed = ED.data.get(it.id)
        if ed and ed.get('equipType') == item.Item.EQUIP_BASETYPE_FASHION:
            slotParts = ed.get('slotParts', [])
            parts = ed.get('parts', [])
            autoParts = [ p for p in slotParts if p not in parts ]
            for p in autoParts:
                p = self.FASHION_PARTS_MAP.get(p, None)
                if p is not None:
                    owner.setAspect(p, it.id, dyeList, it.getRealEnhlv(owner), getattr(it, 'rongGuang', []), useRealAspect=True)

        if part in self.ALL_FASHION_PARTS:
            owner.setSignal(owner.id, gametypes.SIGNAL_SHOW_FASHION, 1)
        elif part in self.WEAPON_MUTEX_PARTS:
            owner.setSignal(owner.id, gametypes.SIGNAL_SHOW_BACK, 1)
        elif part in self.FASHION_WEAPON_PARTS:
            owner.setSignal(owner.id, gametypes.SIGNAL_SHOW_FASHION_WEAPON, 1)
        elif part == gametypes.EQU_PART_CAPE:
            owner._reCalcGuanYinEquipScoreEx(it)
        if it.isWingOrRide():
            it.recalcWingRideTalents(needCalcProps=not strong)
        owner.client.resSet(const.RES_KIND_EQUIP, it, 0, part)
        if oldEquipIt != CONT_EMPTY_VAL:
            Equipment.unApplyEquip(owner, oldEquipIt)
        Equipment.applyEquip(owner, it)
        if strong:
            if owner.rebalanced and owner.rebalancingDict.get(gametypes.REBALANCE_SUBSYS_ID_PROP, False):
                owner._recalcRebalancePROPFactor()
            else:
                owner.calcAllProp(gameconst.CALC_ALL_PROP_SRC_EQUIP)
        if calcSuit:
            owner.recalcEquipSuit(it, strong)
        owner.addPSkillByEquip(it, doCalc=strong, calcCache=calcPskillCache)
        owner.onQuestEquipment(it.id)
        if BigWorld.component in ('cell',):
            owner.onUseOrEquipAppearanceItem(it.id)
            owner.calcMaxEquipEnhanceVal()
        owner._refreshRefineSpecialEffect()
        owner._modifyRefineRoleName(it, const.RES_KIND_EQUIP, part)
        return True

    def enableEquipment(self, owner, part, it, strong = True):
        dyeList = getattr(it, 'dyeList', [])
        owner.setAspect(part, it.id, dyeList, it.getRealEnhlv(owner), getattr(it, 'rongGuang', []), useRealAspect=True)
        ed = ED.data.get(it.id)
        if ed and ed.get('equipType') == item.Item.EQUIP_BASETYPE_FASHION:
            slotParts = ed.get('slotParts', [])
            parts = ed.get('parts', [])
            autoParts = [ p for p in slotParts if p not in parts ]
            for p in autoParts:
                p = self.FASHION_PARTS_MAP.get(p, None)
                if p is not None:
                    owner.setAspect(p, it.id, dyeList, it.getRealEnhlv(owner), getattr(it, 'rongGuang', []), useRealAspect=True)

            if part in self.ALL_FASHION_PARTS:
                owner.setSignal(owner.id, gametypes.SIGNAL_SHOW_FASHION, 1)
            elif part in self.WEAPON_MUTEX_PARTS:
                owner.setSignal(owner.id, gametypes.SIGNAL_SHOW_BACK, 1)
            elif part in self.FASHION_WEAPON_PARTS:
                owner.setSignal(owner.id, gametypes.SIGNAL_SHOW_FASHION_WEAPON, 1)
        owner.client.resSet(const.RES_KIND_EQUIP, it, 0, part)
        Equipment.applyEquip(owner, it)
        if strong:
            owner.calcAllProp(gameconst.CALC_ALL_PROP_SRC_EQUIP)
        owner.addPSkillByEquip(it)

    def unEquipItem(self, owner, part, strong = True, bForce = False, calcSuit = True, calcPskillCache = True):
        if not bForce and self.isRefuse(owner):
            return False
        old = self.get(part)
        if old == CONT_EMPTY_VAL:
            return
        if part == gametypes.EQU_PART_WEAPON_ZHUSHOU:
            owner.setAspect(gametypes.EQU_PART_WUHUN, 0)
        Equipment.unApplyEquip(owner, old)
        self.set(part, CONT_EMPTY_VAL)
        owner._calcEquipEnhanceSuitCache()
        if not self.isEquipedFashion():
            owner.setSignal(owner.id, gametypes.SIGNAL_SHOW_FASHION, 0)
        if part in self.WEAPON_MUTEX_PARTS and not self.isEquipedBack():
            owner.setSignal(owner.id, gametypes.SIGNAL_SHOW_BACK, 0)
        if not self.isEquipedFashionWeapon():
            owner.setSignal(owner.id, gametypes.SIGNAL_SHOW_FASHION_WEAPON, 0)
        if part == gametypes.EQU_PART_FASHION_HEAD:
            owner.setSignal(owner.id, gametypes.SIGNAL_HIDE_FASHION_HEAD, 0)
        elif part == gametypes.EQU_PART_CAPE:
            owner._reCalcGuanYinEquipScoreEx(old)
        owner.setAspect(part, 0, useRealAspect=True)
        ed = ED.data.get(old.id) if old else None
        if ed and ed.get('equipType') == item.Item.EQUIP_BASETYPE_FASHION:
            slotParts = ed.get('slotParts', [])
            parts = ed.get('parts', [])
            autoParts = [ p for p in slotParts if p not in parts ]
            for p in autoParts:
                p = self.FASHION_PARTS_MAP.get(p, None)
                if p is not None:
                    owner.setAspect(p, 0, useRealAspect=True)

        owner.client.resRemove(const.RES_KIND_EQUIP, 0, part)
        if strong:
            if owner.rebalanced and owner.rebalancingDict.get(gametypes.REBALANCE_SUBSYS_ID_PROP, False):
                owner._recalcRebalancePROPFactor()
            else:
                owner.calcAllProp(gameconst.CALC_ALL_PROP_SRC_EQUIP)
        if calcSuit:
            owner.recalcEquipSuit(old, strong)
        owner.removePSkillByEquip(old, strong, calcPskillCache)
        owner._refreshRefineSpecialEffect()
        return True

    def unEquipAll(self, owner, strong = True):
        for part, _ in enumerate(self):
            if self.isEmpty(part):
                continue
            self.unEquipItem(owner, part, False)

        if strong:
            owner.calcAllProp(gameconst.CALC_ALL_PROP_SRC_EQUIP)

    def repairItem(self, owner, part, it, strong = True):
        self.set(part, it)
        if strong:
            owner.calcAllProp(gameconst.CALC_ALL_PROP_SRC_EQUIP)

    def recalc(self, owner):
        owner.calcAllProp(gameconst.CALC_ALL_PROP_SRC_EQUIP)

    def transfer(self, owner):
        for part, e in enumerate(self):
            if self.isEmpty(part):
                continue
            e = self.get(part)
            owner.client.resInsert(const.RES_KIND_EQUIP, e, 0, part)

    def getSendData(self, changeToItem = True):
        data = [ None for x in xrange(EQUIP_PART_NUM) ]
        for part in xrange(EQUIP_PART_NUM):
            it = self.get(part, changeToItem=changeToItem)
            if it == CONT_EMPTY_VAL:
                continue
            data[part] = it.copyDict()

        return data

    def isEquipedFashion(self):
        for part in self.ALL_FASHION_PARTS:
            if self.get(part):
                return True

        return False

    def isEquipedFashionWeapon(self):
        for part in self.FASHION_WEAPON_PARTS:
            if self.get(part):
                return True

        return False

    def isEquipedBack(self):
        for part in self.WEAPON_MUTEX_PARTS:
            if self.get(part):
                return True

        return False

    def initEquipPSkills(self, owner, doCalc = True):
        for e in self:
            if e != CONT_EMPTY_VAL:
                owner.addPSkillByEquip(e, doCalc)

    def updateExpireTimeOfRenewalType(self, owner, renewalType, expireTime):
        updatedCount = 0
        for part in xrange(EQUIP_PART_NUM):
            it = self.get(part)
            if not utils.updateExpireTime(owner, it, renewalType, expireTime, const.RES_KIND_EQUIP):
                continue
            self.set(part, it)
            self.enableEquipment(owner, part, it, True)
            updatedCount += 1

        return updatedCount

    def findEquipByUUID(self, uuid):
        for part in xrange(EQUIP_PART_NUM):
            it = self.get(part)
            if it == CONT_EMPTY_VAL:
                continue
            if it.uuid == uuid:
                return (it, part)

        return (CONT_EMPTY_VAL, const.CONT_NO_POS)
