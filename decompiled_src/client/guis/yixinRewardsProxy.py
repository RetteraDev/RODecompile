#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/yixinRewardsProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
import commcalc
import gametypes
import utils
from guis import uiConst
from guis.uiProxy import UIProxy
from guis import uiUtils
from cdata import game_msg_def_data as GMDD
from data import yixin_reward_data as YRD
from data import sys_config_data as SCD
from data import bonus_data as BD
from data import item_data as ID
from cdata import font_config_data as FCD

class YixinRewardsProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(YixinRewardsProxy, self).__init__(uiAdapter)
        self.modelMap = {'dismiss': self.dismiss,
         'openInstallGuild': self.openInstallGuild,
         'openSetPhotoGuild': self.openSetPhotoGuild,
         'setAutoAdd': self.setAutoAdd,
         'getReward': self.getReward}
        self.mediator = None
        self.isShow = False
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_YIXIN_REWARDS, self.closeWidget)

    def reset(self):
        self.dismiss()

    def setAutoAdd(self, *args):
        ret = args[3][0].GetBool()
        BigWorld.player().base.setYixinAutoAcceptFriend(ret)

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator
        self.refreshPanel()
        BigWorld.player().base.queryYixinReward()
        BigWorld.player().registerEvent(const.EVENT_YIXIN_REWARDS_CHANGE, self.getYixinReward)
        BigWorld.player().registerEvent(const.EVENT_YIXIN_UNBIND_SUCCESS, self.getUnBindEvent)
        self.mediator.Invoke('setSelectedAuto', GfxValue(BigWorld.player().yixinSetting['autoAcceptFriend']))

    def getUnBindEvent(self, params):
        self.closeWidget()

    def refreshPanel(self):
        panelData = []
        keys = YRD.data.keys()
        keys.sort()
        for key in keys:
            data = {}
            currentData = YRD.data[key]
            data['bonusTitle'] = currentData['bonusTitle']
            data['id'] = key
            data['conditionDesc'] = currentData['conditionDesc']
            bonusId = currentData['bonusId']
            fixedBonus = BD.data.get(bonusId, {}).get('fixedBonus', ())
            fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
            bonusItem = []
            bonusItemId = []
            for i in range(0, len(fixedBonus)):
                item = self.__getBonusInfo(fixedBonus, i)
                bonusItem.append(self.__getItemsName(item))
                bonusItemId.append(item[5])

            data['bonusItems'] = bonusItem
            data['bonusItemIds'] = bonusItemId
            if commcalc.getBit(BigWorld.player().yixinRewardList, data['id']):
                data['gotten'] = True
            else:
                data['gotten'] = False
            panelData.append(data)

        self.mediator.Invoke('refreshPanel', uiUtils.array2GfxAarry(panelData, True))

    def __getBonusInfo(self, fixedBonus, index, icon64 = False, forceIcon = False):
        bonusInfo = []
        idd = ID.data
        fcdd = FCD.data
        index = 0 if index >= len(fixedBonus) else index
        bonusType, bonusItemId, bonusNum = fixedBonus[index]
        bonusInfo.insert(0, bonusType)
        bonusInfo.insert(1, bonusNum)
        if bonusType == gametypes.BONUS_TYPE_ITEM or forceIcon:
            itemInfo = idd.get(bonusItemId, {})
            quality = itemInfo.get('quality', 1)
            color = fcdd.get(('item', quality), {}).get('qualitycolor', 'nothing')
            if icon64:
                bonusInfo.insert(2, uiUtils.getItemIconFile64(bonusItemId))
            else:
                bonusInfo.insert(2, uiConst.ITEM_ICON_IMAGE_RES_40 + str(itemInfo.get('icon', 'notFound')) + '.dds')
            bonusInfo.insert(3, itemInfo.get('name', gameStrings.TEXT_TIANYUMALLPROXY_1455))
            bonusInfo.insert(4, color)
            bonusInfo.insert(5, bonusItemId)
        return bonusInfo

    def __getItemsName(self, ret):
        nameMap = {gametypes.BONUS_TYPE_MONEY: gameStrings.TEXT_INVENTORYPROXY_3297,
         gametypes.BONUS_TYPE_FAME: gameStrings.TEXT_CHALLENGEPROXY_199_1,
         gametypes.BONUS_TYPE_EXP: gameStrings.TEXT_GAMETYPES_6408,
         gametypes.BONUS_TYPE_FISHING_EXP: gameStrings.TEXT_ARENARANKAWARDPROXY_213,
         gametypes.BONUS_TYPE_SOC_EXP: gameStrings.TEXT_IMPL_IMPACTIVITIES_663}
        name = ''
        if ret[0] == gametypes.BONUS_TYPE_ITEM:
            name = ret[3] + gameStrings.TEXT_HISTORYCONSUMEDPROXY_256 + str(ret[1])
        else:
            name = str(ret[1]) + gameStrings.TEXT_HISTORYCONSUMEDPROXY_256 + nameMap.get(ret[0])
        return name

    def dismiss(self, *arg):
        self.closeWidget()

    def closeWidget(self):
        if self.isShow:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_YIXIN_REWARDS)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()
        self.isShow = False
        self.mediator = None
        if BigWorld.player():
            if BigWorld.player().__class__.__name__ == 'PlayerAvatar':
                BigWorld.player().unRegisterEvent(const.EVENT_YIXIN_REWARDS_CHANGE, self.getYixinReward)
                BigWorld.player().unRegisterEvent(const.EVENT_YIXIN_UNBIND_SUCCESS, self.getUnBindEvent)

    def getYixinReward(self, params):
        result = params[0]
        self.refreshPanel()
        if result != const.REFRESH_YIXIN_REWARD and result != const.YIXIN_NO_ERROR:
            msg = 0
            if result == const.YIXIN_ERR_REWARD_ALREADY_SET:
                msg = GMDD.data.YIXIN_ERR_REWARD_ALREADY_SET
            elif result == const.YIXIN_ERR_TYPE_OVERFLOW:
                msg = GMDD.data.YIXIN_ERR_TYPE_OVERFLOW
            elif result == const.YIXIN_ERR_NOT_SET_PHOTO:
                msg = GMDD.data.YIXIN_ERR_NOT_SET_PHOTO
            elif result == const.YIXIN_ERR_NOT_BIND:
                msg = GMDD.data.YIXIN_ERR_NOT_BIND
            if msg:
                BigWorld.player().showGameMsg(msg, ())

    def toggle(self):
        if self.isShow:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_YIXIN_REWARDS)
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_YIXIN_REWARDS)
        self.isShow = not self.isShow

    def show(self):
        isShowYixin = gameglobal.rds.configData.get('enableYixin', False)
        if not isShowYixin:
            return
        if not self.isShow:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_YIXIN_REWARDS)
            self.isShow = True

    def openInstallGuild(self, *args):
        url = SCD.data.get('yixinInstallUrl', '')
        BigWorld.openUrl(url)

    def openSetPhotoGuild(self, *args):
        url = SCD.data.get('yixinSetPhotoUrl', '')
        BigWorld.openUrl(url)

    def getReward(self, *args):
        rid = int(args[3][0].GetNumber())
        BigWorld.player().base.getYixinReward(rid)
