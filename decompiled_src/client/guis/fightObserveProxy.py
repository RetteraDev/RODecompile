#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fightObserveProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import formula
import uiUtils
import utils
from guis import ui
from guis import uiConst
from gamestrings import gameStrings
from uiProxy import DataProxy
from data import sys_config_data as SCD
import gametypes
OBSERVE_MODE_FOLLOW = 0
OBSERVE_MODE_FREE = 1

class FightObserveProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(FightObserveProxy, self).__init__(uiAdapter)
        self.modelMap = {'switchObserveFollow': self.onSwitchObserveFollow,
         'followSpecificTarget': self.onFollowSpecificTarget,
         'switchObserveFree': self.onSwitchObserveFree,
         'showFubenState': self.onShowFubenState,
         'leaveObserve': self.onLeaveObserve,
         'changeObserve': self.onChangeObserve,
         'getMonsterInfo': self.onGetMonsterInfo,
         'selectTarget': self.onSelectTarget,
         'showHelp': self.onShowHelp}
        self.type = 'fightObserve'
        self.actionBarMediator = None
        self.monsterBloodMediator = None
        self.monsters = {}
        self.isWin = False
        self.showHelp = True

    @property
    def curObTgtId(self):
        p = BigWorld.player()
        return p.gmFollow

    def getInitInfo(self):
        p = BigWorld.player()
        return {'helpMsg': SCD.data.get('shaXingActionBarHelpMsg', gameStrings.TEXT_AVOIDDOINGACTIVITYTIPPROXY_23),
         'isFree': self.getPlayerIsFree(),
         'showHelp': self.showHelp,
         'isInDota': p.isInBfDota(),
         'isInPUBG': p.isInPUBG()}

    def _registerMediator(self, widgetId, mediator):
        p = BigWorld.player()
        if widgetId == uiConst.WIDGET_FIGHT_OBSERVE_ACTION_BAR:
            self.actionBarMediator = mediator
            if p.isInBfDota():
                BigWorld.callback(0, self.onSwitchObserveFollow)
            return uiUtils.dict2GfxDict(self.getInitInfo(), True)
        if widgetId == uiConst.WIDGET_FIGHT_OBSERVE_MONSTER_BLOOD:
            self.monsterBloodMediator = mediator
            return uiUtils.dict2GfxDict({'info': self.onGetMonsterInfo()}, True)

    def showActionBar(self):
        if gameglobal.rds.configData.get('enableGuildTournamentLiveAndInspire', False) and gameglobal.rds.ui.bFGuildTournamentObserve.isAvaliable():
            gameglobal.rds.ui.bFGuildTournamentObserve.show()
        else:
            enableFightObserve = gameglobal.rds.configData.get('enableFightObserve', False)
            if not enableFightObserve:
                return
            if self.actionBarMediator:
                return
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FIGHT_OBSERVE_ACTION_BAR)
        self.hideOtherWidget()

    def hideOtherWidget(self):
        gameglobal.rds.ui.actionbar.refreshSkillActionBarOpacity()
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_ACTION_BARS, False)
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_ITEMBAR, False)
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_ITEMBAR, False)
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_ITEMBAR2, False)
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_WUSHUANG_BARS, False)
        gameglobal.rds.ui.bullet.setVisible(False)
        if gameglobal.rds.ui.qinggongBar.thisMc:
            gameglobal.rds.ui.qinggongBar.thisMc.SetVisible(False)

    def closeActionBar(self):
        p = BigWorld.player()
        if gameglobal.rds.ui.bFGuildTournamentObserve.widget:
            gameglobal.rds.ui.bFGuildTournamentObserve.hide()
        self.actionBarMediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FIGHT_OBSERVE_ACTION_BAR)
        if not gameglobal.rds.ui.isHideAllUI():
            gameglobal.rds.ui.actionbar.refreshSkillActionBarOpacity()
            itemMc = gameglobal.rds.ui.actionbar.itemMc
            if itemMc and not p.isInBfDota():
                for item in itemMc:
                    if item:
                        item.Invoke('setVisible', GfxValue(True))

                mc = gameglobal.rds.ui.actionbar.mc
                ws = gameglobal.rds.ui.actionbar.wsMc
                if mc:
                    mc.Invoke('setVisible', GfxValue(True))
                if ws:
                    ws.Invoke('setVisible', GfxValue(True))
        elif not p.isInBfDota():
            gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_ACTION_BARS, True)
            gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_ITEMBAR, True)
            gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_WUSHUANG_BARS, True)
            gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_ZAIJU, False)
            gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_ZAIJU_V2, False)
        gameglobal.rds.ui.actionbar.updateSlots()
        gameglobal.rds.ui.bullet.setVisible(True)
        if gameglobal.rds.ui.qinggongBar.thisMc:
            gameglobal.rds.ui.qinggongBar.thisMc.Invoke('forceVisibleByOther')
        if gameglobal.rds.ui.guildBusinessBag.mediator:
            gameglobal.rds.ui.guildBusinessBag.hide()

    def getPlayerIsFree(self):
        p = BigWorld.player()
        if p.isInPUBG():
            return False
        else:
            return p.inFlyTypeObserver()

    @ui.callFilter(2)
    def onSwitchObserveFollow(self, *arg):
        p = BigWorld.player()
        if p.isInBfDota():
            self.autoObSpecificTgb()
        else:
            p.cell.obRandomTgt()

    @ui.callFilter(2, True)
    def onChangeObserve(self, *args):
        p = BigWorld.player()
        if p.isInPUBG():
            self.autoObSpecificTgb()

    def autoObSpecificTgb(self):
        p = BigWorld.player()
        if not p or not p.inFightObserve():
            return
        entityIdsList = []
        if p.isInPUBG():
            entityIdsList = p.getOtherAliveTeamMateEntIdsInPUBG()
        elif p.isInBfDota():
            entityIdsList = p.getOtherAliveTeamMateEntityIds()
        targetId = self.getRealObTgtId(entityIdsList)
        if not targetId:
            if p.isInPUBG():
                pass
            else:
                p.cell.obRandomTgt()
        elif targetId != p.id and targetId != self.curObTgtId:
            if p.isInPUBG():
                p.cell.pubgObserve(targetId, p.getTeamMateGbIdByEntIdInPUBG(targetId))
            else:
                p.cell.obSpecificTgt(targetId)

    def getRealObTgtId(self, idList):
        if not idList:
            return 0
        if self.curObTgtId in idList:
            lastIdx = idList.index(self.curObTgtId)
            targetId = idList[(lastIdx + 1) % len(idList)]
        else:
            targetId = idList[0]
        return targetId

    @ui.callFilter(2)
    def onSwitchObserveFree(self, *arg):
        p = BigWorld.player()
        if p.isInBfDota():
            return
        p.cell.freeModeOb()

    def setSwitchMode(self, mode):
        if self.actionBarMediator:
            self.actionBarMediator.Invoke('setSwitchMode', GfxValue(mode))

    def inArenaPlayoffs(self):
        p = BigWorld.player()
        fbNo = formula.getFubenNo(p.spaceNo)
        if utils.inLiveOfArenaPlayoffs(p) and (utils.isCrossArenaPlayoffsFb(fbNo) or utils.isCrossArenaChallenge(fbNo)):
            return True
        return False

    def onShowFubenState(self, *arg):
        if self.inArenaPlayoffs():
            gameglobal.rds.ui.arena.showArenaTmpResult()
        else:
            gameglobal.rds.ui.fubenStat.show(None, True)

    def onLeaveObserve(self, *arg):
        p = BigWorld.player()
        if self.inArenaPlayoffs() or p.inClanChallengeOb():
            p.abortArena()
        elif p.isInPUBG():
            p.leavePUBG()
        else:
            p.cell.endObserveFuben()

    def onGetMonsterInfo(self, *arg):
        infos = []
        for monster in self.monsters.values():
            info = self.genMonsterInfo(monster)
            infos.append(info)

        monsterArray = uiUtils.array2GfxAarry(infos, True)
        return monsterArray

    def onSelectTarget(self, *arg):
        targetId = int(arg[3][0].GetNumber())
        target = BigWorld.entities.get(targetId)
        if target and target != BigWorld.player().targetLocked:
            BigWorld.player().lockTarget(target)

    def showMonsterBlood(self):
        enableFightObserve = gameglobal.rds.configData.get('enableFightObserve', False)
        if not enableFightObserve:
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_FIGHT_OBSERVE_MONSTER_BLOOD)

    def closeMonsterBlood(self):
        self.monsterBloodMediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FIGHT_OBSERVE_MONSTER_BLOOD)

    def removeMonster(self, monster):
        if not monster:
            return
        monsterId = monster.id
        if not self.monsters.has_key(monsterId):
            return
        self.monsters.pop(monsterId)
        if self.monsterBloodMediator:
            self.monsterBloodMediator.Invoke('removeMonster', GfxValue(monsterId))
        if not self.monsters:
            self.closeMonsterBlood()

    def genMonsterInfo(self, monster):
        monsterMap = {}
        lv = getattr(monster, 'lv', 0)
        if hasattr(monster, 'needHideTargetProxyLv') and monster.needHideTargetProxyLv():
            lv = 0
        monsterMap['lv'] = lv
        monsterMap['id'] = monster.id
        monsterMap['hp'] = monster.hp
        monsterMap['mhp'] = monster.mhp
        monsterMap['name'] = monster.roleName
        monsterMap['school'] = getattr(monster, 'school', 0)
        return monsterMap

    def addMonster(self, monster):
        if len(self.monsters) >= 5:
            return
        monsterId = monster.id
        if self.monsters.has_key(monsterId):
            return
        self.monsters[monsterId] = monster
        if self.monsterBloodMediator:
            monsterMap = self.genMonsterInfo(monster)
            self.monsterBloodMediator.Invoke('addMonster', uiUtils.dict2GfxDict(monsterMap, True))

    def showRaged(self, id, cd):
        if not self.monsterBloodMediator:
            return
        data = {}
        data['id'] = id
        data['cd'] = cd
        self.monsterBloodMediator.Invoke('showRaged', uiUtils.dict2GfxDict(data, True))

    def hideRaged(self, id):
        if not self.monsterBloodMediator:
            return
        data = {}
        data['id'] = id
        self.monsterBloodMediator.Invoke('hideRaged', uiUtils.dict2GfxDict(data, True))

    def setHp(self, monsterId, hp, mhp):
        if not self.monsterBloodMediator:
            return
        self.monsterBloodMediator.Invoke('setMonsterHp', (GfxValue(monsterId), GfxValue(hp), GfxValue(mhp)))

    def setMp(self, monsterId, mp, mmp):
        if not self.monsterBloodMediator:
            return
        self.monsterBloodMediator.Invoke('setMonsterMp', (GfxValue(monsterId), GfxValue(mp), GfxValue(mmp)))

    def resetObserveMode(self):
        p = BigWorld.player()
        if p.isInBfDota():
            return
        if BigWorld.player().inFly == gametypes.IN_FLY_OBSERVER:
            self.setSwitchMode(OBSERVE_MODE_FREE)
        else:
            self.setSwitchMode(OBSERVE_MODE_FOLLOW)

    def onFollowSpecificTarget(self, *arg):
        targetId = 0
        BigWorld.player().obSpecificTgt(targetId)

    def onShowHelp(self, *arg):
        showHelp = arg[3][0].GetBool()
        self.showHelp = showHelp
