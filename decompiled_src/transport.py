#Embedded file name: /WORKSPACE/data/entities/client/transport.o
import BigWorld
import Math
import gameglobal
import const
import formula
import gamelog
import gametypes
import keys
import clientcom
import clientUtils
from iNpc import INpc
from iDisplay import IDisplay
from sfx import sfx
from guis import messageBoxProxy
from helpers import modelServer
from guis import uiUtils
import wingWorldUtils
from data import transport_data as TD
from data import sys_config_data as SCD
from data import region_server_config_data as RSCD
from cdata import game_msg_def_data as GMDD
from cdata import transport_ref_data as TRD
confirmTextMap = {const.PORTAL_FB_EXIT: ('确定要退出副本吗？', '确定', '取消'),
 const.PORTAL_MULTILINE_ENTER: ('确定要进入分线吗？', '确定', '取消'),
 const.PORTAL_MULTILINE_EXIT: ('离开地宫将清除地宫内积累的鼓舞状态，是否确定离开地宫？', '确定', '取消'),
 const.PORTAL_DIGONG_BOSS_ENTER: ('确定要进入boss房吗？', '确定', '取消'),
 const.PORTAL_DIGONG_BOSS_EXIT: ('确定要离开boss房吗？', '确定', '取消'),
 const.PORTAL_TRANSPORT_STONE: ('传送需要花费%d云券', '确定', '取消')}
activeStoneSet = set()

