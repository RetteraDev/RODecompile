#Embedded file name: /WORKSPACE/data/entities/client/treasurebox.o
import BigWorld
import gameglobal
import skillDataInfo
import gametypes
import copy
import const
import utils
from random import choice
import clientcom
from helpers import tintalt
from helpers import action as ACT
from iBox import IBox
from iDisplay import IDisplay
from sfx import sfx
from guis import ui
from guis import cursor
from helpers import scenario
from data import treasure_box_data as TBD
from data import sys_config_data as SCD
from cdata import font_config_data as FCD
from cdata import game_msg_def_data as GMDD
from data import hunt_ghost_config_data as HGCD
ADD_TYPE_FIELDS = 0
RANDOM_EFFECT = 0
ALL_EFFECT = 2

class TreasureBox(IBox, IDisplay):
    FIRE_BURN_MAP = 'system/maps/firedistortion01.bmp'
    FIRE_FLAME_MAP = 'system/maps/flame01.bmp'
    FIRE_SHADER = 'burndead'
    FIRE_TIME = 5
    BINGDONG_SHADER = 'blendout'
    BINGDONG_TIME = 0.5
    IsBox = True

    def __init__(self):
        super(TreasureBox, self).__init__()
        self.validInBianyao = self.getItemData().get('validInBianyao', gametypes.FUNCTION_INVALID_FOR_YAO)

    def getItemData(self):
        itemData = TBD.data.get(self.treasureBoxId, None)
        if not itemData:
            return {'model': gameglobal.defaultModelID,
             'dye': 'Default'}
        boxData = itemData
        randomModels = boxData.get('randomModels', None)
        if randomModels:
            for randomItem in randomModels:
                if randomItem[0] == self.modelId:
                    boxData = copy.copy(boxData)
                    boxData['model'] = randomItem[0]
                    boxData['bornAction'] = randomItem[2]
                    boxData['useAction'] = randomItem[3]
                    boxData['beUsedAction'] = randomItem[4]
                    boxData['effectId'] = randomItem[5]
                    boxData['openEffectId'] = randomItem[6]
                    break

        return boxData

    def needBlackShadow(self):
        data = self.getItemData()
        noBlackUfo = data.get('noBlackUfo', False)
        return not noBlackUfo

    def getModelScale(self):
        scale = self.getItemData().get('modelScale', 1.0)
        return (scale, scale, scale)

    def leaveWorld(self):
        super(TreasureBox, self).leaveWorld()
        self.removeAllFx()
        self.delLingShiExtraTint()

    def addTint(self, tintId, force = False):
        if not self.inWorld:
            return
        tintName, tintPrio, tint = skillDataInfo.getTintDataInfo(self, tintId)
        tintalt.addExtraTint(self.model, tintName, [tint, BigWorld.shaderTime()], 0, None)

    def onBoxOpened(self, ownerId):
        boxData = self.getItemData()
        self.removeEffects(boxData.get('effectBeforeOpen'))
        openedActions = []
        openEffectIds = boxData.get('openEffectId', None)
        openSoundId = boxData.get('openSoundId', None)
        if openSoundId:
            gameglobal.rds.sound.playSound(openSoundId)
        if openEffectIds:
            for openEffectId in openEffectIds:
                sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getEquipEffectLv(),
                 self.getEquipEffectPriority(),
                 self.model,
                 openEffectId,
                 sfx.EFFECT_UNLIMIT))

        useAction = boxData.get('useAction')
        beUsedAction = boxData.get('beUsedAction')
        beUsedTint = boxData.get('beUsedTint')
        useAction and openedActions.append(useAction)
        beUsedAction and openedActions.append(beUsedAction)
        openedActions and self.fashion.playAction(openedActions, ACT.DEAD_ACTION)
        beUsedTint and self.addTint(beUsedTint)
        if boxData.get('pickType', gametypes.TREASURE_BOX_DROPPEDITEM) != gametypes.TREASURE_BOX_PERSONAL:
            if getattr(self, 'remainOpenCnt', 0) <= 0:
                self.isLeaveWorld = True
        self.boxTrapCallback()

    def enterTopLogoRange(self, rangeDist = -1):
        if not self.firstFetchFinished:
            return
        super(TreasureBox, self).enterTopLogoRange(rangeDist)
        self.refreshOpacityState()
        if self.topLogo:
            self.topLogo.setLogoColor(FCD.data['item', self.quality]['color'])

    def set_status(self, old):
        cancelEvent = TBD.data.get(self.treasureBoxId, {}).get('cancelEvent', 0)
        if self.status == const.ST_OPENED and cancelEvent:
            self.setTargetCapsUse(False)
            gameglobal.rds.ui.pressKeyF.hide()

    def resetBox(self):
        if self.model and self.model.inWorld:
            self.model.tpos()

    def afterModelFinish(self):
        super(TreasureBox, self).afterModelFinish()
        self.refreshOpacityState()
        if self.status == const.ST_OPENED:
            cancelEvent = TBD.data.get(self.treasureBoxId, {}).get('cancelEvent', 0)
            cancelEvent and self.setTargetCapsUse(False)
            boxData = self.getItemData()
            beUsedAction = boxData.get('beUsedAction')
            effectId = boxData.get('effectId')
            beUsedAction and self.fashion.playAction([beUsedAction], ACT.DEAD_ACTION)
            effectId and self.addEffects(effectId)
            return
        boxData = self.getItemData()
        bornAction = boxData.get('bornAction')
        bornAction and self.fashion.playSingleAction(bornAction, callback=self.resetBox)
        bornSoundId = boxData.get('bornSoundId')
        if bornSoundId:
            gameglobal.rds.sound.playSound(bornSoundId)
        self.addEffects(boxData.get('effectId'))
        self.addEffects(boxData.get('effectBeforeOpen'))
        self.filter = BigWorld.DumbFilter() if self.useDummyFilter else BigWorld.AvatarDropFilter()
        collideRadiusRatio = boxData.get('collide', 0.0)
        if collideRadiusRatio > 0.0:
            opacityVal, _ = self.getOpacityValue()
            if opacityVal == gameglobal.OPACITY_FULL:
                self.collideWithPlayer = True
                self.am.collideWithPlayer = True
                self.am.collideRadius = collideRadiusRatio
            else:
                self.collideWithPlayer = False
                self.am.collideWithPlayer = False
        self.addLingShiExtraTint()

    def use(self):
        p = BigWorld.player()
        boxData = self.getItemData()
        if boxData.has_key('needLvRange') and (p.lv < boxData['needLvRange'][0] or p.lv > boxData['needLvRange'][1]):
            lvNotEnoughMsgId = boxData.get('lvNotEnoughMsgId', 0)
            if lvNotEnoughMsgId:
                p.showGameMsg(lvNotEnoughMsgId, (boxData['needLvRange'][0],))
                return False
            p.showGameMsg(GMDD.data.OPEN_BOX_FAIL_LV, (boxData['needLvRange'][0], boxData['needLvRange'][1]))
            return False
        if gameglobal.rds.configData.get('enableHuntGhost', False):
            ghostInfos = gameglobal.rds.ui.huntGhost.bigBoxInfo
            if ghostInfos:
                bornTime, _ = ghostInfos.get(self.id, (0, 0))
                if bornTime and utils.getNow() - bornTime < HGCD.data.get('BigBoxExistTime', 120):
                    p.showGameMsg(GMDD.data.HUNT_GHOST_BIG_BOX_LOCKED)
                    return False
        if p.checkCanDoAction():
            super(TreasureBox, self).use()

    def refreshOpacityState(self):
        super(TreasureBox, self).refreshOpacityState()
        opacityVal = self.getOpacityValue()
        if opacityVal[0] == gameglobal.OPACITY_FULL and self.topLogo:
            self.topLogo.showBlood(False)
        self.boxTrapCallback()

    def showTargetUnitFrame(self):
        return False

    def onTargetCursor(self, enter):
        if enter:
            if ui.get_cursor_state() == ui.NORMAL_STATE:
                ui.set_cursor_state(ui.TARGET_STATE)
                cursorIcon = TBD.data.get(self.treasureBoxId, {}).get('cursorIcon', None)
                if (self.position - BigWorld.player().position).length > cursor.TALK_DISTANCE:
                    if cursorIcon:
                        icon_dis = getattr(cursor, cursorIcon[1], '')
                        ui.set_cursor(icon_dis)
                    else:
                        ui.set_cursor(cursor.usebox_dis)
                elif cursorIcon:
                    icon = getattr(cursor, cursorIcon[0], '')
                    ui.set_cursor(icon)
                else:
                    ui.set_cursor(cursor.usebox)
                ui.lock_cursor()
        elif ui.get_cursor_state() == ui.TARGET_STATE:
            ui.reset_cursor()

    def enterWorld(self):
        super(TreasureBox, self).enterWorld()
        self.filter = BigWorld.DumbFilter() if self.useDummyFilter else BigWorld.AvatarDropFilter()

    def getOpacityValue(self):
        tbd = self.getItemData()
        p = BigWorld.player()
        if tbd.has_key('islingshi'):
            return clientcom.getEntityLingShiOpacityValue(tbd)
        if gameglobal.SCENARIO_PLAYING != gameglobal.SCENARIO_END:
            scenarioIns = scenario.Scenario.PLAY_INSTANCE if scenario.Scenario.PLAY_INSTANCE else scenario.Scenario.INSTANCE
            if scenarioIns and scenarioIns.hideTreasureBox:
                return (gameglobal.OPACITY_HIDE, False)
        if self.treasureBoxId in getattr(p, 'invisibleTreasureBoxInfo', []):
            return (gameglobal.OPACITY_HIDE, False)
        return super(TreasureBox, self).getOpacityValue()

    def addLingShiExtraTint(self):
        p = BigWorld.player()
        if not getattr(p, 'lingShiFlag', False):
            return
        lingShiTintName = self.getItemData().get('lingShiTintName', '')
        if lingShiTintName:
            tintalt.ta_reset(self.allModels)
            tintalt.ta_add(self.allModels, lingShiTintName, tintType=tintalt.NPC_LINGSHI)

    def delLingShiExtraTint(self):
        tintalt.ta_reset(self.allModels)

    def addEffects(self, effectData):
        if not effectData:
            return
        effectList = []
        if isinstance(effectData, int):
            effectList.append(effectData)
        else:
            effectList = list(effectData)
            effectType = effectList.pop(ADD_TYPE_FIELDS)
            if effectType == RANDOM_EFFECT:
                selecteId = choice(effectList)
                effectList = [selecteId]
            elif effectType == ALL_EFFECT:
                pass
        for effectId in effectList:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getEquipEffectLv(),
             self.getEquipEffectPriority(),
             self.model,
             effectId,
             sfx.EFFECT_UNLIMIT))
            fx and self.addFx(effectId, fx)

    def removeEffects(self, effectTuple):
        if not effectTuple:
            return
        for effectId in effectTuple[1:]:
            self.removeFx(effectId)

    def setTargetCapsUse(self, bVisible):
        cancelEvent = TBD.data.get(self.treasureBoxId, {}).get('cancelEvent', 0)
        if self.status == const.ST_OPENED and cancelEvent:
            bVisible = False
        super(TreasureBox, self).setTargetCapsUse(bVisible)
