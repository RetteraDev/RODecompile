#Embedded file name: /WORKSPACE/data/entities/client/lifecsmitem.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gametypes
import utils
from helpers import modelServer
from helpers import fashion
from iClient import IClient
from guis.ui import gbk2unicode
from guis import ui
from guis import cursor
from guis import uiUtils
from sfx import sfx
from data import life_skill_collection_data as LSCD
from data import life_skill_resource_data as LSRD
from data import sys_config_data as SCD
from data import marriage_config_data as MCD
from cdata import game_msg_def_data as GMDD
from cdata import living_item_phase_inverted_data as LIID
from cdata import font_config_data as FCD
DUMMY_MODEL_ID = 39999

class LifeCsmItem(IClient):

    def __init__(self):
        super(LifeCsmItem, self).__init__()
        self.firstFetchFinished = False
        self.isLeaveWorld = False
        self.trapId = 0
        self.data = LSCD.data.get(self._getItemId(), {})

    def enterWorld(self):
        super(LifeCsmItem, self).enterWorld()
        self.fashion = fashion.Fashion(self.id)
        self.fashion.loadDummyModel()
        self.modelServer = modelServer.SimpleModelServer(self)
        self.trapId = BigWorld.addPot(self.matrix, SCD.data.get('pickUpLength', 4), self.trapCallback)

    def afterModelFinish(self):
        super(LifeCsmItem, self).afterModelFinish()
        self.setTargetCapsUse(True)
        triggerEff = self.data.get('triggerEff', 0)
        triggerEffScale = self.data.get('triggerEffScale', 1.0)
        if triggerEff:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
             self.getBasicEffectPriority(),
             self.model,
             triggerEff,
             sfx.EFFECT_UNLIMIT))
            if fx:
                if triggerEffScale:
                    for fxItem in fx:
                        fxItem.scale(triggerEffScale, triggerEffScale, triggerEffScale)

                self.addFx(triggerEff, fx)
        collideRadiusRatio = LSCD.data.get(self._getItemId(), {}).get('collide', 0.0)
        if collideRadiusRatio > 0.0:
            self.collideWithPlayer = True
            self.am.collideWithPlayer = True
            self.am.collideRadius = collideRadiusRatio

    def enterTopLogoRange(self, rangeDist = -1):
        if not self.firstFetchFinished:
            return
        super(LifeCsmItem, self).enterTopLogoRange()
        resourceId = self.data['resourceId']
        quality = LSRD.data[resourceId]['quality']
        if self.topLogo != None:
            self.topLogo.setLogoColor(FCD.data['item', quality]['color'])
            if hasattr(self.topLogo, 'movie'):
                self.topLogo.invokeMethod('setName', GfxValue(gbk2unicode(self.getColorName())))
                titleName, style = self.getTitleName()
                self.topLogo.setAvatarTitle(titleName, style)

    def getTitleName(self):
        husbandName = getattr(self, 'husbandName', '')
        if husbandName:
            marriageTitle, style = MCD.data.get('lifeCsmItemTitleName', ('%s', 1))
            marriageTitle = marriageTitle % (husbandName,)
            return (marriageTitle, style)
        return ('', 1)

    def set_quantity(self, old):
        if self == BigWorld.player().targetLocked:
            gameglobal.rds.ui.target.showTargetUnitFrame()
            return

    def getQuality(self):
        resourceId = self.data['resourceId']
        return LSRD.data[resourceId].get('quality', 1)

    def getName(self):
        cId = LIID.data.get((self.gid, self.phase), 0)
        if not BigWorld.player().getAbilityData(gametypes.ABILITY_LS_COLLECTION_SUB_ON, cId):
            return '??Œ¥±Ê ∂'
        resourceId = self.data['resourceId']
        return LSRD.data[resourceId].get('name', None)

    def getColorName(self):
        color = FCD.data['item', self.getQuality()]['color']
        return "<font color=\'" + color + "\'>" + self.getName() + '</font>'

    def getSubType(self):
        return self.data.get('subType', 0)

    def getTargetItemId(self):
        return self.data.get('targetId')

    def getOptionalIcon(self):
        return LSCD.data.get(self._getItemId(), {}).get('optionalIcon', 'notFound')

    def leaveWorld(self):
        super(LifeCsmItem, self).leaveWorld()
        self.isLeaveWorld = True
        self.itemTrapCallback()
        if self.trapId != None:
            BigWorld.delPot(self.trapId)
            self.trapId = None

    def use(self):
        player = BigWorld.player()
        cId = LIID.data.get((self.gid, self.phase), 0)
        if player.isJumping:
            player.showGameMsg(GMDD.data.SKILL_FORBIDDEN_JUMPING, ())
            return
        if not BigWorld.player().getAbilityData(gametypes.ABILITY_LS_COLLECTION_SUB_ON, cId):
            player.showGameMsg(GMDD.data.LIFE_CSM_ITEM_UNIDENTIFIED, ())
            gameglobal.rds.ui.lifeSkillNew.hint(gametypes.ABILITY_LS_COLLECTION_SUB_ON, cId)
            return
        player.cell.clickLivingCsmItem(self.id, [])
        player.tLastMoving = utils.getNow()

    def getItemData(self):
        modelId = self.data.get('modelId', None)
        scale = self.data.get('scale', 1.0)
        if not modelId:
            modelId = DUMMY_MODEL_ID
        return {'model': modelId,
         'dye': 'Default',
         'modelShow': 1,
         'scale': scale}

    def getModelScale(self):
        scale = self.data.get('scale', 1.0)
        return (scale, scale, scale)

    def getPhaseName(self):
        data = LSCD.data[self._getItemId()]
        return data.get('phaseName', '')

    def set_phase(self, old):
        self.data = LSCD.data[self._getItemId()]
        if self.modelServer:
            self.modelServer.release()
            self.modelServer = None
        self.modelServer = modelServer.SimpleModelServer(self)

    def _getItemId(self):
        return LIID.data.get((self.gid, self.phase), 0)

    def onTargetCursor(self, enter):
        if enter:
            if ui.get_cursor_state() == ui.NORMAL_STATE:
                ui.set_cursor_state(ui.TARGET_STATE)
                subType = self.getSubType()
                if (self.position - BigWorld.player().position).length > cursor.TALK_DISTANCE:
                    if subType == 1:
                        ui.set_cursor(cursor.gather_stone_dis)
                    elif subType == 3:
                        ui.set_cursor(cursor.gather_plant_dis)
                    elif subType == 4:
                        ui.set_cursor(cursor.gather_wood_dis)
                    else:
                        ui.set_cursor(cursor.talk_dis)
                elif subType == 1:
                    ui.set_cursor(cursor.gather_stone)
                elif subType == 3:
                    ui.set_cursor(cursor.gather_plant)
                elif subType == 4:
                    ui.set_cursor(cursor.gather_wood)
                else:
                    ui.set_cursor(cursor.talk)
                ui.lock_cursor()
        elif ui.get_cursor_state() == ui.TARGET_STATE:
            ui.reset_cursor()

    def trapCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        self.itemTrapCallback()

    def itemTrapCallback(self):
        pickNearDist = SCD.data.get('pickUpLength', 4)
        ent = []
        for entity in BigWorld.entities.values():
            if not isinstance(entity, LifeCsmItem):
                continue
            if (entity.position - BigWorld.player().position).length <= pickNearDist and entity.isLeaveWorld == False:
                ent.append(entity)

        BigWorld.player().itemTrapCallBack(ent)

    def getFKey(self):
        return self.data.get('fKey', 0)
