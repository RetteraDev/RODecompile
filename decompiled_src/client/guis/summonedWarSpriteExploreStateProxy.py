#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteExploreStateProxy.o
from gamestrings import gameStrings
import BigWorld
import uiConst
import const
import tipUtils
import utils
import gameglobal
import events
import gametypes
import summonSpriteExplore
from uiProxy import UIProxy
from gameStrings import gameStrings
from guis import uiUtils
from guis.asObject import TipManager
from guis.asObject import ASObject
from data import sys_config_data as SCD
from data import summon_sprite_info_data as SSID
from data import summon_sprite_familiar_data as SSFD
from cdata import game_msg_def_data as GMDD
SPRITE_ICON_PATH = 'summonedSprite/icon/%s.dds'
SUM_BONUS_RATE_MAX = 100
SUM_BONUS_RATE_LIMIT = 200

class SummonedWarSpriteExploreStateProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteExploreStateProxy, self).__init__(uiAdapter)
        self.widget = None
        self.spriteIndexs = None
        self.callback = None
        self.callbackPush = None
        self.selectedItem = None
        self.bonusRate = 0
        self.endTime = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_WAR_SPRITE_EXPLORE_STATE, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_WAR_SPRITE_EXPLORE_STATE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_EXPLORE_STATE)

    def reset(self):
        self.spriteIndexs = None
        self.callback = None
        self.selectedItem = None
        self.bonusRate = 0
        self.endTime = 0

    def show(self, spriteIndexs):
        if not spriteIndexs:
            return
        self.spriteIndexs = spriteIndexs
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_EXPLORE_STATE)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        if not self.widget:
            return
        elif not self.spriteIndexs:
            return
        else:
            p = BigWorld.player()
            exploreSprite = p.spriteExtraDict['exploreSprite']
            self.bonusRate = min(p.vipRevise(gametypes.VIP_SERVICE_SPRITE_EXPLORE_ITEM_RATE, exploreSprite.bonusRate), SUM_BONUS_RATE_LIMIT)
            self.endTime = exploreSprite.exploreEndTimeStamp
            leftTime = self.endTime - utils.getNow()
            if leftTime > 0:
                self.updateInWayMc(self.bonusRate)
            self.updateLeftTime()
            self.widget.spriteMc.gotoAndStop('sprite%d' % len(self.spriteIndexs))
            for i in xrange(len(self.spriteIndexs)):
                spriteItem = getattr(self.widget.spriteMc, 'spriteItem%d' % i, None)
                if spriteItem:
                    spriteIndex = self.spriteIndexs[i]
                    spriteItem.idx = i
                    spriteItem.spriteIndex = spriteIndex
                    self.updateSpriteItem(spriteItem)

            return

    def updateSpriteItem(self, spriteItem):
        p = BigWorld.player()
        spriteIndex = spriteItem.spriteIndex
        spriteInfo = p.summonSpriteList.get(spriteIndex, {})
        name = spriteInfo.get('name', '')
        spriteItem.spriteName.text = name
        spriteId = spriteInfo.get('spriteId', 0)
        iconPath = SPRITE_ICON_PATH % str(SSID.data.get(spriteId, {}).get('spriteIcon', '000'))
        spriteItem.itemSlot.slot.spriteIndex = spriteIndex
        spriteItem.itemSlot.slot.fitSize = True
        spriteItem.itemSlot.slot.dragable = False
        spriteItem.itemSlot.slot.setItemSlotData({'iconPath': iconPath})
        spriteItem.itemSlot.slot.addEventListener(events.MOUSE_DOWN, self.handleSlotClick, False, 0, True)
        spriteItem.selectedIcon.visible = False
        if not self.selectedItem:
            self.selectedItem = spriteItem
            spriteItem.selectedIcon.visible = True
            self.updateFamiBar(spriteIndex)
            self.updateExpBar(spriteIndex)
        elif self.selectedItem and self.selectedItem.idx == spriteItem.idx:
            spriteItem.selectedIcon.visible = True
            self.updateFamiBar(spriteIndex)
            self.updateExpBar(spriteIndex)

    def handleSlotClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        spriteItem = target.parent.parent
        if self.selectedItem and self.selectedItem.idx == spriteItem.idx:
            return
        if self.selectedItem:
            self.selectedItem.selectedIcon.visible = False
        spriteIndex = spriteItem.spriteIndex
        spriteItem.selectedIcon.visible = True
        self.selectedItem = spriteItem
        self.updateFamiBar(spriteIndex)
        self.updateExpBar(spriteIndex)

    def handleGetBtnClick(self, *args):
        p = BigWorld.player()
        p.base.exploreSpriteComplete(self.spriteIndexs)
        self.hide()
        self.removeSTamePushMsg()
        gameglobal.rds.ui.summonedWarSpriteExplore.exploreSpriteIdx = {}

    def updateLeftTime(self):
        if not self.widget:
            self.stopCallback()
            return
        nowTime = utils.getNow()
        leftTime = self.endTime - nowTime
        if leftTime <= 0:
            self.widget.exploreState.gotoAndStop('finish')
            self.widget.leftTime.text = ''
            self.updateFinishMc(self.bonusRate)
            self.stopCallback()
            return
        self.widget.exploreState.gotoAndStop('inWay')
        self.widget.leftTime.text = gameStrings.BACK_FLOW_LEFT_TIME_TITLE % utils.formatTime(leftTime)
        self.callback = BigWorld.callback(1, self.updateLeftTime)

    def stopCallback(self):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
            self.callback = None

    def updateInWayMc(self, bonusRate):
        self.widget.finishMc.visible = False
        self.widget.getBackBtn.visible = False
        if bonusRate:
            self.widget.inWayMc.visible = True
            self.widget.noneCarryDesc.visible = False
            rewardItem = self.widget.inWayMc.rewardItem
            self.updateRewardSlot(rewardItem)
            self.updateBounsRate(bonusRate, self.widget.inWayMc.desc0)
        else:
            self.widget.inWayMc.visible = False
            self.widget.noneCarryDesc.visible = True

    def updateFinishMc(self, bonusRate):
        self.widget.noneCarryDesc.visible = False
        self.widget.inWayMc.visible = False
        if bonusRate:
            self.widget.finishMc.visible = True
            self.widget.getBackBtn.visible = False
            rewardItem = self.widget.finishMc.rewardItem
            self.updateRewardSlot(rewardItem)
            self.updateBounsRate(bonusRate, self.widget.finishMc.desc0)
            self.widget.finishMc.getBtn.addEventListener(events.BUTTON_CLICK, self.handleGetBtnClick, False, 0, True)
        else:
            self.widget.finishMc.visible = False
            self.widget.getBackBtn.visible = True
            self.widget.getBackBtn.addEventListener(events.BUTTON_CLICK, self.handleGetBtnClick, False, 0, True)

    def updateBounsRate(self, bonusRate, descText):
        if bonusRate > SUM_BONUS_RATE_MAX:
            tip = uiUtils.getTextFromGMD(GMDD.data.SUMMON_SPRITE_EXPLORE_RATE_OVER, '%d') % (bonusRate - 100)
        else:
            tip = uiUtils.getTextFromGMD(GMDD.data.SUMMON_SPRITE_EXPLORE_RATE_NORMAL, '%d') % bonusRate
        descText.text = gameStrings.TEXT_SUMMONEDWARSPRITEEXPLORESTATEPROXY_211 % bonusRate
        TipManager.addTip(descText, tip)

    def updateRewardSlot(self, rewardItem):
        p = BigWorld.player()
        exploreSprite = p.spriteExtraDict['exploreSprite']
        bonusId = exploreSprite.pendingBonusId if exploreSprite.pendingBonusId else exploreSprite.bonusId
        option = exploreSprite.option
        itemId = summonSpriteExplore.getItemIdByBonusId(option, bonusId)
        itemInfo = uiUtils.getGfxItemById(itemId)
        rewardItem.slot.fitSize = True
        rewardItem.slot.dragable = False
        rewardItem.slot.setItemSlotData(itemInfo)

    def updateFamiBar(self, spriteIndex):
        p = BigWorld.player()
        exploreSprite = p.spriteExtraDict['exploreSprite']
        wealthLv = exploreSprite.wealthLv
        exploreLv = exploreSprite.exploreLv
        expVal, famiVal = summonSpriteExplore.getExploreSpriteReward(exploreLv, wealthLv)
        famiBar = self.widget.famiBar
        famiText = famiBar.valueText
        spriteInfo = p.summonSpriteList.get(spriteIndex, {})
        props = spriteInfo.get('props', {})
        curValue = int(props.get('famiExp', 0))
        maxValue = int(props.get('famiMaxExp', 1))
        familiar = int(props.get('familiar', 0))
        famiAdd = int(props.get('famiEffAdd', 0))
        famiEffLv = int(props.get('famiEffLv', 0))
        famiBar.maxValue = maxValue
        famiBar.currentValues = [curValue, curValue + famiVal]
        self.widget.famiValT.text = familiar
        famiText.text = ''
        self.widget.addFamiVal.text = '+%d' % famiVal
        if famiEffLv < const.MAX_SKILL_LV_SPRITE_FAMILIAR:
            self.widget.famiIcon.gotoAndStop('fami1')
        elif famiEffLv >= const.MAX_SKILL_LV_SPRITE_FAMILIAR:
            self.widget.famiIcon.gotoAndStop('fami3')
        tip = SCD.data.get('spriteFamiTip', '%s, %s, %s') % (famiEffLv, familiar, famiAdd) + SSFD.data.get(famiEffLv, {}).get('tipDesc', '')
        TipManager.addTip(self.widget.famiIcon, tip, tipUtils.TYPE_DEFAULT_BLACK)

    def updateExpBar(self, spriteIndex):
        p = BigWorld.player()
        exploreSprite = p.spriteExtraDict['exploreSprite']
        wealthLv = exploreSprite.wealthLv
        exploreLv = exploreSprite.exploreLv
        expVal, famiVal = summonSpriteExplore.getExploreSpriteReward(exploreLv, wealthLv)
        expBar = self.widget.expBar
        expText = expBar.valueText
        spriteInfo = p.summonSpriteList.get(spriteIndex, {})
        props = spriteInfo.get('props', {})
        curValue = int(props.get('exp', 0))
        maxValue = int(props.get('maxExp', 1))
        expLv = props.get('lv', 0)
        expBar.maxValue = maxValue
        expBar.currentValues = [curValue, curValue + expVal]
        expText.text = ''
        self.widget.addExpVal.text = '+%d' % expVal
        self.widget.expValT.text = expLv
        TipManager.addTip(self.widget.lvIcon, SCD.data.get('spriteLvTip'), tipUtils.TYPE_DEFAULT_BLACK)

    def checkExploreTimeEndPush(self):
        p = BigWorld.player()
        if not getattr(p, 'spriteExtraDict', None):
            return
        elif p.charTempId:
            return
        else:
            exploreSprite = p.spriteExtraDict.get('exploreSprite', None)
            if not exploreSprite:
                return
            endTime = exploreSprite.exploreEndTimeStamp
            if not endTime:
                return
            nowTime = utils.getNow()
            leftTime = endTime - nowTime
            if leftTime <= 0:
                self.pushSTameMessage()
                self.stopCallbackPush()
                return
            if self.callbackPush:
                self.stopCallbackPush()
            self.callbackPush = BigWorld.callback(1, self.checkExploreTimeEndPush)
            return

    def stopCallbackPush(self):
        if self.callbackPush:
            BigWorld.cancelCallback(self.callbackPush)
            self.callbackPush = None

    def pushSTameMessage(self):
        if uiConst.MESSAGE_TYPE_SUMMON_SPRITE_EXPLORE not in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_SUMMON_SPRITE_EXPLORE)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_SUMMON_SPRITE_EXPLORE, {'click': self.onPushMsgClick})

    def removeSTamePushMsg(self):
        if uiConst.MESSAGE_TYPE_SUMMON_SPRITE_EXPLORE in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_SUMMON_SPRITE_EXPLORE)

    def onPushMsgClick(self):
        msg = uiUtils.getTextFromGMD(GMDD.data.SPRITE_EXPLORE_TIME_END_PUSH_MSG, '')
        gameglobal.rds.ui.messageBox.showMsgBox(msg)
        self.removeSTamePushMsg()
