#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impNpcFavor.o
import BigWorld
from gamestrings import gameStrings
from appSetting import Obj as AppSettings
import keys
import gameconfigCommon
import commNpcFavor
import gamelog
import gameglobal
import utils
import gametypes
from guis import uiConst
from guis import uiUtils
from cdata import game_msg_def_data as GMDD
from data import nf_npc_data as NND
from data import nf_give_item_group_data as NFGIGD
from data import nf_npc_friendly_level_data as NNFLD
from data import game_msg_data as GMD
from data import sys_config_data as SCD
from data import nf_npc_level_data as NNLD
FRIEND_LEVEL = 2
HATE_LEVEL = 1

class NpcFriendVal(object):

    def __init__(self, lv, gbId, pfVal, name, sex, school, borderId, timeStamp, photo):
        self.lv = lv
        self.gbId = gbId
        self.pfVal = pfVal
        self.name = name
        self.sex = sex
        self.school = school
        self.borderId = borderId
        self.timeStamp = timeStamp
        self.photo = photo


class NpcFavor(object):

    def __init__(self):
        self.todayFavor = [0, 0]
        self.npcStatusDic = {}
        self.npcFavorValue = {}
        self.npcFavorValueWeekly = {}
        self.npcFavorValueDaily = {}
        self.todaySendNpcRecord = {}
        self.todaySendItemRecord = {}
        self.sendRecordDaily = {}
        self.askRecord = {}
        self.askRecordDaily = {}
        self.topFriend = {}
        self.npcMsgDic = {}
        self.questItemCnt = 0
        self.askItemList = []
        self.isTodayPushed = False
        self.favorGroups = {}
        self.favorSendCnt = {}
        self.dailyGiftRecord = {}
        self.buffRecord = {}
        self.dailyQuestRecord = {}
        self.weeklyQuestRecord = {}
        self.monthlyQuestRecord = {}
        self.questRecord = {}
        self.cosRecord = {}
        self.interactiveRecord = {}
        self.npcRequest = []
        self.nfWHeartBeat = {}

    def isShowNpcDetail(self, npcPId):
        p = BigWorld.player()
        if p.friend.has_key(npcPId):
            return True
        for en in p.entitiesInRange(5, 'Npc'):
            if commNpcFavor.getNpcPId(en.npcId) == npcPId:
                return True

        return False

    def checkDailyGift(self, npcId):
        npcPId = commNpcFavor.getNpcPId(npcId)
        if self.dailyGiftRecord.get(npcPId, False):
            return False
        friendLv, _ = self.getPlayerRelationLvAndVal(npcPId)
        return NNLD.data.get((npcPId, friendLv), {}).has_key('giftId') or NNLD.data.get((npcPId, friendLv), {}).has_key('weekGiftId')

    def getNpcCosList(self, npcId):
        npcPId = commNpcFavor.getNpcPId(npcId)
        if self.cosRecord.get(npcPId, False):
            return []
        friendLv, _ = self.getPlayerRelationLvAndVal(npcPId)
        cosBuffList = []
        buffInfo = NNLD.data[npcPId, friendLv].get('cosID', ())
        buffDic = {}
        for buffId, name in buffInfo:
            buffDic[buffId] = name

        buffList = buffDic.keys()
        cosedBuffList = self.buffRecord.get(npcPId, [])
        cosBuffList.extend(list(set(buffList) - set(cosedBuffList)))
        cosBuffList.sort()
        return [ (id, buffDic[id]) for id in cosBuffList ]

    def checkIsCompleted(self, keys, npcPId, lv):
        friendLv, _ = self.getPlayerRelationLvAndVal(npcPId)
        if friendLv < lv:
            return False
        if keys == 'fameBuff' or keys == 'expBuff':
            return True
        if keys == 'giftId':
            return self.dailyGiftRecord.get(npcPId, False)
        if keys == 'nfBuff':
            return self.cosRecord.get(npcPId, False)
        if keys == 'interactID':
            return self.interactiveRecord.get(npcPId, False)
        if keys == ('questLoop', 'quest'):
            return self.dailyQuestRecord.get(npcPId, 0) or self.questRecord.get(npcPId, 0) or self.weeklyQuestRecord.get(npcPId, 0) or self.monthlyQuestRecord.get(npcPId, 0)

    def checkDailyQuest(self, npcId):
        npcPId = commNpcFavor.getNpcPId(npcId)
        friendLv, _ = self.getPlayerRelationLvAndVal(npcPId)
        if self.dailyQuestRecord.get(npcPId, 0):
            return False
        elif gameconfigCommon.enableNFNewQuestLoop():
            return NNLD.data[npcPId, friendLv].has_key('questLoopDaily')
        else:
            return NNLD.data[npcPId, friendLv].has_key('questLoop')

    def checkWeeklyQuest(self, npcId):
        npcPId = commNpcFavor.getNpcPId(npcId)
        friendLv, _ = self.getPlayerRelationLvAndVal(npcPId)
        if self.weeklyQuestRecord.get(npcPId, 0):
            return False
        return NNLD.data[npcPId, friendLv].has_key('questLoopWeekly')

    def checkMonthlyQuest(self, npcId):
        npcPId = commNpcFavor.getNpcPId(npcId)
        friendLv, _ = self.getPlayerRelationLvAndVal(npcPId)
        if self.monthlyQuestRecord.get(npcPId, 0):
            return False
        return NNLD.data[npcPId, friendLv].has_key('questLoopMonthly')

    def checkQuest(self, npcId):
        npcPId = commNpcFavor.getNpcPId(npcId)
        friendLv, _ = self.getPlayerRelationLvAndVal(npcPId)
        completedQuest = self.questRecord.get(npcPId, ())
        if not NNLD.data.get((npcPId, friendLv), {}).get('quest', None):
            return False
        else:
            return not completedQuest or completedQuest[1] == commNpcFavor.NF_DAILY_QUEST_STAT_ABANDON

    def testNpcFriend(self):
        p = BigWorld.player()

    def getTopFriendlyPlayer(self, npcId):
        if not self.topFriend.has_key(npcId):
            return None
        topList = [ info for info in self.topFriend[npcId] if info.lv >= FRIEND_LEVEL ]
        topList.sort(cmp=self.cmpFriendVal)
        if topList:
            return topList[0]
        else:
            return None

    def getTopHatePlayer(self, npcId):
        if not self.topFriend.has_key(npcId):
            return None
        topList = [ info for info in self.topFriend[npcId] if info.lv <= HATE_LEVEL ]
        topList.sort(cmp=self.cmpFriendVal)
        if topList:
            return topList[-1]
        else:
            return None

    def cmpFriendVal(self, infoA, infoB):
        if infoA.lv != infoB.lv:
            return cmp(infoB.lv, infoA.lv)
        if infoB.pfVal != infoA.pfVal:
            return cmp(infoB.pfVal, infoA.pfVal)
        return cmp(infoA.timeStamp, infoB.timeStamp)

    def getNpcStatus(self, npcPid):
        if not self.npcStatusDic.get(npcPid):
            return [0] * 4
        return self.npcStatusDic.get(npcPid, [0] * 4)

    def isQuestItem(self, npcId, itemGId):
        p = BigWorld.player()
        questNpcPId, questId = self.todayFavor
        isQuestItem = False
        favorNpcPid, _ = p.npcFavor.todayFavor
        if questId and favorNpcPid == npcId:
            questItemInfo = commNpcFavor.getQuestItemInfo(questId)
            questItemGId, questItemCnt = questItemInfo if questItemInfo else ((), 0)
            isQuestItem = itemGId in questItemGId and self.questItemCnt < questItemCnt
        return isQuestItem

    def getPlayerRelationLvAndVal(self, npcId):
        p = BigWorld.player()
        pVal = p.npcFavor.npcFavorValue.get(npcId, 0)
        level = commNpcFavor.getPFriendlyLv(npcId, pVal, p)
        return (level, pVal)

    def isLockLvState(self, npcPId, pfLv):
        return NNLD.data.get((npcPId, pfLv), {}).get('lockQuest', 0) == 9999999 or NNLD.data.get((npcPId, pfLv + 1), {}).get('lockQuest', 0) == 9999999

    def getConfigData(self, npcId):
        return NND.data.get(npcId, {})

    def getNpcLevelName(self, npcId, friendLv):
        npcLv = commNpcFavor.getNpcLv(npcId)
        return NNFLD.data.get((npcLv, friendLv), {}).get('friendlyName', '')

    def getSendUpValue(self, npcPId, item, itemCnt):
        defaultVal = commNpcFavor.getFriendlyVal(item)
        itemGId = commNpcFavor.getGiveItemGId(item)
        likeAdd = 0
        if self.favorGroups.get(npcPId, 0) == itemGId:
            loveCurCnt = self.favorSendCnt.get(npcPId, 0)
            loveMaxCnt = SCD.data.get('nfLoveCount', 0)
            if loveCurCnt < loveMaxCnt:
                loveAddRatio = SCD.data.get('nfLikeGiftAddRatio', 0)
                likeAdd = defaultVal * loveAddRatio * min(loveMaxCnt - loveCurCnt, itemCnt)
        return int(defaultVal * itemCnt + likeAdd)

    def getSendItemMacCount(self, npcPId, item):
        itemGId = commNpcFavor.getGiveItemGId(item)
        questNpcPId, questId = self.todayFavor
        questItemInfo = commNpcFavor.getQuestItemInfo(questId)
        questItemGId, questItemCnt = questItemInfo if questItemInfo else ((), 0)
        if questNpcPId == npcPId and questItemGId and itemGId in questItemGId:
            questItemCnt = max(0, questItemCnt - self.questItemCnt)
        else:
            questItemCnt = 0
        npcCount = NND.data.get(npcPId, {}).get('dailyMaxCnt', 0) - self.todaySendNpcRecord.get(npcPId, 0)
        itemCount = NFGIGD.data.get(itemGId, {}).get('dailyMaxCnt', 0) - self.todaySendItemRecord.get(itemGId, {}).get(npcPId, 0)
        return max(questItemCnt, min(npcCount, itemCount))

    def testTopFriend(self):
        npcTopFriend = []
        self.topFriend[1] = npcTopFriend
        p = BigWorld.player()
        npcTopFriend.append((1, {'gbId': p.gbId + 1,
          'pfVal': 100,
          'name': '1_100',
          'school': p.school,
          'sex': p.physique.sex}))
        npcTopFriend.append((2, {'gbId': p.gbId + 2,
          'pfVal': 101,
          'name': '2_101',
          'school': p.school,
          'sex': p.physique.sex}))
        npcTopFriend.append((3, {'gbId': p.gbId + 3,
          'pfVal': 101,
          'name': '3_101',
          'school': p.school,
          'sex': p.physique.sex}))
        npcTopFriend.append((4, {'gbId': p.gbId + 4,
          'pfVal': 103,
          'name': '4_103',
          'school': p.school,
          'sex': p.physique.sex}))
        npcTopFriend.append((5, {'gbId': p.gbId + 4,
          'pfVal': 105,
          'name': '5_105',
          'school': p.school,
          'sex': p.physique.sex}))
        npcTopFriend.append((6, {'gbId': p.gbId + 4,
          'pfVal': 101,
          'name': '6_101',
          'school': p.school,
          'sex': p.physique.sex}))
        npcTopFriend.append((6, {'gbId': p.gbId + 4,
          'pfVal': 103,
          'name': '6_103',
          'school': p.school,
          'sex': p.physique.sex}))
        npcTopFriend.append((7, {'gbId': p.gbId + 4,
          'pfVal': 103,
          'name': '7_103',
          'school': p.school,
          'sex': p.physique.sex}))
        npcTopFriend.append((7, {'gbId': p.gbId + 4,
          'pfVal': 109,
          'name': '7_109',
          'school': p.school,
          'sex': p.physique.sex}))

    def testTopRank(self):
        import gametypes
        rankData = {}
        rankData[gametypes.TOP_UNIVERSAL_TOP_ID] = gametypes.TOP_TYPE_NPC_FAVOR
        rankData[gametypes.TOP_UNIVERSAL_KEY] = '0'
        dataList = []
        for i in xrange(10):
            info = {}
            info[gametypes.TOP_UNIVERSAL_GBID] = i + 1
            info[gametypes.TOP_UNIVERSAL_SCHOOL] = BigWorld.player().school
            info[gametypes.TOP_UNIVERSAL_ROLE_NAME] = 'npc' + str(i)
            info[gametypes.TOP_UNIVERSAL_VALUE] = i * 200
            dataList.append(info)

        rankData[gametypes.TOP_UNIVERSAL_DATA_LIST] = dataList
        gameglobal.rds.ui.npcRelationshipXindong.updateRankData(rankData)
        rankData = {}
        rankData[gametypes.TOP_UNIVERSAL_TOP_ID] = gametypes.TOP_TYPE_NPC_FAVOR
        rankData[gametypes.TOP_UNIVERSAL_KEY] = '1'
        dataList = []
        for i in xrange(10):
            info = {}
            info[gametypes.TOP_UNIVERSAL_GBID] = i + 1
            info[gametypes.TOP_UNIVERSAL_SCHOOL] = BigWorld.player().school
            info[gametypes.TOP_UNIVERSAL_ROLE_NAME] = 'player' + str(i)
            info[gametypes.TOP_UNIVERSAL_VALUE] = i * 200
            dataList.append(info)

        rankData[gametypes.TOP_UNIVERSAL_DATA_LIST] = dataList
        gameglobal.rds.ui.npcRelationshipXindong.updateRankData(rankData)

    def sendNpcFriendTmpMsg(self, npcPid, content):
        msg = {}
        npcData = NND.data.get(npcPid, {})
        p = BigWorld.player()
        msg['photoBorderIcon'] = p.getPhotoBorderIcon(npcData.get('borderId', 1), uiConst.PHOTO_BORDER_ICON_SIZE108)
        msg['name'] = npcData.get('name', '')
        msg['photo'] = uiUtils.getPNpcIcon(npcPid)
        msg['time'] = utils.getNow()
        msg['msg'] = content
        msg['isMe'] = False
        p._addTempMsg(npcPid, gametypes.NPC_FRIEND_MSG_TYPE, msg)

    def sendSysTmpMsg(self, npcPid, content):
        msg = {}
        npcData = NND.data.get(npcPid, {})
        p = BigWorld.player()
        msg['photoBorderIcon'] = p.getPhotoBorderIcon(npcData.get('borderId', 1), uiConst.PHOTO_BORDER_ICON_SIZE108)
        msg['name'] = npcData.get('name', '')
        msg['photo'] = uiUtils.getPNpcIcon(npcPid)
        msg['time'] = utils.getNow()
        msg['msg'] = content
        msg['isMe'] = False
        p._addTempMsg(npcPid, gametypes.FRIEND_MSG_TYPE_SYSTEM_NOTIFY, msg)


