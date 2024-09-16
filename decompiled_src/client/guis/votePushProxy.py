#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/votePushProxy.o
from gamestrings import gameStrings
import BigWorld
from guis import uiUtils
import gameglobal
import const
from guis import uiConst
from callbackHelper import Functor
from uiProxy import SlotDataProxy
from data import operation_poll_data as OPD
from cdata import game_msg_def_data as GMDD

class VotePushProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(VotePushProxy, self).__init__(uiAdapter)
        self.modelMap = {'getInfo': self.onGetInfo,
         'cancel': self.onCancel,
         'confirm': self.onConfirm,
         'small': self.onSmall}
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_VOTE_PUSH, self.clearWidget)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_VOTE_PUSH:
            self.mediator = mediator

    def show(self, pollId):
        if not self.canVote(pollId):
            return
        self.pollId = pollId
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_VOTE_PUSH)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_VOTE_PUSH)

    def reset(self):
        self.mediator = None
        self.pollIdDict = {}
        self.pollId = 0

    def notifyBonusPushMsg(self, pollId):
        if not self.canVote(pollId):
            return
        pushId = OPD.data.get(pollId, {}).get('pushId', 0)
        gameglobal.rds.ui.pushMessage.addPushMsg(pushId)
        gameglobal.rds.ui.pushMessage.setCallBack(pushId, {'click': Functor(self.show, pollId)})
        if pollId not in self.pollIdDict:
            self.pollIdDict[pollId] = {}
            self.pollIdDict[pollId]['pushId'] = pushId

    def onGetInfo(self, *args):
        ret = {}
        serverNamePair = None
        pollData = OPD.data.get(self.pollId, {})
        serverNameList = pollData.get('mergeServerPairs')
        for pair in serverNameList:
            if gameglobal.gServerName in pair:
                serverNamePair = list(pair)
                break

        desc = pollData.get('desc').strip('\n')
        isNewVote = pollData.get('isNewVote', 0)
        if not serverNamePair:
            ret['desc'] = ['']
        else:
            serverNamePair.remove(gameglobal.gServerName)
            if isNewVote:
                ret['desc'] = [desc]
            else:
                ret['desc'] = [desc % (gameglobal.gServerName, ','.join(serverNamePair))]
        ret['upBtnDesc'] = pollData.get('upBtnDesc')
        ret['downBtnDesc'] = pollData.get('downBtnDesc')
        ret['title'] = pollData.get('title')
        return uiUtils.dict2GfxDict(ret, True)

    def canVote(self, pollId):
        pollData = OPD.data.get(pollId, {})
        serverNameList = pollData.get('mergeServerPairs', ())
        for pair in serverNameList:
            if gameglobal.gServerName in pair:
                return True

        BigWorld.player().showGameMsg(GMDD.data.COMMON_MSG, (gameStrings.TEXT_VOTEPUSHPROXY_89 % gameglobal.gServerName,))
        return False

    def onCancel(self, *args):
        BigWorld.player().base.voteForPoll(self.pollId, const.VOTE_FOR_POLL_DOWN)

    def onConfirm(self, *args):
        BigWorld.player().base.voteForPoll(self.pollId, const.VOTE_FOR_POLL_UP)

    def onSmall(self, *args):
        self.hide(False)

    def hideVote(self, pollId):
        if pollId not in self.pollIdDict:
            return
        gameglobal.rds.ui.pushMessage.removePushMsg(self.pollIdDict[pollId]['pushId'])
        if self.pollId == pollId:
            self.hide(False)

    def hideAllVote(self):
        for pollId in self.pollIdDict:
            gameglobal.rds.ui.pushMessage.removePushMsg(self.pollIdDict[pollId]['pushId'])

        self.hide()

    def voteSucceed(self, pollId):
        if pollId not in self.pollIdDict:
            return
        gameglobal.rds.ui.pushMessage.removePushMsg(self.pollIdDict[pollId]['pushId'])
        self.hide(False)

    def voteFailed(self, pollId):
        self.hide(False)
