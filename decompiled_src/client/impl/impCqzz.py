#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impCqzz.o
import BigWorld
import gamelog
import gameglobal
from callbackHelper import Functor

class ImpCqzz(object):
    """\xe8\x8b\x8d\xe7\xa9\xb9\xe4\xb9\x8b\xe5\xb8\x9c\xe6\x88\x98\xe5\x9c\xba"""

    def onUpdateCqzzFlagCnt(self, camp, cnt):
        """\xe6\x9b\xb4\xe6\x96\xb0\xe9\x98\xb5\xe8\x90\xa5\xe7\x9a\x84\xe6\x97\x97\xe5\xb8\x9c\xe6\x95\xb0\xe9\x87\x8f"""
        gamelog.debug('@zhangkuo onUpdateCqzzFlagCnt', camp, cnt)
        gameglobal.rds.ui.battleCQZZProgressBar.onGetFlagInfo(camp, cnt)

    def clearCqzzFlagHolder(self, camp, gbID):
        """\xe6\xb8\x85\xe9\x99\xa4\xe6\x97\x97\xe6\x89\x8b\xe4\xbf\xa1\xe6\x81\xaf"""
        gamelog.debug('@zhangkuo clearCqzzFlagHolder', camp, gbID)
        gameglobal.rds.ui.battleCQZZProgressBar.resetFlagerInfo(camp, gbID)

    def setCqzzFlagHolder(self, gbID, camp, photo, roleName, hp, mhp, sex, school, hostID):
        """\xe8\xae\xbe\xe7\xbd\xae\xe6\x97\x97\xe6\x89\x8b\xe4\xbf\xa1\xe6\x81\xaf"""
        gamelog.debug('@zhangkuo setCqzzFlagHolder', gbID, camp, photo, roleName, hp, mhp, sex, school, hostID)
        flagerInfo = {'gbId': gbID,
         'camp': camp,
         'photo': photo,
         'name': roleName,
         'hp': hp,
         'mhp': mhp,
         'sex': sex,
         'school': school,
         'hostID': hostID}
        gameglobal.rds.ui.battleCQZZProgressBar.onSetFlagerInfo(camp, gbID, flagerInfo)

    def onUpdateCqzzFlagHolder(self, camp, gbID, hp, pos, flagID):
        """\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\x97\xe6\x89\x8b\xef\xbc\x88\xe6\x97\x97\xe5\xb8\x9c\xef\xbc\x89\xe7\x9a\x84\xe4\xbd\x8d\xe7\xbd\xae\xef\xbc\x8c\xe8\xa1\x80\xe9\x87\x8f"""
        gamelog.debug('@zhangkuo onUpdateCqzzFlagHolder', camp, gbID, hp, pos)
        flagCamp = 1 if camp == 2 else 2
        self.onUpdateCqzzFlagPos(flagID, flagCamp, pos)
        updateInfo = {'camp': camp,
         'gbId': gbID,
         'hp': hp,
         'pos': pos}
        gameglobal.rds.ui.battleCQZZProgressBar.onRefreshFlagerInfo(gbID, updateInfo)

    def onCqzzFlagPicked(self, gbID, camp, flagID):
        """\xe6\x97\x97\xe5\xb8\x9c\xe8\xa2\xab\xe6\x8b\xbe\xe5\x8f\x96(\xe8\xbf\x99\xe9\x87\x8c\xe6\x98\xaf\xe6\x8c\x87\xe7\x9a\x84\xe6\x8a\xa2\xe6\x97\x97\xe5\xad\x90\xe7\x9a\x84\xe6\x8b\xbe\xe5\x8f\x96)"""
        gamelog.debug('@zhangkuo onCqzzFlagPicked', gbID, camp, flagID)

    def onCqzzFlagFallDown(self, gbID, camp, flagID, position):
        """\xe6\x97\x97\xe5\xb8\x9c\xe8\xa2\xab\xe6\x89\x93\xe6\x8e\x89"""
        gamelog.debug('@zhangkuo onCqzzFlagFallDown', gbID, camp, flagID, position)
        flagCamp = 1 if camp == 2 else 2
        self.onUpdateCqzzFlagPos(flagID, flagCamp, position)

    def onCqzzFlagCommited(self, gbID, camp, flagID):
        """\xe6\x97\x97\xe5\xb8\x9c\xe8\xa2\xab\xe6\x8f\x90\xe4\xba\xa4"""
        gamelog.debug('@zhangkuo onCqzzFlagCommited', gbID, camp, flagID)
        flagCamp = 1 if camp == 2 else 2
        BigWorld.callback(1.5, Functor(self.setInitCqzzFlagCallBack, flagCamp))

    def setInitCqzzFlagCallBack(self, flagCamp):
        gameglobal.rds.ui.littleMap.setInitCqzzFlag(flagCamp)

    def syncCqzzDonatePoint(self, point, rank):
        """
        \xe5\x90\x8c\xe6\xad\xa5\xe4\xb8\xaa\xe4\xba\xba\xe8\xb4\xa1\xe7\x8c\xae\xe5\x92\x8c\xe6\x8e\x92\xe5\x90\x8d\xe4\xbf\xa1\xe6\x81\xaf
        :param point: \xe4\xb8\xaa\xe4\xba\xba\xe8\xb4\xa1\xe7\x8c\xae\xe5\x80\xbc
        :param rank: \xe8\xb4\xa1\xe7\x8c\xae\xe6\x8e\x92\xe5\x90\x8d
        """
        gamelog.debug('@zhangkuo syncCqzzDonatePoint [point][rank]', point, rank)

    def onUpdateCqzzFlagPos(self, flagID, camp, pos):
        """\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\x97\xe5\xb8\x9c\xe4\xbd\x8d\xe7\xbd\xae"""
        gamelog.debug('@zhangkuo onUpdateCqzzFlagPos', flagID, camp, pos)
        if not hasattr(self, 'cqzzFlagPosGetState'):
            self.cqzzFlagPosGetState = {}
        self.cqzzFlagPosGetState[camp] = pos
        gameglobal.rds.ui.littleMap.addBattleCqzzFlagIcon(pos, camp, 1)

    def onCqzzFlagPutBack(self, camp, flagID):
        """
        \xe6\x97\x97\xe5\xb8\x9c\xe8\xa2\xab\xe8\xbf\x94\xe5\x9b\x9e\xe5\x8e\x9f\xe5\x9c\xb0
        :param camp: \xe6\x97\x97\xe5\xb8\x9c\xe9\x98\xb5\xe8\x90\xa5
        :param flagID: \xe6\x97\x97\xe5\xb8\x9cID
        """
        gamelog.debug('@zhangkuo onCqzzFlagPutBack', camp, flagID)
        flagCamp = camp
        BigWorld.callback(1.5, Functor(self.setInitCqzzFlagCallBack, flagCamp))
