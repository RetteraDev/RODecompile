#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/generalPushMappings.o
import gameglobal
from data import general_push_icon_data as GPID
GENERAL_PUSH_BALANCE_PLAYOFFS = 1
GENERAL_PUSH_DOUBLE_ARENA = 2
GENERAL_PUSH_BATTLE_OF_FORT = 3
GENERAL_PUSH_CLAN_CHALLENGE = 4
generalPushMap = {GENERAL_PUSH_BALANCE_PLAYOFFS: 'balanceArenaPlayoffsPush',
 GENERAL_PUSH_DOUBLE_ARENA: 'balanceArena2PersonPush',
 GENERAL_PUSH_BATTLE_OF_FORT: 'battleOfFortPush',
 GENERAL_PUSH_CLAN_CHALLENGE: 'clanChallengePush'}

def getGeneralPushProxy(gPushId):
    if not generalPushMap.has_key(gPushId):
        return
    else:
        pushProxy = getattr(gameglobal.rds.ui, generalPushMap.get(gPushId, ''), None)
        return pushProxy
