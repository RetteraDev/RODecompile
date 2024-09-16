#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/myClothProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
from helpers import cellCmd
from uiProxy import UIProxy
import clientcom
import const
import commcalc
import gamelog
import gametypes
import ui
import equipment
import itemToolTipUtils
from item import Item
from guis import uiUtils
from guis import wardrobeHelper
from helpers import charRes
from guis.asObject import ASObject
from guis.asObject import TipManager
from guis import tipUtils
from helpers import aspectHelper
from guis import events
from gamestrings import gameStrings
from cdata import game_msg_def_data as GMDD
from data import gui_bao_ge_config_data as GBGCD
from data import wardrobe_recommend_data as WRD
from guis.messageBoxProxy import MBButton
from callbackHelper import Functor
RECOMM_SCHEME_DEMO = {(5, 2, 1): {'suitName': 'recommendScheme',
             'suitItems': (205219,)},
 (5, 2, 2): {'suitName': 'recommendScheme2',
             'suitItems': (205219,)}}
RECOMM_SCHEME_NUM = 3
SHOW_SLOTS = set(gametypes.EQU_PART_WEAPON_FASHION).union(set(gametypes.EQU_PART_FASHION))
BG_FRAME_MAP = {gametypes.EQU_PART_FASHION_HEAD: 'head',
 gametypes.EQU_PART_FASHION_BODY: 'body',
 gametypes.EQU_PART_FASHION_SHOE: 'jiao',
 gametypes.EQU_PART_FASHION_HAND: 'hand',
 gametypes.EQU_PART_FASHION_LEG: 'tui',
 gametypes.EQU_PART_HEADWEAR: 'touShi',
 gametypes.EQU_PART_HEADWEAR_RIGHT: 'faShi',
 gametypes.EQU_PART_HEADWEAR_LFET: 'faShi',
 gametypes.EQU_PART_FACEWEAR: 'lianShi',
 gametypes.EQU_PART_WAISTWEAR: 'yao',
 gametypes.EQU_PART_BACKWEAR: 'bei',
 gametypes.EQU_PART_TAILWEAR: 'wei',
 gametypes.EQU_PART_CHESTWEAR: 'xiong',
 gametypes.EQU_PART_EARWEAR: 'erShi',
 gametypes.EQU_PART_FASHION_NEIYI: 'neiyi',
 gametypes.EQU_PART_FASHION_NEIKU: 'neiku',
 gametypes.EQU_PART_FOOT_DUST: 'footdust',
 gametypes.EQU_PART_YUANLING: 'xuanshi',
 gametypes.EQU_PART_FASHION_CAPE: 'pifeng',
 gametypes.EQU_PART_FASHION_WEAPON_ZHUSHOU: 'zhushou',
 gametypes.EQU_PART_FASHION_WEAPON_FUSHOU: 'fushou'}

class MyClothProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MyClothProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.type = 'myCloth'
        self.currentScheme = 0
        self.tempNameInputLock = False
        self.currentInput = None
        self.currentSchemeName = ''
        uiAdapter.registerEscFunc(uiConst.WIDGET_MY_CLOTH, self.hideAll)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MY_CLOTH:
            self.widget = widget
            self.addEvent(events.EVENT_MY_CLOTH_CHANGED, self.refreshInfo)
            self.initUI()
            self.refreshInfo()
            self.queryServerInfo()

    def queryServerInfo(self):
        BigWorld.player().base.queryWardrobeCustomScheme()

    def clearWidget(self):
        self.widget = None
        self.currentScheme = 0
        self.currentInput = None
        self.currentSchemeName = ''
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MY_CLOTH)
        aspectHelper.getInstance().resetAll()
        wardrobeHelper.getInstance().resetCamera()

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_MY_CLOTH)
        else:
            self.refreshInfo()

    def hideAll(self):
        wardrobeHelper.getInstance().close()

    def initUI(self):
        self.setSchemeWndVisible(False)
        self.initBg()
        self.initSlotBinding()
        self.widget.schemesMc.closeBtn.addEventListener(events.BUTTON_CLICK, self.onCloseSchemeBtnClick, False, 0, True)
        self.widget.swithBtn.addEventListener(events.BUTTON_CLICK, self.onSwitchBtnClick, False, 0, True)
        self.widget.closeBtn.addEventListener(events.BUTTON_CLICK, self.onCloseBtnClick, False, 0, True)
        self.widget.saveBtn.addEventListener(events.BUTTON_CLICK, self.onSaveBtnClick, False, 0, True)
        TipManager.addTip(self.widget.saveBtn, gameStrings.WARDROBE_SAVE_TIP)
        self.setRecommendSchemeInfo()
        wardrobeHelper.getInstance().addWardrobeBg()

    def initSlotBinding(self):
        for part in SHOW_SLOTS:
            slotMc = self.widget.getChildByName('slot%s' % str(part))
            if slotMc:
                slotMc.slot.binding = 'myCloth.0.%s' % str(part)

    def onCloseBtnClick(self, *args):
        self.hideAll()

    def initBg(self):
        for part in SHOW_SLOTS:
            slotMc = self.widget.getChildByName('slot%s' % str(part))
            if slotMc:
                goFrame = BG_FRAME_MAP.get(part, '')
                if goFrame:
                    slotMc.bg.gotoAndStop(goFrame)
                    slotMc.lock.visible = False
                else:
                    slotMc.lock.visible = True

    def refreshInfo(self):
        if not self.widget:
            return
        else:
            fashions = aspectHelper.getInstance().getFashionInfo()
            for part in SHOW_SLOTS:
                slotMc = self.widget.getChildByName('slot%s' % str(part))
                if slotMc:
                    slotMc.part = part
                    slotMc.suit.visible = False
                    slotMc.addEventListener(events.MOUSE_CLICK, self.handleSlotClick, False, 0, True)
                    if fashions.get(part, {}):
                        fashionInfo = fashions.get(part, {})
                        slotMc.tryMc.visible = fashionInfo.get('isTrial', False)
                        slotMc.slot.setItemSlotData(fashionInfo)
                    else:
                        slotMc.tryMc.visible = False
                        slotMc.slot.setItemSlotData(None)

            self.setFashionSuit(fashions)
            self.refreshSchemeInfo()
            return

    def setFashionSuit(self, fashionInfos):
        for part in fashionInfos:
            fashionInfo = fashionInfos.get(part, {})
            itemId = fashionInfo.get('itemId', 0)
            if itemId:
                aspectParts = [part]
                aspectParts.extend(uiUtils.getAspectParts(itemId))
                if len(aspectParts) > 1:
                    for aspectPart in aspectParts:
                        aspectSlotMc = self.widget.getChildByName('slot%s' % str(aspectPart))
                        if aspectSlotMc:
                            aspectSlotMc.suit.visible = True

    def getItemTipInfoByPart(self, part):
        p = BigWorld.player()
        item = aspectHelper.getInstance().trialEquipment[part] if aspectHelper.getInstance().trialEquipment.has_key(part) else None
        if item:
            return tipUtils.getItemTipById(item.id)
        else:
            item = p.equipment[part]
            if item:
                return tipUtils.getItemTipByLocation(item, const.ITEM_IN_EQUIPMENT)
            return

    def refreshSchemeInfo(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            if p.wardrobeBag.schemeInfo == None or not gameglobal.rds.configData.get('enableWardrobeScheme', False):
                self.widget.schemeName.visible = False
                self.widget.swithBtn.visible = False
                self.widget.saveBtn.visible = False
                self.widget.schemesMc.visible = False
            else:
                self.widget.schemeName.text = self.currentSchemeName
                self.widget.schemeName.visible = True
                self.widget.swithBtn.visible = True
                self.widget.saveBtn.visible = True
                if self.currentScheme:
                    self.currentSchemeName = self.getSchemeName(self.currentScheme)
                    self.widget.schemeName.text = self.currentSchemeName
            self.setSchemeWndVisible(self.widget.schemesMc.visible)
            return

    def getAvaliableSchemeIdx(self):
        schemeInfo = BigWorld.player().wardrobeBag.schemeInfo
        if schemeInfo == None:
            return 0
        else:
            for i in xrange(gametypes.WARDROBE_CUSTOM_SCHEME_CNT):
                schemeData = schemeInfo.get(i + 1, {})
                if schemeData:
                    isEmpty = True
                    for part in SHOW_SLOTS:
                        if schemeData.get(part, None):
                            isEmpty = False
                            break

                    if isEmpty:
                        return i + 1
                else:
                    return i + 1

            return 0

    def getSchemeName(self, schemeIdx):
        schemeInfo = BigWorld.player().wardrobeBag.schemeInfo
        if schemeInfo != None:
            schemeData = schemeInfo.get(schemeIdx, {})
            if not schemeData:
                return gameStrings.WARDROBE_SCHEME_DEFAULT_NAME % str(schemeIdx)
            else:
                return schemeData.get('schemeName', '')

    def onSwitchBtnClick(self, *args):
        self.setSchemeWndVisible(not self.widget.schemesMc.visible)

    def onCloseSchemeBtnClick(self, *args):
        self.setSchemeWndVisible(False)

    def setSchemeWndVisible(self, visible):
        if visible:
            schemeInfo = BigWorld.player().wardrobeBag.schemeInfo
            if schemeInfo == None:
                return
            self.currentInput = None
            for i in xrange(gametypes.WARDROBE_CUSTOM_SCHEME_CNT):
                schemeItemMc = self.widget.schemesMc.getChildByName('myScheme%d' % i)
                if schemeItemMc:
                    schemeItemMc.selectMc.addEventListener(events.MOUSE_CLICK, self.handleClickChangeName, False, 0, True)
                    schemeItemMc.nameInput.visible = False
                    schemeItemMc.NameBtn.idx = i + 1
                    schemeItemMc.idx = i + 1
                    schemeItemMc.NameBtn.label = self.getSchemeName(i + 1)
                    schemeItemMc.NameBtn.selected = self.currentScheme == i + 1
                    schemeItemMc.NameBtn.addEventListener(events.BUTTON_CLICK, self.onChooseScheme, False, 0, True)

        self.widget.schemesMc.visible = visible

    def setRecommendSchemeInfo(self):
        recomSchemInfo = WRD.data
        schemesData = []
        p = BigWorld.player()
        for key in recomSchemInfo:
            if key[0] != p.physique.bodyType:
                continue
            if key[1] != p.physique.sex:
                continue
            suitInfo = recomSchemInfo.get(key)
            suitInfo['key'] = key
            schemesData.append(suitInfo)

        for i in xrange(RECOMM_SCHEME_NUM):
            recomSchemMc = self.widget.schemesMc.getChildByName('scheme%d' % i)
            if recomSchemMc:
                if len(schemesData) > i:
                    schemeData = schemesData[i]
                    recomSchemMc.visible = True
                    recomSchemMc.label = schemeData.get('suitName', '')
                    recomSchemMc.schemeInfo = schemeData
                    recomSchemMc.addEventListener(events.BUTTON_CLICK, self.onRecomSchemeClick, False, 0, True)
                else:
                    recomSchemMc.visible = False

    def convertNumKeyDict(self, dict):
        newDict = {}
        for key in dict:
            newDict[str(key)] = dict[key]

        return newDict

    def onRecomSchemeClick(self, *args):
        e = ASObject(args[3][0])
        schemeData = e.currentTarget.schemeInfo
        schemeItems = schemeData.get('suitItems', ())
        wearSuits = {}
        trialSuits = {}
        for itemId in schemeItems:
            item = Item(itemId)
            wearParts = list(item.whereEquip())
            part = wearParts[0]
            ownItem = gameglobal.rds.ui.wardrobe.getOwnClothInfo(itemId)
            if not part:
                return
            if ownItem:
                wearSuits[part] = ownItem.uuid
            else:
                trialItem = Item(itemId)
                trialSuits[part] = trialItem

        aspectHelper.getInstance().unwearAllAndEquipMultiEquips(wearSuits, identifyStr=schemeData.get('suitName', ''), trialInfoDicts=trialSuits)

    def handleClickChangeName(self, *args):
        e = ASObject(args[3][0])
        schemeItemMc = e.currentTarget.parent
        if self.currentInput:
            if self.currentInput == schemeItemMc.nameInput:
                self.inputFocusOut(schemeItemMc)
            else:
                self.inputFocusOutWithoutSave(self.currentInput.parent)
        else:
            self.inputFocusIn(schemeItemMc)
            self.currentInput = schemeItemMc.nameInput
            schemeItemMc.nameInput.visible = True
            schemeItemMc.nameInput.addEventListener(events.MOUSE_CLICK, self.handleInputClick, False, 0, True)
            schemeItemMc.nameInput.addEventListener(events.KEYBOARD_EVENT_KEY_UP, self.handelInputKeyBoard, False, 0, True)
            self.widget.stage.addEventListener(events.MOUSE_CLICK, self.handleInputFocusOut, False, 0, True)
            schemeItemMc.nameInput.focused = True
        e.stopImmediatePropagation()

    def handelInputKeyBoard(self, *args):
        e = ASObject(args[3][0])
        schemeItemMc = e.currentTarget.parent
        if e.keyCode == events.KEYBOARD_CODE_ENTER or e.keyCode == events.KEYBOARD_CODE_NUMPAD_ENTER:
            self.inputFocusOut(schemeItemMc)

    def handleInputFocusIn(self, *args):
        e = ASObject(args[3][0])
        schemeItemMc = e.currentTarget.parent.parent
        self.inputFocusIn(schemeItemMc)

    def inputFocusIn(self, schemeItemMc):
        self.currentInput = schemeItemMc.nameInput
        oldName = schemeItemMc.NameBtn.label
        schemeItemMc.NameBtn.label = ''
        schemeItemMc.nameInput.text = oldName
        schemeItemMc.nameInput.maxChars = gametypes.WARDROBE_CUSTOM_SCHEME_NAME_LEN_MAX
        schemeItemMc.nameInput.visible = True

    def handleInputClick(self, *args):
        e = ASObject(args[3][0])
        e.stopImmediatePropagation()

    def handleInputFocusOut(self, *args):
        if not self.widget:
            return
        self.widget.stage.removeEventListener(events.MOUSE_CLICK, self.handleInputFocusOut)
        if self.currentInput:
            schemeItemMc = self.currentInput.parent
            self.inputFocusOut(schemeItemMc)

    def inputFocusOut(self, schemeItemMc):
        self.currentInput = None
        newName = schemeItemMc.nameInput.text
        schemeIdx = int(schemeItemMc.idx)
        schemeItemMc.NameBtn.label = self.getSchemeName(schemeIdx)
        schemeItemMc.nameInput.visible = False
        self.changeSchemeName(newName, schemeIdx)

    def inputFocusOutWithoutSave(self, schemeItemMc):
        self.currentInput = None
        newName = schemeItemMc.nameInput.text
        schemeIdx = int(schemeItemMc.idx)
        schemeItemMc.NameBtn.label = self.getSchemeName(schemeIdx)
        schemeItemMc.nameInput.visible = False

    def changeSchemeName(self, schemeName, schemeIdx):
        p = BigWorld.player()
        schemeData = p.wardrobeBag.schemeInfo.get(schemeIdx, {})
        saveParts = []
        saveUUIDs = []
        for part in SHOW_SLOTS:
            if part in schemeData:
                saveParts.append(part)
                saveUUIDs.append(schemeData[part])

        gamelog.debug('dxk@myClothProxy requireSetWardrobeCustomScheme', schemeIdx, schemeName, saveParts, saveUUIDs)
        p.base.requireSetWardrobeCustomScheme(schemeIdx, schemeName, saveParts, saveUUIDs)

    @ui.callFilter(0.5)
    def onChooseScheme(self, *args):
        e = ASObject(args[3][0])
        schemeIdx = e.currentTarget.idx
        schemesInfo = BigWorld.player().wardrobeBag.schemeInfo
        if schemesInfo == None:
            return
        else:
            self.swithToScheme(schemeIdx)
            return

    def showSaveSchemeMsgBox(self, schemeIdx):
        buttonOk = MBButton(gameStrings.TEXT_MYCLOTHPROXY_425, Functor(self.saveScheme, schemeIdx))
        buttonCancel = MBButton(gameStrings.TEXT_MYCLOTHPROXY_426, Functor(self.swithToScheme, schemeIdx))
        text = gameStrings.WARDROBE_SCHEME_CONFIRM_TEXT
        self.safeModeBoxId = gameglobal.rds.ui.messageBox.show(True, '', text, [buttonOk, buttonCancel])

    def swithToScheme(self, schemeIdx):
        schemesInfo = BigWorld.player().wardrobeBag.schemeInfo
        schemeData = schemesInfo.get(schemeIdx, {})
        if not schemeData:
            aspectHelper.getInstance().unwearAllAndEquipMultiEquips({}, identifyStr=str(schemeIdx), trialInfoDicts={}, callBack=self.onChooseSchemeSucess)
        else:
            wearInfoDict = {}
            for key in schemeData:
                if key in SHOW_SLOTS:
                    wearInfoDict[key] = schemeData[key]

            aspectHelper.getInstance().unwearAllAndEquipMultiEquips(wearInfoDict, identifyStr=str(schemeIdx), trialInfoDicts={}, callBack=self.onChooseSchemeSucess)

    def onChooseSchemeSucess(self, schemeStr):
        schemeIdx = int(schemeStr)
        self.currentScheme = schemeIdx
        self.refreshSchemeInfo()

    def onSaveBtnClick(self, *args):
        if self.currentScheme:
            self.saveScheme(self.currentScheme)
        else:
            avaliableScheme = self.getAvaliableSchemeIdx()
            self.saveScheme(avaliableScheme)

    @ui.callFilter(1.2)
    def saveScheme(self, schemeIdx):
        p = BigWorld.player()
        fashions = aspectHelper.getInstance().getFashionInfo()
        currentSchemeName = self.getSchemeName(schemeIdx)
        if not schemeIdx:
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.WARDROBE_SCHEME_SAVE_NOT_SELECTED)
            return
        for part in fashions:
            fashionInfo = fashions.get(part, {})
            if fashionInfo:
                if fashionInfo.get('isTrial', False):
                    gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.WARDROBE_SCHEME_SAVE_HAVE_TRIAL)
                    return

        saveParts, saveUUIDs = self.getWearPartsAndUUIDs()
        gamelog.debug('dxk@myClothProxy requireSetWardrobeCustomScheme', schemeIdx, currentSchemeName, saveParts, saveUUIDs)
        p.base.requireSetWardrobeCustomScheme(schemeIdx, currentSchemeName, saveParts, saveUUIDs)
        self.currentScheme = schemeIdx

    def getWearPartsAndUUIDs(self):
        p = BigWorld.player()
        equips = p.equipment
        saveParts = []
        saveUUIDs = []
        for part in SHOW_SLOTS:
            wearEquip = equips[part]
            if not wearEquip or not wearEquip.isStorageByWardrobe():
                continue
            if wearEquip:
                saveParts.append(part)
                saveUUIDs.append(wearEquip.uuid)

        return (saveParts, saveUUIDs)

    def sendFashionSet(self, part):
        fashions = aspectHelper.getInstance().getFashionInfo()
        fashionInfo = fashions.get(part, {})
        if fashionInfo:
            if fashionInfo.get('isTrial', False):
                return
        p = BigWorld.player()
        if part >= const.SUB_EQUIP_PART_OFFSET:
            equIt = commcalc.getAlternativeEquip(p, part - const.SUB_EQUIP_PART_OFFSET)
            isSubEquip = True
            realPos = gametypes.equipTosubEquipPartMap.get(part - const.SUB_EQUIP_PART_OFFSET, -1)
            if realPos < 0:
                return
        else:
            equIt = p.equipment.get(part)
            isSubEquip = False
            realPos = part
        if equIt == const.CONT_EMPTY_VAL:
            return
        if isSubEquip:
            p.constructItemInfo(const.RES_KIND_SUB_EQUIP_BAG, const.DEFAULT_SUB_EQU_PAGE_NO, realPos)
        else:
            p.constructItemInfo(const.RES_KIND_EQUIP, 0, realPos)

    def handleSlot(self, part, buttonIdx, shiftKey):
        p = BigWorld.player()
        hideDyeList = True
        if buttonIdx == uiConst.LEFT_BUTTON:
            if shiftKey:
                self.sendFashionSet(part)
            elif part:
                fashions = aspectHelper.getInstance().getFashionInfo()
                fashionInfo = fashions.get(part, {})
                if fashionInfo:
                    if not fashionInfo.get('isTrial', False):
                        gameglobal.rds.ui.dyeList.show(part, p.equipment[part])
                        hideDyeList = False
                        gameglobal.rds.ui.wardrobe.scrollToItem(p.equipment[part].id, p.equipment[part].uuid)
                    else:
                        gameglobal.rds.ui.wardrobe.scrollToItem(fashionInfo.get('itemId', 0))
        elif buttonIdx == uiConst.RIGHT_BUTTON:
            if part:
                fashions = aspectHelper.getInstance().getFashionInfo()
                fashionInfo = fashions.get(part, {})
                if fashionInfo:
                    if fashionInfo.get('isTrial', False):
                        aspectHelper.getInstance().unTrailEquip(part)
                    else:
                        p = BigWorld.player()
                        if fashionInfo.get('isWardrobeItem', False):
                            p.cell.exchangeWardrobeEquip([''], [part], False, '')
                        else:
                            page, pos = p.inv.searchEmptyInPages()
                            if pos != const.CONT_NO_POS:
                                cellCmd.exchangeInvEqu(page, pos, part)
                            else:
                                p.showGameMsg(GMDD.data.SHOP_BAG_FULL, ())
        if hideDyeList:
            gameglobal.rds.ui.dyeList.hide()

    def handleSlotClick(self, *args):
        e = ASObject(args[3][0])
        part = e.currentTarget.part
        buttonIdx = e.buttonIdx
        shiftKey = e.shiftKey
        self.handleSlot(part, buttonIdx, shiftKey)
