#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/summonedWarSpriteTameStateProxy.o
import BigWorld
import uiConst
import const
import tipUtils
import utils
import gameglobal
from uiProxy import UIProxy
from gameStrings import gameStrings
from guis import uiUtils
from guis.asObject import TipManager
from data import sys_config_data as SCD
from data import summon_sprite_info_data as SSID
from data import summon_sprite_familiar_data as SSFD
from cdata import game_msg_def_data as GMDD
SPRITE_ICON_PATH = 'summonedSprite/icon/%s.dds'

class SummonedWarSpriteTameStateProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteTameStateProxy, self).__init__(uiAdapter)
        self.widget = None
        self.spriteIndex = None
        self.callback = None
        self.callbackPush = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_WAR_SPRITE_TAME_STATE, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_WAR_SPRITE_TAME_STATE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_TAME_STATE)

    def reset(self):
        self.spriteIndex = None
        self.callback = None

    def show(self, spriteIndex):
        if not spriteIndex:
            return
        self.spriteIndex = spriteIndex
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_TAME_STATE)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.help.helpKey = SCD.data.get('spriteTrainHelpKey', 0)

    def refreshInfo(self):
        if not self.widget:
            return
        if not self.spriteIndex:
            return
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(self.spriteIndex, {})
        name = spriteInfo.get('name', '')
        spriteId = spriteInfo.get('spriteId', 0)
        iconPath = SPRITE_ICON_PATH % str(SSID.data.get(spriteId, {}).get('spriteIcon', '000'))
        self.widget.spriteSlot.slot.fitSize = True
        self.widget.spriteSlot.slot.dragable = False
        self.widget.spriteSlot.slot.setItemSlotData({'iconPath': iconPath})
        self.widget.spriteName.text = name
        self.updateLeftTime()
        self.updateFamiBar(spriteInfo)
        self.updateExpBar(spriteInfo)

    def _onGetSpriteBtnClick(self, e):
        BigWorld.player().base.completeTrainSprite(self.spriteIndex)
        self.hide()
        self.removeSTamePushMsg()

    def updateLeftTime(self):
        if not self.widget:
            self.stopCallback()
            return
        p = BigWorld.player()
        endTime = p.summonSpriteList.get(self.spriteIndex, {}).get('trainEndTimeStamp', 0)
        nowTime = utils.getNow()
        leftTime = endTime - nowTime
        if leftTime <= 0:
            self.widget.tameState.text = gameStrings.SPRITE_TAME_STATE_FINISH
            self.widget.leftTime.text = ''
            self.widget.getSpriteBtn.visible = True
            self.widget.desc.visible = False
            self.stopCallback()
            return
        self.widget.getSpriteBtn.visible = False
        self.widget.desc.visible = True
        self.widget.tameState.text = gameStrings.SPRITE_TAME_STATE_NOT_FINISH
        self.widget.leftTime.text = gameStrings.BACK_FLOW_LEFT_TIME_TITLE % utils.formatTime(leftTime)
        self.callback = BigWorld.callback(1, self.updateLeftTime)

    def stopCallback(self):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
            self.callback = None

    def updateFamiBar(self, spriteInfo):
        props = spriteInfo.get('props', {})
        trainReward = spriteInfo.get('trainReward', {})
        famiBar = self.widget.famiBar
        famiText = famiBar.valueText
        curValue = int(props.get('famiExp', 0))
        maxValue = int(props.get('famiMaxExp', 1))
        familiar = int(props.get('familiar', 0))
        famiAdd = int(props.get('famiEffAdd', 0))
        famiEffLv = int(props.get('famiEffLv', 0))
        trainFami = trainReward.get('famiExp', 0)
        famiBar.maxValue = maxValue
        famiBar.currentValues = [curValue, curValue + trainFami]
        self.widget.famiValT.text = familiar
        famiText.text = '+%d' % trainFami
        if famiEffLv < const.MAX_SKILL_LV_SPRITE_FAMILIAR:
            self.widget.famiIcon.gotoAndStop('fami1')
        elif famiEffLv >= const.MAX_SKILL_LV_SPRITE_FAMILIAR:
            self.widget.famiIcon.gotoAndStop('fami3')
        tip = SCD.data.get('spriteFamiTip', '%s, %s, %s') % (famiEffLv, familiar, famiAdd) + SSFD.data.get(famiEffLv, {}).get('tipDesc', '')
        TipManager.addTip(self.widget.famiIcon, tip, tipUtils.TYPE_DEFAULT_BLACK)

    def updateExpBar(self, spriteInfo):
        props = spriteInfo.get('props', {})
        trainReward = spriteInfo.get('trainReward', {})
        expBar = self.widget.expBar
        expText = expBar.valueText
        curValue = int(props.get('exp', 0))
        maxValue = int(props.get('maxExp', 1))
        expLv = props.get('lv', 0)
        trainExp = trainReward.get('exp', 0)
        expBar.maxValue = maxValue
        expBar.currentValues = [curValue, curValue + trainExp]
        expText.text = '+%d' % trainExp
        self.widget.expValT.text = expLv
        TipManager.addTip(self.widget.lvIcon, SCD.data.get('spriteLvTip'), tipUtils.TYPE_DEFAULT_BLACK)

    def checkTameTimeEndPush(self):
        p = BigWorld.player()
        if not getattr(p, 'spriteExtraDict', None):
            return
        trainingList = list(p.spriteExtraDict.get('trainingIndexSet', set()))
        if not trainingList:
            return
        endTime = p.summonSpriteList.get(trainingList[0], {}).get('trainEndTimeStamp', 0)
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
        self.callbackPush = BigWorld.callback(1, self.checkTameTimeEndPush)

    def stopCallbackPush(self):
        if self.callbackPush:
            BigWorld.cancelCallback(self.callbackPush)
            self.callbackPush = None

    def pushSTameMessage(self):
        if uiConst.MESSAGE_TYPE_SUMMON_SPRITE_TAME not in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_SUMMON_SPRITE_TAME)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_SUMMON_SPRITE_TAME, {'click': self.onPushMsgClick})

    def removeSTamePushMsg(self):
        if uiConst.MESSAGE_TYPE_SUMMON_SPRITE_TAME in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_SUMMON_SPRITE_TAME)

    def onPushMsgClick(self):
        msg = uiUtils.getTextFromGMD(GMDD.data.SPRITE_TAME_TIME_END_PUSH_MSG, '')
        gameglobal.rds.ui.messageBox.showMsgBox(msg)
        self.removeSTamePushMsg()
