#Embedded file name: /WORKSPACE/data/entities/common/cbgitemutils.o
import utils
import gameengine
from data import region_server_config_data as RSCD
CONSIGN_STATE_DEFAULT = 0
CONSIGN_STATE_SHOW = 1
CONSIGN_STATE_ON_BOARD = 2
CONSIGN_STATE_OFF_BOARD = 3
TAKE_BACK_TYPE_CONSIGN = 1
TAKE_BACK_TYPE_PURCHASE = 2

def getCrossCBGItemHostId(hostId = 0):
    hostId = hostId or utils.getHostId()
    return RSCD.data.get(hostId, {}).get('cbgItemRegionHostId', 0)


def getCrossCBGItemStub(hostId = 0):
    return gameengine.getGlobalStubByName('CrossCBGItemStub', utils.getServerName(getCrossCBGItemHostId(hostId)))
