#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/payItemProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
import commQuest
from guis import uiConst
from ui import gbk2unicode
from uiProxy import SlotDataProxy
from guis import uiUtils
from item import Item
from data import item_data as ID
from cdata import font_config_data as FCD
MAX_SLOT_NUM = 3

class PayItemProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(PayItemProxy, self).__init__(uiAdapter)
        self.modelMap = {'closePayItem': self.onClosePayItem,
         'submitPayItem': self.onSubmitPayItem,
         'getContent': self.onGetContent,
         'getSubmitBtnEnable': self.onGetSubmitBtnEnable,
         'getInitItem': self.onGetInitItem}
        self.bindType = 'payBag'
        self.type = 'payBag'
        self.reset()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_PAYITEM:
            self.mediator = mediator

    def getSlotID(self, key):
        idCon, idItem = key.split('.')
        return (0, int(idItem[4:]))

    def onClosePayItem(self, *arg):
        self.clearWidget()

    def onSubmitPayItem(self, *arg):
        if gameglobal.rds.ui.quest.isShow:
            gameglobal.rds.ui.quest.autoCommitItem(self.idNum, self.rewardChoice, self.questId, self.isLoop)
        elif gameglobal.rds.ui.npcV2.isShow:
            gameglobal.rds.ui.npcV2.autoCommitItem(self.idNum, self.rewardChoice, self.questId, self.isLoop)
        self.clearWidget()

    def onGetContent(self, *arg):
        ret = self.itemDesc
        if not ret:
            for index, itemId in enumerate(self.items):
                if self.itemNum[index]:
                    ret += '需要提交%d个%s\n' % (self.itemNum[index], ID.data.get(itemId, {}).get('name', ''))

        return GfxValue(gbk2unicode(ret))

    def onGetSubmitBtnEnable(self, *arg):
        if not self.questId:
            return GfxValue(False)
        return GfxValue(commQuest.isQuestItemSubmitComplete(BigWorld.player(), self.questId))

    def isItemInBag(self, value, num):
        p = BigWorld.player()
        inv = p.inv
        if Item.isQuestItem(value):
            inv = p.questBag
        if inv.hasItemInPages(value, num):
            page, pos = inv.findItemInPages(value, includeExpired=True, includeLatch=True, includeShihun=True)
            return (inv, page, pos)
        else:
            return (None, -1, -1)

    def onGetInitItem(self, *arg):
        ret = []
        for index, itemId in enumerate(self.items):
            if not itemId:
                ret.append([{}, uiConst.ITEM_NORMAL, 'nothing'])
                continue
            inv, pg, ps = self.isItemInBag(itemId, self.itemNum[index])
            if inv != None:
                it = inv.getQuickVal(pg, ps)
                self.curPage[index] = pg
                self.curPos[index] = ps
                self.questItem[index] = Item.isQuestItem(itemId)
                num = min(it.cwrap, self.itemNum[index])
                count = str(num) + '/' + str(self.itemNum[index])
                iconPath = uiUtils.getItemIconFile40(it.id)
                idValue = it.id
                self.showInBag(index, True)
            else:
                it = None
                iconPath = 'notFound'
                idValue = 0
                count = ''
                self.showInBag(index, False)
            state = uiConst.ITEM_NORMAL
            if hasattr(it, 'cdura'):
                if it.cdura == 0:
                    state = uiConst.EQUIP_BROKEN
                else:
                    state = uiConst.ITEM_NORMAL
            if hasattr(it, 'quality'):
                quality = it.quality
            else:
                quality = ID.data.get(idValue, {}).get('quality', 1)
            color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing') if it else 'nothing'
            ret.append([{'iconPath': iconPath,
              'count': count}, state, color])

        return uiUtils.array2GfxAarry(ret, True)

    def onNotifySlotUse(self, *arg):
        return
        key = arg[3][0].GetString()
        page, pos = self.getSlotID(key)
        self.removeItem(page, pos)

    def show(self, itemId, itemNum, idNum, rewardChoice, questId, isLoop, itemDesc = ''):
        self.items = itemId
        self.itemNum = itemNum
        self.items.extend([0] * (MAX_SLOT_NUM - len(itemId)))
        self.itemNum.extend([0] * (MAX_SLOT_NUM - len(itemNum)))
        self.idNum = idNum
        self.rewardChoice = rewardChoice
        self.questId = questId
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PAYITEM)
        gameglobal.rds.ui.inventory.show()
        self.isShow = True
        self.isLoop = isLoop
        self.itemDesc = itemDesc

    def clearWidget(self):
        self.closePayItem()
        gameglobal.rds.ui.inventory.hide()

    def closePayItem(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_PAYITEM)
        self.isShow = False
        for index, itemId in enumerate(self.items):
            self.showInBag(index, False)

    def reset(self):
        self.mediator = None
        self.isShow = False
        self.items = []
        self.curPage = [-1, -1, -1]
        self.curPos = [-1, -1, -1]
        self.questItem = [False, False, False]
        self.itemNum = []
        self.idNum = None
        self.rewardChoice = None
        self.questId = None
        self.bagPos = -1
        self.isLoop = False
        self.itemDesc = ''

    def setItem(self, nPageSrc, nItemSrc, nPageDes, nItemDes):
        item = BigWorld.player().inv.getQuickVal(nPageSrc, nItemSrc)
        if item:
            if item.id != self.items[nItemDes]:
                BigWorld.player().showTopMsg('所缴纳的道具错误')
                return
            self.curPage[nItemDes] = nPageSrc
            self.curPos[nItemDes] = nItemSrc
            self.questItem[nItemDes] = False
            key = 'payBag.slot%d' % nItemDes
            if self.binding.get(key, None):
                if nItemDes < len(self.itemNum):
                    need = self.itemNum[nItemDes]
                else:
                    need = 0
                num = min(item.cwrap, need)
                count = '%d/%d' % (num, need)
                state = uiConst.EQUIP_BROKEN if hasattr(item, 'cdura') and item.cdura == 0 else uiConst.ITEM_NORMAL
                data = uiUtils.getGfxItem(item, appendInfo={'count': count,
                 'state': state})
                self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data, True))

    def removeItem(self, page, pos):
        key = 'payBag.slot%d' % pos
        if self.binding.get(key, None):
            data = GfxValue(1)
            data.SetNull()
            self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_NORMAL))
            self.binding[key][0].Invoke('setSlotColor', GfxValue('nothing'))
            self.binding[key][1].InvokeSelf(data)
            self.curPage[pos] = -1
            self.curPos[pos] = -1
            self.questItem[pos] = False

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        page, pos = self.getSlotID(key)
        if self.curPage[pos] == None or self.curPos[pos] == None:
            return
        if self.questItem[pos]:
            i = BigWorld.player().questBag.getQuickVal(self.curPage[pos], self.curPos[pos])
        else:
            i = BigWorld.player().inv.getQuickVal(self.curPage[pos], self.curPos[pos])
        if i == None:
            return
        return gameglobal.rds.ui.inventory.GfxToolTip(i)

    def showInBag(self, index, visible):
        p = BigWorld.player()
        pg = self.curPage[index]
        ps = self.curPos[index]
        num = self.itemNum[index]
        if ps == -1:
            return
        it = const.CONT_EMPTY_VAL
        if self.questItem[index]:
            it = p.questBag.getQuickVal(pg, ps)
        elif gameglobal.rds.ui.inventory.page == pg:
            it = p.inv.getQuickVal(pg, ps)
        if it and it.id in self.items and hasattr(it, 'cwrap') and it.cwrap >= num:
            gameglobal.rds.ui.inventory.showWarnEffect(ps, visible)
        else:
            gameglobal.rds.ui.inventory.showWarnEffect(ps, False)

    def refreshPayBag(self):
        if self.mediator != None:
            self.mediator.Invoke('refreshPayBag')
