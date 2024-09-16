#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/qteNoticeProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gametypes
import hotkey as HK
import ui
from guis import uiConst
from uiProxy import UIProxy
from guis import uiUtils
from guis import hotkey

class QteNoticeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(QteNoticeProxy, self).__init__(uiAdapter)
        self.modelMap = {'getQteInfo': self.onGetQteInfo}
        self.mediator = None
        self.qteInfo = {}
        self.selfKeyText = ''
        self.switchSkill = set([])

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_QTE_SKILL:
            self.mediator = mediator
            self.setQteVisible(False)

    def clearWidget(self):
        self.mediator = None
        self.switchSkill = set([])
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_QTE_SKILL)

    def reset(self):
        self.qteInfo = {}

    @ui.checkWidgetLoaded(uiConst.WIDGET_QTE_SKILL)
    def refreshQteNotice(self, qteInfo):
        self.qteInfo = qteInfo
        if self.mediator:
            self.mediator.Invoke('setQteInfo', self.createQteInfo())

    def createQteInfo(self):
        ret = []
        idx = 0
        for key, val in self.qteInfo.items():
            for skillId, keyBind, lastTime, beginTime in val:
                iconPath = gameglobal.rds.ui.actionbar._getSwithIcon(skillId)
                passedTime = BigWorld.player().getServerTime() - beginTime
                isActionMode = BigWorld.player().getOperationMode() == gameglobal.ACTION_MODE
                ret.append({'iconPath': iconPath,
                 'keyBind': keyBind,
                 'lastTime': lastTime,
                 'passedTime': passedTime,
                 'isActionMode': isActionMode})
                idx += 1

        return uiUtils.array2GfxAarry(ret, True)

    def getHotKeyDes(self, idx):
        if idx == 0:
            return self.selfKeyText
        elif idx > len(HK.SHORTCUT_QTE_SKILL_KEYS):
            return ''
        detial = HK.HKM[HK.SHORTCUT_QTE_SKILL_KEYS[idx - 1]]
        if detial.key != 0:
            return detial.getBrief()
        elif detial.key2 != 0:
            return detial.getBrief(2)
        else:
            return ''

    def useSkill(self, idx, isDown = False, isKeyMode = True):
        if not self.mediator:
            return
        else:
            p = BigWorld.player()
            if idx >= len(self.qteInfo.keys()):
                return
            skillId = self.qteInfo.keys()[idx]
            if not skillId:
                return
            if skillId != p.circleEffect.skillID:
                p.circleEffect.cancel()
            if gameglobal.rds.ui.zaijuV2.widget and not gameglobal.rds.ui.zaijuV2.serverSkills.has_key(skillId):
                skillLevel = gameglobal.rds.ui.zaijuV2.serverSkills[skillId][1]
            else:
                skillLevel = gameglobal.rds.ui.actionbar._getSkillLv(skillId)
            skillInfo = p.getSkillInfo(skillId, skillLevel)
            isCastSelfKeyDown = hotkey.isCastSelfKeyDown()
            useSelfSkill = False
            skillTargetType, skillTargetValue = p.getSkillTargetType(skillInfo)
            if skillTargetValue:
                if p.getOperationMode() == gameglobal.ACTION_MODE and p.optionalTargetLocked and not isCastSelfKeyDown:
                    pass
                elif skillTargetType == gametypes.SKILL_TARGET_SELF or skillTargetType == gametypes.SKILL_TARGET_SELF_FRIEND and (isCastSelfKeyDown or p.targetLocked == None or not p.isFriend(p.targetLocked)) or skillTargetType == gametypes.SKILL_TARGET_SELF_ENERMY and (isCastSelfKeyDown or p.targetLocked == None or not p.isEnemy(p.targetLocked)) or skillTargetType == gametypes.SKILL_TARGET_ALL_TYPE and (isCastSelfKeyDown or p.targetLocked == None or not p.targetLocked.IsCombatUnit):
                    p.lastTargetLocked = p.targetLocked
                    p.targetLocked = p
                    useSelfSkill = True
            if skillInfo.getSkillData('castType', gametypes.SKILL_FIRE_NORMAL) == gametypes.SKILL_FIRE_SWITCH and isDown:
                self.switchSkill.add((skillInfo.getSkillData('switchState', 0), skillId))
            if not isKeyMode:
                p.useSkillByMouseUp(isDown, skillInfo)
            else:
                p.useSkillByKeyDown(isDown, skillInfo)
            if useSelfSkill:
                p.targetLocked = p.lastTargetLocked
            return

    def removeQteInfo(self, srcId):
        if srcId in self.qteInfo:
            self.qteInfo.pop(srcId)
        self.refreshQteNotice(self.qteInfo)

    def setQteVisible(self, visible):
        gameglobal.rds.ui.qteNotice.mediator.Invoke('setVisible', GfxValue(visible))

    def onGetQteInfo(self, *arg):
        ret = self.createQteInfo()
        return ret
