#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/neteaseAppVipHelper.o
import copy
import BigWorld
import utils
import gameglobal
import gametypes
import const
from guis import messageBoxProxy
from guis.tianyuMallProxy import SubTab
from data import netease_membership_config_data as NMCD
from data import netease_membership_bonus_data as NMBD
from data import bonus_data as BD
from gamestrings import gameStrings
BONUS_NOTVALIABLE = 0
BONUS_AVALIABLE = 1
BONUS_GETED = 2
COMMON_VIP_TITLE_ID = 13
SUPER_VIP_TITLE_ID = 12
BonusGiftMap = {gametypes.RIGHT_TYPE_RECV_BINDING_GIFT: 'binding_gift',
 gametypes.RIGHT_TYPE_RECV_SEQUENT_GIFT: 'sequent_gift',
 gametypes.RIGHT_TYPE_RECV_ACTIVATION_GIFT: 'activation_gift',
 gametypes.RIGHT_TYPE_RECV_RECHARGE_GIFT: 'recharge_game',
 gametypes.RIGHT_TYPE_RECV_SINGLE_GIFT: 'single_gift'}
CheckBonusList = [gametypes.RIGHT_TYPE_RECV_BINDING_GIFT,
 gametypes.RIGHT_TYPE_RECV_SEQUENT_GIFT,
 gametypes.RIGHT_TYPE_RECV_ACTIVATION_GIFT,
 gametypes.RIGHT_TYPE_RECV_SINGLE_GIFT]
TITLE_RECIEVED = -1
TITLE_UNAVALIABLE = 0
TITLE_AVALIABLE = 1

