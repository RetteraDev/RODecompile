#Embedded file name: I:/bag/tmp/tw2/res/entities\client\debug/npcActionProxy.o
import BigWorld
from Scaleform import GfxValue
import gamelog
import gameglobal
from guis.uiProxy import DataProxy
from guis import uiConst
from guis import uiUtils
from data import npc_model_client_data as NMCD

class NpcActionProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(NpcActionProxy, self).__init__(uiAdapter)
        self.bindType = 'npcAction'
        self.modelMap = {'createNpc': self.onCreateNpc,
         'playNpcAction': self.onPlayNpcAction,
         'returnNpc': self.onReturnNpc,
         'sendMoedel': self.onSendModel}
        self.npcData = []
        self.entNpc = None
        self.headGen = None
        self.mediator = None
        self.step = 0

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_NPC_ACTION:
            self.mediator = mediator

    def onCreateNpc(self, *arg):
        if self.step == 0:
            npcId = int(arg[3][0].GetNumber())
            gamelog.debug('npcId', npcId)
            self.destroyNpc()
            param = {'roleName': '调试动作npc',
             'petName': '调试动作npc',
             'showLogo': True,
             'npcId': npcId,
             'isScenario': gameglobal.NORMAL_NPC}
            p = BigWorld.player()
            spaceID = p.spaceID
            entityID = BigWorld.createEntity('Dawdler', spaceID, 0, p.position, (0, 0, p.yaw), param)
            self.entNpc = BigWorld.entity(entityID)
            self.entNpc.fashion.fobidHeadTrack = True
            self.checkNpcAfterModelFinished()
        else:
            actionId = str(int(arg[3][0].GetNumber()))
            gamelog.debug('actionId', actionId)
            self._onPlayNpcAction([actionId])

    def checkNpcAfterModelFinished(self):
        if self.entNpc and self.entNpc.firstFetchFinished:
            ret = self.getNpcAction(self.entNpc)
            self.step = 1
            if self.mediator:
                self.mediator.Invoke('setStepAndListData', (GfxValue(1), uiUtils.array2GfxAarry(ret, True)))
            return
        BigWorld.callback(1.0, self.checkNpcAfterModelFinished)

    def onPlayNpcAction(self, *arg):
        actionIds = arg[3][0].GetString()
        actionIds = actionIds.split(',')
        self._onPlayNpcAction(actionIds)

    def _onPlayNpcAction(self, actionIds):
        gamelog.debug('actionId', actionIds)
        if self.entNpc:
            model = self.entNpc.model
            self.entNpc.fashion.playActionSequence(model, actionIds, None)

    def onReturnNpc(self, *arg):
        if self.mediator:
            self.step = 0
            self.mediator.Invoke('setStepAndListData', (GfxValue(0), self.getValue('npcAction.npcData')))

    def getNpcFile(self):
        self.npcData = []
        for key, value in NMCD.data.iteritems():
            name = value.get('name', '无名小卒')
            model = value.get('model', 0)
            self.npcData.append(':'.join((str(key), name, str(model))))

        self.npcData.sort(cmp=lambda x, y: cmp(x.split(':')[0], y.split(':')[0]))
        return self.npcData

    def getNpcAction(self, npc):
        self.npcData = []
        if npc.firstFetchFinished:
            for key, value in npc.model.actionNamePair():
                self.npcData.append(':'.join((str(key), value)))

        return self.npcData

    def getValue(self, key):
        if key == 'npcAction.npcData':
            return uiUtils.array2GfxAarry(self.getNpcFile(), True)

    def show(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_NPC_ACTION)

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_NPC_ACTION)

    def reset(self):
        self.mediator = None
        self.npcData = []
        self.destroyNpc()
        self.step = 0

    def destroyNpc(self):
        if self.entNpc:
            BigWorld.destroyEntity(self.entNpc.id)
            self.entNpc = None

    def onSendModel(self, *arg):
        prefix = arg[3][0].GetString()
        gamelog.debug('onSendModel', prefix)
        if prefix == '' or not prefix.isdigit():
            return uiUtils.array2GfxAarry(self.npcData, True)
        ret = []
        for item in self.npcData:
            data = item.split(':')
            for key in data:
                if str(key)[:len(prefix)] == prefix:
                    ret.append(item)
                    break

        return uiUtils.array2GfxAarry(ret, True)
