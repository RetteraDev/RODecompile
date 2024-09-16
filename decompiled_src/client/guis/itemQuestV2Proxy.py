#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/itemQuestV2Proxy.o
import BigWorld
import utils
import uiConst
import gametypes
import clientUtils
from gamestrings import gameStrings
from Scaleform import GfxValue
from uiProxy import UIProxy
from guis import uiUtils
from guis.asObject import ASObject
from data import quest_data as QD
from data import sys_config_data as SCD
from data import mail_template_data as MTD
DETAIL_ITEM_OFFSET_Y = 42
ITEM_MAX_CNT = 5

class ItemQuestV2Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ItemQuestV2Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ITEM_QUEST_V2, self.hide)

    def reset(self):
        self.type = None
        self.res = None
        self.page = None
        self.pos = None
        self.isLoop = False
        self.compId = 0
        self.contentTextMc = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ITEM_QUEST_V2:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ITEM_QUEST_V2)

    def show(self, type, res, page, pos):
        self.type = type
        self.res = res
        self.page = page
        self.pos = pos
        if self.widget:
            self.refreshInfo()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ITEM_QUEST_V2)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.contentTextMc = self.widget.getInstByClsName('ItemQuestV2_contentText')
        self.widget.mainDesc.itemRenderer = 'ItemQuestV2_contentText'
        self.widget.mainDesc.dataArray = []
        self.widget.mainDesc.lableFunction = self.itemTextFunction
        self.widget.mainDesc.itemHeightFunction = self.itemHeightFunction

    def refreshInfo(self):
        if not self.widget:
            return
        if self.type == uiConst.ITEM_QUEST_V2_TYPE_QUEST:
            self.refreshQuestInfo()
        else:
            self.refreshCompensatinInfo()

    def refreshCompensatinInfo(self):
        if not self.widget:
            return
        self.widget.confirmBtn.label = gameStrings.ITEM_QUEST_V2_CONFRIM_DESC_COMP
        p = BigWorld.player()
        compInfo = getattr(p, 'compInfo', [])
        if not compInfo:
            return
        lastCompInfo = compInfo[-1]
        mailSubject, mailContent, rewardList, id, compType = clientUtils.unpackCompInfo(lastCompInfo)
        self.widget.title.text = mailSubject
        self.compId = id
        contentList = []
        contentList.append({'desc': mailContent})
        self.widget.mainDesc.dataArray = contentList
        self.widget.timeDesc.visible = False
        detailList = []
        itemList = []
        for reward in rewardList:
            bonusType, itemId, itemNum = reward
            if bonusType == gametypes.BONUS_TYPE_ITEM:
                itemInfo = uiUtils.getGfxItemById(int(itemId), itemNum)
                itemList.append(itemInfo)
            elif bonusType == gametypes.BONUS_TYPE_EXP:
                detailList.append(('exp', itemNum))
            elif bonusType == gametypes.BONUS_TYPE_MONEY:
                if itemId == gametypes.CASH_ITEM:
                    detailList.append(('cash', itemNum))
                elif itemId == gametypes.BIND_CASH_ITEM:
                    detailList.append(('bindCash', itemNum))

        self.widget.reward.itemList.visible = True
        self.refreshRewardDetailList(detailList)
        self.refreshItemList(itemList)

    def itemTextFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.contentText.htmlText = itemData.desc
        itemMc.contentText.height = itemMc.contentText.textHeight + 5

    def itemHeightFunction(self, *args):
        if not self.contentTextMc:
            return
        itemData = ASObject(args[3][0])
        self.contentTextMc.contentText.htmlText = itemData.desc
        return GfxValue(self.contentTextMc.contentText.textHeight + 5)

    def refreshQuestInfo(self):
        if not self.widget:
            return
        self.widget.confirmBtn.label = gameStrings.ITEM_QUEST_V2_CONFRIM_DESC_QUEST
        if len(self.res['available_tasks']) > 0:
            questInfo = self.res['available_tasks'][0]
            self.isLoop = False
        elif len(self.res['available_taskLoops']) > 0:
            questInfo = self.res['available_taskLoops'][0]
            self.isLoop = True
        else:
            return
        questId = questInfo.get('id', 0)
        qdData = QD.data.get(questId, {})
        self.widget.title.text = qdData.get('name', '')
        contentList = []
        shortDesc = qdData.get('shortDesc', '')
        contentList.append({'desc': shortDesc})
        self.widget.mainDesc.dataArray = contentList
        self.widget.timeDesc.visible = True
        self.widget.timeDesc.desc.text = utils.formatTimeStr(qdData.get('timeLimit', 0), 'h:m:s', True, 2, 2, 2)
        self.widget.reward.visible = True
        expBonus = questInfo.get('expBonus', 0)
        goldBonus = questInfo.get('goldBonus', 0)
        lingshi = questInfo.get('lingshi', 0)
        detailList = [('exp', expBonus), ('bindCash', goldBonus), ('lingshi', lingshi)]
        self.refreshRewardDetailList(detailList)
        self.widget.reward.itemList.visible = False
        self.refreshItemList()

    def refreshItemList(self, itemList = []):
        for i in xrange(ITEM_MAX_CNT):
            itemMc = self.widget.reward.itemList.getChildByName('item%d' % i)
            dituMc = self.widget.reward.itemList.ditu.getChildByName('bg%d' % i)
            if i < len(itemList):
                itemMc.visible = True
                dituMc.visible = True
                itemMc.slot.setItemSlotData(itemList[i])
            else:
                itemMc.visible = False
                dituMc.visible = False

    def refreshRewardDetailList(self, detailList):
        if not self.widget:
            return
        starMapDescDict = SCD.data.get('starMapDescDict', {})
        self.widget.removeAllInst(self.widget.reward.detailList)
        posY = 0
        for i in xrange(len(detailList)):
            value = detailList[i][1]
            if value <= 0:
                continue
            itemMc = self.widget.getInstByClsName('ItemQuestV2_DetailItem')
            if not itemMc:
                continue
            itemMc.descIcon.bonusType = detailList[i][0]
            itemMc.desc.text = starMapDescDict.get(value, '') if self.type == uiConst.ITEM_QUEST_V2_TYPE_QUEST else str(value)
            itemMc.y = posY
            posY += DETAIL_ITEM_OFFSET_Y
            self.widget.reward.detailList.addChild(itemMc)

    def _onConfirmBtnClick(self, *args):
        p = BigWorld.player()
        if self.type == uiConst.ITEM_QUEST_V2_TYPE_QUEST:
            if self.isLoop:
                p.cell.acceptQuestLoopByItem(self.page, self.pos)
            else:
                p.cell.acceptQuestByItem(self.page, self.pos)
            self.hide()
        else:
            p.cell.getCompensationFromGUI(self.compId)

    def isCompInfoEmpty(self):
        p = BigWorld.player()
        compInfo = getattr(p, 'compInfo', [])
        if not compInfo:
            return True
        lastCompInfo = compInfo[-1]
        mailTemplateId, rewardList = lastCompInfo[:2]
        return len(rewardList) == 0
