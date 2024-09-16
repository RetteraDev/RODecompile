#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/modelRobber.o
import BigWorld
import gameglobal
import clientcom
from helpers import fashion
from helpers import tintalt
from helpers import modelServer
from gameclass import Singleton
from callbackHelper import Functor

class ModelRobber(object):
    __metaclass__ = Singleton

    def __init__(self):
        super(ModelRobber, self).__init__()
        self.reset()

    def reset(self):
        self.monsters = set()
        self.npcInfo = {}

    def isMonsterRobber(self, entId):
        return entId in self.monsters

    def isActiveNpc(self, entId, npcId):
        en = BigWorld.entity(entId)
        if npcId and en and en.inWorld and getattr(en, 'firstFetchFinished', False) and getattr(en, 'npcId', 0) == npcId:
            if entId not in self.npcInfo:
                return True
        return False

    def addRobInfo(self, monsterEntId, npcEntId):
        if npcEntId not in self.npcInfo:
            self.npcInfo[npcEntId] = monsterEntId
            self.monsters.add(monsterEntId)

    def removeRobInfoByNpc(self, npcEntId):
        if npcEntId in self.npcInfo.keys():
            monsterEntId = self.npcInfo.pop(npcEntId)
            if monsterEntId in self.monsters:
                self.monsters.remove(monsterEntId)
                return True
        return False

    def removeRobInfoByMonster(self, monsterEntId):
        if self.isMonsterRobber(monsterEntId):
            for key, value in self.npcInfo.items():
                if value == monsterEntId:
                    return self.removeRobInfoByNpc(key)

        return False

    def findActiveNpc(self, monsterEnt):
        npcId = monsterEnt.hideNpcId
        ents = BigWorld.entities.values()
        for ent in ents:
            if self.isActiveNpc(ent.id, npcId):
                monsterModelId = monsterEnt.getItemData().get('model', 0)
                entModelId = ent.getItemData().get('model', 0)
                if monsterModelId and entModelId and entModelId == monsterModelId:
                    return ent.id

    def tryRobModel(self, monsterEnt):
        if not gameglobal.rds.configData.get('enableRobModel', False):
            return False
        npcEntId = self.findActiveNpc(monsterEnt)
        if npcEntId:
            self.addRobInfo(monsterEnt.id, npcEntId)
            npcEnt = BigWorld.entity(npcEntId)
            model = npcEnt.model
            npcEnt.fashion.loadDummyModel()
            model.motors = ()
            monsterEnt.fashion = fashion.Fashion(monsterEnt.id)
            monsterEnt.modelServer = modelServer.SimpleModelServer(monsterEnt, monsterEnt.isUrgentLoad(), False, False)
            BigWorld.callback(0, Functor(monsterEnt.modelServer._singlePartModelFinish, model))
            BigWorld.player().hideQuestNpcByMonster(monsterEnt.hideNpcId)
            return True
        return False

    def tryRobAvatarModel(self, monsterEnt):
        if not gameglobal.rds.configData.get('enableRobAvatarModel', False):
            return False
        npcEntId = self.findActiveNpc(monsterEnt)
        if npcEntId:
            self.addRobInfo(monsterEnt.id, npcEntId)
            npcEnt = BigWorld.entity(npcEntId)
            model = npcEnt.model
            npcEnt.fashion.loadDummyModel()
            model.motors = ()
            BigWorld.callback(0, Functor(self.setupAvatarModel, monsterEnt.id, model))
            BigWorld.player().hideQuestNpcByMonster(monsterEnt.hideNpcId)
            return True
        return False

    def setupAvatarModel(self, avatarMonsterId, model):
        monsterEnt = BigWorld.entity(avatarMonsterId)
        if monsterEnt and monsterEnt.inWorld:
            monsterEnt.initYaw = monsterEnt.yaw
            monsterEnt.filter = BigWorld.AvatarDropFilter()
            monsterEnt.modelServer.bodyModel = monsterEnt.model
            monsterEnt.modelServer._bodyModelFinish(model)
            monsterEnt.modelServer.weaponUpdate()

    def tryReturnModel(self, monsterEnt):
        if self.isMonsterRobber(monsterEnt.id):
            for npcEntId, value in self.npcInfo.items():
                if value == monsterEnt.id:
                    self.removeRobInfoByNpc(npcEntId)
                    npcEnt = BigWorld.entity(npcEntId)
                    if npcEnt and npcEnt.inWorld:
                        model = monsterEnt.model
                        model.motors = ()
                        if model in monsterEnt.allModels:
                            monsterEnt.allModels.remove(model)
                        monsterEnt.fashion.loadDummyModel()
                        npcEnt.fashion.setupModel(model)
                        npcEnt.afterModelFinish()
                        dye = clientcom.getMatrialsName(npcEnt, npcEnt.getItemData())
                        if dye != 'DefaultMatter':
                            tintalt.ta_set_static([model], dye)


def getInstance():
    return ModelRobber.getInstance()
