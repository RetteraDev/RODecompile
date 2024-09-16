#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/inviteFriendProxy.o
import BigWorld
from uiProxy import UIProxy
from Scaleform import GfxValue
import gameglobal
import utils
import commInvitation
import const
import gametypes
from guis import ui
from guis import uiConst
from guis import uiUtils
from ui import gbk2unicode
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD
from cdata import invite_data as IVD
from data import invitation_reward_data as IRD
from data import bonus_data as BD

class InviteFriendProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(InviteFriendProxy, self).__init__(uiAdapter)
        self.modelMap = {'initData': self.onInitData,
         'getPopData': self.onGetPopData,
         'closePopWidget': self.onClosePopWidget,
         'submitAccount': self.onSubmitAccount,
         'getRewardList': self.onGetRewardList,
         'getAccountList': self.onGetAccountList,
         'getReward': self.onGetReward}
        self.mediator = None
        self.popupMediator = None
        self.activedAccount = ''
        self.endTime = 0
        self.inviteeRewards = {}
        self.matchInviteCondition = False
        self.invitee = ''
        uiAdapter.registerEscFunc(uiConst.WIDGET_INVITE_FRIEND, self.hide)
        uiAdapter.registerEscFunc(uiConst.WIDGET_INVITE_FRIEND_POPUP, self.hidePopup)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_INVITE_FRIEND:
            self.mediator = mediator
        if widgetId == uiConst.WIDGET_INVITE_FRIEND_POPUP:
            self.popupMediator = mediator

    def show(self):
        if gameglobal.rds.configData.get('enableInviteMate', False):
            self.requestInviteesInfo()
            self.requestRewardList()
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_INVITE_FRIEND, False, True)
        else:
            BigWorld.player().showGameMsg(GMDD.data.INVITE_FRINED_FUNCTION_UNOPEN, ())

    def reset(self):
        self.activedAccount = ''
        self.endTime = 0
        self.inviteeRewards = {}
        self.matchInviteCondition = False
        self.invitee = ''

    def showPop(self, account):
        self.activedAccount = account
        self.endTime = utils.getNow()
        self.updateInviteTip(True)
        self.requestInviteesInfo()
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_INVITE_FRIEND_POPUP)

    def updateInviteTip(self, forceShow):
        p = BigWorld.player()
        if self.mediator and hasattr(p, 'activedAccount') and p.activedAccount != '':
            endTime = utils.formatDatetime(p.endTime + SCD.data.get('invitationExpiredTime', const.TIME_INTERVAL_WEEK))
            stateTip = GMD.data.get(GMDD.data.INVITE_FRINED_ACTIVE_ACCOUNT_SUCCESS_TIP, {}).get('text', '您已成功邀请小伙伴\n%s。') % p.activedAccount
            desc = GMD.data.get(GMDD.data.INVITE_FRINED_ACTIVE_ACCOUNT_SUCCESS_WARNING, {}).get('text', '注意：如果该小伙伴在%s内为上限，将取消资格') % endTime
            self.mediator.Invoke('updateInvietTip', (GfxValue(gbk2unicode(stateTip)), GfxValue(gbk2unicode(desc))))
            if forceShow:
                self.mediator.Invoke('toggleInviteTip', (GfxValue(True), GfxValue(gbk2unicode(stateTip))))

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_INVITE_FRIEND)

    def onClosePopWidget(self, *arg):
        self.hidePopup()

    def hidePopup(self):
        self.popupMediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_INVITE_FRIEND_POPUP)

    def onSubmitAccount(self, *arg):
        p = BigWorld.player()
        account = arg[3][0].GetString()
        account1 = arg[3][1].GetString()
        inviteId = arg[3][2].GetNumber()
        if account == '':
            p.showGameMsg(GMDD.data.NONE_ACCOUNT_INPUT, ())
            if self.mediator:
                self.mediator.Invoke('focuseAccountInput', GfxValue(1))
            return
        if account1 == '':
            p.showGameMsg(GMDD.data.NONE_ACCOUNT_CONFIRM_INPUT, ())
            if self.mediator:
                self.mediator.Invoke('focuseAccountInput', GfxValue(2))
            return
        if account != account1:
            p.showGameMsg(GMDD.data.INPUT_ACCOUNT_INCONSISTENT, ())
            return
        if not utils.isValidEmail(account):
            p.showGameMsg(GMDD.data.INVITE_FRIEND_INVALID_ACCOUNT, ())
            return
        p.cell.inviteMate(inviteId, account)

    def onGetPopData(self, *arg):
        ret = {}
        ret['account'] = self.activedAccount
        endTime = utils.formatDatetime(self.endTime + SCD.data.get('invitationExpiredTime', const.TIME_INTERVAL_WEEK))
        ret['desc'] = GMD.data.get(GMDD.data.INVITE_FRINED_ACTIVE_ACCOUNT_SUCCESS_WARNING, {}).get('text', '若该账号在%s前没有登录过游戏则自动解除资格。') % endTime
        return uiUtils.dict2GfxDict(ret, True)

    def onInitData(self, *arg):
        ret = {}
        limitLv = gameglobal.rds.configData.get('inviterLevel')
        ret['desc'] = GMD.data.get(GMDD.data.INVITE_FRINED_INTRODUCE, {}).get('text', '1.角色等级达到%d级可以激活一个未被激活好友。\n2.帮助小伙伴成长，赢取丰厚奖励') % limitLv
        ret['InviteIdInfo'] = self.getInviteIdInfo()
        self.matchInviteCondition = ret['InviteIdInfo']['inviteState']
        ret['enable'] = self.matchInviteCondition
        ret['stateTip'] = ''
        p = BigWorld.player()
        if not self.matchInviteCondition:
            if hasattr(p, 'activedAccount') and p.activedAccount != '':
                endTime = utils.formatDatetime(p.endTime + SCD.data.get('invitationExpiredTime', const.TIME_INTERVAL_WEEK))
                ret['stateTip'] = GMD.data.get(GMDD.data.INVITE_FRINED_ACTIVE_ACCOUNT_SUCCESS_TIP, {}).get('text', '您已成功邀请小伙伴\n%s。') % p.activedAccount
                ret['desc'] = GMD.data.get(GMDD.data.INVITE_FRINED_ACTIVE_ACCOUNT_SUCCESS_WARNING, {}).get('text', '注意：如果该小伙伴在%s内为上限，将取消资格') % endTime
            else:
                ret['stateTip'] = IVD.data.get(ret['InviteIdInfo']['inviteId'], {}).get('unMatchCondition', '您当前不符合邀请资格')
        return uiUtils.dict2GfxDict(ret, True)

    def getInviteIdInfo(self):
        ret = {}
        ret['inviteId'] = 0
        ret['inviteState'] = False
        p = BigWorld.player()
        inviteData = IVD.data
        for inviteId in inviteData:
            if inviteId in p.inviteExpiredTypes:
                ret['inviteId'] = inviteId
                ret['inviteState'] = False
            else:
                ret['inviteId'] = inviteId
                ret['inviteState'] = self.checkCondition(inviteId)
            return ret

        return ret

    def checkCondition(self, inviteId):
        result = False
        p = BigWorld.player()
        result = commInvitation.inviteMateCheck(p, inviteId)
        return result

    def onGetAccountList(self, *arg):
        ret = []
        p = BigWorld.player()
        if hasattr(p, 'inviteeInfos'):
            for invitee in p.inviteeInfos:
                dataObj = {}
                dataObj['label'] = invitee
                ret.append(dataObj)

        return uiUtils.array2GfxAarry(ret, True)

    def updateInviteeInfos(self, data):
        self.updateInviteTip(False)
        if self.mediator:
            self.mediator.Invoke('updateAccountList')

    def onGetRewardList(self, *arg):
        self.initList()
        if self.inviteeRewards == {}:
            self.requestRewardList()
        invitee = arg[3][0].GetString()
        list = []
        if self.inviteeRewards.has_key(invitee):
            list = self.inviteeRewards[invitee]['rewardList']
        elif self.inviteeRewards.has_key('default'):
            self.inviteeRewards[invitee] = {}
            self.inviteeRewards[invitee]['rewardList'] = self.inviteeRewards['default']['rewardList']
            list = self.inviteeRewards['default']['rewardList']
        return uiUtils.array2GfxAarry(list, True)

    @ui.callFilter(5, False)
    def requestInviteesInfo(self):
        p = BigWorld.player()
        p.cell.fetchAllInviteInfos()

    @ui.callFilter(5, False)
    def requestRewardList(self):
        BigWorld.player().cell.fetchInvitationRewardInfos()

    def getItemList(self, list):
        itemList = []
        for item in list:
            if item[0] == 1:
                data = uiUtils.getGfxItemById(item[1], item[2])
                itemList.append(data)

        return itemList

    def initList(self):
        list = []
        if not self.inviteeRewards.has_key('default'):
            self.inviteeRewards['default'] = {}
        for rewardId in IRD.data:
            rewardData = IRD.data.get(rewardId, {})
            rewardObj = {}
            rewardObj['rewardId'] = rewardId
            rewardObj['title'] = rewardData.get('title', '标题')
            rewardObj['desc'] = rewardData.get('desc', '描述')
            bonusId = rewardData.get('bonusId', 0)
            fixedBonus = BD.data.get(bonusId, {}).get('fixedBonus', [])
            fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
            rewardObj['items'] = self.getItemList(fixedBonus)
            rewardObj['state'] = uiConst.INVITE_FRIEND_CANNOT_GET_REWARD
            list.append(rewardObj)

        self.inviteeRewards['default']['rewardList'] = list

    def updateRewardInfos(self, data):
        self.inviteeRewards = {}
        for invitee in data:
            self.inviteeRewards[invitee] = {}
            self.inviteeRewards[invitee]['rewardList'] = []
            list = []
            for rewardId in IRD.data:
                rewardData = IRD.data.get(rewardId, {})
                rewardObj = {}
                rewardObj['rewardId'] = rewardId
                rewardObj['title'] = rewardData.get('title', '标题')
                rewardObj['desc'] = rewardData.get('desc', '描述 ！')
                bonusId = rewardData.get('bonusId', 0)
                fixedBonus = BD.data.get(bonusId, {}).get('fixedBonus', [])
                fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
                rewardObj['items'] = self.getItemList(fixedBonus)
                if data.has_key(invitee) and data[invitee].has_key(rewardId):
                    if data[invitee][rewardId]:
                        rewardObj['state'] = uiConst.INVITE_FRIEND_GOT_REWARD
                    else:
                        rewardObj['state'] = uiConst.INVITE_FRIEND_CAN_GET_REWARD
                else:
                    rewardObj['state'] = uiConst.INVITE_FRIEND_CANNOT_GET_REWARD
                list.append(rewardObj)

            self.inviteeRewards[invitee]['rewardList'] = list

        if self.mediator:
            self.mediator.Invoke('updateRewardInfo')

    def onGetReward(self, *arg):
        account = arg[3][0].GetString()
        rewardId = int(arg[3][1].GetNumber())
        BigWorld.player().cell.doInvitationReward(account, rewardId)
