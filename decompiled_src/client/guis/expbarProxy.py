#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/expbarProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import formula
import gametypes
import gameglobal
import utils
import gamelog
import const
from guis import uiConst
from uiProxy import UIProxy
from ui import gbk2unicode
from guis import uiUtils
from gamestrings import gameStrings
from cdata import vp_stage_data as VSD
from data import vp_level_data as VLD
from data import vp_tips_data as VTD
from data import avatar_lv_data as ALD
from data import multiline_digong_data as MDD
from data import arena_mode_data as AMD
XIUYING_ACCURACY = 10000

class ExpbarProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ExpbarProxy, self).__init__(uiAdapter)
        self.modelMap = {'getExp': self.onGetExp,
         'getLevel': self.onGetLevel,
         'getVpInfo': self.onGetVpInfo,
         'genVpTip': self.onGenVpTip,
         'getDoubleExpDesc': self.onGetDoubleExpDesc,
         'genXiuYingTip': self.onGenXiuYingTip,
         'refreshXiuYing': self.onRefreshXiuYing}
        self.reset()

    def reset(self):
        self.mediator = None
        self.curExp = 0
        self.maxExp = 1
        self.lv = 1
        self.fpsCallback = None
        self.fpsShow = False

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_EXPBAR:
            self.mediator = mediator
            self.initUI()
            totalTime = gameglobal.rds.ui.expBonus.getTotalRemainTime()
            p = BigWorld.player()
            if totalTime and hasattr(p, 'expBonusFreeze') and not p.expBonusFreeze:
                self.setExpBgColor(True)

    def initUI(self):
        self.initLvStr()

    def initLvStr(self):
        lvExStr = self.getLvExStr()
        self.mediator.Invoke('setLevel', (GfxValue('Lv.%d' % BigWorld.player().lv), GfxValue(gbk2unicode(lvExStr))))

    def onGetExp(self, *arg):
        arr = self.movie.CreateArray()
        p = BigWorld.player()
        if p.life == gametypes.LIFE_DEAD:
            if self.mediator:
                self.mediator.SetVisible(False)
        max = str(ALD.data.get(p.lv, {}).get('upExp', 1))
        return uiUtils.array2GfxAarry((getattr(p, 'exp', 0), max, p.getLvBreakStep()))

    def onGetLevel(self, *arg):
        p = BigWorld.player()
        if p.realLv != None:
            return GfxValue('')
        else:
            return

    def onGetDoubleExpDesc(self, *arg):
        p = BigWorld.player()
        if not p:
            return GfxValue('')
        time = gameglobal.rds.ui.expBonus.getTotalRemainTime()
        if hasattr(p, 'expBonusFreeze') and not p.expBonusFreeze and time:
            desc = uiUtils.toHtml(gameStrings.TEXT_EXPBARPROXY_85 + utils.formatTimeStr(time, gameStrings.TEXT_EXPBARPROXY_85_1), '#73e539')
        elif hasattr(p, 'expBonusFreeze') and p.expBonusFreeze and time:
            desc = uiUtils.toHtml(gameStrings.TEXT_EXPBARPROXY_87 + utils.formatTimeStr(time, gameStrings.TEXT_EXPBARPROXY_85_1), '#e53900')
        else:
            desc = ''
        lvBreakDesc = ''
        if p.isInLvBreak():
            lvBreakDesc = gameStrings.TEXT_EXPBARPROXY_92 % (p.getBreakStartLv() + p.getLvBreakUp())
        if desc:
            desc += '\n' + lvBreakDesc
        else:
            desc += lvBreakDesc
        return GfxValue(gbk2unicode(desc))

    def setExp(self, cur):
        p = BigWorld.player()
        maxValue = str(ALD.data.get(p.lv, {}).get('upExp', 1))
        if self.mediator:
            self.mediator.Invoke('setExp', (GfxValue(cur), GfxValue(maxValue), GfxValue(p.getLvBreakStep())))
            self.refreshXiuYingBar()

    def setVisible(self, isVisible):
        if self.mediator:
            self.mediator.Invoke('setVisible', GfxValue(isVisible))

    def setLevel(self, lv):
        if self.mediator:
            lvExStr = self.getLvExStr()
            self.mediator.Invoke('setLevel', (GfxValue('Lv.%d' % lv), GfxValue(lvExStr)))
            self.lv = lv
            self.refreshXiuYingBar()

    def getLvExStr(self):
        p = BigWorld.player()
        lvStr = ''
        if p.inFuben() and p.fbGuideEffect == const.GUIDE_MASTER_MODE:
            if p.realLv != 0 and p.realLv != p.lv:
                lvStr = gameStrings.LV_GUIDE_TXT % (str(p.lv), str(p.realLv))
        if p.inMLSpace() and MDD.data.get(formula.getMLGNo(p.spaceNo), {}).has_key('digongLv'):
            lvStr = gameStrings.LV_BALANCE_TXT % (str(p.lv), str(p.realLv))
        fbNo = formula.getFubenNo(p.spaceNo)
        if p.isInSSCorTeamSSC():
            lvStr = gameStrings.LV_BALANCE_TXT % (str(p.lv), str(p.realLv))
        arenaMode = formula.fbNo2ArenaMode(fbNo)
        if p.inFubenTypes(const.FB_TYPE_ARENA) and AMD.data.get(arenaMode, {}).get('needReCalcLv', 0):
            lvStr = gameStrings.LV_BALANCE_TXT % (str(p.lv), str(p.realLv))
        return lvStr

    def setExpBgColor(self, isDouble):
        if self.mediator:
            self.mediator.Invoke('setExpBgColor', GfxValue(isDouble))

    def setBarUnFullColor(self):
        if self.mediator:
            self.mediator.Invoke('setBarUnFullColor')

    def onGetVpInfo(self, *arg):
        p = BigWorld.player()
        ret = {'baseVp': p.baseVp,
         'savedVp': p.savedVp,
         'maxVp': p.maxVp,
         'vpStage': p.getVpStage()}
        return uiUtils.dict2GfxDict(ret)

    def setVpStage(self, vpStage):
        if self.mediator:
            self.mediator.Invoke('setVpStage', GfxValue(vpStage))

    def setVpBar(self, numBaseVp, numSavedVp, numMaxVp):
        if self.mediator:
            self.mediator.Invoke('setVpBar', (GfxValue(numBaseVp), GfxValue(numSavedVp), GfxValue(numMaxVp)))

    def onGenVpTip(self, *args):
        p = BigWorld.player()
        vData = VLD.data.get(p.lv, {})
        desc = gameStrings.TEXT_EXPBARPROXY_160 % (p.baseVp + p.savedVp, vData['maxVp'] + p.vpAdd[2])
        desc += gameStrings.TEXT_EXPBARPROXY_161 % p.savedVp
        desc += gameStrings.TEXT_EXPBARPROXY_162 % p.baseVp
        stage = p.getVpStage()
        stageList = [gameStrings.TEXT_EXPBARPROXY_164,
         gameStrings.TEXT_EXPBARPROXY_164_1,
         gameStrings.TEXT_EXPBARPROXY_164_2,
         gameStrings.TEXT_EXPBARPROXY_164_3,
         gameStrings.TEXT_EXPBARPROXY_164_4]
        stageColorList = ['#FFFFF4',
         '#7ACC29',
         '#2996CC',
         '#B54BFF',
         '#E5812E']
        desc += gameStrings.TEXT_EXPBARPROXY_166 % (stageColorList[stage], stageList[stage])
        tips = VTD.data
        expParam = VSD.data.get(stage)['expParam']
        desc += gameStrings.TEXT_EXPBARPROXY_170
        if stage == 0:
            desc += gameStrings.TEXT_EXPBARPROXY_173
        else:
            desc += tips.get(uiConst.VP_PANEL_DESC1, {}).get('desc', '') % (expParam - 1)
            desc += tips.get(uiConst.VP_PANEL_DESC2, {}).get('desc', '') % (expParam - 1)
        desc += ''
        return GfxValue(gbk2unicode(desc))

    def onGenXiuYingTip(self, *args):
        p = BigWorld.player()
        vData = VLD.data.get(p.lv, {})
        vpDefaultLower = vData.get('vpDefaultLower', 0)
        curXiuYing = (p.baseVp + p.savedVp + p.vpStorage) * vpDefaultLower + p.vpPool
        tomorrowXiuYing = vData.get('dailyVp', 0) * vpDefaultLower
        maxXiuYing = p.maxVp * vpDefaultLower
        tmpDesc0 = VTD.data.get(uiConst.VP_XIUYING_DESC_0, {}).get('desc', '')
        tmpDesc1 = VTD.data.get(uiConst.VP_XIUYING_DESC_1, {}).get('desc', '')
        tmpDesc2 = VTD.data.get(uiConst.VP_XIUYING_DESC_2, {}).get('desc', '')
        tmpDesc3 = VTD.data.get(uiConst.VP_XIUYING_DESC_3, {}).get('desc', '')
        tmpDesc4 = VTD.data.get(uiConst.VP_XIUYING_DESC_4, {}).get('desc', '')
        tmpDesc5 = VTD.data.get(uiConst.VP_XIUYING_DESC_5, {}).get('desc', '')
        desc0 = tmpDesc0 % curXiuYing
        desc1 = tmpDesc1 % tomorrowXiuYing
        desc2 = tmpDesc2 % maxXiuYing
        desc3 = ''.join((tmpDesc3,
         '\n',
         tmpDesc4,
         '\n',
         tmpDesc5))
        info = {'desc0': desc0,
         'desc1': desc1,
         'desc2': desc2,
         'desc3': desc3}
        return uiUtils.dict2GfxDict(info, True)

    def refreshXiuYingBar(self):
        if self.mediator:
            p = BigWorld.player()
            curStage, stageList = self.getXiuYingStage()
            curXiuYing = p.baseVp + p.savedVp + p.vpStorage
            curProValue = 0
            if len(stageList) - 1 and curStage >= 0:
                curProValue = curStage * XIUYING_ACCURACY + XIUYING_ACCURACY * (curXiuYing - stageList[curStage]) / (stageList[curStage + 1] - stageList[curStage])
            info = {'curXiuYing': curXiuYing,
             'curStage': curStage,
             'stageList': stageList,
             'stageNum': len(stageList) - 1,
             'curProValue': curProValue,
             'maxValue': (len(stageList) - 1) * XIUYING_ACCURACY}
            gamelog.debug('@zq stageList', curXiuYing, stageList, curStage, curProValue)
            self.mediator.Invoke('refreshXiuYingBar', uiUtils.dict2GfxDict(info, True))

    def getXiuYingStage(self):
        p = BigWorld.player()
        vData = VLD.data.get(p.lv, {})
        if not vData:
            return (0, [0])
        stageList = [0]
        maxVp = p.maxVp
        stages = vData.get('vpStages', 0)
        stage = 0
        if p.baseVp + p.savedVp + p.vpStorage and maxVp:
            for i, stageMaxVal in enumerate(stages):
                if stageMaxVal < maxVp:
                    stageList.append(stageMaxVal)
                    if p.baseVp + p.savedVp + p.vpStorage >= stageList[-1]:
                        stage += 1
                else:
                    stageList.append(maxVp)
                    if p.baseVp + p.savedVp + p.vpStorage >= stageList[-1]:
                        stage += 1
                    break

        stageNum = len(stageList) - 1
        if stage >= stageNum:
            stage = stageNum - 1
        return (stage, stageList)

    def onRefreshXiuYing(self, *args):
        self.refreshXiuYingBar()
