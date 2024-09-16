#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pushBonusProxy.o
import BigWorld
import gameglobal
import gametypes
import utils
import clientUtils
from guis import uiConst
from guis import uiUtils
from guis.uiProxy import UIProxy
from data import bonus_data as BD
from data import mail_template_data as MTD

class PushBonusProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PushBonusProxy, self).__init__(uiAdapter)
        self.modelMap = {'getRewards': self.onGetRewards,
         'closePage': self.onClosePage}
        self.secuInfoIdNum = 0
        self.mediator = None
        self.rewardData = []
        self.fromGMT = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_PUSH_BONUS, self.hide)

    def addRewardData(self, data):
        self.rewardData = data

    def show(self, fromGMT = False):
        p = BigWorld.player()
        self.fromGMT = fromGMT
        if not fromGMT and self.rewardData:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PUSH_BONUS)
        elif fromGMT and self.gmtRewardListHadItem():
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PUSH_BONUS)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_PUSH_BONUS:
            self.mediator = mediator
            return uiUtils.dict2GfxDict(self._getInfoData(), True)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_PUSH_BONUS)
        if not self.fromGMT and gameglobal.rds.ui.pushMessage.msgs.has_key(uiConst.MESSAGE_TYPE_COMPLETE_INFO):
            if self.secuInfoIdNum:
                gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_COMPLETE_INFO)

    def _getInfoData(self):
        ret = {}
        p = BigWorld.player()
        if not self.fromGMT and self.rewardData:
            subRewardData = self.rewardData[0]
            if subRewardData:
                bonusId = subRewardData.get('bonusId', 0)
                extraItems = subRewardData.get('extraItems', 0)
                mailTemplateId = subRewardData.get('mailTemplateId', 0)
                mtd = MTD.data.get(mailTemplateId, {})
                ret['title'] = mtd.get('subject', '')
                ret['content'] = mtd.get('content', '')
                ret['rewardItems'] = self._getInfoRewards(bonusId, extraItems)
        elif self.fromGMT and getattr(p, 'compInfo', None):
            for compInfo in reversed(p.compInfo):
                mailSubject, mailContent, rewards = clientUtils.unpackCompInfo(compInfo)
                if any((reward[0] == gametypes.BONUS_TYPE_ITEM for reward in rewards)):
                    ret['title'] = mailSubject
                    ret['content'] = mailContent
                    tipsList = []
                    for rewardType, itemId, itemNum in rewards:
                        if rewardType == gametypes.BONUS_TYPE_ITEM:
                            tipsList.append(uiUtils.getGfxItemById(itemId, itemNum))

                    ret['rewardItems'] = tipsList
                    break

        return ret

    def gmtRewardListHadItem(self):
        p = BigWorld.player()
        campInfo = getattr(p, 'compInfo', None)
        if campInfo:
            for camp in campInfo:
                _, rewardList = camp[:2]
                hadItem = any((reward[0] == gametypes.BONUS_TYPE_ITEM for reward in rewardList))
                if hadItem:
                    return True

        return False

    def _getInfoRewards(self, bonusId, extraItems):
        itemList = []
        if extraItems:
            for item in extraItems:
                data = uiUtils.getGfxItemById(item[0], item[1])
                itemList.append(data)

        if bonusId:
            items = BD.data.get(bonusId, {}).get('fixedBonus', [])
            items = utils.filtItemByConfig(items, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
            for item in items:
                if item[0] == gametypes.BONUS_TYPE_ITEM:
                    data = uiUtils.getGfxItemById(item[1], item[2])
                    itemList.append(data)

        return itemList

    def onGetRewards(self, *arg):
        p = BigWorld.player()
        if self.fromGMT and self.gmtRewardListHadItem():
            p.cell.getCompensationFromGUI(0)
            return
        if self.rewardData:
            subRewardData = self.rewardData.pop(0)
            rewardType = subRewardData.get('rewardType', 0)
            if rewardType:
                p.base.getActivityRewardFromNpc(rewardType)
        if len(self.rewardData) == 0:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_PUSH_BONUS)
        self.hide()

    def onClosePage(self, *arg):
        self.hide()

    def updatePageView(self):
        if self.mediator:
            ret = self._getInfoData()
            self.mediator.Invoke('updateView', uiUtils.dict2GfxDict(ret, True))
