#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/itemQuestProxy.o
from gamestrings import gameStrings
import types
import Math
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gamelog
import const
import questTypeConst
import gametypes
from guis import uiConst
from guis.uiProxy import DataProxy
from guis import uiUtils
from guis import tipUtils
from data import item_data as ID
from data import quest_data as QD
from data import seeker_data as SD
from cdata import font_config_data as FCD
from data import quest_loop_data as QLD
from data import npc_data as ND
SUCCESS = 1
FAILED = 2

class ItemQuestProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(ItemQuestProxy, self).__init__(uiAdapter)
        self.modelMap = {'getQuestDetail': self.onGetQuestDetail,
         'autoFindPath': self.onAutoFindPath,
         'acceptQuest': self.onAcceptQuest,
         'closePanel': self.onClosePanel,
         'showPosition': self.onShowPosition,
         'getTooltip': self.onGetToolTip}
        self.mediator = None
        self.questId = None
        self.loopId = None
        self.questDetail = None
        self.res = None
        self.itemId = None
        self.page = None
        self.pos = None
        self.isLoop = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_ITEM_QUEST, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ITEM_QUEST:
            self.mediator = mediator

    def show(self, res, itemId, vpage, vpos):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ITEM_QUEST)
        self.res = res
        self.page = vpage
        self.pos = vpos

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ITEM_QUEST)
        self.mediator = None
        self.isLoop = False

    def onGetQuestDetail(self, *arg):
        p = BigWorld.player()
        questId = 0
        loopId = 0
        if len(self.res['available_tasks']) > 0:
            questId = self.res['available_tasks'][0]['id']
            questInfo = self.res['available_tasks'][0]
            self.isLoop = False
        elif len(self.res['available_taskLoops']) > 0:
            questId = self.res['available_taskLoops'][0]['id']
            questInfo = self.res['available_taskLoops'][0]
            loopId = self.res['available_taskLoops'][0]['questLoopId']
            self.isLoop = True
        qd = QD.data.get(questId, {})
        region = qd.get('region', '')
        if region:
            region = gameStrings.TEXT_TIANYUMALLPROXY_1486 + region + gameStrings.TEXT_ITEMQUESTPROXY_85_1
        questName = qd.get('name', gameStrings.TEXT_ITEMQUESTPROXY_87)
        questDesc = qd.get('desc', gameStrings.TEXT_ITEMQUESTPROXY_87)
        moneyUp = False
        expUp = False
        if self.isLoop:
            qld = QLD.data.get(loopId, {})
            if qld:
                questDesc += p._genLoopInfo(loopId)
            else:
                region = ''
                questName = gameStrings.TEXT_ITEMQUESTPROXY_87
                questDesc = gameStrings.TEXT_ITEMQUESTPROXY_99
            loopReward = qld.get('loopReward', {})
            info = p.questLoopInfo.get(loopId, None)
            if info:
                curLoop = info.loopCnt
            else:
                curLoop = 0
            moneyUp = loopReward.get(const.LOOP_QUEST_MONEY, [])
            if curLoop < len(moneyUp):
                isMoneyUp = True if moneyUp[curLoop] == 2 else False
            else:
                isMoneyUp = False
            moneyUp = isMoneyUp
            expUp = loopReward.get(const.LOOP_QUEST_EXP, [])
            if curLoop < len(expUp):
                isExpUp = True if expUp[curLoop] == 2 else False
            else:
                isExpUp = False
            expUp = isExpUp
        expBonus = questInfo['expBonus']
        goldBonus = questInfo['goldBonus']
        lingshi = questInfo.get('lingshi', 0)
        acNpc = qd.get('acNpc', '')
        deliveryNpc = ND.data.get(acNpc, None)
        if deliveryNpc != None:
            questDeliveryNPC = uiUtils.getNpcName(acNpc)
            questDeliveryNPCTk = QD.data.get(questId, {}).get('acNpcTk', 0)
        else:
            questDeliveryNPC = ''
            questDeliveryNPCTk = 0
        questGoal = []
        rewardItems = []
        for item in questInfo['rewardItems']:
            path = uiUtils.getItemIconFile40(item[0])
            quality = ID.data.get(item[0], {}).get('quality', 1)
            color = '0x' + FCD.data.get(('item', quality), {}).get('color', '#FFFFFF')[1:]
            rewardItems.append([path,
             item[1],
             color,
             item[0]])

        rewardChoice = []
        for item in questInfo['rewardChoice']:
            path = uiUtils.getItemIconFile40(item[0])
            quality = ID.data.get(item[0], {}).get('quality', 1)
            color = '0x' + FCD.data.get(('item', quality), {}).get('color', '#FFFFFF')[1:]
            rewardChoice.append([path,
             item[1],
             color,
             item[0]])

        questType = questTypeConst.QUEST_TYPE_LOOP if qd.get('type', 1) == questTypeConst.QUEST_TYPE_LOOP and self.isLoop and qld.get('ranType', 0) != gametypes.QUEST_LOOP_SELECT_SEQUENCE else questTypeConst.QUEST_TYPE_ZHUXIAN
        ret = [region,
         questName,
         questDesc,
         False,
         questGoal,
         questDeliveryNPCTk,
         questDeliveryNPC,
         questType,
         {'money': goldBonus,
          'exp': expBonus,
          'lingshi': lingshi,
          'icon': rewardItems,
          'choiceIcon': rewardChoice,
          'moneyUp': moneyUp,
          'expUp': expUp}]
        return uiUtils.array2GfxAarry(ret, True)

    def onAutoFindPath(self, *arg):
        id = arg[3][0].GetString()
        uiUtils.findPosById(id)

    def onAcceptQuest(self, *arg):
        gamelog.debug('wy:onAcceptQuest', self.page, self.pos, self.isLoop)
        if self.isLoop:
            BigWorld.player().cell.acceptQuestLoopByItem(self.page, self.pos)
        else:
            BigWorld.player().cell.acceptQuestByItem(self.page, self.pos)
        self.clearWidget()

    def onClosePanel(self, *arg):
        self.clearWidget()

    def onShowPosition(self, *arg):
        id = arg[3][0].GetString()
        id = eval(id)
        p = BigWorld.player()
        if type(id) == types.TupleType:
            idList = list(id)
            minDis = -1
            index = 0
            for item in idList:
                data = SD.data.get(item, None)
                if data:
                    pos = Math.Vector3(data['xpos'], data['ypos'], data['zpos'])
                    spaceNo = data['spaceNo']
                    if p.spaceNo == spaceNo:
                        tempDis = (p.position - pos).length
                        if minDis == -1 or minDis > tempDis:
                            minDis = tempDis
                            index = item

            id = index
        if id == 0:
            return GfxValue('')
        elif SD.data.has_key(id):
            sd = SD.data.get(id, {})
            return GfxValue('%d , %d ,%d' % (sd.get('xpos', 0), sd.get('zpos', 0), sd.get('ypos', 0)))
        else:
            return

    def onGetToolTip(self, *arg):
        idx = int(arg[3][0].GetString())
        return tipUtils.getItemTipById(idx)
