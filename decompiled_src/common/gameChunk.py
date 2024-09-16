#Embedded file name: I:/bag/tmp/tw2/res/entities\common/gameChunk.o
import BigWorld
CHUNK_FLAG_SAFETY_ZONE = 1
CHUCK_FLAG_FREE_PK = 2
CHUCK_FLAG_BAI_TAN = 4
CHUCK_FLAG_FLY = 8
CHUCK_FLAG_BORDER = 16
CHUNK_FLAG_CLAN_WAR = 32

def resideInSafetyZone(ent):
    f = _readAiInfo(ent)
    return f & CHUNK_FLAG_SAFETY_ZONE != 0


def resideInFreePk(ent):
    f = _readAiInfo(ent)
    return f & CHUCK_FLAG_FREE_PK != 0


def resideInBooth(ent):
    f = _readAiInfo(ent)
    return f & CHUCK_FLAG_BAI_TAN != 0


def resideInFly(ent):
    f = _readAiInfo(ent)
    return f & CHUCK_FLAG_FLY != 0


def checkFlag(aiinfo, chkTyp):
    return aiinfo & chkTyp != 0


def resideInBorderZone(ent):
    f = _readAiInfo(ent)
    return f & CHUCK_FLAG_BORDER != 0


def resideInClanWarZone(ent):
    f = _readAiInfo(ent)
    return f & CHUNK_FLAG_CLAN_WAR != 0


def _readAiInfo(ent):
    if BigWorld.component == 'client':
        f = BigWorld.aiInfoAt(ent.position)
    elif BigWorld.component == 'cell':
        f = ent.aiInfoAt(ent.position)
    else:
        f = 0
    return f
