#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impWorldBoss.o
import BigWorld
import gamelog
import gameglobal
from guis import worldBossHelper

class ImpWorldBoss(object):

    def onQueryWorldBossList(self, bossList):
        """
        :param bossList: \xe6\x95\xb0\xe7\xbb\x84[{'bossType': charType,
            'bossBox': bossBox,
            'ttl': ttl,            BOSS\xe5\xad\x98\xe6\xb4\xbb\xe6\x97\xb6\xe9\x97\xb4   int
            'startTime': utils.getNow(),    BOSS\xe5\x88\xb7\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4  \xe6\x97\xb6\xe9\x97\xb4\xe6\x88\xb3
            'isLive': True,     BOSS\xe6\x98\xaf\xe5\x90\xa6\xe5\xad\x98\xe6\xb4\xbb    bool
            'version': self.version,    BOSS\xe7\x89\x88\xe6\x9c\xac\xe5\x8f\xb7     int
            'rareWorldBoss': rareWorldBoss,     \xe6\x98\xaf\xe5\x90\xa6\xe6\x98\xaf\xe5\xa4\xa7BOSS    bool
            'position': position,   BOSS\xe5\x87\xba\xe7\x94\x9f\xe5\x9d\x90\xe6\xa0\x87    \xe5\x85\x83\xe7\xa5\x96
            'refId': refId,     BOSS\xe5\x88\xb7\xe6\x96\xb0id\xef\xbc\x88\xe4\xb8\x96\xe7\x95\x8c\xe6\x80\xaa\xe7\x89\xa9\xe5\x88\xb7\xe6\x96\xb0\xe8\xa1\xa8id\xef\xbc\x89 int
            \xe9\xa6\x96\xe5\x88\x80\xe7\x8e\xa9\xe5\xae\xb6\xef\xbc\x88\xe6\xb2\xa1\xe6\x9c\x89\xe4\xb8\xba\xe7\xa9\xba{}\xef\xbc\x89
            'firstAttacker': {
            'photo': avatar.friend.photo,           string
            'borderId': avatar.photoBorder.borderId,    int
            'school': avatar.school,    int
            'playerName': avatar.playerName,        string
            'guildName': guildName,     string
            'mGbid': avatar.gbID,       nuid
            'sex': avatar.sex       int
            },
            \xe5\x87\xbb\xe6\x9d\x80\xe7\x8e\xa9\xe5\xae\xb6\xef\xbc\x88\xe6\xb2\xa1\xe6\x9c\x89\xe4\xb8\xba\xe7\xa9\xba{}\xef\xbc\x89
            'firstKiller': {
            'photo': avatar.friend.photo,
            'borderId': avatar.photoBorder.borderId,
            'school': avatar.school,
            'playerName': avatar.playerName,
            'guildName': guildName,
            'mGbid': avatar.gbID,
            'sex': avatar.sex
            }
            },]
        :return:
        """
        gamelog.debug('dxk@onQueryWorldBossList', bossList)
        worldBossHelper.getInstance().onGetBossInfo(bossList)

    def onQueryWorldBossTopData(self, topData):
        """
        \xe5\x8f\x82\xe4\xb8\x8e\xe5\x8f\x82\xe7\x85\xa7\xe6\x8e\x92\xe8\xa1\x8c\xe6\xa6\x9c
        :param  topData = {
        \xe5\x8f\x82\xe6\x95\xb0\xe7\xb1\xbb\xe5\x9e\x8b \xef\xbc\x9a \xe5\x8f\x82\xe6\x95\xb0
        \xe6\x96\xb0\xe5\xa2\x9e\xe5\x8f\x82\xe6\x95\xb0id  69 \xef\xbc\x9a\xe6\x80\xbb\xe4\xbc\xa4  gametypes.TOP_UNIVERSAL_WORLD_BOSS_TOTAL_DMG
        3\xef\xbc\x9a \xe8\xaf\xb7\xe6\xb1\x82\xe7\x9a\x84BOSS  refId
        1:  \xe6\x8e\x92\xe8\xa1\x8c\xe6\xa6\x9c\xe7\xb1\xbb\xe5\x9e\x8b
        \xe4\xb8\xaa\xe4\xba\xba\xe6\xa6\x9c\xef\xbc\x9a
            4\xef\xbc\x9a[{8: \xe7\x8e\xa9\xe5\xae\xb6nuid\xef\xbc\x8c 9\xef\xbc\x9a\xe7\x8e\xa9\xe5\xae\xb6\xe5\x90\x8d\xef\xbc\x8c 12\xef\xbc\x9a\xe7\x8e\xa9\xe5\xae\xb6\xe6\x80\xbb\xe4\xbc\xa4\xe5\xae\xb3}\xef\xbc\x8c\xe3\x80\x82\xe3\x80\x82\xe3\x80\x82]
        \xe5\xb7\xa5\xe4\xbc\x9a\xe6\xa6\x9c\xef\xbc\x9a
            4\xef\xbc\x9a[{17: \xe5\xb7\xa5\xe4\xbc\x9anuid\xef\xbc\x8c 10\xef\xbc\x9a\xe5\xb7\xa5\xe4\xbc\x9a\xe5\x90\x8d\xef\xbc\x8c 12\xef\xbc\x9a\xe5\xb7\xa5\xe4\xbc\x9a\xe6\x80\xbb\xe4\xbc\xa4\xe5\xae\xb3}\xef\xbc\x8c\xe3\x80\x82\xe3\x80\x82\xe3\x80\x82]
        }
        :return:
        """
        gamelog.debug('dxk@onQueryWorldBossTopData', topData)
        worldBossHelper.getInstance().onGetBossRankInfo(topData)

    def showWorldBossChooseBuffs(self, buffList):
        """
        :param  buffList  dict  {'avatarBox': None(\xe8\xbf\x99\xe4\xb8\xaa\xe5\xbf\xbd\xe7\x95\xa5)\xef\xbc\x8c 'buffs': [buffid1, buffid2,...] \xef\xbc\x88\xe5\x8f\x96\xe8\xbf\x99\xe4\xb8\xaa\xef\xbc\x89}
        :return:
        """
        self.worldBossChooseBuffs = buffList.get('buffs', [])
        self.worldBossBuffDrop = False
        worldBossHelper.getInstance().onWorldBossBuffStatRefresh(True)

    def onWorldBossChooseBuff(self, code, buffId):
        """
        :param  code  \xe6\x98\xaf\xe5\x90\xa6\xe6\x88\x90\xe5\x8a\x9f
        :param  buffId  \xe6\x88\x90\xe5\x8a\x9f\xe9\x80\x89\xe6\x8b\xa9\xe7\x9a\x84buffId  \xe5\xa4\xb1\xe8\xb4\xa5\xe4\xb8\xba0
        :return:
        """
        if code:
            self.worldBossChooseBuffs = buffId
            worldBossHelper.getInstance().onChooseBuff(buffId)

    def worldBossStart(self):
        self.worldBossActivityState = 1
        worldBossHelper.getInstance().onActivityStart()
        self.base.queryBuffList()

    def worldBossRefresh(self):
        worldBossHelper.getInstance().queryWorldBossInfo()

    def worldBossEnd(self):
        self.worldBossActivityState = 0
        worldBossHelper.getInstance().onActivityEnd()

    def onQueryChooseBuff(self, buffList, isDrop, isSelected):
        """
        :param  buffList  [buffID,buffID,buffID]
        :return:
        """
        if isSelected:
            self.worldBossChooseBuffs = buffList[0]
        else:
            self.worldBossChooseBuffs = buffList.get('buffs', [])
        self.worldBossBuffDrop = isDrop
        worldBossHelper.getInstance().onWorldBossBuffStatRefresh()

    def updateWorldBossCard(self, monsterId):
        """
        :param  monterId
        :return:
        """
        gameglobal.rds.ui.worldBossCardGet.show(monsterId)

    def onDropWorldBossBuff(self, code):
        """
        :param  code  \xe5\xa4\xb1\xe8\xb4\xa5\xe4\xb8\xba0  \xe6\x88\x90\xe5\x8a\x9f\xe4\xb8\xba\xe6\x94\xbe\xe5\xbc\x83\xe7\x9a\x84buffid
        :return:
        """
        if code:
            self.worldBossBuffDrop = True
            worldBossHelper.getInstance().onWorldBossBuffStatRefresh()

    def onWorldBossDie(self, refId, guildName):
        """
        :param  refId  \xe6\xad\xbb\xe4\xba\xa1boss\xe7\x9a\x84refid
        :param  guildName  \xe5\x85\xac\xe4\xbc\x9a\xe5\x90\x8d
        :return:
        """
        worldBossHelper.getInstance().queryWorldBossInfo()
        if worldBossHelper.getInstance().isRareBossRefId(refId):
            BigWorld.callback(15, self.doQueryWorldBossResult)

    def doQueryWorldBossResult(self):
        worldBossHelper.getInstance().worldBossResultQueryCheck(True)

    def onQueryWorldBossCard(self, worldBossCard):
        """
        :param  worldBossCard  {monsterid: {cnt: int, isRare: bool}}
        :return:
        """
        self.worldBossCardInfo = worldBossCard
        gameglobal.rds.ui.worldBossCard.refreshInfo()

    def onQueryWorldBossAccount(self, code, guildDmg, myDmg, guildKill, myKill):
        """
        :param
        code    \xe6\x9f\xa5\xe8\xaf\xa2\xe6\x88\x90\xe5\x8a\x9f\xe5\xa4\xb1\xe8\xb4\xa5
        guildDmg    \xe5\x85\xac\xe4\xbc\x9a\xe6\x80\xbb\xe4\xbc\xa4
        myDmg    \xe7\x8e\xa9\xe5\xae\xb6\xe6\x80\xbb\xe4\xbc\xa4
        guildKill     \xe5\x85\xac\xe4\xbc\x9a\xe6\x80\xbb\xe5\x87\xbb\xe6\x9d\x80
        myKill    \xe7\x8e\xa9\xe5\xae\xb6\xe6\x80\xbb\xe5\x87\xbb\xe6\x9d\x80
        :return:
        """
        self.worldBossAccount = (code,
         guildDmg,
         myDmg,
         guildKill,
         myKill)
        if code:
            worldBossHelper.getInstance().addWorldBossResultPushIcon()

    def updateWorldBossJoin(self, checkCnt, refId):
        """
        :param  checkCnt  \xe5\x8f\x82\xe4\xb8\x8e\xe8\xae\xa1\xe6\x95\xb0
        :return:
        """
        if not getattr(self, 'worldBossAttendDict', None):
            self.worldBossAttendDict = {}
        self.worldBossAttendDict[refId] = checkCnt
        worldBossHelper.getInstance().onUpdateAttendValue()

    def onQueryGuildJoinCnt(self, cnt):
        """
        :param  cnt  \xe5\x8f\x82\xe4\xb8\x8e\xe4\xba\xba\xe6\x95\xb0
        :return:
        """
        self.worldBossAttendNum = cnt
        gameglobal.rds.ui.worldBossDetail.refreshAttendNum()
