#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impDoublePlantTree.o
import BigWorld
import gameglobal
import utils
import const
import gamelog
from guis import events
from callbackHelper import Functor
from gamestrings import gameStrings
from guis import uiUtils
from helpers import navigator
from cdata import double_plant_tree_config_data as DPTCD
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD

class ImpDoublePlantTree(object):

    def onStealFruit(self, data):
        pass

    def onWateringPlant(self, data):
        pass

    def onHarvestFruit(self, data):
        pass

    def onSendTreeInfo(self, data):
        pass

    def isInDoublePlantTree(self, showErrMsg = False):
        p = BigWorld.player()
        if not gameglobal.rds.configData.get('enableDoublePlantTree', False):
            return False
        elif p.spaceNo != const.SPACE_NO_BIG_WORLD:
            showErrMsg and p.showGameMsg(GMDD.data.VT_PLANT_NOT_IN_BIG_WORLD, ())
            return False
        else:
            startTime = DPTCD.data.get('startTime', '')
            endTIme = DPTCD.data.get('endTime', '')
            if startTime and endTIme and utils.inCrontabRange(startTime, endTIme):
                return True
            showErrMsg and p.showGameMsg(GMDD.data.VT_ACTIVITY_END, ())
            return False

    def getDoublePlantTreeAreaBounds(self):
        areaBoundList = DPTCD.data.get('areaBoundList', '')
        return areaBoundList

    def doublePlantTreeReq(self, treeEntId):
        p = BigWorld.player()
        if not p.isInDoublePlantTree(showErrMsg=True):
            return
        if not BigWorld.entities.get(treeEntId):
            return
        if not hasattr(p, 'valentineInfo'):
            return
        if p.valentineInfo.treeEntityId == treeEntId:
            if p.valentineInfo.fruitNum > 0:
                if not p.valentineInfo.canHarvest:
                    p.showGameMsg(GMDD.data.VT_ACTIVITY_HARVEST_ALREADY, ())
                    return
                msg = DPTCD.data.get('canHarvestTxt', '')
                if msg and not p.checkMsgOpeningByType('harvestMsgBox'):
                    msg = msg % (p.valentineInfo.fruitNum, DPTCD.data.get('fruitAll', ''), self.getLeftStopHarvestTimeStr(p.valentineInfo.createTime))
                    p.doublePTMsgBoxIdDict['harvestMsgBox'] = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(p.harvestFruitReq, treeEntId), yesBtnText=DPTCD.data.get('canHarvestBtnTxt', gameStrings.CONFIRM), itemData=uiUtils.getGfxItemById(DPTCD.data.get('fruitId', 0)))
            elif p.valentineInfo.canWatering:
                msg = DPTCD.data.get('waterFruitTxt', '')
                if msg and not p.checkMsgOpeningByType('waterMsgBox'):
                    msg = msg % self.getLeftHarvestTimeStr(p.valentineInfo.createTime)
                    p.doublePTMsgBoxIdDict['waterMsgBox'] = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(p.wateringPlantReq, treeEntId), yesBtnText=DPTCD.data.get('waterBtnTxt', gameStrings.CONFIRM))
            else:
                msg = DPTCD.data.get('waitForHarvestingTxt', '')
                if msg and not p.checkMsgOpeningByType('waitForHarvestMsgBox'):
                    msg = msg % self.getLeftHarvestTimeStr(p.valentineInfo.createTime)
                    p.doublePTMsgBoxIdDict['waitForHarvestMsgBox'] = gameglobal.rds.ui.messageBox.showAlertBox(msg)
        else:
            if p.checkMsgOpeningByType('stealMsgBox'):
                p.closeMsgByType('stealMsgBox')
            treeEnt = BigWorld.entity(treeEntId)
            if not treeEnt:
                return
            if treeEnt.isMature:
                treeFruitCount = getattr(treeEnt, 'fruitNum', DPTCD.data.get('fruitLimit', 0))
                if treeFruitCount <= DPTCD.data.get('fruitLimit', 16):
                    p.showGameMsg(GMDD.data.VT_STEAL_INVALID_TREE, ())
                else:
                    canStealFruitCount = min(DPTCD.data.get('stealCountPer', 2), treeFruitCount - DPTCD.data.get('fruitLimit', 16))
                    msg = DPTCD.data.get('stealHarvestTxt', '')
                    if msg:
                        msg = msg % canStealFruitCount
                        p.doublePTMsgBoxIdDict['stealMsgBox'] = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(p.stealFruitReq, treeEntId), yesBtnText=DPTCD.data.get('stealHarvestBtnTxt', gameStrings.CONFIRM), itemData=uiUtils.getGfxItemById(DPTCD.data.get('fruitId', 0)))
            else:
                p.showGameMsg(GMDD.data.VT_ACTIVITY_OTHER_TREE_NOT_HARVEST_NOT_STEAL, ())

    def getLeftHarvestTimeStr(self, startPlantTimeStamp):
        harvestTimeOffset = DPTCD.data.get('harvestTime', 7200)
        startHarvestTimeStamp = startPlantTimeStamp + harvestTimeOffset
        nowTimeStamp = utils.getNow(True)
        if startHarvestTimeStamp > nowTimeStamp:
            leftTimeOffset = startHarvestTimeStamp - nowTimeStamp
        else:
            leftTimeOffset = 0
        return utils.formatTimeStr(leftTimeOffset, 'h:m:s', zeroShow=True, sNum=2, mNum=2, hNum=2)

    def getLeftStopHarvestTimeStr(self, startPlantTimeStamp):
        destroyTimeOffset = DPTCD.data.get('destroyTime', 14400)
        startDestroyTimeStamp = startPlantTimeStamp + destroyTimeOffset
        nowTimeStamp = utils.getNow(True)
        if startDestroyTimeStamp > nowTimeStamp:
            leftTimeOffset = startDestroyTimeStamp - nowTimeStamp
        else:
            leftTimeOffset = 0
        return utils.formatTimeStr(leftTimeOffset, 'h:m:s', zeroShow=True, sNum=2, mNum=2, hNum=2)

    def plantTreeReq(self, useItemCB):
        p = BigWorld.player()
        if not p.isInDoublePlantTree(showErrMsg=True):
            return
        gamelog.info('@zmk plantTreeReq - useItemCB:', useItemCB)
        if useItemCB:
            msg = DPTCD.data.get('plantTreeTxt', '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=useItemCB)

    def stealFruitReq(self, npcEntId):
        gamelog.info('@zmk stealFruitReq - npcEntId:', npcEntId)
        p = BigWorld.player()
        p.cell.stealFruit(npcEntId)

    def harvestFruitReq(self, npcEntId):
        gamelog.info('@zmk harvestFruitReq - npcEntId:', npcEntId)
        p = BigWorld.player()
        p.cell.harvestFruit(npcEntId)

    def wateringPlantReq(self, npcEntId):
        gamelog.info('@zmk wateringPlantReq - npcEntId:', npcEntId)
        p = BigWorld.player()
        p.cell.wateringPlant(npcEntId)

    def checkMsgOpeningByType(self, typeString):
        p = BigWorld.player()
        if not hasattr(self, 'doublePTMsgBoxIdDict'):
            self.doublePTMsgBoxIdDict = dict()
        loadedMsgBoxIdList = gameglobal.rds.ui.messageBox.loadeds.keys()
        if p.doublePTMsgBoxIdDict.get(typeString, 0) in loadedMsgBoxIdList:
            return True
        return False

    def closeMsgByType(self, typeString):
        p = BigWorld.player()
        if not hasattr(self, 'doublePTMsgBoxIdDict'):
            self.doublePTMsgBoxIdDict = dict()
        msgBoxId = p.doublePTMsgBoxIdDict.get(typeString, 0)
        loadedMsgBoxIdList = gameglobal.rds.ui.messageBox.loadeds.keys()
        if msgBoxId in loadedMsgBoxIdList:
            gameglobal.rds.ui.messageBox.dismiss(msgBoxId=msgBoxId, needDissMissCallBack=False)

    def seekToDPTree(self):
        p = BigWorld.player()
        if not p.isInDoublePlantTree(showErrMsg=True):
            return
        if not hasattr(p, 'valentineInfo'):
            return
        treePos = p.valentineInfo.treePos
        if treePos and treePos != (0, 0, 0):
            navigator.getNav().pathFinding((float(treePos[0]),
             float(treePos[1]),
             float(treePos[2]),
             float(const.SPACE_NO_BIG_WORLD)))
        else:
            p.showGameMsg(GMDD.data.VT_PLANT_NOT_NAVIGATE_TO_NONE, ())
