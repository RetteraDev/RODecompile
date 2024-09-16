#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/skillAppearanceProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import skillDataInfo
import utils
import gamelog
import const
import math
from uiProxy import UIProxy
from asObject import ASObject
from guis.asObject import TipManager
from guis import uiUtils
from guis import ui
from gamestrings import gameStrings
from helpers import skillAppearancesUtils
from callbackHelper import Functor
from data import skill_general_template_data as SGTD
from data import skill_appearance_data as SAD
from data import skill_appearance_config_data as SACD
from data import consumable_item_data as CID
from cdata import game_msg_def_data as GMDD

class SkillAppearanceProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SkillAppearanceProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SKILL_APPEARANCE, self.hide)
        self.addEvent(events.EVENT_SKILL_APPERANCE, self.onSkillAppearanceChanged, isGlobal=True)

    def reset(self):
        if self.widget:
            gamelog.debug('ypc@ skillAppearance reset!')
            self.widget.removeToCache(self.skillTip)
            self.widget.removeToCache(self.miniSkillTip)
        self.skillTip = None
        self.miniSkillTip = None
        self.lastRefreshTime = 0

    def _registerASWidget(self, widgetId, widget):
        gamelog.debug('ypc@ skillAppearance _registerASWidget!')
        if widgetId == uiConst.WIDGET_SKILL_APPEARANCE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.reset()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SKILL_APPEARANCE)

    def show(self):
        if not gameglobal.rds.configData.get('enableSkillAppearance', False):
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SKILL_APPEARANCE)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.main.itemRenderer = 'SkillAppearance_AppearanceItem'
        self.widget.main.lableFunction = self.skillItemRenderFunction
        self.widget.main.dataArray = []
        if not self.skillTip:
            self.skillTip = self.widget.getInstByClsName('SKillAppearance_Tip')
        if not self.miniSkillTip:
            self.miniSkillTip = self.widget.getInstByClsName('SkillAppearance_MiniTip')
        self.widget.addEventListener(events.EVENT_ENTER_FRAME, self.handleEnterFrame, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.main.dataArray = self._getSkillAppearanceData()
        self.lastRefreshTime = utils.getNow()

    def skillItemRenderFunction(self, *args):
        itemData = ASObject(args[3][0])
        item = ASObject(args[3][1])
        item.detail.itemRenderer = 'SkillAppearance_DetailItem'
        item.detail.lableFunction = self.skillDetailItemRenderFunction
        detailDataArray = []
        currentDeadline = 0
        for detail in itemData.appearanceIds:
            aid = detail.get('appearanceId', -1)
            isCurrent = aid == itemData.currAppearanceId
            deadLine = detail.get('deadLine', 0)
            if isCurrent:
                currentDeadline = deadLine
            detailDataArray.append({'skillId': itemData.skillId,
             'appearanceId': aid,
             'deadLine': deadLine,
             'isCurrent': isCurrent})

        detailDataArray.sort(key=lambda x: x.get('appearanceId', -1))
        item.detail.dataArray = detailDataArray
        item.detail.validateNow()
        iconPath, skillName = self._getSkillIconPath(itemData.skillId, itemData.currAppearanceId)
        item.skill.icon.enabled = True
        item.skill.icon.focusable = False
        item.skill.icon.slot.dragable = False
        item.skill.icon.slot.setItemSlotData({'iconPath': iconPath})
        item.skill.skillName.text = skillName
        item.skill.icon.data = {'skillId': itemData.skillId,
         'appearanceId': itemData.currAppearanceId,
         'deadline': currentDeadline}
        if itemData.currAppearanceId == 0:
            TipManager.addTipByFunc(item.skill.icon, self.onMiniTipShow, item.skill.icon, False)
        else:
            TipManager.addTipByFunc(item.skill.icon, self.onTipShow, item.skill.icon, False)

    def skillDetailItemRenderFunction(self, *args):
        itemData = ASObject(args[3][0])
        item = ASObject(args[3][1])
        item.icon.focusable = False
        item.icon.addEventListener(events.BUTTON_CLICK, self.handleDetailItemClick, False, 0, True)
        item.icon.selected = itemData.isCurrent
        item.icon.data = {'skillId': itemData.skillId,
         'appearanceId': itemData.appearanceId,
         'deadline': itemData.deadLine}
        item.indate.visible = self._isIndate(itemData.deadLine)
        iconPath, skillName = self._getSkillIconPath(itemData.skillId, itemData.appearanceId)
        item.icon.slot.fitSize = True
        item.icon.slot.dragable = False
        item.icon.slot.setItemSlotData({'iconPath': iconPath})
        if itemData.deadLine == skillAppearancesUtils.APPEARANCE_DEADLINE_NOT_ACTIVE or self._isExpire(itemData.deadLine):
            item.icon.slot.setSlotState(uiConst.ITEM_DISABLE)
        else:
            item.icon.slot.setSlotState(uiConst.ITEM_NORMAL)
        if itemData.appearanceId == 0:
            TipManager.addTipByFunc(item.icon, self.onMiniTipShow, item.icon, False)
        else:
            TipManager.addTipByFunc(item.icon, self.onTipShow, item.icon, False)
        item.icon.slot.validateNow()

    @ui.callFilter(1, False)
    def handleDetailItemClick(self, *args):
        e = ASObject(args[3][0])
        skillId = e.target.data.skillId
        appearanceId = e.target.data.appearanceId
        deadline = e.target.data.deadline
        p = BigWorld.player()
        if self._isAppearanceActive(deadline, utils.getNow()):
            if hasattr(p, 'skillAppearancesDetail'):
                p.skillAppearancesDetail.endTrialAppearance()
                if p.skillAppearancesDetail.getCurrentAppearance(skillId) != appearanceId:
                    gamelog.debug('ypc@ switchSkillAppearance! ', e.target.data.skillId, e.target.data.appearanceId)
                    p.cell.switchSkillAppearance(skillId, appearanceId)
        else:
            trialTime = SACD.data.get('TrialTime', 10)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.SKILL_APPEARANCE_MESSAGE_BOX % trialTime, yesCallback=Functor(self.activeAppearance, skillId, appearanceId), yesBtnText=gameStrings.SKILL_APPEARANCE_MESSAGE_BOX_ACTIVE, noCallback=Functor(self.trialAppearance, skillId, appearanceId), noBtnText=gameStrings.SKILL_APPEARANCE_MESSAGE_BOX_TRIAL)

    def handleEnterFrame(self, *args):
        self._checkAnyAppearanceChanged()

    def activeAppearance(self, skillId, appearanceId):
        p = BigWorld.player()
        itemIds = SAD.data.get(appearanceId, {}).get('useitems', ())
        if not itemIds or len(itemIds) == 0:
            return
        else:
            firstItem = None
            for id in itemIds:
                page, pos = p.inv.findItemInPages(id)
                if page != const.CONT_NO_PAGE and pos != const.CONT_NO_POS:
                    firstItem = p.inv.getQuickVal(page, pos)
                    break

            if firstItem:
                gameglobal.rds.ui.skillAppearanceConfirm.show(firstItem.id, firstItem.uuid)
            else:
                gameglobal.rds.ui.skillAppearanceConfirm.show(itemIds[0], None)
            return

    def trialAppearance(self, skillId, appearanceId):
        p = BigWorld.player()
        if hasattr(p, 'skillAppearancesDetail'):
            p.skillAppearancesDetail.trailAppearance(skillId, appearanceId)

    def getDeadlineText(self, deadline):
        if deadline == 0:
            return gameStrings.SKILL_APPEARANCE_DEADLINE_FOREVER
        if deadline == -1:
            return gameStrings.SKILL_APPEARANCE_DEADLINE_NOT_ACTIVE
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
                return gameStrings.SKILL_APPEARANCE_DEADLINE_NOT_ACTIVE
            return gameStrings.SKILL_APPEARANCE_DEADLINE_TIME % timeTxt
        return gameStrings.SKILL_APPEARANCE_DEADLINE_NOT_ACTIVE

    def getDeadlineTextPure(self, deadline):
        if deadline == 0:
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

    def onSkillAppearanceChanged(self, event):
        if event.data.get('changed', False):
            BigWorld.player().showGameMsg(GMDD.data.COMMON_MSG, gameStrings.SKILL_APPEARANCE_CHANGE_SUCCESS)
            gameglobal.rds.ui.actionbar.refreshActionbar()
        self.refreshInfo()

    def onTipShow(self, *args):
        if not self.widget:
            gamelog.debug('ypc@ onTipShow not self.widget! ')
            return None
        else:
            target = ASObject(args[3][0])
            if not self.skillTip:
                self.skillTip = self.widget.getInstByClsName('SKillAppearance_Tip')
            self.skillTip.visible = True
            gamelog.debug('ypc@ onTipShow! ', self.skillTip.name)
            iconPath, skillName = self._getSkillIconPath(target.data.skillId, target.data.appearanceId)
            self.skillTip.skillName.text = skillName
            self.skillTip.deadline.text = self.getDeadlineText(target.data.deadline)
            if self._isAppearanceActive(target.data.deadline, utils.getNow()):
                self.skillTip.locked.text = gameStrings.SKILL_APPEARANCE_CLICKTIP_USE
            else:
                self.skillTip.locked.text = gameStrings.SKILL_APPEARANCE_CLICKTIP_TRY
            TipManager.showImediateTip(target, self.skillTip)
            return None

    def onMiniTipShow(self, *args):
        if not self.widget:
            gamelog.debug('ypc@ onMiniTipShow not self.widget! ')
            return None
        else:
            target = ASObject(args[3][0])
            if not self.miniSkillTip:
                self.miniSkillTip = self.widget.getInstByClsName('SkillAppearance_MiniTip')
            self.miniSkillTip.visible = True
            gamelog.debug('ypc@ onMiniTipShow! ', self.miniSkillTip.name)
            iconPath, skillName = self._getSkillIconPath(target.data.skillId, target.data.appearanceId)
            self.miniSkillTip.skillName.text = skillName
            TipManager.showImediateTip(target, self.miniSkillTip)
            return None

    def _getSkillIconPath(self, skillId, appearanceId):
        p = BigWorld.player()
        if not appearanceId or appearanceId <= 0:
            playerSkillInfo = p.skills.get(skillId)
            skillInfo = skillDataInfo.ClientSkillInfo(skillId, playerSkillInfo.level if playerSkillInfo else 1)
        else:
            skillInfo = skillDataInfo.AppearanceSkillInfo(skillId, appearanceId)
        iconPath = uiUtils.getSkillIconPath(skillInfo, uiConst.ICON_SIZE40)
        if not appearanceId or appearanceId <= 0:
            skillName = self._getSkillName(skillId)
        else:
            skillName = self._getSkillAppearanceName(appearanceId)
        return (iconPath, skillName)

    def _isIndate(self, deadLine):
        return deadLine != 0 and utils.getNow() < deadLine

    def _isExpire(self, deadLine):
        return deadLine == -1 or deadLine > 0 and deadLine < utils.getNow()

    def _getSkillName(self, skillId):
        return SGTD.data.get(skillId).get('name', '')

    def _getSkillAppearanceName(self, appearanceId):
        return SAD.data.get(appearanceId).get('nName', '')

    def _getSkillAppearanceData(self):
        allData = skillAppearancesUtils.getPlayerAllSkillsWithAppearance()
        if not allData:
            return []
        ret = []
        for skill, detail in allData.iteritems():
            tmp = detail.copy()
            appearances = []
            poptmp = tmp.pop(const.SKILL_APPEARANCE_KEY_INFO, {})
            for aid, deadLine in poptmp.iteritems():
                appearances.append({'appearanceId': aid,
                 'deadLine': deadLine})

            appearances.sort(key=lambda x: x['appearanceId'])
            tmp.update({'skillId': skill,
             const.SKILL_APPEARANCE_KEY_INFO: appearances})
            ret.append(tmp)

        ret.sort(key=lambda x: x['skillId'])
        return ret

    @ui.callFilter(5, False)
    def _checkAnyAppearanceChanged(self):
        allSkillAppearanceData = self._getSkillAppearanceData()
        for skillData in allSkillAppearanceData:
            allAppearanceData = skillData.get(const.SKILL_APPEARANCE_KEY_INFO, [])
            for detail in allAppearanceData:
                deadline = detail.get('deadLine', -1)
                if self._isAppearanceActive(deadline, self.lastRefreshTime) != self._isAppearanceActive(deadline, utils.getNow()):
                    gamelog.debug('ypc@ _checkAnyAppearanceChanged')
                    gameglobal.rds.ui.actionbar.refreshActionbar()
                    self.refreshInfo()
                    return

    def _isAppearanceActive(self, deadline, now):
        return deadline == 0 or deadline > 0 and now < deadline
