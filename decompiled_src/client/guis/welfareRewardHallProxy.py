#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/welfareRewardHallProxy.o
import BigWorld
import ui
import uiConst
import uiUtils
import gameglobal
from uiProxy import UIProxy
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD

class WelfareRewardHallProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WelfareRewardHallProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerMc': self.onRegisterMc,
         'unRegisterMc': self.onUnRegisterMc,
         'showReward': self.onShowReward}
        self.panelMc = None

    def onRegisterMc(self, *arg):
        self.panelMc = arg[3][0]
        self.refreshInfo()

    def onUnRegisterMc(self, *arg):
        self.panelMc = None

    def refreshInfo(self):
        if self.panelMc:
            p = BigWorld.player()
            pushMsgInfo = p.getPushMsgInfo()
            descList = SCD.data.get('REWARDHALL_SLOT_DESC_NEW', ())
            rewardList = []
            for id, desc, frameName in descList:
                rewardInfo = {'id': id,
                 'desc': desc,
                 'frameName': frameName,
                 'hasReward': id in pushMsgInfo}
                rewardList.append(rewardInfo)

            self.panelMc.Invoke('refreshInfo', uiUtils.array2GfxAarry(rewardList, True))

    @ui.callFilter(1, True)
    def onShowReward(self, *arg):
        id = int(arg[3][0].GetNumber())
        self.gotoShowWidget(id)

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

    def updateRewardHall(self):
        self.refreshInfo()
        gameglobal.rds.ui.welfare.refreshInfo()
