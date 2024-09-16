#Embedded file name: /WORKSPACE/data/entities/client/bufferpropertygetter.o
import BigWorld
import utils
import gamelog
import gameconfigCommon
from data import formula_client_data as FCD
from cdata import server_exp_add_data as SEAD
from cdata import server_exp_add_new_data as SEAND
BUFFER_PROPERTY_GETTER_LV_EXP = 2
BUFFER_PROPERTY_GETTER_DESC_WITH_TEMP_CAMP_IN_BATTLE_FIELD = 5
bufferPropertyGetterMap = {}

def bufferPropertyGetter(source):

    def func(method):
        bufferPropertyGetterMap[source] = method.__name__
        return method

    return func


@bufferPropertyGetter(BUFFER_PROPERTY_GETTER_LV_EXP)
def _getExpAddProperty(owner, args):
    gamelog.debug('@zq query#_getExpAddProperty:', owner.id, args)
    playerMaxLv, = args
    p = BigWorld.player()
    serverExpAddParam = 0
    if gameconfigCommon.enableServerExpAddNew():
        serverExpAddParam = p.expAddParamBuffVal - 100
    else:
        serverExpAddParam = p.expAddParamBuffVal
    return serverExpAddParam


@bufferPropertyGetter(BUFFER_PROPERTY_GETTER_DESC_WITH_TEMP_CAMP_IN_BATTLE_FIELD)
def _getBattleFieldHuntFreezeBuffDesc(owner, args):
    from data import battle_field_mode_data as BFMD
    import formula
    clientPropName, = args
    ownerTempCamp = getattr(owner, clientPropName, 1)
    fbNo = formula.getFubenNo(owner.spaceNo)
    fbMode = formula.fbNo2BattleFieldMode(fbNo)
    desc = BFMD.data.get(fbMode, {}).get('freezeBufferTips', {}).get(ownerTempCamp, '倒计时结束时还未参与战斗，则强制离开战场')
    return desc
