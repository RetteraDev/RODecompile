#Embedded file name: I:/bag/tmp/tw2/res/entities\client/iPot.o
import BigWorld
import const
import gameglobal
from iClient import IClient
from helpers import modelServer
from sfx import sfx
from data import pot_data as PD

class IPot(IClient):
    TOPLOGO_OFFSET = 0.5
    POT_RADII = 1.0
    IsPot = True

    def __init__(self):
        super(IPot, self).__init__()
        self.firstFetchFinished = False
        self.hasTriggered = False
        self._reset()

    def _reset(self):
        if getattr(self, 'trapId', None):
            BigWorld.delPot(self.trapId)
            self.trapId = None
        else:
            self.trapId = None
        self.radii = PD.data.get(self.potId, {}).get('radii', IPot.POT_RADII)
        self.topLogoOffset = PD.data.get(self.potId, {}).get('logoOffset', IPot.TOPLOGO_OFFSET)

    def getItemData(self):
        pd = PD.data.get(self.potId, {'model': gameglobal.defaultModelID})
        return pd

    def enterWorld(self):
        super(IPot, self).enterWorld()
        self.modelServer = modelServer.SimpleModelServer(self)
        self.refreshOpacityState()

    def _enableTrap(self, flag):
        if not self.inWorld:
            return
        if flag:
            if self.enable and not self.trapId:
                self.trapId = BigWorld.addPot(self.matrix, self.radii, self.trapCallback)
        elif self.trapId:
            BigWorld.delPot(self.trapId)
            self.trapId = None

    def _checkQuest(self, allFailed = True):
        p = BigWorld.player()
        pd = self.getItemData()
        quests = pd.get('quests', ())
        if quests:
            hasQuest = False
            for questId in quests:
                if questId in p.quests:
                    hasQuest = True
                    if not p.getQuestData(questId, const.QD_FAIL, False):
                        allFailed = False

            if not hasQuest or allFailed:
                return False
        return True

    def trapCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        if enteredTrap:
            p = BigWorld.player()
            if (self.position - p.position).lengthSquared > self.radii * self.radii:
                return
            if not self._checkQuest():
                return
            pd = self.getItemData()
            flySpeed = pd.get('flySpeed', 0)
            if flySpeed:
                self.flyToPlayer()
            else:
                p.cell.potTrigger(self.potId, self.id)

    def flyToPlayer(self):
        self.hasTriggered = True
        if getattr(self, 'firstFetchFinished', False):
            self._realFlyToPlayer()

    def _realFlyToPlayer(self):
        player = BigWorld.player()
        mot = BigWorld.Rlauncher()
        self.model.addMotor(mot)
        mot.target = player.matrix
        self.am.enable = False
        mot.speed = self.getItemData().get('flySpeed', 0)
        mot.acceleration = 4
        mot.proximity = 0.5
        mot.curvature = 0.2
        mot.zroll = 0
        mot.rotateSpeed = (0, 0, 0)
        mot.proximityCallback = self.flyApproach

    def flyApproach(self):
        if not self.inWorld:
            return
        self.removeAllFx()
        self.triggerEff()
        player = BigWorld.player()
        player.cell.potTrigger(self.potId, self.id)

    def needBlackShadow(self):
        return False

    def afterModelFinish(self):
        super(IPot, self).afterModelFinish()
        self.firstFetchFinished = True
        self.initYaw = self.yaw
        self.setTargetCapsUse(False)
        self.noSelected = True
        self.set_enable(self.enable)
        self.refreshOpacityState()
        if self.hasTriggered:
            self._realFlyToPlayer()

    def getTopLogoHeight(self):
        return self.getItemData().get('logoOffset', IPot.TOPLOGO_OFFSET)

    def leaveWorld(self):
        super(IPot, self).leaveWorld()
        self._enableTrap(False)

    def set_enable(self, old):
        self._enableTrap(self.enable)
        if self.enable and not old:
            self.modelServer.attachModelFromData()

    def afterTrigger(self, playerId):
        if not self.inWorld:
            return
        if BigWorld.player().id == playerId:
            pd = PD.data.get(self.potId, {})
            timeTune = pd.get('timeTune', None)
            maxTimeTune = pd.get('maxTimeTune', -60)
            if timeTune:
                questId, tuneTime = timeTune
                p = BigWorld.player()
                if questId in p.quests:
                    p.setJingSuTuneTime(tuneTime, maxTimeTune)
        self.triggerAction()
        flySpeed = self.getItemData().get('flySpeed', 0)
        if not flySpeed:
            self.triggerEff()
        self.triggerSound()

    def triggerAction(self):
        pd = self.getItemData()
        triggerAction = pd.get('triggerAction', '')
        if triggerAction:
            if triggerAction in self.fashion.getActionNameList():
                self.model.action(triggerAction)()

    def triggerEff(self):
        pd = self.getItemData()
        interval = pd.get('interval', 0)
        if interval:
            self.removeAllFx()
        triggerEff = pd.get('triggerEff', 0)
        triggerEffScale = pd.get('triggerEffScale', 1.0)
        if triggerEff:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
             self.getBasicEffectPriority(),
             self.model,
             triggerEff,
             sfx.EFFECT_UNLIMIT))
            if fx:
                if triggerEffScale:
                    for fxItem in fx:
                        fxItem.scale(triggerEffScale, triggerEffScale, triggerEffScale)

                self.addFx(triggerEff, fx)

    def triggerSound(self):
        pd = self.getItemData()
        triggerSound = pd.get('triggerSound', 0)
        if triggerSound:
            BigWorld.player().playSound(triggerSound, None)

    def getModelScale(self):
        pd = self.getItemData()
        scale = pd.get('modelScale', 1.0)
        self.model.scale = (scale, scale, scale)
        return (scale, scale, scale)

    def refreshOpacityState(self):
        if not self._checkQuest(False):
            self.hide(True)
            self._enableTrap(False)
            return
        self.hide(False)
        self._enableTrap(True)

    def set_potId(self, old):
        if not self.inWorld:
            return
        if not self.firstFetchFinished:
            return
        self.removeAllFx()
        self._reset()
        if self.enable:
            self.modelServer.attachModelFromData()
        self._enableTrap(self.enable)
        self.refreshOpacityState()
