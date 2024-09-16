#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/npcSendGiftProxy.o
import BigWorld
from Scaleform import GfxValue
import gameconfigCommon
import gameglobal
import const
import gamelog
import commNpcFavor
from gamestrings import gameStrings
from callbackHelper import Functor
import uiConst
from guis import events
from item import Item
from guis import uiUtils
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis.asObject import TipManager
from guis import ui
from uiProxy import UIProxy
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from data import nf_npc_data as NND
from data import nf_npc_friendly_level_data as NNFLD
from data import equip_data as ED
from data import sys_config_data as SCD
from data import nf_ask_item_data as NAID
from data import nf_give_item_group_data as NGIGD
from data import nf_npc_level_data as NFNLD
from data import equip_gem_data as EGD
ITEM_TYPE_NORMAL = 0
ITEM_TYPE_QUEST = 1
ITEM_TYPE_XINDONG = 2
TEXT_COLOR_RED = '#d34024'
TEXT_COLOR_NORMAL = '#327423'

class NpcSendGiftProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NpcSendGiftProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.multiId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_NPC_SEND_GIFT, self.hide)

    def reset(self):
        self.tabIdx = uiConst.NPC_SEND_GIFT_TAB
        self.entId = 0
        self.npcId = 0
        self.tabMcList = []
        self.selectedMc = None
        self.selectedItemUuid = None
        self.selectedItemId = 0
        self.selectedGId = 0
        self.itemGIdDic = {}
        self.selectedMainTypeMc = None
        self.lockDesc = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_NPC_SEND_GIFT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_NPC_SEND_GIFT)

    def show(self, tabIdx = uiConst.NPC_SEND_GIFT_TAB, entId = 0, npcId = 0):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_NPC_SEND_GIFT)
        self.tabIdx = tabIdx
        self.entId = entId
        self.npcId = npcId

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.clostBtn
        self.widget.tabSend.addEventListener(events.BUTTON_CLICK, self.handleTabSendBtnClick, False, 0, True)
        self.widget.askBtn.addEventListener(events.BUTTON_CLICK, self.handleTabSureBtnClick, False, 0, True)
        favroNpcPid, _ = BigWorld.player().npcFavor.todayFavor
        if favroNpcPid == self.npcId:
            self.widget.tabASk.disabled = False
            self.widget.tabASk.addEventListener(events.BUTTON_CLICK, self.handleTabASKBtnClick, False, 0, True)
        else:
            self.widget.tabASk.disabled = True
            TipManager.addTip(self.widget.tabASk, gameStrings.NPC_CAN_NOT_ASK_TODAY)
        self.widget.chooseItems.hideItemsBtn.addEventListener(events.BUTTON_CLICK, self.handleHideItemsBtnClick, False, 0, True)
        self.widget.chooseItems.visible = False
        self.widget.chooseItems.itemScrollWndList.itemRenderer = 'NpcSendGift_ItemRender'
        self.widget.chooseItems.itemScrollWndList.labelFunction = self.labelFunction
        self.widget.chooseItems.itemScrollWndList.column = 4
        self.widget.chooseItems.itemScrollWndList.itemWidth = 58
        self.widget.chooseItems.itemScrollWndList.itemHeight = 60
        self.widget.chooseItems.sureBtn.addEventListener(events.BUTTON_CLICK, self.handleSureBtnClick, False, 0, True)
        self.widget.chooseItems.dailyTips.txtDesc.text = SCD.data.get('npcSendGiftTips', 'npcSendGiftTips')

    def handleSureBtnClick(self, *args):
        if not self.selectedMc or not self.selectedItemId:
            return
        pos = self.selectedMc.slot.data['pos']
        resKind, page, pos = int(pos[0]), int(pos[1]), int(pos[2])
        item = self.getItem(resKind, page, pos)
        if not item:
            return
        p = BigWorld.player()
        itemId = item.id
        addValue = p.npcFavor.getSendUpValue(self.npcId, item, 1)
        if self.npcId == p.npcFavor.todayFavor[0]:
            addStrFormat = gameStrings.NPC_INTERACTIVE_DAILY_UP
        else:
            level, pVal = p.npcFavor.getPlayerRelationLvAndVal(self.npcId)
            if p.npcFavor.isLockLvState(self.npcId, level) and gameconfigCommon.enableNFNewQuestLoop():
                addStrFormat = gameStrings.NPC_INTERACTIVE_WHEART_BEAT
            else:
                addStrFormat = gameStrings.NPC_INTERACTIVE_UP
        addValueStr = uiUtils.toHtml(addStrFormat % addValue, '#74C424') + '                 ' + '\n' + SCD.data.get('NPC_INTERACTIVE_UP_TIP', '')
        maxCount = int(self.selectedMc.slot.data.count)
        resKind, page, pos = self.selectedMc.slot.data.pos
        location = self.getLocation(resKind)
        itemGId = commNpcFavor.getGiveItemGId(item)
        dailyMaxCnt = NGIGD.data.get(itemGId, {}).get('dailyMaxCnt', 0)
        if dailyMaxCnt:
            itemCount = dailyMaxCnt - BigWorld.player().npcFavor.todaySendItemRecord.get(itemGId, {}).get(self.npcId, 0)
            maxCount = min(maxCount, itemCount)
        maxCount = max(1, maxCount)
        self.multiId = self.uiAdapter.messageBox.showCounterMsgBox(addValueStr, yesCallback=Functor(self.confirmTabSureCallback, self.uiAdapter.npcInteractive.getNormalNpcId(), itemId, resKind, page, pos), counterData=uiUtils.getGfxItem(item, appendInfo={'defaultCount': 1}, location=location), counterRange=(1, maxCount), title=gameStrings.NPC_SEND_GIFT_CONFIRM, counterChangeCallback=Functor(self.addValueCounterChangeCallback, uiUtils.toHtml(addStrFormat, '#74C424'), self.npcId, item))

    def handleHideItemsBtnClick(self, *args):
        self.widget.chooseItems.visible = False

    def getAskInfo(self):
        infoList = []
        p = BigWorld.player()
        level, _ = p.npcFavor.getPlayerRelationLvAndVal(self.npcId)
        for itemId in p.npcFavor.askItemList:
            data = NAID.data.get(itemId, {})
            if data.get('npcPIdList', ()) and self.npcId not in data['npcPIdList']:
                continue
            itemInfo = uiUtils.getGfxItemById(itemId)
            itemInfo['uuid'] = str(itemId).encode('hex')
            itemInfo['needType'] = ITEM_TYPE_NORMAL
            itemInfo['count'] = 1
            askFriendlyLvLimit = data.get('askFriendlyLvLimit', 0)
            itemInfo['isLocked'] = level < askFriendlyLvLimit
            itemInfo['sortOrder'] = data.get('sortOrder', 0)
            npcLv = NND.data.get(self.npcId, {}).get('npcLv', 0)
            lockDesc = ''
            if level < askFriendlyLvLimit:
                lockDesc = gameStrings.NPC_ASK_ITEM_LOCK_LV % NNFLD.data.get((npcLv, askFriendlyLvLimit), {}).get('friendlyName', '')
            permanentMaxCnt = data.get('permanentMaxCnt', 0)
            if permanentMaxCnt:
                if lockDesc:
                    lockDesc += '\n'
                lockDesc += gameStrings.NPC_ASK_LEFT_CNT % (permanentMaxCnt - p.npcFavor.askRecord.get(itemId, 0), permanentMaxCnt)
            self.lockDesc[itemId] = lockDesc
            infoList.append(itemInfo)

        infoList.sort(cmp=lambda a, b: cmp(a['sortOrder'], b['sortOrder']))
        return infoList

    def checkItem(self, it):
        if not it:
            return False
        if getattr(it, 'latchOfCipher', False):
            return False
        id = Item.parentId(it.id)
        if it.isEquipGem() and EGD.data.get(id, {}).get('lv', 0) > SCD.data.get('nfEquipGemLimitLv', 0):
            return False
        if it.isRune() and Item.getRuneCfgData(id).get('lv', 0) > SCD.data.get('nfHierogramLimitLv', 0):
            return False
        ed = ED.data.get(id)
        if not ed:
            return True
        etp = ed.get('equipType')
        atp = ed.get('armorSType')
        jtp = ed.get('jewelSType')
        valid = etp == Item.EQUIP_BASETYPE_WEAPON or etp == Item.EQUIP_BASETYPE_ARMOR and atp in commNpcFavor.NF_ITEM_ARMOR_TYPE or etp == Item.EQUIP_BASETYPE_JEWELRY and jtp in commNpcFavor.NF_ITEM_JEWEL_TYPE
        return valid

    def getItemGIdDic(self):
        self.itemGIdDic.clear()
        p = BigWorld.player()
        for page, poss in enumerate(p.inv.pages):
            for pos, item in enumerate(poss):
                if not self.checkItem(item):
                    continue
                itemGId = commNpcFavor.getGiveItemGId(item) if item else 0
                if itemGId:
                    self.itemGIdDic.setdefault(itemGId, []).append((const.RES_KIND_INV, page, pos))

        for page, poss in enumerate(p.hierogramBag.pages):
            for pos, item in enumerate(poss):
                if not self.checkItem(item):
                    continue
                itemGId = commNpcFavor.getGiveItemGId(item) if item else 0
                if itemGId:
                    self.itemGIdDic.setdefault(itemGId, []).append((const.RES_KIND_HIEROGRAM_BAG, page, pos))

        for page, poss in enumerate(p.materialBag.pages):
            for pos, item in enumerate(poss):
                if not self.checkItem(item):
                    continue
                itemGId = commNpcFavor.getGiveItemGId(item) if item else 0
                if itemGId:
                    self.itemGIdDic.setdefault(itemGId, []).append((const.RES_KIND_MATERIAL_BAG, page, pos))

    def getItem(self, resKind, page, pos):
        p = BigWorld.player()
        if resKind == const.RES_KIND_INV:
            return p.inv.pages[page][pos]
        elif resKind == const.RES_KIND_HIEROGRAM_BAG:
            return p.hierogramBag.pages[page][pos]
        else:
            return p.materialBag.pages[page][pos]

    def refreshInfo(self):
        if not self.widget:
            return
        self.getItemGIdDic()
        self.widget.tabSend.selected = self.tabIdx == uiConst.NPC_SEND_GIFT_TAB
        self.widget.tabASk.selected = self.tabIdx == uiConst.NPC_ASK_GIFT_TAB
        if self.tabIdx == uiConst.NPC_SEND_GIFT_TAB:
            self.refreshSend()
        else:
            self.refreshAsk()

    def mainTypeLabelFunction(self, *args):
        itemGId = int(args[3][0].GetNumber())
        itemMc = ASObject(args[3][1])
        cfgData = NGIGD.data.get(itemGId, {})
        itemMc.txtName.text = cfgData.get('GroupName', '')
        itemMc.typeButton.selected = itemGId == self.selectedGId
        if itemMc.typeButton.selected:
            if self.selectedMainTypeMc:
                self.selectedMainTypeMc.selected = False
            self.selectedMainTypeMc = itemMc.typeButton
        itemMc.itemGId = itemGId
        itemMc.typeButton.rewardMc.icon.fitSize = True
        itemMc.typeButton.rewardMc.icon.loadImage(uiConst.ITEM_ICON_IMAGE_RES_64 + str(cfgData.get('icon', 999)) + '.dds')
        itemMc.typeButton.enabled = bool(self.itemGIdDic.get(itemGId, []))
        itemMc.typeButton.data = itemGId
        itemMc.typeButton.addEventListener(events.BUTTON_CLICK, self.handleMainTypeClick, False, 0, True)
        p = BigWorld.player()
        itemMc.typeButton.isQuest.visible = p.npcFavor.isQuestItem(self.npcId, itemGId)
        loveCurCnt = p.npcFavor.favorSendCnt.get(self.npcId, 0)
        loveMaxCnt = SCD.data.get('nfLoveCount', 0)
        itemMc.typeButton.isFavor.visible = itemGId == p.npcFavor.favorGroups.get(self.npcId, 0) and loveCurCnt < loveMaxCnt
        ASUtils.setHitTestDisable(itemMc.typeButton.isFavor, True)
        ASUtils.setHitTestDisable(itemMc.typeButton.isQuest, True)

    def handleMainTypeClick(self, *args):
        gameglobal.rds.sound.playSound(2)
        e = ASObject(args[3][0])
        if int(e.currentTarget.data) == self.selectedGId:
            self.widget.chooseItems.visible = True
            return
        else:
            self.selectedGId = int(e.currentTarget.data)
            if self.selectedMainTypeMc:
                self.selectedMainTypeMc.selected = False
            self.selectedMainTypeMc = e.currentTarget
            self.selectedMainTypeMc.selected = True
            self.selectedItemUuid = ''
            self.selectedItemId = 0
            if self.selectedMc:
                self.selectedMc.slot.setSlotState(uiConst.ITEM_NORMAL)
                self.selectedMc = None
            self.refreshSendItemList()
            return

    def refreshSendItemList(self):
        if self.selectedGId:
            self.widget.chooseItems.visible = True
            self.widget.chooseItems.typeName.txt.text = NGIGD.data.get(self.selectedGId, {}).get('GroupName', '')
            self.widget.chooseItems.itemScrollWndList.dataArray = self.itemGIdDic.get(self.selectedGId, [])
        else:
            self.widget.chooseItems.visible = False
        if self.selectedMc:
            pos = self.selectedMc.slot.data['pos']
            resKind, page, pos = int(pos[0]), int(pos[1]), int(pos[2])
            item = self.getItem(resKind, page, pos)
            itemGId = commNpcFavor.getGiveItemGId(item)
            dailyMaxCnt = NGIGD.data.get(itemGId, {}).get('dailyMaxCnt', 0)
            if dailyMaxCnt:
                itemCount = dailyMaxCnt - BigWorld.player().npcFavor.todaySendItemRecord.get(itemGId, {}).get(self.npcId, 0)
                itemCount = max(0, itemCount)
                self.widget.chooseItems.leftItemCnt.text = gameStrings.NPC_ITEM_SEND_LEFT_CNT % itemCount if itemCount else ''
            else:
                self.widget.chooseItems.leftItemCnt.text = gameStrings.NPC_ITEM_SEND_UMLIMIT_CNT
        else:
            self.widget.chooseItems.leftItemCnt.text = ''

    def refreshSend(self):
        self.lockDesc.clear()
        self.widget.chooseItems.visible = True
        self.widget.sendGiftTips.visible = True
        p = BigWorld.player()
        if NND.data.get(self.npcId, {}).get('dailyMaxCnt', 0):
            leftCnt = NND.data.get(self.npcId, {}).get('dailyMaxCnt', 0) - p.npcFavor.todaySendNpcRecord.get(self.npcId, 0)
            leftCnt = max(0, leftCnt)
            self.widget.leftNpcSend.text = gameStrings.NPC_SEND_LEFT_CNT % leftCnt
        else:
            self.widget.leftNpcSend.text = gameStrings.NPC_SEND_UNLIMIT_CNT
        self.widget.askBtn.visible = False
        self.widget.mainTypeScrollList.itemRenderer = 'NpcSendGift_MainTypeItemRender'
        self.widget.mainTypeScrollList.column = 3
        self.widget.mainTypeScrollList.itemWidth = 84
        self.widget.mainTypeScrollList.itemHeight = 96
        self.widget.mainTypeScrollList.labelFunction = self.mainTypeLabelFunction
        keys = NGIGD.data.keys()
        keys.sort()
        self.widget.mainTypeScrollList.dataArray = keys
        self.refreshSendItemList()

    def refreshAsk(self):
        self.lockDesc = {}
        self.widget.chooseItems.visible = False
        self.widget.sendGiftTips.visible = False
        self.widget.leftNpcSend.text = ''
        self.widget.askBtn.visible = True
        self.widget.mainTypeScrollList.itemRenderer = 'NpcSendGift_ItemRender'
        self.widget.mainTypeScrollList.labelFunction = self.askGiftLabelFunciton
        self.widget.mainTypeScrollList.column = 4
        self.widget.mainTypeScrollList.itemWidth = 60
        self.widget.mainTypeScrollList.itemHeight = 60
        self.widget.mainTypeScrollList.dataArray = self.getAskInfo()

    def handleTabSendBtnClick(self, *args):
        if self.tabIdx == uiConst.NPC_SEND_GIFT_TAB:
            return
        else:
            self.selectedMc = None
            self.selectedItemId = 0
            self.selectedItemUuid = 0
            self.selectedGId = 0
            self.tabIdx = uiConst.NPC_SEND_GIFT_TAB
            self.refreshInfo()
            return

    def handleTabASKBtnClick(self, *args):
        if self.tabIdx == uiConst.NPC_ASK_GIFT_TAB:
            return
        else:
            self.selectedMc = None
            self.selectedItemId = 0
            self.selectedItemUuid = 0
            self.selectedGId = 0
            self.tabIdx = uiConst.NPC_ASK_GIFT_TAB
            self.refreshInfo()
            return

    def askGiftLabelFunciton(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.slot.setItemSlotData(itemData)
        itemMc.slot.dragable = False
        itemMc.slot.setSlotState(uiConst.ITEM_NORMAL)
        if self.selectedItemUuid == itemData.uuid.decode('hex'):
            if self.selectedMc:
                self.selectedMc.slot.setSlotState(uiConst.ITEM_NORMAL)
            self.selectedMc = itemMc
            self.selectedMc.slot.setSlotState(uiConst.ITEM_SELECTED)
        if itemData.isLocked:
            itemMc.slot.lockMc.visible = True
            itemMc.slot.lockMc.gotoAndStop('lock')
            itemMc.removeEventListener(events.MOUSE_CLICK, self.handleItemClick)
        else:
            itemMc.slot.lockMc.visible = False
            itemMc.addEventListener(events.MOUSE_CLICK, self.handleItemClick, False, 0, True)

    def handleTabSureBtnClick(self, *args):
        if not self.widget:
            return
        if not self.selectedMc:
            return
        itemId = self.selectedItemId
        if not itemId:
            return
        p = BigWorld.player()
        itemGData = NAID.data.get(itemId, {})
        reduceVal = itemGData.get('reduceVal', 0)
        dailyFavor = p.npcFavor.npcFavorValueDaily.get(self.npcId, 0)
        dailyFavorStr = uiUtils.toHtml(str(dailyFavor), TEXT_COLOR_NORMAL if dailyFavor >= reduceVal else TEXT_COLOR_RED)
        delValue = gameStrings.NPC_INTERACTIVE_DOWN % (dailyFavorStr, reduceVal)
        leftAskCnt = itemGData.get('dailyMaxCnt', 0) - p.npcFavor.askRecordDaily.get(itemId, 0)
        if leftAskCnt == 0:
            leftAskDesc = gameStrings.NPC_ASK_CNT % (uiUtils.toHtml('0', TEXT_COLOR_RED), itemGData.get('dailyMaxCnt', 0))
        else:
            leftAskDesc = gameStrings.NPC_ASK_CNT % (uiUtils.toHtml(str(leftAskCnt), TEXT_COLOR_NORMAL), itemGData.get('dailyMaxCnt', 0))
        pfLv, _ = p.npcFavor.getPlayerRelationLvAndVal(self.npcId)
        askProb = min(NFNLD.data.get((self.npcId, pfLv), {}).get('askProb', 0) * (itemGData.get('askItemProb', 0) / 10000.0), 10000)
        askProb = askProb * dailyFavor / reduceVal if dailyFavor < reduceVal else askProb
        askRate = askProb / 10000.0 * 100.0
        if askRate < 100.0:
            textColor = TEXT_COLOR_RED
        else:
            textColor = TEXT_COLOR_NORMAL
        askRateDesc = gameStrings.NPC_ASK_SUCC_RATE % uiUtils.toHtml('%.2f%%' % askRate, textColor)
        self.multiId = self.uiAdapter.messageBox.showCounterMsgBox(leftAskDesc + '\n' + askRateDesc + '\n' + delValue, yesCallback=Functor(self.confirmTabAskCallback, self.uiAdapter.npcInteractive.getNormalNpcId(), itemId), counterData=uiUtils.getGfxItemById(itemId, count=1, appendInfo={'defaultCount': 1}), counterRange=(1, 1), title=gameStrings.NPC_ASK_GIFT_CONFIRM, counterChangeCallback=Functor(self.counterChangeCallback, uiUtils.toHtml(gameStrings.NPC_INTERACTIVE_DOWN, '#74C424'), reduceVal))

    def addValueCounterChangeCallback(self, contentStr, npcId, item, mediator, count):
        p = BigWorld.player()
        addValue = p.npcFavor.getSendUpValue(npcId, item, count)
        content = uiUtils.toHtml(contentStr % addValue, '#74C424') + '                 ' + '\n' + SCD.data.get('NPC_INTERACTIVE_UP_TIP', '')
        mediator.Invoke('setContentText', GfxValue(ui.gbk2unicode(content)))

    def counterChangeCallback(self, contentStr, value, mediator, count):
        content = contentStr % (value * count)
        mediator.Invoke('setContentText', GfxValue(ui.gbk2unicode(content)))

    def confirmTabSureCallback(self, *args):
        npcId, itemId, resKind, page, pos, cnt = args
        gamelog.info('jbx:confirmTabSureCallback', npcId, itemId, cnt, page, pos, resKind)
        p = BigWorld.player()
        item = self.getItem(resKind, page, pos)
        if not item:
            return
        if item.isNewHieroCrystal():
            name = p.getRuneData(item.id, 'name', '')
            text = gameStrings.GIVE_HIEROCRYSTAL_CONFIRM % name
            self.uiAdapter.messageBox.showYesNoMsgBox(text, Functor(BigWorld.player().base.giveItemNF, npcId, itemId, cnt, page, pos, resKind))
        else:
            BigWorld.player().base.giveItemNF(npcId, itemId, cnt, page, pos, resKind)

    def confirmTabAskCallback(self, *args):
        npcId, itemId, cnt = args
        gamelog.info('jbx:confirmTabAskCallback', args)
        BigWorld.player().base.askItemNF(npcId, itemId)

    def getLocation(self, resKind):
        if resKind == const.RES_KIND_INV:
            location = const.ITEM_IN_BAG
        elif resKind == const.RES_KIND_HIEROGRAM_BAG:
            location = const.ITEM_IN_HIEROGRAM_BAG
        else:
            location = const.ITEM_IN_METERIAL_BAG
        return location

    def labelFunction(self, *args):
        data = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        resKind, page, pos = int(data[0]), int(data[1]), int(data[2])
        item = self.getItem(resKind, page, pos)
        itemMc.posData = (resKind, page, pos)
        location = self.getLocation(resKind)
        itemData = uiUtils.getGfxItem(item, location=location)
        itemData['pos'] = (resKind, page, pos)
        itemMc.slot.setItemSlotData(itemData)
        itemMc.slot.dragable = False
        itemMc.slot.lockMc.visible = False
        itemMc.addEventListener(events.MOUSE_CLICK, self.handleItemClick, False, 0, True)
        if self.selectedItemUuid == itemData['uuid'].decode('hex'):
            if self.selectedMc:
                self.selectedMc.slot.setSlotState(uiConst.ITEM_NORMAL)
            self.selectedMc = itemMc
            self.selectedMc.slot.setSlotState(uiConst.ITEM_SELECTED)
        else:
            itemMc.slot.setSlotState(uiConst.ITEM_NORMAL)

    def handleItemClick(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.slot.data.uuid == self.selectedItemUuid:
            return
        if self.selectedMc:
            self.selectedMc.slot.setSlotState(uiConst.ITEM_NORMAL)
        self.selectedMc = e.currentTarget
        self.selectedItemUuid = e.currentTarget.slot.data.uuid.decode('hex')
        self.selectedItemId = int(e.currentTarget.slot.data.id)
        self.selectedMc.slot.setSlotState(uiConst.ITEM_SELECTED)
        if self.tabIdx == uiConst.NPC_SEND_GIFT_TAB and self.selectedMc.slot.data.pos:
            pos = self.selectedMc.slot.data['pos']
            resKind, page, pos = int(pos[0]), int(pos[1]), int(pos[2])
            item = self.getItem(resKind, page, pos)
            itemGId = commNpcFavor.getGiveItemGId(item)
            dailyMaxCnt = NGIGD.data.get(itemGId, {}).get('dailyMaxCnt', 0)
            if dailyMaxCnt:
                itemCount = dailyMaxCnt - BigWorld.player().npcFavor.todaySendItemRecord.get(itemGId, {}).get(self.npcId, 0)
                itemCount = max(0, itemCount)
                self.widget.chooseItems.leftItemCnt.text = gameStrings.NPC_ITEM_SEND_LEFT_CNT % itemCount if itemCount >= 0 else ''
            else:
                self.widget.chooseItems.leftItemCnt.text = gameStrings.NPC_ITEM_SEND_UMLIMIT_CNT
