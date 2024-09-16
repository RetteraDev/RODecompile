#Embedded file name: /WORKSPACE/data/entities/common/guildutils.o
import gametypes

def wingWorldGuildSignUpState2Desc(state):
    if state == gametypes.WW_CAMP_GUILD_STATE_DEFAULT:
        return 'δ����'
    elif state == gametypes.WW_CAMP_GUILD_STATE_SIGNED:
        return '�ѱ���'
    elif state == gametypes.WW_CAMP_GUILD_STATE_COMMIT:
        return '��ʽ�ύ'
    elif state == gametypes.WW_CAMP_GUILD_STATE_FINISH:
        return '��������'
    else:
        return ''


def getGuildMemberDesc(member, showList):
    ret = ''
    for gbId in showList:
        mVal = member.get(gbId)
        if mVal:
            ret += '	' + mVal.role + '	' + str(gbId) + '\n'

    return ret


def getWingWorldSoulBossConsignType(consignType, cfgId):
    if consignType == gametypes.GUILD_CONSIGN_ITEM_ON_SALE_SOURCE_SOUL_BOSS_FIRST_ATTACK:
        return gametypes.GUILD_CONSIGN_ITEM_ON_WING_SOUL_BOSS_START + cfgId - 1
    if consignType == gametypes.GUILD_CONSIGN_ITEM_ON_SALE_SOURCE_SOUL_BOSS_KILL:
        return gametypes.GUILD_CONSIGN_ITEM_ON_WING_SOUL_BOSS_KILL_START + cfgId - 1
    if consignType == gametypes.GUILD_CONSIGN_ITEM_ON_SALE_SOURCE_SOUL_BOSS_DAMAGE:
        return gametypes.GUILD_CONSIGN_ITEM_ON_WING_SOUL_BOSS_DAMAGE_START + cfgId - 1
    return 0


def getGuildTopRewardData(tData, rank):
    for td in tData:
        minRank, maxRank = td['rankRange']
        if not minRank <= rank <= maxRank:
            continue
        return td
