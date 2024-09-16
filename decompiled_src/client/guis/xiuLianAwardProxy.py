#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/xiuLianAwardProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import clientUtils
import utils
from Scaleform import GfxValue
from uiProxy import SlotDataProxy
from guis import uiConst
from guis import uiUtils
from cdata import skill_enhance_bonus_data as SEBD
UNACHIEVE_XIULIAN = 0
ACHIEVE_XIULIAN = 1
FETCH_XIULIAN = 2

class XiuLianAwardProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(XiuLianAwardProxy, self).__init__(uiAdapter)
        self.modelMap = {'getInfo': self.onGetInfo,
         'getBonus': self.onGetBonus}
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_XIULIAN_AWARD, self.hide)

    def show(self):
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_XIULIAN_AWARD)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_XIULIAN_AWARD:
            self.mediator = mediator

    def reset(self):
        super(self.__class__, self).reset()
        self.mediator = None

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        if self.mediator:
            self.mediator = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_XIULIAN_AWARD)

    def onGetInfo(self, *arg):
        info = []
        ThreeItemInfo = []
        for point in sorted(SEBD.data.keys()):
            itemInfo = self.getPointInfo(point)
            ThreeItemInfo.append(itemInfo)
            if len(ThreeItemInfo) >= 3:
                info.append(ThreeItemInfo)
                ThreeItemInfo = []

        if ThreeItemInfo and len(ThreeItemInfo) > 0:
            info.append(ThreeItemInfo)
        return uiUtils.array2GfxAarry(info, True)

    def onGetBonus(self, *arg):
        point = int(arg[3][0].GetNumber())
        BigWorld.player().cell.getSkillEnhanceBonus(point)

    def refreshIcon(self, point):
        itemInfo = self.getPointInfo(point)
        if self.mediator:
            self.mediator.Invoke('refreshIcon', (GfxValue(point), uiUtils.dict2GfxDict(itemInfo, True)))

    def getPointInfo(self, point):
        p = BigWorld.player()
        itemInfo = {}
        awardData = SEBD.data.get(point, {})
        itemInfo['awardPointDesc'] = gameStrings.TEXT_XIULIANAWARDPROXY_79 % point
        itemInfo['point'] = point
        if awardData:
            questId = awardData.get('questId', 0)
            bonusId = awardData.get('bonusId', 0)
            myEnhPoint = utils.getTotalSkillEnhancePoint(p)
            if point in p.skillEnhancePointBonus:
                itemInfo['getFlag'] = FETCH_XIULIAN
            elif myEnhPoint < point:
                itemInfo['getFlag'] = UNACHIEVE_XIULIAN
            elif not p.getQuestFlag(questId):
                itemInfo['getFlag'] = ACHIEVE_XIULIAN
            else:
                itemInfo['getFlag'] = FETCH_XIULIAN
            if bonusId:
                rewardItems = clientUtils.genItemBonus(bonusId)
                itemList = []
                for itemId, itemNum in rewardItems:
                    iconPath = uiUtils.getItemIconFile64(itemId)
                    icon = {'iconPath': iconPath,
                     'itemId': itemId,
                     'count': itemNum}
                    itemList.append(icon)

                itemInfo['itemList'] = itemList
        return itemInfo
