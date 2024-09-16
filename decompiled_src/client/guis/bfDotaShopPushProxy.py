#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bfDotaShopPushProxy.o
import BigWorld
import uiConst
import copy
from item import Item
import itemToolTipUtils
from guis import uiUtils
from uiProxy import UIProxy
from guis import hotkey as HK
from guis.asObject import ASUtils
from guis.asObject import TipManager
from guis.asObject import ASObject
from guis import events
from guis import ui
from data import zaiju_data as ZD
from data import item_data as ID
from data import duel_config_data as DCD
ITEM_DISPLAY_CNT = 2
SHORTCUT_KEY_BG_WIDTH = 20
SHORTCUT_KEY_BG_POS_X = 11
TXT_DISPLAY_CNT = 3
DOTA_ITEM_MAX_LV = 3
TXT_PROP_IDX = 'txtProp'
TXT_INITIATIVESKILL = 'txtInitiativeSkill'
TXT_PSKILL = 'txtPSkill'

class BfDotaShopPushProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BfDotaShopPushProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.itemList = []
        self.resetCacheInfo()
        self.txtCache = {}
        self.preBuyItemId = 0

    def resetCacheInfo(self):
        self.lastUpperLvPushEquip = []
        self.lastRealPushEquip = []
        self.pushEquipBasicDetailCache = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BF_DOTA_SHOP_PUSH:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.reset()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BF_DOTA_SHOP_PUSH)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BF_DOTA_SHOP_PUSH)

    def initUI(self):
        self.itemList.append(self.widget.item0)
        self.itemList.append(self.widget.item1)
        for itemMC in self.itemList:
            txtMCList = []
            itemMC.pushMC.tipsInfo.txtProp.multiline = False
            itemMC.pushMC.tipsInfo.txtProp.wordWrap = False
            txtMCList.append(itemMC.pushMC.tipsInfo.txtProp)
            itemMC.pushMC.tipsInfo.txtInitiativeSkill.multiline = False
            itemMC.pushMC.tipsInfo.txtInitiativeSkill.wordWrap = False
            txtMCList.append(itemMC.pushMC.tipsInfo.txtInitiativeSkill)
            itemMC.pushMC.tipsInfo.txtPSkill.multiline = False
            itemMC.pushMC.tipsInfo.txtPSkill.wordWrap = False
            txtMCList.append(itemMC.pushMC.tipsInfo.txtPSkill)
            ASUtils.setHitTestDisable(itemMC.pushMC.eff, True)
            ASUtils.setHitTestDisable(itemMC.pushMC.shortcutKey, True)
            ASUtils.setHitTestDisable(itemMC.pushMC.tipsInfo, True)
            itemMC.pushMC.icon.addEventListener(events.MOUSE_CLICK, self.handleBuyIcon, False, 0, True)
            self.txtCache[itemMC.name] = txtMCList

        self.refreshShortcutKeyDesc()

    def handleBuyIcon(self, *args):
        icon = ASObject(args[3][0]).currentTarget
        self.buyItemBuyByIcon(icon)

    @ui.callFilter(0.5, False)
    def buyItemBuyByIcon(self, icon):
        if not icon or not icon.parent.parent.visible:
            return
        itemId = int(icon.itemId)
        p = BigWorld.player()
        consumeCash = self.uiAdapter.bfDotaShop.getRealConsumeCash(itemId)
        if p.battleFieldDotaCash < consumeCash:
            return
        p.cell.unionEquipment(itemId)

    def shortCutBuy(self, idx):
        if not self.widget:
            return
        self.buyItemBuyByIcon(self.itemList[idx].pushMC.icon)

    def refreshShortcutKeyDesc(self):
        if not self.widget:
            return
        for i in xrange(ITEM_DISPLAY_CNT):
            itemMC = self.itemList[i]
            itemMC.pushMC.shortcutKey.txtKey.text = HK.HKM[HK.KEY_DOTA_BUY_ITEM_SHORTCUT0 + i].getDesc()
            width = itemMC.pushMC.shortcutKey.txtKey.textWidth + 5
            itemMC.pushMC.shortcutKey.bg.width = width

    def isNeedPushEquip(self):
        p = BigWorld.player()
        maxLvEquipCnt = 0
        for item in p.battleFieldBag.values():
            if item != None and ID.data.get(item.id, {}).get('dotaEquipLv', 0) == DOTA_ITEM_MAX_LV:
                maxLvEquipCnt += 1

        return maxLvEquipCnt < uiConst.BF_DOTA_BAG_ITEM_CNT

    def isBagFull(self):
        lvEquipCnt = 0
        p = BigWorld.player()
        for item in p.battleFieldBag.values():
            if item != None:
                lvEquipCnt += 1

        return lvEquipCnt == uiConst.BF_DOTA_BAG_ITEM_CNT

    def refreshInfo(self):
        if not self.widget:
            return
        equipList = self.getPushEquipmentInfo()
        changed = equipList != self.lastRealPushEquip
        for i in xrange(ITEM_DISPLAY_CNT):
            if i < len(equipList) and equipList[i][0] and equipList[i][1]:
                self.itemList[i].visible = True
                detailInfo = self.getPushEquipDetailInfo(equipList[i][0], i)
                self.refreshItem(detailInfo, self.itemList[i])
                if changed:
                    self.addTweener(self.itemList[i].pushMC.tipsInfo, i)
            else:
                self.itemList[i].visible = False

        self.lastRealPushEquip = equipList

    def addTweener(self, itemMC, index):
        itemMC.alpha = 1.0
        fadeTime = DCD.data.get('dotaEquipFadeTime', 10)
        tweenData = {'time': fadeTime,
         'alpha': 0,
         'onCompleteParams': (index,),
         'transition': 'easeInElastic'}
        ASUtils.addTweener(itemMC, tweenData)

    def refreshItem(self, detailInfo, itemMc):
        itemMc.pushMC.icon.itemId = detailInfo['itemId']
        itemMc.pushMC.icon.quality.gotoAndStop(uiUtils.getItemQualityColor(detailInfo['itemId']))
        itemMc.pushMC.icon.icon.fitSize = True
        itemMc.pushMC.icon.icon.loadImage(detailInfo['iconPath'])
        itemMc.pushMC.eff.visible = detailInfo['enough']
        itemMc.pushMC.tipsInfo.equipName.htmlText = detailInfo['itemName']
        txtDescList = detailInfo['txtDescList']
        txtMCList = self.txtCache[itemMc.name]
        for i in range(TXT_DISPLAY_CNT):
            if i < len(txtDescList):
                txtMCList[i].visible = True
                txtMCList[i].htmlText = txtDescList[i]
                ASUtils.truncateString(txtMCList[i])
            else:
                txtMCList[i].visible = False

        itemMc.pushMC.txtCash.text = str(detailInfo['cash'])
        uiUtils.addItemTipById(itemMc.pushMC.icon, detailInfo['itemId'])

    def getPushEquipmentInfo(self):
        if not self.isNeedPushEquip():
            return []
        if self.preBuyItemId:
            return self.getPrebuyPushEquipInfo()
        isBagFull = self.isBagFull()
        pushEquipmentInfo = self.getUpperLvPushEquipmentInfo()
        realPushEquipmentInfo = []
        for index, equipInfo in enumerate(pushEquipmentInfo):
            if not equipInfo[1] and not isBagFull:
                fittest = self.getFittestUnionPartEquip(equipInfo[0], realPushEquipmentInfo)
                if fittest:
                    realPushEquipmentInfo.append(fittest)
                else:
                    realPushEquipmentInfo.append(equipInfo)
            elif isBagFull and not self.isHadChildItem(equipInfo[0]):
                continue
            else:
                realPushEquipmentInfo.append(equipInfo)

        return realPushEquipmentInfo

    def isHadChildItem(self, itemId):
        childItemList = self.uiAdapter.bfDotaShop.getChildItemList(itemId)[1:]
        for itemInfo in childItemList:
            if self.uiAdapter.bfDotaShop.hadItem(itemInfo['itemId']):
                return True

        return False

    def isRepeated(self, itemId, pushEquipmentInfo):
        for pushItemId, cashEnough in pushEquipmentInfo:
            if pushItemId == itemId:
                return True

        return False

    def getFittestUnionPartEquip(self, itemId, pushEquipmentInfo):
        p = BigWorld.player()
        childItemList = self.uiAdapter.bfDotaShop.getChildItemList(itemId, self.uiAdapter.bfDotaShop.getItemCntDic())[1:]
        canBuyItemList = []
        ownCash = p.battleFieldDotaCash
        itemCntDic = self.uiAdapter.bfDotaShop.getItemCntDic()
        for itemInfo in childItemList:
            info = {}
            itemId = itemInfo['itemId']
            info['itemId'] = itemId
            subValue = ownCash - self.uiAdapter.bfDotaShop.getRealConsumeCash(itemId)
            if subValue >= 0:
                if itemCntDic.get(itemId, 0):
                    itemCntDic[itemId] = itemCntDic[itemId] - 1
                    continue
                else:
                    canBuyItemList.append((itemId, subValue))

        if canBuyItemList:
            canBuyItemList.sort(cmp=lambda x, y: cmp(x[1], y[1]))
            for itemId, subValue in canBuyItemList:
                if not self.isRepeated(itemId, pushEquipmentInfo):
                    return (itemId, True)

            if not self.isRepeated(canBuyItemList[0][0], pushEquipmentInfo):
                return (canBuyItemList[0][0], True)

    def getPrebuyPushEquipInfo(self):
        p = BigWorld.player()
        equipmentInfo = []
        ownCash = p.battleFieldDotaCash
        itemCntDic = self.uiAdapter.bfDotaShop.getItemCntDic()
        isBagFull = self.isBagFull()
        if isBagFull:
            if self.isHadChildItem(self.preBuyItemId):
                parentList = []
                for itemInfo in self.uiAdapter.bfDotaShop.getChildItemList(self.preBuyItemId, itemCntDic):
                    itemId = itemInfo['itemId']
                    realConsumeCash = self.uiAdapter.bfDotaShop.getRealConsumeCash(itemId)
                    if not self.isHadChildItem(itemId) or ownCash < realConsumeCash:
                        continue
                    parentList.append((itemId, realConsumeCash))

                parentList.sort(cmp=lambda x, y: cmp(x[1], y[1]), reverse=True)
                if parentList:
                    equipmentInfo.append((parentList[0][0], True))
            return equipmentInfo
        for itemInfo in self.uiAdapter.bfDotaShop.getChildItemList(self.preBuyItemId, itemCntDic):
            hadSameItem = False
            itemId = itemInfo['itemId']
            for info in equipmentInfo:
                if info[0] == itemId:
                    hadSameItem = True
                    break

            if hadSameItem:
                continue
            consumeCash = self.uiAdapter.bfDotaShop.getRealConsumeCash(itemId)
            if ownCash >= consumeCash:
                equipmentInfo.append([itemId, True, consumeCash])
                if itemId == self.preBuyItemId:
                    break

        equipmentInfo.sort(cmp=lambda x, y: cmp(x[2], y[2]), reverse=True)
        return equipmentInfo

    def getUpperLvPushEquipmentInfo(self):
        p = BigWorld.player()
        equipmentInfo = []
        if not self.lastUpperLvPushEquip:
            needUpdate = True
        else:
            needUpdate = False
            for index, info in enumerate(self.lastUpperLvPushEquip):
                info[1] = p.battleFieldDotaCash >= self.uiAdapter.bfDotaShop.getRealConsumeCash(info[0])
                if self.uiAdapter.bfDotaShop.hadItem(info[0]):
                    needUpdate = True
                    break

        if not needUpdate:
            equipmentInfo = self.lastUpperLvPushEquip
        equipmentInfo = [ info for info in equipmentInfo if not self.hadGroupItem(info[0]) ]
        p = BigWorld.player()
        cash = p.battleFieldDotaCash
        recommend_equips = self.uiAdapter.bfDotaShop.getRecommEquip()[-1]
        for itemId in recommend_equips:
            if not itemId:
                continue
            if len(equipmentInfo) == 2:
                break
            if self.uiAdapter.bfDotaShop.hadItem(itemId) or self.isRepeated(itemId, equipmentInfo) or self.hadGroupItem(itemId):
                continue
            equipmentInfo.append([itemId, cash >= self.uiAdapter.bfDotaShop.getRealConsumeCash(itemId)])

        self.lastUpperLvPushEquip = equipmentInfo
        return equipmentInfo

    def hadGroupItem(self, itemId):
        p = BigWorld.player()
        groupId = ID.data.get(itemId, {}).get('dotaEquipGroup', 0)
        if groupId:
            for _, item in p.battleFieldBag.iteritems():
                if item:
                    if ID.data.get(item.id, {}).get('dotaEquipGroup', 0) == groupId:
                        return True

        return False

    def getPushEquipDetailInfo(self, itemId, pushIndex):
        p = BigWorld.player()
        if itemId in self.pushEquipBasicDetailCache:
            basicDetailInfo = self.pushEquipBasicDetailCache[itemId]
        else:
            basicDetailInfo = {}
            p = BigWorld.player()
            basicDetailInfo['itemId'] = itemId
            basicDetailInfo['iconPath'] = uiUtils.getItemIconPath(itemId)
            basicDetailInfo['itemName'] = uiUtils.getItemColorName(itemId)
            item = Item(itemId)
            tipsData = itemToolTipUtils.formatRet(p, item)
            txtDescList = []
            propDes = ''
            for propInfo in tipsData['propList']:
                if propDes:
                    propDes += ' %s%s' % (propInfo['pName'], propInfo['pValue'])
                else:
                    propDes += '%s%s' % (propInfo['pName'], propInfo['pValue'])

            if propDes:
                txtDescList.append(propDes)
            if tipsData['initiativeSkillDesc']:
                txtDescList.append(tipsData['initiativeSkillDesc'])
            if tipsData['pskillDesc']:
                txtDescList.append(tipsData['pskillDesc'])
            basicDetailInfo['txtDescList'] = txtDescList
            self.pushEquipBasicDetailCache[itemId] = basicDetailInfo
        detailInfo = copy.deepcopy(basicDetailInfo)
        detailInfo['cash'] = self.uiAdapter.bfDotaShop.getRealConsumeCash(itemId)
        detailInfo['enough'] = p.battleFieldDotaCash >= detailInfo['cash']
        return detailInfo
