#Embedded file name: /WORKSPACE/data/entities/client/logicinfo.o
import BigWorld
import gamelog
import utils
from data import item_data as ID
from data import skill_general_data as SGD
cooldownItem = {}
commonCooldownItem = {}
cooldownWeaponSkill = {}
commonCooldownWeaponSkill = (0, 0, None)
commonCooldownDodge = (0, 0, None)

def isUseableItem(id):
    remain = getItemCooldownRemainTime(id)
    if remain > 0:
        return False
    return True


def getItemCooldownRemainTime(id):
    global cooldownItem
    global commonCooldownItem
    remain = 0
    data = ID.data[id]
    tp = data['type']
    stype = data['stype']
    key = (tp, stype)
    cremain = 0
    if key in commonCooldownItem:
        cremain = commonCooldownItem[key][0] - BigWorld.time()
    if id in cooldownItem:
        remain = cooldownItem[id][0] - BigWorld.time()
    remain = max(cremain, remain)
    if remain < 0:
        remain = 0
    return remain


def getItemCooldDownTime(itemId):
    total = 0
    end = 0
    remain = 0
    data = ID.data.get(itemId, {})
    typeNum = data.get('cdgroup', itemId)
    if itemId in cooldownItem:
        end, total = cooldownItem[itemId]
        remain = end - BigWorld.time()
    if typeNum in commonCooldownItem:
        cend, ctotal = commonCooldownItem[typeNum]
        cremain = cend - BigWorld.time()
        if cremain > remain:
            remain = cremain
            total = ctotal
    return (remain, total)


cooldownOrder = {}

def isUseableOrder(id):
    global cooldownOrder
    if id in cooldownOrder:
        cool = cooldownOrder[id]
        if cool[0] > BigWorld.time():
            return False
    return True


cooldownRideSkill = {}

def isUseableRideSkill(id):
    global cooldownRideSkill
    if id in cooldownRideSkill:
        cool = cooldownRideSkill[id]
        if cool[0] > BigWorld.time():
            return False
    return True


cooldownGuildMemberSkill = {}

def isUseableGuildMemberSkill(id):
    global cooldownGuildMemberSkill
    if id in cooldownGuildMemberSkill:
        cool = cooldownGuildMemberSkill[id]
        if cool[0] > BigWorld.time():
            return False
    return True


cooldownWWArmySkill = {}

def isUseableWWArmySkill(id):
    global cooldownWWArmySkill
    if id in cooldownWWArmySkill:
        cool = cooldownWWArmySkill[id]
        if cool[0] > BigWorld.time():
            return False
    return True


cooldownClanWarSkill = {}

def isUseableClanWarSkill(id):
    global cooldownClanWarSkill
    if id in cooldownClanWarSkill:
        cool = cooldownClanWarSkill[id]
        if cool[0] > BigWorld.time():
            return False
    return True


cooldownSkill = {}

def isUseableSkill(id):
    global cooldownSkill
    global commonCooldownWeaponSkill
    time = BigWorld.time()
    p = BigWorld.player()
    gamelog.debug('isUseableSkill:', id, cooldownSkill, commonCooldownWeaponSkill[0] > time)
    if not p.gmMode and id in cooldownSkill:
        if id in cdStorageSkill:
            return cdStorageSkill[id][1] > 0
        if cooldownSkill[id][0] > time:
            return False
    if commonCooldownWeaponSkill[0] > time:
        return False
    return True


cdStorageSkill = {}

def initCdStoreageSkill(skillId):
    if not cdStorageSkill.has_key(skillId) and utils.isCDStorageSkill(skillId, 1):
        times = SGD.data.get((skillId, 1), {}).get('cdstorage', 3)
        cdStorageSkill[skillId] = (0, times)


def isSkillCooldowning(id):
    time = BigWorld.time()
    p = BigWorld.player()
    if not p.gmMode and id in cooldownSkill:
        if id in cdStorageSkill:
            if cdStorageSkill[id][1] > 0:
                return False
        elif cooldownSkill[id][0] > time:
            return True
    return False


def isInSkillCommonTime():
    time = BigWorld.time()
    commontime = commonCooldownWeaponSkill[0]
    if time < commontime:
        return True
    return False


def isUseableWeaponSkill(id):
    global cooldownWeaponSkill
    time = BigWorld.time()
    if id in cooldownWeaponSkill:
        if cooldownWeaponSkill[id][0] > time:
            return False
    if commonCooldownWeaponSkill[0] > time:
        return False
    return True


def isInDodgeCoolDownTime():
    time = BigWorld.time()
    commontime = commonCooldownDodge[0]
    if time < commontime:
        return True
    return False


def clearCoolDown():
    global commonCooldownClanSkill
    global cooldownWWArmySkill
    global cooldownSkill
    global cooldownRideSkill
    global commonCooldownItem
    global cooldownGuildMemberSkill
    global commonCooldownShapeSkill
    global cooldownClanSkill
    global cooldownWeaponSkill
    global cooldownOrder
    global cooldownItem
    global commonCooldownBeastSkill
    global cooldownShapeSkill
    global cooldownHbSkill
    global cooldownBeastSkill
    global commonCooldownWeaponSkill
    cooldownWeaponSkill = {}
    commonCooldownWeaponSkill = (0, 0, None)
    cooldownShapeSkill = {}
    commonCooldownShapeSkill = (0, 0, None)
    cooldownBeastSkill = {}
    commonCooldownBeastSkill = (0, 0, None)
    cooldownSkill = {}
    cooldownItem = {}
    commonCooldownItem = {}
    cooldownOrder = {}
    cooldownRideSkill = {}
    cooldownHbSkill = {}
    cooldownClanSkill = {}
    commonCooldownClanSkill = (0, 0, None)
    cooldownGuildMemberSkill = {}
    cooldownWWArmySkill = {}
    cooldownClanSkill = {}


spriteManualSkillCoolDown = None
spriteTeleportSkillCoolDown = None
