#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteMineProxy.o
import BigWorld
import Math
import events
import gametypes
import gameglobal
import gamelog
import uiConst
import skillDataInfo
import tipUtils
import random
import ui
import utils
import commcalc
import const
import math
from uiProxy import UIProxy
from asObject import ASObject
from guis import uiUtils
from guis import summonedWarSpriteProperty
from guis import summonedWarSpriteSkill
from guis import summonedWarSpriteSkin
from item import Item
from helpers import capturePhoto
from gamestrings import gameStrings
from sfx import flyEffect
from sfx import sfx
from callbackHelper import Functor
from asObject import RedPotManager
from Scaleform import GfxValue
from guis.asObject import ASUtils
from guis.asObject import MenuManager
from guis.asObject import TipManager
from data import sys_config_data as SCD
from data import summon_sprite_info_data as SSID
from data import summon_sprite_skill_data as SSSD
from data import item_data as ID
from data import consumable_item_data as CID
from data import summon_sprite_levelup_data as SSLD
from data import summon_sprite_familiar_data as SSFD
from data import game_msg_data as GMD
from data import summon_sprite_skin_data as SSSKIND
from data import summon_sprite_foot_dust_data as SSFDD
from data import sprite_upgrade_data as SUD
from data import monster_model_client_data as MMCD
from data import summon_sprite_data as SSD
from cdata import game_msg_def_data as GMDD
from cdata import summon_sprite_bonus_skill_data as SSBSD
from cdata import font_config_data as FCD
TAB_INDEX0 = 0
TAB_INDEX1 = 1
TAB_INDEX2 = 2
TAB_INDEX3 = 3
SORT_TYPE_FAMIEFFLV = 0
SORT_TYPE_LV = 1
SORT_TYPE_MHP = 2
SORT_TYPE_PHY_ATTACK = 3
SORT_TYPE_MAG_ATTACK = 4
SORT_TYPE_PHY_EQUIP = 5
SORT_TYPE_MAG_EQUIP = 6
MAX_TALENT_NUM = 4
MAX_BONUS_NUM = 2
SPRITE_SKILL_SIGN_ID = 100
HUNGER_ITEM_NUM_LIMIT = 1
BONUS_POINT_NUM_ONE = 1
BONUS_POINT_NUM_TWO = 2
BONUS_POINT_TYPE0 = 0
BONUS_POINT_TYPE1 = 1
BONUS_POINT_TYPE2 = 2
SPRITE_ICON_PATH = 'summonedSprite/icon/%s.dds'
TABLE_BTN_NAME_OVERVIEW = 'overviewTabBtn'
TABLE_BTN_NAME_ATTRIBUTE = 'attributeTabBtn'
TABLE_BTN_NAME_SKILL = 'skillTabBtn'
TABLE_BTN_NAME_PEELER = 'changeSkinTabBtn'
m_tTabBtnList = {TABLE_BTN_NAME_OVERVIEW: 'overviewMc',
 TABLE_BTN_NAME_ATTRIBUTE: 'attributeMc',
 TABLE_BTN_NAME_SKILL: 'skillMc',
 TABLE_BTN_NAME_PEELER: 'changeSkinMc'}
SUB_TAB_MAP = {1: TABLE_BTN_NAME_OVERVIEW,
 2: TABLE_BTN_NAME_ATTRIBUTE,
 3: TABLE_BTN_NAME_SKILL,
 4: TABLE_BTN_NAME_PEELER}
FEED_EXP_PANEL = 'feedExpMc'
FEED_PRIVITY_PANEL = 'feedPrivityMc'
FEED_HUNGER_PANEL = 'feedHungerMc'

class SummonedWarSpriteMineProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteMineProxy, self).__init__(uiAdapter)
        self.widget = None
        self.currentTabIndex = -1
        self.warSpriteList = []
        self.spriteItemList = []
        self.selectTabBtnName = ''
        self.currSelectSpriteNumber = 0
        self.currSelectItem = None
        self.currSelectItemSpriteIndex = None
        self.headGen = None
        self.recordfamiLv = {}
        self.feedTipsPanel = None
        self.currShowFeedMc = None
        self.currSelectFeedItem = None
        self.currSelectFoodItemId = None
        self.callback = None
        self.isTransform = False
        self.propertyProxy = summonedWarSpriteProperty.SummonedWarSpriteMineProperty(self)
        self.skillProxy = summonedWarSpriteSkill.SummonedWarSpriteSkill(self)
        self.changeSkinProxy = summonedWarSpriteSkin.SummonedWarSpriteSkin(self)
        self.subProxys = {TABLE_BTN_NAME_OVERVIEW: self,
         TABLE_BTN_NAME_ATTRIBUTE: self.propertyProxy,
         TABLE_BTN_NAME_SKILL: self.skillProxy,
         TABLE_BTN_NAME_PEELER: self.changeSkinProxy}
        self.gotoTabBtnNames = ''
        self.qualityColorDic = {0: 'white',
         1: 'green_1',
         2: 'blue_2',
         3: 'purple_3',
         4: 'golden_4'}
        self.isGotoAddPrivity = False
        self.isShiftKeyDown = False

    def reset(self):
        self.currentTabIndex = -1
        self.warSpriteList = []
        self.spriteItemList = []
        self.selectTabBtnName = ''
        self.currSelectItem = None
        self.recordfamiLv = {}
        self.currSelectItemSpriteIndex = None
        self.currSelectSpriteNumber = 0
        self.feedTipsPanel = None
        self.currShowFeedMc = None
        self.currSelectFeedItem = None
        self.currSelectFoodItemId = None
        self.isTransform = False

    def unRegisterPanel(self):
        self.propertyProxy.hideWidget()
        self.skillProxy.hideWidget()
        self.changeSkinProxy.hideWidget()
        self.widget = None
        self.reset()

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()
        if self.gotoTabBtnNames:
            self.selectTabBtnName = self.gotoTabBtnNames
            self.gotoTabBtnNames = ''
            ASUtils.DispatchButtonEvent(getattr(self.widget.mineWarSpritePanel, self.selectTabBtnName))
        else:
            self.selectTabBtnName = TABLE_BTN_NAME_OVERVIEW
        self.widget.stage.addEventListener(events.KEYBOARD_EVENT_KEY_DOWN, self.handleKeyEvent, False, 0, True)
        self.widget.stage.addEventListener(events.KEYBOARD_EVENT_KEY_UP, self.handleKeyEvent, False, 0, True)

    def setSubTabIdx(self, idx):
        if not SUB_TAB_MAP.has_key(idx):
            return
        if self.widget:
            ASUtils.DispatchButtonEvent(getattr(self.widget.mineWarSpritePanel, SUB_TAB_MAP[idx]))
        else:
            self.gotoTabBtnNames = SUB_TAB_MAP[idx]

    def initUI(self):
        mineWarSpritePanel = self.widget.mineWarSpritePanel
        if not gameglobal.rds.configData.get('enableSummonedWarSpriteDisabledFun', False):
            mineWarSpritePanel.changeSkinTabBtn.disabled = True
            mineWarSpritePanel.overviewMc.aWakeBtn.disabled = True
            TipManager.addTip(mineWarSpritePanel.changeSkinTabBtn, gameStrings.SUMMONED_WAR_SPRITE_COMING_SOON)
            TipManager.addTip(mineWarSpritePanel.overviewMc.aWakeBtn, gameStrings.SUMMONED_WAR_SPRITE_COMING_SOON)
        mineWarSpritePanel.commentBtn.visible = False
        mineWarSpritePanel.overviewTabBtn.addEventListener(events.BUTTON_CLICK, self.handleTabBtnClick, False, 0, True)
        mineWarSpritePanel.attributeTabBtn.addEventListener(events.BUTTON_CLICK, self.handleTabBtnClick, False, 0, True)
        mineWarSpritePanel.skillTabBtn.addEventListener(events.BUTTON_CLICK, self.handleTabBtnClick, False, 0, True)
        mineWarSpritePanel.changeSkinTabBtn.addEventListener(events.BUTTON_CLICK, self.handleTabBtnClick, False, 0, True)
        mineWarSpritePanel.rememberBtn.addEventListener(events.BUTTON_CLICK, self.handleRememberBtnClick, False, 0, True)
        mineWarSpritePanel.commentBtn.addEventListener(events.BUTTON_CLICK, self.handleCommentBtnClick, False, 0, True)
        TipManager.addTip(mineWarSpritePanel.rememberBtn, gameStrings.SPRITE_PICTURE_TIP)
        self.initLeftWarSpritesMc()
        self.initOverviewMc()
        self.currSelectSpriteNumber = gameglobal.rds.ui.summonedWarSprite.recordSpriteNumber
        self.currSelectItemSpriteIndex = gameglobal.rds.ui.summonedWarSprite.recordSpriteIndex
        RedPotManager.removeRedPotById(uiConst.SUMMONED_WAR_SPRITE_CHANGE_SKIN_BTN)
        RedPotManager.addRedPot(mineWarSpritePanel.changeSkinTabBtn, uiConst.SUMMONED_WAR_SPRITE_CHANGE_SKIN_BTN, (mineWarSpritePanel.changeSkinTabBtn.width - 8, -3), self.visiblePotFunChangeSkinBtn)
        p = BigWorld.player()
        if p.isUsingTemp():
            mineWarSpritePanel.changeSkinTabBtn.visible = False
            mineWarSpritePanel.rememberBtn.visible = False

    def visiblePotFunChangeSkinBtn(self, *args):
        return GfxValue(self.changeSkinProxy.checkSkinBtnRedPoint(self.currSelectItemSpriteIndex) or self.changeSkinProxy.checkDustBtnRedPoint(self.currSelectItemSpriteIndex))

    def updateChangeSkinBtnRedPot(self):
        RedPotManager.updateRedPot(uiConst.SUMMONED_WAR_SPRITE_CHANGE_SKIN_BTN)

    def handleTabBtnClick(self, *args):
        e = ASObject(args[3][0])
        btnName = e.currentTarget.name
        self.setTabSelected(btnName)

    def setTabSelected(self, btnName):
        if btnName != self.selectTabBtnName:
            self.selectTabBtnName = btnName
            subProxy = self.subProxys.get(btnName)
            if subProxy:
                subProxy.showWidget()

    def showWidget(self):
        self.updateTabBtnState()

    def handleAWakeBtnClick(self, *args):
        p = BigWorld.player()
        p.base.preSummonSpriteJuexing(self.currSelectItemSpriteIndex)

    def handleRareTransferBtnClick(self, *args):
        gameglobal.rds.ui.summonedWarSpriteRareTransfer.show(self.currSelectItemSpriteIndex)

    def handleUpGradeBtnClick(self, *args):
        gameglobal.rds.ui.summonedWarSpriteUpGrade.show(self.currSelectItemSpriteIndex)

    def handleReadyBtnClick(self, *args):
        gameglobal.rds.ui.summonedWarSpriteFight.show()

    def handleXiuLianBtnClick(self, *args):
        gameglobal.rds.ui.summonedWarSpriteEffect.show(self.currSelectItemSpriteIndex)

    def handleMainAttrBtnClick(self, *args):
        self.updateAttributeInfoOther(True)
        self.updateAttributeInfo()

    def handleFightAttrBtnClick(self, *args):
        self.updateAttributeInfoOther(False)
        self.updateAttributeInfo()
        if gameglobal.rds.configData.get('enableSpriteFamiV2', False):
            BigWorld.player().base.querySpriteSummonProps(self.currSelectItemSpriteIndex)

    def handleDeourOrLunhuiBtnClick(self, *args):
        e = ASObject(args[3][0])
        isLunhui = e.currentTarget.isLunhui
        if isLunhui:
            self.uiAdapter.summonedWarSpriteLunhui.show(self.currSelectItemSpriteIndex)
        else:
            self.uiAdapter.summonedWarSpriteSwallow.show(self.getCurSelectSpriteInfo())

    def handleRememberBtnClick(self, *args):
        spriteInfo = self.getCurSelectSpriteInfo()
        spriteId = spriteInfo.get('spriteId', 0)
        gameglobal.rds.ui.summonedWarSpriteBiography.setBiographySelectSpriteIndex(spriteId)
        gameglobal.rds.ui.summonedWarSprite.show(uiConst.WAR_SPRITE_TAB_INDEX4)

    def handleCommentBtnClick(self, *args):
        p = BigWorld.player()
        p.showGameMsg(GMDD.data.SPRITE_ERROR_MSG_NONE_COMMEND, ())

    def handleChangeNameBtnClick(self, *args):
        e = ASObject(args[3][0])
        if not self.currSelectItemSpriteIndex:
            return
        spriteInfo = self.getCurSelectSpriteInfo()
        name = spriteInfo.get('name', '')
        gameglobal.rds.ui.summonedWarSpriteRemark.show(self.currSelectItemSpriteIndex, name)

    def handleSpriteRemoveBtnClick(self, *args):
        e = ASObject(args[3][0])
        if not self.currSelectItemSpriteIndex:
            return
        if len(self.warSpriteList) == 1:
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.SUMMONED_WAR_SPRITE_LIMITS, ())
        else:
            gameglobal.rds.ui.summonedWarSpriteRelease.show(self.currSelectItemSpriteIndex)

    def handleSpriteChangeFormBtnClick(self, *args):
        e = ASObject(args[3][0])
        if not self.currSelectItemSpriteIndex:
            return
        if self.headGen:
            if self.isTransform:
                self.isTransform = False
            elif not self.isTransform:
                self.isTransform = True
            self.takePhoto3D()

    @ui.checkInventoryLock()
    def sureRemoveSprite(self, spriteIndex):
        p = BigWorld.player()
        p.base.removeSummonSprite(spriteIndex, p.cipherOfPerson)

    def removeSpriteSucc(self, index = None):
        if index and self.currSelectItemSpriteIndex == index:
            self.currSelectItemSpriteIndex = None
            self.currSelectSpriteNumber = 0
            self.isTransform = False
            gameglobal.rds.ui.summonedWarSprite.saveSpriteIndex(self.currSelectSpriteNumber, self.currSelectItemSpriteIndex)
            gameglobal.rds.ui.summonedWarSprite.hideSubPanel()

    def getSpriteBornPos(self):
        spriteBornPosList = SCD.data.get('spriteBornPosList', [])
        bornPos = (0, 0, 0)
        p = BigWorld.player()
        for posArg in spriteBornPosList:
            pos = utils.getRelativePosition(p.position, p.yaw, posArg[0], posArg[1])
            if flyEffect._checkCollide(p.position, pos):
                continue
            pos = BigWorld.findDropPoint(p.spaceID, Math.Vector3(pos[0], pos[1] + 5.0, pos[2]))
            if pos:
                if abs(pos[0][1] - p.position[1]) > SCD.data.get('spriteBornPosTolerate', 3):
                    continue
                else:
                    return pos[0]

        return bornPos

    def handleSpriteCallBackBtnClick(self, *args):
        e = ASObject(args[3][0])
        if not self.currSelectItemSpriteIndex:
            return
        p = BigWorld.player()
        szLabel = e.currentTarget.label
        if szLabel == gameStrings.SUMMONED_WAR_SPRITE_CALL_BACK:
            p.base.applyDismissSprite()
            self.uiAdapter.summonedWarSprite.hide()
        elif szLabel == gameStrings.SUMMONED_WAR_SPRITE_CALL_OUT:
            self.callOutSprite(self.currSelectItemSpriteIndex)

    def callOutSprite(self, index):
        p = BigWorld.player()
        if index == p.lastSpriteBattleIndex and p.summonedSpriteInWorld:
            p.showGameMsg(GMDD.data.THE_SAME_SPRITE_CANNOT_CALL_OUT_MSG, ())
            return
        bornPos = self.getSpriteBornPos()
        BigWorld.player().base.applySummonSprite(index, bornPos)
        gameglobal.rds.ui.summonedWarSprite.hide()

    def handleSpriteAddExpBtnClick(self, *args):
        e = ASObject(args[3][0])
        self.currShowFeedMc = FEED_EXP_PANEL
        tAddExpList = self.getFeedExpItemList()
        if not tAddExpList:
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.SPRITE_FEED_ERROR_NO_ADD_EXP_ITEM, ())
            gameglobal.rds.ui.help.show(SCD.data.get('DESC_HELP_NO_ADD_SPRITE_EXP_ITEM', gameStrings.DESC_HELP_SPRITE_FEED_DEFAULT))
            return
        self.showFeedSpriteMc(e.target, tAddExpList)

    def handleFeedSpriteBtnClick(self, *args):
        p = BigWorld.player()
        if not self.currSelectFoodItemId:
            p.showGameMsg(GMDD.data.SPRITE_FEED_ERROR_NO_SELECT_ITEM, ())
            return
        if self.currSelectItemSpriteIndex and self.currSelectFoodItemId:
            if self.currShowFeedMc == FEED_HUNGER_PANEL:
                isDiKouItem = self.feedTipsPanel.checkBox.selected
                feedIemNum = self.currSelectFeedItem.itemNum
                price = self.currSelectFeedItem.price * HUNGER_ITEM_NUM_LIMIT
                if feedIemNum >= HUNGER_ITEM_NUM_LIMIT:
                    feedIemNum = HUNGER_ITEM_NUM_LIMIT
                    dikouItemNum = 0
                elif isDiKouItem and p.bindCash + p.cash >= price:
                    feedIemNum = 0
                    dikouItemNum = HUNGER_ITEM_NUM_LIMIT
                else:
                    feedIemNum = 0
                    dikouItemNum = 0
                if isDiKouItem and p.bindCash < price:
                    msg = uiUtils.getTextFromGMD(GMDD.data.BINDCASH_IS_NOT_ENOUGH, '')
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(p.base.feedToAddSpriteHungry, self.currSelectItemSpriteIndex, self.currSelectFoodItemId, feedIemNum, dikouItemNum), msgType='bindCash', isShowCheckBox=True)
                else:
                    p.base.feedToAddSpriteHungry(self.currSelectItemSpriteIndex, self.currSelectFoodItemId, feedIemNum, dikouItemNum)
            elif self.currShowFeedMc == FEED_EXP_PANEL:
                diff = self.checkWeeklyLimits(0, 'expSrcCnt')
                if diff <= 0:
                    p.showGameMsg(GMDD.data.NOT_ENOUGH_SPACE_TO_FEED_EXP, ())
                    return
                cidData = CID.data.get(self.currSelectFoodItemId, {})
                sType = cidData.get('sType', 0)
                spriteExp = cidData.get('spriteExp', 0)
                msg = uiUtils.getTextFromGMD(GMDD.data.SPRITE_FEED_EXP_ERROR_OVER_WEEK_LIMIT, '')
                if sType == Item.SUBTYPE_2_SPRITE_FOOD:
                    count = self.feedTipsPanel.feedMoreMc.counterBtn.count
                    fullExpFoods = self.getFullExpFoodNum()
                    if count >= fullExpFoods and fullExpFoods:
                        count = fullExpFoods
                    if spriteExp * count > diff:
                        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.base.feedSpriteExpWithFood, self.currSelectItemSpriteIndex, [self.currSelectFoodItemId], [count]))
                    else:
                        p.base.feedSpriteExpWithFood(self.currSelectItemSpriteIndex, [self.currSelectFoodItemId], [count])
            elif self.currShowFeedMc == FEED_PRIVITY_PANEL:
                cidData = CID.data.get(self.currSelectFoodItemId, {})
                sType = cidData.get('sType', 0)
                if sType == Item.SUBTYPE_2_SPRITE_FOOD:
                    diff = self.checkWeeklyLimits(1, 'famiSrcCnt')
                    if diff <= 0:
                        p.showGameMsg(GMDD.data.NOT_ENOUGH_SPACE_TO_FEED_FAMI, ())
                        return
                    familiarExp = cidData.get('familiarExp', 0)
                    msg = uiUtils.getTextFromGMD(GMDD.data.SPRITE_FEED_FAMI_ERROR_OVER_WEEK_LIMIT, '')
                    count = self.feedTipsPanel.feedMoreMc.counterBtn.count
                    if familiarExp * count > diff:
                        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.base.feedSpriteExpWithFood, self.currSelectItemSpriteIndex, [self.currSelectFoodItemId], [count]))
                    else:
                        p.base.feedSpriteExpWithFood(self.currSelectItemSpriteIndex, [self.currSelectFoodItemId], [count])
                elif sType == Item.SUBTYPE_2_SPRITE_SPECIAL:
                    p.base.incSpriteLvWithSpecial(self.currSelectItemSpriteIndex, self.currSelectFoodItemId, 1)

    def getFullExpFoodNum(self):
        spriteInfo = self.getCurSelectSpriteInfo()
        props = spriteInfo.get('props', {})
        exp = int(props.get('exp', 0))
        curSpriteLv = props.get('lv', 0)
        maxLvLimit = self.getSpriteMaxLvLimit(props.get('juexing', False))
        allExp = 0
        for spriteLv in xrange(curSpriteLv, maxLvLimit):
            upExp = SSLD.data.get(spriteLv, {}).get('upExp', 0)
            allExp += upExp

        allExpLeft = max(0, allExp - exp)
        spriteExp = CID.data.get(self.currSelectFoodItemId).get('spriteExp', 0)
        count = 0
        if spriteExp:
            count = int(math.ceil(allExpLeft * 1.0 / spriteExp))
        return count

    def checkWeeklyLimits(self, i, szType):
        p = BigWorld.player()
        wLmt = SCD.data.get('spriteWeeklyExpLimits', (0, 0))[i]
        weeklyData = p.summonSpriteList.get(self.currSelectItemSpriteIndex, {}).get('weeklyData', {})
        srcCnt = weeklyData.get(szType, 0)
        diff = max(0, wLmt - srcCnt)
        return diff

    def handleSelectCheckBox(self, *args):
        e = ASObject(args[3][0])
        self.updateFeedBtnState()

    def handlenNextLevelBtnClick(self, *args):
        if not self.currSelectFoodItemId or not self.currSelectItemSpriteIndex:
            return
        p = BigWorld.player()
        spriteInfo = self.getCurSelectSpriteInfo()
        props = spriteInfo.get('props', {})
        cidData = CID.data.get(self.currSelectFoodItemId, {})
        expValue = 0
        count = 0
        if self.currShowFeedMc == FEED_EXP_PANEL:
            spriteLv = int(props.get('lv', 0))
            maxLvLimit = self.getSpriteMaxLvLimit(props.get('juexing', False))
            if maxLvLimit <= spriteLv:
                p.showGameMsg(GMDD.data.SPRITE_FEED_ERROR_OVER_PALYER_LV, ())
                return
            diff = self.checkWeeklyLimits(0, 'expSrcCnt')
            if diff <= 0:
                p.showGameMsg(GMDD.data.NOT_ENOUGH_SPACE_TO_FEED_EXP, ())
                return
            msg = uiUtils.getTextFromGMD(GMDD.data.SPRITE_FEED_EXP_ERROR_OVER_WEEK_LIMIT, '')
            spriteExp = cidData.get('spriteExp', 0)
            if spriteExp:
                curValue = int(props.get('exp', 0))
                maxValue = int(props.get('maxExp', 1))
                count = max(1, int(math.ceil((maxValue - curValue) * 1.0 / spriteExp)))
                expValue = spriteExp
        elif self.currShowFeedMc == FEED_PRIVITY_PANEL:
            diff = self.checkWeeklyLimits(1, 'famiSrcCnt')
            if diff <= 0:
                p.showGameMsg(GMDD.data.NOT_ENOUGH_SPACE_TO_FEED_FAMI, ())
                return
            msg = uiUtils.getTextFromGMD(GMDD.data.SPRITE_FEED_FAMI_ERROR_OVER_WEEK_LIMIT, '')
            familiarExp = cidData.get('familiarExp', 0)
            if familiarExp:
                curValue = int(props.get('famiExp', 0))
                maxValue = int(props.get('famiMaxExp', 1))
                count = max(0, int(math.ceil((maxValue - curValue) * 1.0 / familiarExp)))
                expValue = familiarExp
        p = BigWorld.player()
        itemNum = p.inv.countItemInPages(uiUtils.getParentId(self.currSelectFoodItemId), enableParentCheck=True)
        if itemNum < count:
            count = itemNum
        sType = cidData.get('sType', 0)
        if sType == Item.SUBTYPE_2_SPRITE_FOOD and count:
            if expValue * count > diff:
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.base.feedSpriteExpWithFood, self.currSelectItemSpriteIndex, [self.currSelectFoodItemId], [count]))
            else:
                p.base.feedSpriteExpWithFood(self.currSelectItemSpriteIndex, [self.currSelectFoodItemId], [count])

    def handleCancelFeedSpriteBtnClick(self, *args):
        if self.widget:
            MenuManager.getInstance().hideMenu()

    def handleFeedSlotClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        if self.currSelectFeedItem:
            self.currSelectFeedItem.selected = False
        target.selected = True
        self.currSelectFeedItem = target
        self.currSelectFoodItemId = target.foodItemId
        self.updateFeedMoreFoodMc()

    def handleSpriteAddPrivityBtnClick(self, *args):
        e = ASObject(args[3][0])
        self.currShowFeedMc = FEED_PRIVITY_PANEL
        tAddPrivityList = self.getFeedFamiItemList()
        if not tAddPrivityList:
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.SPRITE_FEED_ERROR_NO_ADD_PRIVITY_ITEM, ())
            gameglobal.rds.ui.help.show(SCD.data.get('DESC_HELP_NO_ADD_SPRITE_PRIVITY_ITEM', gameStrings.DESC_HELP_SPRITE_FEED_DEFAULT))
            return
        self.showFeedSpriteMc(e.target, tAddPrivityList)

    def handleHungerBtnClick(self, *args):
        e = ASObject(args[3][0])
        self.currShowFeedMc = FEED_HUNGER_PANEL
        tHungerList = self.getFeedHungerItemList()
        if not tHungerList:
            return
        self.showFeedSpriteMc(e.target, tHungerList)

    def handleFamiliarBtnClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        if target.disabled:
            return
        gameglobal.rds.ui.summonedWarSpriteFamiliar.show(self.currSelectItemSpriteIndex)

    def handleChatBtnClick(self, *args):
        if not self.currSelectItemSpriteIndex:
            return
        gameglobal.rds.ui.summonedWarSpriteChat.show(self.currSelectItemSpriteIndex)

    @ui.callFilter(SCD.data.get('spriteActionGcd', 1))
    def handlePhotoAreaClick(self, *args):
        e = ASObject(args[3][0])
        self.playSoundAndAction('spriteSoundList2', 'spriteActionList2', 'spriteActionPro2')

    def playSoundAndAction(self, spriteSoundList, spriteActionList, spriteActionPro):
        if not self.currSelectItemSpriteIndex:
            return
        spriteInfo = self.getCurSelectSpriteInfo()
        spriteId = spriteInfo.get('spriteId', 0)
        spriteSoundList = SSID.data.get(spriteId, {}).get(spriteSoundList, [])
        spriteActionList = SSID.data.get(spriteId, {}).get(spriteActionList, [])
        spriteActionPro = SSID.data.get(spriteId, {}).get(spriteActionPro, [])
        if spriteActionPro:
            choice = commcalc.weightingChoiceIndex(spriteActionPro)
        else:
            choice = random.randint(0, max(len(spriteActionList) - 1, 0))
        if spriteActionList and choice < len(spriteActionList):
            action = spriteActionList[choice]
            model = self.headGen.adaptor.attachment
            try:
                aq = model.action(action)()
                getattr(aq, '1101')()
            except:
                pass

        if spriteSoundList and choice < len(spriteSoundList):
            soundId = spriteSoundList[choice]
            gameglobal.rds.sound.playSound(soundId)

    def getSpriteMaxLvLimit(self, juexing):
        p = BigWorld.player()
        if not juexing:
            return p.lv
        return p.lv + SCD.data.get('spriteLvExceedIfJuexing', 0)

    def showFeedSpriteMc(self, target, tDataList):
        if not self.widget:
            return
        else:
            self.currSelectFeedItem = None
            self.currSelectFoodItemId = None
            self.feedTipsPanel = self.widget.getInstByClsName('SummonedWarSpriteMine_feedSprite')
            self.feedTipsPanel.feedScrollWndList.itemHeight = 65
            self.feedTipsPanel.feedScrollWndList.itemRenderer = 'SummonedWarSpriteMine_feedItem'
            self.feedTipsPanel.feedScrollWndList.dataArray = tDataList
            self.feedTipsPanel.feedScrollWndList.lableFunction = self.feedItemFunction
            if self.currShowFeedMc == FEED_HUNGER_PANEL:
                self.feedTipsPanel.feedHelp.visible = False
                self.feedTipsPanel.checkBox.selected = True
                self.feedTipsPanel.checkBox.visible = True
                self.feedTipsPanel.checkBox.label = GMD.data.get(GMDD.data.SPRITE_HUNGER_FEED_CHECK_LABEL, {}).get('text', '')
                self.feedTipsPanel.feedMoreMc.visible = False
                self.feedTipsPanel.checkBox.addEventListener(events.MOUSE_CLICK, self.handleSelectCheckBox, False, 0, True)
            else:
                expKey, famiKey = SCD.data.get('spriteFeedPanelHelpKeys', (0, 0))
                self.feedTipsPanel.feedHelp.helpKey = expKey if self.currShowFeedMc == FEED_EXP_PANEL else famiKey
                self.feedTipsPanel.feedHelp.visible = True
                self.feedTipsPanel.checkBox.visible = False
                self.feedTipsPanel.feedMoreMc.visible = True
                self.feedTipsPanel.feedMoreMc.nextLevelBtn.addEventListener(events.BUTTON_CLICK, self.handlenNextLevelBtnClick, False, 0, True)
            self.feedTipsPanel.feedBtn.addEventListener(events.BUTTON_CLICK, self.handleFeedSpriteBtnClick, False, 0, True)
            self.feedTipsPanel.feedCancelBtn.addEventListener(events.BUTTON_CLICK, self.handleCancelFeedSpriteBtnClick, False, 0, True)
            menuParent = self.widget.mineWarSpritePanel.overviewMc
            MenuManager.getInstance().showMenu(target, self.feedTipsPanel, {'x': 341,
             'y': 26}, False, menuParent)
            return

    def getSelectedSubProxy(self):
        return self.subProxys.get(self.selectTabBtnName)

    def refreshInfo(self):
        if not self.widget:
            return
        self.updateLeftWarSpritesMc()
        self.getSelectedSubProxy().refreshWidget()

    def refreshWidget(self):
        self.updateFeedMc()

    def updateFeedMc(self):
        if self.feedTipsPanel and self.feedTipsPanel.stage:
            if self.currShowFeedMc == FEED_EXP_PANEL:
                tAddExpList = self.getFeedExpItemList()
                self.feedTipsPanel.feedScrollWndList.dataArray = tAddExpList
            elif self.currShowFeedMc == FEED_PRIVITY_PANEL:
                tAddPrivityList = self.getFeedFamiItemList()
                self.feedTipsPanel.feedScrollWndList.dataArray = tAddPrivityList
            elif self.currShowFeedMc == FEED_HUNGER_PANEL:
                tHungerList = self.getFeedHungerItemList()
                self.feedTipsPanel.feedScrollWndList.dataArray = tHungerList

    def updateFeedBtnState(self):
        spriteInfo = self.getCurSelectSpriteInfo()
        props = spriteInfo.get('props', {})
        curHungerVal = int(props.get('hungry', 0))
        val0, val1, val2, val3 = SCD.data.get('spriteHungryThresholds', ())
        self.feedTipsPanel.feedBtn.disabled = False
        TipManager.removeTip(self.feedTipsPanel.feedBtn)
        if curHungerVal >= val3:
            self.feedTipsPanel.feedBtn.disabled = True
            tipMsg = GMD.data.get(GMDD.data.SPRITE_HUNGER_FEED_FULL_TIP, {}).get('text', '')
            TipManager.addTip(self.feedTipsPanel.feedBtn, tipMsg)
        else:
            p = BigWorld.player()
            itemNum = p.inv.countItemInPages(uiUtils.getParentId(self.currSelectFoodItemId), enableParentCheck=True)
            isDiKouItem = self.feedTipsPanel.checkBox.selected
            if itemNum <= 0 and not isDiKouItem:
                self.feedTipsPanel.feedBtn.disabled = True
                TipManager.addTip(self.feedTipsPanel.feedBtn, gameStrings.SPRITE_FOOD_NUM_LIMIT)

    def updateFeedMoreFoodMc(self):
        if not self.feedTipsPanel:
            return
        feedMoreMc = self.feedTipsPanel.feedMoreMc
        if not self.currSelectFoodItemId:
            feedMoreMc.visible = False
            return
        if self.currShowFeedMc == FEED_HUNGER_PANEL:
            self.updateFeedBtnState()
            return
        p = BigWorld.player()
        itemNum = p.inv.countItemInPages(uiUtils.getParentId(self.currSelectFoodItemId), enableParentCheck=True)
        upMode = 0
        spriteInfo = self.getCurSelectSpriteInfo()
        props = spriteInfo.get('props', {})
        if self.currShowFeedMc == FEED_EXP_PANEL:
            lv = int(props.get('lv', 0))
            upMode = SSLD.data.get(lv, {}).get('upMode', 0)
        elif self.currShowFeedMc == FEED_PRIVITY_PANEL:
            familiar = int(props.get('familiar', 0))
            upMode = SSFD.data.get(familiar, {}).get('upMode', 0)
        sType = CID.data.get(self.currSelectFoodItemId, {}).get('sType', 0)
        if sType == Item.SUBTYPE_2_SPRITE_FOOD and itemNum > 0:
            feedMoreMc.visible = True
            self.feedTipsPanel.feedMoreMc.counterBtn.minCount = 1
            self.feedTipsPanel.feedMoreMc.counterBtn.maxCount = max(1, itemNum)
            self.feedTipsPanel.feedMoreMc.counterBtn.count = 1
            self.feedTipsPanel.feedMoreMc.nextLevelBtn.disabled = True if upMode else False
        else:
            feedMoreMc.visible = False
        TipManager.removeTip(self.feedTipsPanel.feedBtn)
        if upMode:
            self.feedTipsPanel.feedBtn.disabled = True
            TipManager.addTip(self.feedTipsPanel.feedBtn, gameStrings.SPRITE_LEVEL_LIMITED)
        else:
            self.feedTipsPanel.feedBtn.disabled = True if itemNum <= 0 else False
            if itemNum <= 0:
                TipManager.addTip(self.feedTipsPanel.feedBtn, gameStrings.SPRITE_FOOD_NUM_LIMIT)

    def handleItemMcClick(self, *args):
        self.uiAdapter.itemSourceInfor.openPanel()

    def feedItemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.addEventListener(events.MOUSE_DOWN, self.handleFeedSlotClick, False, 0, True)
        itemMc.validateNow()
        itemMc.mouseChildren = True
        itemMc.foodItemId = itemData.foodItemId
        itemMc.itemNum = itemData.itemNum
        itemMc.price = getattr(itemData, 'price', 0)
        idData = ID.data.get(itemData.foodItemId, {})
        name = idData.get('name', '')
        desc = idData.get('funcDesc', '')
        itemMc.labels = [name, desc]
        itemMc.itemSlot.slot.dragable = False
        itemMc.itemSlot.slot.setItemSlotData(uiUtils.getGfxItemById(itemData.foodItemId, itemData.itemNum))
        itemMc.itemSlot.slot.validateNow()
        if not itemData.itemNum:
            count = uiUtils.toHtml(itemData.itemNum, '#FF0000')
            itemMc.itemSlot.slot.setValueAmountTxt(count)
            itemMc.disabled = True
            itemMc.itemSlot.slot.setSlotState(uiConst.COMPLETE_ITEM_LEAKED)
            itemMc.itemSlot.slot.addEventListener(events.MOUSE_DOWN, self.handleItemMcClick, False, 0, True)
        else:
            itemMc.disabled = False
            itemMc.itemSlot.slot.setSlotState(uiConst.ITEM_NORMAL)
            itemMc.itemSlot.slot.removeEventListener(events.MOUSE_DOWN, self.handleItemMcClick)
        TipManager.addItemTipById(itemMc, itemData.foodItemId)
        itemMc.selected = False
        if self.currSelectFoodItemId and self.currSelectFoodItemId == itemMc.foodItemId:
            itemMc.selected = True
        elif not self.currSelectFoodItemId:
            itemMc.selected = True
        if itemMc.selected:
            self.currSelectFoodItemId = itemData.foodItemId
            self.currSelectFeedItem = itemMc
            self.updateFeedMoreFoodMc()

    def getFeedExpItemList(self):
        tExpList = []
        p = BigWorld.player()
        for id in SCD.data.get('spriteExpFoodList', []):
            itemNum = p.inv.countItemInPages(uiUtils.getParentId(id), enableParentCheck=True)
            tExpList.append({'foodItemId': id,
             'itemNum': itemNum})

        return tExpList

    def getFeedFamiItemList(self):
        tFamList = []
        p = BigWorld.player()
        for id in SCD.data.get('spriteFamiliarFoodList', []):
            itemNum = p.inv.countItemInPages(uiUtils.getParentId(id), enableParentCheck=True)
            tFamList.append({'foodItemId': id,
             'itemNum': itemNum})

        return tFamList

    def getFeedHungerItemList(self):
        tHungetList = []
        p = BigWorld.player()
        for id, price, hungerVal in SCD.data.get('spriteHungryItems', []):
            itemNum = p.inv.countItemInPages(uiUtils.getParentId(id), enableParentCheck=True)
            tHungetList.append({'foodItemId': id,
             'itemNum': itemNum,
             'price': price})

        return tHungetList

    def handleSelectWarSpriteType(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if itemMc.selectedIndex != -1:
            self.updateWarSpritesTypeList(itemMc.selectedIndex)

    def initLeftWarSpritesMc(self):
        warSpritesMc = self.widget.mineWarSpritePanel.warSpritesMc
        warSpritesMc.spriteList.itemHeight = 65
        warSpritesMc.spriteList.itemRenderer = 'SummonedWarSpriteMine_LeftItem'
        warSpritesMc.spriteList.barAlwaysVisible = True
        warSpritesMc.spriteList.dataArray = []
        warSpritesMc.spriteList.lableFunction = self.itemFunction
        warSpritesMc.spriteTypeDropdown.addEventListener(events.INDEX_CHANGE, self.handleSelectWarSpriteType, False, 0, True)
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

    def updateLeftWarSpritesMc(self):
        warSpritesMc = self.widget.mineWarSpritePanel.warSpritesMc
        p = BigWorld.player()
        spriteNumLimit = p.spriteExtraDict['spriteSlotNum']
        warSpritesMc.holdSpritesText.text = '%d/%d' % (len(p.summonSpriteList), spriteNumLimit)
        self.updateWarSpritesTypeList(warSpritesMc.spriteTypeDropdown.selectedIndex)

    def sortWarSpriteList(self, typeIndex):
        p = BigWorld.player()
        if typeIndex == SORT_TYPE_FAMIEFFLV:

            def sortFamiEffLv(spriteData1, spriteData2):
                if spriteData1['props']['famiEffLv'] != spriteData2['props']['famiEffLv']:
                    return spriteData1['props']['famiEffLv'] - spriteData2['props']['famiEffLv']
                if spriteData1['props']['lv'] != spriteData2['props']['lv']:
                    return spriteData1['props']['lv'] - spriteData2['props']['lv']
                return self.longNumsCompare(spriteData1['props']['exp'], spriteData2['props']['exp'])

            return sorted(p.summonSpriteList.values(), cmp=sortFamiEffLv, reverse=True)
        elif typeIndex == SORT_TYPE_LV:
            return sorted(p.summonSpriteList.values(), key=lambda d: d['props']['lv'], reverse=True)
        else:
            return sorted(p.summonSpriteList.values(), key=lambda d: d['props']['vPropCache'][typeIndex - 2], reverse=True)

    def sortOtherSpriteList(self, data, typeIndex):
        if typeIndex == SORT_TYPE_FAMIEFFLV:

            def sortFamiEffLv(spriteData1, spriteData2):
                if spriteData1[const.SPRITE_DICT_INDEX_famiEffLv] != spriteData2[const.SPRITE_DICT_INDEX_famiEffLv]:
                    return spriteData1[const.SPRITE_DICT_INDEX_famiEffLv] > spriteData2[const.SPRITE_DICT_INDEX_famiEffLv]
                return spriteData1[const.SPRITE_DICT_INDEX_lv] > spriteData2[const.SPRITE_DICT_INDEX_lv]

            return sorted(data.values(), cmp=sortFamiEffLv)
        elif typeIndex == SORT_TYPE_LV:
            return sorted(data.values(), key=lambda d: d[const.SPRITE_DICT_INDEX_lv], reverse=True)
        else:
            return sorted(data.values(), key=lambda d: d[const.SPRITE_DICT_INDEX_vPropCache][typeIndex - 2], reverse=True)

    def getSpriteItemInfoList(self, warSpriteList, typeIndex, showSortDetailInfo = False):
        p = BigWorld.player()
        spriteItemList = list()
        for i in xrange(len(warSpriteList)):
            spriteInfo = warSpriteList[i]
            props = spriteInfo.get('props', {})
            itemInfo = dict()
            itemInfo['numberId'] = i
            itemInfo['warSpriteIndex'] = spriteInfo.get('index', 0)
            itemInfo['spriteId'] = spriteInfo.get('spriteId', 0)
            itemInfo['name'] = spriteInfo.get('name', '')
            itemInfo['showFamiliar'] = False
            itemInfo['famiExp'] = props.get('famiExp', 0)
            itemInfo['famiMaxExp'] = props.get('famiMaxExp', 1)
            itemInfo['familiar'] = props.get('familiar', 0)
            itemInfo['famiEffAdd'] = props.get('famiEffAdd', 0)
            itemInfo['famiEffLv'] = props.get('famiEffLv', 0)
            szLv = 'lv %s' % str(props.get('lv', 0))
            propsText = szLv
            if showSortDetailInfo:
                if typeIndex == SORT_TYPE_FAMIEFFLV:
                    itemInfo['showFamiliar'] = True
                elif typeIndex == SORT_TYPE_LV:
                    pass
                else:
                    value = spriteInfo['props']['vPropCache'][typeIndex - 2]
                    otherP = '%s %s' % (self.typeToSort[typeIndex], str(value))
                    propsText = '%s %s' % (szLv, otherP)
            itemInfo['lv'] = propsText
            itemInfo['life'] = True
            if p.summonedSpriteLifeList and itemInfo['warSpriteIndex'] in p.summonedSpriteLifeList or p.spriteBattleCallBackList and itemInfo['warSpriteIndex'] in p.spriteBattleCallBackList:
                itemInfo['life'] = False
            itemInfo['beReadyFight'] = gameglobal.rds.ui.summonedWarSpriteFight.checkSpriteReadyFightState(spriteInfo.get('index', 0))
            itemInfo['isShowUnlockSlot'] = False
            spriteItemList.append(itemInfo)

        return spriteItemList

    def updateWarSpritesTypeList(self, typeIndex):
        p = BigWorld.player()
        self.warSpriteList = self.sortWarSpriteList(typeIndex)
        self.spriteItemList = self.getSpriteItemInfoList(self.warSpriteList, typeIndex, showSortDetailInfo=True)
        if gameglobal.rds.configData.get('enableExpandSpriteSlot', False) and p.spriteExtraDict['spriteSlotNum'] < SCD.data.get('spriteSlotLimit', 30):
            self.spriteItemList.append({'isShowUnlockSlot': True})
        self.widget.mineWarSpritePanel.warSpritesMc.spriteList.dataArray = self.spriteItemList
        self.widget.mineWarSpritePanel.warSpritesMc.spriteList.validateNow()
        spriteNumber = self.getSpriteNumber()
        pos = self.widget.mineWarSpritePanel.warSpritesMc.spriteList.getIndexPosY(spriteNumber)
        self.widget.mineWarSpritePanel.warSpritesMc.spriteList.scrollTo(pos)

    def getSpriteNumber(self):
        if not self.currSelectItemSpriteIndex:
            return 0
        number = 0
        for teamInfo in self.spriteItemList:
            if self.currSelectItemSpriteIndex == teamInfo.get('warSpriteIndex', 0):
                return number
            number += 1

        return number

    def updateSpriteLifeState(self):
        if not self.widget:
            return
        p = BigWorld.player()
        for itemInfo in self.spriteItemList:
            if itemInfo.get('warSpriteIndex', 0):
                itemInfo['life'] = True
                if p.summonedSpriteLifeList and itemInfo['warSpriteIndex'] in p.summonedSpriteLifeList or p.spriteBattleCallBackList and itemInfo['warSpriteIndex'] in p.spriteBattleCallBackList:
                    itemInfo['life'] = False

        self.widget.mineWarSpritePanel.warSpritesMc.spriteList.dataArray = self.spriteItemList

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        self._setSpriteMCData(itemData, itemMc)

    def _setSpriteMCData(self, itemData, spriteHeadMc):
        spriteHeadMc.data = itemData
        if itemData.isShowUnlockSlot:
            spriteHeadMc.unlockItem.visible = True
            spriteHeadMc.headItem.vislible = False
            spriteHeadMc.unlockItem.addEventListener(events.MOUSE_DOWN, self.handleUnlockItem, False, 0, True)
            return
        spriteHeadMc.unlockItem.visible = False
        spriteHeadMc.headItem.vislible = True
        itemMc = spriteHeadMc.headItem
        itemMc.addEventListener(events.MOUSE_DOWN, self.updateTabBtnAndMc, False, 0, True)
        itemMc.numberId = itemData.numberId
        itemMc.warSpriteIndex = itemData.warSpriteIndex
        itemMc.szName = itemData.name
        itemMc.szLv = itemData.lv
        itemMc.labels = [itemMc.szName, itemMc.szLv]
        self.setFamiliarMc(itemMc.familiarMc, itemData.showFamiliar, float(itemData.familiar), float(itemData.famiEffAdd), float(itemData.famiEffLv))
        iconId = SSID.data.get(itemData.spriteId, {}).get('spriteIcon', '000')
        iconPath = SPRITE_ICON_PATH % str(iconId)
        itemMc.itemSlot.slot.setItemSlotData({'iconPath': iconPath})
        itemMc.readyFight.visible = itemData.beReadyFight
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
        itemMc.disabled = not itemData.life
        itemMc.dieIcon.visible = not itemData.life
        itemMc.selected = False
        if self.currSelectItemSpriteIndex and self.currSelectItemSpriteIndex == itemData.warSpriteIndex:
            itemMc.selected = True
        elif not self.currSelectItemSpriteIndex and itemData.numberId == 0:
            itemMc.selected = True
        if itemMc.enabled and itemMc.selected:
            self.currSelectItem = itemMc
            self.currSelectSpriteNumber = itemData.numberId
            self.currSelectItemSpriteIndex = itemData.warSpriteIndex
            self.updateTabBtnState()
            self.getSpritePropList(self.currSelectItemSpriteIndex)
            gameglobal.rds.ui.summonedWarSprite.saveSpriteIndex(itemData.numberId, itemData.warSpriteIndex)
            self.updateChangeSkinBtnRedPot()
        itemMc.itemSlot.slot.binding = 'summonedWarSprite.%s.%s' % (itemData.warSpriteIndex, itemData.spriteId)
        itemMc.validateNow()
        itemMc.mouseChildren = True
        itemMc.itemSlot.slot.validateNow()
        TipManager.addTipByType(itemMc.itemSlot.slot, tipUtils.TYPE_SPRITE_HEAD_TIP, (itemData.warSpriteIndex,), False, 'upLeft')
        RedPotManager.removeRedPotById(itemMc.warSpriteIndex * 1000)
        RedPotManager.addRedPot(itemMc, itemMc.warSpriteIndex * 1000, (itemMc.itemSlot.width + 1, 1), self.visiblePotFunSpriteItem, itemMc.warSpriteIndex)

    @ui.checkInventoryLock()
    def handleUnlockItem(self, *args):
        p = BigWorld.player()
        curSlotNum = p.spriteExtraDict['spriteSlotNum']
        nextSlotNum = curSlotNum + 1
        yunchuiCost = SCD.data.get('expandSpriteSlotCost', {}).get(nextSlotNum, 0)
        msg = uiUtils.getTextFromGMD(GMDD.data.SPRITE_UNLOCK_HEAD_SLOT_DESC, '%d-%d') % (yunchuiCost, nextSlotNum)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.base.expandSpriteSlot, p.cipherOfPerson))

    def visibleItemRedPoint(self, spriteIndex):
        return gameglobal.rds.ui.summonedWarSpriteAwake.checkRedPoint(spriteIndex) or self.changeSkinProxy.checkSkinBtnRedPoint(spriteIndex) or self.changeSkinProxy.checkDustBtnRedPoint(spriteIndex)

    def visiblePotFunSpriteItem(self, *args):
        spriteIndex = int(args[3][0].GetNumber())
        if spriteIndex:
            return GfxValue(self.visibleItemRedPoint(spriteIndex))
        return GfxValue(False)

    def updateSpriteItemRedPot(self):
        if not self.currSelectItemSpriteIndex:
            return
        RedPotManager.updateRedPot(self.currSelectItemSpriteIndex * 1000)

    def getSpritePropList(self, index, force = False):
        if index:
            if not BigWorld.player().summonSpriteProps.get(index) or force:
                BigWorld.player().base.getSpritePropList(index)

    def updateTabBtnAndMc(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        self.handleSpriteItemClick(itemMc)
        if not itemMc.enabled:
            return
        if self.currSelectItemSpriteIndex and self.currSelectItemSpriteIndex == itemMc.warSpriteIndex:
            return
        if self.currSelectItem:
            self.currSelectItem.selected = False
        self.isTransform = False
        self.changeSkinProxy.reset()
        itemMc.selected = True
        self.currSelectItem = itemMc
        self.currSelectSpriteNumber = itemMc.numberId
        self.currSelectItemSpriteIndex = itemMc.warSpriteIndex
        self.updateTabBtnState()
        self.getSpritePropList(self.currSelectItemSpriteIndex)
        gameglobal.rds.ui.summonedWarSprite.saveSpriteIndex(itemMc.numberId, itemMc.warSpriteIndex)
        gameglobal.rds.ui.summonedWarSprite.hideSubPanel()
        self.updateChangeSkinBtnRedPot()

    def updateTabBtnState(self):
        for i, btnName in enumerate(m_tTabBtnList):
            btnMc = self.widget.mineWarSpritePanel.getChildByName(btnName)
            btnMc.fixedSize = True
            panelMc = self.widget.mineWarSpritePanel.getChildByName(m_tTabBtnList[btnName])
            if btnName == self.selectTabBtnName:
                btnMc.selected = True
                if panelMc:
                    panelMc.visible = True
                    self.updateSelectTabMc(panelMc)
            else:
                btnMc.selected = False
                if panelMc:
                    panelMc.visible = False

    def updateSelectTabMc(self, panelMc):
        if panelMc.name == 'overviewMc':
            self.updateOverviewMc()
        elif panelMc.name == 'attributeMc':
            self.propertyProxy.refreshWidget()
        elif panelMc.name == 'skillMc':
            self.skillProxy.refreshWidget()
        else:
            self.changeSkinProxy.refreshWidget()

    def initOverviewMc(self):
        overviewMc = self.widget.mineWarSpritePanel.overviewMc
        overviewMc.overview_changeName.addEventListener(events.BUTTON_CLICK, self.handleChangeNameBtnClick, False, 0, True)
        overviewMc.overview_spriteRemove.addEventListener(events.BUTTON_CLICK, self.handleSpriteRemoveBtnClick, False, 0, True)
        overviewMc.overview_changeForm.addEventListener(events.BUTTON_CLICK, self.handleSpriteChangeFormBtnClick, False, 0, True)
        overviewMc.overview_callBackBtn.addEventListener(events.BUTTON_CLICK, self.handleSpriteCallBackBtnClick, False, 0, True)
        overviewMc.overview_spriteAddExp.addEventListener(events.BUTTON_CLICK, self.handleSpriteAddExpBtnClick, False, 0, True)
        overviewMc.overview_spriteAddPrivity.addEventListener(events.BUTTON_CLICK, self.handleSpriteAddPrivityBtnClick, False, 0, True)
        overviewMc.overview_photo.addEventListener(events.MOUSE_CLICK, self.handlePhotoAreaClick, False, 0, True)
        overviewMc.familiarBtn.addEventListener(events.MOUSE_CLICK, self.handleFamiliarBtnClick, False, 0, True)
        overviewMc.chatBtn.addEventListener(events.MOUSE_CLICK, self.handleChatBtnClick, False, 0, True)
        overviewMc.aWakeBtn.addEventListener(events.BUTTON_CLICK, self.handleAWakeBtnClick, False, 0, True)
        overviewMc.rareTransferBtn.addEventListener(events.BUTTON_CLICK, self.handleRareTransferBtnClick, False, 0, True)
        overviewMc.upGradeBtn.addEventListener(events.BUTTON_CLICK, self.handleUpGradeBtnClick, False, 0, True)
        overviewMc.readyBtn.addEventListener(events.BUTTON_CLICK, self.handleReadyBtnClick, False, 0, True)
        overviewMc.xiuLianBtn.addEventListener(events.BUTTON_CLICK, self.handleXiuLianBtnClick, False, 0, True)
        overviewMc.mainAttrBtn.addEventListener(events.BUTTON_CLICK, self.handleMainAttrBtnClick, False, 0, True)
        overviewMc.fightAttrBtn.visible = gameglobal.rds.configData.get('enableSpriteFamiV2', False)
        overviewMc.fightAttrBtn.addEventListener(events.BUTTON_CLICK, self.handleFightAttrBtnClick, False, 0, True)
        TipManager.addTip(overviewMc.overview_changeName, SCD.data.get('spriteChangeNameTip', ''))
        TipManager.addTip(overviewMc.attrTitleTxt, SCD.data.get('spriteAttrTitleTip', 'spriteAttrTitleTip'), tipUtils.TYPE_DEFAULT_BLACK)
        TipManager.addTip(overviewMc.overview_changeForm, SCD.data.get('spriteTransformBtnTip', ''))
        TipManager.addTip(overviewMc.overview_spriteAddExp, SCD.data.get('spriteAddExpBtnTip', ''))
        TipManager.addTip(overviewMc.overview_spriteAddPrivity, SCD.data.get('spriteAddPrivityBtnTip', ''))
        TipManager.addTip(overviewMc.chatBtn, gameStrings.SUMMONED_WAR_SPRITE_CHAT_TIP)
        overviewMc.familiarBtn.visible = gameglobal.rds.configData.get('enableSummonedWarSpriteFamiliar', False)
        overviewMc.chatBtn.visible = gameglobal.rds.configData.get('enableSummonedWarSpriteChat', False)
        overviewMc.xiuLianBtn.visible = gameglobal.rds.configData.get('enableSummonedWarSpriteEffect', False) and gameglobal.rds.ui.summonedWarSprite.checkXiuLianLvAndJinejie()
        if gameglobal.rds.configData.get('enableSpriteAutoCallOut', False):
            overviewMc.readyBtn.visible = True
            overviewMc.overview_callBackBtn.x = 399
        else:
            overviewMc.readyBtn.visible = False
            overviewMc.overview_callBackBtn.x = 443
        RedPotManager.addRedPot(overviewMc.aWakeBtn, uiConst.SUMMONED_WAR_SPRITE_AWAKE_RED_POT, (58, -3), self.visiblePotFunAwake)
        overviewMc.fightAttrHelpMc.visible = gameglobal.rds.configData.get('enableSpriteFamiV2', False)
        overviewMc.fightAttrHelpMc.helpKey = SCD.data.get('spriteFightAttrHelpId', 0)

    def checkUpGradeBtnVisible(self):
        spriteInfo = self.getCurSelectSpriteInfo()
        spriteId = spriteInfo.get('spriteId', 0)
        grade = spriteInfo.get('upgradeStage', 0)
        return (spriteId, grade) in SUD.data and gameglobal.rds.configData.get('enableSpriteUpgrade', False)

    def visiblePotFunAwake(self, *args):
        isRedPot = gameglobal.rds.ui.summonedWarSpriteAwake.checkRedPoint(self.currSelectItemSpriteIndex)
        return GfxValue(isRedPot)

    def updateAwakeBtnRedPot(self):
        RedPotManager.updateRedPot(uiConst.SUMMONED_WAR_SPRITE_AWAKE_RED_POT)

    def updateOverviewMc(self):
        p = BigWorld.player()
        p.base.updateClientExpFamiliar(self.currSelectItemSpriteIndex)
        self.updateAwakeBtnRedPot()
        self.updateCallBackBtnLabel()
        self.updateCallBackBtnState()
        self.updateSpriteExpBar()
        self.updateSpritePrivityBar()
        self.updateSpriteOhterInfo()
        self.updateSpritePhoto3D()
        self.updateSpriteSkill()
        self.updateAttributeInfoOther(True)
        self.updateAttributeInfo()
        self.updateSpriteHunger()
        if self.isGotoAddPrivity:
            overviewMc = self.widget.mineWarSpritePanel.overviewMc
            ASUtils.DispatchButtonEvent(overviewMc.overview_spriteAddPrivity)
            self.isGotoAddPrivity = False
        self.setOverViewTemplateState()

    def setOverViewTemplateState(self):
        p = BigWorld.player()
        if p.isUsingTemp():
            overviewMc = self.widget.mineWarSpritePanel.overviewMc
            overviewMc.upGradeBtn.visible = False
            overviewMc.lunhuiBtn.visible = False
            overviewMc.aWakeBtn.visible = False
            overviewMc.overview_spriteAddPrivity.visible = False
            overviewMc.overview_spriteAddExp.visible = False
            overviewMc.hungerBtn.visible = False
            overviewMc.familiarBtn.visible = False
            overviewMc.rareTransferBtn.visible = False
            overviewMc.overview_changeName.visible = False
            overviewMc.chatBtn.visible = False
            overviewMc.overview_spriteRemove.visible = False

    def updateCallBackBtnState(self):
        if not self.widget:
            return
        p = BigWorld.player()
        callBackBtn = self.widget.mineWarSpritePanel.overviewMc.overview_callBackBtn
        callBackBtn.enabled = True
        TipManager.removeTip(callBackBtn)
        if self.currSelectItemSpriteIndex in p.summonedSpriteLifeList or self.currSelectItemSpriteIndex in p.spriteBattleCallBackList:
            callBackBtn.enabled = False

    def updateCallBackBtnLabel(self):
        if not self.widget:
            return
        overviewMc = self.widget.mineWarSpritePanel.overviewMc
        if utils.getSpriteBattleState(self.currSelectItemSpriteIndex):
            overviewMc.overview_callBackBtn.label = gameStrings.SUMMONED_WAR_SPRITE_CALL_BACK
        else:
            overviewMc.overview_callBackBtn.label = gameStrings.SUMMONED_WAR_SPRITE_CALL_OUT

    def updateSpriteOhterInfo(self):
        overviewMc = self.widget.mineWarSpritePanel.overviewMc
        spriteInfo = self.getCurSelectSpriteInfo()
        spriteId = spriteInfo.get('spriteId', 0)
        rareLv = spriteInfo.get('rareLv', 0)
        spriteData = SSID.data.get(spriteId, {})
        self.updateSpriteBattleBigState()
        overviewMc.overview_spriteName.htmlText = spriteInfo.get('name', '')
        attackType = spriteData.get('atkType', 0)
        tipMsg = ''
        if attackType == 1:
            overviewMc.overview_attackType1.gotoAndStop('nearWar')
            tipMsg = SCD.data.get('spriteNearWarTip', '')
        elif attackType == 2:
            overviewMc.overview_attackType1.gotoAndStop('farWar')
            tipMsg = SCD.data.get('spriteFarWarTip', '')
        elif attackType == 3:
            overviewMc.overview_attackType1.gotoAndStop('magic')
            tipMsg = SCD.data.get('spriteMagicTip', '')
        elif attackType == 4:
            overviewMc.overview_attackType1.gotoAndStop('nearMagic')
            tipMsg = SCD.data.get('spriteNearMagicTip', '')
        tipMsg = tipMsg + spriteData.get('spriteTypeLabel', '')
        TipManager.addTip(overviewMc.overview_attackType1, tipMsg)
        overviewMc.attributeScoreText.text = int(spriteInfo['combatScore'])
        TipManager.addTip(overviewMc.attributeScoreText, SCD.data.get('spriteScoreTip'), tipUtils.TYPE_DEFAULT_BLACK)
        TipManager.addTip(overviewMc.attributeScoreTextField, SCD.data.get('spriteScoreTip'), tipUtils.TYPE_DEFAULT_BLACK)
        overviewMc.rareIcon.visible = rareLv
        if overviewMc.rareIcon.visible:
            overviewMc.rareIcon.gotoAndStop('type' + str(rareLv))
        p = BigWorld.player()
        if p.summonSpriteSkin.has_key(spriteId):
            skinId = p.summonSpriteSkin[spriteId].curUseDict.get(self.currSelectItemSpriteIndex, 0)
            skinData = SSSKIND.data.get((spriteId, skinId), {})
            overviewMc.overview_changeForm.visible = skinData.get('transformModelIdAfter', 0)
        overviewMc.rareTransferBtn.visible = self.isRareTransferBtnVisible(spriteId, rareLv)
        upgradeStage = spriteInfo.get('upgradeStage', 0)
        if (spriteId, upgradeStage) in SUD.data:
            overviewMc.overview_spriteRemove.disabled = True
            tipMsg = uiUtils.getTextFromGMD(GMDD.data.CANNOT_REMOVE_UPGRADE_SPRITE, '')
            TipManager.addTip(overviewMc.overview_spriteRemove, tipMsg)
        else:
            overviewMc.overview_spriteRemove.disabled = False
            TipManager.addTip(overviewMc.overview_spriteRemove, SCD.data.get('spriteRemoveTip', ''))

    def isRareTransferBtnVisible(self, spriteId, rareLv):
        if not gameglobal.rds.configData.get('enableSpriteRareTransfer', False):
            return False
        if rareLv != gametypes.SPRITE_RARE_TYPE_SPECIAL:
            return False
        blackList = SCD.data.get('spriteRareTransferBlackList', ())
        if spriteId in blackList:
            return False
        return True

    def updateSpriteBattleBigState(self):
        overviewMc = self.widget.mineWarSpritePanel.overviewMc
        if utils.getSpriteBattleState(self.currSelectItemSpriteIndex):
            overviewMc.overview_spriteState.visible = True
            overviewMc.overview_spriteState.gotoAndStop('state1')
            overviewMc.familiarBtn.disabled = True
            tip = uiUtils.getTextFromGMD(GMDD.data.SUMMON_SPRITE_FAMILIAR_IN_BATTLE, 'battle')
            TipManager.addTip(overviewMc.familiarBtn, tip)
        elif utils.getSpriteAccessoryState(self.currSelectItemSpriteIndex):
            overviewMc.overview_spriteState.visible = True
            overviewMc.overview_spriteState.gotoAndStop('state0')
            overviewMc.familiarBtn.disabled = True
            tip = uiUtils.getTextFromGMD(GMDD.data.SUMMON_SPRITE_FAMILIAR_IN_ACCESSORY, 'accessory')
            TipManager.addTip(overviewMc.familiarBtn, tip)
        else:
            overviewMc.overview_spriteState.visible = False
            overviewMc.familiarBtn.disabled = False
            TipManager.removeTip(overviewMc.familiarBtn)

    def updateSpritePhoto3D(self):
        self.initHeadGen()
        self.takePhoto3D()

    def updateSpriteExpBar(self):
        if not self.widget:
            return
        if not self.widget.mineWarSpritePanel:
            return
        overviewMc = self.widget.mineWarSpritePanel.overviewMc
        spriteInfo = self.getCurSelectSpriteInfo()
        props = spriteInfo.get('props', {})
        expBar = overviewMc.overview_spriteExpBar
        expText = overviewMc.overview_spriteLv
        curValue = int(props.get('exp', 0))
        maxValue = int(props.get('maxExp', 1))
        expText.text = '%d' % props.get('lv', 0)
        expBar.exp.text = '%d/%d' % (curValue, int(maxValue))
        expBar.currentValue = curValue
        expBar.maxValue = maxValue
        TipManager.addTip(overviewMc.lvIcon, SCD.data.get('spriteLvTip'), tipUtils.TYPE_DEFAULT_BLACK)
        TipManager.addTip(expText, SCD.data.get('spriteLvTip'), tipUtils.TYPE_DEFAULT_BLACK)

    def updateSpritePrivityBar(self):
        if not self.widget:
            return
        if not self.widget.mineWarSpritePanel:
            return
        overviewMc = self.widget.mineWarSpritePanel.overviewMc
        spriteInfo = self.getCurSelectSpriteInfo()
        props = spriteInfo.get('props', {})
        privityText = overviewMc.overview_spritePrivityValue
        privityBar = overviewMc.overview_spritePrivityBar
        curValue = int(props.get('famiExp', 0))
        maxValue = int(props.get('famiMaxExp', 1))
        familiar = int(props.get('familiar', 0))
        famiAdd = int(props.get('famiEffAdd', 0))
        famiEffLv = int(props.get('famiEffLv', 0))
        color = '#489713' if famiAdd > 0 else '#623A17'
        privityText.htmlText = uiUtils.toHtml(famiEffLv, color)
        privityBar.privity.text = '%d/%d' % (curValue, maxValue)
        privityBar.currentValue = curValue
        privityBar.maxValue = maxValue
        if self.currSelectItemSpriteIndex in self.recordfamiLv:
            famiPreLv = self.recordfamiLv[self.currSelectItemSpriteIndex]
        else:
            self.recordfamiLv[self.currSelectItemSpriteIndex] = 0
            famiPreLv = 0
        familiarChangeTo = SCD.data.get('spriteFamiliarChangeTo', 20)
        if famiEffLv < familiarChangeTo:
            overviewMc.famiIcon.gotoAndStop('fami1')
        elif famiEffLv == familiarChangeTo and famiPreLv and famiPreLv < familiarChangeTo:
            overviewMc.famiIcon.gotoAndStop('fami2')
            overviewMc.famiIcon.famiStage2.gotoAndPlay(1)
        else:
            overviewMc.famiIcon.gotoAndStop('fami3')
        self.recordfamiLv[self.currSelectItemSpriteIndex] = famiEffLv
        self.addFamiliarIconTip(privityText, familiar, famiAdd, famiEffLv, showFamiPercentTip=True, curFamiExp=curValue, maxFamiExp=maxValue)
        self.addFamiliarIconTip(overviewMc.famiIcon, familiar, famiAdd, famiEffLv, showFamiPercentTip=True, curFamiExp=curValue, maxFamiExp=maxValue)
        self.addFamiliarIconTip(privityBar, familiar, famiAdd, famiEffLv, showFamiPercentTip=True, curFamiExp=curValue, maxFamiExp=maxValue)

    def updateDeourBtnAndLunhuiBtn(self, btn, index, isLunhui):
        btn.isLunhui = isLunhui
        tip = None
        if utils.getSpriteAccessoryState(index):
            if isLunhui:
                tip = uiUtils.getTextFromGMD(GMDD.data.SUMMON_SPRITE_LUNHUI_IN_ACCESSORY, 'accessory')
            else:
                tip = uiUtils.getTextFromGMD(GMDD.data.SUMMON_SPRITE_SWALLOW_IN_ACCESSORY, 'accessory')
        elif utils.getSpriteBattleState(index):
            if isLunhui:
                tip = uiUtils.getTextFromGMD(GMDD.data.SUMMON_SPRITE_LUNHUI_IN_BATTLE_STATE, 'battle')
            else:
                tip = uiUtils.getTextFromGMD(GMDD.data.SUMMON_SPRITE_SWALLOW_IN_BATTLE_STATE, 'battle')
        if tip:
            btn.disabled = True
            TipManager.addTip(btn, tip)
        else:
            btn.disabled = False
            TipManager.removeTip(btn)
            btn.addEventListener(events.BUTTON_CLICK, self.handleDeourOrLunhuiBtnClick, False, 1, True)

    def updateSpriteSkill(self):
        overviewMc = self.widget.mineWarSpritePanel.overviewMc
        spriteInfo = self.getCurSelectSpriteInfo()
        spriteId = spriteInfo.get('spriteId', 0)
        props = spriteInfo.get('props', {})
        skillInfo = spriteInfo.get('skills', {})
        bAwake = props.get('juexing', False)
        familiar = props.get('familiar', 0)
        index = spriteInfo.get('index', 0)
        rareLv = spriteInfo.get('rareLv', 0)
        naturals = skillInfo.get('naturals', [])
        bonus = skillInfo.get('bonus', [])
        sData = SSID.data.get(spriteId, {})
        awakeNeedFamiliarLv = sData.get('awakeNeedFamiliarLv', 0)
        bAwakeDisabled = familiar < awakeNeedFamiliarLv
        if self.checkUpGradeBtnVisible():
            overviewMc.upGradeBtn.visible = True
            overviewMc.devourBtn.visible = False
        else:
            overviewMc.upGradeBtn.visible = False
            if rareLv == gametypes.SPRITE_RARE_TYPE_SPECIAL:
                overviewMc.devourBtn.visible = False
            else:
                overviewMc.devourBtn.visible = True
                self.updateDeourBtnAndLunhuiBtn(overviewMc.devourBtn, index, False)
        overviewMc.lunhuiBtn.disabled = False
        TipManager.removeTip(overviewMc.lunhuiBtn)
        if len(naturals) < const.SSPRITE_NATURAM_SKILL_NUM_LIMIT:
            overviewMc.lunhuiBtn.disabled = True
            tip = uiUtils.getTextFromGMD(GMDD.data.SPRITE_NATURAM_SKILL_NUM_LIMIT_LUNHUI_1, '')
            TipManager.addTip(overviewMc.lunhuiBtn, tip)
        else:
            self.updateDeourBtnAndLunhuiBtn(overviewMc.lunhuiBtn, index, True)
        overviewMc.aWakeBtn.visible = False if bAwake else True
        overviewMc.aWakedP.visible = True if bAwake else False
        self.updatePassiveAndAwakeSkill(overviewMc.overview_passiveSkillSlot, props, skillInfo, 'trait', [], False)
        self.updatePassiveAndAwakeSkill(overviewMc.overview_avtiveSkillSlot, props, skillInfo, 'awake', bonus, bAwakeDisabled)
        talentSkill0, talentSkill1 = self.getBonusToSKillIds(bonus)
        for i in range(MAX_TALENT_NUM):
            skillIcon = overviewMc.getChildByName('overview_skill%d' % i)
            cornerPic = overviewMc.getChildByName('cornerPic%d' % i)
            bonusPoint = overviewMc.getChildByName('bonusPoint%d' % i)
            skillIcon.lockMC.visible = False
            ASUtils.setHitTestDisable(bonusPoint, True)
            if i < len(naturals):
                skillIcon.alpha = 1
                skillType = naturals[i]
                skillId = SSSD.data.get(skillType, {}).get('virtualSkill', 0)
                universalLabel = SSSD.data.get(skillType, {}).get('universalLabel', 0)
                ASUtils.setHitTestDisable(skillIcon.slot, False)
                if skillId:
                    self.updateSkillSlotIcon(skillIcon.slot, None, skillId, 'naturals')
                cornerPic.visible = True
                signId = universalLabel if universalLabel else SPRITE_SKILL_SIGN_ID
                cornerPic.gotoAndStop('sign_%d' % signId)
                if skillType in talentSkill0 and skillType in talentSkill1:
                    bonusPoint.visible = True
                    bonusPoint.gotoAndStop('point%d' % BONUS_POINT_TYPE2)
                elif skillType in talentSkill0:
                    bonusPoint.visible = True
                    bonusPoint.gotoAndStop('point%d' % BONUS_POINT_TYPE0)
                elif skillType in talentSkill1:
                    bonusPoint.visible = True
                    bonusPoint.gotoAndStop('point%d' % BONUS_POINT_TYPE1)
                else:
                    bonusPoint.visible = False
            else:
                skillIcon.alpha = 0.45
                cornerPic.visible = False
                bonusPoint.visible = False
                skillIcon.slot.setItemSlotData(None)
                ASUtils.setHitTestDisable(skillIcon.slot, True)

        overviewMc.bonusTitle.text = '%s%s' % (gameStrings.SUMMONED_WAR_SPRITE_BONUS_TITLE, sData.get('spriteTypeLabel', ''))
        if bonus:
            overviewMc.bonusMc.visible = True
            for i in range(MAX_BONUS_NUM):
                skillText = overviewMc.bonusMc.getChildByName('bonusDesc%d' % i)
                bonusBg = overviewMc.bonusMc.getChildByName('bonusBg%d' % i)
                if i < len(bonus):
                    skillText.visible = True
                    bonusBg.visible = True
                    skillText.htmlText = SSSD.data.get(bonus[i], {}).get('bonusName', '')
                    tip = SSSD.data.get(bonus[i], {}).get('bonusDesc', '')
                    TipManager.addTip(skillText, tip)
                else:
                    skillText.visible = False
                    bonusBg.visible = False

        else:
            overviewMc.bonusMc.visible = False

    def getBonusToSKillIds(self, bonus):
        if len(bonus) == BONUS_POINT_NUM_ONE:
            bonusId0 = bonus[0]
            bonusId1 = 0
        elif len(bonus) == BONUS_POINT_NUM_TWO:
            bonusId0 = bonus[0]
            bonusId1 = bonus[1]
        else:
            bonusId0 = 0
            bonusId1 = 0
        return (SSBSD.data.get(bonusId0, {}).get('talentCombo', ()), SSBSD.data.get(bonusId1, {}).get('talentCombo', ()))

    def updatePassiveAndAwakeSkill(self, skillSlot, props, skillInfo, szType, bonus = [], bAwakeDisabled = False):
        typeId = skillInfo.get(szType, 0)
        sssdData = SSSD.data.get(typeId, {})
        skillId = sssdData.get('virtualSkill', 0)
        skillAddId, skillLvAdd = sssdData.get('skillAddVirtualLv', (0, 0))
        addVirtualLv = skillLvAdd if skillAddId in bonus else 0
        if skillId:
            self.updateSkillSlotIcon(skillSlot.slotS, skillSlot.nameS, skillId, szType, addVirtualLv)
            skillSlot.lockS.visible = False
            skillSlot.blackBg.visible = False
            skillSlot.lessFamiIcon.visible = False
            bAwake = props.get('juexing', False)
            if szType == 'awake':
                if not bAwake:
                    skillSlot.lockS.visible = True
                    skillSlot.blackBg.visible = True
                    skillSlot.lessFamiIcon.visible = False
                    ASUtils.setHitTestDisable(skillSlot.blackBg, True)
                elif bAwakeDisabled:
                    skillSlot.lessFamiIcon.visible = True
                    tip = uiUtils.getTextFromGMD(GMDD.data.SPRITE_AWAKE_NEED_FAMI_TIP, '')
                    TipManager.addTip(skillSlot.lessFamiIcon, tip)

    def updateSkillSlotIcon(self, slot, nameText, skillId, szType, addVirtualLv = 0):
        famiEfflv = self.getCurSelectSpriteInfo().get('props', {}).get('famiEffLv', 1)
        effLv = utils.getEffLvBySpriteFamiEffLv(famiEfflv, szType, const.DEFAULT_SKILL_LV_SPRITE)
        lv = min(effLv + addVirtualLv, const.MAX_SKILL_LEVEL)
        try:
            skillInfo = skillDataInfo.ClientSkillInfo(skillId, lv=lv)
            iconPath = uiUtils.getSkillIconPath(skillInfo, uiConst.ICON_SIZE64)
            slot.fitSize = True
            slot.dragable = False
            slot.setItemSlotData({'iconPath': iconPath})
            slot.validateNow()
            TipManager.addTipByType(slot, tipUtils.TYPE_SKILL, {'skillId': skillId,
             'lv': lv}, False, 'upLeft')
            if nameText:
                nameText.text = skillInfo.getSkillData('sname', '')
        except Exception as e:
            gamelog.error(e)

    def getCurSelectSpriteProp(self):
        idx = self.currSelectItemSpriteIndex
        return BigWorld.player().summonSpriteProps.get(idx, {})

    def getCurSelectSpritePropWithFami(self):
        idx = self.currSelectItemSpriteIndex
        return BigWorld.player().summonSpritePropsWithFami.get(idx, {})

    def getCurSelectSpriteInfo(self):
        return BigWorld.player().summonSpriteList.get(self.currSelectItemSpriteIndex, {})

    def updateAttributeInfo(self):
        overviewMc = self.widget.mineWarSpritePanel.overviewMc
        if overviewMc.mainAttrBtn.selected:
            spriteInfo = self.getCurSelectSpriteProp()
            mainPropInfo = uiUtils.getSpritePropsArray(uiConst.MAIN_PROPS)
        else:
            spriteInfo = self.getCurSelectSpritePropWithFami()
            mainPropInfo = uiUtils.getSpritePropsArray(uiConst.MAIN_PROPS)
        mainInfo = uiUtils.createSpriteArr(spriteInfo, mainPropInfo, False)
        for i, info in enumerate(mainInfo):
            itemMc = overviewMc.getChildByName('overview_value%d' % i)
            itemMc.nameTF.text = info[0]
            itemMc.valueTF.text = info[1]
            tip = uiUtils.getSpritePropsTooltip(spriteInfo, int(info[2]), int(info[3]))
            TipManager.addTip(itemMc.valueTF, tip, tipUtils.TYPE_DEFAULT_BLACK)
            TipManager.addTip(itemMc.nameTF, tip, tipUtils.TYPE_DEFAULT_BLACK)

    def updateAttributeInfoOther(self, mainAttrBtnSelected):
        p = BigWorld.player()
        overviewMc = self.widget.mineWarSpritePanel.overviewMc
        overviewMc.mainAttrBtn.selected = mainAttrBtnSelected
        overviewMc.fightAttrBtn.selected = not mainAttrBtnSelected
        overviewMc.fightAttrHintIcon.visible = not mainAttrBtnSelected
        overviewMc.fightAttrHintTxt.visible = not mainAttrBtnSelected
        guardMaxFami = self.getGuardSpriteMaxFami()
        curSpriteFami, _, _ = utils.getSpriteFamiByIdx(self.currSelectItemSpriteIndex)
        syncMaxFami = guardMaxFami if guardMaxFami > curSpriteFami else curSpriteFami
        if p.isUsingTemp():
            syncMaxFami = SCD.data.get('charTempSpriteFamiliar', 200)
        overviewMc.fightAttrHintTxt.htmlText = gameStrings.SUMMONED_WAR_SPRITE_FIGHT_ATTR_HINT % syncMaxFami

    def updateSpriteBattleState(self, index):
        if not self.widget:
            return
        warSpritesMc = self.widget.mineWarSpritePanel.warSpritesMc
        wndListItems = warSpritesMc.spriteList.items
        wndListLen = len(wndListItems)
        for i in xrange(wndListLen):
            spriteHeadMc = wndListItems[i]
            if spriteHeadMc.data and spriteHeadMc.data['isShowUnlockSlot']:
                continue
            itemMc = spriteHeadMc.headItem
            if itemMc.warSpriteIndex == index:
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
                self.updateSpriteBattleBigState()
                self.updateCallBackBtnLabel()
                break

    def takePhoto3D(self):
        spriteInfo = self.getCurSelectSpriteInfo()
        spriteId = spriteInfo.get('spriteId', 0)
        p = BigWorld.player()
        skinId = 0
        if p.summonSpriteSkin.has_key(spriteId):
            skinId = p.summonSpriteSkin[spriteId].curUseDict.get(self.currSelectItemSpriteIndex, 0)
        skinData = SSSKIND.data.get((spriteId, skinId), {})
        if skinData:
            if self.isTransform:
                spriteModel = skinData.get('transformModelIdAfter', 0)
                materials = skinData.get('materialsAfter', 'Default')
            else:
                spriteModel = skinData.get('transformModelIdBefore', 0)
                materials = skinData.get('materialsBefore', 'Default')
            if not self.headGen:
                self.headGen = capturePhoto.SummonedWarSpritePhotoGen.getInstance('gui/taskmask.tga', 299)
            self.headGen.startCapture(spriteModel, materials, None)
        else:
            if not self.headGen:
                self.headGen = capturePhoto.SummonedWarSpritePhotoGen.getInstance('gui/taskmask.tga', 299)
            charType = SSD.data.get(spriteId, {}).get('charType', 0)
            spriteModel = MMCD.data.get(charType, {}).get('model', 0)
            self.headGen.startCapture(spriteModel, None, None)

    def updateAttachEffect(self, model, previewDustId, isPreview):
        spriteInfo = self.getCurSelectSpriteInfo()
        spriteId = spriteInfo.get('spriteId', 0)
        p = BigWorld.player()
        if not isPreview and not previewDustId and p.summonSpriteFootDust.has_key(spriteId):
            dustId = p.summonSpriteFootDust[spriteId].curUseDict.get(self.currSelectItemSpriteIndex, 0)
        elif isPreview and previewDustId:
            dustId = previewDustId
        else:
            dustId = 0
        dustData = SSFDD.data.get((spriteId, dustId), {})
        effects = dustData.get('footDustEffects', [])
        eScale = dustData.get('footDustEffectScale', 1.0)
        if model and effects:
            for effect in effects:
                efs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (p.getEquipEffectLv(),
                 p.getEquipEffectPriority(),
                 model,
                 effect,
                 sfx.EFFECT_LIMIT_MISC))
                if efs:
                    for ef in efs:
                        ef and ef.scale(eScale)

    def resetHeadGen(self):
        if self.headGen:
            self.headGen.endCapture()

    def initHeadGen(self):
        if not self.headGen:
            self.headGen = capturePhoto.SummonedWarSpritePhotoGen.getInstance('gui/taskmask.tga', 299)
        self.headGen.initFlashMesh()

    def updateSpriteHunger(self):
        if not self.widget:
            return
        hungerBtn = self.widget.mineWarSpritePanel.overviewMc.hungerBtn
        hungerBtn.addEventListener(events.BUTTON_CLICK, self.handleHungerBtnClick, False, 0, True)
        val0, val1, val2, val3 = SCD.data.get('spriteHungryThresholds', ())
        spriteInfo = self.getCurSelectSpriteInfo()
        props = spriteInfo.get('props', {})
        curHungerVal = int(props.get('hungry', 0))
        step = 0
        if curHungerVal >= val0 and curHungerVal <= val1:
            step = 0
        elif curHungerVal > val1 and curHungerVal <= val2:
            step = 1
        elif curHungerVal > val2:
            step = 2
        hungerBtn.label = '%d/%d' % (curHungerVal, val3)
        hungerBtn.hungerState.gotoAndStop('hunger%d' % step)
        hungerBtn.hungerBar.gotoAndStop('hunger%d' % step)
        heigth = hungerBtn.hungerMask.height
        hungerBtn.hungerMask.y = max(0, heigth - curHungerVal * 1.0 * 40 / val3)
        tip = SCD.data.get('spriteHungryTip', {}).get(step, '')
        TipManager.addTip(hungerBtn, tip)

    def refreshSpriteProp(self, index):
        gamelog.debug('m.l@SummonedWarSpriteMineProxy.refreshSpritePropWhenChange', index)
        proxy = self.getSelectedSubProxy()
        if hasattr(proxy, 'refreshSpritePropInfo'):
            self.getSelectedSubProxy().refreshSpritePropInfo(index)

    def refreshSpritePropInfo(self, index):
        gamelog.debug('m.l@SummonedWarSpriteMineProxy.refreshSpritePropInfo', index)
        self.updateAttributeInfo()

    def refreshLearnedSkillSfx(self, index, slot):
        if not self.widget:
            return
        if self.currSelectItemSpriteIndex != index:
            return
        proxy = self.getSelectedSubProxy()
        if hasattr(proxy, 'palyLearnedSkillSfx'):
            self.getSelectedSubProxy().palyLearnedSkillSfx(slot)

    def showLearnedSpriteSkillMsg(self, index, newRefID, oldRefID):
        if not self.widget:
            return
        proxy = self.getSelectedSubProxy()
        if hasattr(proxy, 'showLearnedSkillMsg'):
            self.getSelectedSubProxy().showLearnedSkillMsg(index, newRefID, oldRefID)

    def updateSpriteSkinOrFootDust(self):
        if not self.widget:
            return
        proxy = self.getSelectedSubProxy()
        if self.selectTabBtnName == TABLE_BTN_NAME_OVERVIEW:
            if hasattr(proxy, 'updateSpritePhoto3D'):
                proxy.updateSpritePhoto3D()
        elif self.selectTabBtnName == TABLE_BTN_NAME_PEELER:
            if hasattr(proxy, 'updateSpriteSkinOrFootDustMc'):
                proxy.updateSpriteSkinOrFootDustMc()

    def setSpriteSelected(self, spriteIdx, tabName = None):
        if not self.widget:
            return
        if self.currSelectItemSpriteIndex == spriteIdx:
            if tabName and self.selectTabBtnName != tabName:
                self.selectTabBtnName = tabName
                self.updateTabBtnState()
            return
        numberId = -1
        for itemData in self.spriteItemList:
            if itemData.get('warSpriteIndex', 0) == spriteIdx:
                numberId = itemData['numberId']
                break

        if numberId < 0:
            return
        self.currSelectSpriteNumber = numberId
        self.currSelectItemSpriteIndex = spriteIdx
        if self.currSelectItem and self.currSelectItem.warSpriteIndex != spriteIdx:
            self.currSelectItem.selected = False
        gameglobal.rds.ui.summonedWarSprite.saveSpriteIndex(numberId, spriteIdx)
        spriteList = self.widget.mineWarSpritePanel.warSpritesMc.spriteList
        for item in spriteList.items:
            if item.data and hasattr(item.data, 'warSpriteIndex') and item.data['warSpriteIndex'] == spriteIdx:
                spriteList.labelFunction(item.data, item)
                self._setSpriteMCData(item.data, item)

        pos = spriteList.getIndexPosY(self.currSelectSpriteNumber)
        spriteList.scrollTo(pos)
        if tabName:
            self.selectTabBtnName = tabName
        self.updateTabBtnState()

    def openSpriteFeedPanel(self, feedItemPanel):
        if not self.widget:
            return
        if not feedItemPanel:
            return
        if self.selectTabBtnName != TABLE_BTN_NAME_OVERVIEW:
            return
        overviewMc = self.widget.mineWarSpritePanel.overviewMc
        self.currShowFeedMc = feedItemPanel
        if feedItemPanel == FEED_EXP_PANEL:
            tList = self.getFeedExpItemList()
            btn = overviewMc.overview_spriteAddExp
        elif feedItemPanel == FEED_PRIVITY_PANEL:
            tList = self.getFeedFamiItemList()
            btn = overviewMc.overview_spriteAddPrivity
        elif feedItemPanel == FEED_HUNGER_PANEL:
            tList = self.getFeedHungerItemList()
            btn = overviewMc.hungerBtn
        self.showFeedSpriteMc(btn, tList)

    def checkSpriteHungry(self):
        p = BigWorld.player()
        spriteBattleIndex = getattr(p, 'spriteBattleIndex', None)
        if not spriteBattleIndex:
            self.stopCallback()
            self.removeSpriteHungerPushMsg()
            return
        else:
            spriteInfo = p.summonSpriteList.get(spriteBattleIndex, {})
            props = spriteInfo.get('props', {})
            curHungerVal = int(props.get('hungry', 0))
            val0, val1, val2, val3 = SCD.data.get('spriteHungryThresholds', ())
            if curHungerVal > val1:
                self.stopCallback()
                self.removeSpriteHungerPushMsg()
                return
            if self.callback:
                self.stopCallback()
            self.pushSpriteHungerMessage(spriteBattleIndex)
            self.callback = BigWorld.callback(SCD.data.get('spriteHungerPushMsgCD', 60), self.checkSpriteHungry)
            return

    def stopCallback(self):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
            self.callback = None

    def pushSpriteHungerMessage(self, spriteIndex):
        if uiConst.MESSAGE_TYPE_SPRITE_BATTLE_HUNGER not in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_SPRITE_BATTLE_HUNGER)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_SPRITE_BATTLE_HUNGER, {'click': Functor(self.onPushMsgClick, spriteIndex)})

    def removeSpriteHungerPushMsg(self):
        if uiConst.MESSAGE_TYPE_SPRITE_BATTLE_HUNGER in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_SPRITE_BATTLE_HUNGER)

    def onPushMsgClick(self, spriteIndex):
        gameglobal.rds.ui.summonedWarSprite.show(uiConst.WAR_SPRITE_TAB_INDEX0, spriteIndex, 'feedHungerMc')

    def updateSpriteSkillReplaceSucc(self, index, slot, newRefID, oldRefID):
        if not self.widget:
            return
        if self.currSelectItemSpriteIndex != index:
            return
        proxy = self.getSelectedSubProxy()
        if hasattr(proxy, 'usedSkillReplaceSucc'):
            self.getSelectedSubProxy().usedSkillReplaceSucc(slot, newRefID, oldRefID)

    def getSpriteTipByIndex(self, spriteIndex):
        p = BigWorld.player()
        if spriteIndex not in p.summonSpriteList:
            return uiUtils.dict2GfxDict({}, True)
        spriteInfo = p.summonSpriteList[spriteIndex]
        spriteTipInfo = self.getSpriteTipByInfo(spriteInfo, oriData=True)
        if not BigWorld.isPublishedVersion():
            spriteTipInfo['spriteName'] = '%s(%s)' % (spriteTipInfo.get('spriteName', ''), str(spriteIndex))
        return uiUtils.dict2GfxDict(spriteTipInfo, True)

    def getSpriteDetailTipByIndex(self, spriteIndex):
        p = BigWorld.player()
        if spriteIndex not in p.summonSpriteList:
            return uiUtils.dict2GfxDict({}, True)
        spriteInfo = p.summonSpriteList[spriteIndex]
        spriteInfoDict = self.getSpriteMineInfoDict(spriteInfo)
        return gameglobal.rds.ui.summonedWarSprite.getSpriteDetailTipData(spriteInfoDict, True, rtype='rank')

    def getSpriteMineInfoDict(self, spriteInfo):
        tipsData = {const.SPRITE_DICT_INDEX_spriteId: spriteInfo['spriteId'],
         const.SPRITE_DICT_INDEX_name: spriteInfo['name'],
         const.SPRITE_DICT_INDEX_lv: spriteInfo['props']['lv'],
         const.SPRITE_DICT_INDEX_combatScore: spriteInfo['combatScore'],
         const.SPRITE_DICT_INDEX_bindType: spriteInfo['bindType'],
         const.SPRITE_DICT_INDEX_naturals: spriteInfo['skills']['naturals'],
         const.SPRITE_DICT_INDEX_bonus: spriteInfo['skills']['bonus'],
         const.SPRITE_DICT_INDEX_famiEffLv: spriteInfo['props']['famiEffLv'],
         const.SPRITE_DICT_INDEX_juexing: spriteInfo['props']['juexing'],
         const.SPRITE_DICT_INDEX_awake: spriteInfo['skills']['awake'],
         const.SPRITE_DICT_INDEX_oriPrimaryProp: spriteInfo['props']['oriPrimaryProp'],
         const.SPRITE_DICT_INDEX_attrAgi: spriteInfo['props']['attrAgi'],
         const.SPRITE_DICT_INDEX_attrInt: spriteInfo['props']['attrInt'],
         const.SPRITE_DICT_INDEX_attrPhy: spriteInfo['props']['attrPhy'],
         const.SPRITE_DICT_INDEX_attrPw: spriteInfo['props']['attrPw'],
         const.SPRITE_DICT_INDEX_attrSpr: spriteInfo['props']['attrSpr'],
         const.SPRITE_DICT_INDEX_oriAptitudeAgi: spriteInfo['props']['oriAptitudeAgi'],
         const.SPRITE_DICT_INDEX_oriAptitudeInt: spriteInfo['props']['oriAptitudeInt'],
         const.SPRITE_DICT_INDEX_oriAptitudePhy: spriteInfo['props']['oriAptitudePhy'],
         const.SPRITE_DICT_INDEX_oriAptitudePw: spriteInfo['props']['oriAptitudePw'],
         const.SPRITE_DICT_INDEX_oriAptitudeSpr: spriteInfo['props']['oriAptitudeSpr'],
         const.SPRITE_DICT_INDEX_aptitudeAgi: spriteInfo['props']['aptitudeAgi'],
         const.SPRITE_DICT_INDEX_aptitudeInt: spriteInfo['props']['aptitudeInt'],
         const.SPRITE_DICT_INDEX_aptitudePhy: spriteInfo['props']['aptitudePhy'],
         const.SPRITE_DICT_INDEX_aptitudePw: spriteInfo['props']['aptitudePw'],
         const.SPRITE_DICT_INDEX_aptitudeSpr: spriteInfo['props']['aptitudeSpr'],
         const.SPRITE_DICT_INDEX_famiEffAdd: spriteInfo['props']['famiEffAdd'],
         const.SPRITE_DICT_INDEX_growthRatio: spriteInfo['props']['growthRatio'],
         const.SPRITE_DICT_INDEX_boneLv: spriteInfo['props']['boneLv'],
         const.SPRITE_DICT_INDEX_clever: spriteInfo['props']['clever'],
         const.SPRITE_DICT_INDEX_vPropCache: spriteInfo['props']['vPropCache'],
         const.SPRITE_DICT_INDEX_baseGrowthRatio: spriteInfo['props']['baseGrowthRatio'],
         const.SPRITE_DICT_INDEX_trait: spriteInfo['skills']['trait'],
         const.SPRITE_DICT_INDEX_upgradeStage: spriteInfo['upgradeStage']}
        learns = []
        for i, dic in enumerate(spriteInfo['skills']['learns']):
            learns.append((dic['id'], dic['slot'], dic['part']))

        tipsData[const.SPRITE_DICT_INDEX_learns] = learns
        return tipsData

    def getSpriteTipByInfo(self, spriteInfo, oriData = False):
        spriteId = spriteInfo.get('spriteId', 0)
        ssidData = SSID.data.get(spriteId, {})
        iconId = ssidData.get('spriteIcon', '000')
        iconPath = SPRITE_ICON_PATH % str(iconId)
        bindType = spriteInfo.get('bindType', gametypes.ITEM_BIND_TYPE_NONE)
        skills = spriteInfo.get('skills', {})
        naturals = skills.get('naturals', [])
        bonus = skills.get('bonus', [])
        talentSkill0, talentSkill1 = self.getBonusToSKillIds(bonus)
        talentSkillList = []
        for skillType in naturals:
            skillId = SSSD.data.get(skillType, {}).get('virtualSkill', 0)
            famiEfflv = spriteInfo.get('props', {}).get('famiEffLv', 1)
            lv = utils.getEffLvBySpriteFamiEffLv(famiEfflv, 'naturals', const.DEFAULT_SKILL_LV_SPRITE)
            skillInfo = skillDataInfo.ClientSkillInfo(skillId, lv=lv)
            skillIcon = uiUtils.getSkillIconPath(skillInfo, uiConst.ICON_SIZE64)
            sname = skillInfo.getSkillData('sname', '')
            if skillType in talentSkill0 and skillType in talentSkill1:
                pointGoto = 'point%d' % BONUS_POINT_TYPE2
            elif skillType in talentSkill0:
                pointGoto = 'point%d' % BONUS_POINT_TYPE0
            elif skillType in talentSkill1:
                pointGoto = 'point%d' % BONUS_POINT_TYPE1
            else:
                pointGoto = ''
            universalLabel = SSSD.data.get(skillType, {}).get('universalLabel', 0)
            signId = universalLabel if universalLabel else SPRITE_SKILL_SIGN_ID
            cornerPicGoto = 'sign_%d' % signId
            talentSkillList.append({'sname': sname,
             'skillIcon': skillIcon,
             'pointGoto': pointGoto,
             'cornerPicGoto': cornerPicGoto})

        bonusNameList = []
        for bonusId in bonus:
            bonusName = SSSD.data.get(bonusId, {}).get('bonusName', '')
            bonusNameList.append(bonusName)

        spriteBindTypeDesc = SCD.data.get('spriteBindTypeDesc', (gameStrings.GUILD_AUCTION_BIND_TYPE_NOT_FOREVER, gameStrings.GUILD_AUCTION_BIND_TYPE_FOREVER))
        info = {}
        info['iconPath'] = iconPath
        info['qualityColor'] = self.qualityColorDic[len(naturals)]
        info['spriteName'] = spriteInfo.get('name', '')
        info['spriteType'] = ssidData.get('spriteRace', '')
        info['spriteLv'] = gameStrings.SPRITE_TIP_LV_DESC % spriteInfo.get('props', {}).get('lv', 0)
        info['bindTypeText'] = spriteBindTypeDesc[1] if bindType else spriteBindTypeDesc[0]
        info['talentSkillList'] = talentSkillList
        info['bonusNameList'] = bonusNameList
        props = spriteInfo.get('props', {})
        lvStr = "%d<font color = \'#73e539\'>+%d</font>" % (props.get('familiar', 0), props.get('famiEffAdd', 0))
        info['privityText'] = gameStrings.SPRITE_TIP_PRIVITY_LV % lvStr
        if oriData:
            return info
        return uiUtils.dict2GfxDict(info, True)

    def handleSpriteItemClick(self, spriteItem):
        if self.isShiftKeyDown and getattr(spriteItem, 'warSpriteIndex', None):
            BigWorld.player().constructSpriteInfo(spriteItem.warSpriteIndex)

    def handleKeyEvent(self, *args):
        e = ASObject(args[3][0])
        if e.keyCode == 16:
            self.isShiftKeyDown = e.type == events.KEYBOARD_EVENT_KEY_DOWN

    @property
    def typeToSort(self):
        return SCD.data.get('spriteMajorAbility', [])

    def setFamiliarMc(self, mc, showFamiliar, familiar, famiEffAdd, famiEffLv):
        mc.visible = showFamiliar
        mc.famiLv.text = '%s+%s' % (int(familiar), int(famiEffAdd))
        gameglobal.rds.ui.summonedWarSpriteMine.addFamiliarIconTip(mc.famiIcon, float(familiar), float(famiEffAdd), float(famiEffLv))

    def addFamiliarIconTip(self, mc, familiar, famiAdd, famiEffLv, showFamiPercentTip = False, curFamiExp = 0, maxFamiExp = 1):
        privityBarTip = ''
        if showFamiPercentTip:
            if familiar >= SCD.data.get('spriteFamiPercentShowLevel', 30):
                curPre = int(math.floor(curFamiExp * 1.0 / maxFamiExp * 100))
                privityBarTip = gameStrings.SUMMON_SPRITE_PRIVITY_BAR_TIP % (str(curPre), str(curPre * 0.005), str(curPre * 0.0025))
        tip = SCD.data.get('spriteFamiTip', '%s, %s, %s') % (famiEffLv, familiar, famiAdd) + SSFD.data.get(famiEffLv, {}).get('tipDesc', '') + privityBarTip
        TipManager.addTip(mc, tip, tipUtils.TYPE_DEFAULT_BLACK)

    def getGuardSpriteMaxFami(self):
        p = BigWorld.player()
        accesspryDict = p.summonedSpriteAccessory
        maxFami = 0
        for guardInfo in accesspryDict.itervalues():
            spriteIndex = guardInfo.get('spriteIndex', 0)
            if spriteIndex:
                familiar, _, _ = utils.getSpriteFamiByIdx(spriteIndex)
                maxFami = max(maxFami, familiar)

        return maxFami

    def longNumsCompare(self, a, b):
        if a > b:
            return 1
        if a < b:
            return -1
        return 0
