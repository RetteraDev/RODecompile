#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impJunJie.o
import cPickle
import zlib
import gameglobal
import gametypes
import gamelog
import utils
import time
from guis import uiConst
from data import famous_general_config_data as FGCD
from cdata import game_msg_def_data as GMDD

class ImpJunJie(object):

    def onQueryLastSeasonsBakInfo(self, info):
        info = cPickle.loads(zlib.decompress(info))
        gamelog.debug('@hjx famous general#onQueryLastSeasonsBakInfo:', info)
        gameglobal.rds.ui.famousRankList.refreshMostFamousRankInfo(info)

    def onQueryFullJunjieCnt(self, fullJunjieCnt):
        gamelog.debug('@hjx famous general#onQueryFullJunjieCnt:', fullJunjieCnt)
        gameglobal.rds.ui.roleInformationJunjie.maxLvNum = fullJunjieCnt
        gameglobal.rds.ui.roleInformationJunjie.initNextJunjieInfoMax()

    def onQueryFamousGeneralSeasonStage(self, stage, seasonCnt):
        gamelog.debug('@hjx famous general#onQueryFamousGeneralSeasonStage:', stage, seasonCnt)
        gameglobal.rds.ui.roleInformationJunjie.stage = stage
        gameglobal.rds.ui.roleInformationJunjie.famousSeasonNum = seasonCnt
        gameglobal.rds.ui.roleInformationJunjie.initSeasonTime()
        if gameglobal.rds.ui.roleInformationJunjie.isReadyForFamous():
            gameglobal.rds.ui.roleInformationJunjie.initNextJunjieInfoMax()

    def applyFamousRecordRewardSucc(self):
        self.cell.queryFamousRecordInfo()

    def onNotifyFamousGeneralRatioChange(self, ratio):
        """
        \xe9\x80\x9a\xe7\x9f\xa5\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe5\xa8\x81\xe6\x9c\x9b\xe5\x80\xbc\xe7\x9a\x84\xe6\xaf\x94\xe4\xbe\x8b\xe6\x94\xb9\xe5\x8f\x98\xe4\xba\x86
        Returns:
        
        """
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_FAMOUS_GET_UP)
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_FAMOUS_GET_UP, {'click': self.onClickFamousGetUpMsg})

    def onClickFamousGetUpMsg(self):
        self.showGameMsg(GMDD.data.FAMOUS_GET_UP_TIP, ())
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_FAMOUS_GET_UP)

    def onQueryFamousRecordInfo(self, recordInfo):
        """
        
        Args:
            recordInfo: {'currentRound' : \xe5\xbd\x93\xe5\x89\x8d\xe8\xbd\xae\xe6\x95\xb0, 'canApplyRewardList' : [\xe5\x8f\xaf\xe9\xa2\x86\xe5\xa5\x96\xe7\x9a\x84\xe8\xbd\xae\xe6\x95\xb0],
             'currentWeek': \xe5\xbd\x93\xe5\x89\x8d\xe7\x9a\x84\xe5\x91\xa8\xe6\x95\xb0(\xe6\xb3\xa8\xe6\x84\x8f:\xe5\xbd\x93\xe4\xb8\xba-1\xe6\x97\xb6\xef\xbc\x8c\xe8\xa1\xa8\xe7\xa4\xba\xe6\x8f\x90\xe5\x89\x8d\xe7\xbb\x93\xe6\x9d\x9f\xef\xbc\x8c\xe8\xbf\x99\xe5\x91\xa8\xe7\x9a\x84\xe5\x89\xa9\xe4\xbd\x99\xe5\xa4\xa9\xe6\x95\xb0\xe4\xb9\x9f\xe8\xa6\x81\xe5\x8a\xa0\xe4\xb8\x8a)}
        
        Returns:
        
        """
        gameglobal.rds.ui.famousRecord.recordInfo = recordInfo
        gameglobal.rds.ui.famousRecord.show()
