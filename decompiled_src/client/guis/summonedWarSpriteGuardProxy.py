#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteGuardProxy.o
import BigWorld
import events
import gameglobal
import const
import utils
import math
import commcalc
import formula
from collections import Iterable
from uiProxy import UIProxy
from asObject import ASObject
from guis import uiUtils
from guis import uiConst
from guis import tipUtils
from guis.asObject import ASUtils
from guis.asObject import MenuManager
from guis.asObject import TipManager
from gameStrings import gameStrings
from data import sys_config_data as SCD
from data import prop_ref_data as PRD
from data import summon_sprite_info_data as SSID
from data import summon_sprite_accessory_template_data as SSATD
from data import prop_ref_data as PRD
from cdata import summon_sprite_accessory_data as SSAD
from cdata import pskill_data as PD
from cdata import prop_def_data as PDD
from cdata import pskill_template_data as PTD
SPRITE_ICON_PATH = 'summonedSprite/icon/%s.dds'
SLOT_TYPE_NUM = 3
TYPE_NUM_TO_SHOW_SLOT_POS = {1: [1],
 2: [0, 2],
 3: [0, 1, 2]}
ACCESSORY_SPRITE_PROPIDS = frozenset([PDD.data.PROPERTY_MHP,
 PDD.data.PROPERTY_PHY_ATK_ADD,
 PDD.data.PROPERTY_MAG_ATK_ADD,
 PDD.data.PROPERTY_EQUIP_PHY_DEF,
 PDD.data.PROPERTY_PHY_DEF_ADD,
 PDD.data.PROPERTY_EQUIP_MAG_DEF,
 PDD.data.PROPERTY_MGI_DEF_ADD])

class SummonedWarSpriteGuardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteGuardProxy, self).__init__(uiAdapter)
        self.widget = None
        self.typeToSort = []
        self.currSelectItem = None
        self.currSelectItemSpriteIndex = None
        self.clickGuardSpriteIndex = None
        self.clickAccessoryPart = None
        self.currSelectSpriteNumber = 0
        self.spriteGuardTipPanel = None
        self.guardMainInfoOpening = False

    def reset(self):
        self.typeToSort = []
        self.currSelectItem = None
        self.clickGuardSpriteIndex = None
        self.clickAccessoryPart = None
        self.currSelectItemSpriteIndex = None
        self.currSelectSpriteNumber = 0
        self.spriteGuardTipPanel = None

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def initUI(self):
        changeBtn = self.widget.warSpriteGuardPanel.guardRightMc.changeBtn
        changeBtn.disabled = True
        TipManager.addTip(changeBtn, gameStrings.SUMMONED_WAR_SPRITE_COMING_SOON)
        changeBtn.addEventListener(events.BUTTON_CLICK, self.handleChangeBtnClick, False, 0, True)
        guardCenterHintMc = self.widget.warSpriteGuardPanel.guardRightMc.guardCenterHint
        guardCenterHint = SCD.data.get('spriteGuardCenterBottomHint', None)
        if guardCenterHint:
            TipManager.addTip(guardCenterHintMc, guardCenterHint)
        self.currSelectSpriteNumber = gameglobal.rds.ui.summonedWarSprite.recordSpriteNumber
        self.currSelectItemSpriteIndex = gameglobal.rds.ui.summonedWarSprite.recordSpriteIndex

    def handleChangeBtnClick(self, *args):
        if not gameglobal.rds.ui.summonedWarSpriteGuardStruct.widget:
            gameglobal.rds.ui.summonedWarSpriteGuardStruct.show()

    def handleSpriteItemBtnClick(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if not itemMc.enabled:
            return
        if self.currSelectItemSpriteIndex and self.currSelectItemSpriteIndex == itemMc.warSpriteIndex:
            return
        if self.currSelectItem:
            self.currSelectItem.selected = False
        itemMc.selected = True
        self.currSelectItem = itemMc
        self.currSelectSpriteNumber = itemMc.numberId
        self.currSelectItemSpriteIndex = itemMc.warSpriteIndex
        gameglobal.rds.ui.summonedWarSprite.saveSpriteIndex(itemMc.numberId, itemMc.warSpriteIndex)

    def handleStateChange(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        target.spriteName.text = target.szName
        target.spriteLv.text = target.szLv

    def handleSelectWarSpriteType(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if itemMc.selectedIndex != -1:
            self.updateWarSpritesTypeList(itemMc.selectedIndex, scrollTo=True)

    def handleGuardBtnClick(self, *args):
        e = ASObject(args[3][0])
        guardSlot = e.currentTarget.parent
        if guardSlot.accessoryPart and self.currSelectItemSpriteIndex:
            p = BigWorld.player()
            p.base.equipSummonedSpriteAccessory(self.currSelectItemSpriteIndex, guardSlot.accessoryPart)

    def handleReplaceBtnClick(self, *args):
        e = ASObject(args[3][0])
        if self.clickGuardSpriteIndex == self.currSelectItemSpriteIndex:
            return
        p = BigWorld.player()
        p.base.replaceEquipSummonedSpriteAccessory(self.clickGuardSpriteIndex, self.currSelectItemSpriteIndex, self.clickAccessoryPart)
        MenuManager.getInstance().hideMenu()

    def handleLeaveBtnClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        clickAccessoryPart = target.parent.accessoryPart
        p = BigWorld.player()
        p.base.unEquipSummonedSpriteAccessory(clickAccessoryPart)
        MenuManager.getInstance().hideMenu()

    def handleOpenGuardMainInfo(self, *args):
        self.guardMainInfoOpening = not self.guardMainInfoOpening
        self.updateGuardMainInfo()

    def handleSlotClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        self.clickGuardSpriteIndex = target.parent.spriteIndex
        self.clickAccessoryPart = target.parent.accessoryPart
        self.showSpriteGuardTipMc(target)

    def showSpriteGuardTipMc(self, target):
        if not self.clickGuardSpriteIndex:
            return
        self.spriteGuardTipPanel = self.widget.getInstByClsName('SummonedWarSpriteGuard_spriteGuardTip')
        spriteItem = self.spriteGuardTipPanel.spriteItem
        spriteInfo = self.getCurSelectSpriteInfo(self.clickGuardSpriteIndex)
        spriteId = spriteInfo.get('spriteId', 0)
        name = spriteInfo.get('name', '')
        lv = spriteInfo.get('props', {}).get('lv', 0)
        spriteItem.itemSlot.slot.fitSize = True
        spriteItem.itemSlot.slot.dragable = False
        spriteItem.itemSlot.slot.setItemSlotData({'iconPath': self.getSpriteIconPath(spriteId)})
        spriteItem.spriteName.text = name
        spriteItem.spriteLv.text = 'Lv %d' % lv
        self.spriteGuardTipPanel.tipScrollWndList.itemRenderer = 'SummonedWarSpriteGuard_addTipAttributeItem'
        self.spriteGuardTipPanel.tipScrollWndList.dataArray = self.getSpriteBasicInfo()
        self.spriteGuardTipPanel.tipScrollWndList.lableFunction = self.tipItemFunction
        menuParent = self.widget.warSpriteGuardPanel.guardRightMc
        MenuManager.getInstance().showMenu(target, self.spriteGuardTipPanel, {'x': target.parent.x + target.parent.width - 5,
         'y': target.parent.y - target.parent.height + 20}, False, menuParent)

    def getSpriteBasicInfo(self):
        p = BigWorld.player()
        accesspryDict = p.summonedSpriteAccessory
        tPropsList = []
        tSpecialList = []
        for i in range(1, const.SUMMONED_SPRITE_ACCESSORY_COUNT + 1):
            if self.clickAccessoryPart != i:
                continue
            if 'props' in accesspryDict[i]:
                tPropsList = accesspryDict[i]['props']
            if 'specialPSkills' in accesspryDict[i]:
                tSpecialList = accesspryDict[i]

        itemList = []
        for v in tPropsList:
            prd = PRD.data.get(v[0], {})
            name = prd.get('name', '')
            showType = prd.get('showType', 0)
            value = uiUtils.formatProp(v[2], 0, showType)
            szValue = '+%s' % str(value)
            itemList.append({'name': name,
             'value': szValue,
             'color': '#40C133'})

        for sid in tSpecialList:
            value = PD.data.get((sid, 1), {}).get('desc', '')
            name = PTD.data.get(sid, {}).get('sname', '')
            itemList.append({'name': name,
             'value': value,
             'color': '#FFB85D'})

        return itemList

    def tipItemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.nameText.text = itemData.name
        itemMc.valueText.htmlText = uiUtils.toHtml(itemData.value, itemData.color)

    def refreshInfo(self):
        if not self.widget:
            return
        self.updateLeftWarSpritesMc()
        self.updateRightGuardMc()

    def updateLeftWarSpritesMc(self):
        p = BigWorld.player()
        warSpritesMc = self.widget.warSpriteGuardPanel.warSpritesMc
        warSpritesMc.spriteList.itemHeight = 65
        warSpritesMc.spriteList.itemRenderer = 'SummonedWarSpriteGuard_LeftItem'
        warSpritesMc.spriteList.barAlwaysVisible = True
        warSpritesMc.spriteList.dataArray = []
        warSpritesMc.spriteList.lableFunction = self.itemFunction
        spriteNumLimit = p.spriteExtraDict['spriteSlotNum']
        warSpritesMc.holdSpritesText.text = '%d/%d' % (len(p.summonSpriteList), spriteNumLimit)
        warSpritesMc.spriteTypeDropdown.addEventListener(events.INDEX_CHANGE, self.handleSelectWarSpriteType, False, 0, True)
        self.typeToSort = SCD.data.get('spriteMajorAbility', [])
        typeList = []
        for i, vlaue in enumerate(self.typeToSort):
            typeInfo = {}
            typeInfo['label'] = gameStrings.SUMMONED_WAR_SPRITE_TXT1 + '<font color=\"#de5900\">' + vlaue + '</font>' + gameStrings.SUMMONED_WAR_SPRITE_TXT2
            typeInfo['typeIndex'] = i
            typeList.append(typeInfo)

        ASUtils.setDropdownMenuData(warSpritesMc.spriteTypeDropdown, typeList)
        warSpritesMc.spriteTypeDropdown.menuRowCount = min(len(typeList), 5)
        if warSpritesMc.spriteTypeDropdown.selectedIndex == -1:
            warSpritesMc.spriteTypeDropdown.selectedIndex = 0
        self.updateWarSpritesTypeList(warSpritesMc.spriteTypeDropdown.selectedIndex)

    def updateWarSpritesTypeList(self, typeIndex, scrollTo = False):
        warSpriteList = gameglobal.rds.ui.summonedWarSpriteMine.sortWarSpriteList(typeIndex)
        teamList = gameglobal.rds.ui.summonedWarSpriteMine.getSpriteItemInfoList(warSpriteList, typeIndex, showSortDetailInfo=True)
        self.widget.warSpriteGuardPanel.warSpritesMc.spriteList.dataArray = teamList
        self.widget.warSpriteGuardPanel.warSpritesMc.spriteList.validateNow()
        if scrollTo:
            pos = self.widget.warSpriteGuardPanel.warSpritesMc.spriteList.getIndexPosY(self.currSelectSpriteNumber)
            self.widget.warSpriteGuardPanel.warSpritesMc.spriteList.scrollTo(pos)

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.addEventListener(events.MOUSE_DOWN, self.handleSpriteItemBtnClick, False, 0, True)
        itemMc.addEventListener(events.COMPONENT_STATE_CHANGE, self.handleStateChange)
        itemMc.numberId = itemData.numberId
        itemMc.warSpriteIndex = itemData.warSpriteIndex
        itemMc.szName = itemData.name
        itemMc.szLv = '%s' % itemData.lv
        gameglobal.rds.ui.summonedWarSpriteMine.setFamiliarMc(itemMc.familiarMc, itemData.showFamiliar, float(itemData.familiar), float(itemData.famiEffAdd), float(itemData.famiEffLv))
        itemMc.spriteName.text = itemMc.szName
        itemMc.spriteLv.text = itemMc.szLv
        itemMc.itemSlot.slot.setItemSlotData({'iconPath': self.getSpriteIconPath(itemData.spriteId)})
        if utils.getSpriteBattleState(itemMc.warSpriteIndex) and utils.getSpriteAccessoryState(itemMc.warSpriteIndex):
            itemMc.spriteState.visible = True
            itemMc.spriteState.gotoAndStop('zhanAndfu')
        elif utils.getSpriteBattleState(itemMc.warSpriteIndex):
            itemMc.spriteState.visible = True
            itemMc.spriteState.gotoAndStop('zhan')
        elif utils.getSpriteAccessoryState(itemMc.warSpriteIndex):
            itemMc.spriteState.visible = True
            itemMc.spriteState.gotoAndStop('fu')
        else:
            itemMc.spriteState.visible = False
        itemMc.selected = False
        if self.currSelectItemSpriteIndex and self.currSelectItemSpriteIndex == itemData.warSpriteIndex:
            itemMc.selected = True
        elif not self.currSelectItemSpriteIndex and itemData.numberId == 0:
            itemMc.selected = True
        if itemMc.enabled and itemMc.selected:
            self.currSelectItem = itemMc
            self.currSelectSpriteNumber = itemData.numberId
            self.currSelectItemSpriteIndex = itemData.warSpriteIndex
            gameglobal.rds.ui.summonedWarSprite.saveSpriteIndex(itemData.numberId, itemData.warSpriteIndex)
        itemMc.itemSlot.slot.binding = 'summonedWarSprite.%s.%s' % (itemData.warSpriteIndex, itemData.spriteId)
        itemMc.validateNow()
        itemMc.mouseChildren = True
        itemMc.itemSlot.slot.validateNow()
        TipManager.addTipByType(itemMc.itemSlot.slot, tipUtils.TYPE_SPRITE_HEAD_TIP, (itemData.warSpriteIndex,), False, 'upLeft')

    def updateSpriteItemBtnState(self, warSpriteIndex):
        if not self.widget:
            return
        p = BigWorld.player()
        warSpritesMc = self.widget.warSpriteGuardPanel.warSpritesMc
        wndListItems = warSpritesMc.spriteList.items
        wndListLen = len(wndListItems)
        for i in xrange(wndListLen):
            itemMc = wndListItems[i]
            if itemMc.warSpriteIndex == warSpriteIndex:
                if utils.getSpriteBattleState(itemMc.warSpriteIndex) and utils.getSpriteAccessoryState(itemMc.warSpriteIndex):
                    itemMc.spriteState.visible = True
                    itemMc.spriteState.gotoAndStop('zhanAndfu')
                elif utils.getSpriteBattleState(itemMc.warSpriteIndex):
                    itemMc.spriteState.visible = True
                    itemMc.spriteState.gotoAndStop('zhan')
                elif utils.getSpriteAccessoryState(itemMc.warSpriteIndex):
                    itemMc.spriteState.visible = True
                    itemMc.spriteState.gotoAndStop('fu')
                else:
                    itemMc.spriteState.visible = False

    def getCurSelectSpriteInfo(self, idx):
        return BigWorld.player().summonSpriteList.get(idx, {})

    def updateRightGuardMc(self):
        self.updateStructNameAndIcon()
        self.updateStructMc()
        self.updateAttributeMc()
        self.updateGuardMainInfo()

    def updateStructNameAndIcon(self):
        if not self.widget:
            return
        p = BigWorld.player()
        templateId = p.summonedSpriteAccessory.templateId
        if not templateId:
            return
        templateInfo = SSATD.data.get(templateId, {})
        guardRightMc = self.widget.warSpriteGuardPanel.guardRightMc
        guardRightMc.structName.text = templateInfo.get('name', '')

    def updateStructMc(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            accesspryDict = p.summonedSpriteAccessory
            structMc = self.widget.warSpriteGuardPanel.guardRightMc.structMc
            spriteAccessoryOpenLv = SCD.data.get('spriteAccessoryOpenLv', [])
            unLockMsg = SCD.data.get('spriteAccessoryLockInfo', '%d')
            for i in range(1, const.SUMMONED_SPRITE_ACCESSORY_COUNT + 1):
                guardSlot = structMc.getChildByName('spriteGuardSlot%d' % i)
                guardSlot.slot.fitSize = True
                guardSlot.slot.dragable = False
                guardSlot.familiarMc.visible = False
                guardSlot.accessoryPart = i
                if 'spriteIndex' in accesspryDict[i] and accesspryDict[i]['spriteIndex']:
                    guardSlot.spriteIndex = accesspryDict[i]['spriteIndex']
                    spriteInfo = self.getCurSelectSpriteInfo(accesspryDict[i]['spriteIndex'])
                    spriteId = spriteInfo.get('spriteId', 0)
                    guardSlot.slot.setItemSlotData({'iconPath': self.getSpriteIconPath(spriteId)})
                    guardSlot.guardBtn.visible = False
                    guardSlot.lockPicture.visible = False
                    guardSlot.unlockText.visible = False
                    guardSlot.removeSpriteBtn.visible = True
                    guardSlot.guardSfx.visible = False
                    guardSlot.slot.addEventListener(events.MOUSE_CLICK, self.handleSlotClick, False, 0, True)
                    guardSlot.removeSpriteBtn.addEventListener(events.BUTTON_CLICK, self.handleLeaveBtnClick, False, 0, True)
                    gameglobal.rds.ui.summonedWarSpriteMine.setFamiliarMc(guardSlot.familiarMc, True, float(spriteInfo['props']['familiar']), float(spriteInfo['props']['famiEffAdd']), float(spriteInfo['props']['famiEffLv']))
                elif i - 1 < len(spriteAccessoryOpenLv) and p.lv < spriteAccessoryOpenLv[i - 1]:
                    guardSlot.spriteIndex = None
                    guardSlot.slot.setItemSlotData(None)
                    guardSlot.guardBtn.visible = False
                    guardSlot.lockPicture.visible = True
                    guardSlot.unlockText.visible = True
                    guardSlot.unlockText.text = unLockMsg % spriteAccessoryOpenLv[i - 1]
                    guardSlot.removeSpriteBtn.visible = False
                    guardSlot.guardSfx.visible = False
                else:
                    guardSlot.spriteIndex = None
                    guardSlot.slot.setItemSlotData(None)
                    guardSlot.guardBtn.visible = True
                    guardSlot.lockPicture.visible = False
                    guardSlot.unlockText.visible = False
                    guardSlot.removeSpriteBtn.visible = False
                    guardSlot.guardSfx.visible = True
                    guardSlot.guardBtn.addEventListener(events.BUTTON_CLICK, self.handleGuardBtnClick, False, 0, True)
                spriteAbilitys = SSAD.data.get((p.summonedSpriteAccessory.templateId, i, p.school), {}).get('showChar', [])
                self.updateSlotType(guardSlot, spriteAbilitys)

            return

    def updateSlotType(self, guardSlot, spriteAbilitys):
        if not spriteAbilitys:
            return
        typeList = TYPE_NUM_TO_SHOW_SLOT_POS[len(spriteAbilitys)]
        idx = 0
        for i in range(SLOT_TYPE_NUM):
            typeItem = guardSlot.getChildByName('type%d' % i)
            if i in typeList:
                typeItem.visible = True
                tInfo = spriteAbilitys[idx]
                typeItem.addText.text = str(tInfo[1] * 100) + '%'
                typeItem.gotoAndStop(tInfo[0])
                idx = idx + 1
            else:
                typeItem.visible = False

    def getSpriteIconPath(self, spriteId):
        iconId = SSID.data.get(spriteId, {}).get('spriteIcon', '000')
        iconPath = SPRITE_ICON_PATH % str(iconId)
        return iconPath

    def addSpriteGuardSlot(self, spriteIndex, accessoryPart):
        if not self.widget:
            return
        self.refreshInfo()

    def removeSpriteGuardSlot(self, accessoryPart):
        if not self.widget:
            return
        self.refreshInfo()

    def updateAttributeMc(self):
        if not self.widget:
            return
        guardRightMc = self.widget.warSpriteGuardPanel.guardRightMc
        attributeMc = guardRightMc.attributeMc
        self.widget.removeAllInst(attributeMc)
        attributeDict, specialPSkills, allAtkV, extraAdd = self.getSpriteGuardAttribute()
        data = PRD.data
        for i, key in enumerate(sorted(attributeDict.keys())):
            itemMc = self.widget.getInstByClsName('SummonedWarSpriteGuard_addAttributeItem')
            showType = data.get('showType', 0)
            value = uiUtils.formatProp(attributeDict[key], 0, showType)
            name = data.get(key, {}).get('name', '')
            itemMc.y = i * itemMc.height + 5
            itemMc.nameText.text = name
            itemMc.valueText.text = '+%s' % str(value)
            extraVal = int(extraAdd.get(key, 0))
            oriVal = attributeDict[key] - extraVal
            tips = gameStrings.SUMMONED_ACCESSORY_ADD_PROP % (oriVal,
             name,
             extraVal,
             name)
            TipManager.addTip(itemMc, tips, tipUtils.TYPE_DEFAULT_BLACK)
            attributeMc.addChild(itemMc)

        for i, sid in enumerate(specialPSkills):
            itemMc = self.widget.getInstByClsName('SummonedWarSpriteGuard_addAttributeItem')
            value = PD.data.get((sid, 1), {}).get('desc', '')
            name = PTD.data.get(sid, {}).get('sname', '')
            itemMc.y = (len(attributeDict) + i) * itemMc.height + 5
            itemMc.nameText.text = name
            itemMc.valueText.text = value
            attributeMc.addChild(itemMc)

        guardRightMc.atkValT.text = allAtkV

    def updateGuardMainInfo(self):
        guardMainInfoMc = self.widget.warSpriteGuardPanel.guardRightMc.guardMainInfo
        guardMainInfoMc.visible = True
        guardMainInfoMc.guardMainInfoBtn.removeEventListener(events.BUTTON_CLICK, self.handleOpenGuardMainInfo)
        guardMainInfoMc.guardMainInfoBtn.addEventListener(events.BUTTON_CLICK, self.handleOpenGuardMainInfo, False, 0, True)
        if not self.guardMainInfoOpening:
            guardMainInfoMc.gotoAndStop('open')
            guardMainInfoMc.guardMainInfoTxt.htmlText = SCD.data.get('noneSpriteAccessoryInfo', '')
            TipManager.removeTip(guardMainInfoMc.guardMainInfoBtn)
        else:
            guardMainInfoMc.gotoAndStop('close')
            TipManager.addTip(guardMainInfoMc.guardMainInfoBtn, gameStrings.SUMMONED_WAR_SPRITE_GUARD_MAIN_INFO, tipUtils.TYPE_DEFAULT_BLACK)

    def getSpriteGuardAttribute(self):
        p = BigWorld.player()
        accesspryDict = p.summonedSpriteAccessory
        allPorps = []
        specialPSkills = []
        allAtkV = 0
        extraAdd = {}
        cardSystemAdd = p.calcCardSummonedAccessoryProp()
        for k, v in accesspryDict.iteritems():
            if v:
                allPorps += v.get('props', [])
                specialPSkills += v.get('specialPSkills', [])
                allAtkV += v.get('score', 0)
                spriteIndex = v.get('spriteIndex', 0)
                spriteInfo = p.summonSpriteList[spriteIndex]
                spritePropInfo = p.summonSpriteProps.get(spriteIndex, {})
                mainPropInfo = uiUtils.getSpritePropsArray(uiConst.MAIN_PROPS)
                originValDict = {}
                for idx, item in enumerate(mainPropInfo):
                    for i, propInfo in enumerate(item.get('idParam', [])):
                        params, formulaVal = propInfo
                        for idx in xrange(len(params)):
                            prop = params[idx]
                            pVal = commcalc.getSummonedSpritePropValueById(spritePropInfo, prop)
                            originValDict[prop] = pVal

                accessoryInfo = SSAD.data.get((p.summonedSpriteAccessory.templateId, k, p.school), {})
                propTrans = {}
                for srcPropIds, dstPropId, ratio in accessoryInfo['spriteAbilitys']:
                    srcPropId = 0
                    if not (isinstance(srcPropIds, tuple) or isinstance(srcPropIds, list)):
                        srcPropId = srcPropIds
                    else:
                        srcPropId = self._choseMaxValuePropId(originValDict, srcPropIds)
                    if srcPropId not in ACCESSORY_SPRITE_PROPIDS:
                        continue
                    propTrans[dstPropId] = {'srcProp': srcPropId,
                     'ratio': ratio}

                skills = spriteInfo.get('skills', {})
                naturals = skills.get('naturals', [])
                bonus = skills.get('bonus', [])
                argDict = {'naturalSkillNum': len(naturals),
                 'bonusSkillNum': len(bonus),
                 'bonusSkills': [ e for e in bonus ]}
                spriteAccEnhFunc = SCD.data.get('spriteAccEnhFormula', (0, 0, 0))
                accEnhRatio = formula.calcFormulaWithPArg(spriteAccEnhFunc, argDict, 0.0) + 1
                for pId, _, val in v.get('props', []):
                    propertyId = PRD.data.get(pId, {}).get('property', 0)
                    srcPropertyId = propTrans.get(propertyId, {}).get('srcProp', 0)
                    ratio = propTrans.get(propertyId, {}).get('ratio', 0)
                    oriVal = originValDict.get(srcPropertyId, 0)
                    cardAddPercent = cardSystemAdd.get(k, 0)
                    if cardAddPercent:
                        extraAdd.setdefault(pId, 0)
                        extraAdd[pId] += val - int(oriVal * ratio * accEnhRatio)

        result = {}
        for k, _, v in allPorps:
            result[k] = result.get(k, 0) + v

        return (result,
         specialPSkills,
         math.floor(allAtkV),
         extraAdd)

    def _choseMaxValuePropId(self, propDict, srcPropIds):
        maxValue = -1
        retPropId = 0
        for propId in srcPropIds:
            propVal = propDict.get(propId, 0)
            if propVal > maxValue:
                maxValue = propVal
                retPropId = propId

        return retPropId