class ImpNpcFavor(object):

    def initNpcFavor(self):
        self.npcFavor = NpcFavor()

    def sendOnLoginNF(self, data):
        """
        :param data:
        data[0]: int \xe4\xbb\xbb\xe5\x8a\xa1npc\xe7\x88\xb6Id  npcPId
        data[1]: int \xe4\xbb\xbb\xe5\x8a\xa1Id questId
        data[2]: dict npc\xe7\x8a\xb6\xe6\x80\x81 {npcPId: [foodVal, energyVal, moodVal, healthVal, socialVal], ...}
        data[3]: dict npc\xe5\xa5\xbd\xe6\x84\x9f\xe5\xba\xa6\xef\xbc\x88\xe6\xb0\xb8\xe4\xb9\x85\xef\xbc\x89 {npcPId: val, ...}
        data[4]: dict npc\xe5\xa5\xbd\xe6\x84\x9f\xe5\xba\xa6\xef\xbc\x88\xe5\x91\xa8\xef\xbc\x89{npcPId: val, ...}
        data[5]: dict npc\xe5\xa5\xbd\xe6\x84\x9f\xe5\xba\xa6\xef\xbc\x88\xe6\x97\xa5\xef\xbc\x89{npcPId: val, ...}
        data[6]: dict \xe9\x80\x81\xe7\xa4\xbc\xe8\xae\xb0\xe5\xbd\x95\xef\xbc\x88\xe6\x97\xa5\xef\xbc\x89 {npcPId: cnt, ...}
        data[7]: dict \xe9\x80\x81\xe7\xa4\xbc\xe8\xae\xb0\xe5\xbd\x95\xef\xbc\x88\xe6\x97\xa5\xef\xbc\x89 {itemGId: {npcPId:cnt, ...}, ...}
        data[8]: dict \xe7\xb4\xa2\xe5\x8f\x96\xe8\xae\xb0\xe5\xbd\x95\xef\xbc\x88\xe6\xb0\xb8\xe4\xb9\x85\xef\xbc\x89 {itemGId: cnt, ...}
        data[9]: dict \xe7\xb4\xa2\xe5\x8f\x96\xe8\xae\xb0\xe5\xbd\x95\xef\xbc\x88\xe6\x97\xa5\xef\xbc\x89 {itemGId: cnt, ...}
        data[10]: int  \xe5\xb7\xb2\xe8\xb5\xa0\xe9\x80\x81\xe4\xbb\xbb\xe5\x8a\xa1\xe7\x89\xa9\xe5\x93\x81\xe6\x95\xb0\xe9\x87\x8f questItemCnt
        data[11]: list \xe7\xb4\xa2\xe8\xa6\x81\xe7\x89\xa9\xe5\x93\x81\xe5\x88\x97\xe8\xa1\xa8 [itemId1, itemId2, ...]
        data[12]: dict \xe5\xbf\x83\xe5\x8a\xa8\xe7\x89\xa9\xe5\x93\x81 {npcPId1: itemId1, ...}
        data[13]: dict \xe5\xb7\xb2\xe9\x80\x81\xe5\xbf\x83\xe5\x8a\xa8\xe7\x89\xa9\xe5\x93\x81 {npcPId1: itemCnt1, ...}
        data[14]: dict \xe5\xbd\x93\xe6\x97\xa5\xe5\xb7\xb2\xe9\xa2\x86\xe5\x8f\x96\xe7\xa4\xbc\xe7\x89\xa9\xe6\xa0\x87\xe5\xbf\x97 {npcPId: flag, ...}
        data[15]: dict \xe5\xbd\x93\xe6\x97\xa5\xe5\xb7\xb2\xe6\x89\xae\xe6\xbc\x94\xe6\xa0\x87\xe5\xbf\x97 {npcPId: flag, ...}
        data[16]: dict \xe5\xbd\x93\xe6\x97\xa5\xe6\x97\xa5\xe5\xb8\xb8\xe4\xbb\xbb\xe5\x8a\xa1 {npcPId: questLoopId, ...}
        data[17]: dict \xe5\xbd\x93\xe6\x97\xa5\xe4\xbb\xbb\xe5\x8a\xa1 {npcPId: (questId, flag), ...}
        data[18]: dict \xe5\xbd\x93\xe5\x91\xa8\xe5\xb7\xb2\xe9\xa2\x86\xe5\x8f\x96\xe7\xa4\xbc\xe7\x89\xa9\xe6\xa0\x87\xe5\xbf\x97 {npcPId: flag, ...}
        data[19]: dict \xe5\xb7\xb2\xe4\xba\xa4\xe4\xba\x92\xe6\xa0\x87\xe5\xbf\x97 {npcPId: flag, ...}
        data[20]: dict \xe5\xa5\x96\xe5\x8a\xb1\xe5\x91\xa8\xe5\xa5\xbd\xe6\x84\x9f {npcPId: val, ...}
        data[21]: dict \xe5\x91\xa8\xe6\x97\xa5\xe5\xb8\xb8\xe4\xbb\xbb\xe5\x8a\xa1 {npcPId: questLoopId, ...}
        data[22]: dict \xe6\x9c\x88\xe6\x97\xa5\xe5\xb8\xb8\xe4\xbb\xbb\xe5\x8a\xa1 {npcPId: questLoopId, ...}
        data[23]: dict 7\xe6\x97\xa5\xe5\xbf\x83\xe5\x8a\xa8\xe5\x80\xbc {npcPId: val, ...}
        :return:
        """
        gamelog.info('jbx:sendOnLoginNF', data)
        self.npcFavor.todayFavor = [data[0], data[1]]
        self.npcFavor.npcStatusDic = data[2]
        self.npcFavor.npcFavorValue = data[3]
        self.npcFavor.npcFavorValueWeekly = data[4]
        self.npcFavor.npcFavorValueDaily = data[5]
        self.npcFavor.todaySendNpcRecord = data[6]
        self.npcFavor.todaySendItemRecord = data[7]
        self.npcFavor.askRecord = data[8]
        self.npcFavor.askRecordDaily = data[9]
        self.npcFavor.needTodayFavorPush = data[0]
        self.npcFavor.questItemCnt = data[10] if data[10] else 0
        self.npcFavor.askItemList = data[11]
        self.npcFavor.isTodayPushed = False
        self.npcFavor.favorGroups = data[12]
        self.npcFavor.favorSendCnt = data[13]
        self.npcFavor.dailyGiftRecord = data[14]
        self.npcFavor.dailyGiftRecord.update(data[18])
        self.npcFavor.cosRecord = data[15]
        self.npcFavor.dailyQuestRecord = data[16]
        self.npcFavor.questRecord = data[17]
        self.npcFavor.interactiveRecord = data[19]
        self.npcFavor.weeklyQuestRecord = data[21]
        self.npcFavor.monthlyQuestRecord = data[22]
        self.npcFavor.nfWHeartBeat = data[23]
        self.checkPushNpc()

    def checkNpcFrindLv(self):
        return self.lv >= SCD.data.get('nfLvLimit', 20)

    def checkNpcFavorDailyPush(self):
        key = keys.SET_NPC_FAVOR_PUSH_DAILY % self.gbId
        if utils.isSameDay(utils.getNow(), AppSettings.get(key, 0)):
            return False
        return True

    def checkPushNpc(self):
        if not self.checkNpcFavorDailyPush():
            return False
        if not gameconfigCommon.enableNpcFavor():
            return
        if not self.checkNpcFrindLv():
            return
        if self.lv < SCD.data.get('npcQuestLv', 99):
            return
        if self.npcFavor.isTodayPushed:
            return
        if not self.npcFavor.todayFavor[0]:
            return
        if commNpcFavor.checkInLockTime():
            return
        npcId = self.npcFavor.todayFavor[0]
        if self.needPushNpcQuest(npcId) and not getattr(self, 'needNpcPush', 0):
            key = keys.SET_NPC_FAVOR_PUSH_DAILY % self.gbId
            AppSettings[key] = utils.getNow()
            AppSettings.save()
            self.needNpcPush = self.npcFavor.todayFavor[0]
            self.npcFavor.isTodayPushed = True
            friendLv, _ = self.npcFavor.getPlayerRelationLvAndVal(npcId)
            intDay = utils.getMonthDayInt(utils.getNow())
            questChatMsg = NNLD.data.get((npcId, friendLv), {}).get('questChatMsg', ('day0', 'day1'))
            msg = questChatMsg[intDay % len(questChatMsg)]
            self.needNpcPush = 0
            self.npcFavor.sendNpcFriendTmpMsg(npcId, msg)

    def needPushNpcQuest(self, npcId):
        return npcId == self.npcFavor.todayFavor[0] and not self.npcFavor.todayFavor[1]

    def sendOnResetWeeklyNF(self, data):
        """
        :param data: {npcPId: val, ...} npc\xe5\xa5\xbd\xe6\x84\x9f\xe5\xba\xa6\xef\xbc\x88\xe5\x91\xa8\xef\xbc\x89
        :return:
        """
        gamelog.info('jbx:sendOnResetWeeklyNF')
        self.npcFavor.npcFavorValueWeekly = data

    def sendOnResetDailyNF(self, data):
        """
        :param data:
        data[0]: dict npc\xe7\x8a\xb6\xe6\x80\x81 {npcPId: [foodVal, energyVal, moodVal, healthVal, socialVal], ...}
        data[1]: dict npc\xe5\xa5\xbd\xe6\x84\x9f\xe5\xba\xa6\xef\xbc\x88\xe6\xb0\xb8\xe4\xb9\x85\xef\xbc\x89 {npcPId: val, ...}
        data[2]: dict npc\xe5\xa5\xbd\xe6\x84\x9f\xe5\xba\xa6\xef\xbc\x88\xe5\x91\xa8\xef\xbc\x89{npcPId: val, ...}
        data[3]: dict npc\xe5\xa5\xbd\xe6\x84\x9f\xe5\xba\xa6\xef\xbc\x88\xe6\x97\xa5\xef\xbc\x89{npcPId: val, ...}
        data[4]: dict \xe9\x80\x81\xe7\xa4\xbc\xe8\xae\xb0\xe5\xbd\x95\xef\xbc\x88\xe6\x97\xa5\xef\xbc\x89 {npcPId: cnt, ...}
        data[5]: dict \xe9\x80\x81\xe7\xa4\xbc\xe8\xae\xb0\xe5\xbd\x95\xef\xbc\x88\xe6\x97\xa5\xef\xbc\x89 {itemGId: {npcPId:cnt, ...}, ...}
        data[6]: dict \xe7\xb4\xa2\xe5\x8f\x96\xe8\xae\xb0\xe5\xbd\x95\xef\xbc\x88\xe6\x97\xa5\xef\xbc\x89 {itemGId: cnt, ...}
        data[7]: int  \xe5\xb7\xb2\xe8\xb5\xa0\xe9\x80\x81\xe4\xbb\xbb\xe5\x8a\xa1\xe7\x89\xa9\xe5\x93\x81\xe6\x95\xb0\xe9\x87\x8f questItemCnt
        data[8]: int \xe4\xbb\xbb\xe5\x8a\xa1Id questId
        data[9]: dict \xe5\xb7\xb2\xe9\x80\x81\xe5\xbf\x83\xe5\x8a\xa8\xe7\x89\xa9\xe5\x93\x81 {npcPId1: itemCnt1, ...}
        data[10]: dict \xe5\xbd\x93\xe6\x97\xa5\xe5\xb7\xb2\xe9\xa2\x86\xe5\x8f\x96\xe7\xa4\xbc\xe7\x89\xa9\xe6\xa0\x87\xe5\xbf\x97 {npcPId: flag, ...}
        data[11]: dict \xe5\xbd\x93\xe6\x97\xa5\xe5\xb7\xb2\xe6\x89\xae\xe6\xbc\x94\xe6\xa0\x87\xe5\xbf\x97 {npcPId: flag, ...}
        data[12]: dict \xe5\xbd\x93\xe6\x97\xa5\xe6\x97\xa5\xe5\xb8\xb8\xe4\xbb\xbb\xe5\x8a\xa1 {npcPId: questLoopId, ...}
        data[13]: dict \xe5\xbd\x93\xe6\x97\xa5\xe4\xbb\xbb\xe5\x8a\xa1 {npcPId: (questId, flag), ...}
        data[14]: dict \xe5\xbd\x93\xe5\x91\xa8\xe5\xb7\xb2\xe9\xa2\x86\xe5\x8f\x96\xe7\xa4\xbc\xe7\x89\xa9\xe6\xa0\x87\xe5\xbf\x97 {npcPId: flag, ...}
        data[15]: dict \xe5\xb7\xb2\xe4\xba\xa4\xe4\xba\x92\xe6\xa0\x87\xe5\xbf\x97 {npcPId: flag, ...}
        data[16]: dict \xe5\xa5\x96\xe5\x8a\xb1\xe5\x91\xa8\xe5\xa5\xbd\xe6\x84\x9f {npcPId: val, ...}
        data[17]: dict \xe5\x91\xa8\xe6\x97\xa5\xe5\xb8\xb8\xe4\xbb\xbb\xe5\x8a\xa1 {npcPId: questLoopId, ...}
        data[18]: dict \xe6\x9c\x88\xe6\x97\xa5\xe5\xb8\xb8\xe4\xbb\xbb\xe5\x8a\xa1 {npcPId: questLoopId, ...}
        data[19]: dict 7\xe6\x97\xa5\xe5\xbf\x83\xe5\x8a\xa8\xe5\x80\xbc {npcPId: val, ...}
        :return:
        """
        gamelog.info('jbx:sendOnResetDailyNF', data)
        self.npcFavor.npcStatusDic = data[0]
        for npcPId, value in data[1].iteritems():
            self.onNpcFavorVarChange(npcPId, value)

        self.npcFavor.npcFavorValueWeekly = data[2]
        self.npcFavor.npcFavorValueDaily = data[3]
        self.npcFavor.todaySendNpcRecord = data[4]
        self.npcFavor.todaySendItemRecord = data[5]
        self.npcFavor.askRecordDaily = data[6]
        self.npcFavor.questItemCnt = data[7]
        self.npcFavor.todayFavor[1] = data[8]
        self.npcFavor.sendRecordDaily = data[9]
        self.npcFavor.dailyGiftRecord = data[10]
        self.npcFavor.dailyGiftRecord.update(data[14])
        self.npcFavor.cosRecord = data[11]
        self.npcFavor.dailyQuestRecord = data[12]
        self.npcFavor.questRecord = data[13]
        self.npcFavor.interactiveRecord = data[15]
        self.npcFavor.weeklyQuestRecord = data[17]
        self.npcFavor.monthlyQuestRecord = data[18]
        self.npcFavor.nfWHeartBeat = data[19]

    def sendOnSyncQuestInfoNF(self, data):
        """
        :param data:
        data[0]: int \xe4\xbb\xbb\xe5\x8a\xa1npc\xe7\x88\xb6Id  npcPId
        data[1]: int \xe4\xbb\xbb\xe5\x8a\xa1Id  questId(=0\xe4\xbb\xa3\xe8\xa1\xa8\xe6\x9c\xaa\xe9\xa2\x86\xe5\x8f\x96)
        data[2]: list \xe7\xb4\xa2\xe8\xa6\x81\xe7\x89\xa9\xe5\x93\x81\xe5\x88\x97\xe8\xa1\xa8 [itemId1, itemId2, ...]
        data[3]: dict \xe5\xbf\x83\xe5\x8a\xa8\xe7\x89\xa9\xe5\x93\x81 {npcPId1: itemId1, ...}
        :return:
        """
        gamelog.info('jbx:sendOnSyncQuestInfoNF', data)
        self.npcFavor.todayFavor = [data[0], data[1]]
        self.npcFavor.askItemList = data[2]
        self.npcFavor.isTodayPushed = False
        self.checkPushNpc()

    def sendFeaturePartNF(self, data):
        """
        :param data: {npcPId: [foodVal, energyVal, moodVal, healthVal, socialVal], ...} npc\xe7\x8a\xb6\xe6\x80\x81
        :return:
        """
        gamelog.info('jbx:sendFeaturePartNF', data)
        self.npcFavor.npcStatusDic.update(data)
        gameglobal.rds.ui.npcInteractive.refreshInfo()

    def onGiveItemNF(self, data):
        """
        :param data:  \xe5\x9d\x87\xe4\xb8\xba\xe4\xb8\x8enpcPId\xe3\x80\x81itemGId\xe5\x85\xb3\xe8\x81\x94\xe7\x9a\x84\xe5\xa2\x9e\xe9\x87\x8f
        data[0]: int \xe9\x80\x81\xe7\xa4\xbc\xe8\xae\xb0\xe5\xbd\x95\xef\xbc\x88\xe6\x97\xa5\xe3\x80\x81npcPId\xe5\x85\xb3\xe8\x81\x94\xef\xbc\x89 val
        data[1]: int \xe9\x80\x81\xe7\xa4\xbc\xe8\xae\xb0\xe5\xbd\x95\xef\xbc\x88\xe6\x97\xa5\xe3\x80\x81itemGId\xe5\x85\xb3\xe8\x81\x94\xef\xbc\x89val
        data[2]: int npc\xe5\xa5\xbd\xe6\x84\x9f\xe5\xba\xa6\xef\xbc\x88\xe6\xb0\xb8\xe4\xb9\x85\xef\xbc\x89val
        data[3]: int npc\xe5\xa5\xbd\xe6\x84\x9f\xe5\xba\xa6\xef\xbc\x88\xe5\x91\xa8\xef\xbc\x89val
        data[4]: int npc\xe5\xa5\xbd\xe6\x84\x9f\xe5\xba\xa6\xef\xbc\x88\xe6\x97\xa5\xef\xbc\x89val
        data[5]: list npc\xe7\x8a\xb6\xe6\x80\x81  [foodVal, energyVal, moodVal, healthVal, socialVal]
        data[6]: int npcPId
        data[7]: int itemGId
        data[8]: int  \xe5\xb7\xb2\xe8\xb5\xa0\xe9\x80\x81\xe4\xbb\xbb\xe5\x8a\xa1\xe7\x89\xa9\xe5\x93\x81\xe6\x95\xb0\xe9\x87\x8f questItemCnt
        data[9]: int  \xe5\xb7\xb2\xe8\xb5\xa0\xe9\x80\x81\xe5\xa5\xbd\xe6\x84\x9f\xe7\x89\xa9\xe5\x93\x81\xe6\x95\xb0\xe9\x87\x8f loveCurCnt
        data[10]: int npc\xe5\xa5\xbd\xe6\x84\x9f\xe5\xba\xa6\xef\xbc\x88\xe5\x91\xa8\xe5\xa5\x96\xe5\x8a\xb1\xef\xbc\x89val
        data[11]: int npc\xe5\xbf\x83\xe5\x8a\xa8\xe5\x80\xbc val
        :return:
        """
        gamelog.info('jbx:onGiveItemNF', data)
        npcId, itemId = data[6], data[7]
        self.npcFavor.todaySendNpcRecord[npcId] = data[0]
        self.npcFavor.todaySendItemRecord.setdefault(itemId, {})[npcId] = data[1]
        self.onNpcFavorVarChange(npcId, data[2])
        self.npcFavor.npcFavorValueWeekly[npcId] = data[3]
        self.npcFavor.npcFavorValueDaily[npcId] = data[4]
        self.npcFavor.npcStatusDic[npcId] = data[5]
        self.npcFavor.questItemCnt = data[8]
        self.npcFavor.favorSendCnt[npcId] = data[9]
        self.npcFavor.nfWHeartBeat[npcId] = data[11]
        gameglobal.rds.ui.npcSendGift.refreshInfo()
        gameglobal.rds.ui.npcInteractive.refreshInfo()
        self.showAddContactNF(npcId)

    def onNpcFavorVarChange(self, npcPId, newVal):
        oldLv = commNpcFavor.getPFriendlyLv(npcPId, self.npcFavor.npcFavorValue.get(npcPId, 0), self)
        self.npcFavor.npcFavorValue[npcPId] = newVal
        newLv = commNpcFavor.getPFriendlyLv(npcPId, self.npcFavor.npcFavorValue.get(npcPId, 0), self)
        if oldLv != newLv:
            quests = NNLD.data.get((npcPId, newLv), {}).get('quest', [])
            self._onUpdateQuestInfoCacheModified(quests)

    def onAskItemNF(self, data):
        """
        :param data:  \xe5\x9d\x87\xe4\xb8\xba\xe4\xb8\x8enpcPId\xe3\x80\x81itemGId\xe5\x85\xb3\xe8\x81\x94\xe7\x9a\x84\xe5\xa2\x9e\xe9\x87\x8f
        data[0]: int \xe7\xb4\xa2\xe8\xa6\x81\xe8\xae\xb0\xe5\xbd\x95\xef\xbc\x88\xe6\x97\xa5\xe3\x80\x81itemGId\xe5\x85\xb3\xe8\x81\x94\xef\xbc\x89 val
        data[1]: int \xe7\xb4\xa2\xe8\xa6\x81\xe8\xae\xb0\xe5\xbd\x95\xef\xbc\x88\xe6\xb0\xb8\xe4\xb9\x85\xe3\x80\x81itemGId\xe5\x85\xb3\xe8\x81\x94\xef\xbc\x89val
        data[2]: int npc\xe5\xa5\xbd\xe6\x84\x9f\xe5\xba\xa6\xef\xbc\x88\xe6\x97\xa5\xef\xbc\x89val
        data[3]: int npcPId
        data[4]: int itemGId
        :return:
        """
        gamelog.info('jbx:onAskItemNF', data)
        npcPId, itemGid = data[3], data[4]
        self.npcFavor.askRecordDaily[itemGid] = data[0]
        self.npcFavor.askRecord[itemGid] = data[1]
        self.npcFavor.npcFavorValueDaily[npcPId] = data[2]
        gameglobal.rds.ui.npcSendGift.refreshInfo()
        gameglobal.rds.ui.npcInteractive.refreshInfo()
        gameglobal.rds.ui.npcSendGift.handleTabSureBtnClick()

    def onQueryTopPFriendlyWithLvNF(self, npcPId, data):
        """
        :param npcPId: npc\xe7\x88\xb6Id
        :param data: [(lv, {gbId: (pfVal, name, sex, school, borderId, (photo), timeStamp) ...}), ...]   npc\xe7\x9a\x84\xe6\xaf\x8f\xe4\xb8\xaa\xe5\xa5\xbd\xe6\x84\x9f\xe7\xad\x89\xe7\xba\xa7\xe6\xae\xb5\xe7\x9a\x84\xe5\x89\x8dN\xe5\x90\x8d\xe7\x8e\xa9\xe5\xae\xb6\xe7\x9a\x84\xe5\xa5\xbd\xe6\x84\x9f\xe5\xba\xa6\xef\xbc\x88\xe6\xb0\xb8\xe4\xb9\x85\xef\xbc\x89
        :return:
        """
        gamelog.info('jbx:onQueryTopPFriendlyWithLvNF', npcPId, data)
        friendList = []
        for lv, info in data:
            for gbId, detailInfo in info.iteritems():
                detailInfo = list(detailInfo)
                if len(detailInfo) == 5:
                    detailInfo.append(0)
                if len(detailInfo) == 6:
                    pfVal, name, sex, school, borderId, timeStamp = detailInfo
                    photo = ''
                else:
                    pfVal, name, sex, school, borderId, photo, timeStamp = detailInfo
                newVal = NpcFriendVal(lv, gbId, pfVal, name, sex, school, borderId, timeStamp, photo)
                friendList.append(newVal)

        self.npcFavor.topFriend[npcPId] = friendList
        gameglobal.rds.ui.npcInteractive.refreshInfo()
        gameglobal.rds.ui.npcRelationshipHaogan.refreshInfo()

    def doActionNF(self, npcId, likeId, sumVal):
        """
        :param npcId:
        :param likeId:
        :param sumVal:
        :return:
        """
        gamelog.info('jbx:doActionNF', npcId, likeId, sumVal)
        cfgNames = ('nfLikeGiftHateAction', 'nfLikeGiftNotLikeAction', 'nfLikeGiftLikeAction', 'nfLikeGiftLoveAction')
        self.playNpcFavorSound(npcId, sumVal)
        for cfgName in cfgNames:
            actions = NND.data.get(commNpcFavor.getNpcPId(npcId), {}).get(cfgName, ())
            for minVal, maxVal, actionId in actions:
                if minVal <= sumVal <= maxVal:
                    gameglobal.rds.ui.npcInteractive.doAction(npcId, actionId)
                    return

    def playNpcFavorSound(self, npcId, sumVal):
        favorSounds = NND.data.get(commNpcFavor.getNpcPId(npcId), {}).get('favorSounds', ())
        for minVal, maxVal, actionId in favorSounds:
            if minVal <= sumVal <= maxVal:
                gameglobal.rds.sound.playSound(actionId)
                return

    def showChatMsgNF(self, npcId, msgId, args):
        """
        :param npcId:
        :param msgId:
        :param args: (a,b,c,...)
        :return:
        """
        gamelog.info('jbx:showChatMsgNF', npcId, msgId, args)
        if msgId == GMDD.data.NF_ASK_ITEM_SUCCESS:
            self.showGameMsg(msgId, args)
            return
        content = GMD.data.get(msgId, {}).get('text', '') % args
        npcPId = commNpcFavor.getNpcPId(npcId)
        self.npcFavor.sendNpcFriendTmpMsg(npcPId, content)
        self.chatDB.saveNpcMsg(self.gbId, npcPId, content, utils.getNow())

    def showAddContactNF(self, npcPId):
        """
        :param npcPId:
        :return:
        """
        gamelog.info('jbx:showAddContactNF', npcPId)
        if npcPId not in self.npcFavor.npcRequest and not self.friend.has_key(npcPId):
            self.npcFavor.npcRequest.append(npcPId)
            gameglobal.rds.ui.friendRequest.show()

    def onAcceptQuestNF(self, questId):
        """
        :param questId: \xe6\x8e\xa5\xe5\x8f\x96\xe7\x9a\x84\xe4\xbb\xbb\xe5\x8a\xa1Id
        :return:
        """
        self.npcFavor.todayFavor[1] = questId

    def onReceiveGiftNF(self, npcPId, receiveGiftFlag):
        """
        :param npcPId: int npc\xe7\x88\xb6id
        :param receiveGiftFlag: int \xe5\xb7\xb2\xe9\xa2\x86\xe5\x8f\x96\xe6\xa0\x87\xe5\xbf\x97
        :return:
        """
        gamelog.info('jbx:onReceiveGiftNF', npcPId, receiveGiftFlag)
        self.npcFavor.dailyGiftRecord[npcPId] = receiveGiftFlag

    def onActorRoleNF(self, npcPId, actorRoleFlag):
        """
        :param npcPId: int npc\xe7\x88\xb6id
        :param actorRoleFlag: int \xe5\xb7\xb2\xe6\x89\xae\xe6\xbc\x94\xe6\xa0\x87\xe5\xbf\x97
        :return:
        """
        gamelog.info('jbx:onActorRoleNF', npcPId, actorRoleFlag)
        self.npcFavor.cosRecord[npcPId] = actorRoleFlag
        gameglobal.rds.ui.cosNpc.hide()

    def onAcceptDailyQuestLoopNF(self, npcPId, questLoopId, questType):
        """
        :param npcPId: int npc\xe7\x88\xb6id
        :param questLoopId: int \xe5\xbe\xaa\xe7\x8e\xaf\xe4\xbb\xbb\xe5\x8a\xa1id
        :return:
        """
        gamelog.info('jbx:onAcceptDailyQuestLoopNF', npcPId, questLoopId, questType)
        if questType == gametypes.NF_QUESTLOOP_DAILY:
            self.npcFavor.dailyQuestRecord[npcPId] = questLoopId
        elif questType == gametypes.NF_QUESTLOOP_WEEKLY:
            self.npcFavor.weeklyQuestRecord[npcPId] = questLoopId
        elif questType == gametypes.NF_QUESTLOOP_MONTHLY:
            self.npcFavor.monthlyQuestRecord[npcPId] = questLoopId

    def onAcceptDailyQuestNF(self, npcPId, questId, flag):
        """
        :param npcPId: int npc\xe7\x88\xb6id
        :param questId: int \xe4\xbb\xbb\xe5\x8a\xa1id
        :param flag: int \xe4\xbb\xbb\xe5\x8a\xa1\xe7\x8a\xb6\xe6\x80\x81\xef\xbc\x8ccommNpcFavor.NF_DAILY_QUEST_STAT_RECEIVE
        :return:
        """
        gamelog.info('jbx:onAcceptDailyQuestNF', npcPId, questId)
        self.npcFavor.questRecord[npcPId] = (questId, flag)

    def onAddPFriendlyNF(self, pfData, wfData, hfdata):
        """
        :param pfData: dict {npcPId : pfVal, ...}
        :param wfData: dict {npcPId : wfVal, ...}
        :param hfdata: dict {npcPId : hfVal, ...}
        :return:
        """
        gamelog.info('jbx:onAddPFriendlyNF', pfData)
        for npcPId, pFVal in pfData.iteritems():
            diffVal = pFVal - self.npcFavor.npcFavorValue.get(npcPId, 0)
            self.onNpcFavorVarChange(npcPId, pFVal)
            if diffVal > 0:
                name = gameStrings.NPF_FAVOR % NND.data.get(npcPId, {}).get('name', '')
                gameglobal.rds.ui.showDefaultLabel(name, diffVal, '#47E036')

        for npcPId, nfHeartBeatValue in hfdata.iteritems():
            self.npcFavor.nfWHeartBeat[npcPId] = nfHeartBeatValue

        gameglobal.rds.ui.npcInteractive.refreshInfo()

    def onInteractiveNF(self, iteractiveFlag):
        """
        :param iteractiveFlag: dict {npcPId: flag, ...}
        :return:
        """
        gamelog.info('jbx:iteractiveFlag', iteractiveFlag)
        self.npcFavor.interactiveRecord.update(iteractiveFlag)

    def onSyncPFriendlyOneNF(self, npcPId, pfVal):
        """
        :param npcPId:
        :param pfVal:
        :return:
        """
        self.onNpcFavorVarChange(npcPId, pfVal)

    def onSyncWFriendlyOneNF(self, npcPId, wfVal):
        """
        :param npcPId:
        :param wfVal:
        :return:
        """
        self.npcFavor.npcFavorValueWeekly[npcPId] = wfVal

    def onSyncDFriendlyOneNF(self, npcPId, dfVal):
        """
        :param npcPId:
        :param dfVal:
        :return:
        """
        self.npcFavor.npcFavorValueDaily[npcPId] = dfVal

    def onSyncWHeartBeatOneNF(self, npcPId, dfVal):
        """
        :param npcPId:
        :param dfVal:
        :return:
        """
        gamelog.info('jbx:onSyncWHeartBeatOneNF', npcPId, dfVal)
        self.npcFavor.nfWHeartBeat[npcPId] = dfVal
        gameglobal.rds.ui.npcInteractive.refreshInfo()
