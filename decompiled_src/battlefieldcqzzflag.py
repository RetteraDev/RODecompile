#Embedded file name: /WORKSPACE/data/entities/client/battlefieldcqzzflag.o
import BigWorld
import Math
import const
import clientUtils
import gametypes
from helpers import fashion
import gamelog
from sfx import sfx
import gameglobal
import gamelog
from helpers import modelServer
from helpers import tintalt
from iClient import IClient
from iDisplay import IDisplay
from data import battle_field_fort_data as BFFD
from data import duel_config_data as DCD
from cdata import game_msg_def_data as GMDD
defaultFlagsInfo = {1: {'model': 60051,
     'fKey': (2461, 2462),
     'fKeyRadius': 3,
     'flagName': 'flag'},
 2: {'model': 60051,
     'fKey': (2461, 2462),
     'fKeyRadius': 3,
     'flagName': 'enermyFlag'}}

class BattleFieldCqzzFlag(IClient, IDisplay):
    IsBattleFieldCqzzFlag = True

    def __init__(self):
        super(BattleFieldCqzzFlag, self).__init__()
        self.trapId = None
        self.roleName = ''

    def getItemData(self):
        flagsInfo = DCD.data.get('cqzzFlagInfo', defaultFlagsInfo)
        return flagsInfo.get(self.camp, {})

    def enterWorld(self):
        gamelog.debug('@zhangkuo CqzzFlag.enterWorld', self.position, self.id, self.camp, self.flagID)
        super(BattleFieldCqzzFlag, self).enterWorld()
        self.modelServer = modelServer.SimpleModelServer(self, self.isUrgentLoad())
        self.fashion = fashion.Fashion(self.id)
        flagInfo = self.getItemData()
        self.trapId = BigWorld.addPot(self.matrix, flagInfo.get('fKeyRadius', 3.0), self.trapCallback)
        self.filter = BigWorld.AvatarDropFilter()
        self.filter.disableSmooth = True
        self.roleName = flagInfo.get('flagName', '')

    def trapCallback(self, enteredTrap, handle):
        if enteredTrap:
            if not self.inWorld:
                return
            if not self.beHide:
                if self.state == gametypes.CQZZ_FLAG_STATE_FELL or self.state == gametypes.CQZZ_FLAG_STATE_DEFAULT:
                    gameglobal.rds.ui.pressKeyF.addEnt(self.id, const.F_BATTLE_FIELD_CQZZ_FLAG)
        else:
            gameglobal.rds.ui.pressKeyF.delEnt(self.id, const.F_BATTLE_FIELD_CQZZ_FLAG)

    def hide(self, bHide, retainTopLogo = False):
        super(BattleFieldCqzzFlag, self).hide(bHide, retainTopLogo)
        if bHide:
            if self.trapId:
                BigWorld.delPot(self.trapId)
                self.trapId = None
            gameglobal.rds.ui.pressKeyF.delEnt(self.id, const.F_BATTLE_FIELD_CQZZ_FLAG)
        elif not self.trapId:
            flagInfo = self.getItemData()
            self.trapId = BigWorld.addPot(self.matrix, flagInfo.get('fKeyRadius', 3.0), self.trapCallback)

    def getFKey(self):
        p = BigWorld.player()
        fKeys = self.getItemData().get('fKey', (0, 0))
        if self.camp != p.tempCamp:
            return fKeys[0]
        else:
            return fKeys[1]

    def leaveWorld(self):
        super(BattleFieldCqzzFlag, self).leaveWorld()
        if self.trapId:
            gameglobal.rds.ui.pressKeyF.delEnt(self.id, const.F_BATTLE_FIELD_CQZZ_FLAG)
        gamelog.debug('@zhangkuo CqzzFlag.leaveWorld', self.position, self.id)

    def afterModelFinish(self):
        super(BattleFieldCqzzFlag, self).afterModelFinish()
        self.model.setModelNeedHide(0, 0.5)
        self.model.action('1101')()
        self.filter = BigWorld.AvatarDropFilter()
        self.filter.disableSmooth = True
        self.attachSfxEffect()

    def attachSfxEffect(self):
        effects = ''
        eScale = 1
        if effects and effects != self.effects:
            self.effects = effects
            for effectId in effects:
                efs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
                 gameglobal.EFF_HIGHEST_PRIORITY,
                 self.model,
                 effectId,
                 sfx.EFFECT_UNLIMIT))
                if efs:
                    self.statusFx[effectId] = efs
                    for ef in efs:
                        ef and ef.scale(eScale)

    def releaseSfxEffect(self):
        if self.statusFx:
            for effectId in self.statusFx.keys():
                sfx.detachEffect(self.model, effectId, self.statusFx[effectId], True)

            self.statusFx = {}
            self.effects = []

    def _getModelId(self):
        return self.getItemData().get('modelId')

    def getModelScale(self):
        scale = self.getItemData().get('scale', 1)
        return (scale, scale, scale)

    def use(self):
        p = BigWorld.player()
        gamelog.debug('@dxk BattleFiledCqzzFlag pickflag', p.id, self.id)
        if self.camp == p.tempCamp and self.state == gametypes.CQZZ_FLAG_STATE_DEFAULT:
            p.showGameMsg(GMDD.data.FORBIDDEN_PICK_CQZZ_INITFLAG, ())
        else:
            p.base.pickCqzzFlag(self.id)
