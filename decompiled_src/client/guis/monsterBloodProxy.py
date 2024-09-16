#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/monsterBloodProxy.o
import BigWorld
from Scaleform import GfxValue
import ui
import uiConst
import uiUtils
import gameglobal
from uiProxy import UIProxy

class MonsterBloodProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MonsterBloodProxy, self).__init__(uiAdapter)
        self.modelMap = {'groupMonsterInfo': self.onGroupMonsterInfo,
         'clickMonsterItem': self.onClickMonsterItem}
        self.mediator = None
        self.castTestHandler = None
        self.groupMonsterArray = []
        self.canFindMonsterList = []

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_MONSTER_BLOOD:
            self.mediator = mediator
            if self.castTestHandler:
                BigWorld.cancelCallback(self.castTestHandler)
            self.castTestHandler = BigWorld.callback(0.2, self.refreshCanFindMonster)

    @ui.scenarioCallFilter()
    def show(self):
        if gameglobal.rds.configData.get('enableMonsterBlood', False):
            self.uiAdapter.loadWidget(uiConst.WIDGET_MONSTER_BLOOD)

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MONSTER_BLOOD)

    def reset(self):
        self.mediator = None
        self.groupMonsterArray = []
        self.canFindMonsterList = []
        if self.castTestHandler:
            BigWorld.cancelCallback(self.castTestHandler)
            self.castTestHandler = None

    def onGroupMonsterInfo(self, *arg):
        monsterArray = uiUtils.array2GfxAarry(self.groupMonsterArray, True)
        return monsterArray

    def removeMonster(self, monsterId):
        if gameglobal.rds.configData.get('enableMonsterBlood', False):
            for monsterItem in self.groupMonsterArray:
                if monsterItem['id'] == monsterId:
                    self.groupMonsterArray.remove(monsterItem)
                    if self.mediator:
                        self.mediator.Invoke('removeMonster', GfxValue(monsterId))
                        break

            if self.groupMonsterArray == []:
                self.hide()

    def addMonster(self, monsterId, roleName, hp, mhp):
        if gameglobal.rds.configData.get('enableMonsterBlood', False):
            if len(self.groupMonsterArray) >= 5:
                return
            monsterMap = {}
            monsterMap['id'] = monsterId
            monsterMap['name'] = roleName
            value = float(hp) / float(mhp) * 100
            strValue = str('%.1f' % value)
            monsterMap['hp'] = strValue
            self.groupMonsterArray.append(monsterMap)
            if self.mediator:
                self.mediator.Invoke('addMonster', uiUtils.dict2GfxDict(monsterMap, True))
                if len(self.groupMonsterArray) == 1:
                    if self.castTestHandler:
                        BigWorld.cancelCallback(self.castTestHandler)
                    self.castTestHandler = BigWorld.callback(0.2, self.refreshCanFindMonster)

    def setHp(self, monsterId, hp, mhp):
        if not self.mediator:
            return
        for monsterItem in self.groupMonsterArray:
            if monsterItem['id'] == monsterId:
                value = float(hp) / float(mhp) * 100
                strValue = str('%.1f' % value)
                self.mediator.Invoke('setMonsterHp', (GfxValue(monsterId), GfxValue(strValue)))

    def onClickMonsterItem(self, *arg):
        entId = int(arg[3][0].GetNumber())
        ent = BigWorld.entities.get(entId)
        if ent:
            uiUtils.onTargetSelect(ent)

    def setLockMonster(self, monsterId):
        if self.mediator:
            self.mediator.Invoke('setSelect', GfxValue(monsterId))
        if gameglobal.rds.ui.fightObserve.monsterBloodMediator:
            gameglobal.rds.ui.fightObserve.monsterBloodMediator.Invoke('showSelected', GfxValue(monsterId))

    def setUnlockMonster(self):
        if self.mediator:
            self.mediator.Invoke('unSelect')

    def refreshCanFindMonster(self):
        if not self.groupMonsterArray:
            return
        ret = []
        for monsterItem in self.groupMonsterArray:
            ent = BigWorld.entities.get(monsterItem['id'])
            canCastSkill = False
            if ent:
                canCastSkill = uiUtils.canCastSkill(ent)
                ret.append((monsterItem['id'], canCastSkill))

        if self.canFindMonsterList != ret:
            self.canFindMonsterList = ret
            self.mediator.Invoke('refreshCanFindMonster', uiUtils.array2GfxAarry(ret))
        if self.castTestHandler:
            BigWorld.cancelCallback(self.castTestHandler)
        self.castTestHandler = BigWorld.callback(0.3, self.refreshCanFindMonster)