class NetEaseAppVipHelper(object):

    def __init__(self):
        super(NetEaseAppVipHelper, self).__init__()
        self.subTab = None

    def initVipMallItemInfo(self):
        mallItems = {'value': NMCD.data.get('mallItemsNew', ())}
        self.subTab = SubTab(0, mallItems)

    def getVipMallItemInfo(self):
        p = BigWorld.player()
        now = utils.getNow()
        if not self.subTab:
            self.initVipMallItemInfo()
        itemsInfo = self.subTab.children
        for item in itemsInfo:
            packageId = item.get('packageID', 0)
            item['expire'] = p.vipAddedPackage.get(packageId, {}).get('tExpire', 0) - now
            item['vipDayList'] = gameglobal.rds.ui.tianyuMall.genVipDayList(packageId)

        itemsInfo = gameglobal.rds.ui.tianyuMall.appendLimitInfo(itemsInfo)
        return itemsInfo

    def getVipBonusItemInfo(self):
        bonusItems = []
        bonusData = NMBD.data
        for key in bonusData:
            data = bonusData.get(key, {})
            bonusInfo = copy.deepcopy(data)
            bonusInfo['itemList'] = self.genBonusInfo(data.get('bonusId', 0))
            bonusInfo['bonusType'] = key
            bonusItems.append(bonusInfo)

        return bonusItems

    def getTitleRecieveState(self):
        keys = []
        if self.isCommonVip():
            keys.append(NMCD.data.get('mallVIPPrivilegeGameTitle', COMMON_VIP_TITLE_ID))
        if self.isSuperVip():
            keys = []
            keys.append(NMCD.data.get('mallVIPPrivilegeGameTitle', COMMON_VIP_TITLE_ID))
            keys.append(NMCD.data.get('mallVIPPrivilegeSuperTitle', SUPER_VIP_TITLE_ID))
        recieveState = TITLE_UNAVALIABLE
        for key in keys:
            p = BigWorld.player()
            privilegesData = getattr(p, 'mallPrivilegeData', {})
            privilegeData = privilegesData.get(key, {})
            if privilegeData.get('state', 0) == TITLE_AVALIABLE:
                return TITLE_AVALIABLE
            if privilegeData.get('state', 0) == TITLE_RECIEVED:
                recieveState = TITLE_RECIEVED

        return recieveState

    def getUnRecieveTitles(self):
        p = BigWorld.player()
        keys = []
        if self.isCommonVip():
            keys.append(NMCD.data.get('mallVIPPrivilegeGameTitle', COMMON_VIP_TITLE_ID))
        if self.isSuperVip():
            keys = []
            keys.append(NMCD.data.get('mallVIPPrivilegeGameTitle', COMMON_VIP_TITLE_ID))
            keys.append(NMCD.data.get('mallVIPPrivilegeSuperTitle', SUPER_VIP_TITLE_ID))
        recvKeys = []
        for key in keys:
            p = BigWorld.player()
            privilegesData = getattr(p, 'mallPrivilegeData', {})
            privilegeData = privilegesData.get(key, {})
            if privilegeData.get('state', 0) == TITLE_AVALIABLE:
                recvKeys.append(key)

        if keys:
            p.base.receiveMallVIPPrivilegeTitle(keys)

    def getSequenceBindTime(self):
        p = BigWorld.player()
        if hasattr(p, 'neteaseMembershipInfo'):
            return getattr(p.neteaseMembershipInfo, 'sequent_gift_info', {}).get('keep_bind_game_count', 0)
        return False

    def getVipBonusState(self, rightType):
        if not BonusGiftMap.has_key(rightType):
            return BONUS_NOTVALIABLE
        elif rightType != gametypes.RIGHT_TYPE_RECV_RECHARGE_GIFT and rightType != gametypes.RIGHT_TYPE_RECV_ACTIVATION_GIFT and not self.isBind():
            return BONUS_NOTVALIABLE
        giftName = BonusGiftMap[rightType]
        p = BigWorld.player()
        if not hasattr(p, 'neteaseMembershipInfo'):
            return BONUS_NOTVALIABLE
        giftInfo = getattr(p.neteaseMembershipInfo, giftName + '_info', None)
        if not giftInfo:
            return BONUS_NOTVALIABLE
        canGet = giftInfo.get('is_' + giftName, False)
        if canGet:
            return BONUS_AVALIABLE
        elif giftInfo.get('is_get_' + giftName, False):
            return BONUS_GETED
        else:
            return BONUS_NOTVALIABLE

    def needShowNewIcon(self):
        if not self.isAppVip():
            return False
        if self.getTitleRecieveState() == 1:
            return True
        for bonusType in CheckBonusList:
            if self.getVipBonusState(bonusType) == BONUS_AVALIABLE:
                return True

        return False

    def isBind(self):
        p = BigWorld.player()
        if hasattr(p, 'neteaseMembershipInfo'):
            if p.neteaseMembershipInfo.is_bind_this_game:
                return True
        return False

    def hasRebet(self):
        bonusState = self.getVipBonusState(gametypes.RIGHT_TYPE_RECV_RECHARGE_GIFT)
        p = BigWorld.player()
        if bonusState == BONUS_AVALIABLE and hasattr(p, 'birthInDB'):
            return utils.getNow() - p.birthInDB < NMCD.data.get('rechargeGiftBirthInDBLimit', const.TIME_INTERVAL_MONTH)
        return False

    def isAppVip(self):
        p = BigWorld.player()
        if hasattr(p, 'neteaseMembershipInfo'):
            return not p.neteaseMembershipInfo.isMembershipExpire()
        return False

    def getVipLevel(self):
        p = BigWorld.player()
        if hasattr(p, 'neteaseMembershipInfo'):
            vipInfo = p.neteaseMembershipInfo
            level = vipInfo.level
            return level
        return -1

    def isSuperVip(self):
        p = BigWorld.player()
        if hasattr(p, 'neteaseMembershipInfo'):
            return p.neteaseMembershipInfo.isSuperMembership()
        return False

    def isCommonVip(self):
        p = BigWorld.player()
        if hasattr(p, 'neteaseMembershipInfo'):
            return p.neteaseMembershipInfo.isGameMembership()
        return False

    def showPrivilegeBindWnd(self):
        p = BigWorld.player()
        if hasattr(p, 'neteaseMembershipInfo'):
            if p.neteaseMembershipInfo.isHasMallDiscount():
                return True
            MBButton = messageBoxProxy.MBButton
            buttons = [MBButton(gameStrings.MALL_BIND_CONFIRM, self.bindAppPrivilege), MBButton(gameStrings.CBG_HOME_GUANBI, None)]
            gameglobal.rds.ui.messageBox.show(True, gameStrings.MALL_BIND_TITLE, gameStrings.MALL_BIND_MSG, buttons)
        return False

    def bindAppPrivilege(self):
        p = BigWorld.player()
        p.base.applyMembershipInGame()

    def getVipBonusInfo(self):
        pass

    def genBonusInfo(self, bonusId):
        bonusData = BD.data.get(bonusId, {})
        fixedBonus = bonusData.get('fixedBonus', [])
        bonusItems = []
        for bType, itemId, itemNum in fixedBonus:
            if bType != gametypes.BONUS_TYPE_ITEM:
                continue
            bonusItems.append((bType, itemId, itemNum))

        return bonusItems


instance_ = None

def getInstance():
    global instance_
    if not instance_:
        instance_ = NetEaseAppVipHelper()
    return instance_
