#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/protect.o
import BigWorld
import NEProtect
import gamelog
import gameglobal
import utils
gNEProtectEnable = True
gNEProtectName = 'ty'
gNEProtectServer = '0D9440E828D715838E9AA98DD5D53987BA3F56200ADBE20C56'
gNEProtectCode = 1900
gNEProtectLNP = 2047391196
if utils.isInternationalVersion():
    gNEProtectServer = '5AD9F15D386AD3DF13AD86B282BAA287C1F151D9DA50'
    gNEProtectLNP = 3263353795L

def nepInit():
    global gNEProtectServer
    global gNEProtectCode
    global gNEProtectEnable
    global gNEProtectLNP
    global gNEProtectName
    if not gNEProtectEnable:
        return
    try:
        rs = NEProtect.init(gNEProtectName, gNEProtectServer, gNEProtectCode, gNEProtectLNP)
        gamelog.debug('jjh@nepInit ', gNEProtectName, gNEProtectServer, gNEProtectCode, gNEProtectLNP, rs)
    except:
        pass


def nepChooseServer(serverId, serverName):
    if not gNEProtectEnable:
        return
    try:
        hostId = int(serverId)
        rs = NEProtect.chooseServer(hostId, serverName)
        gamelog.debug('jjh@nepChooseServer ', hostId, serverName, rs)
    except:
        pass


def nepRoleLogin(account, role, gbId, lv):
    if not gNEProtectEnable:
        return
    try:
        rs = NEProtect.roleLogin(account, role, gbId, lv)
        gamelog.debug('jjh@nepRoleLogin ', account, role, gbId, lv, rs)
    except:
        pass


def nepRoleLogout(account, gbId):
    if not gNEProtectEnable:
        return
    try:
        rs = NEProtect.roleLogout(account, gbId)
        gamelog.debug('jjh@nepRoleLogout ', account, gbId, rs)
    except:
        pass


def nepShutdown():
    try:
        NEProtect.shutdown()
        gamelog.debug('jjh@nepShutdown ')
    except:
        pass


def nepLimitClientNum(limitNum, protectNow):
    if not BigWorld.isPublishedVersion() or not gNEProtectEnable:
        return 0
    try:
        return NEProtect.limitClientNum(limitNum, protectNow)
    except:
        return 0


def nepCheckAccelerator():
    if not gNEProtectEnable:
        return 0
    try:
        return NEProtect.checkAccelerator()
    except:
        return 0


NEMAP_UNKOWN = 0
NEMAP_SAFE = 1
NEMAP_BOOTH = 2
NEMAP_PK = 3
NEMAP_FB = 4

def nepActionUpdateMap(mapType, dwMapID):
    if not gNEProtectEnable:
        return
    enableNepSync = gameglobal.rds.configData.get('enableNepSync', False)
    if not enableNepSync:
        return
    try:
        NEProtect.nepActionUpdateMap(mapType, dwMapID)
    except:
        pass


eNEActivity_Default = 0
eNEActivity_KMonster = 1
eNEActivity_Collect = 2
eNEActivity_Pickup = 3
eNEActivity_DupTask = 4
eNEActivity_TeachTask = 5
eNEActivity_MainTask = 6

def nepActionRoleActivity(activityType, dwActivityID, dwObjectID, dwObjectSum):
    if not gNEProtectEnable:
        return
    enableNepSync = gameglobal.rds.configData.get('enableNepSync', False)
    if not enableNepSync:
        return
    try:
        NEProtect.nepActionRoleActivity(activityType, dwActivityID, dwObjectID, dwObjectSum)
    except:
        pass


def nepActionRoleDeadAlive(aliveData):
    if not gNEProtectEnable:
        return
    enableNepSync = gameglobal.rds.configData.get('enableNepSync', False)
    if not enableNepSync:
        return
    try:
        NEProtect.nepActionRoleDeadAlive(aliveData)
    except:
        pass


eMove_Default = 0
eMove_AutoToNPC = 1
eMove_AutoToPlace = 2
eMove_InputToXY = 3
eMove_ClickToXY = 4

def nepActionRoleMoveTo(moveType, dwMoveToX, dwMoveToY):
    if not gNEProtectEnable:
        return
    enableNepSync = gameglobal.rds.configData.get('enableNepSync', False)
    if not enableNepSync:
        return
    try:
        NEProtect.nepActionRoleMoveTo(moveType, dwMoveToX, dwMoveToY)
    except:
        pass
