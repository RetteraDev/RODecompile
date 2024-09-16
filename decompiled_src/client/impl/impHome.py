#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impHome.o
from gamestrings import gameStrings
import cPickle
import zlib
import random
import BigWorld
from appearance import Appearance
from equipment import Equipment
from item import Item
from physique import Physique
import gamelog
import gameglobal
import const
import gametypes
import formula
import utils
from helpers import strmap
from guis import uiConst
from guis import uiUtils
from helpers import editorHelper
from callbackHelper import Functor
import logicInfo
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD
from data import home_data as HD
from cdata import home_config_data as HCD
from data import map_config_data as MCD
from data import fitting_room_upgrade_data as FRUD

class ImpHome(object):

    def onQueryDoorplate(self, opType, lineNo, maxFloorNo, data):
        gamelog.debug('@zq onQueryDoorplate', maxFloorNo, cPickle.loads(zlib.decompress(data)))
        if opType == const.HOME_QUERY_DOOR_BUY_HOUSE:
            gameglobal.rds.ui.homeBuyHouses.show(maxFloorNo, cPickle.loads(zlib.decompress(data)))
        if opType == const.HOME_QUERY_DOOR_SEND_FLOOR:
            gameglobal.rds.ui.homeSendToFloor.show(maxFloorNo)

    def onQueryRoomInfo(self, opType, gbId, data):
        gamelog.debug('@zq onQueryRoomInfo', gbId, cPickle.loads(zlib.decompress(data)))
        if opType == const.HOME_QUERY_ROOM_TYPE_JIEQI_SHOW:
            gameglobal.rds.ui.homeCheckHouses.show(bool(cPickle.loads(zlib.decompress(data))))
        if opType == const.HOME_QUERY_ROOM_TYPE_REFRESH or opType == const.HOME_QUERY_HOME_KEY:
            if gameglobal.rds.ui.homeCheckHouses.mediator:
                gameglobal.rds.ui.homeCheckHouses.setCurData(gbId, cPickle.loads(zlib.decompress(data)))
                gameglobal.rds.ui.homeCheckHouses.refreshCurContent()

    def onQueryFloorInfo(self, floorNo, data):
        gamelog.debug('@zq onQueryFloorInfo', floorNo, cPickle.loads(zlib.decompress(data)))
        if gameglobal.rds.ui.homeSendToFloor.mediator:
            gameglobal.rds.ui.homeSendToFloor.refreshItems(floorNo, cPickle.loads(zlib.decompress(data)))

    def onOpenHomeEntrance(self, npcId, lines):
        gamelog.debug('@zq onOpenHomeEntrance:npcId,lines ', npcId, lines)
        if lines:
            if len(lines) > 1:
                gameglobal.rds.ui.homeEnterLines.show(lines)
            else:
                self.cell.enterHomeCommunity(lines[0])

    def onBeginModifyRoom(self, ok):
        gamelog.debug('@zq onBeginModifyRoom', ok)
        if ok:
            gameglobal.rds.ui.homeEditor.setEditMode()

    def onGetRoomData(self, ownerGbID, roomData, ownerName, furnitureExpireData, versionId, idx):
        roomData = cPickle.loads(zlib.decompress(roomData))
        furnitureExpireData = cPickle.loads(zlib.decompress(furnitureExpireData))
        oldVersionId = gameglobal.rds.roomVersionIds.get(ownerGbID, -1)
        if versionId < oldVersionId:
            return
        if idx == 0:
            gameglobal.rds.roomData = roomData
            gameglobal.rds.furnitureExpireData = furnitureExpireData
        else:
            if idx == -1:
                if oldVersionId == versionId:
                    gameglobal.rds.roomData.update(roomData)
                    gameglobal.rds.furnitureExpireData.update(furnitureExpireData)
                else:
                    gameglobal.rds.roomData = roomData
                    gameglobal.rds.furnitureExpireData = furnitureExpireData
                self.onGetAllRoomData(ownerGbID, gameglobal.rds.roomData, ownerName, gameglobal.rds.furnitureExpireData)
                gameglobal.rds.roomData = {}
                gameglobal.rds.furnitureExpireData = {}
                gameglobal.rds.roomVersionIds[ownerGbID] = -1
                return
            if idx and oldVersionId == versionId and idx == gameglobal.rds.roomDataIdx + 1:
                gameglobal.rds.roomData.update(roomData)
                gameglobal.rds.furnitureExpireData.update(furnitureExpireData)
        gameglobal.rds.roomDataIdx = idx
        gameglobal.rds.roomVersionIds[ownerGbID] = versionId

    def onGetAllRoomData(self, ownerGbID, roomData, ownerName, furnitureExpireData):
        gamelog.debug('@zq onGetRoomData', ownerGbID, roomData, ownerName, furnitureExpireData)
        self.furnitureExpireDict = {}
        self.setFurnitureExpireCallBack(furnitureExpireData)
        ins = editorHelper.instance()
        ins.ownerGbID = ownerGbID
        ins.ownerName = ownerName
        ins.removeAllFurniture()
        BigWorld.callback(1, Functor(ins.init, ownerGbID, roomData))

    def confirmRemoveRoom(self):

        def _closeNpcFunc(inputStr = ''):
            if gameglobal.rds.ui.funcNpc.isOnFuncState():
                gameglobal.rds.ui.funcNpc.close()

        def _expandHomeRoom(inputStr = ''):
            if inputStr == gameStrings.TEXT_IMPHOME_119:
                p = BigWorld.player()
                p.cell.removeHomeRoom()
                gameglobal.rds.ui.messageBox.dismiss()
                if gameglobal.rds.ui.funcNpc.isOnFuncState():
                    gameglobal.rds.ui.funcNpc.close()
            else:
                self.showGameMsg(GMDD.data.HOME_REMOVE_ROOM_INPUT_ERROR, ())

        gameglobal.rds.ui.messageBox.showYesNoInput(msg=gameStrings.TEXT_IMPHOME_128, yesCallback=_expandHomeRoom, title=gameStrings.TEXT_IMPHOME_130, inputMax=10, style=uiConst.MSG_BOX_INPUT_STRING, noCallback=_closeNpcFunc, dismissOnClick=False)

    def createHomeRoomSucc(self, lineNo, roomId, floorNo, roomNo):
        gamelog.debug('@zq createHomeRoomSucc', lineNo, roomId, floorNo, roomNo)
        msg = gameStrings.TEXT_IMPHOME_138 % (floorNo, uiConst.ROOM_NO_COLOR.get(roomNo, ''))
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.cell.enterRoomDirectlyByGbID, self.gbId))

    def openBuyHouse(self):
        if not self.myHome.curLineNo:
            self.showGameMsg(GMDD.data.PLAYER_NOT_IN_HOME_LINE, ())
        elif self.myHome.hasHome():
            self.showGameMsg(GMDD.data.PLAYER_ALREADY_HAS_HOME, ())
        elif self.lv < SCD.data.get('HOME_LV_LIMIT', 49):
            self.showGameMsg(GMDD.data.HOME_PLAYER_LV_NOT_ENOUGH, ())
        else:
            self.cell.queryDoorplate(const.HOME_QUERY_DOOR_BUY_HOUSE, self.myHome.curLineNo)

    def openCheckHouse(self):
        if self.friend.intimacyTgt:
            self.cell.queryRoomInfo(const.HOME_QUERY_ROOM_TYPE_JIEQI_SHOW, self.friend.intimacyTgt)
        else:
            gameglobal.rds.ui.homeCheckHouses.show(False)

    def openSendToFloor(self):
        self.cell.queryDoorplate(const.HOME_QUERY_DOOR_SEND_FLOOR, self.myHome.curLineNo)

    def onEnterHomeRoom(self):
        gameglobal.rds.ui.homeEditor.show()
        self.showGameMsg(GMDD.data.HOME_FURNITURE_IS_LOADING, ())

    def onLeaveHomeRoom(self):
        self.cancelRoomFurnitureCallBack()
        self.furnitureExpireDict = {}
        gameglobal.rds.ui.homeEditor.hide()
        gameglobal.rds.ui.homePermission.hide()

    def confirmExpendRoom(self):
        itemId, needNum = HD.data.get(self.myHome.roomId, {}).get('expandItemNeed', (0, 0))
        itemData = {}
        pg, ps = (-1, -1)
        if itemId:
            itemData = uiUtils.getGfxItemById(itemId)
            count = self.inv.countItemInPages(itemId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True)
            itemData['count'] = uiUtils.convertNumStr(count, needNum)
            pg, ps = self.inv.findItemInPages(itemId)
        cash = HD.data.get(self.myHome.roomId).get('expandCashNeed', 0)
        yesBtnEnable = True
        if self.cash + self.bindCash < cash or itemData and (pg == -1 or ps == -1):
            yesBtnEnable = False
        cashStr = uiUtils.convertNumStr(self.cash + self.bindCash, cash, showOwnStr=False)
        bonusIcon = {'bonusType': 'bindCash',
         'value': str(cashStr)}

        def _closeNpcFunc():
            if gameglobal.rds.ui.funcNpc.isOnFuncState():
                gameglobal.rds.ui.funcNpc.close()

        def _expandHomeRoom():
            self.cell.expandHomeRoom()
            if gameglobal.rds.ui.funcNpc.isOnFuncState():
                gameglobal.rds.ui.funcNpc.close()

        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_IMPHOME_196, Functor(self.confirmCashPay, cash, _expandHomeRoom), itemData=itemData, bonusIcon=bonusIcon, yesBtnEnable=yesBtnEnable, style=uiConst.MSG_BOX_BUY_ITEM, noCallback=_closeNpcFunc)

    def getPlayerHairColor(self):
        s = strmap.strmap(BigWorld.player().avatarConfig)
        return s.map.get('hairDyes', '')

    def adjustAvatarConfig(self, avatarConfig, hairColor):
        a = strmap.strmap(avatarConfig)
        a.set('hairDyes', hairColor)
        a.set('dyeMode', 1)
        return str(a)

    def updateFittingRoomData(self, uuid, equips, aspect, physique, avatarConfig, hairColor, actionId, itemPlusInfo):
        avatarConfig = self.adjustAvatarConfig(avatarConfig, hairColor)
        editorHelper.instance().updatePhysiqueInfo(uuid, equips, aspect, physique, avatarConfig, actionId, itemPlusInfo)
        entityId = editorHelper.instance().getEntityId(uuid)
        if entityId:
            entity = BigWorld.entities.get(entityId, None)
            if entity and entity.inWorld:
                entity.updatePhysiqueInfo(equips, aspect, physique, avatarConfig, actionId, itemPlusInfo)
                gameglobal.rds.ui.modelFittingRoom.refreshPartBoard()
                gameglobal.rds.ui.modelFittingRoom.refreshModel(entity)

    def cancelRoomFurnitureCallBack(self):
        if hasattr(self, 'furnitureExpireCallBack') and self.furnitureExpireCallBack:
            BigWorld.cancelCallback(self.furnitureExpireCallBack)
        self.furnitureExpireCallBack = None

    def removeRoomFurnitureFunc(self, uuid):
        if hasattr(self, 'furnitureExpireDict') and self.furnitureExpireDict.get(uuid, None):
            _info = {uuid: 0}
            ins = editorHelper.instance()
            ins.addModifiedSuccData(const.HOME_FURNITURE_OP_REMOVE, _info)
            self.furnitureExpireDict[uuid] = None

    def updateFurnitureFunc(self):
        delKeyList = []
        for key, value in self.furnitureExpireDict.iteritems():
            if value and not value - utils.getNow() > 0:
                self.removeRoomFurnitureFunc(key)
                delKeyList.append(key)

        for item in delKeyList:
            del self.furnitureExpireDict[item]

        self.setFurnitureExpireCallBack(self.furnitureExpireDict, False)

    def setFurnitureExpireCallBack(self, _info, bUpdate = True):
        self.cancelRoomFurnitureCallBack()
        if not hasattr(self, 'furnitureExpireDict'):
            self.furnitureExpireDict = {}
        if bUpdate:
            self.furnitureExpireDict.update(_info)
        if self.furnitureExpireDict:
            self.furnitureExpireCallBack = BigWorld.callback(5, self.updateFurnitureFunc)

    def onHomeAlterRoomFurniture(self, ownerGbID, addedInfo, removedInfo, extra):
        gamelog.debug('@bgf onHomeAlterRoomFurniture', ownerGbID, addedInfo, removedInfo, extra)
        expireDict = extra.get('expireDict', {})
        self.setFurnitureExpireCallBack(expireDict)
        ins = editorHelper.instance()
        if addedInfo:
            ins.addModifiedSuccData(const.HOME_FURNITURE_OP_ADD, addedInfo, ownerGbID=ownerGbID, extra=extra)
        if removedInfo:
            ins.addModifiedSuccData(const.HOME_FURNITURE_OP_REMOVE, removedInfo)
        if addedInfo or removedInfo:
            ins.batchSave(True, False)

    def onHomeUpdateRoomFurniture(self, ownerGbID, data):
        gamelog.debug('@bgf onHomeUpdateRoomFurniture', ownerGbID, data)
        ins = editorHelper.instance()
        if data:
            ins.addModifiedSuccData(const.HOME_FURNITURE_OP_UPDATE, data)
            ins.batchSave(False, True)

    def updateFittingRoomDataOther(self, ownerGbID, uuid, equips, aspect, physique, avatarConfig, hairColor, actionId, itemPlusInfo):
        avatarConfig = self.adjustAvatarConfig(avatarConfig, hairColor)
        editorHelper.instance().updatePhysiqueInfo(uuid, equips, aspect, physique, avatarConfig, actionId, itemPlusInfo)
        entityId = editorHelper.instance().getEntityId(uuid)
        if entityId:
            entity = BigWorld.entities.get(entityId, None)
            if entity and entity.inWorld:
                entity.updatePhysiqueInfo(equips, aspect, physique, avatarConfig, actionId, itemPlusInfo)

    def useGoHomeRoomSkill(self):
        if self.myHome.inHomeRoom():
            self.showGameMsg(GMDD.data.HOME_ALREADY_IN_ROOM, ())
        elif self.myHome.hasHome():
            if self.mapID == const.SPACE_NO_BIG_WORLD:
                lastTime = self.myHome.lastUseBackHomeSkillTime
                total = HCD.data.get('backHomeSkillCD', 1800)
                if utils.getNow() - lastTime < total:
                    self.showGameMsg(GMDD.data.ENTER_ROOM_FAILED_SKILL_CD, ())
                    return
            self.cell.enterRoomDirectlyByGbID(self.gbId)
        else:
            seekId = HCD.data.get('go_home_apartment_seekId', 0)
            msg = gameStrings.TEXT_IMPHOME_300 % seekId
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(uiUtils.findPosById, seekId), yesBtnText=gameStrings.TEXT_IMPHOME_301)

    def confirmCashPay(self, needCash, callFunction):
        if needCash <= self.cash + self.bindCash and needCash > self.bindCash:
            msg = GMD.data.get(GMDD.data.BINDCASH_IS_NOT_ENOUGH, {}).get('text', gameStrings.TEXT_SKILLPROXY_1402)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=callFunction, msgType='bindCash', isShowCheckBox=True)
        elif needCash > self.cash + self.bindCash:
            self.showGameMsg(GMDD.data.HOME_BUY_CASH_NOT_ENOUGH, ())
        elif needCash <= self.bindCash:
            callFunction()

    def homeRoomFangKaDian(self):
        if formula.spaceInHome(self.spaceNo):
            self.cell.homeRoomFangKaDian()

    def inHomeFittingRoom(self, position = None, fittingRoomLv = 0):
        if formula.spaceInHomeRoom(self.spaceNo):
            fittingRoomBound = MCD.data.get(self.mapID, {}).get('fittingRoomBound', [])
            if fittingRoomLv:
                fittingRoomBound = [fittingRoomBound[fittingRoomLv - 1]]
            if fittingRoomBound:
                for bound in fittingRoomBound:
                    bound0, bound1 = bound
                    x0, x1 = min(bound0[0], bound1[0]), max(bound0[0], bound1[0])
                    z0, z1 = min(bound0[2], bound1[2]), max(bound0[2], bound1[2])
                    if position == None:
                        position = self.position
                    x, y, z = position
                    if x0 <= x <= x1 and z0 <= z <= z1:
                        return True

        return False

    def onGetFittingRoomItemLink(self, uuid, nuid, equipments, aspect, physique, avatarConfig, itemId, ownerName):
        furnitureName = utils.getFurnitureName(itemId)
        msg = utils.getModelShareLinkMsg(ownerName, str(nuid), furnitureName)
        gameglobal.rds.ui.sendLink(msg)

    def onTakeFittingRoomItemDetail(self, stamp, data, fid):
        equips = data.get('equips')
        aspect = data.get('aspect')
        physique = data.get('physique')
        avatarConfig = data.get('avatarConfig')
        roleName = data.get('roleName', '')
        itemId = data.get('itemId', '')
        hairColor = data.get('hairColor', '')
        uuid = data.get('uuid', '')
        itemPlusInfo = data.get('extra', {})
        avatarConfig = self.adjustAvatarConfig(avatarConfig, hairColor)
        equipment = Equipment()
        if equips:
            for part, value in equips.iteritems():
                equipment[part] = Item(value)

        uiUtils.setItemPlusInfo(equipment, itemPlusInfo)
        aspect = aspect if aspect else Appearance({})
        physique = Physique(physique)
        school = physique.school
        gameglobal.rds.ui.modelRoleInfo.showRoleInfo(None, equipment, school, aspect, physique, avatarConfig, True, roleName, itemId, uuid, stamp)

    def enlarageFittingRoom(self):
        ud = FRUD.data.get((self.myHome.roomId, self.myHome.fittingRoomLv))
        expandCashNeed = ud.get('expandCashNeed', 0)
        expandItemNeed = ud.get('expandItemNeed', [])
        if not ud or not expandCashNeed and not expandItemNeed:
            self.showGameMsg(GMDD.data.ENLARGE_ROOM_FORBIDDEN, ())
            return
        else:
            itemData = {}
            needNum = 0
            count = 0
            if expandItemNeed:
                itemId, needNum = expandItemNeed[0]
                if itemId:
                    itemData = uiUtils.getGfxItemById(itemId)
                    count = self.inv.countItemInPages(itemId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST)
                    itemData['count'] = uiUtils.convertNumStr(count, needNum)
            yesBtnEnable = False
            if self.cash + self.bindCash >= expandCashNeed and itemData and count >= needNum:
                yesBtnEnable = True
            cashStr = uiUtils.convertNumStr(self.cash + self.bindCash, expandCashNeed, showOwnStr=False)
            bonusIcon = {'bonusType': 'bindCash',
             'value': str(cashStr)}
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_IMPHOME_387, self.confirmEnlarageFittingRoom, itemData=itemData, bonusIcon=bonusIcon, yesBtnEnable=yesBtnEnable, style=uiConst.MSG_BOX_BUY_ITEM, noCallback=None)
            return

    def confirmEnlarageFittingRoom(self):
        self.cell.fittingRoomLvUp()

    def spaceInHomeOrLargeRoom(self):
        return formula.spaceInHomeRoom(self.spaceNo) or formula.spaceInHomeEnlargedRoom(self.spaceNo)

    def transferLargeRoomValidArea(self, pos):
        if formula.spaceInHomeEnlargedRoom(self.spaceNo):
            mcd = MCD.data.get(self.mapID, {})
            largeRoomBound = mcd.get('largeRoomBound', [])
            homeRoomFanKadianPos = mcd.get('homeRoomFanKadianPos', [()])
            if largeRoomBound:
                bound0, bound1 = largeRoomBound
                x0, x1 = min(bound0[0], bound1[0]), max(bound0[0], bound1[0])
                z0, z1 = min(bound0[2], bound1[2]), max(bound0[2], bound1[2])
                x, y, z = pos
                if x0 <= x <= x1 and z0 <= z <= z1:
                    return pos
                else:
                    pos = homeRoomFanKadianPos[0]
                    return (pos[0] + 1, pos[1] + 0.5, pos[2])
            else:
                return pos
        return pos

    def inMainRoomValidArea(self, pos):
        mcd = MCD.data.get(self.mapID, {})
        largeRoomBound = mcd.get('largeRoomBound', [])
        if largeRoomBound:
            bound0, bound1 = largeRoomBound
            x0, x1 = min(bound0[0], bound1[0]), max(bound0[0], bound1[0])
            z0, z1 = min(bound0[2], bound1[2]), max(bound0[2], bound1[2])
            x, y, z = pos
            if x0 <= x <= x1 and z0 <= z <= z1:
                return True
            else:
                return False
        return True

    def transferFittingRoomValidArea(self, pos, ownerGbID):
        if formula.spaceInHomeRoom(self.spaceNo):
            fittingRoomBound = MCD.data.get(self.mapID, {}).get('fittingRoomBound', [])
            if fittingRoomBound:
                if self.gbId == ownerGbID and self.myHome.fittingRoomLv:
                    fittingRoomBound = (fittingRoomBound[self.myHome.fittingRoomLv - 1],)
                for bound in fittingRoomBound:
                    bound0, bound1 = bound
                    x0, x1 = min(bound0[0], bound1[0]), max(bound0[0], bound1[0])
                    z0, z1 = min(bound0[2], bound1[2]), max(bound0[2], bound1[2])
                    x, y, z = pos
                    if x0 <= x <= x1 and z0 <= z <= z1 and editorHelper.getFloorHeightMin() - 1 < y < editorHelper.getFloorHeightMax() + 1:
                        return pos
                else:
                    if self.gbId == ownerGbID and self.myHome.fittingRoomLv:
                        ud = FRUD.data.get((self.myHome.roomId, self.myHome.fittingRoomLv), {})
                        entPos = ud.get('entPos', None)
                        if entPos:
                            offsetX = random.uniform(-4, 4)
                            offsetY = random.uniform(-4, 4)
                            return (entPos[0] + offsetX, entPos[1], entPos[2] + offsetY)
                    return pos

            else:
                return pos
        return pos

    def transferHomeRoomValidArea(self, pos):
        if formula.spaceInHomeRoom(self.spaceNo):
            x, y, z = pos
            if y > editorHelper.getFloorHeightMax() + 1 or x < 0 or z < 0:
                mcd = MCD.data.get(self.mapID, {})
                homeRoomFanKadianPos = mcd.get('homeRoomFanKadianPos', [()])
                pos = homeRoomFanKadianPos[0]
                return (pos[0] + 1, pos[1] + 0.5, pos[2])
        return pos

    def _inRangePosArea(self, pos, rangePos):
        if rangePos:
            player = BigWorld.player()
            pPos = player.position
            bound0, bound1 = rangePos
            x0, x1 = min(bound0[0], bound1[0]), max(bound0[0], bound1[0])
            z0, z1 = min(bound0[2], bound1[2]), max(bound0[2], bound1[2])
            x, y, z = pos
            if x0 <= x <= x1 and z0 <= z <= z1 and x0 <= pPos.x <= x1 and z0 <= pPos.z <= z1:
                return True
            else:
                return False
        return True

    def inHomeRoomValidArea(self, pos):
        mcd = MCD.data.get(self.mapID, {})
        largeRoomBound = mcd.get('largeRoomBound', [])
        fittingRoomBound = mcd.get('fittingRoomBound', [])
        if largeRoomBound or fittingRoomBound:
            ret = False
            if largeRoomBound:
                ret = self._inRangePosArea(pos, largeRoomBound)
            if not ret and fittingRoomBound:
                ins = editorHelper.instance()
                if self == BigWorld.player() and self.myHome.fittingRoomLv and self.gbId == ins.ownerGbID:
                    return self._inRangePosArea(pos, fittingRoomBound[self.myHome.fittingRoomLv - 1])
                for bound in fittingRoomBound:
                    if self._inRangePosArea(pos, bound):
                        return True
                else:
                    return False

            return ret
        return True

    def onQueryMyRoomAuth(self, data):
        gamelog.debug('@zs onQueryMyRoomAuth', data)
        gameglobal.rds.ui.homePermission.refreshFrame(data)

    def onQueryReceivedRoomAuth(self, data):
        gamelog.debug('@zs onQueryReceivedRoomAuth', data)
        gameglobal.rds.ui.homeCheckHouses.openPanel(data)

    def giveupRoomAuthSucc(self, gbid):
        if gbid:
            self.base.queryReceivedRoomAuth()

    def visitRoom(self, gbId, roleName = '', hostId = 0):
        if hostId and gbId and hostId != utils.getHostId():
            self.cell.enterCrossHomeRoom(gbId, hostId)
            return
        if gbId:
            gbId = str(gbId)
            if not gbId.startswith('#'):
                gbId = '#' + gbId
        else:
            gbId = '#'
        if self.checkPathfinding():
            self.cancelPathfinding()
        canUse = logicInfo.isUseableGuildMemberSkill(const.GUILD_SKILL_XIAOFEIXIE)
        if canUse:
            if gbId != '#':
                self.cell.useGuildMemberSkillWithParam(const.GUILD_SKILL_XIAOFEIXIE, (gbId,))
            elif roleName:
                self.base.enterRoomDirectlyByName(roleName)
        elif self.canResetCD(const.GUILD_SKILL_XIAOFEIXIE):
            msg = GMD.data.get(GMDD.data.CONFIRM_RESET_TRACK_CD, {}).get('text', gameStrings.TEXT_UIUTILS_914)
            itemFameData = {}
            resetCDItems = SCD.data.get('resetGuildTrackSkillCDItems', ())
            if resetCDItems:
                p = BigWorld.player()
                itemId, needNum = resetCDItems
                item = Item(itemId)
                currentCount = BigWorld.player().inv.countItemInPages(item.getParentId(), enableParentCheck=True)
                itemFameData['itemId'] = itemId
                itemFameData['deltaNum'] = needNum - currentCount
            func = Functor(self.cell.resetGuildSkillCD, const.GUILD_SKILL_XIAOFEIXIE, (gbId, roleName))
            if not gameglobal.rds.ui.messageBox.getCheckOnceData(uiConst.CHECK_ONCE_TYPE_RESET_TRACK_CD):
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, func, isShowCheckBox=True, itemFameData=itemFameData, checkOnceType=uiConst.CHECK_ONCE_TYPE_RESET_TRACK_CD)
            else:
                func()
        else:
            self.showGameMsg(GMDD.data.GUILD_SKILL_TRACK_CD, ())

    def sendRoomPhotoData(self, photoDict):
        pass
