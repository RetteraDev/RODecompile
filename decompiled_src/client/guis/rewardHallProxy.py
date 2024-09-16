#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/rewardHallProxy.o
import BigWorld
import ui
import uiConst
import uiUtils
import gameglobal
from uiProxy import UIProxy
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD

class RewardHallProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RewardHallProxy, self).__init__(uiAdapter)
        self.modelMap = {'getReward': self.onGetReward,
         'showReward': self.onShowReward,
         'setGetRewardBtn': self.onSetGetRewardBtn}
        self.mediator = None
        self.initData = ((),)
        self.isShowRewardNotify = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_REWARD_HALL, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_REWARD_HALL:
            self.mediator = mediator
            self.initData = SCD.data.get('REWARDHALL_SLOT_DESC', ())
            return uiUtils.array2GfxAarry(self.initData, True)

    def show(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_REWARD_HALL)

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_REWARD_HALL)

    def reset(self):
        self.mediator = None
        self.isShowRewardNotify = False

    @ui.callFilter(1, True)
    def onGetReward(self, *arg):
        str = arg[3][0].GetString()
        id = int(self.getNumberFromStr(str))
        self.gotoShowWidget(id)

    @ui.callFilter(1, True)
    def onShowReward(self, *arg):
        str = arg[3][0].GetString()
        id = int(self.getNumberFromStr(str))
        self.gotoShowWidget(id)

    def getNumberFromStr(self, oldS):
        newS = ''
        for s in oldS:
            if not s.isalpha():
                newS += s

        return newS

    def onSetGetRewardBtn(self, *arg):
        p = BigWorld.player()
        pushMsgInfo = p.getPushMsgInfo()
        arr = self.excludeData(pushMsgInfo)
        if not arr:
            self.isShowRewardNotify = False
        else:
            self.isShowRewardNotify = True
        return uiUtils.array2GfxAarry(arr)

    def gotoShowWidget(self, id):
        p = BigWorld.player()
        openQumoLv = SCD.data.get('OpenQumoLv', 30)
        openJunjieLv = SCD.data.get('OpenJunjieLv', 30)
        if id == uiConst.REWARD_QUMO:
            if p.lv >= openQumoLv:
                gameglobal.rds.ui.roleInfo.show(uiConst.ROLEINFO_TAB_QUMO)
            else:
                p.showGameMsg(GMDD.data.ROLEINFO_TAB_QUMO_NOTIFY, ())
        elif id == uiConst.REWARD_ANQUAN:
            if gameglobal.rds.configData.get('enableBindReward', False):
                gameglobal.rds.ui.accountBind.show()
            else:
                gameglobal.rds.ui.userAccountBind.show()
        elif id == uiConst.REWARD_DUIHUAN:
            gameglobal.rds.ui.applyReward.show()
        elif id == uiConst.REWARD_JUNJIE:
            if p.lv >= openJunjieLv:
                gameglobal.rds.ui.roleInfo.show(uiConst.ROLEINFO_TAB_JUNJIE)
            else:
                p.showGameMsg(GMDD.data.REWARD_JUNJIE_NOTIFY, ())
        elif id == uiConst.REWARD_SHENJI:
            pass
        elif id == uiConst.REWARD_XIULIAN:
            gameglobal.rds.ui.xiuLianAward.show()
        elif id == uiConst.REWARD_ZHIYOU:
            if gameglobal.rds.configData.get('enableInvitePoint', False):
                if gameglobal.rds.configData.get('enableSummonFriendV2', False):
                    gameglobal.rds.ui.summonFriendBGV2.show()
                else:
                    gameglobal.rds.ui.summonFriendNew.show()
            else:
                gameglobal.rds.ui.summonFriend.show(0)

    def excludeData(self, arr):
        ret = []
        for i in self.initData:
            if i[0] in arr:
                ret.append(i[0])

        return ret

    def updateRewardHall(self):
        p = BigWorld.player()
        pushMsgInfo = p.getPushMsgInfo()
        self.isShowRewardNotify = p.checkNeedPushMsg()
        if self.mediator:
            self.mediator.Invoke('setGetRewardBtnState', uiUtils.array2GfxAarry(pushMsgInfo))
