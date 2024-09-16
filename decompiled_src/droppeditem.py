#Embedded file name: /WORKSPACE/data/entities/client/droppeditem.o
import BigWorld
import gameglobal
import const
import formula
import gamelog
from item import Item
from helpers import modelServer
from helpers import fashion
from guis import ui
from guis import cursor
from sfx import sfx
from iClient import IClient
from iDisplay import IDisplay
from data import item_data as ID
from data import sys_config_data as SCD
from data import map_config_data as MCD
from cdata import font_config_data as FCD

class DroppedItem(IClient, IDisplay):
    CURVRATE = 0.2
    SCALEMODELHEIGHT = 1.78
    DROPSPEED = 4.0

    def __init__(self):
        gamelog.debug('jorsef: DroppedItem, __init__', self.quality)
        super(DroppedItem, self).__init__()
        self.firstFetchFinished = False
        self.itemData = ID.data.get(self.itemId, {})
        self.isLeaveWorld = False
        self.trapId = None
        self.srcPosition = None

    def afterModelFinish(self):
        super(DroppedItem, self).afterModelFinish()
        opacityVal = self.getOpacityValue()
        if opacityVal[0] == gameglobal.OPACITY_HIDE:
            self.hide(True)
            return
        self.topLogo.hide(gameglobal.gHideItemLogoFlag)
        modelScale = self.itemData.get('modelScale', 1.0)
        p = BigWorld.player()
        if not p._isOnZaijuOrBianyao():
            modelScale = modelScale * p.model.height / self.SCALEMODELHEIGHT
            node = self.model.node('biped_Obj')
            if node:
                node.scale(modelScale)
        m = BigWorld.entities.get(self.srcMonsterId)
        if self.srcMonsterId and not m:
            gamelog.debug('jorsef:no monster, return')
            self.hide(False)
            self.droppedItemTrapCallback()
        self.filter = BigWorld.DumbFilter() if self.useDummyFilter else BigWorld.AvatarDropFilter()
        self.am.enable = False
        if m:
            self.srcPosition = m.position
        if self.showEffectDelay == 0:
            self.showEffect()
        else:
            self.hide(True)
            BigWorld.callback(self.showEffectDelay, self.showEffect)

    def hide(self, bHide):
        super(DroppedItem, self).hide(bHide)
        self.bHide = bHide
        self.droppedItemTrapCallback()

    def enterWorld(self):
        self.fashion = fashion.Fashion(self.id)
        self.fashion.loadDummyModel()
        self.filter = BigWorld.DumbFilter() if self.useDummyFilter else BigWorld.AvatarDropFilter()
        self.initYaw = self.yaw
        self.modelServer = modelServer.DroppedItemModelServer(self)
        self.trapId = BigWorld.addPot(self.matrix, SCD.data.get('pickNearLength', 4), self.trapCallback)

    def trapCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        if self.itemData.get('type') == Item.BASETYPE_MONEY and enteredTrap:
            self.use()
            return
        self.droppedItemTrapCallback()

    def leaveWorld(self):
        super(DroppedItem, self).leaveWorld()
        self.isLeaveWorld = True
        self.droppedItemTrapCallback()
        if self.trapId != None:
            BigWorld.delPot(self.trapId)
            self.trapId = None

    def enterTopLogoRange(self, rangeDist = -1):
        if not self.firstFetchFinished:
            return
        super(DroppedItem, self).enterTopLogoRange()
        quality = self.quality
        if self.topLogo != None:
            self.topLogo.setLogoColor(FCD.data['item', quality]['color'])
            self._checkPickItem(BigWorld.player(), True)

    def leaveTopLogoRange(self, rangeDist = -1):
        super(DroppedItem, self).leaveTopLogoRange(rangeDist)
        BigWorld.player().removeRefreshDroppedItem(self)

    def showEffect(self):
        if not self.inWorld:
            return
        if self.useDummyFilter:
            self.endFly()
            return
        self.hide(False)
        if self.showEffectDelay:
            sfx.attachEffect(gameglobal.ATTACH_EFFECT_ONNODE, (self.getBasicEffectLv(),
             self.getBasicEffectPriority(),
             self.model,
             'biped_FX',
             SCD.data.get('sfxDropItemTail', 70003),
             sfx.EFFECT_LIMIT,
             1.0))
        try:
            self.model.action('1102')(0, None, 0, 1.0, 10000)
        except:
            pass

        if self.srcPosition != None:
            self.topLogo.hide(True)
            self.model.position = self.srcPosition
            sfx.droppedItemFlyDemo(self.srcPosition, self, self.endFly)
        else:
            self.endFly()

    def onTargetCursor(self, enter):
        if enter:
            if ui.get_cursor_state() == ui.NORMAL_STATE:
                ui.set_cursor_state(ui.TARGET_STATE)
                if (self.position - BigWorld.player().position).length > cursor.TALK_DISTANCE:
                    ui.set_cursor(cursor.pickup_dis)
                else:
                    ui.set_cursor(cursor.pickup)
                ui.lock_cursor()
        elif ui.get_cursor_state() == ui.TARGET_STATE:
            ui.reset_cursor()

    def endFly(self):
        gamelog.debug('jorsef:endFly')
        if not hasattr(self, 'itemData'):
            return
        self.am.enable = True
        self.topLogo.hide(False)
        effs = SCD.data.get('SFX_DROPPED_ITEM', gameglobal.SFX_DROPPED_ITEM)
        quality = self.itemData.get('quality', 0)
        if hasattr(self, 'quality'):
            quality = self.quality
        if effs.has_key(quality):
            eff = effs[quality]
            if self.itemData.get('droppedEff', None):
                eff = self.itemData.get('droppedEff', None)
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
             self.getBasicEffectPriority(),
             self.model,
             eff,
             sfx.EFFECT_LIMIT_MISC,
             gameglobal.EFFECT_LAST_TIME * 25,
             0))
            if fx:
                info = sfx.gEffectInfoMap.getInfo(eff)
                try:
                    self.model.node(info[0][0][1]).scale(*self.model.scale)
                except:
                    fx[0].scale(*self.model.scale)

        self.hide(False)
        self.__playDropItemSound()
        self.droppedItemTrapCallback()
        try:
            self.model.action('1101')()
        except:
            pass

    def __playDropItemSound(self):
        soundIdx = self.itemData.get('dropItemSound', 0)
        gameglobal.rds.sound.playSound(soundIdx)

    def use(self):
        gamelog.debug('jorsef:beforPick')
        if self.beHide:
            return
        p = BigWorld.player()
        if not self._checkPickItem(p):
            return
        if p.isInPUBG():
            return False
        p.pickItem(self)
        gameglobal.rds.sound.playSound(gameglobal.SD_20)

    def getItemData(self):
        gamelog.debug('jorsef: DroppedItem#getItemData', self.itemId)
        modelId = self.itemData.get('modelId', 0)
        gamelog.debug('jorsef: get modelId: ', modelId)
        dye = self.itemData.get('materials', 'Default')
        if modelId == 0:
            return {'model': 30005,
             'dye': dye,
             'fullPath': 'item/model/30005/30005.model',
             'materials': dye}
        soundName = self.itemData.get('dropItemSound', None)
        return {'model': modelId,
         'dye': dye,
         'fullPath': 'item/model/%d/%d.model' % (modelId, modelId),
         'dropItemSound': soundName,
         'materials': dye}

    def droppedItemTrapCallback(self):
        pickNearDist = SCD.data.get('pickNearLength', 4)
        p = BigWorld.player()
        if (self.position - p.position).lengthSquared < pickNearDist * pickNearDist and self.isLeaveWorld == False and self._checkPickItem(p):
            p.droppedItemTrapInCallback((self,))
        else:
            p.droppedItemTrapOutCallback((self,))
        p.droppedItemTrapCallBack((self,))

    def _checkPickItem(self, picker, isUpdateTopLogo = False):
        p = BigWorld.player()
        if not self.inWorld:
            return False
        if not self.getOpacityValue()[0] == gameglobal.OPACITY_FULL:
            return False
        now = picker.getServerTime()
        spaceNo = formula.getMapId(picker.spaceNo)
        pickInterval = SCD.data.get('droppedItemFreePickInterval', const.DROPPED_ITEM_FREE_PICK_INTERVAL)
        droppedItemFreePickInterval = MCD.data.get(spaceNo, {}).get('droppedItemFreePickInterval', pickInterval)
        if now - self.dropTime > droppedItemFreePickInterval:
            if getattr(self, 'visibleGbId', 0) > 0:
                if picker.gbId != self.visibleGbId:
                    return False
                else:
                    return True
            return True
        if self.ownerGroupNUID != 0:
            if picker.groupNUID != self.ownerGroupNUID:
                if isUpdateTopLogo:
                    picker.addRefreshDroppedItem(self)
                return False
        if not self.ownerGbIdList:
            return True
        if picker.gbId in self.ownerGbIdList:
            return True
        if isUpdateTopLogo:
            picker.addRefreshDroppedItem(self)
        return False

    def showTargetUnitFrame(self):
        return False

    def needBlackShadow(self):
        return False
