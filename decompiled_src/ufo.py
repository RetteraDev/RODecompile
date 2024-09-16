#Embedded file name: /WORKSPACE/data/entities/client/helpers/ufo.o
import BigWorld
import Pixie
import keys
import gameglobal
import gamelog
import clientUtils
from sfx import sfx
from data import sys_config_data as SYSCD
UFO_NULL = -1
UFO_NORMAL = 1
UFO_NORMAL_AIR = 2
UFO_ATK_ENEMY = 3
UFO_ATK_ENEMY_AIR = 4
UFO_PASSIVE_ENEMY = 5
UFO_PASSIVE_ENEMY_AIR = 6
UFO_DEAD = 7
UFO_SHADOW = keys.COLOR_SHADOW
SELECTOR_ARGS_MAP = {UFO_NULL: (False,),
 UFO_NORMAL: (True, 'green'),
 UFO_NORMAL_AIR: (True, 'green'),
 UFO_ATK_ENEMY: (True, 'red'),
 UFO_ATK_ENEMY_AIR: (True, 'red'),
 UFO_PASSIVE_ENEMY: (True, 'yellow'),
 UFO_PASSIVE_ENEMY_AIR: (True, 'yellow'),
 UFO_DEAD: (False,),
 UFO_SHADOW: (False,)}
UFO_RES = {UFO_SHADOW: SYSCD.data.get('ufoShadow', gameglobal.SFX_UFO_SHADOW),
 UFO_NORMAL: SYSCD.data.get('sfxUfoNormal', gameglobal.SFX_UFO_NORMAL),
 UFO_NORMAL_AIR: sfx.getPath(SYSCD.data.get('sfxUfoNormalAir', gameglobal.SFX_UFO_NORMAL_AIR)),
 UFO_PASSIVE_ENEMY: SYSCD.data.get('sfxUfoPassiveEnemy', gameglobal.SFX_UFO_PASSIVE_ENEMY),
 UFO_PASSIVE_ENEMY_AIR: sfx.getPath(SYSCD.data.get('sfxUfoPassiveEnemyAir', gameglobal.SFX_UFO_PASSIVE_ENEMY_AIR)),
 UFO_ATK_ENEMY: SYSCD.data.get('sfxUfoAtkEnemy', gameglobal.SFX_UFO_ATK_ENEMY),
 UFO_ATK_ENEMY_AIR: sfx.getPath(SYSCD.data.get('sfxUfoAtkEnemyAir', gameglobal.SFX_UFO_ATK_ENEMY_AIR)),
 UFO_DEAD: SYSCD.data.get('sfxUfoDead', gameglobal.SFX_UFO_DEAD)}
UFO_TYPE_NOT_FX = (UFO_NULL,
 UFO_NORMAL,
 UFO_ATK_ENEMY,
 UFO_PASSIVE_ENEMY,
 UFO_DEAD,
 UFO_SHADOW)

class UFOOBj(object):

    def __init__(self, ufoType):
        super(UFOOBj, self).__init__()
        if ufoType in UFO_TYPE_NOT_FX:
            ufoRes = UFO_RES[ufoType]
            if hasattr(BigWorld, 'useDecalUFO') and ufoType == UFO_SHADOW:
                ufoRes = gameglobal.SFX_UFO_NEW_SHADOW
            self.obj = BigWorld.UFO(ufoRes)
            self.obj.maxLod = 15.0
            self.obj.minShowUfoDist = gameglobal.rds.minShowUfoDist
            self.obj.clipUnderWater = True
        else:
            self.obj = clientUtils.pixieFetch(UFO_RES[ufoType])
            self.obj.setAttachMode(0, 1, 0)
            self.obj.force()
        self.ufoType = ufoType


class UFOMgr(object):

    def __init__(self):
        super(UFOMgr, self).__init__()
        self.cache = {}

    def getUFO(self, ufoType):
        if ufoType == UFO_SHADOW:
            return UFOOBj(ufoType)
        if self.cache.has_key(ufoType):
            return self.cache[ufoType]
        self.cache[ufoType] = UFOOBj(ufoType)
        return self.cache[ufoType]

    def giveBack(self, ufoObj):
        pass

    def clear(self):
        pass


_gUfoMgr = None

def getUFO(ufoType):
    global _gUfoMgr
    if ufoType >= keys.COLOR_MON_0:
        ufoType = keys.COLOR_MON_PK5
    gamelog.debug('getUFO..........', ufoType)
    if _gUfoMgr == None:
        _gUfoMgr = UFOMgr()
    return _gUfoMgr.getUFO(ufoType)


def giveBack(ufoObj):
    _gUfoMgr.giveBack(ufoObj)


def clearCache():
    if _gUfoMgr:
        _gUfoMgr.clear()
