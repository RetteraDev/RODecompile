#Embedded file name: I:/bag/tmp/tw2/res/entities\client\debug/monsterActionProxy.o
import BigWorld
from Scaleform import GfxValue
import gamelog
from guis.uiProxy import DataProxy
from guis import uiConst
from guis import uiUtils
from data import monster_model_client_data as MMCD

class MonsterActionProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(MonsterActionProxy, self).__init__(uiAdapter)
        self.bindType = 'monsterAction'
        self.modelMap = {'createMonster': self.onCreateMonster,
         'playMonsterAction': self.onPlayMonsterAction,
         'returnMonster': self.onReturnMonster,
         'sendMoedel': self.onSendModel}
        self.headGen = None
        self.mediator = None
        self.step = 0
        self.monsterData = []
        self.entMonster = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_MONSTER_ACTION_DEBUG:
            self.mediator = mediator

    def onCreateMonster(self, *arg):
        if self.step == 0:
            monsterId = int(arg[3][0].GetNumber())
            gamelog.debug('monsterId', monsterId)
            self.destroyMonster()
            param = {'charType': monsterId}
            p = BigWorld.player()
            spaceID = p.spaceID
            entityID = BigWorld.createEntity('Monster', spaceID, 0, p.position, (0, 0, p.yaw), param)
            self.entMonster = BigWorld.entity(entityID)
            self.entMonster.fashion.fobidHeadTrack = True
            self.checkMonsterAfterModelFinished()
        else:
            actionId = str(int(arg[3][0].GetNumber()))
            gamelog.debug('actionId', actionId)
            self._onPlayMonsterAction([actionId])

    def checkMonsterAfterModelFinished(self):
        if self.entMonster and self.entMonster.firstFetchFinished:
            ret = self.getMonsterAction(self.entMonster)
            self.step = 1
            if self.mediator:
                self.mediator.Invoke('setStepAndListData', (GfxValue(1), uiUtils.array2GfxAarry(ret, True)))
            return
        BigWorld.callback(1.0, self.checkMonsterAfterModelFinished)

    def onPlayMonsterAction(self, *arg):
        actionIds = arg[3][0].GetString()
        actionIds = actionIds.split(',')
        self._onPlayMonsterAction(actionIds)

    def _onPlayMonsterAction(self, actionIds):
        gamelog.debug('actionId', actionIds)
        if self.entMonster:
            model = self.entMonster.model
            self.entMonster.fashion.playActionSequence(model, actionIds, None)

    def onReturnMonster(self, *arg):
        if self.mediator:
            self.step = 0
            self.mediator.Invoke('setStepAndListData', (GfxValue(0), self.getValue('monsterAction.monsterData')))

    def getMonsterFile(self):
        self.monsterData = []
        for key, value in MMCD.data.iteritems():
            name = value.get('name', 'ÎÞÃûÐ¡×ä')
            model = value.get('model', 0)
            self.monsterData.append(':'.join((str(key), name, str(model))))

        self.monsterData.sort(cmp=lambda x, y: cmp(x.split(':')[0], y.split(':')[0]))
        return self.monsterData

    def getMonsterAction(self, monster):
        self.monsterData = []
        if monster.firstFetchFinished:
            for key, value in monster.model.actionNamePair():
                self.monsterData.append(':'.join((str(key), value)))

        return self.monsterData

    def getValue(self, key):
        if key == 'monsterAction.monsterData':
            return uiUtils.array2GfxAarry(self.getMonsterFile(), True)

    def show(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_MONSTER_ACTION_DEBUG)

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MONSTER_ACTION_DEBUG)

    def reset(self):
        self.mediator = None
        self.monsterData = []
        self.destroyMonster()
        self.step = 0

    def destroyMonster(self):
        if self.entMonster:
            BigWorld.destroyEntity(self.entMonster.id)
            self.entMonster = None

    def onSendModel(self, *arg):
        prefix = arg[3][0].GetString()
        gamelog.debug('onSendModel', prefix)
        if prefix == '' or not prefix.isdigit():
            return uiUtils.array2GfxAarry(self.monsterData, True)
        ret = []
        for item in self.monsterData:
            data = item.split(':')
            for key in data:
                if str(key)[:len(prefix)] == prefix:
                    ret.append(item)
                    break

        return uiUtils.array2GfxAarry(ret, True)
