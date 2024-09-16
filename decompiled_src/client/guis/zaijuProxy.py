#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/zaijuProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gametypes
import skillDataInfo
import const
import utils
import uiUtils
import commQuest
import hotkey as HK
from gameclass import SkillInfo
from guis import uiConst
from guis import hotkey
from guis import hotkeyProxy
from uiProxy import SlotDataProxy
from guis import chickenFoodFactory
from data import sys_config_data as SCD
from data import zaiju_data as ZD
from cdata import game_msg_def_data as GMDD
from data import zaiju_data as ZJD
from data import wing_world_config_data as WWCD

class ZaijuProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(ZaijuProxy, self).__init__(uiAdapter)
        self.modelMap = {'getHpAndMp': self.onGetHpAndMp,
         'leaveZaiju': self.onLeaveZaiju,
         'openBag': self.onOpenBag,
         'openBusinessFind': self.onOpenBusinessFind,
         'getKeyText': self.onGetKeyText,
         'switchCarrouselAni': self.onSwitchCarrouselAni,
         'updateSlots': self.onUpdateSlots}
        self.bindType = 'zaiju'
        self.type = 'zaiju'
        self.binding = {}
        self.skills = [[0, 0]] * 6
        self.serverSkills = {}
        self.mediator = None
        self.exitMediator = None
        self.isShow = False
        self.useSelfSkill = False
        self.zaijuType = uiConst.ZAIJU_TYPE_SKILL
        self.isCarrousel = False
        self.switchSkill = set([])

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ZAIJU:
            self.mediator = mediator
            if self.isCarrousel:
                carrousel = BigWorld.entities[BigWorld.player().carrousel[0]]
                if carrousel:
                    canSwitchCamera = carrousel.canSwitchCameraAni()
                    isLeaveForbid = carrousel.getItemData().get('leaveForbid', 0)
                else:
                    canSwitchCamera = False
                    isLeaveForbid = False
                return uiUtils.dict2GfxDict({'isCarrousel': self.isCarrousel,
                 'canSwitchCamera': bool(canSwitchCamera),
                 'isLeaveForbid': bool(isLeaveForbid)})
            else:
                p = BigWorld.player()
                zjd = ZD.data.get(p._getZaijuNo(), {})
                leaveForbid = zjd.get('leaveForbid', 0)
                if leaveForbid:
                    exitBtn = self.mediator.Invoke('getWidget').GetMember('zaijuMc').GetMember('exitBtn')
                    if exitBtn:
                        exitBtn.SetMember('enabled', GfxValue(False))
                isBusiness = utils.isInBusinessZaiju(p)
                if isBusiness:
                    gameglobal.rds.ui.guildBusinessBag.setBagSlotCount(zjd.get('bagSlotCount', 0))
                bfyZaijuNo = SCD.data.get('bfyZaijuNo', ())
                isChickenFood = p.mapID == const.FB_NO_SPRING_ACTIVITY and p._isOnZaijuOrBianyao() and p._getZaijuOrBianyaoNo() in bfyZaijuNo
                return uiUtils.dict2GfxDict({'isBusiness': isBusiness,
                 'isChickenFood': isChickenFood})
        elif widgetId == uiConst.WIDGET_EXIT_ZAIJU:
            self.exitMediator = mediator
            leaveForbid = ZD.data.get(BigWorld.player()._getZaijuNo(), {}).get('leaveForbid', 0)
            if leaveForbid:
                exitBtn = mediator.Invoke('getWidget').GetMember('exitBtn')
                if exitBtn:
                    exitBtn.SetMember('enabled', GfxValue(False))

    def onGetHpAndMp(self, *arg):
        ret = self.movie.CreateArray()
        p = BigWorld.player()
        ret.SetElement(0, GfxValue(float(p.hp) / p.mhp))
        ret.SetElement(1, GfxValue(float(p.mp) / p.mmp))
        return ret

    def onLeaveZaiju(self, *arg):
        p = BigWorld.player()
        if self.isCarrousel:
            p.leaveCarrousel()
        elif p.inInteractiveObject():
            p.quitInteractiveObj()
        elif self.zaijuType == uiConst.ZAIJU_TYPE_WEAR:
            if p.weaponInHandState() == gametypes.WEAR_BACK_ATTACH:
                p.updateBackWear(True)
                if p.modelServer.backwear.isActionJustSkillWear():
                    p.fashion.stopAllActions()
            elif p.weaponInHandState() == gametypes.WEAR_WAIST_ATTACH:
                p.updateWaistWear(True)
                if p.modelServer.waistwear.isActionJustSkillWear():
                    p.fashion.stopAllActions()
        elif p.isInCoupleRide():
            p.cell.cancelCoupleEmote()
        else:
            self.leaveZaiju()

    def leaveZaiju(self):
        p = BigWorld.player()
        if p.isOnWingWorldCarrier():
            dist = p.qinggongMgr.getDistanceFromGround()
            if dist != p.flyHeight and dist < WWCD.data.get('heightForLeaveCarrier', 5):
                p.cell.applyLeaveWingWorldCarrier()
            else:
                p.showGameMsg(GMDD.data.UNABLE_TO_LEAVE_CARRIER, ())
        elif not utils.isInBusinessZaiju(p) or p.zaijuBag.countZaijuBagNum() <= 0:
            zjd = ZJD.data.get(p._getZaijuNo(), {})
            if zjd.has_key('leaveZaijuNeedShowTip'):
                msg = uiUtils.getTextFromGMD(GMDD.data.LEAVE_ZAIJU_DISAPPREAR_TIP, '')
                self.bagMsgBoxId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, p.cell.leaveZaiju)
            else:
                p.cell.leaveZaiju()
        else:
            bagMsgBoxId = getattr(self, 'bagMsgBoxId', None)
            if bagMsgBoxId:
                gameglobal.rds.ui.messageBox.dismiss(bagMsgBoxId)
            msg = uiUtils.getTextFromGMD(GMDD.data.GUILD_BUSINESS_LEAVE_ZAIJU_HINT, '')
            self.bagMsgBoxId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, p.cell.leaveZaiju)

    def onOpenBag(self, *arg):
        gameglobal.rds.ui.guildBusinessBag.show()

    def onOpenBusinessFind(self, *arg):
        gameglobal.rds.ui.guildBusinessFindPath.show()

    def onNotifySlotUse(self, *arg):
        key = arg[3][0].GetString()
        _, slotId = self.getSlotID(key)
        self.useSkill(0, slotId, False, False)

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        bar, idNum = self.getSlotID(key)
        skillId, skillLv = self.getSkillInfo(idNum)
        if skillId in self.serverSkills:
            skillLv = self.serverSkills[skillId][1]
        if skillId != 0:
            if skillLv != -1:
                tooltip = gameglobal.rds.ui.actionbar.formatToolTip(skillId, skillLv)
            else:
                tooltip = ''
            return tooltip

    def getSlotID(self, key):
        idCon, idItem = key.split('.')
        return (0, int(idItem[4:]))

    def _getKey(self, bar, slotId):
        return 'zaiju.slot%d' % slotId

    def getSlotValue(self, movie, idItem, idCon):
        dataObj = self.movie.CreateObject()
        skillId, skillLv = self.getSkillInfo(idItem)
        iconPath = self.__getSkillIcon(skillId, skillLv)
        dataObj.SetMember('name', GfxValue(iconPath))
        dataObj.SetMember('iconPath', GfxValue(iconPath))
        return dataObj

    def getSkillInfo(self, idItem):
        skillId, skillLv = (0, 0)
        if idItem == None:
            return (skillLv, skillLv)
        else:
            if self.uiAdapter.vehicleSkill.widget:
                if idItem < len(self.uiAdapter.vehicleSkill.skillDataList):
                    skillId = self.uiAdapter.vehicleSkill.skillDataList[idItem]['id']
                    skillLv = self.uiAdapter.vehicleSkill.skillDataList[idItem]['lv']
            else:
                skillId, skillLv = self.skills[idItem]
            return (skillId, skillLv)

    def __getSkillIcon(self, skillId, level = 1):
        if skillId == 0:
            return 'notFound'
        else:
            skills = ZD.data.get(BigWorld.player()._getZaijuNo(), {}).get('skills', [])
            isSkill = False
            for id, lv in skills:
                if skillId == id:
                    isSkill = True
                    break

            if isSkill or self.zaijuType == uiConst.ZAIJU_TYPE_WEAR:
                sd = skillDataInfo.ClientSkillInfo(skillId, level)
                icon = sd.getSkillData('icon', None)
                if icon != None:
                    return 'skill/icon/' + str(icon) + '.dds'
            else:
                icon = commQuest.getEmotionIcon(skillId)
                if icon != None:
                    return 'emote/%d.dds' % icon
            return 'notFound'

    def show(self, skills, zaijuType = uiConst.ZAIJU_TYPE_SKILL):
        self.skills = list(skills)
        self.skills.extend([[0, 0]] * (6 - len(skills)))
        self.zaijuType = zaijuType
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ZAIJU)
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_ZAIJU, True)
        self.isShow = True
        self.isCarrousel = False
        self.hideOtherWidget()

    def showCarrousel(self):
        self.isCarrousel = True
        self.isShow = True
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ZAIJU)
        self.hideOtherWidget()

    def hideOtherWidget(self):
        if gameglobal.rds.ui.actionbar.mc:
            gameglobal.rds.ui.actionbar.mc.Invoke('setVisible', GfxValue(False))
        if gameglobal.rds.ui.actionbar.wsMc:
            gameglobal.rds.ui.actionbar.wsMc.Invoke('setVisible', GfxValue(False))
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_ACTION_BARS, False)
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_WUSHUANG_BARS, False)
        gameglobal.rds.ui.bullet.setVisible(False)
        if gameglobal.rds.ui.qinggongBar.thisMc:
            gameglobal.rds.ui.qinggongBar.thisMc.SetVisible(False)

    def close(self):
        if not gameglobal.rds.ui.isHideAllUI():
            if gameglobal.rds.ui.actionbar.mc:
                gameglobal.rds.ui.actionbar.mc.Invoke('setVisible', GfxValue(True))
            if gameglobal.rds.ui.actionbar.wsMc:
                gameglobal.rds.ui.actionbar.wsMc.Invoke('setVisible', GfxValue(True))
        else:
            gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_ACTION_BARS, True)
            gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_WUSHUANG_BARS, True)
            gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_ZAIJU, False)
        gameglobal.rds.ui.actionbar.updateSlots()
        gameglobal.rds.ui.bullet.setVisible(True)
        if gameglobal.rds.ui.qinggongBar.thisMc:
            gameglobal.rds.ui.qinggongBar.thisMc.Invoke('forceVisibleByOther')
        if gameglobal.rds.ui.guildBusinessBag.mediator:
            gameglobal.rds.ui.guildBusinessBag.hide()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ZAIJU)

    def clearWidget(self):
        self.close()
        self.switchSkill = set([])
        if not self.isCarrousel:
            self.closeExitBtn()

    def reset(self):
        self.binding = {}
        self.skills = [[0, 0]] * 6
        self.serverSkills = {}
        self.isShow = False
        self.useSelfSkill = False
        self.zaijuType = uiConst.ZAIJU_TYPE_SKILL
        self.isCarrousel = False

    def enableSkillInZaiju(self, enabled):
        for skillId in BigWorld.player().getSkills().keys():
            state = uiConst.SKILL_ICON_STAT_USEABLE if enabled else uiConst.SKILL_ICON_STAT_GRAY
            gameglobal.rds.ui.actionbar.setSlotState(skillId, state)

    def showExitBtn(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EXIT_ZAIJU)
        self.enableSkillInZaiju(False)

    def closeExitBtn(self):
        self.exitMediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EXIT_ZAIJU)
        self.enableSkillInZaiju(True)

    def setHpAndMp(self, info):
        if self.mediator:
            ret = []
            val = 1.0
            if info[1] != 0:
                val = float(info[0]) / info[1]
            ret.append(val)
            val = 1.0
            if info[3] != 0:
                val = float(info[2]) / info[3]
            ret.append(val)
            self.mediator.Invoke('setHpAndMp', uiUtils.array2GfxAarry(ret))

    def setServerSkills(self, info):
        self.serverSkills = {}
        for item in info:
            if item[0] not in self.serverSkills:
                self.serverSkills[item[0]] = item

    def useSkill(self, bar, soltId, isDown = False, isKeyMode = True, autoUseSkill = False):
        p = BigWorld.player()
        if isDown:
            gameglobal.rds.bar = bar
            gameglobal.rds.soltId = soltId
        else:
            gameglobal.rds.bar = None
            gameglobal.rds.soltId = None
        if self.mediator and soltId >= len(self.skills):
            p.chatToEventEx(gameStrings.TEXT_ZAIJUPROXY_327, const.CHANNEL_COLOR_RED)
            return
        else:
            skillId = self.getSkillInfo(soltId)[0]
            if skillId == 0:
                return
            isQteSkill = False
            if p.skillQteData.has_key(skillId):
                skillId = p.skillQteData[skillId].qteSkills[0]
                isQteSkill = True
            if self.zaijuType == uiConst.ZAIJU_TYPE_WEAR and isDown == False:
                p.useWearSkillBySlotId(True, soltId)
                return
            zaijuNo = p._getZaijuNo()
            if zaijuNo == 0:
                gameStrings.TEXT_ZAIJUPROXY_343
                return
            if p.mapID == const.FB_NO_SPRING_ACTIVITY:
                cins = chickenFoodFactory.getInstance()
                isLight, canUse, _type, _remain, _total = cins.getSkillState(skillId)
                if not canUse or _remain > 0:
                    return
            skills = ZD.data.get(zaijuNo, {}).get('skills', [])
            isSkill = False
            for id, lv in skills:
                if skillId == id:
                    isSkill = True
                    break

            if isSkill or isQteSkill:
                _, skillLevel = self.getSkillInfo(soltId)
                skillInfo = SkillInfo(skillId, skillLevel)
                needAutoUseSkill = skillInfo.getSkillData('autoUseSkill', 0)
                if autoUseSkill:
                    if not needAutoUseSkill:
                        return
                skillInfo = SkillInfo(skillId, skillLevel)
                isCastSelfKeyDown = hotkey.isCastSelfKeyDown()
                self.useSelfSkill = False
                skillTargetType, skillTargetValue = p.getSkillTargetType(skillInfo)
                if skillTargetValue:
                    if skillTargetType == gametypes.SKILL_TARGET_SELF or skillTargetType == gametypes.SKILL_TARGET_SELF_FRIEND and (isCastSelfKeyDown or p.targetLocked == None or not p.isFriend(p.targetLocked)) or skillTargetType == gametypes.SKILL_TARGET_SELF_ENERMY and (isCastSelfKeyDown or p.targetLocked == None or not p.isEnemy(p.targetLocked)) or skillTargetType == gametypes.SKILL_TARGET_ALL_TYPE and (isCastSelfKeyDown or p.targetLocked == None or not p.targetLocked.IsCombatUnit):
                        p.lastTargetLocked = p.targetLocked
                        p.targetLocked = p
                        self.useSelfSkill = True
                if skillInfo.getSkillData('castType', gametypes.SKILL_FIRE_NORMAL) == gametypes.SKILL_FIRE_SWITCH and isDown:
                    self.switchSkill.add((self._getKey(bar, soltId), skillInfo.getSkillData('switchState', 0)))
                if not isKeyMode:
                    p.useSkillByMouseUp(isDown, skillInfo)
                else:
                    p.useSkillByKeyDown(isDown, skillInfo)
                if self.useSelfSkill:
                    p.targetLocked = p.lastTargetLocked
            else:
                if not p.stateMachine.checkStatus(const.CT_USE_MARKER_NPC):
                    return
                p.cell.onClickItemNearMarker(skillId)
            return

    def _createKeyText(self):
        keyArr = [ ('...' if len(x) > 4 else x) for x in hotkeyProxy.getInstance().shortKey.getKeyDescArray()[0:6] ]
        keyArr.append(hotkeyProxy.getInstance().shortKey.getKeyDescById(HK.KEY_LEAVE_ZAIJU))
        return keyArr

    def onGetKeyText(self, *arg):
        keyArr = self._createKeyText()
        return uiUtils.array2GfxAarry(keyArr, True)

    def onSwitchCarrouselAni(self, *arg):
        if self.isCarrousel:
            BigWorld.player().modelServer.switchCarrouselAni()

    def setSlotKeyText(self, keyArr):
        if self.mediator:
            self.mediator.Invoke('setSlotKeyText', uiUtils.array2GfxAarry(self._createKeyText(), True))

    def onUpdateSlots(self, *arg):
        gameglobal.rds.ui.actionbar.updateSlots()
