#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPlayerComm.o
from gamestrings import gameStrings
import random
import time
import math
import zlib
import cPickle
import BigWorld
import Math
import const
import commcalc
import formula
import gameglobal
import gamelog
import gametypes
import utils
import skillDataInfo
import appSetting
import netWork
import commQuest
import appSetting
import clientcom
import clientUtils
import keys
from callbackHelper import Functor
from guis import hotkey as HK
from guis import messageBoxProxy
from guis import ui
from guis import uiConst, uiUtils
from helpers import action
from helpers import cellCmd
from helpers import navigator
from helpers import modelServer
from helpers import outlineHelper
from helpers import tintalt
from helpers import scenario
from helpers import loadingProgress
from helpers import ccManager
from item import Item
from helpers import editorHelper
from sfx import screenEffect
from sMath import inRange3D
from appSetting import Obj as AppSettings
from gamestrings import gameStrings
from helpers import blackEffectManager
from skillDataInfo import ClientSkillInfo
from data import monster_event_trigger_data as METD
from data import map_config_data as MCD
from data import zaiju_data as ZD
from data import game_msg_data as GMD
from data import qte_data as QTED
from data import carrousel_data as CD
from data import item_data as ID
from cdata import game_msg_def_data as GMDD
from data import equip_data as ED
from data import horsewing_camera_data as HCD
from data import sys_config_data as SCD
from data import couple_emote_basic_data as CEBD
from cdata import prop_def_data as PDD
from data import treasure_box_data as TBD
from data import quest_loop_data as QLD
from data import wing_world_config_data as WWCD
from data import marriage_config_data as MCDD
from data import marriage_package_data as MPD
from data import wing_world_carrier_data as WWWCD
from data import fb_data as FD
from data import multiline_digong_data as MDD
from data import npc_data as ND
PERFORMANCE_EYS = {'commitedmem': 'commitedMem',
 'phymem': 'phyMem',
 'availmem': 'availMem',
 'ioread': 'ioRead',
 'iowrite': 'ioWrite',
 'ioother': 'ioOther',
 'corenum': 'coreNum',
 'fps_5': 'fps5',
 'fps_10': 'fps10',
 'fps_15': 'fps15',
 'fps_20': 'fps20',
 'fps_25': 'fps25',
 'fps_30': 'fps30',
 'fps_40': 'fps40',
 'fps_50': 'fps50',
 'fps_60': 'fps60',
 'fps_200000': 'fps200000',
 'gputotalmem_0': 'gpuTotalMem0',
 'gputotalmem_1': 'gpuTotalMem1',
 'gputotalmem_2': 'gpuTotalMem2',
 'gpuload_0': 'gpuLoad0',
 'gpuload_1': 'gpuLoad1',
 'gpuload_2': 'gpuLoad2',
 'gpuusedmem_0': 'gpuUsedMem0',
 'gpuusedmem_1': 'gpuUsedMem1',
 'gpuusedmem_2': 'gpuUsedMem2',
 'gpusensor_0': 'gpuSensor0',
 'gpusensor_1': 'gpuSensor1',
 'gpusensor_2': 'gpuSensor2',
 'gpusensor_3': 'gpuSensor3',
 'processorType': 'processorType',
 'cpuFreq': 'cpuFreq',
 'totalcpu': 'totalCpu'}

