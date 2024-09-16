#Embedded file name: I:/bag/tmp/tw2/res/entities\common/wushuang.o
import gametypes
import gamelog
import BigWorld
import const
from sMath import limit
from userSoleType import UserSoleType
from userDictType import UserDictType
from userType import MemberProxy
from gameclass import SkillInfo
from data import ws_skill_config_data as WSCD
from data import prop_data as PD
from data import skill_general_data as SGD
from cdata import ws_enhance_data as WED
from cdata import game_msg_def_data as GMDD
from cdata import prop_def_data as PDD
from data import sys_config_data as SCD
if BigWorld.component in ('base', 'cell'):
    import Netease
    from data import log_src_def_data as LSDD

class Wushuang(UserSoleType):
    MAX_WS_SKILL_CNT = 3
    ws = MemberProxy('ws')
    mws = MemberProxy('mws')
    xiuwei = MemberProxy('xiuwei')
    exp = MemberProxy('exp')
    potential = MemberProxy('potential')
    lockExp = MemberProxy('lockExp')
    mwsEnhanceCnt = MemberProxy('mwsEnhanceCnt')
    xiuweiEnhanceCnt = MemberProxy('xiuweiEnhanceCnt')
    selectedWs = MemberProxy('selectedWs')
    selectedWs1 = MemberProxy('selectedWs1')
    selectedWs2 = MemberProxy('selectedWs2')
    wsType = MemberProxy('wsType')

    def __init__(self, dict):
        if not dict.has_key('ws'):
            dict['ws'] = 0
        if not dict.has_key('mws') or not dict['mws']:
            dict['mws'] = 0
        if not dict.has_key('xiuwei') or not dict['xiuwei']:
            dict['xiuwei'] = gametypes.WUSHUANG_XIUWEI_INITIAL
        if not dict.has_key('exp'):
            dict['exp'] = 0
        if not dict.has_key('potential'):
            dict['potential'] = 0
        if not dict.has_key('lockExp'):
            dict['lockExp'] = False
        if not dict.has_key('mwsEnhanceCnt'):
            dict['mwsEnhanceCnt'] = 0
        if not dict.has_key('xiuweiEnhanceCnt'):
            dict['xiuweiEnhanceCnt'] = 0
        if not dict.has_key('selectedWs') or not dict['selectedWs']:
            dict['selectedWs'] = [0, 0, 0]
        if not dict.has_key('selectedWs1') or not dict['selectedWs1']:
            dict['selectedWs1'] = [0, 0, 0]
        if not dict.has_key('selectedWs2') or not dict['selectedWs2']:
            dict['selectedWs2'] = [0, 0, 0]
        if not dict.has_key('wsType'):
            dict['wsType'] = 1
        self.fixedDict = dict

    def _getWsSkillCnt(self, index = const.SHORTCUT_SCHEME_ID_DEFAULT):
        selectedWs = self.getWsSkill(index)
        return len([ sk for sk in selectedWs if sk ])

    def canAddWsSkill(self, owner, skillId, bMsg = True, index = const.SHORTCUT_SCHEME_ID_DEFAULT):
        if not owner.wsSkills.has_key(skillId):
            return False
        if not WSCD.data.has_key(skillId):
            return False
        selectedWs = self.getWsSkill(index)
        if all(selectedWs):
            return False
        skillInfo = SkillInfo(skillId, owner.wsSkills[skillId].level)
        wsNeedKey = 'wsNeed%d' % self.wsType
        if not skillInfo or not skillInfo.hasSkillData(wsNeedKey):
            bMsg and gamelog.debug('wsType not match', skillId, self.wsType)
            return False
        if skillId in selectedWs:
            return False
        return True

    def addWsSkill(self, owner, skillId, index = const.SHORTCUT_SCHEME_ID_DEFAULT):
        if not self.canAddWsSkill(owner, skillId, index=index):
            return False
        if index not in const.SHORTCUT_SCHEME_ID_ALL:
            return False
        selectedWs = self.getWsSkill(index)
        emptyPos = selectedWs.index(0)
        selectedWs[emptyPos] = skillId
        return True

    def removeWsSkill(self, owner, skillId, index = const.SHORTCUT_SCHEME_ID_DEFAULT):
        if index not in const.SHORTCUT_SCHEME_ID_ALL:
            return False
        selectedWs = self.getWsSkill(index)
        if skillId in selectedWs:
            pos = selectedWs.index(skillId)
            selectedWs[pos] = 0

    def getWsSkill(self, index = const.SHORTCUT_SCHEME_ID_DEFAULT):
        selectedWs = [0, 0, 0]
        if index == const.SHORTCUT_SCHEME_ID_DEFAULT:
            selectedWs = self.selectedWs
        elif index == const.SHORTCUT_SCHEME_ID_EXTRA1:
            selectedWs = self.selectedWs1
        elif index == const.SHORTCUT_SCHEME_ID_EXTRA2:
            selectedWs = self.selectedWs2
        return selectedWs

    def removeAllWsSkillBySkilId(self, skillId):
        if skillId in self.selectedWs:
            pos = self.selectedWs.index(skillId)
            self.selectedWs[pos] = 0
        if skillId in self.selectedWs1:
            pos = self.selectedWs1.index(skillId)
            self.selectedWs1[pos] = 0
        if skillId in self.selectedWs2:
            pos = self.selectedWs2.index(skillId)
            self.selectedWs2[pos] = 0

    def removeAllWsSkillByIndex(self, index = const.SHORTCUT_SCHEME_ID_DEFAULT):
        if index == const.SHORTCUT_SCHEME_ID_DEFAULT:
            self.selectedWs = [0, 0, 0]
        elif index == const.SHORTCUT_SCHEME_ID_EXTRA1:
            self.selectedWs1 = [0, 0, 0]
        elif index == const.SHORTCUT_SCHEME_ID_EXTRA2:
            self.selectedWs2 = [0, 0, 0]

    def addWsExp(self, val):
        if self.lockExp:
            return
        self.exp = self.exp + val

    def unLockExp(self):
        self.lockExp = False

    def canUseWsExp(self):
        if self.exp < gametypes.WUSHUANG_EXP_MAX:
            return False
        return True

    def convertPotential(self):
        if not self.canUseWsExp():
            return
        self.exp = 0
        self.potential += 1

    def resetWs(self, toVal = 0):
        self.ws = toVal

    def reduceWs(self, val):
        self.ws = limit(self.ws - val, 0, self.mws)

    def addWs(self, val):
        self.ws = limit(self.ws + val, 0, self.mws)

    def getMaxMws(self):
        propId = PDD.data.PROPERTY_MAX_WSP_A if self.wsType == gametypes.WS_TYPE_1 else PDD.data.PROPERTY_MAX_WSP_B
        maxMws = PD.data.get(propId, {}).get('max', gametypes.WUSHUANG_POINT_MAX)
        return maxMws

    def setMws(self, owner, mws):
        if mws <= self.getMaxMws():
            self.mws = mws
            owner.calcAllProp()

    def getMws(self, owner):
        if owner._isSchoolSwitch():
            return self.getMaxMws()
        if self.wsType == gametypes.WS_TYPE_1:
            return owner.mws[0]
        return owner.mws[1]

    def getMwsAdd(self, owner):
        if owner._isSchoolSwitch():
            wsSkills = owner.schoolSwitchInfo.switchedWSSkills
        else:
            wsSkills = owner.wsSkills
        mws = self.mws
        mwsAddBySkills = []
        for skillId, sVal in wsSkills.iteritems():
            sData = SGD.data.get((skillId, sVal.level), {})
            mwsAdd = sData.get('mwsAdd')
            if mwsAdd and sData.get('wsType') == self.wsType:
                mwsAddBySkills.append(mwsAdd)

        mwsAddBySkills.sort(reverse=True)
        skillCnt = SCD.data.get('wsAddSkiillCount')
        if skillCnt:
            mws += sum(mwsAddBySkills[:skillCnt])
        return mws

    def setXiuwei(self, xiuwei):
        if xiuwei <= gametypes.WUSHUANG_XIUWEI_MAX:
            self.xiuwei = xiuwei

    def getXiuwei(self, owner):
        if owner._isSchoolSwitch():
            return gametypes.WUSHUANG_XIUWEI_MAX
        return self.xiuwei

    def canEnhanceMws(self, owner, useItems):
        enhanceCnt = self.mwsEnhanceCnt + 1
        enhanceData = WED.data.get(enhanceCnt, {})
        if not enhanceData:
            return False
        if self.exp < enhanceData['mwsExpCost']:
            return False
        if self.getMws(owner) >= self.getMaxMws():
            return False
        if owner.inv.isRefuse():
            owner.client.showGameMsg(GMDD.data.ITEM_INV_LOCKED, ())
            return False
        enhanceItems = [ it for it in enhanceData['mwsEnhanceItems'] if it[0] in useItems ]
        for itemId, itemCnt, _ in enhanceItems:
            if not owner.inv.hasItemInPages(itemId, itemCnt, enableParentCheck=True):
                gamelog.debug('zt: not enough enhance items')
                return False

        return True

    def enhanceMws(self, owner, useItems):
        if not self.canEnhanceMws(owner, useItems):
            return
        enhanceData = WED.data[self.mwsEnhanceCnt + 1]
        enhanceItems = [ it for it in enhanceData['mwsEnhanceItems'] if it[0] in useItems ]
        mwsAdd = enhanceData['mwsAdd']
        opNUID = Netease.getNUID()
        for itemId, itemCnt, enhanceVal in enhanceItems:
            if owner.inv.autoConsumeItems(owner, itemId, itemCnt, opNUID, LSDD.data.LOG_SRC_ENHANCE_MWS, False, detail=str(self.wsType), enableParentCheck=True):
                mwsAdd += enhanceVal

        self.mwsEnhanceCnt += 1
        self.exp -= enhanceData['mwsExpCost']
        self.mws += mwsAdd

    def canEnhanceXiuwei(self, owner, useItems):
        enhanceCnt = self.xiuweiEnhanceCnt + 1
        enhanceData = WED.data.get(enhanceCnt, {})
        if not enhanceData:
            return False
        if self.xiuwei >= gametypes.WUSHUANG_XIUWEI_MAX:
            return False
        if self.potential < enhanceData['xiuweiPotentialCost']:
            return False
        if owner.inv.isRefuse():
            owner.client.showGameMsg(GMDD.data.ITEM_INV_LOCKED, ())
            return False
        enhanceItems = [ it for it in enhanceData['xiuweiEnhanceItems'] if it[0] in useItems ]
        for itemId, itemCnt, _ in enhanceItems:
            if not owner.inv.hasItemInPages(itemId, itemCnt, enableParentCheck=True):
                gamelog.debug('zt: not enough enhance items')
                return False

        return True

    def enhanceXiuwei(self, owner, useItems):
        if not self.canEnhanceXiuwei(owner, useItems):
            return
        enhanceData = WED.data[self.xiuweiEnhanceCnt + 1]
        enhanceItems = [ it for it in enhanceData['xiuweiEnhanceItems'] if it[0] in useItems ]
        xiuweiAdd = enhanceData['xiuweiAdd']
        opNUID = Netease.getNUID()
        for itemId, itemCnt, enhanceVal in enhanceItems:
            if owner.inv.autoConsumeItems(owner, itemId, itemCnt, opNUID, LSDD.data.LOG_SRC_ENHANCE_WS_XIUWEI, False, detail=str(self.wsType), enableParentCheck=True):
                xiuweiAdd += enhanceVal

        self.xiuweiEnhanceCnt += 1
        self.potential -= enhanceData['xiuweiPotentialCost']
        self.xiuwei = limit(self.xiuwei + xiuweiAdd, 0, gametypes.WUSHUANG_XIUWEI_MAX)


class WushuangDict(UserDictType):

    def resetWs(self, toVal = 0):
        for wsVal in self.values():
            wsVal.resetWs(toVal)

    def _lateReload(self):
        super(Wushuang, self)._lateReload()
        for wsVal in self.itervalues():
            wsVal.reloadScript()
