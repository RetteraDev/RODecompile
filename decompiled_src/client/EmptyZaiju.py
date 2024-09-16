#Embedded file name: I:/bag/tmp/tw2/res/entities\client/EmptyZaiju.o
import random
import BigWorld
import gameglobal
import gametypes
import utils
import const
from guis import ui
from guis import cursor
from iCombatUnit import ICombatUnit
from iDisplay import IDisplay
from iNpc import INpc
from sfx import sfx
from data import empty_zaiju_data as EZD
from data import sys_config_data as SCD
from data import zaiju_data as ZD
from data import yabiao_config_data as YCD

class EmptyZaiju(INpc, ICombatUnit):
    IsCombatUnit = True
    IsNaiveCombatUnit = True
    IsEmptyZaiju = True

    def __init__(self):
        super(EmptyZaiju, self).__init__()
        self.trapId = None
        self.isLeaveWorld = False
        self.holdModelByPlayer = False
        self.keepEffects = []

    def releaseKeepEffects(self):
        if self.keepEffects:
            for ef in self.keepEffects:
                if ef:
                    ef.stop()

            self.keepEffects = []

    def getItemData(self):
        itemData = EZD.data.get(self.zaijuNo, None)
        modelId = itemData.get('modelId')
        modelScale = itemData.get('modelScale', 1.0)
        res = {'dye': 'Default',
         'model': modelId,
         'modelScale': modelScale}
        return res

    def needBlackShadow(self):
        data = EZD.data.get(self.zaijuNo, None)
        noBlackUfo = data.get('noBlackUfo', False)
        return not noBlackUfo

    def use(self):
        if self.isValidUse():
            BigWorld.player().cell.useEmptyZaiju(self.id)

    def isValidUse(self):
        if self.visibility == const.VISIBILITY_HIDE:
            return False
        player = BigWorld.player()
        if self.ownerGbId != player.gbId:
            ezd = EZD.data.get(self.zaijuNo)
            useType = ezd['useType']
            if useType == gametypes.ZAIJU_USE_GROUP:
                if self.groupNUID == 0 or self.groupNUID != player.groupNUID:
                    return False
            elif useType == gametypes.ZAIJU_USE_TEAM:
                if self.groupNUID == 0 or self.groupNUID != player.groupNUID or self.groupIndex < 0 or not utils.isSameTeam(self.groupIndex, player.groupIndex):
                    return False
            elif useType == gametypes.ZAIJU_USE_GUILD:
                if self.guildNUID == 0 or self.guildNUID != player.guildNUID:
                    return False
            elif useType == gametypes.ZAIJU_USE_CAMP:
                if player.inFuben():
                    if self.tCamp != player.tCamp:
                        return False
                elif player.inWorldWarEx():
                    if self.tCamp != player.getWorldWarSide():
                        return False
                elif self.camp != player.camp:
                    return False
        return True

    def enterWorld(self):
        super(EmptyZaiju, self).enterWorld()
        self.initYaw = self.yaw
        self.trapId = BigWorld.addPot(self.matrix, SCD.data.get('pickUpLength', 4), self.trapCallback)

    def afterModelFinish(self):
        super(EmptyZaiju, self).afterModelFinish()
        self.filter = BigWorld.DumbFilter()
        self.filter.clientYawMinDist = 0.0
        self.filter.setYaw(self.initYaw)
        itemData = EZD.data.get(self.zaijuNo, None)
        scale = itemData.get('modelScale', 1.0)
        self.model.scale = (scale, scale, scale)
        if self.isValidUse() and itemData.get('showTopIndicator', None):
            self.topLogo.showSkillIndicator()
        effs = itemData.get('keepEffects')
        if effs:
            effectScale = itemData.get('effectScale', None)
            for i in effs:
                priority = self.getBasicEffectPriority()
                res = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getSkillEffectLv(),
                 priority,
                 self.model,
                 i,
                 sfx.EFFECT_LIMIT_MISC,
                 -1))
                if res:
                    if effectScale:
                        for fxItem in res:
                            fxItem.scale(effectScale, effectScale, effectScale)

                    self.keepEffects += res

        if itemData.get('isYabiao'):
            self.yabiaoTrapId = BigWorld.addPot(self.matrix, YCD.data['yabiaoWarningScope'], self.leaveYabiaoCallback)

    def leaveWorld(self):
        self.releaseKeepEffects()
        super(EmptyZaiju, self).leaveWorld()
        self.isLeaveWorld = True
        self.zaijuTrapCallback()
        if self.trapId != None:
            BigWorld.delPot(self.trapId)
            self.trapId = None
        if hasattr(self, 'yabiaoTrapId') and self.yabiaoTrapId:
            BigWorld.delPot(self.yabiaoTrapId)
            self.yabiaoTrapId = None

    def onTargetCursor(self, enter):
        p = BigWorld.player()
        if p.inWorldWarEx():
            if enter:
                relation = BigWorld.player().playerRelation(self)
                if relation == gametypes.RELATION_ENEMY:
                    if ui.get_cursor_state() == ui.NORMAL_STATE:
                        ui.reset_cursor()
                        ui.set_cursor_state(ui.ZAIJU_STATE)
                        ui.set_cursor(cursor.attack)
                        ui.lock_cursor()
                        return
        if enter and self.isValidUse():
            if ui.get_cursor_state() == ui.NORMAL_STATE:
                ui.reset_cursor()
                ui.set_cursor_state(ui.ZAIJU_STATE)
                ui.set_cursor(cursor.zaiju)
                ui.lock_cursor()
        elif ui.get_cursor_state() == ui.ZAIJU_STATE or ui.get_cursor_state() == ui.TARGET_STATE:
            ui.reset_cursor()

    def getOpacityValue(self):
        return IDisplay.getOpacityValue(self)

    def trapCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        self.zaijuTrapCallback()

    def zaijuTrapCallback(self):
        pickNearDist = SCD.data.get('pickUpLength', 4)
        ent = []
        if (self.position - BigWorld.player().position).length <= pickNearDist and self.isLeaveWorld == False and self.isValidUse():
            ent.append(self)
        BigWorld.player().zaijuTrapCallBack(ent)

    def leaveYabiaoCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        if enteredTrap:
            return
        player = BigWorld.player()
        if player.groupNUID == self.groupNUID and player.ybStatus:
            player.cell.leaveYabiao(self.groupNUID, self.position)

    def beHit(self, host, damage = None, callback = None, forceBeHitAct = False, clientSkillInfo = None):
        if not self.inWorld:
            return
        if self.life == gametypes.LIFE_DEAD:
            return
        beHitActions = EZD.data.get(self.zaijuNo, {}).get('beHitAction', ())
        if beHitActions:
            beHitAction = random.choice(beHitActions)
            if beHitAction:
                try:
                    act = self.model.action(beHitAction)
                except:
                    return

                act.enableAlpha(True)
                act(0)

    def getFKey(self):
        return EZD.data.get(self.zaijuNo, {}).get('fKey', 0)

    def getWorldWarSide(self):
        ezd = EZD.data[self.zaijuNo]
        zjd = ZD.data[ezd['zaijuNo']]
        if zjd.get('onlySoulEnemy'):
            return gametypes.WORLD_WAR_CAMP_DEFEND
        else:
            return self.tempCamp

    def set_visibility(self, old):
        super(EmptyZaiju, self).set_visibility(old)
        self.zaijuTrapCallback()
        itemData = EZD.data.get(self.zaijuNo, None)
        if self.topLogo:
            if self.isValidUse() and itemData.get('showTopIndicator', None):
                self.topLogo.showSkillIndicator()
            else:
                self.topLogo.removeSkillIndicator()