class Transport(INpc, IDisplay):
    ACTIVE_DIST = 20

    def getItemData(self):
        td = TD.data.get(self.charType, None)
        if not td:
            return {'model': gameglobal.defaultModelID,
             'dye': 'Default'}
        else:
            itemData = {}
            itemkeys = ('heightOffset', 'modelShow', 'modelScale', 'dye', 'canselect')
            itemData.update([ (k, td[k]) for k in itemkeys if td.has_key(k) ])
            if self.pType == const.PORTAL_TRANSPORT_STONE:
                actualPhase = const.TRANSPORT_PHASE_ENABLED if self.isActiveStone() else const.TRANSPORT_PHASE_DISABLED
                if td.has_key('models'):
                    itemData['model'] = td['models'][actualPhase - 1]
                if td.has_key('attaches'):
                    itemData['attaches'] = [td['attaches'][actualPhase - 1]]
            else:
                if td.has_key('models'):
                    itemData['model'] = td['models'][self.phase - 1]
                if td.has_key('attaches'):
                    itemData['attaches'] = [td['attaches'][self.phase - 1]]
            return itemData

    def __init__(self):
        super(Transport, self).__init__()
        self.trapId = None
        self.activeTrapId = None
        self.isLeaveWorld = False
        self.confirmBoxId = 0
        self.radii = TD.data.get(self.charType, {}).get('radii', 0)
        self.clientTrigger = TD.data.get(self.charType, {}).get('clientTrigger', False)
        self.teleportType = TD.data.get(self.charType, {}).get('teleportType', const.TELEPORT_IMMEDIATE)
        self.initActive = TD.data.get(self.charType, {}).get('initActive', 0)
        self.validInBianyao = TD.data.get(self.charType, {}).get('validInBianyao', gametypes.FUNCTION_INVALID_FOR_YAO)
        self.obstacleModel = None
        p = BigWorld.player()
        if self.initActive and hasattr(p, 'transportHistory') and self.charType not in p.transportHistory:
            p.transportHistory.append(self.charType)

    def inTrap(self, ent):
        radii = self.radii or const.TRANSPORT_USE_DIST
        if (ent.position - self.position).lengthSquared <= radii ** 2:
            return True
        return False

    def enterWorld(self):
        super(Transport, self).enterWorld()
        if self.radii:
            self.trapId = BigWorld.addPot(self.matrix, self.radii, self.entitiesChanged)
        else:
            if getattr(self, 'trapId', None) != None:
                BigWorld.delPot(self.trapId)
                self.trapId = None
            self.trapId = BigWorld.addPot(self.matrix, const.TRANSPORT_USE_DIST, self.trapCallback)
        if self.isActiveStone():
            self.addActiveStone()
        elif self.pType == const.PORTAL_TRANSPORT_STONE:
            self.activeTrapId = BigWorld.addPot(self.matrix, self.ACTIVE_DIST, self.activeTrapCallback)
        BigWorld.player().transportIdSet.add(self.id)

    def getOpacityValue(self):
        p = BigWorld.player()
        data = TD.data.get(self.charType, {})
        visibleLvMin = data.get('visibleLvMin', 0)
        visibleLvMax = data.get('visibleLvMax', 0)
        if visibleLvMin + visibleLvMax:
            if p.lv < visibleLvMin or p.lv > visibleLvMax:
                return (gameglobal.OPACITY_HIDE, True)
        visibleNeedFinishedQuestID = data.get('visibleNeedFinishedQuestID', 0)
        if visibleNeedFinishedQuestID and not p.isQuestComplete(visibleNeedFinishedQuestID):
            return (gameglobal.OPACITY_HIDE, True)
        return (gameglobal.OPACITY_FULL, True)

    def afterModelFinish(self):
        super(Transport, self).afterModelFinish()
        self.refreshOpacityState()
        self.filter = BigWorld.DumbFilter()
        self.filter.clientYawMinDist = 0.0
        self.initYaw = self.yaw
        self.setTargetCapsUse(self.canSelected())
        if getattr(self, 'am', None):
            self.am.matchCaps = [keys.CAPS_HAND_FREE, keys.CAPS_GROUND]
        if self.isActiveStone():
            if TD.data.get(self.charType, {}).has_key('afterActiveAction'):
                self.fashion.playSingleAction(TD.data[self.charType]['afterActiveAction'])
        self.createObstacleModel()
        self.checkCollideWithPlayer(self.model)
        if self.topLogo and self.phase == const.TRANSPORT_PHASE_DISABLED:
            self.topLogo.hide(True)
        self.refreshOpacityState()

    def createObstacleModel(self):
        data = TD.data.get(self.charType, {})
        modelId = data.get('obstacleModel', 0)
        scale = data.get('modelScale', 1.0)
        if modelId:
            modelName = 'char/%d/%d.model' % (modelId, modelId)
            scaleMatrix = Math.Matrix()
            scaleMatrix.setScale((scale, scale, scale))
            mp = Math.MatrixProduct()
            mp.a = scaleMatrix
            mp.b = self.matrix
            BigWorld.fetchObstacleModel(modelName, mp, True, self._onLoadObstacleModel)

    def _onLoadObstacleModel(self, model):
        if not self.inWorld:
            return
        if model:
            self.obstacleModel = model
            self.addModel(model)
            model.setEntity(self.id)
            needCollide = TD.data.get(self.charType, {}).get('needCollide', True)
            model.setCollide(needCollide)
            self.checkCollideWithPlayer(model)

    def leaveWorld(self):
        super(Transport, self).leaveWorld()
        self.isLeaveWorld = True
        self.transportTrapCallback()
        if self.trapId != None:
            BigWorld.delPot(self.trapId)
            self.trapId = None
        if self.activeTrapId != None:
            BigWorld.delPot(self.activeTrapId)
            self.activeTrapId = None
        self.dismissConfirm()
        self.dismissDigongUI()
        self.removeActiveStone()
        self.removeAllFx()
        if self.obstacleModel:
            self.delModel(self.obstacleModel)
            self.obstacleModel = None
        if self.id in BigWorld.player().transportIdSet:
            BigWorld.player().transportIdSet.remove(self.id)

    def entitiesChanged(self, enteredTrap, handle):
        if not self.inWorld:
            return
        if enteredTrap and not self._invisiableOnYaoli():
            self.use()
        else:
            self.dismissConfirm()
            self.dismissDigongUI()

    def trapCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        opacityValue = self.getOpacityValue()
        if enteredTrap and opacityValue[0] == gameglobal.OPACITY_HIDE:
            return
        self.transportTrapCallback()

    def activeTrapCallback(self, enteredTrap, handle):
        if enteredTrap and not self.isActiveStone():
            self.cell.activeTransportStone()

    def transportTrapCallback(self):
        useDist = const.TRANSPORT_USE_DIST
        entities = []
        for entity in BigWorld.entities.values():
            if not isinstance(entity, Transport):
                continue
            if entity.clientTrigger:
                continue
            if entity.radii:
                continue
            if not (entity.position - BigWorld.player().position).lengthSquared < useDist * useDist:
                continue
            if entity.isLeaveWorld:
                continue
            if entity.phase == const.TRANSPORT_PHASE_DISABLED:
                continue
            entities.append(entity)

        BigWorld.player().transportTrapCallback(entities)

    def needBlackShadow(self):
        td = TD.data.get(self.charType, {})
        noBlackUfo = td.get('noBlackUfo', False)
        return not noBlackUfo

    def canSelected(self):
        return self.getItemData().get('canselect', 1)

    def confirmRefresh(self):
        self.confirmShow = False
        BigWorld.player().cell.applyFubenOnceAgain()

    def confirmOK(self):
        self.confirmShow = False
        p = BigWorld.player()
        if self.pType == const.PORTAL_TRANSPORT_STONE:
            if p.stateMachine.checkStatus(const.CT_TRANSPORT_USE):
                gameglobal.rds.ui.littleMap.doTeleport()
        else:
            enableTeleportSpell = gameglobal.rds.configData.get('enableTeleportSpell', False)
            if enableTeleportSpell:
                p.enterTeleportSpell(gameglobal.TELEPORT_SPELL_LEAVE_FUBEN, self.cell.teleportConfirmed)
            else:
                self.cell.teleportConfirmed()
        if getattr(p, 'inGroupFollow', None):
            p.cell.cancelGroupFollow()

    def confirmCancel(self):
        self.confirmShow = False
        if self.pType == const.PORTAL_TRANSPORT_STONE:
            gameglobal.rds.ui.littleMap.unShowTransportDest()

    def reloadModel(self):
        self.removeAllFx()
        itemData = self.getItemData()
        modelServer.loadModelByItemData(self.id, gameglobal.URGENT_THREAD, self.reloadFinished, itemData)
        if self.pType == const.PORTAL_TRANSPORT_STONE:
            gameglobal.rds.ui.littleMap.updateTransportStone(self.charType)

    def reloadFinished(self, model):
        self.modelServer._singlePartModelFinish(model)

    def checkRefresPrivilege(self):
        p = BigWorld.player()
        if p.isHeader():
            return True
        fbNo = formula.getFubenNo(p.spaceNo)
        if p.groupNUID:
            if formula.inMapGameSingleFuben(fbNo):
                return True
        else:
            fbType = formula.whatFubenType(fbNo)
            if fbType in const.FB_TYPE_SINGLE_SET:
                return True
        return False

    def showConfirm(self, destId = None):
        opacityValue = self.getOpacityValue()
        if opacityValue[0] == gameglobal.OPACITY_HIDE:
            return
        if hasattr(self, 'confirmShow') and self.confirmShow:
            return
        td = TD.data.get(self.charType, {})
        refresh = None
        if td.has_key('confirmText'):
            if len(td['confirmText']) == 4:
                content, refresh, ok, cancel = td['confirmText']
            else:
                content, ok, cancel = td['confirmText']
        else:
            content, ok, cancel = confirmTextMap.get(self.pType, ('\xc8\xb7\xb6\xa8\xd2\xaa\xb4\xab\xcb\xcd\xc2\xf0\xa3\xbf', '\xc8\xb7\xb6\xa8', '\xc8\xa1\xcf\xfb'))
        if self.pType == const.PORTAL_TRANSPORT_STONE:
            content = content % BigWorld.player().getTeleportCost(destId)
        MBButton = messageBoxProxy.MBButton
        gamelog.debug('zt: show transport confirm', content)
        if refresh != None and self.checkRefresPrivilege():
            buttons = [MBButton(refresh, self.confirmRefresh), MBButton(ok, self.confirmOK), MBButton(cancel, self.confirmCancel)]
        else:
            buttons = [MBButton(ok, self.confirmOK), MBButton(cancel, self.confirmCancel)]
        self.confirmBoxId = gameglobal.rds.ui.messageBox.show(False, '', content, buttons)
        self.confirmShow = True

    def dismissConfirm(self):
        if hasattr(self, 'confirmShow') and self.confirmShow:
            gameglobal.rds.ui.messageBox.dismiss(self.confirmBoxId)
            self.confirmShow = False

    def dismissDigongUI(self):
        if gameglobal.rds.ui.diGong.transportId == self.id:
            gameglobal.rds.ui.diGong.onClosePanel()

    @clientUtils.callFilter(1.0, False)
    def use(self):
        opacityValue = self.getOpacityValue()
        if opacityValue[0] == gameglobal.OPACITY_HIDE:
            return
        p = BigWorld.player()
        if self.phase == const.TRANSPORT_PHASE_OCCUPIED and self.belongTo != p.groupNUID:
            p.showGameMsg(GMDD.data.TRANSPORT_OCCUPIED, ())
            return
        if self.phase == const.TRANSPORT_PHASE_DISABLED:
            p.showGameMsg(GMDD.data.TRANSPORT_DISABLED, ())
            return
        checkStatus = const.CT_TRANSPORT_USE
        if self.pType == const.PORTAL_TRANSPORT_STONE:
            checkStatus = const.CT_TRANSPORT_STONE_USE
        if p._isOnZaiju() and p._getZaijuNo() in wingWorldUtils.getYabiaoZaijuNos():
            exclude = ('ZAIJU_ST', 'COMBAT_ST')
        else:
            exclude = ()
        if not p.stateMachine.checkStatus(checkStatus, exclude):
            return
        if self.pType == const.PORTAL_TRANSPORT_STONE and self.charType not in p.transportHistory:
            self.cell.activeTransportStone()
        else:
            self.cell.use()
        if self.phase == const.TRANSPORT_PHASE_OCCUPIED:
            p.cancelTransportSpell(const.CANCEL_ACT_TELEPORT)

    def activeTransportStone(self):
        td = TD.data.get(self.charType, {})
        actions = []
        if td.has_key('activeAction'):
            actions.append(td['activeAction'])
        if td.has_key('afterActiveAction'):
            actions.append(td['afterActiveAction'])
        if actions and self.fashion:
            self.fashion.playAction(tuple(actions), callback=getattr(self.modelServer, 'attachModelFromData', None), trigger=0)
        p = BigWorld.player()
        p.showGameMsg(GMDD.data.TRANSPORT_ACTIVED, td.get('name', ''))

    def set_phase(self, oldPhase):
        self.transportTrapCallback()
        self.reloadModel()

    def activeTransportStoneSuccessed(self):
        p = BigWorld.player()
        if not self.isActiveStone():
            self.activeTransportStone()
        p.transportHistory.append(self.charType)
        self.addActiveStone()
        sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (p.getEquipEffectLv(),
         p.getEquipEffectPriority(),
         p.model,
         SCD.data.get('sfxActiveTransport', 1272),
         sfx.EFFECT_LIMIT))
        gameglobal.rds.ui.littleMap.updateTransportStone(self.charType)

    def addActiveStone(self):
        if self.isActiveStone():
            activeStoneSet.add(self)

    def removeActiveStone(self):
        if self in activeStoneSet:
            activeStoneSet.remove(self)

    def isActiveStone(self):
        if self.pType == const.PORTAL_TRANSPORT_STONE:
            if self.charType in BigWorld.player().transportHistory or self.initActive:
                return True
        return False

    def leaveDlgRange(self, unUsedDist):
        if gameglobal.rds.ui.littleMap.stoneId == self.id:
            gameglobal.rds.ui.littleMap.unShowTransportDest()

    def showTargetUnitFrame(self):
        return False

    def enterTopLogoRange(self, rangeDist = -1):
        super(Transport, self).enterTopLogoRange(rangeDist)
        if not self.topLogo:
            return
        if self.phase == const.TRANSPORT_PHASE_DISABLED:
            self.topLogo.hide(True)

    def enterLoadModelRange(self, rangeDist = -1):
        pass

    def leaveLoadModelRange(self, rangeDist = -1):
        pass

    def checkCollideWithPlayer(self, model):
        player = BigWorld.player()
        if not model or not model.inWorld or not getattr(model, 'collidable', False) or not player.ap:
            return
        if clientcom.isIntersectWithPlayer(model):
            dist = 2.0
            invMatrix = Math.Matrix(model.matrix)
            invMatrix.invert()
            localPos = invMatrix.applyPoint(player.position)
            if localPos.x < 0:
                dstPos = Math.Vector3(0, 0, -dist)
            else:
                dstPos = Math.Vector3(0, 0, dist)
            mat = Math.Matrix(model.matrix)
            dstPos = mat.applyPoint(dstPos)
            player.physics.teleport(dstPos)

    def canOutline(self):
        return False

    def isUrgentLoad(self):
        return True


def isActiveStone(seekId):
    transportId = TRD.data.get(seekId, {}).get('destId', 0)
    p = BigWorld.player()
    if transportId:
        data = TD.data.get(transportId, {})
        if p.inWingCityOrBornIsland() and data.get('cityId'):
            if data.get('mustOwner', 0):
                cityId = data.get('cityId')
                if p.isWingWorldCampMode():
                    if not p.wingWorldCamp:
                        return cityId == RSCD.data.get(p.getOriginHostId(), {}).get('wingWorldNeighborCityId', 0)
                    return cityId in p.wingWorld.country.getOwnCamp().ownedCityIds or cityId == RSCD.data.get(p.getOriginHostId(), {}).get('wingWorldNeighborCityId', 0)
                else:
                    return cityId in p.wingWorld.country.getOwn().ownedCityIds or cityId == RSCD.data.get(p.getOriginHostId(), {}).get('wingWorldNeighborCityId', 0)
            else:
                return True
        elif data.get('initActive', 0) or transportId in getattr(BigWorld.player(), 'transportHistory', {}):
            return True
    return False


def getHiddenStone(seekId):
    isHiddenStone = TRD.data.get(seekId, {}).get('isHiddenStone', 0)
    return isHiddenStone
