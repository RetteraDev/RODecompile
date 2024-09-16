#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteSkin.o
import BigWorld
import events
import gameglobal
import utils
import keys
import uiConst
import gametypes
from asObject import ASObject
from asObject import RedPotManager
from appSetting import Obj as AppSettings
from Scaleform import GfxValue
from guis.asObject import TipManager
from helpers import tickManager
from data import summon_sprite_skin_data as SSSD
from data import summon_sprite_foot_dust_data as SSFDD
from data import sys_config_data as SCD
from data import summon_sprite_info_data as SSID
from data import summon_sprite_data as SSD
from cdata import summon_sprite_skin_seq_data as SSSSD
from cdata import summon_sprite_foot_dust_seq_data as SSFDSD
from cdata import game_msg_def_data as GMDD
from gamestrings import gameStrings
GETED_AND_USED = 2
GETED_AND_NONE_USE = 1
NONE_GETED = 0
SPRITE_SKIN_ICON_PATH = 'summonedSprite/skinIcon/%s.dds'
SPRITE_FOOTDUST_ICON_PATH = 'summonedSprite/footDustIcon/%s.dds'

class SummonedWarSpriteSkin(object):

    def __init__(self, proxy):
        super(SummonedWarSpriteSkin, self).__init__()
        self.parentProxy = proxy
        self.curSelectSkinItem = None
        self.curSelectSkinId = None
        self.tickId = 0
        self.curSelectFootDustItem = None
        self.curSelectFootDustId = None

    def getWidget(self):
        return self.parentProxy.widget

    def getCurSelectSpriteInfo(self):
        idx = self.parentProxy.currSelectItemSpriteIndex
        return BigWorld.player().summonSpriteList.get(idx, {})

    def hideWidget(self):
        self.reset()

    def showWidget(self):
        widget = self.getWidget()
        if not widget:
            return
        if self.tickId:
            tickManager.stopTick(self.tickId)
        self.tickId = tickManager.addTick(10, self.refreshLeftTimeFunc)
        self.parentProxy.updateTabBtnState()

    def reset(self):
        self.curSelectSkinItem = None
        self.curSelectSkinId = None
        self.curSelectFootDustItem = None
        self.curSelectFootDustId = None
        if self.tickId:
            tickManager.stopTick(self.tickId)
        self.tickId = None

    def handleGetFromBtnClick(self, *args):
        widget = self.getWidget()
        changeSkinMc = widget.mineWarSpritePanel.changeSkinMc
        spriteInfo = self.getCurSelectSpriteInfo()
        spriteId = spriteInfo.get('spriteId', 0)
        if changeSkinMc.changeSkinBtn.selected:
            helpKeyWord = SSSD.data.get((spriteId, self.curSelectSkinId), {}).get('helpPathWay', '')
        else:
            helpKeyWord = SSFDD.data.get((spriteId, self.curSelectFootDustId), {}).get('helpPathWay', '')
        gameglobal.rds.ui.help.show(helpKeyWord)

    def handleChangeSkinBtnClick(self, *args):
        e = ASObject(args[3][0])
        changeSkinMc = e.currentTarget.parent
        changeSkinMc.changeSkinBtn.selected = True
        changeSkinMc.stepDustBtn.selected = False
        self.updateSpriteSkinOrFootDustMc()

    def handleStepDustBtnClick(self, *args):
        e = ASObject(args[3][0])
        changeSkinMc = e.currentTarget.parent
        changeSkinMc.changeSkinBtn.selected = False
        changeSkinMc.stepDustBtn.selected = True
        self.updateSpriteSkinOrFootDustMc()

    def handleToUsedBtnClick(self, *args):
        p = BigWorld.player()
        if p.summonedSpriteInWorld and p.summonedSpriteInWorld.inCombat:
            p.showGameMsg(GMDD.data.SPRITE_INCOMBAT_CANNOT_CHANGE_SKIN_DUST, ())
            return
        spriteInfo = self.getCurSelectSpriteInfo()
        spriteId = spriteInfo.get('spriteId', 0)
        widget = self.getWidget()
        changeSkinMc = widget.mineWarSpritePanel.changeSkinMc
        if changeSkinMc.changeSkinBtn.selected:
            p.base.useSummonSpriteSkin(self.parentProxy.currSelectItemSpriteIndex, spriteId, self.curSelectSkinId)
        else:
            p.base.useSummonSpriteFootDust(self.parentProxy.currSelectItemSpriteIndex, spriteId, self.curSelectFootDustId)

    def hanedleSkinItemClick(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        spriteInfo = self.getCurSelectSpriteInfo()
        spriteId = spriteInfo.get('spriteId', 0)
        if self.curSelectSkinId and self.curSelectSkinId == itemMc.skinId and spriteId == itemMc.spriteId:
            return
        if self.curSelectSkinItem:
            self.curSelectSkinItem.skinSP.visible = False
        itemMc.skinSP.visible = True
        self.curSelectSkinItem = itemMc
        self.curSelectSkinId = itemMc.skinId
        self.changeSpriteSkin()
        self.updateUsedBtnState(itemMc.spriteSkinState)
        self.updateSelectName(itemMc.skinName)
        self.saveClickSkin(itemMc.spriteId, itemMc.skinId)
        self.updateSkinMcRedPot()
        self.updateSkinBtnRedPot()
        self.parentProxy.updateChangeSkinBtnRedPot()
        self.parentProxy.updateSpriteItemRedPot()
        gameglobal.rds.ui.summonedWarSprite.updateSpriteTab0RedPot()
        self.parentProxy.playSoundAndAction('spriteSoundList4', 'spriteActionList4', 'spriteActionPro4')

    def hanedleFootDustItemClick(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        spriteInfo = self.getCurSelectSpriteInfo()
        spriteId = spriteInfo.get('spriteId', 0)
        if self.curSelectFootDustId and self.curSelectFootDustId == itemMc.footDustId and spriteId == itemMc.spriteId:
            return
        if self.curSelectFootDustItem:
            self.curSelectFootDustItem.skinSP.visible = False
        itemMc.skinSP.visible = True
        self.curSelectFootDustItem = itemMc
        self.curSelectFootDustId = itemMc.footDustId
        self.changeSpriteFootDust()
        self.updateUsedBtnState(itemMc.footDustState)
        self.updateSelectName(itemMc.footDustName)
        self.saveClickDust(itemMc.spriteId, itemMc.footDustId)
        self.updateDustMcRedPot()
        self.updateDustBtnRedPot()
        self.parentProxy.updateChangeSkinBtnRedPot()
        self.parentProxy.updateSpriteItemRedPot()
        gameglobal.rds.ui.summonedWarSprite.updateSpriteTab0RedPot()

    def handleChangeFormBtnClick(self, *args):
        e = ASObject(args[3][0])
        if self.parentProxy.isTransform:
            self.parentProxy.isTransform = False
        else:
            self.parentProxy.isTransform = True
        self.changeSpriteSkin()

    def refreshWidget(self):
        widget = self.getWidget()
        if not widget:
            return
        changeSkinMc = widget.mineWarSpritePanel.changeSkinMc
        changeSkinMc.changeForm.addEventListener(events.BUTTON_CLICK, self.handleChangeFormBtnClick, False, 0, True)
        changeSkinMc.changeSkinBtn.addEventListener(events.BUTTON_CLICK, self.handleChangeSkinBtnClick, False, 0, True)
        changeSkinMc.stepDustBtn.addEventListener(events.BUTTON_CLICK, self.handleStepDustBtnClick, False, 0, True)
        changeSkinMc.changeSkinBtn.selected = True
        changeSkinMc.stepDustBtn.selected = False
        TipManager.addTip(widget.mineWarSpritePanel.changeSkinMc.changeForm, SCD.data.get('spriteTransformBtnTip', ''))
        RedPotManager.removeRedPotById(uiConst.SUMMONED_WAR_SPRITE_SKIN_BTN)
        RedPotManager.addRedPot(changeSkinMc.changeSkinBtn, uiConst.SUMMONED_WAR_SPRITE_SKIN_BTN, (changeSkinMc.changeSkinBtn.width - 9, -3), self.visiblePotFunSkinBtn)
        RedPotManager.removeRedPotById(uiConst.SUMMONED_WAR_SPRITE_DUST_BTN)
        RedPotManager.addRedPot(changeSkinMc.stepDustBtn, uiConst.SUMMONED_WAR_SPRITE_DUST_BTN, (changeSkinMc.stepDustBtn.width - 9, -3), self.visiblePotFunDustBtn)
        self.updateWarSpriteInfo()
        self.updateSpriteSkinOrFootDustMc()

    def visiblePotFunSkinBtn(self, *args):
        return GfxValue(self.checkSkinBtnRedPoint(self.parentProxy.currSelectItemSpriteIndex))

    def updateSkinBtnRedPot(self):
        RedPotManager.updateRedPot(uiConst.SUMMONED_WAR_SPRITE_SKIN_BTN)

    def updateSkinMcRedPot(self):
        if not self.curSelectSkinItem:
            return
        self.curSelectSkinItem.redPotIcon.visible = False

    def visiblePotFunDustBtn(self, *args):
        return GfxValue(self.checkDustBtnRedPoint(self.parentProxy.currSelectItemSpriteIndex))

    def updateDustBtnRedPot(self):
        RedPotManager.updateRedPot(uiConst.SUMMONED_WAR_SPRITE_DUST_BTN)

    def updateDustMcRedPot(self):
        if not self.curSelectFootDustItem:
            return
        self.curSelectFootDustItem.redPotIcon.visible = False

    def updateWarSpriteInfo(self):
        widget = self.getWidget()
        spriteInfo = self.getCurSelectSpriteInfo()
        spriteId = spriteInfo.get('spriteId', 0)
        spriteData = SSID.data.get(spriteId, {})
        changeSkinMc = widget.mineWarSpritePanel.changeSkinMc
        changeSkinMc.spriteName.text = spriteInfo.get('name', '')
        attackType = spriteData.get('atkType', 0)
        tipMsg = ''
        if attackType == 1:
            changeSkinMc.attackType.gotoAndStop('nearWar')
            tipMsg = SCD.data.get('spriteNearWarTip', '')
        elif attackType == 2:
            changeSkinMc.attackType.gotoAndStop('farWar')
            tipMsg = SCD.data.get('spriteFarWarTip', '')
        elif attackType == 3:
            changeSkinMc.attackType.gotoAndStop('magic')
            tipMsg = SCD.data.get('spriteMagicTip', '')
        TipManager.addTip(changeSkinMc.attackType, tipMsg)
        changeSkinMc.rareIcon.visible = spriteData.get('isRare', False)
        if changeSkinMc.rareIcon.visible:
            changeSkinMc.rareIcon.gotoAndStop('type' + str(spriteData.get('isRare')))
        self.updateSpriteBattleBigState()
        transformModelId = SSD.data.get(spriteId, {}).get('transformModelId', 0)
        changeSkinMc.changeForm.visible = transformModelId

    def updateSpriteBattleBigState(self):
        stateMc = self.getWidget().mineWarSpritePanel.changeSkinMc.spriteType
        if utils.getSpriteBattleState(self.parentProxy.currSelectItemSpriteIndex):
            stateMc.visible = True
            stateMc.gotoAndStop('state1')
        elif utils.getSpriteAccessoryState(self.parentProxy.currSelectItemSpriteIndex):
            stateMc.visible = True
            stateMc.gotoAndStop('state0')
        else:
            stateMc.visible = False

    def updateSpriteSkinOrFootDustMc(self):
        widget = self.getWidget()
        if not widget:
            return
        changeSkinMc = widget.mineWarSpritePanel.changeSkinMc
        if changeSkinMc.changeSkinBtn.selected:
            bSkinSelect = True
        else:
            bSkinSelect = False
        spriteInfo = self.getCurSelectSpriteInfo()
        spriteId = spriteInfo.get('spriteId', 0)
        changeSkinMc.spriteSkinList.itemRenderer = 'SummonedWarSpriteMine_changeSkinItem'
        changeSkinMc.spriteSkinList.dataArray = []
        if bSkinSelect:
            changeSkinMc.spriteSkinList.lableFunction = self.itemSkinFunction
            self.updateSkinItem(spriteId)
        else:
            changeSkinMc.spriteSkinList.lableFunction = self.itemFootDustFunction
            self.updateFootDustItem(spriteId)

    def updateSkinItem(self, spriteId):
        widget = self.getWidget()
        changeSkinMc = widget.mineWarSpritePanel.changeSkinMc
        p = BigWorld.player()
        skinDict = SSSSD.data.get(spriteId, {})
        itemSkinList = []
        for k in sorted(skinDict.keys()):
            skinId = skinDict[k]
            skinData = SSSD.data.get((spriteId, skinId), {})
            iconId = skinData.get('skinIcon', 0)
            itemInfo = {}
            itemInfo['index'] = k
            itemInfo['skinId'] = skinId
            itemInfo['spriteId'] = spriteId
            itemInfo['iconPath'] = SPRITE_SKIN_ICON_PATH % str(iconId)
            itemInfo['skinName'] = skinData.get('skinName', '')
            itemInfo['tExpire'] = self.getSkinItemExpire(spriteId, skinId)
            if spriteId in p.summonSpriteSkin and p.summonSpriteSkin[spriteId].curUseDict.get(self.parentProxy.currSelectItemSpriteIndex, 0) == skinId:
                itemInfo['skinState'] = GETED_AND_USED
            elif spriteId in p.summonSpriteSkin and skinId in p.summonSpriteSkin[spriteId].totalList:
                itemInfo['skinState'] = GETED_AND_NONE_USE
            else:
                itemInfo['skinState'] = NONE_GETED
            itemInfo['isRedPot'] = self.checkSpirteSkinClick(self.parentProxy.currSelectItemSpriteIndex, spriteId, skinId)
            itemSkinList.append(itemInfo)

        changeSkinMc.spriteSkinList.dataArray = itemSkinList
        changeSkinMc.spriteSkinList.validateNow()

    def getSkinItemExpire(self, spriteId, skinId):
        p = BigWorld.player()
        return p.summonSpriteSkin[spriteId].tempDict.get(skinId, 0)

    def getFootDustExpire(self, spriteId, dustId):
        p = BigWorld.player()
        return p.summonSpriteFootDust[spriteId].tempDict.get(dustId, 0)

    def getExpireText(self, tExpire):
        if tExpire:
            leftTime = max(0, tExpire - utils.getNow())
            day = utils.formatDurationLeftDay(leftTime)
            hour = utils.formatDurationLeftHour(leftTime)
            minute = utils.formatDurationLeftMin(leftTime)
            return gameStrings.BACK_FLOW_LEFT_TIME % (day, hour, minute)
        return ''

    def refreshLeftTimeFunc(self):
        widget = self.getWidget()
        if not widget:
            return
        spriteSkinList = widget.mineWarSpritePanel.changeSkinMc.spriteSkinList
        for i in xrange(spriteSkinList.canvas.numChildren):
            skinItem = spriteSkinList.canvas.getChildAt(i)
            expireText = self.getExpireText(skinItem.tExpire)
            if expireText:
                skinItem.timeArea.visible = True
                skinItem.timeArea.textField.text = expireText
            else:
                skinItem.timeArea.visible = False

    def itemSkinFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.removeEventListener(events.MOUSE_DOWN, self.hanedleFootDustItemClick)
        itemMc.addEventListener(events.MOUSE_DOWN, self.hanedleSkinItemClick, False, 0, True)
        itemMc.skinId = itemData.skinId
        itemMc.spriteId = itemData.spriteId
        itemMc.spriteSkinState = itemData.skinState
        itemMc.skinName = itemData.skinName
        itemMc.isRedPot = itemData.isRedPot
        itemMc.tExpire = itemData.tExpire
        itemMc.skinN.text = itemData.skinName
        itemMc.icon.clear()
        itemMc.icon.fitSize = True
        itemMc.icon.loadImage(itemData.iconPath)
        if itemData.skinState == GETED_AND_USED:
            itemMc.skinState.visible = True
            itemMc.skinState.gotoAndStop('yiqiyong')
        elif itemData.skinState == NONE_GETED:
            itemMc.skinState.visible = True
            itemMc.skinState.gotoAndStop('weijiesuo')
        else:
            itemMc.skinState.visible = False
        expireText = self.getExpireText(itemData.tExpire)
        if expireText:
            itemMc.timeArea.visible = True
            itemMc.timeArea.textField.text = expireText
        else:
            itemMc.timeArea.visible = False
        itemMc.redPotIcon.visible = not itemData.isRedPot
        itemMc.skinSP.visible = False
        if self.curSelectSkinId and self.curSelectSkinId == itemData.skinId:
            itemMc.skinSP.visible = True
        elif not self.curSelectSkinId and itemData.skinState == GETED_AND_USED:
            itemMc.skinSP.visible = True
        elif not self.curSelectSkinId and itemData.skinState == GETED_AND_NONE_USE:
            itemMc.skinSP.visible = True
        elif not self.curSelectSkinId:
            itemMc.skinSP.visible = True
        if itemMc.skinSP.visible:
            self.curSelectSkinItem = itemMc
            self.curSelectSkinId = itemMc.skinId
            self.changeSpriteSkin()
            self.updateUsedBtnState(itemData.skinState)
            self.updateSelectName(itemData.skinName)
            self.saveClickSkin(itemMc.spriteId, itemMc.skinId)
            self.updateSkinBtnRedPot()
            self.parentProxy.updateChangeSkinBtnRedPot()
            self.parentProxy.updateSpriteItemRedPot()
            gameglobal.rds.ui.summonedWarSprite.updateSpriteTab0RedPot()

    def changeSpriteSkin(self):
        spriteInfo = self.getCurSelectSpriteInfo()
        spriteId = spriteInfo.get('spriteId', 0)
        skinData = SSSD.data.get((spriteId, self.curSelectSkinId), {})
        if self.parentProxy.isTransform:
            spriteModel = skinData.get('transformModelIdAfter', 0)
            materials = skinData.get('materialsAfter', 'Default')
        else:
            spriteModel = skinData.get('transformModelIdBefore', 0)
            materials = skinData.get('materialsBefore', 'Default')
        if gameglobal.rds.ui.summonedWarSpriteMine.headGen and spriteModel:
            gameglobal.rds.ui.summonedWarSpriteMine.headGen.startCapture(spriteModel, materials, None)

    def updateUsedBtnState(self, state):
        widget = self.getWidget()
        changeSkinMc = widget.mineWarSpritePanel.changeSkinMc
        if state == GETED_AND_USED:
            changeSkinMc.toUseBtn.visible = False
            changeSkinMc.usedP.visible = True
            changeSkinMc.getFromBtn.visible = False
        elif state == GETED_AND_NONE_USE:
            changeSkinMc.toUseBtn.visible = True
            changeSkinMc.usedP.visible = False
            changeSkinMc.getFromBtn.visible = False
            changeSkinMc.toUseBtn.addEventListener(events.BUTTON_CLICK, self.handleToUsedBtnClick, False, 0, True)
        else:
            changeSkinMc.toUseBtn.visible = False
            changeSkinMc.usedP.visible = False
            changeSkinMc.getFromBtn.visible = True
            changeSkinMc.getFromBtn.addEventListener(events.BUTTON_CLICK, self.handleGetFromBtnClick, False, 0, True)

    def updateSelectName(self, selectName):
        widget = self.getWidget()
        changeSkinMc = widget.mineWarSpritePanel.changeSkinMc
        changeSkinMc.skinName.text = selectName

    def updateFootDustItem(self, spriteId):
        widget = self.getWidget()
        footDustDict = SSFDSD.data.get(spriteId, {})
        p = BigWorld.player()
        spriteSkinList = widget.mineWarSpritePanel.changeSkinMc.spriteSkinList
        itemList = []
        for k in sorted(footDustDict.keys()):
            footDustId = footDustDict[k]
            footDustData = SSFDD.data.get((spriteId, footDustId), {})
            iconId = footDustData.get('footDustIcon', 0)
            itemInfo = {}
            itemInfo['footDustId'] = footDustId
            itemInfo['spriteId'] = spriteId
            itemInfo['iconPath'] = SPRITE_FOOTDUST_ICON_PATH % str(iconId)
            itemInfo['footDustName'] = footDustData.get('footDustName', '')
            itemInfo['tExpire'] = self.getFootDustExpire(spriteId, footDustId)
            if spriteId in p.summonSpriteFootDust and p.summonSpriteFootDust[spriteId].curUseDict.get(self.parentProxy.currSelectItemSpriteIndex, 0) == footDustId:
                itemInfo['footDustState'] = GETED_AND_USED
            elif spriteId in p.summonSpriteFootDust and footDustId in p.summonSpriteFootDust[spriteId].totalList:
                itemInfo['footDustState'] = GETED_AND_NONE_USE
            else:
                itemInfo['footDustState'] = NONE_GETED
            itemInfo['isFootRedPot'] = self.checkSpirteDustClick(self.parentProxy.currSelectItemSpriteIndex, spriteId, footDustId)
            itemList.append(itemInfo)

        spriteSkinList.dataArray = itemList
        spriteSkinList.validateNow()

    def itemFootDustFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.removeEventListener(events.MOUSE_DOWN, self.hanedleSkinItemClick)
        itemMc.addEventListener(events.MOUSE_DOWN, self.hanedleFootDustItemClick, False, 0, True)
        itemMc.footDustId = itemData.footDustId
        itemMc.spriteId = itemData.spriteId
        itemMc.footDustState = itemData.footDustState
        itemMc.footDustName = itemData.footDustName
        itemMc.skinN.text = itemData.footDustName
        itemMc.icon.clear()
        itemMc.icon.fitSize = True
        itemMc.icon.loadImage(itemData.iconPath)
        if itemData.footDustState == GETED_AND_USED:
            itemMc.skinState.visible = True
            itemMc.skinState.gotoAndStop('yiqiyong')
        elif itemData.footDustState == NONE_GETED:
            itemMc.skinState.visible = True
            itemMc.skinState.gotoAndStop('weijiesuo')
        else:
            itemMc.skinState.visible = False
        itemMc.tExpire = itemData.tExpire
        expireText = self.getExpireText(itemData.tExpire)
        if expireText:
            itemMc.timeArea.visible = True
            itemMc.timeArea.textField.text = expireText
        else:
            itemMc.timeArea.visible = False
        itemMc.redPotIcon.visible = not itemData.isFootRedPot
        itemMc.skinSP.visible = False
        if self.curSelectFootDustId and self.curSelectFootDustId == itemData.footDustId:
            itemMc.skinSP.visible = True
        elif not self.curSelectFootDustId and itemData.skinState == GETED_AND_USED:
            itemMc.skinSP.visible = True
        elif not self.curSelectFootDustId and itemData.skinState == GETED_AND_NONE_USE:
            itemMc.skinSP.visible = True
        elif not self.curSelectFootDustId:
            itemMc.skinSP.visible = True
        if itemMc.skinSP.visible:
            self.curSelectFootDustItem = itemMc
            self.curSelectFootDustId = itemMc.footDustId
            self.changeSpriteFootDust()
            self.updateUsedBtnState(itemData.footDustState)
            self.updateSelectName(itemData.footDustName)
            self.saveClickDust(itemData.spriteId, itemData.footDustId)
            self.updateDustBtnRedPot()
            self.parentProxy.updateChangeSkinBtnRedPot()
            self.parentProxy.updateSpriteItemRedPot()
            gameglobal.rds.ui.summonedWarSprite.updateSpriteTab0RedPot()

    def changeSpriteFootDust(self):
        if not gameglobal.rds.ui.summonedWarSpriteMine.headGen:
            return
        model = gameglobal.rds.ui.summonedWarSpriteMine.headGen.adaptor.attachment
        self.parentProxy.updateAttachEffect(model, self.curSelectFootDustId, True)

    def saveClickSkin(self, spriteId, skinId):
        if self.checkSpirteSkinClick(self.parentProxy.currSelectItemSpriteIndex, spriteId, skinId):
            return
        self.realSaveSkin(spriteId, skinId)

    def realSaveSkin(self, spriteId, skinId):
        p = BigWorld.player()
        redStr = '%d-%d-%d' % (p.gbId, spriteId, skinId)
        tmpVal = AppSettings.get(keys.SET_DONE_RED_POT_SPRITE_SKINS, '')
        AppSettings[keys.SET_DONE_RED_POT_SPRITE_SKINS] = '%s,%s' % (tmpVal, redStr)
        AppSettings.save()

    def checkSkinSaved(self, spriteId, skinId):
        p = BigWorld.player()
        tmpVal = AppSettings.get(keys.SET_DONE_RED_POT_SPRITE_SKINS, '')
        redPotArr = tmpVal.split(',')
        for redStr in redPotArr:
            redList = redStr.split('-')
            if redList and len(redList) > 2:
                if int(redList[0]) == p.gbId and int(redList[1]) == spriteId and int(redList[2]) == skinId:
                    return True

        return False

    def checkSpirteSkinClick(self, spriteIndex, spriteId, skinId):
        if not spriteIndex:
            return
        p = BigWorld.player()
        if spriteId in p.summonSpriteSkin and p.summonSpriteSkin[spriteId].curUseDict.get(spriteIndex, 0) == skinId:
            if not self.checkSkinSaved(spriteId, skinId):
                self.realSaveSkin(spriteId, skinId)
            return True
        unlockType = SSSD.data.get((spriteId, skinId), {}).get('unlockType', ())
        for typeV in unlockType:
            if typeV == gametypes.SPRITE_APPEARANCE_UNLOCK_TYPE_DEFAULT:
                if not self.checkSkinSaved(spriteId, skinId):
                    self.realSaveSkin(spriteId, skinId)
                return True

        if spriteId in p.summonSpriteSkin and skinId not in p.summonSpriteSkin[spriteId].totalList:
            return True
        return self.checkSkinSaved(spriteId, skinId)

    def checkSkinBtnRedPoint(self, spriteIndex):
        if not spriteIndex:
            return False
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(spriteIndex, {})
        spriteId = spriteInfo.get('spriteId', 0)
        if not spriteId:
            return False
        skinDict = SSSSD.data.get(spriteId, {})
        for k in sorted(skinDict.keys()):
            skinId = skinDict[k]
            if self.checkSpirteSkinClick(spriteIndex, spriteId, skinId):
                continue
            return True

        return False

    def saveClickDust(self, spriteId, dustId):
        if self.checkSpirteDustClick(self.parentProxy.currSelectItemSpriteIndex, spriteId, dustId):
            return
        self.realSaveDust(spriteId, dustId)

    def realSaveDust(self, spriteId, dustId):
        p = BigWorld.player()
        redStr = '%d-%d-%d' % (p.gbId, spriteId, dustId)
        tmpVal = AppSettings.get(keys.SET_DONE_RED_POT_SPRITE_DUSTS, '')
        AppSettings[keys.SET_DONE_RED_POT_SPRITE_DUSTS] = '%s,%s' % (tmpVal, redStr)
        AppSettings.save()

    def checkDustSaved(self, spriteId, footDustId):
        p = BigWorld.player()
        tmpVal = AppSettings.get(keys.SET_DONE_RED_POT_SPRITE_DUSTS, '')
        redPotArr = tmpVal.split(',')
        for redStr in redPotArr:
            redList = redStr.split('-')
            if redList and len(redList) > 2:
                if int(redList[0]) == p.gbId and int(redList[1]) == spriteId and int(redList[2]) == footDustId:
                    return True

        return False

    def checkSpirteDustClick(self, spriteIndex, spriteId, footDustId):
        if not spriteIndex:
            return
        p = BigWorld.player()
        if spriteId in p.summonSpriteFootDust and p.summonSpriteFootDust[spriteId].curUseDict.get(spriteIndex, 0) == footDustId:
            if not self.checkDustSaved(spriteId, footDustId):
                self.realSaveDust(spriteId, footDustId)
            return True
        unlockType = SSFDD.data.get((spriteId, footDustId), {}).get('unlockType', ())
        for typeV in unlockType:
            if typeV == gametypes.SPRITE_APPEARANCE_UNLOCK_TYPE_DEFAULT:
                if not self.checkDustSaved(spriteId, footDustId):
                    self.realSaveDust(spriteId, footDustId)
                return True

        if spriteId in p.summonSpriteFootDust and footDustId not in p.summonSpriteFootDust[spriteId].totalList:
            return True
        return self.checkDustSaved(spriteId, footDustId)

    def checkDustBtnRedPoint(self, spriteIndex):
        if not spriteIndex:
            return False
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(spriteIndex, {})
        spriteId = spriteInfo.get('spriteId', 0)
        if not spriteId:
            return False
        dustDict = SSFDSD.data.get(spriteId, {})
        for k in sorted(dustDict.keys()):
            dustId = dustDict[k]
            if self.checkSpirteDustClick(spriteIndex, spriteId, dustId):
                continue
            return True

        return False