class ImpPlayerComm(object):

    def removeRefreshDroppedItem(self, droppedItem):
        if droppedItem in self.refreshDroppedItemList:
            self.refreshDroppedItemList.remove(droppedItem)
            if not self.refreshDroppedItemList and self.refreshDroppedItemHandle:
                BigWorld.cancelCallback(self.refreshDroppedItemHandle)
                self.refreshDroppedItemHandle = None

    def addRefreshDroppedItem(self, droppedItem):
        if droppedItem not in self.refreshDroppedItemList:
            self.refreshDroppedItemList.append(droppedItem)
            if not self.refreshDroppedItemHandle:
                self.refreshDroppedItemHandle = BigWorld.callback(2, self.refreshDroppedItem)

    def refreshDroppedItem(self):
        if not self.inWorld:
            return
        else:
            refreshDroppedItemTuple = tuple(self.refreshDroppedItemList)
            for droppedItem in refreshDroppedItemTuple:
                if droppedItem._checkPickItem(self):
                    self.refreshDroppedItemList.remove(droppedItem)
                    if droppedItem.inWorld and droppedItem.topLogo != None:
                        droppedItem.topLogo.setDropItemIconVisible(True)

            if self.refreshDroppedItemHandle:
                BigWorld.cancelCallback(self.refreshDroppedItemHandle)
                self.refreshDroppedItemHandle = None
            if self.refreshDroppedItemList:
                self.refreshDroppedItemHandle = BigWorld.callback(2, self.refreshDroppedItem)
            return

    def recordQingGongTime(self, qingGongState):
        self.qingGongTimePair = (qingGongState, time.time(), self.ep)

    def enterInteractiveCallback(self, entity):
        if entity and (entity.__class__.__name__ == 'Avatar' or utils.instanceof(entity, 'Puppet')):
            if gameglobal.rds.ui.pressKeyF.mediator and gameglobal.rds.ui.pressKeyF.type == const.F_WING_WORLD_CARRIR:
                return
            if gameglobal.rds.ui.pressKeyF.isInteractiveAvatar == False:
                gameglobal.rds.ui.pressKeyF.isInteractiveAvatar = True
                gameglobal.rds.ui.pressKeyF.interactiveAvatars = set([entity])
                gameglobal.rds.ui.pressKeyF.setType(const.F_AVATAR)
            else:
                gameglobal.rds.ui.pressKeyF.interactiveAvatars.add(entity)

    def leaveInteractiveCallback(self, entity):
        if entity and (entity.__class__.__name__ == 'Avatar' or utils.instanceof(entity, 'Puppet')):
            interactiveAvatars = gameglobal.rds.ui.pressKeyF.interactiveAvatars
            if entity in interactiveAvatars:
                interactiveAvatars.remove(entity)
            avatars = []
            for a in interactiveAvatars:
                if a and a.inWorld:
                    avatars.append(a)

            gameglobal.rds.ui.pressKeyF.interactiveAvatars = set(avatars)
            if not gameglobal.rds.ui.pressKeyF.interactiveAvatars:
                gameglobal.rds.ui.pressKeyF.isInteractiveAvatar = False
                gameglobal.rds.ui.pressKeyF.removeType(const.F_AVATAR)

    def droppedItemTrapInCallback(self, entitiesInTrap):
        for droppedItem in entitiesInTrap:
            if droppedItem.__class__.__name__ == 'DroppedItem':
                if gameglobal.rds.ui.pressKeyF.isDroppedItem == False:
                    gameglobal.rds.ui.pressKeyF.isDroppedItem = True
                    gameglobal.rds.ui.pressKeyF.itemEnt = set([droppedItem])
                    gameglobal.rds.ui.pressKeyF.setType(const.F_DROPPEDITEM)
                else:
                    gameglobal.rds.ui.pressKeyF.itemEnt.add(droppedItem)

    def droppedItemTrapOutCallback(self, entitiesInTrap):
        for droppedItem in entitiesInTrap:
            itemEnt = gameglobal.rds.ui.pressKeyF.itemEnt
            if droppedItem in itemEnt:
                itemEnt.remove(droppedItem)

        if not itemEnt:
            gameglobal.rds.ui.pressKeyF.isDroppedItem = False
            gameglobal.rds.ui.pressKeyF.removeType(const.F_DROPPEDITEM)

    def droppedItemTrapCallBack(self, entitiesInTrap):
        p = BigWorld.player()
        if p.isInPUBG():
            p.pickNearItemsInPUBG()

    def addBoxTrapEx(self, box):
        if box.__class__.__name__ == 'QuestBox' and not box.beHide:
            if box.isQuestValid():
                gameglobal.rds.ui.pressKeyF.addEnt(box.id, const.F_QUESTBOX)
                return True
        if utils.instanceofTypes(box, ('TreasureBox', 'MultiPlayerTreasureBox', 'BattleFieldPUBGTreasureBox')) and not box.beHide:
            cancelEvent = TBD.data.get(box.treasureBoxId, {}).get('cancelEvent', 0)
            if cancelEvent and box.status == const.ST_OPENED:
                return False
            gameglobal.rds.ui.pressKeyF.addEnt(box.id, const.F_TREASUREBOX)
            return False
        return False

    def delBoxTrapEx(self, box):
        if box.__class__.__name__ == 'QuestBox':
            gameglobal.rds.ui.pressKeyF.delEnt(box.id, const.F_QUESTBOX)
        elif utils.instanceofTypes(box, ('TreasureBox', 'MultiPlayerTreasureBox', 'BattleFieldPUBGTreasureBox')):
            gameglobal.rds.ui.pressKeyF.delEnt(box.id, const.F_TREASUREBOX)

    def boxTrapCallback(self, entitiesInTrap):
        result = False
        for box in entitiesInTrap:
            result = result or self.addBoxTrapEx(box)

        if not result:
            gameglobal.rds.ui.pressKeyF.delEntByType(const.F_QUESTBOX)
            gameglobal.rds.ui.pressKeyF.delEntByType(const.F_TREASUREBOX)

    def transportTrapCallback(self, entitiesInTrap):
        for transport in entitiesInTrap:
            if transport.__class__.__name__ == 'Transport':
                if gameglobal.rds.ui.pressKeyF.isTransport == False:
                    gameglobal.rds.ui.pressKeyF.isTransport = True
                    gameglobal.rds.ui.pressKeyF.setType(const.F_TRANSPORT)
                return

        if gameglobal.rds.ui.pressKeyF.isTransport == True:
            gameglobal.rds.ui.pressKeyF.isTransport = False
            gameglobal.rds.ui.pressKeyF.removeType(const.F_TRANSPORT)

    def monsterTrapCallback(self, entitiesInTrap):
        for monster in entitiesInTrap:
            if monster.__class__.__name__ == 'Monster':
                gameglobal.rds.ui.pressKeyF.monster = monster
                if gameglobal.rds.ui.pressKeyF.isMonster == False:
                    gameglobal.rds.ui.pressKeyF.isMonster = True
                    gameglobal.rds.ui.pressKeyF.setType(const.F_MONSTER)
                return

        if gameglobal.rds.ui.pressKeyF.isMonster == True:
            gameglobal.rds.ui.pressKeyF.isMonster = False
            if gameglobal.rds.ui.pressKeyF.monster:
                spellId = getattr(self, 'spellTargetId', 0)
                if gameglobal.rds.ui.pressKeyF.monster.id == spellId:
                    monster = gameglobal.rds.ui.pressKeyF.monster
                    eventData = METD.data[monster.charType][monster.triggerEventIndex]
                    radii = eventData.get('radii')
                    if radii:
                        if not inRange3D(radii, self.position, gameglobal.rds.ui.pressKeyF.monster.position) or gameglobal.rds.ui.pressKeyF.monster.isLeaveWorld:
                            self.cell.cancelAction(const.CANCEL_ACT_ANY_WAY)
            gameglobal.rds.ui.pressKeyF.monster = None
            gameglobal.rds.ui.pressKeyF.removeType(const.F_MONSTER)

    def battleFieldFlagTrapCallback(self, entitiesInTrap):
        for battleFieldFlag in entitiesInTrap:
            if battleFieldFlag.__class__.__name__ == 'BattleFieldFlag':
                gameglobal.rds.ui.pressKeyF.battleFieldFlag = battleFieldFlag
                if gameglobal.rds.ui.pressKeyF.isBattleFieldFlag == False:
                    gameglobal.rds.ui.pressKeyF.isBattleFieldFlag = True
                    gameglobal.rds.ui.pressKeyF.setType(const.F_BATTLE_FIELD_FLAG)
                return

        if gameglobal.rds.ui.pressKeyF.isBattleFieldFlag == True:
            gameglobal.rds.ui.pressKeyF.isBattleFieldFlag = False
            gameglobal.rds.ui.pressKeyF.battleFieldFlag = None
            gameglobal.rds.ui.pressKeyF.removeType(const.F_BATTLE_FIELD_FLAG)

    def movingPlatformTrapCallback(self, entitiesInTrap):
        for movingPlatform in entitiesInTrap:
            if movingPlatform.__class__.__name__ in ('MovingPlatform', 'MultiplayMovingPlatform'):
                gameglobal.rds.ui.pressKeyF.movingPlatform = movingPlatform
                if gameglobal.rds.ui.pressKeyF.isMovingPlatform == False:
                    gameglobal.rds.ui.pressKeyF.isMovingPlatform = True
                    gameglobal.rds.ui.pressKeyF.setType(const.F_MOVING_PLATFORM)
                return

        if gameglobal.rds.ui.pressKeyF.isMovingPlatform == True:
            gameglobal.rds.ui.pressKeyF.isMovingPlatform = False
            gameglobal.rds.ui.pressKeyF.movingPlatform = None
            gameglobal.rds.ui.pressKeyF.removeType(const.F_MOVING_PLATFORM)

    def roundTableTrapCallback(self, entitiesInTrap):
        for roundTable in entitiesInTrap:
            if roundTable.__class__.__name__ == 'RoundTable':
                gameglobal.rds.ui.pressKeyF.roundTable = roundTable
                if gameglobal.rds.ui.pressKeyF.isRoundTable == False:
                    gameglobal.rds.ui.pressKeyF.isRoundTable = True
                    gameglobal.rds.ui.pressKeyF.setType(const.F_ROUND_TABLE)
                return

        if gameglobal.rds.ui.pressKeyF.isRoundTable == True:
            gameglobal.rds.ui.pressKeyF.isRoundTable = False
            gameglobal.rds.ui.pressKeyF.roundTable = None
            gameglobal.rds.ui.pressKeyF.removeType(const.F_ROUND_TABLE)

    def interactiveTrapCallback(self, entitiesInTrap):
        for interactiveObj in entitiesInTrap:
            if interactiveObj.__class__.__name__ == 'InteractiveObject':
                gameglobal.rds.ui.pressKeyF.interactiveObj = interactiveObj
                if gameglobal.rds.ui.pressKeyF.isInteractive == False:
                    gameglobal.rds.ui.pressKeyF.isInteractive = True
                    gameglobal.rds.ui.pressKeyF.setType(const.F_INTERACTIVE)
                return

        if gameglobal.rds.ui.pressKeyF.isInteractive == True:
            gameglobal.rds.ui.pressKeyF.isInteractive = False
            gameglobal.rds.ui.pressKeyF.interactiveObj = None
            gameglobal.rds.ui.pressKeyF.removeType(const.F_INTERACTIVE)

    def businessItemTrapCallback(self, entitiesInTrap):
        for businessItem in entitiesInTrap:
            if businessItem.__class__.__name__ == 'BusinessItem':
                if gameglobal.rds.ui.pressKeyF.isBusinessItem == False:
                    gameglobal.rds.ui.pressKeyF.isBusinessItem = True
                    gameglobal.rds.ui.pressKeyF.setType(const.F_BUSINESS_ITEM)
                return

        if gameglobal.rds.ui.pressKeyF.isBusinessItem == True:
            gameglobal.rds.ui.pressKeyF.isBusinessItem = False
            gameglobal.rds.ui.pressKeyF.removeType(const.F_BUSINESS_ITEM)

    def npcTrapInCallback(self, entitiesInTrap):
        for npc in entitiesInTrap:
            npcData = ND.data.get(npc.npcId, {})
            buffRequire = npcData.get('buffRequire', 0)
            p = BigWorld.player()
            if buffRequire and not p.statesServerAndOwn.has_key(buffRequire):
                return
            if npc.__class__.__name__ in ('Npc', 'Dawdler', 'ClientNpc', 'GuildDawdler', 'MovableNpc') and not npc.beHide:
                if gameglobal.rds.ui.pressKeyF.isNormalNpc == False:
                    gameglobal.rds.ui.pressKeyF.isNormalNpc = True
                    gameglobal.rds.ui.pressKeyF.npcEnt = set([npc])
                    gameglobal.rds.ui.pressKeyF.setType(const.F_NORMALNPC)
                else:
                    gameglobal.rds.ui.pressKeyF.npcEnt.add(npc)

    def npcTrapOutCallback(self, entitiesInTrap):
        for npc in entitiesInTrap:
            npcEnt = gameglobal.rds.ui.pressKeyF.npcEnt
            if npc in npcEnt:
                npcEnt.remove(npc)

        if not npcEnt:
            gameglobal.rds.ui.pressKeyF.isNormalNpc = False
            gameglobal.rds.ui.pressKeyF.removeType(const.F_NORMALNPC)

    def jiguanTrapInCallBack(self, entitiesInTrap):
        if len(entitiesInTrap) > 0:
            gameglobal.rds.ui.pressKeyF.isJiguan = True
            gameglobal.rds.ui.pressKeyF.setType(const.F_JIGUAN)
            return
        if gameglobal.rds.ui.pressKeyF.isJiguan == True:
            gameglobal.rds.ui.pressKeyF.isJiguan = False
            gameglobal.rds.ui.pressKeyF.removeType(const.F_JIGUAN)

    def zaijuTrapCallBack(self, entitiesInTrap):
        if len(entitiesInTrap) > 0:
            gameglobal.rds.ui.pressKeyF.isZaiju = True
            gameglobal.rds.ui.pressKeyF.zaiju = entitiesInTrap[0]
            gameglobal.rds.ui.pressKeyF.setType(const.F_ZAIJU)
            return
        else:
            if gameglobal.rds.ui.pressKeyF.isZaiju == True:
                gameglobal.rds.ui.pressKeyF.isZaiju = False
                gameglobal.rds.ui.pressKeyF.zaiju = None
                gameglobal.rds.ui.pressKeyF.removeType(const.F_ZAIJU)
            return

    def itemTrapCallBack(self, entitiesInTrap):
        if len(entitiesInTrap) > 0:
            gameglobal.rds.ui.pressKeyF.isLifeCsmItem = True
            gameglobal.rds.ui.pressKeyF.lifeCsmItem = entitiesInTrap[0]
            gameglobal.rds.ui.pressKeyF.setType(const.F_LifeCsmItem)
            return
        else:
            if gameglobal.rds.ui.pressKeyF.isLifeCsmItem == True:
                gameglobal.rds.ui.pressKeyF.isLifeCsmItem = False
                gameglobal.rds.ui.pressKeyF.lifeCsmItem = None
                gameglobal.rds.ui.pressKeyF.removeType(const.F_LifeCsmItem)
            return

    def _enterFubenBefore(self):
        gameglobal.rds.ui.fubenLogin.dismiss()
        gameglobal.rds.ui.unLoadAllWidget([uiConst.WIDGET_COMM_TEAM_PLAYER,
         uiConst.WIDGET_TD_COUNTDOWN,
         uiConst.WIDGET_FUBEN_CLOCK,
         uiConst.WIDGET_DEAD_RELIVE,
         uiConst.WIDGET_ACTION_BARS,
         uiConst.WIDGET_WUSHUANG_BARS,
         uiConst.WIDGET_ITEMBAR,
         uiConst.WIDGET_ZAIJU,
         uiConst.WIDGET_ZAIJU_V2,
         uiConst.WIDGET_ARENA_COUNT_DOWN,
         uiConst.WIDGET_BULLET,
         uiConst.WIDGET_EQUIP_REPAIR,
         uiConst.WIDGET_TOPBAR,
         uiConst.WIDGET_EXIT_ZAIJU,
         uiConst.WIDGET_ZAIJU_V2,
         uiConst.WIDGET_AIR_BATTLE_BAR,
         uiConst.WIDGET_ITEMBAR2,
         uiConst.WIDGET_BUFF_LISTENER_SHOW])
        gameglobal.rds.ui.initHud()

    def motionPin(self):
        gamelog.debug('jorsef: motionPin')
        if not self.inWorld:
            return
        else:
            self.isPin = True
            self.resetHorizontalMove()
            if self.fashion != None and self.touchAirWallProcess != 1:
                self.fashion.breakJump()
                self.fashion.breakFall()
            self.isAscending = False
            if self.ap != None:
                self.ap.stopMove()
            return

    def needForbidHorizontalMove(self):
        if self.isPin:
            if self.inDanDao:
                return False
            else:
                return True
        return False

    def resetHorizontalMove(self):
        if self.needForbidHorizontalMove():
            self.physics.forbidHorizontalMove = True
        else:
            self.physics.forbidHorizontalMove = False

    def motionUnpin(self):
        gamelog.debug('jorsef: motionUnpin')
        if not self.inWorld:
            return
        if self.fashion:
            self.fashion.breakJump()
            self.fashion.breakFall()
        self.isPin = False
        self.isAscending = False
        self.resetHorizontalMove()
        self.updateActionKeyState()
        actType = self.fashion.doingActionType()
        if actType in [action.HANG_WEAPON_ACTION]:
            self.fashion.movingNotifier(True)

    def resetCamera(self):
        if self._isOnZaijuOrBianyao():
            beastKey = self._getZaijuOrBianyaoNo()
            scrollRange = ZD.data.get(beastKey, {}).get('scrollRange', None)
            if scrollRange:
                gameglobal.rds.cam.setScrollRange(scrollRange[0:2], scrollRange[-1])
        if self.inCarrousel():
            carrousel = BigWorld.entities.get(self.carrousel[0], None)
            if carrousel:
                data = CD.data.get(carrousel.carrouselId, {})
                scrollRange = data.get('scrollRange', None)
                if scrollRange:
                    gameglobal.rds.cam.setScrollRange(scrollRange[0:2], scrollRange[-1])
        elif self.modelServer.state == modelServer.STATE_HUMAN:
            gameglobal.rds.cam.setScrollRange()
        self.resetCameraOffset()
        BigWorld.callback(0.1, gameglobal.rds.cam.reset)

    def refreshCameraFarPlane(self):
        if self.isInPUBG():
            BigWorld.projection().farPlane = const.PUBG_CAMERA_FARPLANE
        else:
            BigWorld.projection().farPlane = const.NORMAL_CAMERA_FARPLANE

    def getRideCameraOffset(self, rideId):
        horsewingCameraId = ED.data.get(rideId, {}).get('horsewingCameraId', None)
        horsewingCameraData = HCD.data.get(horsewingCameraId, {})
        return horsewingCameraData.get('cameraOffset', None)

    def resetCameraOffset(self):
        if gameglobal.rds.GameState == gametypes.GS_PLAYGAME:
            p = BigWorld.player()
            cameraOffset = None
            if hasattr(p, 'bianshen') and p.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
                cameraOffset = self.getRideCameraOffset(p.bianshen[1])
            elif hasattr(p, 'isRidingTogetherAsVice') and p.isRidingTogetherAsVice():
                if hasattr(p, 'tride'):
                    header = p.tride.getHeader()
                    if header and header.inWorld:
                        cameraOffset = self.getRideCameraOffset(header.bianshen[1])
            if cameraOffset:
                gameglobal.rds.cam.setCameraOffset(cameraOffset)
            else:
                gameglobal.rds.cam.setCameraOffset((0, 0, 0))

    def clearShapeEffect(self):
        for fx in self.circleShapes:
            if self.model and fx in self.model.root.attachments:
                self.model.root.detach(fx)
                fx.clear()
                fx.scale(1)
            fx.stop()
            fx = None

        self.circleShapes = []

    def playHoverEffect(self, skillId, level = None):
        if not gameglobal.ENABLE_SKILL_HOVER_EFFECT:
            return
        else:
            skillId = int(skillId) if skillId else 0
            if level == None:
                sVal = self.getSkills().get(skillId, None)
                if not sVal:
                    return
                level = sVal.level
            clientSkillInfo = ClientSkillInfo(skillId, level, 0)
            effects = skillDataInfo.getSkillEffects(clientSkillInfo, gameglobal.S_HOVER)
            self.stopHoverEffect()
            if effects:
                if self.circleShapeCallback:
                    BigWorld.cancelCallback(self.circleShapeCallback)
                self.circleShapeCallback = BigWorld.callback(1, Functor(self._showHoverEffect, effects))
            return

    def _showHoverEffect(self, effects):
        self.stopHoverEffect()
        idx = effects[0]
        xScale = effects[1]
        zScale = effects[2]
        shapeFx = self.circleShapes[idx - 1]
        shapeFx.clear()
        shapeFx.scale(xScale, xScale, zScale)
        model = self.model if self._isOnZaijuOrBianyao else self.modelServer.bodyModel
        if not model:
            return
        if not model.root:
            return
        if shapeFx and not shapeFx.attached and shapeFx not in model.root.attachments:
            model.root.attach(shapeFx)
            shapeFx.force()

    def stopHoverEffect(self):
        if self.circleShapeCallback:
            BigWorld.cancelCallback(self.circleShapeCallback)
        model = self.model if self._isOnZaijuOrBianyao else self.modelServer.bodyModel
        for fx in self.circleShapes:
            try:
                model.root.detach(fx)
                fx.clear()
                fx.scale(1)
            except:
                pass

    def followTarget(self):
        if not self.stateMachine.checkStatus(const.CT_FOLLOW_TARGET):
            return
        target = self.targetLocked
        if target and target.inWorld and hasattr(target, 'roleName'):
            self.ap.traceEntity(target, 1.0)

    def followOtherAvatar(self, ent):
        if not self.stateMachine.checkStatus(const.CT_FOLLOW_TARGET):
            return
        if self.qinggongMgr.isJumping():
            return
        if ent and ent.inWorld and hasattr(ent, 'roleName'):
            self.ap.traceEntity(ent, 1.0)

    def followOtherAvatarWithDist(self, ent, dist):
        if not self.stateMachine.checkStatus(const.CT_FOLLOW_TARGET):
            return
        if self.qinggongMgr.isJumping():
            return
        if ent and ent.inWorld and hasattr(ent, 'roleName'):
            self.ap.traceEntity(ent, dist)

    def getOperationMode(self):
        if hasattr(self, '_keyboardPhysics') and self.ap == self._keyboardPhysics:
            return gameglobal.KEYBOARD_MODE
        if hasattr(self, '_actionPhysics') and self.ap == self._actionPhysics:
            return gameglobal.ACTION_MODE
        return gameglobal.MOUSE_MODE

    def startKeyModeFlow(self, target):
        if not target:
            return
        if not self.isCombatUnit(target):
            self.mouseModeFlow(target)
        elif not self.canBeAttack(target):
            self.startKeyModeCombatUnitInteractFlow(target)
        else:
            self.startKeyModeFightFlow(target)

    def startMouseModeFlow(self, target):
        if not self.isCombatUnit(target):
            self.mouseModeFlow(target)
        elif not self.canBeAttack(target):
            self.startKeyModeCombatUnitInteractFlow(target)
        else:
            self.startMouseModeFightFlow(target)

    def startKeyModeCombatUnitInteractFlow(self, target):
        needDist = self.getUseRange(target)
        dist = self.position.distTo(target.position)
        if target.IsAvatar:
            target.use()
            return
        if getattr(target, 'IsMonster', False) or getattr(target, 'IsSummonedBeast', False):
            return
        if needDist < dist:
            self.actionAfterLock(target)
            return
        if self.getOperationMode() == gameglobal.MOUSE_MODE:
            self.faceTo(target, True)
        if hasattr(target, 'canBeUse'):
            target.canBeUse()
        elif hasattr(target, 'use'):
            target.use()

    def startKeyModeFightFlow(self, target):
        dist = self.position.distTo(target.position)
        self.autoSkill.switchToMouseMode()
        if self.autoSkill.getDistWithBodySize() < dist:
            self.chaseEntity(target, self.autoSkill.getDistWithBodySize() - 1)
        else:
            self.autoSkill.start()

    def startMouseModeFightFlow(self, target):
        if not target or not target.inWorld:
            return
        dist = self.position.distTo(target.position)
        self.autoSkill.switchToMouseMode()
        if self.autoSkill.getDistWithBodySize() < dist:
            self.chaseEntity(target, self.autoSkill.getDistWithBodySize() - 1)
        else:
            self.autoSkill.start()

    def mouseModeFlow(self, target):
        if not target or not target.inWorld:
            return
        dmdDist = self.getUseRange(target)
        dist = self.position.distTo(target.position)
        if dmdDist < dist:
            self.actionAfterLock(target)
        else:
            if self.getOperationMode() == gameglobal.MOUSE_MODE:
                self.faceTo(target, True)
            if hasattr(target, 'canBeUse'):
                target.canBeUse()
            elif hasattr(target, 'use'):
                target.use()

    def updateActionKeyState(self):
        if self.ap and not self.ap.isChasing and not self.inForceMove and not self.ap.checkLockMoveActionWing() and not self.doManDownUpAction() and not gameglobal.rds.ui.inQTE:
            self.ap.updateMoveControl()

    def _confirmStopScenarioPlay(self, scenarioIns):
        if scenarioIns.confirmStopMsgBoxId:
            self.showGameMsg(GMDD.data.QUIT_SCENARIO_PLAY, ())
            scenarioIns.stopPlay()

    def _cancelStopScenarioPlay(self, scenarioIns):
        if scenarioIns.confirmStopMsgBoxId:
            scenarioIns.confirmStopMsgBoxId = None

    def updateTargetFocus(self, entity):
        if entity == self.target and hasattr(entity, 'canOutline') and entity.canOutline():
            if not (self.getOperationMode() == gameglobal.ACTION_MODE and not self.ap.showCursor):
                outlineHelper.setTarget(self.target)

    def isInChoose(self):
        if hasattr(self, 'chooseEffect') and self.chooseEffect.isShowingEffect:
            if not gameglobal.isWidgetNeedShowCursor:
                return True
        return False

    def getUseRange(self, target):
        targetBodySize = getattr(target, 'bodySize', 1.0)
        if self.isEnemy(target):
            return self.atkRange + targetBodySize
        seekDist = 0
        if hasattr(target, 'getSeekDist'):
            seekDist = target.getSeekDist()
        if seekDist:
            return seekDist
        else:
            return 2.0 + targetBodySize

    def getChaseDist(self, target):
        if self.getOperationMode() == gameglobal.MOUSE_MODE:
            if self.isEnemy(target):
                return self.atkRange
        seekDist = 0
        if hasattr(target, 'getSeekDist'):
            seekDist = target.getSeekDist()
        if seekDist:
            return seekDist
        else:
            return 2.0

    def chaseEntity(self, entity, desiredDist, commander = None, callback = None):
        gamelog.debug('jorsef: chaseEntity', entity, desiredDist, commander)
        self.chaseEntityCallback = callback
        if commander != None:
            self.chaseCommander = commander
        else:
            self.chaseCommander = entity
        dist = self.position.distTo(entity.position)
        height = (entity.model and (entity.model.height,) or (0,))[0]
        dist1 = self.position.distTo(entity.position + Math.Vector3(0, height, 0))
        if dist <= desiredDist or dist1 <= desiredDist:
            self.reachDesiredDist()
        else:
            self.ap.beginChase(entity, desiredDist)

    def reachDesiredDist(self):
        if self.chaseEntityCallback:
            self.chaseEntityCallback()
            self.chaseEntityCallback = None
        cmder = None
        if hasattr(self, 'chaseCommander'):
            cmder = self.chaseCommander
        if cmder:
            self.chaseCommander = None
            if hasattr(cmder, 'inWorld') and not cmder.inWorld:
                return
            if hasattr(cmder, 'canBeUse'):
                cmder.canBeUse()
            elif hasattr(cmder, 'position'):
                if utils.instanceof(cmder, 'DroppedItem'):
                    dmdDist = SCD.data.get('pickUpLength', 4)
                else:
                    dmdDist = self.getUseRange(cmder) + 1
                dist = self.position.distTo(cmder.position)
                if dist <= dmdDist:
                    cmder.use()
            else:
                cmder.use()
            gamelog.debug('bgf:reachDesiredDist', cmder, self.autoUseSkill)
            if self.autoUseSkill:
                skillInfo = self.getSkillInfo(self.skillId, self.skillLevel)
                if not self.checkSkill(skillInfo, target=cmder):
                    return
                if self.autoUseSkill:
                    isSpellCharge = skillDataInfo.isChargeSkill(skillInfo)
                    gamelog.debug('bgf:reachDesiredDist1', isSpellCharge, self.isChargeKeyDown)
                    if isSpellCharge:
                        if self.isChargeKeyDown:
                            cellCmd.castChargeSkill()
                        else:
                            self.useskill()
                    elif cmder.IsCombatUnit:
                        self.useskill(cmder)
                    self.autoUseSkill = False
            elif self.canBeAttack(cmder):
                self.autoSkill.start()

    def faceTo(self, target, immediately = False, forbidCamRotate = False):
        if target == None or target == self:
            return
        else:
            dir = target.position - self.position
            self.faceToDir(dir.yaw, immediately, forbidCamRotate)
            return

    def faceToDir(self, yaw, immediately = False, forbidCamRotate = False):
        self.ap.setYaw(yaw, forbidCamRotate)
        if immediately:
            if self.vehicle:
                self.filter.yaw = yaw - self.vehicle.yaw
            else:
                self.filter.yaw = yaw
            self.updatePoseImmediately()

    def faceToDirWidthCamera(self, yaw, immediately = False):
        self.faceToDir(yaw, immediately)
        cc = gameglobal.rds.cam.cc
        deltaYaw = yaw - cc.direction.yaw
        if deltaYaw > math.pi:
            deltaYaw -= math.pi * 2
        if deltaYaw < -math.pi:
            deltaYaw += math.pi * 2
        cc.deltaYaw += deltaYaw

    def toggleFashionBag(self, down):
        if down:
            if gameglobal.rds.ui.fashionBag.mediator:
                gameglobal.rds.ui.fashionBag.hide()
            else:
                gameglobal.rds.ui.fashionBag.askForShow()

    def toggleRideWing(self, down):
        if down:
            gameglobal.rds.ui.wingAndMount.toggle()

    def reliveHere(self):
        self.cell.confirmRelive(gametypes.RELIVE_TYPE_XIN_CHUN_GE, True)

    def reliveByLinHunShi(self):
        self.cell.confirmRelive(gametypes.RELIVE_TYPE_BY_LINHUNSHI, True)

    def reliveByFrame(self):
        self.cell.confirmRelive(gametypes.RELIVE_TYPE_WING_PEACE_BY_FRAME, True)

    def reliveHereRes(self, resultCode):
        if resultCode == const.RELIVE_HERE_OK:
            self.touchAirWallProcess = 0
            self.reliveResult(True)
        elif resultCode == const.RELIVE_HERE_FAIL_NO_ITEM:
            self.showGameMsg(GMDD.data.CANNOT_USE_RELIVE_ITEM, ())

    def reliveClanWarYaBiao(self):
        self.cell.confirmRelive(gametypes.RELIVE_TYPE_BY_CLAN_COURIER_JCT, True)

    def reliveOrigin(self):
        self.cell.confirmRelive(gametypes.RELIVE_TYPE_LIVE_AT_POINT, True)
        gameglobal.rds.ui.deadAndRelive.hide()
        if gameglobal.rds.ui.fbDeadData.mediator:
            gameglobal.rds.ui.fbDeadData.hide()
        if gameglobal.rds.ui.fbDeadDetailData.mediator:
            gameglobal.rds.ui.fbDeadDetailData.hide()
        if not self.inWorldWarBattle():
            BigWorld.callback(2, self.checkReliveOriginResult)
        self.touchAirWallProcess = 0
        if ui.entityClicked and ui.entityClicked.__class__.__name__.find('Npc') != -1:
            gameglobal.rds.ui.clearNPCDlg(ui.entityClicked)

    def checkReliveOriginResult(self):
        if self.life == gametypes.LIFE_DEAD:
            reliveHereEnable = not (self.touchAirWallProcess > 0 or self.downCliff > 0)
            spaceNo = formula.getMapId(self.spaceNo)
            reliveHereType = MCD.data.get(spaceNo, {}).get('reliveHereType', gametypes.RELIVE_HERE_TYPE_FORBID)
            if uiUtils.isInFubenShishenLow():
                reliveHereType = gametypes.RELIVE_HERE_TYPE_NORMAL
            reliveHereEnable = reliveHereEnable and reliveHereType != gametypes.RELIVE_HERE_TYPE_FORBID
            reliveNearEnable = not MCD.data.get(spaceNo, {}).get('forbidReliveNear', 0) and self.canReliveNear
            gameglobal.rds.ui.deadAndRelive.show(reliveHereEnable, reliveNearEnable, False, None, reliveHereType)
            if self.inFubenTypes(const.FB_TYPE_GROUP_SET) and not self.canReliveNear:
                gameglobal.rds.ui.deadAndRelive.tip = gameStrings.TEXT_AVATAR_1730
            else:
                gameglobal.rds.ui.deadAndRelive.tip = ''

    def reliveResult(self, alive = False):
        if self.life == gametypes.LIFE_ALIVE:
            alive = True
        if alive:
            gameglobal.rds.ui.deadAndRelive.hide()
            if gameglobal.rds.ui.fbDeadData.mediator:
                gameglobal.rds.ui.fbDeadData.hide()
            if gameglobal.rds.ui.fbDeadDetailData.mediator:
                gameglobal.rds.ui.fbDeadDetailData.hide()
        else:
            BigWorld.callback(0.5, Functor(self.reliveResult, False))

    def showReliveMessageBox(self):
        MBButton = messageBoxProxy.MBButton
        reliveHereEnable = not (self.touchAirWallProcess > 0 or self.downCliff > 0)
        buttonHere = MBButton(gameStrings.TEXT_IMPPLAYERCOMM_885, Functor(self.reliveHere), reliveHereEnable, False)
        if formula.spaceInFbOrDuel(self.spaceNo):
            buttons = [buttonHere, MBButton(gameStrings.TEXT_IMPPLAYERCOMM_887, Functor(self.reliveOrigin), True, False)]
        else:
            buttons = [buttonHere, MBButton(gameStrings.TEXT_IMPPLAYERCOMM_889, Functor(self.reliveOrigin), True, False)]
        gameglobal.rds.ui.messageBox.show(False, '', '', buttons, True)

    def keyInSkill(self, key, mods):
        tempKey = HK.keyDef(key, 1, mods)
        args = map(lambda k: HK.HKM[k], HK.SHORCUT_SKILL_KEYS)
        if tempKey in args:
            return True
        args = map(lambda k: HK.HKM[k], HK.SHORTCUT_ITEM_KEYS)
        return tempKey in args

    def keyInBindings(self, key, mods):
        tempKey = HK.keyDef(key, 1, mods)
        args = [ item[0][0] for item in self.keyBindings ]
        return tempKey in args

    def onSlowTimeActionProcessed(self, action):
        if not self.inSlowTime or not self.slowTimeNeedActions:
            return
        for idx, needAction in enumerate(self.slowTimeNeedActionsTemp):
            if needAction[0] == action:
                needAction.remove(action)
            else:
                needAction = self.slowTimeNeedActions[idx]
            if not needAction:
                self.inSlowTime = False
                self.slowTimeNeedActions = []
                self.slowTimeNeedActionsTemp = []
                try:
                    BigWorld.setSlowTime(1)
                except:
                    pass

                if self.stageFinishCallback:
                    self.stageFinishCallback()
                break

    def cameraCloseTo(self, down):
        if self.isInBfDotaChooseHero:
            return
        if down and not HK.checkMouseRollUp():
            gameglobal.rds.cam.closeTo(1)

    def cameraAwayFrom(self, down):
        if self.isInBfDotaChooseHero:
            return
        if down and not HK.checkMouseRollDown():
            gameglobal.rds.cam.awayFrom(-1)

    def _checkDisableAllSlot(self, oldFlags, newFlags):
        if not commcalc.getBitDword(oldFlags, gametypes.FLAG_NO_SKILL) and commcalc.getBitDword(newFlags, gametypes.FLAG_NO_SKILL):
            return True
        return False

    def _checkRecoverAllSlot(self, oldFlags, newFlags):
        if commcalc.getBitDword(newFlags, gametypes.FLAG_NO_SKILL):
            return False
        if commcalc.getBitDword(oldFlags, gametypes.FLAG_NO_SKILL):
            return True
        return False

    def isQingGongSkillLearned(self, skillId):
        if not self.checkExcitementFeature(gametypes.EXCITEMENT_FEATURE_QINGGONG):
            return False
        if skillId in (gametypes.QINGGONG_FLAG_AUTO_PATHFINDING,) and gameglobal.rds.configData.get('enableQingGongPathFinding', False):
            return True
        if gametypes.LEARN_ALL_GQINGGONG and skillId not in (gametypes.QINGGONG_FLAG_AUTO_PATHFINDING, gametypes.QINGGONG_FLAG_DISMISS_MAN_DOWN):
            return True
        return self.qingGongSkills.get(skillId)

    def hideMonsterNearby(self, beHide):
        ent = BigWorld.entities.items()
        gameglobal.gHideMonsterFlag = beHide
        for id, e in ent:
            if hasattr(e, 'monsterInstance') and e.monsterInstance:
                if beHide == gameglobal.HIDE_ALL_MONSTER:
                    e.hide(True)
                elif beHide == gameglobal.HIDE_NOT_SPECIAL_MONSTER:
                    visibleGbId = getattr(e, 'visibleGbId', 0)
                    if visibleGbId and visibleGbId != self.gbId:
                        e.hide(True)
                    else:
                        e.hide(False)
                else:
                    e.refreshOpacityState()
                    e.enterTopLogoRange()

    def restoreMonsterNearby(self):
        flag = gameglobal.gHideMode >> 4 & 15
        self.hideMonsterNearby(flag)

    def hideMonsterTopLogo(self, down):
        if down:
            gameglobal.gHideMonsterTopLogo = not gameglobal.gHideMonsterTopLogo
            ent = BigWorld.entities.items()
            for id, e in ent:
                if e.IsMonster:
                    e.topLogo.hideName(gameglobal.gHideMonsterTopLogo)

    def hideTopLogo(self, isHide):
        gameglobal.gHideTopLogo = isHide
        ent = BigWorld.entities.values()
        for e in ent:
            if getattr(e, 'topLogo', None) and hasattr(e, 'beHide') and not e.beHide:
                if e == self:
                    e.topLogo.hide(isHide)
                elif e.__class__.__name__ in ('Avatar', 'SummonedSprite'):
                    if isHide:
                        e.topLogo.hide(isHide)
                    else:
                        e.refreshOpacityState()
                elif e.__class__.__name__ in ('Dawdler',) or e.IsMonster:
                    if not (e.IsMonster and not isHide and getattr(e, 'life', 0) == gametypes.LIFE_DEAD):
                        e.topLogo.hide(isHide)
                elif e.__class__.__name__ in ('Npc', 'MovableNpc') and getattr(e, 'isScenario', None) == gameglobal.NORMAL_NPC:
                    e.topLogo.hide(isHide)

    def hidePlayerNearby(self, beHide):
        gamelog.debug('hidePlayerNearby', beHide)
        if self.isolateType != gametypes.ISOLATE_TYPE_NONE and beHide != gameglobal.HIDE_ALL_PLAYER:
            return
        gameglobal.gHideOtherPlayerFlag = beHide
        self._realHidePlayerNearby()

    def hidePlayerNearbyCustom(self):
        gamelog.debug('@zrz:', 'hidePlayerNearbyCustom')
        gameglobal.gHideOtherPlayerFlag = gameglobal.HIDE_DEFINE_SELF
        self._realHidePlayerNearby()

    def _realHidePlayerNearby(self):
        ent = BigWorld.entities.items()
        beasts = {}
        for id, e in ent:
            if e.__class__.__name__ == 'Avatar':
                if self.isInBfDota() and e.hidingPower:
                    pass
                else:
                    e.refreshOpacityState()
                if e.topLogo == None:
                    e.enterTopLogoRange()
            elif e.__class__.__name__ == 'MultiplayMovingPlatform':
                e.refreshOpacityState()
            if e.IsSummoned and e.ownerId != self.id and not e.IsSummonedSprite:
                beasts[e.ownerId] = beasts.get(e.ownerId, []) + [e]
            if e.IsSummonedSprite:
                e.refreshOpacityState()

        for avatarId in beasts.iterkeys():
            avatar = BigWorld.entities.get(avatarId)
            if avatar:
                for sb in beasts[avatarId]:
                    sb.hide(avatar.beHide)

    def restorePlayerNearby(self):
        flag = gameglobal.gHideMode & 15
        self.hidePlayerNearby(flag)

    def hideNpcNearby(self, beHide):
        ent = BigWorld.entities.values()
        gameglobal.gHideNpcFlag = beHide
        for e in ent:
            className = e.__class__.__name__
            if className.find('Npc') != -1 or className == 'Dawdler' or className == 'HomeFurniture':
                if beHide:
                    e.hide(True)
                else:
                    e.refreshOpacityState()

    def hideAllNearby(self, exclude = ()):
        ent = BigWorld.entities.items()
        for id, e in ent:
            className = e.__class__.__name__
            if (className == 'Avatar' or hasattr(e, 'monsterInstance') and e.monsterInstance or className.find('Npc') != -1 or className == 'Dawdler' or className == 'HomeFurniture') and id not in exclude:
                e.hide(True)

        self.hide(True)
        gameglobal.gHideMonsterFlag = gameglobal.HIDE_ALL_MONSTER
        gameglobal.gHideOtherPlayerFlag = gameglobal.HIDE_ALL_PLAYER
        gameglobal.gHideNpcFlag = True

    def restoreAllNearby(self):
        self.refreshOpacityState()
        self.restoreMonsterNearby()
        self.restorePlayerNearby()
        self.hideNpcNearby(False)

    def hidePlayerAndMonster(self, down):
        if not down:
            return
        hideSettings = gameglobal.rds.ui.hideModeSetting.getHideModeSetting()
        isHide = gameglobal.HIDE_MODE_CUSTOM < len(hideSettings)
        if not isHide:
            self.showGameMsg(GMDD.data.HIDE_NOBODY, ())
            gameglobal.HIDE_MODE_CUSTOM = 0
            self.switchHideModeCustom(isHide)
        else:
            hideSetting = hideSettings[gameglobal.HIDE_MODE_CUSTOM]
            gameglobal.HIDE_MODE_CUSTOM += 1
            hideModeDesc = '/'.join([ gameglobal.HIDE_CUSTOM_DESC[i] for i, x in enumerate(hideSetting) if x and gameglobal.HIDE_CUSTOM_DESC[i] ])
            if hideModeDesc:
                hideModeDesc = gameStrings.TEXT_IMPPLAYERCOMM_1122 % (gameglobal.HIDE_MODE_CUSTOM, hideModeDesc)
            else:
                hideModeDesc = gameglobal.HIDE_MODE_CUSTOM
            self.showGameMsg(GMDD.data.HIDE_MODE, (hideModeDesc,))
            self.switchHideModeCustom(isHide, hideSetting[0], hideSetting[1], hideSetting[2], hideSetting[3], hideSetting[4], hideSetting[5], hideSetting[6])

    def switchHideModeCustom(self, isHide, showTopLogo = False, showGrouper = False, showEnemy = False, showBooth = False, showTeamer = False, showFriendSprite = False, showEnemySprite = False):
        if not isHide:
            gameglobal.gHideMode = gameglobal.HIDE_MODE0
            self.hidePlayerNearby(gameglobal.HIDE_NOBODY)
            self.restoreGuildIconNearby()
        else:
            gameglobal.gHideMode = gameglobal.HIDE_MODE7
            gameglobal.HIDE_MODE_CUSTOM_SHOW_TOPLOGO = showTopLogo
            gameglobal.HIDE_MODE_CUSTOM_SHOW_GROUPER = showGrouper
            gameglobal.HIDE_MODE_CUSTOM_SHOW_ENEMY = showEnemy
            gameglobal.HIDE_MODE_CUSTOM_SHOW_BOOTH = showBooth
            gameglobal.HIDE_MODE_CUSTOM_SHOW_TEAMER = showTeamer
            gameglobal.HIDE_MODE_CUSTOM_SHOW_FRIEND_SPRITE = showFriendSprite
            gameglobal.HIDE_MODE_CUSTOM_SHOW_ENEMY_SPRITE = showEnemySprite
            self.hidePlayerNearbyCustom()

    def restoreGuildIconNearby(self):
        ents = BigWorld.entities.values()
        count = 0
        if not gameglobal.gHideAvatarGuild:
            for e in ents:
                if e.__class__.__name__ == 'Avatar':
                    if e.topLogo and e.guildNUID:
                        count += 1
                        e.topLogo.addGuildIcon(e.guildFlag)
                        if count > gameglobal.GUILDICON_MAX_COUNT:
                            break

    def refreshCurrMode(self):
        if gameglobal.HIDE_MODE_CUSTOM == 0:
            return
        hideSettings = gameglobal.rds.ui.hideModeSetting.getHideModeSetting()
        hideSetting = hideSettings[gameglobal.HIDE_MODE_CUSTOM - 1]
        self.switchHideModeCustom(True, hideSetting[0], hideSetting[1], hideSetting[2], hideSetting[3], hideSetting[4], hideSetting[5], hideSetting[6])

    def switchHideMode(self, hideMode):
        if hideMode != gameglobal.HIDE_MODE_RESTORE:
            gameglobal.gOldHideMode = gameglobal.gHideMode
        if hideMode == gameglobal.HIDE_MODE0:
            self.showGameMsg(GMDD.data.HIDE_NOBODY, ())
            gameglobal.gHideMode = gameglobal.HIDE_MODE0
            self.hidePlayerNearby(gameglobal.HIDE_NOBODY)
        elif hideMode == gameglobal.HIDE_MODE1:
            self.showGameMsg(GMDD.data.HIDE_NOT_GROUPER_WITHOUT_ENEMY, ())
            gameglobal.gHideMode = gameglobal.HIDE_MODE1
            self.hidePlayerNearby(gameglobal.HIDE_NOT_GROUPER_WITHOUT_ENEMY)
        elif hideMode == gameglobal.HIDE_MODE2:
            self.showGameMsg(GMDD.data.HIDE_NOT_TEAMER_WITHOUT_ENEMY, ())
            gameglobal.gHideMode = gameglobal.HIDE_MODE2
            self.hidePlayerNearby(gameglobal.HIDE_NOT_TEAMER_WITHOUT_ENEMY)
        elif hideMode == gameglobal.HIDE_MODE3:
            self.showGameMsg(GMDD.data.HIDE_ALL_WITHOUT_ENEMY, ())
            gameglobal.gHideMode = gameglobal.HIDE_MODE3
            self.hidePlayerNearby(gameglobal.HIDE_ALL_WITHOUT_ENEMY)
        elif hideMode == gameglobal.HIDE_MODE4:
            self.showGameMsg(GMDD.data.HIDE_ALL_WITHOUT_TOPLOGO, ())
            gameglobal.gHideMode = gameglobal.HIDE_MODE4
            self.hidePlayerNearby(gameglobal.HIDE_ALL_WITHOUT_TOPLOGO)
        elif hideMode == gameglobal.HIDE_MODE5:
            self.showGameMsg(GMDD.data.HIDE_ALL_PLAYER, ())
            gameglobal.gHideMode = gameglobal.HIDE_MODE5
            self.hidePlayerNearby(gameglobal.HIDE_ALL_PLAYER)
        elif hideMode == gameglobal.HIDE_MODE6:
            gameglobal.gHideMode = gameglobal.HIDE_MODE6
            self.hidePlayerNearby(gameglobal.HIDE_ALL_PLAYER_AND_ATTACK)
        elif hideMode == gameglobal.HIDE_MODE_RESTORE:
            gameglobal.gHideMode = gameglobal.gOldHideMode
            self.restorePlayerNearby()
        gameglobal.rds.ui.topBar.updateMode('avatarMode')
        self.cell.updateHideFlags(gameglobal.gHideOtherPlayerFlag)

    def hidePlayerBlood(self, beHide, forceDo = False):
        if (self.inCombat or forceDo) and self.topLogo:
            self.topLogo.showBlood(not beHide)
        gameglobal.gHidePlayerBlood = beHide

    def hideAvatarBlood(self, beHide, forceDo = False):
        ent = BigWorld.entities.items()
        for id, e in ent:
            if e.__class__.__name__ == 'Avatar':
                if (e.inCombat or forceDo) and e.topLogo:
                    e.topLogo.showBlood(not beHide)

        gameglobal.gHideAvatarBlood = beHide

    def hideMonsterBlood(self, beHide, forceDo = False):
        ent = BigWorld.entities.items()
        for id, e in ent:
            if e.__class__.__name__ == 'Monster':
                if (e.inCombat or forceDo) and e.topLogo:
                    e.topLogo.showBlood(not beHide)

        gameglobal.gHideMonsterBlood = beHide

    def hideSpriteBlood(self, beHide):
        sprite = self.summonedSpriteInWorld
        if sprite and getattr(sprite, 'inCombat', False) and getattr(sprite, 'topLogo', None):
            sprite.topLogo.showBlood(not beHide)
        gameglobal.gHideSpriteBlood = beHide

    def hideOtherSpriteBlood(self, beHide):
        ent = BigWorld.entities.items()
        p = BigWorld.player()
        for id, e in ent:
            if e.__class__.__name__ == 'SummonedSprite':
                if e.inCombat and e.topLogo and p.summonedSpriteInWorld != e:
                    e.topLogo.showBlood(not beHide)

        gameglobal.gHideOtherSpriteBlood = beHide

    def hideSpriteName(self, beHide):
        sprite = self.summonedSpriteInWorld
        if sprite and getattr(sprite, 'topLogo', None):
            sprite.topLogo.hideName(beHide)
        gameglobal.gHideSpriteName = beHide

    def hideOtherSpriteName(self, beHide):
        ent = BigWorld.entities.items()
        p = BigWorld.player()
        for id, e in ent:
            if e.__class__.__name__ == 'SummonedSprite':
                if e.topLogo and p.summonedSpriteInWorld != e:
                    e.topLogo.hideName(beHide)

        gameglobal.gHideOtherSpriteName = beHide

    def hidePlayerName(self, beHide):
        if self.topLogo:
            self.topLogo.hideName(beHide)
            self.topLogo.hideAvatarTitle(gameglobal.gHidePlayerTitle)
        gameglobal.gHidePlayerName = beHide

    def hideAvatarName(self, beHide):
        ent = BigWorld.entities.items()
        for id, e in ent:
            if e.__class__.__name__ == 'Avatar':
                if e.topLogo:
                    e.topLogo.hideName(beHide)
                    e.topLogo.hideAvatarTitle(gameglobal.gHideAvatarTitle)

        gameglobal.gHideAvatarName = beHide

    def hidePlayerGuild(self, beHide):
        gameglobal.gHidePlayerGuild = beHide
        if self.topLogo and self.guildNUID:
            if beHide:
                self.topLogo.hideGuildIcon(True)
            else:
                self.topLogo.hideGuildIcon(False)

    def hideAvatarGuild(self, beHide):
        gameglobal.gHideAvatarGuild = beHide
        ent = BigWorld.entities.items()
        for id, e in ent:
            if e.__class__.__name__ == 'Avatar':
                if e.topLogo and e.guildNUID:
                    if beHide:
                        e.topLogo.hideGuildIcon(True)
                    else:
                        e.topLogo.hideGuildIcon(False)

    def hideMonsterName(self, beHide):
        ent = BigWorld.entities.items()
        for id, e in ent:
            if e.__class__.__name__ == 'Monster':
                if e.topLogo:
                    e.topLogo.hideName(beHide)
                    e.topLogo.hideTitleName(gameglobal.gHideMonsterTitle)

        gameglobal.gHideMonsterName = beHide

    def hideNpcName(self, beHide):
        ent = BigWorld.entities.items()
        for id, e in ent:
            if e.__class__.__name__ in ('Npc', 'Dawdler', 'MovableNpc'):
                if e.topLogo:
                    e.topLogo.hideName(beHide)
                    e.topLogo.hideTitleName(gameglobal.gHideNpcTitle)

        gameglobal.gHideNpcName = beHide

    def hidePlayerTitle(self, beHide):
        gameglobal.gHidePlayerTitle = beHide
        if self.topLogo:
            self.topLogo.hideAvatarTitle(beHide)

    def hideAvatarTitle(self, beHide):
        gameglobal.gHideAvatarTitle = beHide
        ent = BigWorld.entities.items()
        for id, e in ent:
            if e.__class__.__name__ == 'Avatar':
                if e.topLogo:
                    e.topLogo.hideAvatarTitle(beHide)

    def hideMonsterTitle(self, beHide):
        ent = BigWorld.entities.items()
        for id, e in ent:
            if e.__class__.__name__ == 'Monster':
                if e.topLogo:
                    e.topLogo.hideTitleName(beHide)

        gameglobal.gHideMonsterTitle = beHide

    def hideNpcTitle(self, beHide):
        ent = BigWorld.entities.items()
        for id, e in ent:
            if e.__class__.__name__ in ('Npc', 'Dawdler', 'MovableNpc'):
                if e.topLogo:
                    e.topLogo.hideTitleName(beHide)

        gameglobal.gHideNpcTitle = beHide

    def canFloatage(self):
        return getattr(self.model, 'floatage', None)

    def isLoseGravity(self):
        return self.physics.gravity <= 0.0

    def inMoving(self):
        if abs(self.physics.velocity.x) > 0.0 or abs(self.physics.velocity.z) > 0.0:
            self.isMoving = True
        else:
            self.isMoving = False
        return self.isMoving or abs(self.physics.velocity.y) > 0.0

    def onKeyLeaveRideAndZaiju(self, down):
        if down:
            if self.inFlyTypeWing():
                self.cell.leaveWingFly()
                if self.checkPathfinding():
                    self.cancelPathfinding()
            if self.carrier.get(self.id) and self.carrier.isRunningState():
                self.cell.applyLeaveCarrier()
                return
            if self.carrier.get(self.id) and self.carrier.isReadyState():
                self.cell.cancelSelfReadyState()
                return
            if self.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
                self.cell.leaveRide()
            if self.bianshen[0] != gametypes.BIANSHEN_HUMAN:
                if gameglobal.rds.ui.zaiju.mediator:
                    gameglobal.rds.ui.zaiju.leaveZaiju()
                else:
                    gameglobal.rds.ui.zaijuV2.leaveZaiju()
            if self.inCarrousel():
                if not self._checkCanLeaveCarrousel():
                    self.showGameMsg(GMDD.data.FORBID_LEAVE_CARROUSEL, ())
                else:
                    self.cell.leaveCarrousel()
            if self.inInteractiveObject():
                self.quitInteractiveObj()
            if self.weaponInHandState() == gametypes.WEAR_BACK_ATTACH:
                self.updateBackWear(True)
                if self.modelServer.backwear.isActionJustSkillWear():
                    self.fashion.stopAllActions()
            elif self.weaponInHandState() == gametypes.WEAR_WAIST_ATTACH:
                self.updateWaistWear(True)
                if self.modelServer.waistwear.isActionJustSkillWear():
                    self.fashion.stopAllActions()
            if self.inCarrousel():
                self.leaveCarrousel()
            gameglobal.rds.ui.buffSkill.pressLeaveZaiJu()

    def getSpeedData(self):
        return utils.getAvatarSpeedData(self)

    def changeModel(self):
        self.modelServer.bodyUpdateStatus = modelServer.BODY_UPDATE_STATUS_NORMAL
        self.modelServer.bodyUpdate()
        self.modelServer.wearUpdate()

    def showEntityId(self, show):
        gameglobal.gmShowEntityID = show
        self.topLogo.showEntityId(gameglobal.showEntityID)

    def testCreateNpc(self):
        self.cell.testCreateNpc(10275)
        self.cell.testCreateNpc(10276)
        self.cell.testCreateNpc(10277)
        self.cell.testCreateNpc(10278)
        self.cell.testCreateNpc(10279)
        self.cell.testCreateNpc(10287)

    def testFollow(self, owner):
        entityID = BigWorld.createEntity('Actor', self.spaceID, owner.id, owner.position, (0, 0, 0), {'modelID': 54001})
        entity = BigWorld.entity(entityID)
        entity.fashion.loadSinglePartModel('char/54001/54001.model')
        scaleMatrix = Math.Matrix()
        scaleMatrix.setScale((5.0, 2.0, 5.0))
        mp = Math.MatrixProduct()
        mp.a = scaleMatrix
        mp.b = entity.matrix
        model = BigWorld.PyModelObstacle('char/54001/54001.model', mp, True)
        entity.addModel(model)
        model.vehicleID = owner.id
        model.setEntity(self.id)
        entity.firstFetchFinished = True
        entity.setTargetCapsUse(True)
        entity.filter = BigWorld.ClientFilter()
        follow = BigWorld.Follow()
        follow.target = owner.model.node('HP_back')
        follow.biasPos = (0, owner.model.height + 0.2, 0)
        follow.clampPos = False
        follow.clampYaw = True
        follow.applyDrop = False
        follow.hardAttach = False
        entity.model.addMotor(follow)

    def testCreateAvatars(self, radius = 20, createNumber = 20, isShowFashion = False):
        if BigWorld.isPublishedVersion():
            return
        signal = 0
        signal = commcalc.setSingleBit(signal, gametypes.SIGNAL_SHOW_FASHION, isShowFashion)
        res = self._randomCircle(self.position, radius, createNumber)
        for i in xrange(0, createNumber):
            entityID = BigWorld.createEntity('Avatar', self.spaceID, 0, res[i], (1, 0, 0), {'camp': 1,
             'pubAspect': self.aspect,
             'pubAvatarConfig': self.avatarConfig,
             'physique': self.physique,
             'signal': signal})
            createAvatars.append(entityID)

    def testDestroyAllAvatars(self):
        global createAvatars
        for eid in createAvatars:
            BigWorld.destroyEntity(eid)

        createAvatars = []

    def _randomCircle(self, center, radius, n):
        res = []
        for i in xrange(n):
            r = random.random() * radius
            t = random.random() * 6.28318530717958
            x = center[0] + r * math.cos(t)
            y = center[1]
            z = center[2] + r * math.sin(t)
            res.append((x, y, z))

        return res

    def testPathFind(self, seekPos):
        spaceNo = seekPos[-1] if len(seekPos) == 4 else self.spaceNo
        navigator.getNav().pathFinding((seekPos[0],
         seekPos[1],
         seekPos[2],
         spaceNo))

    def moveCameraNear(self, down):
        if self.isInBfDotaChooseHero:
            return
        if down and not HK.checkMouseRollUp():
            gameglobal.rds.cam.awayFrom(1)

    def moveCameraFar(self, down):
        if self.isInBfDotaChooseHero:
            return
        if down and not HK.checkMouseRollDown():
            gameglobal.rds.cam.closeTo(1)

    def startAutoMove(self, down):
        if down and self.ap:
            if self.ap.isAutoMoving:
                self.ap.stopAutoMove()
            else:
                self.ap.startAutoMove()

    def switchToRun(self, down):
        if not self.stateMachine.checkStatus(const.CT_WALK):
            return
        if self.ap:
            self.ap.switchToWalk(down)

    def needLockCameraAndDc(self):
        if self._isOnZaiju():
            zjd = ZD.data.get(self._getZaijuNo(), {})
            if zjd.get('lockCameraAndDc', False):
                return True
        if self._isInQTE():
            data = QTED.data.get(self.qteId, {})
            if data.get('lockCameraAndDc', False):
                return True
        if getattr(self, 'inMeiHuo', False):
            return True
        elif getattr(self, 'inFear', False):
            return True
        elif getattr(self, 'inChaoFeng', False):
            return True
        elif self.fashion.doingActionType() == action.WA_BAO_ACTION:
            return True
        else:
            if self.inCarrousel():
                carrousel = BigWorld.entities.get(self.carrousel[0], None)
                if carrousel:
                    data = CD.data.get(carrousel.carrouselId, {})
                    if data.get('lockCameraAndDc', False):
                        return True
            if self.isInApprenticeTrain() or self.isInApprenticeBeTrain():
                return True
            if self.coupleEmote:
                lockDC = CEBD.data.get(self.coupleEmote[0], {}).get('lockDC', None)
                if lockDC:
                    return True
            return False

    def forbidChangeYaw(self):
        if self._isOnZaijuOrBianyao():
            zNo = self._getZaijuOrBianyaoNo()
            if ZD.data.get(zNo, {}).get('lockTurnDir', None):
                return True
        return False

    def _teleportConfirmOK(self, destId):
        if not self._checkTeleportCD(2, True):
            return
        if gameglobal.rds.ui.map.isShow:
            gameglobal.rds.ui.map.openMap(False)
        clientUtils.teleportToStone(self.cell.onStoneTeleportConfirmed, destId)
        self.confirmBoxId = 0
        if self.checkPathfinding():
            self.cancelPathfinding()

    def _teleportAndReliveConfirmOK(self, destId):
        if not self._checkTeleportCD(2, True):
            return
        if gameglobal.rds.ui.map.isShow:
            gameglobal.rds.ui.map.openMap(False)
        self.cell.onStoneTeleportAndReliveConfirmed(destId)
        self.confirmBoxId = 0
        if self.checkPathfinding():
            self.cancelPathfinding()

    def _teleportConfirmCancel(self):
        self.confirmBoxId = 0

    def showTeleportStoneConfirm(self, destId, costItemId):
        if getattr(self, 'confirmBoxId', 0):
            return
        ok, cancel = gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, gameStrings.TEXT_PLAYRECOMMPROXY_494_1
        cash = self.getTeleportCost(destId)
        itemFameData = {}
        if costItemId:
            p = BigWorld.player()
            costItemName = ID.data.get(costItemId, {}).get('name', '')
            content = GMD.data.get(GMDD.data.TELEPORT_STONE_COST_CASH_ITEM).get('text') % (cash, costItemName)
            item = Item(costItemId)
            if p._isSoul():
                currentCount = p.crossInv.countItemInPages(item.getParentId(), enableParentCheck=True)
            else:
                currentCount = p.inv.countItemInPages(item.getParentId(), enableParentCheck=True)
            needNum = 1
            itemFameData['itemId'] = costItemId
            itemFameData['deltaNum'] = needNum - currentCount
        else:
            content = GMD.data.get(GMDD.data.TELEPORT_STONE_COST_CASH).get('text') % (cash,)
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(ok, Functor(self._teleportConfirmOK, destId)), MBButton(cancel, self._teleportConfirmCancel)]
        self.confirmBoxId = gameglobal.rds.ui.messageBox.show(True, '', content, buttons, itemFameData=itemFameData)

    def showWingWorldTeleportStoneConfirm(self, destId, cash, extraCash):
        if getattr(self, 'confirmBoxId', 0):
            return
        ok, cancel = gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, gameStrings.TEXT_PLAYRECOMMPROXY_494_1
        if extraCash:
            if cash:
                content = GMD.data.get(GMDD.data.WING_WORLD_TELEPORT_STONE_COST_CASH_EXTRA).get('text') % (cash, extraCash)
            else:
                content = GMD.data.get(GMDD.data.WING_WORLD_TELEPORT_STONE_COST_CASH_ONLY_EXTRA).get('text') % (extraCash,)
        else:
            content = GMD.data.get(GMDD.data.WING_WORLD_TELEPORT_STONE_COST_CASH).get('text') % (cash,)
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(ok, Functor(self._teleportConfirmOK, destId)), MBButton(cancel, self._teleportConfirmCancel)]
        self.confirmBoxId = gameglobal.rds.ui.messageBox.show(True, '', content, buttons, itemFameData={})

    def showTeleportStoneAndReliveConfirm(self, destId, costItemId):
        if getattr(self, 'confirmBoxId', 0):
            return
        ok, cancel = gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, gameStrings.TEXT_PLAYRECOMMPROXY_494_1
        cash = self.getTeleportCost(destId)
        if costItemId:
            costItemName = ID.data.get(costItemId, {}).get('name', '')
            content = GMD.data.get(GMDD.data.TELEPORT_STONE_COST_CASH_ITEM).get('text') % (cash, costItemName)
        else:
            content = GMD.data.get(GMDD.data.TELEPORT_STONE_COST_CASH).get('text') % (cash,)
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(ok, Functor(self._teleportAndReliveConfirmOK, destId)), MBButton(cancel, self._teleportConfirmCancel)]
        self.confirmBoxId = gameglobal.rds.ui.messageBox.show(True, '', content, buttons)

    def showLvUpEffect(self):
        gameglobal.rds.sound.playSound(gameglobal.SD_21)
        tintLvUpDelay = SCD.data.get('tintLvUpDelay', 0.6)
        cameraLvUpDelay = SCD.data.get('cameraLvUpDelay', 0.6)
        screenEffectLvUpDelay = SCD.data.get('screenEffectLvUpDelay', 0.6)
        BigWorld.callback(tintLvUpDelay, lambda : tintalt.ta_add([self.modelServer.bodyModel], SCD.data.get('tintLvUp', 'gaoLiangShengji'), ['gaoLiang', BigWorld.shaderTime()], 3, tintType=tintalt.AVATARTINT))
        cameraPram = SCD.data.get('cameraParamLvUp', (0.1,
         0.1,
         0.1,
         0,
         (0.2, 0.05, 0.1),
         10,
         ((0.05, 0.2),)))
        BigWorld.callback(cameraLvUpDelay, Functor(self.playSpecialShakeCamera, {'shakeCamera': cameraPram}))
        effectId = SCD.data.get('screenEffectParamLvUp', 1012)
        BigWorld.callback(screenEffectLvUpDelay, Functor(screenEffect.startEffect, gameglobal.EFFECT_TAG_LVUP, effectId))

    def needSelectEntity(self, entityId):
        entity = BigWorld.entities.get(entityId)
        if not entity or not entity.inWorld:
            return False
        canSelect = self.ap.needSelect(entity)
        return canSelect

    def checkMapLimitUI(self, uiType):
        mapId = formula.getMapId(self.spaceNo)
        data = MCD.data.get(mapId, {})
        limitUIs = data.get('limitUIs')
        if not limitUIs:
            return True
        elif limitUIs == gametypes.MAP_LIMIT_UI_ALL or uiType in limitUIs:
            self.showGameMsg(GMDD.data.MAP_LIMIT_OP, (gametypes.MAP_LIMIT_OP_NAME.get(gametypes.MAP_LIMIT_OP_UI),))
            return False
        else:
            return True

    def logClientPerFormace(self):
        enableLogClientPerformance = gameglobal.rds.configData.get('enableLogClientPerformance', False)
        if not enableLogClientPerformance:
            return
        else:
            perFormanceInfo = BigWorld.getPerformanceInfo()
            if not perFormanceInfo:
                return
            perFormanceInfoKeys = perFormanceInfo.keys()
            for key in perFormanceInfoKeys:
                if key not in ('gpusensor_0', 'gpusensor_1', 'gpusensor_2', 'gpusensor_3'):
                    val = float(perFormanceInfo[key])
                if PERFORMANCE_EYS.has_key(key):
                    del perFormanceInfo[key]
                    perFormanceInfo[PERFORMANCE_EYS[key]] = val

            perFormanceInfo['roleName'] = self.roleName
            perFormanceInfo['lv'] = self.lv
            perFormanceInfo['serverId'] = gameglobal.rds.gServerid
            perFormanceInfo['mapId'] = str(self.mapID)
            perFormanceInfo['gbId'] = self.gbId
            perFormanceInfo['position'] = str(self.position)
            perFormanceInfo['videoQualityLv'] = appSetting.VideoQualitySettingObj.getVideoQualityLv()
            calcFrameHistory = getattr(BigWorld, 'calculateFrameHistory', None)
            calcTimedHistory = getattr(BigWorld, 'calculateTimedHistory', None)
            if calcFrameHistory != None:
                perFormanceInfo['frame_time'] = calcFrameHistory('frame_time', 'mean', 300)
                for k in ['pause_time_ratio', 'pause_count_ratio']:
                    perFormanceInfo[k] = calcFrameHistory(k, 'mean', 2)

            if calcTimedHistory != None:
                for k in ['pymodel_count',
                 'particle_count',
                 'bgtask_count',
                 'world_gui_draw_count']:
                    perFormanceInfo[k] = calcTimedHistory(k, 'mean', 60)

            perFormanceInfo['isBackground'] = float(not gameglobal.gIsAppActive)
            perFormanceInfo['screenWidth'] = BigWorld.screenWidth()
            perFormanceInfo['screenHeight'] = BigWorld.screenHeight()
            perFormanceInfo['runTime'] = BigWorld.time()
            perFormanceInfo['inCombat'] = self.inCombat
            perFormanceInfo['inLoadingProgress'] = self.ap.inLoadingProgress
            perFormanceInfo['entityCnt'] = len(BigWorld.entities.values())
            perFormanceInfo = zlib.compress(cPickle.dumps(perFormanceInfo, -1))
            self.base.recordClientPerFormance(gametypes.CLIENT_RECORD_TYPE_PERFORMANCE, perFormanceInfo)
            return

    def checkLatency(self, latencyTime):
        latencyThreshold = SCD.data.get('latencyThreshold', 500)
        if gameglobal.rds.configData.get('enablePushUU', False) and not self.hasPushLatencyMsg and latencyTime >= latencyThreshold:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_LATENCY, {'latencyTime': latencyTime})
            self.hasPushLatencyMsg = True

    def isRealInFuben(self):
        return self.inFuben() and not self.inDuelZone()

    def cancelBdbErrorTip(self):
        pass

    def showBdbErrorTip(self):
        bdbMsgBoxId = getattr(self, 'bdbMsgBoxId', None)
        if bdbMsgBoxId:
            gameglobal.rds.ui.messageBox.dismiss(bdbMsgBoxId)
        msg = SCD.data.get('bdbErrorTipMsg', gameStrings.TEXT_IMPPLAYERCOMM_1715)
        self.bdbMsgBoxId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, BigWorld.quit, gameStrings.TEXT_PLAYRECOMMPROXY_495, self.cancelBdbErrorTip, gameStrings.TEXT_IMPPLAYERCOMM_1716)

    def _checkTeleportCD(self, cd = 2.0, reset = False):
        lastTeleportCheckTime = getattr(self, 'lastTeleportCheckTime', 0)
        flag = utils.getNow() - lastTeleportCheckTime > cd
        if flag and reset:
            self.lastTeleportCheckTime = utils.getNow()
        return flag

    def delayTakeFigurePhto(self):
        enableCharSnapshot = gameglobal.rds.configData.get('enableCharSnapshot', False)
        if not enableCharSnapshot:
            return
        checkTime = random.uniform(2, 120) * 5
        BigWorld.callback(checkTime, self.takeFigurePhoto)

    def rideWingBagSlotEnlarge(self, page, pos):
        self.rideWingBag.posCountDict[page] = pos
        gameglobal.rds.ui.wingAndMount.refreshCommonPart()

    def pushZixunMsg(self):
        if gameglobal.rds.ui.ziXunInfo.canShow():
            now = utils.getNow()
            if utils.isSameDay(now, self.latestZiXunTime):
                return
            self.base.checkLatestZiXunTime(now)

    def notifyZiXunTime(self, succ, time):
        self.latestZiXunTime = time
        if succ:
            gameglobal.rds.ui.ziXunInfo.show()

    def nofityModelFinish(self):
        self.pushZixunMsg()

    def onEnterWorld(self):
        if gameglobal.rds.configData.get('enableWearPhysics', True):
            phy = None
            try:
                import PhysX as phy
                gameglobal.rds.wearPhysX = phy
            except:
                phy = None

            if phy:
                phy.init()
        if (self.profileIconStatus == gametypes.NOS_FILE_STATUS_SERVER_APPROVED or self.profileIconStatus == gametypes.NOS_FILE_STATUS_APPROVED) and self.profileIconUsed == False and self.iconUpload == True:
            photo = self.profileIcon if self.profileIcon else ''
            sex = self.physique.sex
            self.base.abandonNOSFile(self.friend.photo)
            self.cell.updateProfileApply(True, False)
            self.base.updateProfile(0, photo, 0, 1, 1, sex, 0, 0, 0, '', '', '')
            keyList = [const.PERSONAL_ZONE_DATA_CUSTOM_PHOTO, const.PERSONAL_ZONE_DATA_CURR_PHOTO]
            valueList = [self.profileIcon, self.profileIcon]
            self.base.setPersonalZoneInfo(keyList, valueList)
        BigWorld.callback(2, self._onEnterWorldDelay)
        if hasattr(BigWorld, 'setClientScriptTickMaxTime'):
            BigWorld.setClientScriptTickMaxTime(gameglobal.SCRIPT_TICK_MAX_TIME)
        if hasattr(self, 'guild') and hasattr(self.guild, 'announcement') and self.guild.announcement:
            gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_GUILD, gameStrings.TEXT_IMPGUILD_500 + self.guild.announcement, '')
        if gameglobal.rds.configData.get('enableCCSpeak', False) and not AppSettings.get(keys.SET_TEAM_OPEN_CC, 1):
            ccManager.instance().init()

    def _onEnterWorldDelay(self):
        if not self.inWorld:
            return
        self.checkAvatarZhuangshi()
        gameglobal.rds.ui.excitementIcon.show()
        self.cell.queryPartnersEquipment()

    def sendFeiHuoInfo(self):
        if gameglobal.rds.loginType == gameglobal.GAME_LOGIN_TYPE_FEIHUO:
            gameglobal.rds.logLoginState = gameglobal.GAME_FEIHUO_PLAYER
        elif gameglobal.rds.loginType == gameglobal.GAME_LOGIN_TYPE_YIYOU:
            gameglobal.rds.logLoginState = gameglobal.GAME_YIYOU_PLAYER
        elif gameglobal.rds.loginType == gameglobal.GAME_LOGIN_TYPE_SHUNWANG:
            gameglobal.rds.logLoginState = gameglobal.GAME_SHUNWANG_PLAYER
        else:
            gameglobal.rds.logLoginState = gameglobal.GAME_PLAYER
        netWork.sendInfoForLianYun(gameglobal.rds.logLoginState)

    def onLeaveWorld(self):
        try:
            scenIns = scenario.Scenario.PLAY_INSTANCE
            if scenIns and gameglobal.SCENARIO_PLAYING:
                scenIns.stopPlay()
        except:
            pass

        editorHelper.instance().destroy()
        gameglobal.rds.roomData = {}
        gameglobal.rds.furnitureExpireData = {}
        gameglobal.rds.roomVersionIds = {}
        gameglobal.rds.roomDataIdx = -1
        if gameglobal.CURRENT_WINDOW_STYLE == gameglobal.WINDOW_STYLE_CHAT:
            self.setWindowStyle(gameglobal.WINDOW_STYLE_NORMAL)
        gameglobal.rds.ui.voiceSetting.resetMode()
        ccManager.instance().release()

    def getFearRandomPos(self):
        distance = SCD.data.get('fearRadomDist', 6)
        x = self.position[0] + (random.random() - 0.5) * distance * 2
        z = self.position[2] + (random.random() - 0.5) * distance * 2
        pos = BigWorld.findDropPoint(self.spaceID, Math.Vector3(x, self.position[1], z))
        if pos:
            pos = pos[0]
        return pos

    def beginFear(self):
        self.endFearCallback()
        randomPos = self.getFearRandomPos()
        if not randomPos:
            randomPos = self.getFearRandomPos()
        if randomPos:
            self.ap.seekPath(randomPos)
        fearInterval = SCD.data.get('fearInterval', 0.5)
        self.fearCB = BigWorld.callback(fearInterval, self.beginFear)

    def endFearCallback(self):
        if self.fearCB:
            BigWorld.cancelCallback(self.fearCB)
            self.fearCB = None

    def getMeiHuoTarget(self):
        if self.isEnemy(self.targetLocked):
            return self.targetLocked
        else:
            return self.getNearestTargetForMeiHuo(BigWorld.entities.values())

    def beginMeiHuo(self):
        self.endMeiHuoCallback()
        target = self.getMeiHuoTarget()
        if target:
            if self.targetLocked != target:
                self.lockTarget(target)
            length = self.getHorDist(target)
            self.faceTo(target)
            if length > self.autoSkill.getDistWithBodySize() - 1:
                if not self.ap.isChasing:
                    self.chaseEntity(target, self.autoSkill.getDistWithBodySize() - 1)
            elif self.canBeAttack(target):
                self.autoSkill.start()
        fearInterval = SCD.data.get('fearInterval', 0.5)
        self.meiHuoCB = BigWorld.callback(fearInterval, self.beginMeiHuo)

    def endMeiHuoCallback(self):
        if self.meiHuoCB:
            BigWorld.cancelCallback(self.meiHuoCB)
            self.meiHuoCB = None
            self.autoSkill.stop()

    def getChaoFengTarget(self):
        chaoFengState = self.inChaoFeng
        if chaoFengState:
            state = self.statesServerAndOwn.get(chaoFengState)
            if state:
                srcId = state[0][gametypes.STATE_INDEX_SRCID]
                return BigWorld.entities.get(srcId)

    def getHorDist(self, target):
        return (self.position - target.position).length

    def beginChaoFeng(self):
        self.endChaoFengCallback()
        target = self.getChaoFengTarget()
        if target:
            if self.targetLocked != target:
                self.lockTarget(target)
            length = self.getHorDist(target)
            self.faceTo(target)
            if length > self.autoSkill.getDistWithBodySize() - 1:
                if not self.ap.isChasing:
                    self.chaseEntity(target, self.autoSkill.getDistWithBodySize() - 1)
            elif self.canBeAttack(target):
                self.autoSkill.start()
        fearInterval = SCD.data.get('fearInterval', 0.5)
        self.chaoFengCB = BigWorld.callback(fearInterval, self.beginChaoFeng)

    def endChaoFengCallback(self):
        if self.chaoFengCB:
            BigWorld.cancelCallback(self.chaoFengCB)
            self.chaoFengCB = None
            self.autoSkill.stop()

    def beginSpeedField(self):
        self.endSpeedFieldCB()
        if self.speedField and self.speedField[0]:
            self.ap.updateVelocity()
        speedFieldInterval = SCD.data.get('speedFieldInterval', 0.5)
        self.speedFieldCB = BigWorld.callback(speedFieldInterval, self.beginSpeedField)

    def endSpeedFieldCB(self):
        if self.speedFieldCB:
            BigWorld.cancelCallback(self.speedFieldCB)
            self.speedFieldCB = None

    def turnCamera(self, isDown):
        if not isDown:
            return
        if self.inCombat:
            return
        cam = gameglobal.rds.cam
        cam.changeView(cam.currentScrollNum - 3)
        dc = BigWorld.dcursor()
        cc = BigWorld.camera()
        dc.pitch = 0
        deltaYaw = self.yaw + math.pi
        if deltaYaw > math.pi:
            deltaYaw -= 2 * math.pi
        if hasattr(cc, 'deltaYaw'):
            cc.deltaYaw += deltaYaw - cc.direction.yaw

    def isNewRoleForOperation(self):
        if not hasattr(self, 'birthTime'):
            return False
        return self.birthTime > SCD.data.get('birthTimeForOperation', 1460104200)

    def showInteractiveObjStory(self, objId):
        interactiveObjStoryInterval = SCD.data.get('interactiveObjStoryInterval', 90)
        if utils.getNow() - self.interactiveObjStoryLastTime < interactiveObjStoryInterval:
            return
        self.interactiveObjStoryLastTime = utils.getNow()
        gameglobal.rds.ui.interactiveObj.showStoryWidget(objId)

    def showShaXingWaitMsgBox(self, delayTime):
        msg = SCD.data.get('shaXingWaitMsg', gameStrings.TEXT_SHAXINGPROXY_38)
        gameglobal.rds.ui.shaXing.showWait(int(delayTime), msg)

    def hideShaXingWaitMsgBox(self):
        gameglobal.rds.ui.shaXing.closeWaitWidget()

    def showChooseGroupFailMsgBox(self):
        msg = SCD.data.get('shaXingchooseGroupFailMsg', gameStrings.TEXT_SHAXINGPROXY_39)
        gameglobal.rds.ui.shaXing.showNotChoose(msg)

    def refreshFightObserveActionBar(self):
        if self.inFightObserve():
            gameglobal.rds.ui.fightObserve.showActionBar()
        else:
            gameglobal.rds.ui.fightObserve.closeActionBar()

    def inFightObserve(self):
        return bool(self.obSpaceNo)

    def getObservedMembers(self):
        return self.observedMembers

    def inClanChallenge(self):
        fbNo = formula.getFubenNo(self.spaceNo)
        return fbNo in const.FB_NO_CLAN_WAR_CHALLENGE

    def inClanChallengeOb(self):
        fbNo = formula.getFubenNo(self.spaceNo)
        return fbNo in const.FB_NO_CLAN_WAR_CHALLENGE and self.inFightObserve()

    def tryOnModel(self, equip):
        items = []
        if not equip:
            self.showGameMsg(GMDD.data.NOTHING_TO_DREES_UP, ())
            return
        if equip.noEquip():
            self.showGameMsg(GMDD.data.NOTHING_TO_DREES_UP, ())
            return
        for equip in equip:
            if equip and equip.isFashionEquip():
                items.append(Item(equip.id))

        gameglobal.rds.ui.fittingRoom.addItems(items)

    def stopDelayQuestSimpleFindPos(self):
        if hasattr(self, 'delayQuestSimpleFindPosCallback') and self.delayQuestSimpleFindPosCallback != None:
            BigWorld.cancelCallback(self.delayQuestSimpleFindPosCallback)
            self.delayQuestSimpleFindPosCallback = None

    def delayQuestSimpleFindPos(self):
        self.stopDelayQuestSimpleFindPos()
        self.delayQuestSimpleFindPosCallback = BigWorld.callback(2, Functor(self.questSimpleFindPos, True))

    def questSimpleFindPos(self, isDown):
        if isDown:
            if gameglobal.rds.ui.questTrack.mediator and gameglobal.rds.ui.questTrack.simpleFindPosInfo:
                simpleFindPosInfo = gameglobal.rds.ui.questTrack.simpleFindPosInfo
                questId = simpleFindPosInfo.get('questId', 0)
                trackIdx = gameglobal.rds.ui.questTrack.getTrackedIds(questId) - 1
                if trackIdx < 0:
                    return
                type = simpleFindPosInfo.get('type', 0)
                if type == uiConst.QUEST_QUICK_COMPLETE_TYPE_FIND_POS:
                    if not gameglobal.rds.ui.puzzle.mediator:
                        uiUtils.findPosById(simpleFindPosInfo.get('posId', 0), True, self.stopAutoQuest)
                elif type == uiConst.QUEST_QUICK_COMPLETE_TYPE_AUCTION:
                    name = ID.data.get(simpleFindPosInfo.get('itemId', 0), {}).get('name', '')
                    self.openAuctionFun(searchItemName=name)
                questLoopId = commQuest.getQuestLoopIdByQuestId(questId)
                if type == uiConst.QUEST_QUICK_COMPLETE_TYPE_FIND_POS and QLD.data.get(questLoopId, {}).get('auto', 0):
                    self.startAutoQuest()
                    self.updateAutoQuestLoopId(questLoopId)
                else:
                    self.stopAutoQuest()

    def getQuestSimpleFindPosNeedMonsterIdList(self):
        if gameglobal.rds.ui.questTrack.mediator and gameglobal.rds.ui.questTrack.simpleFindPosInfo:
            simpleFindPosInfo = gameglobal.rds.ui.questTrack.simpleFindPosInfo
            questId = simpleFindPosInfo.get('questId', 0)
            trackIdx = gameglobal.rds.ui.questTrack.getTrackedIds(questId) - 1
            if trackIdx < 0:
                return []
            return commQuest.getQuestMonsterKillNeedMonsterIdList(BigWorld.player(), questId)
        return []

    def getSummonedSpritePrimaryPropBaseValue(self, index, propId):
        v = 0
        if propId == PDD.data.PROPERTY_ATTR_PW:
            v = self.primaryProp.bpow
        elif propId == PDD.data.PROPERTY_ATTR_INT:
            v = self.primaryProp.bint
        elif propId == PDD.data.PROPERTY_ATTR_PHY:
            v = self.primaryProp.bphy
        elif propId == PDD.data.PROPERTY_ATTR_SPR:
            v = self.primaryProp.bspr
        elif propId == PDD.data.PROPERTY_ATTR_AGI:
            v = self.primaryProp.bagi
        return v

    def isForbidRideFly(self):
        zoneName = ''
        if hasattr(BigWorld, 'getCurrentZoneName'):
            zoneName = BigWorld.getCurrentZoneName()
        forbidZonePrex = SCD.data.get('forbidZonePrex', 'forbidRideFly')
        if forbidZonePrex not in zoneName:
            return False
        return True

    def setDynamicSkybox(self, newMapId):
        newZoneName = ''
        newBaseProp = 0
        newTgtProp = 0
        if newMapId in WWCD.data.get('dynamicSkyboxMaps', ()):
            openedStage = getattr(self, 'wingWorldOpenedStage', 0)
            newZoneName, newBaseProp, newTgtProp = WWCD.data.get('dynamicSkyboxInfos', {}).get(openedStage, ('', -2, 101))
        elif newMapId in const.FB_NO_MARRIAGE_HALL_SET:
            p = BigWorld.player()
            marriageBeInvitedInfo = getattr(self, 'marriageBeInvitedInfo', None)
            if marriageBeInvitedInfo:
                marriagePackageList = marriageBeInvitedInfo.get('marriagePackageList', ())
                mType = marriageBeInvitedInfo.get('mType', 0)
                subType = marriageBeInvitedInfo.get('subType', 0)
                if marriagePackageList and mType and subType:
                    zhutiData, fenweiData, xlYifuData, xnYifuData, blYifuData, bnYifuData, cheduiData = marriagePackageList
                    fenweiDataList = MPD.data.get((mType, subType), {}).get('fenwei', ())
                    fId = fenweiDataList[fenweiData - 1]
                    newZoneName, newBaseProp, newTgtProp = MCDD.data.get('dynamicSkyboxInfos', {}).get((newMapId, fId), ('', 0, 0))
        elif newMapId in (const.FB_NO_MARRIAGE_AMERICAN_HALL_ONLY, const.FB_NO_MARRIAGE_GREAT_ONLY):
            nowTime = formula.getXingJiTime()
            intTime = int(nowTime)
            idx = uiUtils.getXingJiWordIdx(intTime)
            for k, v in const.MARRIAGE_HALL_REVIEW_SKYBOX.iteritems():
                if idx in k:
                    newZoneName, newBaseProp, newTgtProp = v, const.MARRIAGE_HALL_BASE_PROP, const.MARRIAGE_HALL_TGT_PROP
                    break

        if newZoneName:
            oldZoneName, oldBaseProp, oldTgtProp = getattr(self, 'oldDynamicZoneInfo', ('', 0, 0))
            oldZoneName and BigWorld.setZonePriority(oldZoneName, oldBaseProp)
            BigWorld.setZonePriority(newZoneName, newTgtProp)
            self.oldDynamicZoneInfo = (newZoneName, newBaseProp, newTgtProp)

    def setMapConfig(self, old):
        oldMapId = formula.getMapId(old)
        newMapId = formula.getMapId(self.spaceNo)
        newMCD = MCD.data.get(newMapId, {})
        oldMCD = MCD.data.get(oldMapId, {})
        wingWorldOpenSkyboxMaps = WWCD.data.get('dynamicSkyboxMaps', ())
        if oldMapId in wingWorldOpenSkyboxMaps and newMapId not in wingWorldOpenSkyboxMaps:
            oldZoneName, oldBaseProp, oldTgtProp = getattr(self, 'oldDynamicZoneInfo', ('', 0, 0))
            _skybox = [ name for name, _, _ in WWCD.data.get('dynamicSkyboxInfos', {}).values() ]
            if oldZoneName in _skybox:
                BigWorld.setZonePriority(oldZoneName, oldBaseProp)
        if newMCD.has_key('setSkyZonePriority'):
            zoneName, basepri, tgtpri = newMCD['setSkyZonePriority']
            BigWorld.setZonePriority(zoneName, tgtpri)
        if oldMCD.has_key('setSkyZonePriority') and navigator.getPhaseMappingNum(old) == navigator.getPhaseMappingNum(self.spaceNo):
            zoneName, basepri, tgtpri = oldMCD['setSkyZonePriority']
            BigWorld.setZonePriority(zoneName, basepri)
        if newMCD.has_key('dynamicSkybox'):
            self.setDynamicSkybox(newMapId)
        if newMCD.get('enablePointLight', 0):
            BigWorld.enablePBRPointLight(True)
        elif oldMCD.get('enablePointLight', 0):
            BigWorld.enablePBRPointLight(False)
        if hasattr(BigWorld, 'enableVolDecal'):
            if newMCD.get('enableVolDecal', 0):
                BigWorld.enableVolDecal(True)
            elif oldMCD.get('enableVolDecal', 0):
                BigWorld.enableVolDecal(False)
        shaderIndex = newMCD.get('shaderIndex', 0)
        if shaderIndex:
            self.setSpaceShaderIndex(shaderIndex, True)
        else:
            self.forbidApplyShader = False
            oldShaderIndex = oldMCD.get('shaderIndex', 0)
            if oldShaderIndex:
                self.setSpaceShaderIndex(None, False)
        canGroupFollow = newMCD.get('canGroupFollow', 0)
        if not canGroupFollow:
            if getattr(self, 'groupNUID', None):
                if hasattr(self, 'isHeader') and self.isHeader():
                    if hasattr(self, 'getIsAllNotFollow') and not self.getIsAllNotFollow():
                        self.showGameMsg(GMDD.data.GROUPFOLLOW_FORBIDDEN_SPACE_HEADER_MSG, ())
                elif getattr(self, 'inGroupFollow', None):
                    self.showGameMsg(GMDD.data.GROUPFOLLOW_FORBIDDEN_SPACE_MEMBER_MSG, ())
                self.cell.cancelGroupFollow()
        videoSettingObj = appSetting.VideoQualitySettingObj
        if not videoSettingObj.isDofEnable():
            if newMCD.get('enableU3DOF', 0):
                BigWorld.enableU3DOF(True)
            elif oldMCD.get('enableU3DOF', 0):
                BigWorld.enableU3DOF(False)
        if oldMCD.has_key('playSoundId'):
            gameglobal.rds.sound.stopSound(oldMCD['playSoundId'])
        if newMCD.has_key('playSoundId'):
            gameglobal.rds.sound.playSound(newMCD['playSoundId'])
        if hasattr(BigWorld, 'occlusSetFrustumCullingOnly'):
            if const.WING_CITY_SPACE_START[0] <= newMapId <= const.WING_CITY_SPACE_START[1]:
                BigWorld.occlusSetFrustumCullingOnly(True)
            else:
                BigWorld.occlusSetFrustumCullingOnly(False)
        if newMapId == const.SPACE_NO_WING_WORLD_ISLAND:
            BigWorld.setVideoParams({'SHADOW': 0})
        elif oldMapId == const.SPACE_NO_WING_WORLD_ISLAND:
            videoSettingObj.apply()

    def notifyMusicCallBack(self, isValid, mId):
        if isValid:
            gameglobal.rds.sound.playMusic(mId)
        else:
            gameglobal.rds.sound.stopMusic(mId)

    def notifySoundEffectCallBack(self, isValid, sId):
        if isValid:
            gameglobal.rds.sound.playSound(sId)
        else:
            gameglobal.rds.sound.stopSound(sId)

    def setWindowStyle(self, style, isDebug = False, extra = {}):
        if style == gameglobal.CURRENT_WINDOW_STYLE:
            return
        if hasattr(BigWorld, 'setWindowStyle'):
            BigWorld.setWindowStyle(style)
        if not isDebug and hasattr(BigWorld, 'moveWindow'):
            if style != gameglobal.WINDOW_STYLE_NORMAL:
                size = gameglobal.WINDOW_STYLE_SIZE[style]
                w, h, _, _ = BigWorld.getScreenState()
                offsetHeight = (h - size[1]) / 2
                if offsetHeight < 0:
                    offsetHeight = 0
                BigWorld.moveWindow(w - size[0], offsetHeight, size[0] + 20, size[1] + 20)
            else:
                appSetting.setScreenSize()
                BigWorld.moveWindow(0, 0, 0, 0)
        oldStyle = gameglobal.CURRENT_WINDOW_STYLE
        gameglobal.CURRENT_WINDOW_STYLE = style
        if style in (gameglobal.WINDOW_STYLE_CHAT, gameglobal.WINDOW_STYLE_FLOAT_BALL):
            gameglobal.rds.ui.hideAllUIByLock()
            if not isDebug:
                BigWorld.limitForegroundFPS(30)
                BigWorld.worldDrawEnabled(0)
                self.lockKey(gameglobal.KEY_POS_FLOAT_BALL)
                self.addUnlockableHotKey(HK.KEY_SIMPLE_FIND_POS)
                self.oldScreenSize = BigWorld.getInnerScreenSize()
                BigWorld.setInnerScreenSize(1)
        else:
            BigWorld.worldDrawEnabled(1)
            gameglobal.rds.ui.restoreUIByUnLock()
            self.unlockKey(gameglobal.KEY_POS_FLOAT_BALL)
            self.removeUnlockableHotKey(HK.KEY_SIMPLE_FIND_POS)
            clientcom.resetLimitFps()
            if hasattr(self, 'oldScreenSize'):
                BigWorld.setInnerScreenSize(self.oldScreenSize)
        if oldStyle == gameglobal.WINDOW_STYLE_CHAT:
            gameglobal.rds.ui.extendChatBox.hide()
        elif oldStyle == gameglobal.WINDOW_STYLE_FLOAT_BALL:
            gameglobal.rds.ui.floatBall.hide()
        if style == gameglobal.WINDOW_STYLE_CHAT:
            BigWorld.limitWindowRange(gameglobal.EXTEND_CHAT_WIDTH, gameglobal.EXTEND_CHAT_HEIGHT, gameglobal.EXTEND_CHAT_MAX_WIDTH, gameglobal.EXTEND_CHAT_MAX_HEIGHT)
            gameglobal.rds.ui.extendChatBox.show(isDebug)
        elif style == gameglobal.WINDOW_STYLE_FLOAT_BALL:
            gameglobal.rds.ui.floatBall.show()
        elif style == gameglobal.WINDOW_STYLE_NORMAL:
            BigWorld.limitWindowRange(800, 600, -1, -1)
            gameglobal.rds.ui.chat.setLinkClickInfo(extra)
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CHAT_LOG)
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PUSH_MESSSAGES)

    def addUnlockableHotKey(self, key):
        if not hasattr(self, 'exclusiveHotKey'):
            self.exclusiveHotKey = []
        self.exclusiveHotKey.append(key)

    def removeUnlockableHotKey(self, key):
        if hasattr(self, 'exclusiveHotKey') and key in self.exclusiveHotKey:
            self.exclusiveHotKey.remove(key)

    def isInUnlockableHotKey(self, key, mods):
        if hasattr(self, 'exclusiveHotKey'):
            rdfkey = HK.keyDef(key, 1, mods)
            args = [ HK.HKM[k] for k in self.exclusiveHotKey ]
            if rdfkey in args:
                return True
        return False

    def checkWingFlyDash(self):
        result = self.stateMachine.checkStatus(const.CT_WINGFLY_DASH) and formula.getFubenNo(self.spaceNo) != const.FB_NO_MARRIAGE_GREAT_HALL
        return result

    def getModelHeight(self):
        carrierNo = self.wingWorldCarrier.carrierNo
        if carrierNo:
            wwcd = WWWCD.data.get(carrierNo, {})
            if wwcd.get('modelHeight', 0):
                return wwcd.get('modelHeight', 0)
        return super(self.__class__, self).getModelHeight()

    def showArmorMsg(self):
        mlgNo = formula.getMLGNo(self.spaceNo)
        showArmorTip = MDD.data.get(mlgNo, {}).get('showArmorTip', False) | FD.data.get(self.mapID, {}).get('showArmorTip', False)
        if showArmorTip and not self.isShowClanWarExcludeSelf():
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.ARMOR_MODE_TEXT, uiUtils.enabledClanWarArmorMode, isModal=False)

    def setBlackScreenEff(self, srcId, enable):
        blackEffMgr = blackEffectManager.getInstance()
        blackEffMgr.setBlackScreenEff(srcId, enable)
