#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impYixin.o
import cPickle
import zlib
import BigWorld
import gamelog
import const
import commcalc
from cdata import game_msg_def_data as GMDD

class ImpYixin(object):

    def onYixinRewardResultCallBack(self, result, rewardId):
        gamelog.debug('jinjj--------onYixinRewardResultCallBack----', result)
        if result == const.YIXIN_NO_ERROR:
            commcalc.setBit(BigWorld.player().yixinRewardList, rewardId, True)
        self.dispatchEvent(const.EVENT_YIXIN_REWARDS_CHANGE, (result,))

    def rspYixinReward(self, rewardList):
        BigWorld.player().yixinRewardList = rewardList
        self.dispatchEvent(const.EVENT_YIXIN_REWARDS_CHANGE, (const.REFRESH_YIXIN_REWARD,))

    def onBindYixinResultCallBack(self, result, openId):
        if result == const.YIXIN_NO_ERROR:
            BigWorld.player().yixinOpenId = openId
            self.dispatchEvent(const.EVENT_YIXIN_BIND_SUCCESS, ())
        else:
            self.dispatchEvent(const.EVENT_YIXIN_BIND_FAILED, (result,))

    def onUnBindYixinResultCallBack(self, result):
        gamelog.debug('jinjj--------onUnBindYixinResultCallBack---')
        if result == const.YIXIN_NO_ERROR:
            BigWorld.player().yixinOpenId = 0
            self.dispatchEvent(const.EVENT_YIXIN_UNBIND_SUCCESS, result)
            BigWorld.player().showGameMsg(GMDD.data.YIXIN_UNBIND_SUCCESS, ())
        else:
            self.dispatchEvent(const.EVENT_YIXIN_UNBIND_FAILED, result)
            BigWorld.player().showGameMsg(GMDD.data.YIXIN_UNBIND_FAILED, ())

    def onAddGuildMemberCallback(self, error):
        if error == const.YIXIN_NO_ERROR:
            BigWorld.player().showGameMsg(GMDD.data.YIXIN_ADDGUILD_SUCCESS, ())
        else:
            BigWorld.player().showGameMsg(GMDD.data.YIXIN_ADDGUILD_FAILED, ())

    def registerEvent(self, eventId, eventFunc):
        if not hasattr(self, 'eventFuncDict'):
            self.eventFuncDict = {}
        if self.eventFuncDict.has_key(eventId):
            finded = False
            for i in self.eventFuncDict[eventId]:
                if i == eventFunc:
                    finded = True

            if finded == False:
                self.eventFuncDict[eventId].append(eventFunc)
        else:
            self.eventFuncDict[eventId] = [eventFunc]

    def unRegisterAllEvent(self):
        self.eventFuncDict = {}

    def unRegisterEvent(self, eventId, eventFunc):
        if not hasattr(self, 'eventFuncDict'):
            self.eventFuncDict = {}
        if self.eventFuncDict.has_key(eventId):
            for i in xrange(len(self.eventFuncDict[eventId])):
                if self.eventFuncDict[eventId][i] == eventFunc:
                    del self.eventFuncDict[eventId][i]
                    break

    def dispatchEvent(self, eventId, *params):
        if not hasattr(self, 'eventFuncDict'):
            self.eventFuncDict = {}
        if self.eventFuncDict.has_key(eventId):
            for func in self.eventFuncDict[eventId]:
                func(*params)

    def onSetYixinSettings(self, settings):
        if settings == BigWorld.player().yixinSetting:
            BigWorld.player().showGameMsg(GMDD.data.YIXIN_SETTING_FAILED, ())
        else:
            BigWorld.player().yixinSetting = settings
            BigWorld.player().showGameMsg(GMDD.data.YIXIN_SETTING_SUCCESS, ())

    def sendYixinSettings(self, settings):
        data = cPickle.loads(zlib.decompress(settings))
        BigWorld.player().yixinOpenId = data['openid']
        BigWorld.player().yixinRewardList = data['rewardList']
        BigWorld.player().isAutoAddYixinFriend = data['setting']['autoAcceptFriend']
        BigWorld.player().yixinSetting = data['setting']

    def onAddYixinFriendCallback(self, error):
        msg = 0
        if error == const.YIXIN_ERR_SRC_NOT_EXIST:
            msg = GMDD.data.YIXIN_ERR_SRC_NOT_EXIST
        elif error == const.YIXIN_ERR_TGT_NOT_EXIST:
            msg = GMDD.data.YIXIN_ERR_TGT_NOT_EXIST
        elif error == const.YIXIN_ERR_MAX_FRIEND_LIMIT:
            msg = GMDD.data.YIXIN_ERR_MAX_FRIEND_LIMIT
        elif error == const.YIXIN_ERR_IN_BLACK_LIST:
            msg = GMDD.data.YIXIN_ERR_IN_BLACK_LIST
        elif error == const.YIXIN_ERR_ALREADY_FRIEND:
            msg = GMDD.data.YIXIN_ERR_ALREADY_FRIEND
        elif error == const.YIXIN_ERR_MAX_ADD_FRIEND_FREQUENT:
            msg = GMDD.data.YIXIN_ERR_MAX_ADD_FRIEND_FREQUENT
        elif error == const.YIXIN_ERR_AUTO_ADD_FRIEND:
            msg = GMDD.data.YIXIN_ERR_AUTO_ADD_FRIEND
        elif error == const.YIXIN_ERR_BAD_YIXIN_SERVER_REPLY:
            msg = GMDD.data.YIXIN_ERR_BAD_YIXIN_SERVER_REPLY
        elif error == const.YIXIN_NO_ERROR:
            msg = GMDD.data.YIXIN_ADD_YIXINFRIEND_SUCCESS
        if msg:
            BigWorld.player().showGameMsg(msg, ())

    def onAddYixinFriend(self, gbId, msg):
        pass
