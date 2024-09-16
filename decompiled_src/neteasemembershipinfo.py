#Embedded file name: /WORKSPACE/data/entities/common/neteasemembershipinfo.o
import utils
import gamelog
import json
import gametypes
from data import netease_membership_config_data as NMCD

class NeteaseMembershipEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


class NeteaseMembership(object):

    def __init__(self):
        self.mallDiscountMonthSec = 0
        self.super_expire_date = 0
        self.game_expire_date = 0
        self.level = 0

    def loadFromDict(self, origin):
        for key, value in origin.iteritems():
            setattr(self, key, value)

        self.super_expire_date = utils._covertToTimestampFromExpireDate(self.super_expire_date)
        self.game_expire_date = utils._covertToTimestampFromExpireDate(self.game_expire_date)

    def dumpToJson(self):
        return json.dumps(self.__dict__, cls=NeteaseMembershipEncoder, separators=(',', ':'))

    def isMembershipExpire(self):
        expireDate = max(self.super_expire_date, self.game_expire_date)
        if not expireDate:
            return True
        return utils.getNow() > expireDate

    def isSuperMembership(self):
        if not self.super_expire_date:
            return False
        return self.super_expire_date > utils.getNow()

    def isGameMembership(self):
        if not self.game_expire_date:
            return False
        return self.game_expire_date > utils.getNow()

    def isHasMembershipRight(self):
        return not self.isMembershipExpire()

    def getSuperExpireDate(self):
        return self.super_expire_date

    def getGameExpireDate(self):
        return self.game_expire_date

    def setGameExpireDate(self, newDate):
        self.game_expire_date = newDate

    def getMembershpExpireDate(self):
        return max(self.super_expire_date, self.game_expire_date)

    def isHasMallDiscount(self, now = 0):
        if now == 0:
            now = utils.getNow()
        return utils.getMonthSecond(now) == self.mallDiscountMonthSec and self.is_bind_this_game

    def canGetRight(self, rightType):
        if rightType == gametypes.RIGHT_TYPE_BINDING_GAME:
            return self.left_bind_game_count > 0
        if rightType == gametypes.RIGHT_TYPE_RECV_BINDING_GIFT:
            return self.binding_gift_info['is_binding_gift']
        if rightType == gametypes.RIGHT_TYPE_RECV_SEQUENT_GIFT:
            return self.sequent_gift_info['is_sequent_gift']
        if rightType == gametypes.RIGHT_TYPE_RECV_SINGLE_GIFT:
            return self.single_gift_info['is_single_gift']
        if rightType == gametypes.RIGHT_TYPE_RECV_ACTIVATION_GIFT:
            return self.activation_gift_info['is_activation_gift']
        if rightType == gametypes.RIGHT_TYPE_RECV_RECHARGE_GIFT:
            return self.recharge_game_info['is_recharge_game']
        return False

    def __repr__(self):
        return repr(self.__dict__)

    __str__ = __repr__
