#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/actEffectAppearanceProxy.o
import BigWorld
import gameglobal
import uiConst
import utils
import const
import events
import math
import gameconfigCommon
from sfx import physicsEffect
from asObject import ASObject
from asObject import TipManager
from gamestrings import gameStrings
from callbackHelper import Functor
from uiProxy import UIProxy
from data import act_appearance_data as AAD
from data import act_appearance_reverse_data as AARD
from data import sys_config_data as SCD

class ActEffectAppearanceProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActEffectAppearanceProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ACTION_EFFECT_APPEARANCE, self.hide)

    def reset(self):
        self.skillTip = None
        self.miniSkillTip = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ACTION_EFFECT_APPEARANCE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.reset()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ACTION_EFFECT_APPEARANCE)

    def show(self):
        if not gameconfigCommon.enableActAppearance():
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ACTION_EFFECT_APPEARANCE)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.main.itemRenderer = 'ActEffectAppearance_AppearanceItem'
        self.widget.main.lableFunction = self.actEffectGroupFunction
        self.widget.main.dataArray = []
        if not self.skillTip:
            self.skillTip = self.widget.getInstByClsName('ActEffectAppearance_Tip')
        if not self.miniSkillTip:
            self.miniSkillTip = self.widget.getInstByClsName('ActEffectAppearance_MiniTip')

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.main.dataArray = self.getActEffectGroupData()
        self.widget.main.validateNow()

    def getActEffectGroupData(self):
        groupDataArr = []
        for groupId in AARD.data.keys():
            groupDataArr.append({'groupId': groupId})

        return groupDataArr

    def actEffectGroupFunction(self, *args):
        if not self.widget:
            return
        info = ASObject(args[3][0])
        item = ASObject(args[3][1])
        p = BigWorld.player()
        currAppId = p.actAppearances.get(const.ACT_APPEARANCE_ACTIVE_ACT, {}).get(info.groupId, 0)
        if not currAppId:
            currAppId = physicsEffect.getDefaultAppearanceId(info.groupId)
        item.detail.itemRenderer = 'ActEffectAppearance_DetailItem'
        item.detail.lableFunction = self.actEffectItemFunction
        detailDataArray = []
        appIds = AARD.data.get(info.groupId, {}).get('id', [])
        for appId in appIds:
            detailDataArray.append({'groupId': info.groupId,
             'appId': appId,
             'curGruopAppId': currAppId})

        item.detail.dataArray = detailDataArray
        item.detail.validateNow()
        item.skill.icon.enabled = True
        item.skill.icon.focusable = False
        item.skill.icon.slot.fitSize = True
        item.skill.icon.slot.dragable = False
        iconPath = physicsEffect.getAppearanceIcon(currAppId)
        item.skill.icon.slot.setItemSlotData({'iconPath': iconPath})
        item.skill.icon.data = {'appearanceId': currAppId}
        appData = AAD.data.get(currAppId, {})
        appearanceName = appData.get('nName', '')
        item.skill.skillName.text = appearanceName
        isDefault = appData.get('default', 0)
        if isDefault:
            TipManager.addTipByFunc(item.skill.icon, self.onMiniTipShow, item.skill.icon, False)
        else:
            TipManager.addTipByFunc(item.skill.icon, self.onTipShow, item.skill.icon, False)

    def actEffectItemFunction(self, *args):
        if not self.widget:
            return
        info = ASObject(args[3][0])
        item = ASObject(args[3][1])
        isCurrent = info.appId == info.curGruopAppId
        appData = AAD.data.get(info.appId, {})
        isDefault = appData.get('default', 0)
        item.icon.focusable = False
        item.icon.addEventListener(events.BUTTON_CLICK, self.handleDetailItemClick, False, 0, True)
        item.icon.selected = isCurrent
        item.icon.data = {'appearanceId': info.appId}
        item.indate.visible = physicsEffect.inDate(info.appId)
        item.icon.slot.dragable = False
        iconPath = physicsEffect.getAppearanceIcon(info.appId)
        item.icon.slot.setItemSlotData({'iconPath': iconPath})
        if physicsEffect.isActive(info.appId):
            item.icon.slot.setSlotState(uiConst.ITEM_NORMAL)
        else:
            item.icon.slot.setSlotState(uiConst.ITEM_DISABLE)
        if isDefault:
            TipManager.addTipByFunc(item.icon, self.onMiniTipShow, item.icon, False)
        else:
            TipManager.addTipByFunc(item.icon, self.onTipShow, item.icon, False)
        item.icon.validateNow()

    def getDeadlineText(self, deadline):
        if deadline == 0:
            return gameStrings.ACT_APPEARANCE_DEADLINE_NOT_ACTIVE
        if deadline == -1:
            return gameStrings.ACT_APPEARANCE_DEADLINE_FOREVER
        if deadline > 0:
            leftTime = deadline - utils.getNow()
            if leftTime > const.TIME_INTERVAL_DAY:
                timeTxt = str(int(math.ceil(float(leftTime) / const.TIME_INTERVAL_DAY))) + gameStrings.COMMON_DAY
            elif leftTime > const.TIME_INTERVAL_HOUR:
                timeTxt = str(int(math.ceil(float(leftTime) / const.TIME_INTERVAL_HOUR))) + gameStrings.COMMON_HOUR
            elif leftTime > const.TIME_INTERVAL_MINUTE:
                timeTxt = str(int(math.ceil(float(leftTime) / const.TIME_INTERVAL_MINUTE))) + gameStrings.COMMON_MINUTE
            elif leftTime > 0:
                timeTxt = gameStrings.COMMON_LESSTHAN_ONE_MINUTE
            else:
                return gameStrings.ACT_APPEARANCE_DEADLINE_NOT_ACTIVE
            return gameStrings.ACT_APPEARANCE_DEADLINE_TIME % timeTxt
        return gameStrings.ACT_APPEARANCE_DEADLINE_NOT_ACTIVE

    def getDeadlineTextPure(self, deadline):
        if deadline == -1:
            return gameStrings.COMMON_INFINITE_TIME
        else:
            leftTime = deadline - utils.getNow()
            if leftTime > const.TIME_INTERVAL_DAY:
                timeTxt = str(int(math.ceil(float(leftTime) / const.TIME_INTERVAL_DAY))) + gameStrings.COMMON_DAY
            elif leftTime > const.TIME_INTERVAL_HOUR:
                timeTxt = str(int(math.ceil(float(leftTime) / const.TIME_INTERVAL_HOUR))) + gameStrings.COMMON_HOUR
            elif leftTime > const.TIME_INTERVAL_MINUTE:
                timeTxt = str(int(math.ceil(float(leftTime) / const.TIME_INTERVAL_MINUTE))) + gameStrings.COMMON_MINUTE
            else:
                timeTxt = gameStrings.COMMON_LESSTHAN_ONE_MINUTE
            return timeTxt

    def onTipShow(self, *args):
        if not self.widget:
            return None
        else:
            target = ASObject(args[3][0])
            if not self.skillTip:
                self.skillTip = self.widget.getInstByClsName('SKillAppearance_Tip')
            self.skillTip.visible = True
            appId = target.data.appearanceId
            appData = AAD.data.get(appId, {})
            nName = appData.get('nName', '')
            self.skillTip.skillName.text = nName
            self.skillTip.deadline.text = self.getDeadlineText(physicsEffect.getAppearanceDeadLineTime(appId))
            if physicsEffect.isActive(appId):
                self.skillTip.locked.text = gameStrings.ACT_APPEARANCE_CLICKTIP_USE
            else:
                self.skillTip.locked.text = gameStrings.ACT_APPEARANCE_CLICKTIP_TRY
            TipManager.showImediateTip(target, self.skillTip)
            return None

    def onMiniTipShow(self, *args):
        if not self.widget:
            return None
        else:
            target = ASObject(args[3][0])
            if not self.miniSkillTip:
                self.miniSkillTip = self.widget.getInstByClsName('SkillAppearance_MiniTip')
            self.miniSkillTip.visible = True
            appData = AAD.data.get(target.data.appearanceId, {})
            nName = appData.get('nName', '')
            desc = appData.get('desc', '')
            self.miniSkillTip.skillName.text = nName
            self.miniSkillTip.desc.text = desc
            self.miniSkillTip.bg.height = self.miniSkillTip.skillName.textHeight + self.miniSkillTip.defaultDesc.textHeight + self.miniSkillTip.desc.textHeight + 40
            TipManager.showImediateTip(target, self.miniSkillTip)
            return None

    def handleDetailItemClick(self, *args):
        e = ASObject(args[3][0])
        appearanceId = e.target.data.appearanceId
        p = BigWorld.player()
        if physicsEffect.isActive(appearanceId):
            aData = AAD.data.get(appearanceId, {})
            groupId = aData.get('groupId', 0)
            currAppId = p.actAppearances.get(const.ACT_APPEARANCE_ACTIVE_ACT, {}).get(groupId, 0)
            if currAppId == appearanceId:
                return
            p.cell.switchActAppearance(appearanceId)
        else:
            actEffectTrialTime = SCD.data.get('actEffectTrialTime', 0)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.ACT_APPEARANCE_MESSAGE_BOX % actEffectTrialTime, yesCallback=Functor(self.activeAppearance, appearanceId), yesBtnText=gameStrings.ACT_APPEARANCE_MESSAGE_BOX_ACTIVE, noCallback=Functor(self.trialAppearance, appearanceId), noBtnText=gameStrings.ACT_APPEARANCE_MESSAGE_BOX_TRIAL)

    def activeAppearance(self, appearanceId):
        p = BigWorld.player()
        itemIds = AAD.data.get(appearanceId, {}).get('useitems', ())
        if not itemIds or len(itemIds) == 0:
            return
        else:
            firstItem = None
            for itemId in itemIds:
                page, pos = p.inv.findItemInPages(itemId)
                if page != const.CONT_NO_PAGE and pos != const.CONT_NO_POS:
                    firstItem = p.inv.getQuickVal(page, pos)
                    break

            if firstItem:
                gameglobal.rds.ui.actEffectAppearanceConfirm.show(firstItem.id, firstItem.uuid)
            else:
                gameglobal.rds.ui.actEffectAppearanceConfirm.show(itemIds[0], None)
            return

    def trialAppearance(self, appearanceId):
        physicsEffect.trialActEffectAppearance(appearanceId)
