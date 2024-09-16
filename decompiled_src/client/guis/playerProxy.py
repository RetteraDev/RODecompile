#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/playerProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
import gamelog
import copy
import appSetting
import keys
import formula
import utils
import math
from guis import uiConst
from ui import gbk2unicode
from uiProxy import DataProxy
from callbackHelper import Functor
from guis import ui
from guis import uiUtils
from guis import messageBoxProxy
from guis import groupUtils
from messageBoxProxy import MBButton
from gameStrings import gameStrings
from guis.asObject import ASObject
from data import sheng_si_chang_data as SSCD
from data import multiline_digong_data as MDD
from data import arena_mode_data as AMD
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD
from data import item_data as ID
from data import photo_border_data as PBD
from cdata import pskill_data as PD
unitTypePath = 'unitType/icon/'
statePath = 'state/icon/'
POOL_TEXT_CONVERT_THRESHOLD = 10000

class PlayerProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(PlayerProxy, self).__init__(uiAdapter)
        self.bindType = 'player'
        self.modelMap = {'selectSelf': self.onSelectSelf,
         'closePKConfig': self.onClosePKConfig,
         'confirmPKConfig': self.onConfirmPKConfig,
         'confirmLevel': self.onConfirmLevel,
         'initPKConfigData': self.onInitPKConfigData,
         'initPKState': self.onInitPKState,
         'selectPeaceMode': self.onSelectPeaceMode,
         'selectKillMode': self.onSelectKillMode,
         'selectDiDuiMode': self.onSelectDiDuiMode,
         'selectPKConfig': self.onSelectPKConfig,
         'clickYaoli': self.onClickYaoli,
         'getYaoliTip': self.onGetYaoliTip,
         'clickHpPoolMc': self.onClickHpPoolMc,
         'clickMpPoolMc': self.onClickMpPoolMc,
         'clickFbAvoidDieMc': self.onClickFbAvoidDieMc,
         'initPlayerUnitFrame': self.onInitPlayerUnitFrame}
        self.mediator = None
        self.pkMediator = None
        self.pkModeDict = {const.PK_MODE_PEACE: {'state': 'heping',
                               'stateDesc': gameStrings.TEXT_PLAYERPROXY_67},
         const.PK_MODE_KILL: {'state': 'shalu',
                              'stateDesc': gameStrings.TEXT_PLAYERPROXY_68},
         const.PK_MODE_DEFENSE: {'state': 'ziwei',
                                 'stateDesc': gameStrings.TEXT_PLAYERPROXY_69},
         const.PK_MODE_POLICE: {'state': 'xiayi',
                                'stateDesc': gameStrings.TEXT_PLAYERPROXY_70},
         const.PK_MODE_HOSTILE: {'state': 'didui',
                                 'stateDesc': gameStrings.TEXT_PLAYERPROXY_71}}
        uiAdapter.registerEscFunc(uiConst.WIDGET_PK_CONFIG, Functor(self.hidePkConfig))

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_PLAYER_UF:
            self.mediator = mediator
            hpMode = appSetting.Obj.get(keys.SET_HP_MODE, 0)
            self.setHpMode(hpMode)
            BigWorld.player().addPlayerAllStateIcon()
            BigWorld.player().setSafeModeState()
            BigWorld.player().setVIPModeState()
            jingjie = BigWorld.player().jingJie
            self.setJingJie(jingjie)
            BigWorld.player().setActivityState()
        elif widgetId == uiConst.WIDGET_PK_CONFIG:
            self.pkMediator = mediator

    def onUpdateActivityStateBonus(self):
        if not gameglobal.rds.configData.get('enableActivityStateBonus', False):
            for stateId in BigWorld.player().activityStateIds:
                BigWorld.player().quitFakeState(stateId)

        else:
            BigWorld.player().setActivityState()

    def getValue(self, key):
        p = BigWorld.player()
        if key == 'player.init':
            pass
        else:
            if key == 'player.name':
                return GfxValue(gbk2unicode(p.realRoleName))
            if key == 'player.hp':
                return GfxValue(p.hp)
            if key == 'player.mhp':
                return GfxValue(p.mhp)
            if key == 'player.sp':
                return GfxValue(p.mp)
            if key == 'player.msp':
                return GfxValue(p.mmp)
            if key == 'player.baseVp':
                return GfxValue(p.baseVp)
            if key == 'player.savedVp':
                return GfxValue(p.savedVp)
            if key == 'player.maxVp':
                return GfxValue(p.maxVp)
            if key == 'player.yaoliPoint':
                return GfxValue(p.yaoliPoint)
            if key == 'player.yaoliMPoint':
                return GfxValue(p.getYaoliMPoint())
            if key == 'player.doubleExp':
                return GfxValue(p.doubleExpPointInML)
            if key == 'player.doubleMExp':
                return GfxValue(p.getYaoliMPoint())
            if key == 'player.vpStage':
                return GfxValue(p.getVpStage())
            if key == 'player.teamLeader':
                if hasattr(p, 'headerGbId') and p.headerGbId == p.gbId:
                    return GfxValue(True)
                else:
                    return GfxValue(False)
            else:
                if key == 'player.showDoubleExp':
                    return GfxValue(p.inMLDoubleExpSpace() and gameglobal.rds.configData.get('enableDoubleExpPointInML', False))
                if key == 'player.combat':
                    return GfxValue(p.inCombat)
                if key == 'player.level':
                    lvStr = 'Lv.' + str(p.lv)
                    if p.inFuben() and p.fbGuideEffect == const.GUIDE_MASTER_MODE:
                        if p.realLv != 0 and p.realLv != p.lv:
                            lvStr = 'Lv.' + str(p.lv) + gameStrings.TEXT_PLAYERPROXY_142 + str(p.realLv) + ')'
                    if p.inMLSpace() and MDD.data.get(formula.getMLGNo(p.spaceNo), {}).has_key('digongLv'):
                        lvStr = gameStrings.LV_BALANCE_TXT % (str(p.lv), str(p.realLv))
                    fbNo = formula.getFubenNo(p.spaceNo)
                    arenaMode = formula.fbNo2ArenaMode(fbNo)
                    if p.inFubenTypes(const.FB_TYPE_ARENA) and AMD.data.get(arenaMode, {}).get('needReCalcLv', 0):
                        lvStr = gameStrings.LV_BALANCE_TXT % (str(p.lv), str(p.realLv))
                    if p.isInSSCorTeamSSC():
                        lvStr = gameStrings.LV_BALANCE_TXT % (str(p.lv), str(p.realLv))
                    return GfxValue(gbk2unicode(lvStr))
                if key == 'player.entityId':
                    return GfxValue(p.id)
                if key == 'player.jingjie':
                    return GfxValue(p.jingJie)
                if key == 'player.hpPool':
                    return (GfxValue(self.getHpMpPoolShowText(p.hpPool)), GfxValue(self.needShowHpMpPoolIcon()))
                if key == 'player.mpPool':
                    return (GfxValue(self.getHpMpPoolShowText(p.mpPool)), GfxValue(self.needShowHpMpPoolIcon()))
                if key == 'player.addHpPoolTip':
                    return GfxValue(gbk2unicode(self.getHpPoolTip()))
                if key == 'player.addMpPoolTip':
                    return GfxValue(gbk2unicode(self.getMpPoolTip()))
                if key == 'player.hpText':
                    isShow = appSetting.Obj.get(keys.SET_HP_SHOW, 1)
                    return GfxValue(isShow)
                if key == 'player.fbAvoidDie':
                    if gameglobal.rds.configData.get('enableFbAvoidDieItem', False):
                        return GfxValue(p.fbAvoidDieItemCnt)
                    else:
                        return GfxValue(0)
                elif key == 'player.addFbAvoidDieTip':
                    return GfxValue(gbk2unicode(self.getFbAvoidDieTip()))

    def confirmBianyao(self):
        p = BigWorld.player()
        p.cell.requestEnterBianyao()

    def onClickYaoli(self, *arg):
        p = BigWorld.player()
        if p._isInBianyao():
            p.cell.requestLeaveBianyao()
        else:
            p.cell.requestEnterBianyao()

    def onGetYaoliTip(self, *args):
        tip = SCD.data.get('yaoliTip', gameStrings.TEXT_PLAYERPROXY_197) % self.getKillMonsterNum()
        return GfxValue(gbk2unicode(tip))

    def getKillMonsterNum(self):
        p = BigWorld.player()
        members = p._getSortedMembers()
        groupNum = min(len([ 1 for x, _ in members if groupUtils.isInSameTeam(p.gbId, x) ]), const.TEAM_MAX_NUMBER)
        mlgNo = formula.getMLGNo(p.spaceNo)
        mddd = MDD.data.get(mlgNo, {})
        if not mddd:
            mddd = MDD.data.get(100, {})
        defYaoLiValue = [10,
         10,
         10,
         10,
         10]
        yaoliValue = mddd.get('yaoLiValue', defYaoLiValue)
        if type(yaoliValue) != tuple or len(yaoliValue) != 5:
            yaoliValue = defYaoLiValue
        point = int(round(yaoliValue[groupNum - 1] * (1 - p.yaoliReducePercent)))
        curNum = math.ceil(p.yaoliPoint / point)
        totalNum = math.ceil(p.getYaoliMPoint() / point)
        return (curNum, totalNum)

    def setName(self, name):
        if self.binding.has_key('player.name'):
            self.binding['player.name'][1].InvokeSelf(GfxValue(gbk2unicode(name)))

    def setLv(self, lv):
        p = BigWorld.player()
        lvStr = 'Lv.' + str(p.lv)
        if p.inFuben() and p.fbGuideEffect == const.GUIDE_MASTER_MODE:
            if p.realLv != 0 and p.realLv != p.lv:
                lvStr = 'Lv.' + str(p.lv) + gameStrings.TEXT_PLAYERPROXY_142 + str(p.realLv) + ')'
        if p.inMLSpace() and MDD.data.get(formula.getMLGNo(p.spaceNo), {}).has_key('digongLv'):
            lvStr = gameStrings.LV_BALANCE_TXT % (str(p.lv), str(p.realLv))
        fbNo = formula.getFubenNo(p.spaceNo)
        if p.isInSSCorTeamSSC():
            lvStr = gameStrings.LV_BALANCE_TXT % (str(p.lv), str(p.realLv))
        arenaMode = formula.fbNo2ArenaMode(fbNo)
        if p.inFubenTypes(const.FB_TYPE_ARENA) and AMD.data.get(arenaMode, {}).get('needReCalcLv', 0):
            lvStr = gameStrings.LV_BALANCE_TXT % (str(p.lv), str(p.realLv))
        if self.binding.has_key('player.level'):
            self.binding['player.level'][1].InvokeSelf(GfxValue(gbk2unicode(lvStr)))

    def setHpMode(self, mode):
        if self.binding.has_key('player.hp'):
            self.binding['player.name'][0].Invoke('setHpMode', GfxValue(mode))

    def setHp(self, hp):
        if self.binding.has_key('player.hp'):
            self.binding['player.hp'][1].InvokeSelf(GfxValue(hp))

    def setMhp(self, mhp):
        if self.binding.has_key('player.mhp'):
            self.binding['player.mhp'][1].InvokeSelf(GfxValue(mhp))

    def setSp(self, sp):
        if self.binding.has_key('player.sp'):
            self.binding['player.sp'][1].InvokeSelf(GfxValue(sp))

    def setMsp(self, msp):
        if self.binding.has_key('player.msp'):
            self.binding['player.msp'][1].InvokeSelf(GfxValue(msp))

    def setJingJie(self, jingJie):
        if self.binding.has_key('player.jingJie'):
            self.binding['player.jingJie'][1].InvokeSelf(GfxValue(jingJie))

    def setEp(self, ep):
        pass

    def setMep(self, mep):
        pass

    def setBaseVp(self, value):
        if self.binding.has_key('player.baseVp'):
            self.binding['player.baseVp'][1].InvokeSelf(GfxValue(value))

    def setSavedVp(self, value):
        if self.binding.has_key('player.savedVp'):
            self.binding['player.savedVp'][1].InvokeSelf(GfxValue(value))

    def setMaxVp(self, value):
        if self.binding.has_key('player.maxVp'):
            self.binding['player.maxVp'][1].InvokeSelf(GfxValue(value))

    def setYaoliPoint(self, value):
        if self.binding.has_key('player.yaoliPoint'):
            self.binding['player.yaoliPoint'][1].InvokeSelf(GfxValue(value))

    def setYaoliMPoint(self, value):
        if self.binding.has_key('player.yaoliMPoint'):
            self.binding['player.yaoliMPoint'][1].InvokeSelf(GfxValue(value))

    def setDoubleExp(self, value):
        if self.binding.has_key('player.doubleExp'):
            self.binding['player.doubleExp'][1].InvokeSelf(GfxValue(value))

    def setDoubleMExp(self, value):
        if self.binding.has_key('player.doubleMExp'):
            self.binding['player.doubleMExp'][1].InvokeSelf(GfxValue(value))

    def setVpStage(self, value):
        if self.binding.has_key('player.vpStage'):
            self.binding['player.vpStage'][1].InvokeSelf(GfxValue(value))

    def setLeaderIcon(self, flag):
        if self.binding.has_key('player.teamLeader') and self.mediator:
            self.binding['player.teamLeader'][1].InvokeSelf(GfxValue(flag))

    def setCombatVisible(self, bVisible):
        if self.binding.has_key('player.name'):
            self.binding['player.name'][0].Invoke('setCombatVisible', GfxValue(bVisible))

    def setUnitType(self, iconPath):
        if self.binding.has_key('player.unitType'):
            self.binding['player.unitType'][0].Invoke('setUnitType', GfxValue(iconPath))

    def changeMergeIcon(self, mergeBuff):
        if self.binding.has_key('player.name'):
            self.binding['player.name'][0].Invoke('mergeState', uiUtils.array2GfxAarry(mergeBuff, True))

    def changeStateIcon(self, addData, delData):
        if self.binding.has_key('player.name'):
            self.binding['player.name'][0].Invoke('changeState', (uiUtils.array2GfxAarry(addData), uiUtils.array2GfxAarry(delData)))

    def changeHpTextShow(self, isShow):
        if self.binding.has_key('player.hpText'):
            self.binding['player.hpText'][1].InvokeSelf(GfxValue(isShow))

    def showBeHit(self):
        if self.binding.has_key('player.name'):
            self.binding['player.name'][0].GotoAndPlay('impact')

    def tweenMp(self, time):
        if self.binding.has_key('player.name'):
            self.binding['player.name'][0].Invoke('tweenMp', GfxValue(time))

    def stopTweenMp(self):
        if self.binding.has_key('player.name'):
            self.binding['player.name'][0].Invoke('stopTweenMp')

    def tweenEp(self, time, marknum):
        pass

    def stopTweenEp(self):
        pass

    def onSelectSelf(self, *arg):
        gamelog.debug('hjx debug onSelectSelf')
        p = BigWorld.player()
        isShowingEffect = p.chooseEffect.isShowingEffect
        if isShowingEffect:
            p.chooseEffect.run(p)
            p.ap.reset()
            return
        p.lockTarget(p)

    def getPkModeDict(self, state = None):
        p = BigWorld.player()
        if state == None:
            state = p.pkMode
        stateDic = self.pkModeDict.get(state, {})
        if stateDic:
            stateDic = copy.deepcopy(stateDic)
            stateDic['stateDesc'] += gameStrings.PLAYER_UNIT_FRAME_KILL % p.pkPunishTime
        return stateDic

    def updatePKState(self, state):
        if self.mediator:
            state = self.getPkModeDict(state)
            if state:
                self.mediator.Invoke('updatePKState', uiUtils.dict2GfxDict(state, True))

    def onInitPKState(self, *arg):
        stateDict = self.getPkModeDict()
        return uiUtils.dict2GfxDict(stateDict, True)

    def onSelectPeaceMode(self, *arg):
        p = BigWorld.player()
        p.cell.switchPkMode(const.PK_MODE_PEACE, '')

    @ui.checkInventoryLock()
    def onSelectKillMode(self, *arg):
        now = utils.getNow()
        p = BigWorld.player()
        if p.pkMode in (const.PK_MODE_KILL, const.PK_MODE_HOSTILE) and now - p.lastSwitchPKModeStamp <= const.PK_SWITCH_CD:
            p.showGameMsg(GMDD.data.SWITCH_PK_MODE_TIME, ())
            return
        p.cell.switchPkMode(const.PK_MODE_KILL, BigWorld.player().cipherOfPerson)

    @ui.checkInventoryLock()
    def onSelectDiDuiMode(self, *arg):
        now = utils.getNow()
        p = BigWorld.player()
        enableGuildEnemy = gameglobal.rds.configData.get('enableGuildEnemy', False)
        if not enableGuildEnemy:
            p.showGameMsg(GMDD.data.GUILD_ENEMY_CLOSED, ())
            return
        if p.pkMode in (const.PK_MODE_KILL, const.PK_MODE_HOSTILE) and now - p.lastSwitchPKModeStamp <= const.PK_SWITCH_CD:
            p.showGameMsg(GMDD.data.SWITCH_PK_MODE_TIME, ())
            return
        p.cell.switchPkMode(const.PK_MODE_HOSTILE, BigWorld.player().cipherOfPerson)
        if self.pkMediator:
            self.pkMediator.Invoke('setDisableDiDuiMode', ())

    def onSelectPKConfig(self, *arg):
        self.show()

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PK_CONFIG)

    def onInitPKConfigData(self, *arg):
        movie = arg[0]
        obj = movie.CreateObject()
        p = BigWorld.player()
        obj.SetMember('level', GfxValue(p.pkProtectLv))
        ar = movie.CreateArray()
        ar.SetElement(0, GfxValue(p.checkPkProtectMode(const.PK_PROTECT_MODE_GROUP)))
        ar.SetElement(1, GfxValue(p.checkPkProtectMode(const.PK_PROTECT_MODE_GUILD)))
        ar.SetElement(2, GfxValue(p.checkPkProtectMode(const.PK_PROTECT_MODE_CLAN)))
        ar.SetElement(3, GfxValue(p.checkPkProtectMode(const.PK_PROTECT_MODE_GREEN)))
        ar.SetElement(4, GfxValue(gbk2unicode(gameStrings.TEXT_PLAYERPROXY_431)))
        ar.SetElement(5, GfxValue(gbk2unicode(gameStrings.TEXT_PLAYERPROXY_432)))
        ar.SetElement(6, GfxValue(gbk2unicode(gameStrings.TEXT_PLAYERPROXY_433)))
        ar.SetElement(7, GfxValue(gbk2unicode(gameStrings.TEXT_PLAYERPROXY_434)))
        lvLowerLimit = utils.getLvLimit(p)
        ar.SetElement(8, GfxValue(gbk2unicode(gameStrings.TEXT_PLAYERPROXY_436 % lvLowerLimit)))
        ar.SetElement(9, GfxValue(p.checkPkProtectMode(const.PK_PROTECT_MODE_WHITE_ATTRACK_RED)))
        ar.SetElement(10, GfxValue(p.lv))
        ar.SetElement(11, GfxValue(lvLowerLimit))
        ar.SetElement(12, GfxValue(p.pkMode))
        ar.SetElement(13, GfxValue(not bool(p.getMapConfigPKProtectMode())))
        ar.SetElement(14, GfxValue(p.getMapConfigPKProtectLevel() == 0))
        ar.SetElement(15, GfxValue(self.isAdaptable()))
        obj.SetMember('ar', ar)
        enableClan = gameglobal.rds.configData.get('enableClan', False)
        obj.SetMember('enableClan', GfxValue(enableClan))
        return obj

    def isAdaptable(self):
        if gameglobal.rds.ui.huntGhost.isInHuntGhostArea():
            return False
        return True

    def onClosePKConfig(self, *arg):
        self.hidePkConfig()

    def hidePkConfig(self):
        self.pkMediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_PK_CONFIG)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.pkMediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_PK_CONFIG)

    def onConfirmPKConfig(self, *arg):
        ar = arg[3][0]
        p = BigWorld.player()
        newConfig = (ar.GetElement(0).GetBool(),
         ar.GetElement(1).GetBool(),
         ar.GetElement(2).GetBool(),
         ar.GetElement(3).GetBool(),
         ar.GetElement(4).GetBool())
        if newConfig[0] != p.checkPkProtectMode(const.PK_PROTECT_MODE_GROUP):
            p.cell.setPkProtectMode(const.PK_PROTECT_MODE_GROUP, newConfig[0])
        if newConfig[1] != p.checkPkProtectMode(const.PK_PROTECT_MODE_GUILD):
            p.cell.setPkProtectMode(const.PK_PROTECT_MODE_GUILD, newConfig[1])
        if newConfig[2] != p.checkPkProtectMode(const.PK_PROTECT_MODE_CLAN):
            p.cell.setPkProtectMode(const.PK_PROTECT_MODE_CLAN, newConfig[2])
        if newConfig[3] != p.checkPkProtectMode(const.PK_PROTECT_MODE_GREEN):
            p.cell.setPkProtectMode(const.PK_PROTECT_MODE_GREEN, newConfig[3])
        lvLowerLimit = utils.getLvLimit(p)
        if newConfig[4] != p.checkPkProtectMode(const.PK_PROTECT_MODE_WHITE_ATTRACK_RED) and p.lv >= lvLowerLimit:
            p.cell.setPkProtectMode(const.PK_PROTECT_MODE_WHITE_ATTRACK_RED, newConfig[4])

    def onConfirmLevel(self, *arg):
        p = BigWorld.player()
        if not arg[3][0].GetString():
            lvLowerLimit = utils.getLvLimit(p)
            p.showGameMsg(GMDD.data.PK_SET_LV_PROTECT_WRONG_LV, lvLowerLimit)
            return
        lv = int(arg[3][0].GetString())
        p.cell.setPkProtectLv(lv)
        self.hidePkConfig()

    def resetTimer(self):
        if self.binding.has_key('player.name'):
            self.binding['player.name'][0].Invoke('resetTimer')

    def refreshUnitType(self):
        p = BigWorld.player()
        self.setLv(p.realLv)

    def onGetVpDesc(self, *arg):
        return self.uiAdapter.roleInfo.onGetVpDesc()

    def showYaoli(self):
        value = BigWorld.player().inMLYaoLiSpace()
        if self.binding.has_key('player.showYaoli'):
            self.binding['player.showYaoli'][1].InvokeSelf(GfxValue(value))

    def showDoubleExp(self):
        value = BigWorld.player().inMLDoubleExpSpace()
        if self.binding.has_key('player.showDoubleExp') and gameglobal.rds.configData.get('enableDoubleExpPointInML', False):
            self.binding['player.showDoubleExp'][1].InvokeSelf(GfxValue(value))

    def reset(self):
        self.binding = {}
        self.mediator = None

    def onStartBattleFieldRelive(self, timeInterval):
        if self.mediator:
            self.mediator.Invoke('setDeadTimer', GfxValue(timeInterval))
        p = BigWorld.player()
        if timeInterval > 1 and not p.isInBfDota():
            txt = uiUtils.getTextFromGMD(GMDD.data.PLAYER_KNOW_THAT, gameStrings.TEXT_PLAYERPROXY_533)
            buttons = [MBButton(txt)]
            gameglobal.rds.ui.messageBox.show(True, gameStrings.TEXT_PLAYERPROXY_535, gameStrings.TEXT_PLAYERPROXY_535_1, buttons, repeat=timeInterval)

    def setReliveCountDown(self, timeInterval):
        if self.mediator:
            self.mediator.Invoke('setDeadTimer', GfxValue(timeInterval))

    def showPlayerUF(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_PLAYER_UF)

    def closePlayerUF(self):
        self.mediator = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PLAYER_UF)

    def needHidePlayerUF(self):
        p = BigWorld.player()
        if p.inFightObserve():
            return True
        return False

    def resetPlayerUFOpacity(self):
        if self.needHidePlayerUF():
            self.closePlayerUF()
        elif not self.mediator:
            self.showPlayerUF()

    def setHpPool(self, hpValue):
        needShow = self.needShowHpMpPoolIcon()
        if self.binding.has_key('player.hpPool'):
            hpValueStr = self.getHpMpPoolShowText(hpValue)
            self.binding['player.hpPool'][1].InvokeSelf((GfxValue(hpValueStr), GfxValue(needShow)))

    def setMpPool(self, mpValue):
        needShow = self.needShowHpMpPoolIcon()
        if self.binding.has_key('player.mpPool'):
            mpValueStr = self.getHpMpPoolShowText(mpValue)
            self.binding['player.mpPool'][1].InvokeSelf((GfxValue(mpValueStr), GfxValue(needShow)))

    def setFbAvoidDieCnt(self, num):
        if self.binding.has_key('player.fbAvoidDie'):
            if gameglobal.rds.configData.get('enableFbAvoidDieItem', False):
                self.binding['player.fbAvoidDie'][1].InvokeSelf(GfxValue(num))
                self.addFbAvoidDieTip()
            else:
                self.binding['player.fbAvoidDie'][1].InvokeSelf(GfxValue(0))

    def addHpToolTip(self):
        if not self.needShowHpMpPoolIcon():
            return
        if self.binding.has_key('player.addHpPoolTip'):
            tipStr = self.getHpPoolTip()
            self.binding['player.addHpPoolTip'][1].InvokeSelf(GfxValue(gbk2unicode(tipStr)))

    def addMpToolTip(self):
        if not self.needShowHpMpPoolIcon():
            return
        if self.binding.has_key('player.addMpPoolTip'):
            tipStr = self.getMpPoolTip()
            self.binding['player.addMpPoolTip'][1].InvokeSelf(GfxValue(gbk2unicode(tipStr)))

    def addFbAvoidDieTip(self):
        if not BigWorld.player().fbAvoidDieItemCnt:
            return
        if self.binding.has_key('player.addFbAvoidDieTip'):
            tipStr = self.getFbAvoidDieTip()
            self.binding['player.addFbAvoidDieTip'][1].InvokeSelf(GfxValue(gbk2unicode(tipStr)))

    def getHpMpPoolShowText(self, value):
        if value > POOL_TEXT_CONVERT_THRESHOLD:
            value = gbk2unicode('%dw' % int(value / POOL_TEXT_CONVERT_THRESHOLD))
        elif value <= 0:
            value = gbk2unicode(gameStrings.EMPTY_HP_MP_POOL)
        return value

    def getHpPoolTip(self):
        p = BigWorld.player()
        return SCD.data.get('hpPoolTipStr', 'hpPoolValue:%d') % p.hpPool

    def getMpPoolTip(self):
        p = BigWorld.player()
        return SCD.data.get('mpPoolTipStr', 'mpPoolValue:%d') % p.mpPool

    def getFbAvoidDieTip(self):
        p = BigWorld.player()
        itemId = SCD.data.get('returnFbAvoidDieItemId', 0)
        itemData = ID.data.get(itemId, {})
        funcDesc = itemData.get('funcDesc', '')
        pskId = SCD.data.get('fbAvoidDiePskId', 8752)
        validDesc = ''
        if pskId:
            fbNo = formula.getFubenNo(p.spaceNo)
            skillLevel = p.triggerPSkills[pskId].level if pskId in p.triggerPSkills else 1
            validFbNo = PD.data.get((pskId, skillLevel), {}).get('preConditonVal')
            if fbNo in validFbNo:
                validDesc = gameStrings.FB_AVOID_DIE_TIP_GREEN
            else:
                validDesc = gameStrings.FB_AVOID_DIE_TIP_RED
        tips = validDesc + '<BR>' + funcDesc
        return tips

    def needShowHpMpPoolIcon(self):
        p = BigWorld.player()
        lvLimit = SCD.data.get('hpMpPoolLvLimit', 20)
        return p.lv >= lvLimit and gameglobal.rds.configData.get('enableHpMpPool', False)

    def onClickHpPoolMc(self, *args):
        seekId = SCD.data.get('hpMpPoolStoreSeekId')
        uiUtils.findPosWithAlert(seekId)

    def onClickMpPoolMc(self, *args):
        seekId = SCD.data.get('hpMpPoolStoreSeekId')
        uiUtils.findPosWithAlert(seekId)

    def resetHpMpPool(self):
        p = BigWorld.player()
        self.setHpPool(p.hpPool)
        self.setMpPool(p.mpPool)
        self.addHpToolTip()
        self.addMpToolTip()

    def onClickFbAvoidDieMc(self, *args):
        e = ASObject(args[3][0])
        if e.buttonIdx != uiConst.RIGHT_BUTTON:
            return
        msg = SCD.data.get('returnFbAvoidDieItemMsg', '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self.returnFbAvoidDieItem)

    def getPlayerUnitFrameWidget(self):
        if not self.mediator:
            return None
        else:
            return ASObject(self.mediator).getWidget()

    def onInitPlayerUnitFrame(self, *args):
        widget = self.getPlayerUnitFrameWidget()
        if not widget:
            return
        p = BigWorld.player()
        defaultPhoto = 'headIcon/%s.dds' % str(p.school * 10 + p.physique.sex)
        widget.frame.playerIcon.headIcon.fitSize = True
        widget.frame.playerIcon.headIcon.loadImage(defaultPhoto)
        widget.frame.jobIcon.gotoAndStop(uiConst.SCHOOL_FRAME_DESC[BigWorld.player().school])
        widget.frame.tf_Level.visible = True
        self.updateBorderIcon()

    def updateBorderIcon(self):
        widget = self.getPlayerUnitFrameWidget()
        if not widget or not widget.frame.playerIcon:
            return
        p = BigWorld.player()
        if widget.frame.playerIcon:
            widget.frame.playerIcon.borderImg.fitSize = True
            borderIconPath = p.getPhotoBorderIcon(getattr(p, 'photoBorderId', 0), uiConst.PHOTO_BORDER_ICON_SIZE40)
            widget.frame.playerIcon.borderImg.loadImage(borderIconPath)
        photoBorderId = getattr(p, 'photoBorderId', 1)
        prefixBg = PBD.data.get(photoBorderId, {}).get('prefixBg', '')
        widget.frame.prefixBg = prefixBg
        widget.frame.setCombatVisible(p.inCombat)

    def returnFbAvoidDieItem(self):
        p = BigWorld.player()
        if not p:
            return
        num = p.fbAvoidDieItemCnt
        p.cell.revertFbAvoidItem(num)
