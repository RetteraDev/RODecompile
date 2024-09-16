#Embedded file name: I:/bag/tmp/tw2/res/entities\client/FishGroup.o
import BigWorld
import gameglobal
import clientcom
from guis import ui
from guis import cursor
from iClient import IClient
from helpers import modelServer
from sfx import sfx
from data import fish_data as FD
from data import sys_config_data as SCD
FISH_BOUND_LV1 = 3
FISH_BOUND_LV2 = 6
FISH_BOUND_LV3 = 7
FISH_RADIUS_LV1 = 0.5
FISH_RADIUS_LV2 = 1.0
FISH_RADIUS_LV3 = 1.5

class FishGroup(IClient):

    def __init__(self):
        super(FishGroup, self).__init__()
        self.hp = 1000
        self.mhp = 1000
        self.mp = 1000
        self.mmp = 1000
        self.lv = 1
        self.timer = None
        self.biteTime = 0
        self.isSpecial = False

    def getItemData(self):
        return {'model': gameglobal.FISH_GROUP_MODEL,
         'dye': 'Default'}

    def isUrgentLoad(self):
        return False

    def canSelected(self):
        return False

    def enterWorld(self):
        super(FishGroup, self).enterWorld()
        self.setTargetCapsUse(True)
        self.modelServer = modelServer.SimpleModelServer(self, self.isUrgentLoad())
        fd = FD.data.get(self.fishId, {})
        self.roleName = fd.get('name', '')
        self.biteTime = fd.get('biteTime', 0)
        self.isSpecial = fd.get('specialEffect', 0)

    def leaveWorld(self):
        super(FishGroup, self).leaveWorld()
        self.removeAllFx()
        self._stopTips()

    def afterModelFinish(self):
        super(FishGroup, self).afterModelFinish()
        self.filter = BigWorld.DumbFilter()
        if self.inWorld:
            fishEff = []
            if self.fishCount <= FISH_BOUND_LV1:
                fishEff.append(SCD.data.get('sfxFishNum3', gameglobal.SFX_FISH_NUM3))
            elif self.fishCount <= FISH_BOUND_LV2:
                fishEff.append(SCD.data.get('sfxFishNum6', gameglobal.SFX_FISH_NUM6))
            else:
                fishEff.append(SCD.data.get('sfxFishNum9', gameglobal.SFX_FISH_NUM9))
            if self.isSpecial:
                fishEff.append(SCD.data.get('sfxFishSpecial', gameglobal.SFX_FISH_SPECIAL))
            elif self.radii <= FISH_RADIUS_LV1:
                fishEff.append(SCD.data.get('sfxFishRadius1', gameglobal.SFX_FISH_RADIUS1))
            elif self.radii <= FISH_RADIUS_LV2:
                fishEff.append(SCD.data.get('sfxFishRadius2', gameglobal.SFX_FISH_RADIUS2))
            elif self.radii <= FISH_RADIUS_LV3:
                fishEff.append(SCD.data.get('sfxFishRadius3', gameglobal.SFX_FISH_RADIUS3))
            for effectId in fishEff:
                fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
                 self.getBasicEffectPriority(),
                 self.model,
                 effectId,
                 sfx.EFFECT_UNLIMIT))
                self.addFx(effectId, fx)

    def set_fishCount(self, old):
        BigWorld.callback(self.biteTime, self.refershFishEffect)

    def refershFishEffect(self):
        if self.inWorld:
            if self.fishCount == FISH_BOUND_LV2:
                self.removeFx(SCD.data.get('sfxFishNum9', gameglobal.SFX_FISH_NUM9))
                fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
                 self.getBasicEffectPriority(),
                 self.model,
                 SCD.data.get('sfxFishNum6', gameglobal.SFX_FISH_NUM6),
                 sfx.EFFECT_UNLIMIT))
                self.addFx(SCD.data.get('sfxFishNum6', gameglobal.SFX_FISH_NUM6), fx)
            elif self.fishCount == FISH_BOUND_LV1:
                self.removeFx(SCD.data.get('sfxFishNum6', gameglobal.SFX_FISH_NUM6))
                fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
                 self.getBasicEffectPriority(),
                 self.model,
                 SCD.data.get('sfxFishNum3', gameglobal.SFX_FISH_NUM3),
                 sfx.EFFECT_UNLIMIT))
                self.addFx(SCD.data.get('sfxFishNum3', gameglobal.SFX_FISH_NUM3), fx)

    def showFishTips(self, isShow):
        if isShow:
            self._updateTips()
        else:
            self._stopTips()

    def _stopTips(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            gameglobal.rds.ui.hideFishGroupTips()
            self.timer = 0

    def _updateTips(self):
        self._showFishTips()
        self.timer = BigWorld.callback(0.3, self._updateTips)

    def _showFishTips(self):
        fd = FD.data.get(self.fishId)
        if fd:
            fishName = fd.get('name', '')
            fishLv = fd.get('lv', 1)
            p = BigWorld.player()
            dir = self.position - p.position
            dir.y = 0
            length = dir.length
            x, y = clientcom.worldPointToScreen(self.position)
            title = '%s(%d¼¶)' % (fishName, fishLv)
            distance = '¾àÀë%.1fÃ×' % length
            needBaitDesc = fd.get('needBaitDesc', '')
            if needBaitDesc:
                distance += '\n' + needBaitDesc
            gameglobal.rds.ui.showFishGroupTips(x, y, title, distance)

    def getTopLogoHeight(self):
        return 0.8

    def showTargetUnitFrame(self):
        return False

    def getSeekDist(self):
        return SCD.data.get('fishGroupSeekDist', 30)

    def use(self):
        gameglobal.rds.ui.fishing.show()

    def onTargetCursor(self, enter):
        if enter:
            if ui.get_cursor_state() == ui.NORMAL_STATE:
                ui.set_cursor_state(ui.TARGET_STATE)
                ui.set_cursor(cursor.gather_fish)
                ui.lock_cursor()
        elif ui.get_cursor_state() == ui.TARGET_STATE:
            ui.reset_cursor()
