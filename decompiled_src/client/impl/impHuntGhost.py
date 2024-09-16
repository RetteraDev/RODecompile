#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impHuntGhost.o
from gamestrings import gameStrings
import copy
import BigWorld
import gametypes
import gamelog
import gameglobal
import const
from cdata import game_msg_def_data as GMDD
from data import hunt_ghost_area_data as HGAD
from data import hunt_ghost_config_data as HGCD

class ImpHuntGhost(object):

    def onSyncHuntGhostAreaStart(self, areaIdList, needBroad):
        gamelog.info('@zmm onSyncHuntGhostAreaStart areaIdList, needBroad:', areaIdList, needBroad)
        if needBroad:
            gameglobal.rds.ui.huntGhost.showPicTips(True)
            areaText = self.getAreaText(areaIdList)
            self.showGameMsg(GMDD.data.SHOW_HUNT_GHOST_AREA, areaText)
        gameglobal.rds.ui.huntGhost.onStartActivity(areaIdList)

    def getAreaText(self, areaIdList):
        areaText = ''
        for areaId in areaIdList:
            areaName = HGAD.data.get(areaId, {}).get('name', '')
            if areaText == '':
                areaText += areaName
            else:
                areaText += ', ' + areaName

        return areaText

    def onSyncHuntGhostAreaStop(self):
        gamelog.info('@zmm onSyncHuntGhostAreaStop')
        gameglobal.rds.ui.huntGhost.onStopActivity()

    def onSyncAreaGhostSpawnPoint(self, areaId, ghostPoint, broadcastType):
        gamelog.info('@zmm onSyncAreaGhostSpawnPoint areaId, ghostPoint, broadcastType', areaId, ghostPoint, broadcastType)
        if broadcastType == const.HUNT_GHOST_POINT_BROAD_BY_TURN_ON:
            gameglobal.rds.ui.huntGhost.onGetGhostPos(areaId, ghostPoint)
        elif broadcastType == const.HUNT_GHOST_POINT_BROAD_BY_TURN_OFF:
            gameglobal.rds.ui.huntGhost.onCancelGhost()

    def onExploreGhostToGenBox(self, treasureBoxType, treasureBoxId):
        """
        #\xe6\x8e\xa2\xe9\xad\x82\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe7\x94\x9f\xe6\x88\x90\xe5\xae\x9d\xe7\xae\xb1
        :param treasureBoxType: =1 \xe8\xa1\xa8\xe7\xa4\xba\xe5\xa4\xa7\xe5\xae\x9d\xe7\xae\xb1\xef\xbc\x8c =2 \xe8\xa1\xa8\xe7\xa4\xba\xe5\xb0\x8f\xe5\xae\x9d\xe7\xae\xb1
        :param treasureBoxId:
        :return:
        """
        gamelog.info('@zmm onExploreGhostToGenBox treasureBoxType, treasureBoxId', treasureBoxType, treasureBoxId)
        if treasureBoxId:
            gameglobal.rds.ui.huntGhost.onExploreGhostToGenBox()
        gameglobal.rds.ui.huntGhost.setGhostType(treasureBoxType)
        if treasureBoxType == 1:
            gameglobal.rds.ui.huntGhost.onBigGhostAppear(treasureBoxId)
        else:
            gameglobal.rds.ui.huntGhost.onGhostAppear(treasureBoxId)

    def huntGhostFlagCreateOk(self):
        """
        \xe9\x98\x9f\xe4\xbc\x8d\xe9\xac\xbc\xe7\x82\xb9\xe6\xa0\x87\xe8\xae\xb0\xe5\x88\x9b\xe5\xbb\xba\xe6\x88\x90\xe5\x8a\x9f
        :return:
        """
        gameglobal.rds.ui.huntGhost.onHuntGhostFlagCreateOk()
        gamelog.info('@zmm huntGhostFlagCreateOk')

    def createAllResetHuntGhostTreasureBoxBig(self, bigBoxEntBornList, bigBoxCount, bigBoxInfo):
        """
        \xe5\x85\xa8\xe6\x9c\x8d\xe5\x89\xa9\xe4\xbd\x99\xe5\xa4\xa7\xe5\xae\x9d\xe7\xae\xb1\xe5\x85\xa8\xe9\x83\xa8\xe5\x88\xb7\xe5\x87\xba\xe6\x8e\xa5\xe5\x8f\xa3
        :param bigBoxEntBornList: [(boxEntId, bornTime),(boxEntId, bornTime),(boxEntId, bornTime),(boxEntId, bornTime),(boxEntId, bornTime),...]
        :param bigBoxCount: \xe5\x89\xa9\xe4\xbd\x99\xe5\xa4\xa7\xe5\xae\x9d\xe7\xae\xb1\xe7\x9a\x84\xe6\x80\xbb\xe4\xb8\xaa\xe6\x95\xb0
        :param bigBoxInfo: \xe5\xa4\xa7\xe5\xae\x9d\xe7\xae\xb1\xe7\x9a\x84\xe6\x95\xb0\xe6\x8d\xae
        :return:
        """
        if bigBoxEntBornList and len(bigBoxEntBornList) >= 1:
            boxEntId, _ = bigBoxEntBornList[0]
            gameglobal.rds.ui.huntGhost.onBigGhostAppear(boxEntId)
        if self.spaceNo == const.SPACE_NO_BIG_WORLD:
            self.showGameMsg(GMDD.data.CREATE_HUNT_GHOST_BIG_BOX, ())
        gameglobal.rds.ui.huntGhost.onGetBigBoxLeftCount(bigBoxCount, bigBoxInfo)
        gamelog.debug('@zmm createAllResetHuntGhostTreasureBoxBig bigBoxEntBornList, bigBoxCount, bigBoxInfo', bigBoxEntBornList, bigBoxCount, bigBoxInfo)

    def createHuntGhostTreasureBoxBig(self, boxEntId, bornTime, bigBoxCount, bigBoxInfo):
        """
        \xe5\xb9\xbf\xe6\x92\xad\xe5\x85\xa8\xe6\x9c\x8d\xe4\xb8\x80\xe4\xb8\xaa\xe5\xa4\xa7\xe5\xae\x9d\xe7\xae\xb1\xe8\xaf\x9e\xe7\x94\x9f
        :param boxEntId: \xe5\xae\x9d\xe7\xae\xb1entity ID
        :param bornTime: \xe5\xae\x9d\xe7\xae\xb1\xe8\xaf\x9e\xe7\x94\x9f\xe6\x97\xb6\xe9\x97\xb4\xef\xbc\x882\xe5\x88\x86\xe9\x92\x9f\xe5\x86\x85\xe4\xb8\x8d\xe5\x85\x81\xe8\xae\xb8\xe7\x82\xb9\xe5\x87\xbb\xe5\xae\x9d\xe7\xae\xb1\xef\xbc\x89
        :param bigBoxCount: \xe5\x89\xa9\xe4\xbd\x99\xe5\xa4\xa7\xe5\xae\x9d\xe7\xae\xb1\xe7\x9a\x84\xe6\x80\xbb\xe4\xb8\xaa\xe6\x95\xb0
        :param bigBoxCount: \xe5\xa4\xa7\xe5\xae\x9d\xe7\xae\xb1\xe7\x9a\x84\xe6\x95\xb0\xe6\x8d\xae
        :return:
        """
        gameglobal.rds.ui.huntGhost.onBigGhostAppear(boxEntId)
        if self.spaceNo == const.SPACE_NO_BIG_WORLD:
            self.showGameMsg(GMDD.data.CREATE_HUNT_GHOST_BIG_BOX, ())
        gameglobal.rds.ui.huntGhost.onGetBigBoxLeftCount(bigBoxCount, bigBoxInfo)
        gamelog.debug('@zmm createHuntGhostTreasureBoxBig boxEntId, bornTime, bigBoxCount, bigBoxInfo', boxEntId, bornTime, bigBoxCount, bigBoxInfo)

    def onGetBigBoxLeftCount(self, bigBoxCount, bigBoxInfo):
        """
        \xe5\x90\x8c\xe6\xad\xa5\xe5\xbd\x93\xe5\x89\x8d\xe6\x9c\x8d\xe5\x89\xa9\xe4\xbd\x99\xe5\xa4\xa7\xe5\xae\x9d\xe7\xae\xb1\xe7\x9a\x84\xe6\x80\xbb\xe4\xb8\xaa\xe6\x95\xb0
        :param bigBoxCount: \xe5\x89\xa9\xe4\xbd\x99\xe5\xa4\xa7\xe5\xae\x9d\xe7\xae\xb1\xe7\x9a\x84\xe6\x80\xbb\xe4\xb8\xaa\xe6\x95\xb0
        :param bigBoxCount: \xe5\xa4\xa7\xe5\xae\x9d\xe7\xae\xb1\xe7\x9a\x84\xe6\x95\xb0\xe6\x8d\xae
        :return:
        """
        gamelog.info(gameStrings.TEXT_IMPHUNTGHOST_144, bigBoxCount, bigBoxInfo)
        gameglobal.rds.ui.huntGhost.onGetBigBoxLeftCount(bigBoxCount, bigBoxInfo)

    def onFindGhostTreasureBox(self, areaId, ghostPoint, treasureBoxId, treasureBoxType):
        gamelog.info('@zmm onFindGhostTreasureBox areaId, ghostPoint, treasureBoxType, treasureBoxId:', areaId, ghostPoint, treasureBoxType, treasureBoxId)
        gameglobal.rds.ui.huntGhost.onFindGhostTreasureBox(areaId, ghostPoint, treasureBoxType)
