#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/diGongDetailProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gametypes
import clientUtils
import formula
import ui
from guis import uiConst
from guis import uiUtils
from uiProxy import UIProxy
from cdata import exp_level_diff_data as ELDD
from data import formula_client_data as FCD
from data import sys_config_data as SCD
from data import multiline_digong_data as MDD
from data import exp_space_data as ESD

class DiGongDetailProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(DiGongDetailProxy, self).__init__(uiAdapter)
        self.modelMap = {'getDigongDetail': self.onGetDigongDetail,
         'getVipInfo': self.onGetVipInfo,
         'openBuyVipConfirm': self.onOpenBuyVipConfirm,
         'openDoubleExp': self.onOpenDoubleExp,
         'getDoubleExpInfo': self.onGetDoubleExpInfo,
         'gotoNpc': self.onGotoNpc,
         'toggleDoubleExp': self.onToggleDoubleExp}
        self.mediator = None
        self.callback = None
        self.digongLvDict = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_DIGONG_DETAIL:
            self.mediator = mediator
            return uiUtils.dict2GfxDict(self._getDidongDetailData(), True)

    def show(self):
        if not gameglobal.rds.configData.get('enableDigongDetail', False):
            return
        else:
            self._callDigongLv()
            if self.checkIsValidDigong():
                self.uiAdapter.loadWidget(uiConst.WIDGET_DIGONG_DETAIL)
                if self.callback:
                    BigWorld.cancelCallback(self.callback)
                    self.callback = None
                self.callback = BigWorld.callback(5.0, self.refreshDigongDetail)
            return

    def clearWidget(self):
        self.mediator = None
        self.digongLvDict = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_DIGONG_DETAIL)
        if self.callback:
            BigWorld.cancelCallback(self.callback)
            self.callback = None

    def reset(self):
        self.mediator = None

    def checkIsValidDigong(self):
        digongId = formula.getMLGNo(BigWorld.player().spaceNo)
        return digongId in SCD.data.get('validDigongIds', [120])

    def onGetDigongDetail(self, *arg):
        return uiUtils.dict2GfxDict(self._getDidongDetailData(), True)

    def refreshDigongDetail(self):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
        self.callback = BigWorld.callback(5.0, self.refreshDigongDetail)
        if self.mediator:
            self.mediator.Invoke('updateView', uiUtils.dict2GfxDict(self._getDidongDetailData(), True))

    def _getDidongDetailData(self):
        p = BigWorld.player()
        ret = {}
        monsterNum = gameglobal.rds.ui.player.getKillMonsterNum()
        ret['monsters'] = str(int(monsterNum[1]) - int(monsterNum[0]))
        ret['exp'] = p.getMLExpStat()
        finalExp = self._getFinalExp()
        ret['goalExp'] = int(finalExp[1])
        ret['finalExp'] = int(finalExp[0])
        ret['finalTips'] = SCD.data.get('digongDetailFinalTip', gameStrings.TEXT_DIGONGDETAILPROXY_90)
        ret['maxTips'] = SCD.data.get('digongDetailMaxTip', gameStrings.TEXT_DIGONGDETAILPROXY_90)
        ret['states'] = self._getStatesStr()
        return ret

    def _convertStateObj(self, stateName, state, value, valuable, helpKey):
        obj = {}
        obj['stateName'] = stateName
        obj['state'] = state
        obj['helpKey'] = helpKey
        if valuable:
            obj['stateStr'] = value
        elif state:
            obj['stateStr'] = gameStrings.TEXT_DIGONGDETAILPROXY_104
        else:
            obj['stateStr'] = gameStrings.TEXT_DIGONGDETAILPROXY_106
        return obj

    def _getStatesStr(self):
        p = BigWorld.player()
        stateStr = []
        totalTime = gameglobal.rds.ui.expBonus.getTotalRemainTime()
        isEnableDouble = hasattr(p, 'expBonusFreeze') and not p.expBonusFreeze and totalTime
        stateStr.append(self._convertStateObj(gameStrings.TEXT_DIGONGDETAILPROXY_115, isEnableDouble, 0, False, 283))
        monsterLv = self._getDigongMonsterLv()
        isEnableGuild = clientUtils.getRealGroupGuideMode(p, p.spaceNo, monsterLv)
        stateStr.append(self._convertStateObj(gameStrings.TEXT_DIGONGDETAILPROXY_123, isEnableGuild, 0, False, 284))
        if hasattr(p, 'expAdd') and p.expAdd[4]:
            stateStr.append(self._convertStateObj(gameStrings.TEXT_DIGONGDETAILPROXY_127, True, '+%.1f' % (p.expAdd[4] * 100) + str('%'), True, 285))
        if p.vipBarRank:
            vipBarConfig = SCD.data.get('vipBarConfig', {})
            vipBonus = vipBarConfig.get(p.vipBarRank, [0, ''])
            stateStr.append(self._convertStateObj(gameStrings.TEXT_DIGONGDETAILPROXY_133, True, '+%.0f' % (vipBonus[0] * 100) + str('%'), True, 286))
        return stateStr

    def _getFinalExp(self):
        p = BigWorld.player()
        monsterLv = self._getDigongMonsterLv()
        monsterNum = gameglobal.rds.ui.player.getKillMonsterNum()
        maxmonsterNum = int(monsterNum[1] - monsterNum[0])
        monsterExp = 0
        fd = FCD.data.get(gametypes.FORMULA_ID_DIGONG_MONSTER_EXP)
        func = fd.get('formula', None)
        if func:
            monsterExp = func({'lv': monsterLv,
             'plv': p.lv})
        digongId = formula.getMLGNo(BigWorld.player().spaceNo)
        isLingzhuDigong = MDD.data.get(digongId, {}).get('owerFortId', 0)
        if isLingzhuDigong:
            monsterExp *= 1.2
        lvDiff = p.lv - monsterLv
        coefficients = 1
        if lvDiff > 0:
            try:
                coefficients = ELDD.data[lvDiff]['coefficients'][1]
            except KeyError:
                if lvDiff < 0:
                    index = min(ELDD.data.keys())
                else:
                    index = max(ELDD.data.keys())
                coefficients = ELDD.data[index]['coefficients'][1]

        bonus = 0
        if p.vipBarRank:
            vipBarConfig = SCD.data.get('vipBarConfig', {})
            vipBonus = vipBarConfig.get(p.vipBarRank, [0, ''])
            bonus += vipBonus[0]
        if hasattr(p, 'expAdd') and p.expAdd[4]:
            bonus += p.expAdd[4]
        guideBonus = 0
        if clientUtils.getRealGroupGuideMode(p, p.spaceNo, monsterLv):
            guideBonus += SCD.data.get('guideBonus', 0.1)
        yaoliReduce = 1
        if p.yaoliReducePercent > 0:
            yaoliReduce = SCD.data.get('yaoliReduce', 0.8)
        totalTime = gameglobal.rds.ui.expBonus.getTotalRemainTime()
        isEnableDouble = hasattr(p, 'expBonusFreeze') and not p.expBonusFreeze and totalTime
        doubleBonus = 0
        if isEnableDouble:
            doubleBonus = 1
        finalExp = p.getMLExpStat() + maxmonsterNum * monsterExp * (1 + doubleBonus + bonus + guideBonus) / yaoliReduce * coefficients
        finalMaxExp = p.getMLExpStat() + maxmonsterNum * monsterExp * (2 + bonus + 0.1) / 0.8 * coefficients
        return (finalExp, finalMaxExp)

    def _getDigongMonsterLv(self):
        self._callDigongLv()
        monsterLv = 0
        monsterLvDict = self.digongLvDict
        digongId = formula.getMLGNo(BigWorld.player().spaceNo)
        isLingzhuDigong = MDD.data.get(digongId, {}).get('owerFortId', 0)
        if isLingzhuDigong and monsterLvDict and monsterLvDict.has_key(digongId):
            monsterLv = monsterLvDict[digongId]
        else:
            digongId = formula.getMapId(BigWorld.player().spaceNo)
            monsterLv = ESD.data.get(digongId, {}).get('defaultMonsterLv', 0)
        return monsterLv

    def updateDigongDict(self, digongLvDict):
        self.digongLvDict = digongLvDict
        if self.mediator:
            self.refreshDigongDetail()

    @ui.callInCD(2)
    def _callDigongLv(self):
        BigWorld.player().getMaxLingzhuDigongLv()

    def onGetVipInfo(self, *args):
        return gameglobal.rds.ui.tianyuMall.onGetVipRoleInfo()

    def onOpenBuyVipConfirm(self, *args):
        return gameglobal.rds.ui.tianyuMall.onOpenVipBasicPackageConfirm()

    def onOpenDoubleExp(self, *args):
        gameglobal.rds.ui.expBonus.show(0, 10001, True)

    def onGetDoubleExpInfo(self, *args):
        return gameglobal.rds.ui.tianyuMall.onGetDoubleExpInfo()

    def onGotoNpc(self, *args):
        seekId = SCD.data.get('diGongDoubleExpMap', ())
        uiUtils.findPosWithAlert(seekId)

    def onToggleDoubleExp(self, *args):
        return gameglobal.rds.ui.tianyuMall.onToggleDoubleExp()
