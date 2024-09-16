#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impClanWarCourier.o
import BigWorld
import gameconfigCommon
import gamelog
import gameglobal
import const
import utils
import gametypes
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from data import clan_courier_config_data as CCCD

class ImpClanWarCourier(object):
    """\xe9\xa2\x86\xe5\x9c\xb0\xe6\x88\x98\xe6\x8a\xbc\xe9\x95\x96"""

    def notifyEnterJCT(self, courierGuildNUID, guildName, occupyName):
        """\xe9\x80\x9a\xe7\x9f\xa5\xe9\x9d\x9e\xe5\x8d\xa0\xe9\xa2\x86\xe5\x85\xac\xe4\xbc\x9a\xe6\x88\x90\xe5\x91\x98\xe8\xbf\x9b\xe5\x85\xa5\xe4\xb9\x9d\xe9\x87\x8d\xe5\xa4\xa9"""
        if self.guildNUID == courierGuildNUID:
            return
        if not BigWorld.player().spaceNo == const.SPACE_NO_BIG_WORLD:
            return
        gamelog.debug('@zhangkuo notifyEnterJCT', courierGuildNUID, guildName, occupyName)
        reqLvJCT = CCCD.data.get('reqLvJCT', 40)
        if self.lv < reqLvJCT:
            return
        gameglobal.rds.ui.clanWarYaBiao.showJoinClanWarHuntConfirm()

    def testOnEnterCourierJct(self):
        courierList = []
        for i in [0, 2]:
            dic = {}
            dic['courierID'] = i + 1
            dic['mhp'] = self.mhp * (i + 1)
            dic['hp'] = self.hp
            dic['pos'] = self.position
            dic['res'] = 100
            dic['tStartMove'] = utils.getNow()
            dic['state'] = gametypes.CLAN_COURIER_NORMAL
            courierList.append(dic)

        self.onCourierCreate(courierList)

    def onEnterCourierJct(self, courierList):
        """
        \xe5\x8a\xa0\xe5\x85\xa5\xe4\xb9\x9d\xe9\x87\x8d\xe5\xa4\xa9
        :param courierList: [{'courierID':courierID, 'mhp':mhp, 'hp': hp, , 'pos': pos, 'res': res, 'tStartMove':int,'state':int}]
        :return:
        """
        gamelog.debug('@zhangkuo onEnterCourierJct', courierList)
        self.clanCourierDic = {d['courierID']:d for d in courierList}
        for value in self.clanCourierDic.itervalues():
            value['isEnd'] = value.get('state', 0) in (gametypes.CLAN_COURIER_DEAD, gametypes.CLAN_COURIER_COMMITED)

        gameglobal.rds.ui.clanWarYaBiao.showJoindClanWarHunt()
        gameglobal.rds.ui.clanWarYaBiao.show()

    def onCourierCreate(self, data):
        """
        \xe5\x88\x9b\xe5\xbb\xba\xe9\x95\x96\xe8\xbd\xa6
        :param data: [{'courierID':courierID, 'mhp':mhp, 'hp': hp, , 'pos': pos, 'res': res}]
        :return:
        """
        gamelog.debug('@zhangkuo onCourierCreate', data)
        if not hasattr(self, 'clanCourierDic'):
            self.clanCourierDic = {}
        self.clanCourierDic.update({d['courierID']:d for d in data})
        if self.isClanCourierAvatar():
            gameglobal.rds.ui.clanWarYaBiao.show()

    def onCourierStart(self, guildNUID, tStartMove):
        """\xe9\x95\x96\xe8\xbd\xa6\xe5\x87\xba\xe5\x8f\x91"""
        for value in self.clanCourierDic.itervalues():
            value['tStartMove'] = tStartMove

        gamelog.debug('@zhangkuo onCourierStart', guildNUID, tStartMove)

    def getClanWarCourierStartTime(self):
        for value in self.clanCourierDic.itervalues():
            if value.get('tStartMove', 0):
                return value['tStartMove']

        return 0

    def onCourierCommit(self, courierID):
        """\xe4\xb8\x8a\xe4\xba\xa4\xe9\x95\x96\xe8\xbd\xa6"""
        gamelog.debug('@zhangkuo onCourierCommit', courierID)
        self.clanCourierDic.setdefault(courierID, {})['isEnd'] = True
        self.clanCourierDic.setdefault(courierID, {})['diedTime'] = utils.getNow()
        self.showGameMsg(GMDD.data.COMMIT_CLAN_COURIER_GUILD, ())

    def onCourierDead(self, courierID, diedTime):
        """\xe9\x95\x96\xe8\xbd\xa6\xe8\xa2\xab\xe5\x87\xbb\xe6\x9d\x80"""
        self.clanCourierDic.setdefault(courierID, {})['isEnd'] = True
        self.clanCourierDic[courierID]['state'] = gametypes.CLAN_COURIER_DEAD
        self.clanCourierDic[courierID]['diedTime'] = diedTime
        gamelog.debug('@zhangkuo onCourierDead', courierID, diedTime)

    def onCourierTimeout(self, courierID):
        """\xe9\x95\x96\xe8\xbd\xa6\xe8\xb6\x85\xe6\x97\xb6\xe5\xbc\xba\xe5\x88\xb6\xe7\xbb\x93\xe6\x9d\x9f"""
        self.clanCourierDic.setdefault(courierID, {})['isEnd'] = True
        self.clanCourierDic.setdefault(courierID, {})['diedTime'] = utils.getNow()
        gamelog.debug('@zhangkuo onCourierTimeout', courierID)

    def onPushCourierHp(self, courierID, hp, mhp):
        """\xe9\x95\x96\xe8\xbd\xa6\xe8\xa1\x80\xe9\x87\x8f\xe5\x90\x8c\xe6\xad\xa5"""
        if self.clanCourierDic.has_key(courierID):
            self.clanCourierDic[courierID]['hp'] = hp
            if mhp:
                self.clanCourierDic[courierID]['mhp'] = mhp
        gamelog.debug('@zhangkuo onPushCourierHp', courierID, hp, mhp)
        if hp == 0:
            self.onPushCourierRes(courierID, 0)

    def onPushCourierPos(self, courierID, pos):
        """\xe9\x95\x96\xe8\xbd\xa6\xe4\xbd\x8d\xe7\xbd\xae"""
        if self.clanCourierDic.has_key(courierID):
            self.clanCourierDic[courierID]['pos'] = pos
        gameglobal.rds.ui.map.addClanWarYaBiao()
        gameglobal.rds.ui.littleMap.addClanWarYaBiao()
        gamelog.debug('@zhangkuo onPushCourierPos', courierID, pos)

    def onPushCourierRes(self, courierID, res):
        """\xe9\x95\x96\xe8\xbd\xa6\xe8\xb5\x84\xe6\xba\x90"""
        gamelog.debug('@zhangkuo onPushCourierRes', courierID, res)
        if self.clanCourierDic.has_key(courierID):
            self.clanCourierDic[courierID]['res'] = res

    def testOnPushCourierTopMember(self):
        memberList = []
        for i in xrange(3):
            info = (i + 1,
             i + 2,
             i + 3,
             i + 10,
             'name',
             0)
            memberList.append(info)

        self.onPushCourierTopMember(memberList)

    def onPushCourierTopMember(self, member):
        """top\xe6\x88\x90\xe5\x91\x98\xe8\xb4\xa1\xe7\x8c\xae\xe4\xbf\xa1\xe6\x81\xaf\xe5\x90\x8c\xe6\xad\xa5"""
        self.clanCourierTopMember = member
        gamelog.debug('@zhangkuo onPushCourierTopMember', member)

    def onPushCourierDonate(self, donate):
        """\xe8\xb4\xa1\xe7\x8c\xae\xe5\x88\x86"""
        gamelog.debug('@zhangkuo onPushCourierDonate', donate)
        self.courierDonate = donate

    def inClanCourier(self):
        """\xe5\xbd\x93\xe5\x89\x8d\xe6\x98\xaf\xe5\x90\xa6\xe5\xa4\x84\xe4\xba\x8e\xe9\xa2\x86\xe5\x9c\xb0\xe6\x88\x98\xe6\x8a\xbc\xe9\x95\x96\xe6\x9c\x9f\xe9\x97\xb4"""
        if not gameglobal.rds.configData.get('enableClanWarCourier', False):
            return False
        if self.courierGuildNUID == 0:
            return False
        return self.spaceNo == const.SPACE_NO_BIG_WORLD

    def isClanCourierAvatar(self):
        """\xe6\x98\xaf\xe5\x90\xa6\xe6\x98\xaf\xe6\x8a\xbc\xe9\x95\x96\xe4\xb8\xad\xe7\x9a\x84\xe5\x8d\xa0\xe9\xa2\x86\xe5\x85\xac\xe4\xbc\x9a\xe6\x88\x90\xe5\x91\x98"""
        if self.courierGuildNUID == 0:
            return False
        return self.courierGuildNUID == self.guildNUID

    def notifyCourierJctExit(self):
        """\xe9\x80\x9a\xe7\x9f\xa5\xe4\xb9\x9d\xe9\x87\x8d\xe5\xa4\xa9\xe7\x8e\xa9\xe5\xae\xb6\xe9\x80\x80\xe5\x87\xba\xe4\xb9\x9d\xe9\x87\x8d\xe5\xa4\xa9"""
        gamelog.debug('@zhangkuo notifyCourierJctExit')
        gameglobal.rds.ui.clanWarYaBiao.handleExitBtnClick()

    def getJCTRoleName(self):
        if not getattr(self, 'jctSeq', ''):
            return self.roleName
        else:
            return CCCD.data.get('roleName', 'prefix%d') % self.jctSeq

    def changeClanWarHunt(self, isJoin = True):
        if self.topLogo:
            self.topLogo.updateRoleName(self.topLogo.name)
            self.topLogo.setAvatarTitle('', 1)
            self.topLogo.removeGuildIcon()
            self.topLogo.addGuildIcon(self.guildFlag)
            self.topLogo.hideTitleEffect(True)
        if self == BigWorld.player():
            if isJoin:
                gameglobal.rds.ui.clanWarYaBiao.show()
            else:
                gameglobal.rds.ui.clanWarYaBiao.hide()

    def set_courierGuildNUID(self, old):
        if self.id != BigWorld.player().id:
            return
        if gameconfigCommon.enableClanWarCourier() and BigWorld.player().inClanCourier():
            if self.isClanCourierAvatar() or self.isJct:
                gameglobal.rds.ui.clanWarYaBiao.show()

    def set_isJct(self, old):
        if self.id != BigWorld.player().id:
            return
        if old and not self.isJct:
            gameglobal.rds.ui.clanWarYaBiao.hide()

    def pushCourierData(self, data):
        """
        \xe6\x8e\xa8\xe9\x80\x81\xe6\x89\x80\xe6\x9c\x89\xe9\x95\x96\xe8\xbd\xa6\xe4\xbf\xa1\xe6\x81\xaf
        [{'courierID':courierID, 'mhp':mhp, 'hp': hp, , 'pos': pos, 'res': res, 'tStartMove':int,'state':int}]
        """
        gamelog.debug('@zhangkuo pushCourierData', data)
        self.clanCourierDic = {d['courierID']:d for d in data}
        for value in self.clanCourierDic.itervalues():
            value['isEnd'] = value.get('state', 0) in (gametypes.CLAN_COURIER_DEAD, gametypes.CLAN_COURIER_COMMITED)

        if gameconfigCommon.enableClanWarCourier() and self.inClanCourier():
            if self.isClanCourierAvatar() or self.isJct:
                gameglobal.rds.ui.clanWarYaBiao.show()
