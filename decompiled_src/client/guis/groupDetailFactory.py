#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/groupDetailFactory.o
from gamestrings import gameStrings
import BigWorld
import utils
import formula
import uiConst
import const
import gamelog
import gametypes
import uiUtils
import gameglobal
import copy
from gameclass import Singleton
from gamestrings import gameStrings
from data import fb_data as FD
from cdata import mapSearch_iii_data as MID
from data import group_goal_data as GGD
from data import arena_mode_data as AMD
from cdata import group_fb_menu_data as GFMD
from cdata import game_msg_def_data as GMDD
from data import group_label_data as GLD
from data import sys_config_data as SCD
GOAL_TYPE_DESEC = {const.GROUP_GOAL_DEFAULT: gameStrings.TEXT_GROUPDETAILFACTORY_27,
 const.GROUP_GOAL_FB: gameStrings.TEXT_GROUPDETAILFACTORY_28,
 const.GROUP_GOAL_DUEL: 'PVP',
 const.GROUP_GOAL_QUEST: gameStrings.TEXT_GROUPDETAILFACTORY_30,
 const.GROUP_GOAL_RELAXATION: gameStrings.TEXT_GROUPDETAILFACTORY_31,
 const.GROUP_HOT_TAGS: gameStrings.TEXT_GROUPDETAILFACTORY_32,
 const.GROUP_GOAL_GUILD_FB: gameStrings.TEXT_GROUPDETAILFACTORY_33}

class ActAvlData(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.reset()
        self.refresh()

    def reset(self):
        self.actAvlData = {}
        self.actTypeData = {}

    def refresh(self):
        p = BigWorld.player()
        if p == None:
            return
        elif not getattr(p, 'IsAvatar', False):
            return
        else:
            groupActType = SCD.data.get('groupActivityType', {})
            if not self.actTypeData:
                actTypeData = {}
                for tid in groupActType.keys():
                    actTypeData[tid] = []

                for key, val in GLD.data.items():
                    type = val.get('type', 0)
                    if type not in groupActType.keys():
                        continue
                    actTypeData[type].append(key)

                for type, li in actTypeData.items():
                    actTypeData[type].sort(key=lambda x: GLD.data.get(x, {}).get('order', 0), reverse=True)

                self.actTypeData = actTypeData
            self.actAvlData = self.avlFilter(self.actTypeData)
            return

    def avlFilter(self, data):
        tData = copy.deepcopy(data)
        gldd = GLD.data
        for type, typeList in data.iteritems():
            tmpList = tData.get(type, [])
            for key in typeList:
                item = gldd.get(key, {})
                if not self.checkAvailable(item):
                    tmpList.remove(key)

        return tData

    def checkAvailable(self, item):
        p = BigWorld.player()
        if item.get('lv'):
            minlv, maxlv = item['lv']
            if p.lv < minlv or p.lv > maxlv:
                return False
        weekSet = item.get('weekSet', 0)
        timeStart = item.get('timeStart')
        timeEnd = item.get('timeEnd')
        if timeStart and timeEnd:
            if not utils.inCrontabRange(timeStart, timeEnd, weekSet=weekSet):
                return False
        return True


def getActAvlInstance():
    return ActAvlData.getInstance()


def getActAvlData():
    if not getActAvlInstance().actAvlData:
        getActAvlInstance().refresh()
    return ActAvlData.getInstance().actAvlData


class IGroupInfo(object):

    def __init__(self, details):
        self.details = self.preProcessDetails(details)
        self.firstMenuIndex = -1
        self.secondMenuIndex = -1
        self.thirdMenuIndex = -1
        self.dropDownMenuInfo = []

    def getGoalTypeInfos(self):
        info = []
        cnt = 0
        for item in self.details:
            item['cnt'] = cnt
            info.append(item)
            cnt += 1

        return info

    def preProcessDetails(self, details):
        for item in details:
            item['goalDesc'] = self.getTeamGoalDesc(item['firstKey'], item['secondKey'], item['thirdKey'])
            for mVal in item['memInfo']:
                if mVal['school'] not in const.SCHOOL_SET:
                    continue
                mVal['schoolFrame'] = uiConst.SCHOOL_FRAME_DESC[mVal['school']]
                mVal['schoolName'] = const.SCHOOL_DICT[mVal['school']]

        details.sort(lambda x, y: cmp(y['buildTime'], x['buildTime']))
        return details

    def resetDropDownMenuInfo(self):
        self.firstDDMenuIndex = -1
        self.secondDDMenuIndex = -1
        self.thirdDDMenuIndex = -1
        self.dropDownMenuInfo = []

    def groupMatchBtnVisiable(self):
        return False

    def filterDetails(self):
        info = []
        for item in self.details:
            if item['teamGoal'] == self.goal:
                info.append(item)

        self.details = info

    def setFilterKey(self, fMenuIndex, sMenuIndex):
        self.firstMenuIndex = fMenuIndex
        self.secondMenuIndex = sMenuIndex

    def setDropDownMenuIndex(self, fDDMenuIndex, sDDMenuIndex, tDDMenuIndex):
        self.firstDDMenuIndex = fDDMenuIndex
        self.secondDDMenuIndex = sDDMenuIndex
        self.thirdDDMenuIndex = tDDMenuIndex

    def resetDetailByType(self, details):
        self.details = self.preProcessDetails(details)

    def getFirstVal(self):
        if self.firstMenuIndex == -1:
            gamelog.error('@hjx IGroupInfo#getFirstVal error: self.firstMenuIndex == -1')
            return None
        elif self.firstMenuIndex >= len(self.menuInfo):
            gamelog.error('@hjx IGroupInfo#getFirstVal error: self.firstMenuIndex >= len(self.menuInfo)')
            return None
        else:
            return self.menuInfo[self.firstMenuIndex]['key']

    def getSecondVal(self):
        if self.secondMenuIndex == -1:
            gamelog.error('@hjx IGroupInfo#getSecondVal error: self.secondMenuIndex == -1')
            return None
        elif self.secondMenuIndex >= len(self.menuInfo[self.firstMenuIndex]['data']):
            gamelog.error('@hjx IGroupInfo#getSecondVal error: self.secondMenuIndex >= len(self.menuInfo[self.firstMenuIndex][data]')
            return None
        else:
            return self.menuInfo[self.firstMenuIndex]['data'][self.secondMenuIndex]['key']

    def getMenuInfo(self):
        menuInfo = []
        self.reset()
        for key, val in GGD.data.iteritems():
            if val['gType'] != self.goal:
                continue
            menuInfo.append({'key': key[0],
             'keyName': val['name'],
             'data': []})

        self.menuInfo = menuInfo
        return self.menuInfo

    def getTeamDetailInfo(self):
        info = []
        firstKey = self.getFirstVal()
        if firstKey is None:
            return []
        else:
            cnt = 0
            for item in self.details:
                if item['firstKey'] != firstKey:
                    continue
                item['cnt'] = cnt
                info.append(item)
                cnt += 1

            return info

    def dropMenuVal2Index(self):
        p = BigWorld.player()
        firstKey = p.detailInfo['firstKey']
        fDropMenuIndex = 0
        sDropMenuIndex = -1
        tDropMenuIndex = -1
        for fIndex, fVal in enumerate(self.dropDownMenuInfo):
            if fVal['key'] == firstKey:
                fDropMenuIndex = fIndex

        return [fDropMenuIndex, sDropMenuIndex, tDropMenuIndex]

    def getTeamItemDetail(self, index):
        if index == -1 or index >= len(self.details):
            return None
        else:
            return self.details[index]

    def getDefaultFirstKey(self):
        if len(self.menuInfo) > 0:
            return self.dropDownMenuInfo[0]['key']
        else:
            return const.DEFAULT_GROUP_FIRST_KEY

    def getDefaultSecondKey(self):
        return const.DEFAULT_GROUP_SECOND_KEY

    def getDefaultThirdKey(self):
        return const.DEFAULT_GROUP_THIRD_KEY

    def getDropDownMenuInfo(self):
        dropDownMenuInfo = [{'key': 0,
          'keyName': gameStrings.TEXT_GROUPDETAILFACTORY_264,
          'data': []}]
        self.resetDropDownMenuInfo()
        for key, val in GGD.data.iteritems():
            if val['gType'] != self.goal:
                continue
            dropDownMenuInfo.append({'key': key[0],
             'keyName': val['name'],
             'data': []})

        self.dropDownMenuInfo = dropDownMenuInfo
        return self.dropDownMenuInfo

    def getCreateTeamKeys(self, fKeyIndex, sKeyIndex, tKeyIndex):
        keys = []
        if fKeyIndex == -1 or fKeyIndex >= len(self.dropDownMenuInfo):
            return [self.getDefaultFirstKey(), self.getDefaultSecondKey(), self.getDefaultThirdKey()]
        keys.append(self.dropDownMenuInfo[fKeyIndex]['key'])
        if sKeyIndex == -1 or sKeyIndex >= len(self.dropDownMenuInfo[fKeyIndex]['data']):
            keys.extend([self.getDefaultSecondKey(), self.getDefaultThirdKey()])
            return keys
        keys.append(self.dropDownMenuInfo[fKeyIndex]['data'][sKeyIndex]['key'])
        if tKeyIndex == -1 or tKeyIndex >= len(self.dropDownMenuInfo[fKeyIndex]['data'][sKeyIndex]['data']):
            keys.append(self.getDefaultThirdKey())
            return keys
        keys.append(self.dropDownMenuInfo[fKeyIndex]['data'][sKeyIndex]['data'][tKeyIndex]['key'])
        gamelog.debug('@hjx social#getCreateTeamKeys:', keys)
        return keys


class AreaGroupInfo(IGroupInfo):

    def __init__(self, details):
        super(AreaGroupInfo, self).__init__(details)
        self.goal = const.GROUP_GOAL_DEFAULT
        self.filterDetails()

    def isPlayerTeam(self, item):
        p = BigWorld.player()
        if not p.isInTeamOrGroup():
            return False
        for val in item['memInfo']:
            if val['roleName'] == p.realRoleName:
                return True

        return False

    def isPlayerNeighbor(self, item):
        p = BigWorld.player()
        if item['firstKey'] == p.mapAreaId:
            return True
        else:
            return False

    def getDefaultSecondKey(self):
        return BigWorld.player().spaceNo

    def isInSameDiGong(self, item):
        p = BigWorld.player()
        mlgNo = formula.getMLGNo(p.spaceNo)
        if not formula.inMultiLine(mlgNo):
            return False
        else:
            secondKey = item.get('secondKey', 0)
            if secondKey and secondKey == p.spaceNo:
                return True
            return False

    def preProcessDetails(self, details):
        for item in details:
            item['goalDesc'] = self.getTeamGoalDesc(item['firstKey'], item['secondKey'], item['thirdKey'])
            if self.isPlayerTeam(item):
                item['sortId'] = 1
            elif self.isPlayerNeighbor(item):
                item['sortId'] = 2
            else:
                item['sortId'] = 3
            for mVal in item['memInfo']:
                if mVal['school'] not in const.SCHOOL_SET:
                    continue
                mVal['schoolFrame'] = uiConst.SCHOOL_FRAME_DESC[mVal['school']]
                mVal['schoolName'] = const.SCHOOL_DICT[mVal['school']]

        details.sort(lambda x, y: cmp(y['buildTime'], x['buildTime']))
        return details

    def getTeamGoalDesc(self, firstKey, secondKey, thirdKey):
        try:
            desc = MID.data[firstKey]['mapName_iii']
        except:
            desc = ''

        return desc

    def getMenuInfo(self):
        return []

    def resetDetailByType(self, details):
        super(AreaGroupInfo, self).resetDetailByType(details)
        self.firstMenuIndex = 0

    def getTeamDetailInfo(self):
        info = []
        cnt = 0
        for item in sorted(self.details, key=lambda detail: detail['sortId']):
            item['cnt'] = cnt
            info.append(item)
            cnt += 1

        return info


class FbGroupInfo(IGroupInfo):

    def __init__(self, details):
        super(FbGroupInfo, self).__init__(details)
        self.goal = const.GROUP_GOAL_FB
        self.reset()
        self.filterDetails()

    def reset(self):
        self.firstMenuIndex = -1
        self.secondMenuIndex = -1
        self.thirdMenuIndex = -1
        self.menuInfo = []

    def getTeamGoalDesc(self, firstKey, secondKey, thirdKey):
        try:
            desc = uiUtils.getFbGroupDesc(firstKey, secondKey, thirdKey)
        except:
            desc = ''

        return desc

    def getDropDownMenuInfo(self):
        dropDownMenuInfo = [{'key': 0,
          'keyName': gameStrings.TEXT_GROUPDETAILFACTORY_264,
          'data': []}]
        self.resetDropDownMenuInfo()
        for key, val in GFMD.data.iteritems():
            sList = [{'key': 0,
              'keyName': gameStrings.TEXT_ACTIVITYFACTORY_107,
              'data': []}]
            for sKey, sVal in val.iteritems():
                fbNo = 0
                tList = [{'key': const.GROUP_MATCH_FB_SECOND_LEVEL_MODE_ALL,
                  'keyName': gameStrings.TEXT_ACTIVITYFACTORY_107,
                  'data': []}]
                for tKey, tVal in sVal.iteritems():
                    fbNo = tVal['fbNo']
                    if uiUtils.checkFbGroupMatchCondition(tVal['fbNo']):
                        tList.append({'key': tKey,
                         'keyName': FD.data[fbNo]['modeName'],
                         'data': []})

                pFbNo = GFMD.data[key][sKey].values()[0]['fbNo']
                if len(tList) > 1:
                    sList.append({'key': sKey,
                     'keyName': FD.data[pFbNo]['primaryLevelName'],
                     'data': tList})

            if len(sList) > 1:
                dropDownMenuInfo.append({'key': key,
                 'keyName': uiUtils.getFbGroupName(key),
                 'data': sList})

        self.dropDownMenuInfo = dropDownMenuInfo
        return self.dropDownMenuInfo

    def getMenuInfo(self):
        menuInfo = []
        self.reset()
        for key, val in GFMD.data.iteritems():
            sList = []
            lvMin = 9999
            for sKey, sVal in val.iteritems():
                fbNo = 0
                tList = []
                isValid = False
                for tKey, tVal in sVal.iteritems():
                    fbNo = tVal['fbNo']
                    if uiUtils.checkFbGroupMatchCondition(tVal['fbNo']):
                        isValid = True
                        tList.append({'key': tKey,
                         'keyName': FD.data[fbNo]['modeName'],
                         'data': []})
                        if lvMin > FD.data[fbNo]['lvMin']:
                            lvMin = FD.data[fbNo]['lvMin']

                if isValid:
                    pFbNo = GFMD.data[key][sKey].values()[0]['fbNo']
                    sList.append({'key': sKey,
                     'keyName': FD.data[pFbNo]['primaryLevelName'],
                     'data': tList})

            if sList:
                menuInfo.append({'key': key,
                 'keyName': uiUtils.getFbGroupName(key),
                 'data': sList,
                 'lvMin': lvMin})

        menuInfo.sort(lambda x, y: cmp(x['lvMin'], y['lvMin']))
        self.menuInfo = menuInfo
        return self.menuInfo

    def getTeamDetailInfo(self):
        info = []
        firstKey = self.getFirstVal()
        secondKey = self.getSecondVal()
        if firstKey is None:
            return []
        else:
            cnt = 0
            for item in self.details:
                if item['firstKey'] != firstKey:
                    continue
                if item['secondKey'] != 0 and secondKey != None and item['secondKey'] != secondKey:
                    continue
                item['cnt'] = cnt
                info.append(item)
                cnt += 1

            return info

    def applyGroupMatch(self):
        fKey = self.getFirstVal()
        if not fKey:
            return
        else:
            sKey = self.getSecondVal()
            if sKey is None:
                fbNo = GFMD.data[fKey].values()[0].values()[0]['fbNo']
            else:
                fbNo = GFMD.data[fKey][sKey].values()[0]['fbNo']
            gameglobal.rds.ui.fubenLogin.selectedFb = fbNo
            gameglobal.rds.ui.fubenLogin.showFbGroupMatch()
            return

    def dropMenuVal2Index(self):
        p = BigWorld.player()
        firstKey = p.detailInfo['firstKey']
        secondKey = p.detailInfo['secondKey']
        thirdKey = p.detailInfo['thirdKey']
        fDropMenuIndex = 0
        sDropMenuIndex = -1
        tDropMenuIndex = -1
        for fIndex, fVal in enumerate(self.dropDownMenuInfo):
            if fVal['key'] == firstKey:
                fDropMenuIndex = fIndex
                for sIndex, sVal in enumerate(fVal['data']):
                    if sVal['key'] == secondKey:
                        sDropMenuIndex = sIndex
                        for tIndex, tVal in enumerate(sVal['data']):
                            if tVal['key'] == thirdKey:
                                tDropMenuIndex = tIndex
                                return [fDropMenuIndex, sDropMenuIndex, tDropMenuIndex]

        return [fDropMenuIndex, sDropMenuIndex, tDropMenuIndex]

    def getDefaultSecondKey(self):
        if len(self.dropDownMenuInfo) == 0:
            return const.DEFAULT_GROUP_SECOND_KEY
        if self.firstDDMenuIndex >= len(self.dropDownMenuInfo) or len(self.dropDownMenuInfo[self.firstDDMenuIndex]['data']) == 0:
            return const.DEFAULT_GROUP_SECOND_KEY
        return self.dropDownMenuInfo[self.firstDDMenuIndex]['data'][0]['key']

    def getDefaultThirdKey(self):
        return const.GROUP_MATCH_FB_SECOND_LEVEL_MODE_ALL


class DuelGroupInfo(IGroupInfo):

    def __init__(self, details):
        super(DuelGroupInfo, self).__init__(details)
        self.goal = const.GROUP_GOAL_DUEL
        self.reset()
        self.filterDetails()

    def reset(self):
        self.firstMenuIndex = 0
        self.secondMenuIndex = 0
        self.menuInfo = []

    def getTeamGoalDesc(self, firstKey, secondKey, thirdKey):
        try:
            if firstKey == 0 or secondKey == 0:
                desc = ''
            else:
                desc = gameStrings.TEXT_GROUPDETAILFACTORY_582 + AMD.data[secondKey]['name']
        except:
            desc = ''

        return desc

    def getDropDownMenuInfo(self):
        dropDownMenuInfo = [{'key': 0,
          'keyName': gameStrings.TEXT_GROUPDETAILFACTORY_264,
          'data': []}]
        self.resetDropDownMenuInfo()
        p = BigWorld.player()
        duelInfo = [{'key': 1,
          'keyName': gameStrings.TEXT_FRIENDPROXY_1225,
          'data': AMD.data}]
        for val in duelInfo:
            sList = [{'key': 0,
              'keyName': gameStrings.TEXT_ACTIVITYFACTORY_107,
              'data': []}]
            for sKey, sVal in sorted(val['data'].iteritems(), reverse=True):
                if not sVal.get('isEnableGroup', 0):
                    continue
                if formula.getArenaLvTag(sKey, p.lv) != -1:
                    sList.append({'key': sKey,
                     'keyName': sVal['name'],
                     'data': []})

            if len(sList) > 1:
                dropDownMenuInfo.append({'key': val['key'],
                 'keyName': val['keyName'],
                 'data': sList})

        self.dropDownMenuInfo = dropDownMenuInfo
        return self.dropDownMenuInfo

    def getMenuInfo(self):
        menuInfo = []
        self.reset()
        p = BigWorld.player()
        duelInfo = [{'key': 1,
          'keyName': gameStrings.TEXT_FRIENDPROXY_1225,
          'data': AMD.data}]
        for val in duelInfo:
            sList = []
            for sKey, sVal in sorted(val['data'].iteritems(), reverse=True):
                if not sVal.get('isEnableGroup', 0):
                    continue
                if formula.getArenaLvTag(sKey, p.lv) != -1:
                    sList.append({'key': sKey,
                     'keyName': sVal['name'],
                     'data': []})

            if len(sList) > 0:
                menuInfo.append({'key': val['key'],
                 'keyName': val['keyName'],
                 'data': sList})

        self.menuInfo = menuInfo
        return self.menuInfo

    def getTeamDetailInfo(self):
        info = []
        firstKey = self.getFirstVal()
        secondKey = self.getSecondVal()
        if firstKey is None:
            return []
        else:
            cnt = 0
            for item in self.details:
                if item['firstKey'] != 0:
                    if item['firstKey'] != firstKey:
                        continue
                    if item['secondKey'] != 0 and secondKey != None and item['secondKey'] != secondKey:
                        continue
                item['cnt'] = cnt
                info.append(item)
                cnt += 1

            return info

    def dropMenuVal2Index(self):
        p = BigWorld.player()
        firstKey = p.detailInfo['firstKey']
        secondKey = p.detailInfo['secondKey']
        fDropMenuIndex = 0
        sDropMenuIndex = -1
        tDropMenuIndex = -1
        for fIndex, fVal in enumerate(self.dropDownMenuInfo):
            if fVal['key'] == firstKey:
                fDropMenuIndex = fIndex
                for sIndex, sVal in enumerate(fVal['data']):
                    if sVal['key'] == secondKey:
                        sDropMenuIndex = sIndex
                        return [fDropMenuIndex, sDropMenuIndex, tDropMenuIndex]

        return [fDropMenuIndex, sDropMenuIndex, tDropMenuIndex]


class QuestGroupInfo(IGroupInfo):

    def __init__(self, details):
        super(QuestGroupInfo, self).__init__(details)
        self.goal = const.GROUP_GOAL_QUEST
        self.reset()
        self.filterDetails()

    def reset(self):
        self.firstMenuIndex = -1
        self.menuInfo = []

    def getTeamGoalDesc(self, firstKey, secondKey, thirdKey):
        try:
            desc = GGD.data[firstKey, self.goal]['name']
        except:
            desc = ''

        return desc


class HotGroupInfo(IGroupInfo):

    def __init__(self, details):
        super(HotGroupInfo, self).__init__(details)
        self.goal = const.GROUP_HOT_TAGS
        self.reset()
        self.filterDetails()

    def refreshHotTagItems(self):
        tagList = set()
        for key, value in GLD.data.iteritems():
            if ActAvlData.getInstance().checkAvailable(value) and value.get('hot', 0):
                tagList.add(key)

        self.hotTagItems = list(tagList)
        self.hotTagItems.sort(key=lambda x: GLD.data.get(x, {}).get('order', 0), reverse=True)

    def reset(self):
        self.hotTagItems = set()

    def getMenuInfo(self):
        self.reset()
        self.refreshHotTagItems()
        dataList = []
        for key in self.hotTagItems:
            info = {}
            value = GLD.data.get(key, {})
            info['key'] = key
            info['keyName'] = value.get('name', '')
            info['data'] = []
            dataList.append(info)

        self.menuInfo = dataList
        return self.menuInfo

    def setFilterKey(self, fMenuIndex, sMenuIndex):
        if fMenuIndex >= 0:
            key = self.hotTagItems[fMenuIndex]
            value = GLD.data.get(key, {})
            self.firstMenuIndex = value.get('type', 0)
            self.secondMenuIndex = key

    def getTeamDetailInfo(self):
        info = []
        firstKey = self.firstMenuIndex
        secondKey = self.secondMenuIndex
        if firstKey is None:
            return []
        else:
            cnt = 0
            for item in self.details:
                if item['firstKey'] != 0:
                    if item['firstKey'] != firstKey:
                        continue
                    if item['secondKey'] != 0 and secondKey != None and item['secondKey'] != secondKey:
                        continue
                item['cnt'] = cnt
                info.append(item)
                cnt += 1

            return info

    def getTeamGoalDesc(self, firstKey, secondKey, thirdKey):
        if firstKey == 0:
            return ''
        firstDes = ''
        secondDes = ''
        fdesRef = {1: gameStrings.TEXT_GROUPDETAILFACTORY_769,
         2: gameStrings.TEXT_GROUPDETAILFACTORY_769_1,
         3: gameStrings.TEXT_GROUPDETAILFACTORY_769_2}
        firstDes = fdesRef[firstKey]
        secondDes = GLD.data.get(secondKey, {}).get('name', '')
        return '%s-%s' % (firstDes, secondDes)

    def resetDetailByType(self, details):
        filterDetails = []
        for item in details:
            secondKey = item.get('secondKey', -1)
            if secondKey in self.hotTagItems:
                filterDetails.append(item)

        super(self.__class__, self).resetDetailByType(filterDetails)


class RelaxationGroupInfo(IGroupInfo):

    def __init__(self, details):
        super(RelaxationGroupInfo, self).__init__(details)
        self.goal = const.GROUP_GOAL_RELAXATION
        self.reset()
        self.filterDetails()

    def reset(self):
        self.firstMenuIndex = 0
        self.menuInfo = []

    def getTeamGoalDesc(self, firstKey, secondKey, thirdKey):
        groupActType = SCD.data.get('groupActivityType', {})
        gldd = GLD.data
        try:
            desc = groupActType.get(firstKey) + '-' + gldd.get(secondKey)['name']
        except:
            desc = ''

        return desc

    def getDropDownMenuInfo(self):
        groupActType = SCD.data.get('groupActivityType', {})
        gldd = GLD.data
        dropDownMenuInfo = [{'key': 0,
          'keyName': gameStrings.TEXT_GROUPDETAILFACTORY_264,
          'data': []}]
        self.resetDropDownMenuInfo()
        p = BigWorld.player()
        for key, val in getActAvlData().items():
            sList = [{'key': 0,
              'keyName': gameStrings.TEXT_ACTIVITYFACTORY_107,
              'data': []}]
            for sKey in val:
                sList.append({'key': sKey,
                 'keyName': gldd.get(sKey, {}).get('name', ''),
                 'data': []})

            if len(sList) > 0:
                dropDownMenuInfo.append({'key': key,
                 'keyName': groupActType.get(key, ''),
                 'data': sList})

        self.dropDownMenuInfo = dropDownMenuInfo
        return self.dropDownMenuInfo

    def getMenuInfo(self):
        menuInfo = []
        self.reset()
        p = BigWorld.player()
        groupActType = SCD.data.get('groupActivityType', {})
        gldd = GLD.data
        for key, val in getActAvlData().items():
            sList = [{'key': 0,
              'keyName': gameStrings.TEXT_ACTIVITYFACTORY_107,
              'data': []}]
            for sKey in val:
                sList.append({'key': sKey,
                 'keyName': gldd.get(sKey, {}).get('name', ''),
                 'data': []})

            menuInfo.append({'key': key,
             'keyName': groupActType.get(key, ''),
             'data': sList})

        self.menuInfo = menuInfo
        return self.menuInfo

    def dropMenuVal2Index(self):
        p = BigWorld.player()
        firstKey = p.detailInfo['firstKey']
        secondKey = p.detailInfo['secondKey']
        fDropMenuIndex = 0
        sDropMenuIndex = -1
        tDropMenuIndex = -1
        for fIndex, fVal in enumerate(self.dropDownMenuInfo):
            if fVal['key'] == firstKey:
                fDropMenuIndex = fIndex
                for sIndex, sVal in enumerate(fVal['data']):
                    if sVal['key'] == secondKey:
                        sDropMenuIndex = sIndex
                        return [fDropMenuIndex, sDropMenuIndex, tDropMenuIndex]

        return [fDropMenuIndex, sDropMenuIndex, tDropMenuIndex]

    def getTeamDetailInfo(self):
        info = []
        firstKey = self.getFirstVal()
        secondKey = self.getSecondVal()
        if firstKey is None:
            return []
        else:
            cnt = 0
            for item in self.details:
                if item['firstKey'] != 0:
                    if item['firstKey'] != firstKey:
                        continue
                    if item['secondKey'] != 0 and secondKey != None and item['secondKey'] != secondKey:
                        continue
                item['cnt'] = cnt
                info.append(item)
                cnt += 1

            return info


class GuildFubenGroupInfo(IGroupInfo):

    def __init__(self, details):
        super(GuildFubenGroupInfo, self).__init__(details)
        self.goal = const.GROUP_GOAL_GUILD_FB
        self.reset()
        self.filterDetails()

    def reset(self):
        self.firstMenuIndex = -1
        self.menuInfo = []

    def getTeamGoalDesc(self, firstKey, secondKey, thirdKey):
        try:
            desc = gameStrings.TEXT_GROUPDETAILFACTORY_33 + str(firstKey)
        except:
            desc = ''

        return desc


class GroupDetailFactory(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.curGoal = const.GROUP_HOT_TAGS
        self.goalList = [const.GROUP_HOT_TAGS,
         const.GROUP_GOAL_FB,
         const.GROUP_GOAL_DUEL,
         const.GROUP_GOAL_RELAXATION,
         const.GROUP_GOAL_DEFAULT,
         const.GROUP_GOAL_GUILD_FB]
        self.goalIns = {}
        self.reset()

    def __createIns(self, gType, details):
        if gType == const.GROUP_GOAL_DEFAULT or gType == const.GROUP_GOAL_WW_RAW or gType == const.GROUP_GOAL_WW_SOUL:
            return AreaGroupInfo(details)
        elif gType == const.GROUP_GOAL_FB:
            return FbGroupInfo(details)
        elif gType == const.GROUP_GOAL_DUEL:
            return DuelGroupInfo(details)
        elif gType == const.GROUP_GOAL_QUEST:
            return QuestGroupInfo(details)
        elif gType == const.GROUP_GOAL_RELAXATION:
            return RelaxationGroupInfo(details)
        elif gType == const.GROUP_HOT_TAGS:
            return HotGroupInfo(details)
        elif gType == const.GROUP_GOAL_GUILD_FB:
            return GuildFubenGroupInfo(details)
        else:
            return None

    def applyGroupInDiGong(self, info):
        p = BigWorld.player()
        if p.groupNUID > 0:
            p.showGameMsg(GMDD.data.APPLY_GROUP_FAILED_ALREADY_IN_GROUP, ())
            return
        elif self.diGongIns is None:
            return
        else:
            self.resetDiGongTeamDetail(info)
            cnt = 0
            for item in self.diGongIns.details:
                if cnt >= const.AUTO_APPLY_GROUP_MAX_NUM:
                    break
                if item.get('teamGoal', 0) != const.GROUP_GOAL_DEFAULT:
                    continue
                if item.get('groupType', 0) != gametypes.GROUP_TYPE_TEAM_GROUP:
                    continue
                if len(item.get('memInfo', [])) >= const.TEAM_MAX_NUMBER:
                    continue
                if not self.diGongIns.isInSameDiGong(item):
                    continue
                if p.lv < item['lvMin'] or p.lv > item['lvMax']:
                    continue
                if p.school not in item.get('schoolReq', []):
                    continue
                if item.get('teamHeader', '') == '':
                    continue
                p.cell.applyGroup(item['teamHeader'])
                cnt += 1

            if cnt > 0:
                self.isApplyJoining = True
            else:
                p.showGameMsg(GMDD.data.APPLY_QUICK_GROUP_FAILED_NO_TEAM, ())
            return

    def applyGroupInWorldWar(self, info):
        p = BigWorld.player()
        if p.groupNUID > 0:
            p.showGameMsg(GMDD.data.APPLY_GROUP_FAILED_ALREADY_IN_GROUP, ())
            return
        if not p.inWorldWar():
            return
        srcGoalType = utils.genWorldWarOnlyGroupGoalType(p)
        cnt = 0
        for item in info:
            if cnt >= const.AUTO_APPLY_GROUP_MAX_NUM:
                break
            if item.get('teamGoal', 0) != srcGoalType:
                continue
            if len(item.get('memInfo', [])) >= const.TEAM_MAX_NUMBER:
                continue
            if p.lv < item['lvMin'] or p.lv > item['lvMax']:
                continue
            if p.school not in item.get('schoolReq', []):
                continue
            if item.get('teamHeader', '') == '':
                continue
            if not utils.fromSameServerByName(p.roleName, item['teamHeader']):
                continue
            p.cell.applyGroup(item['teamHeader'])
            cnt += 1

        if cnt > 0:
            self.isApplyJoining = True
        else:
            p.showGameMsg(GMDD.data.APPLY_QUICK_GROUP_FAILED_NO_TEAM, ())

    def resetApplyJoining(self):
        self.diGongIns = AreaGroupInfo([])
        self.isApplyJoining = False

    def resetDiGongTeamDetail(self, details):
        if self.diGongIns is None:
            return
        else:
            self.diGongIns.resetDetailByType(details)
            return

    def addGroupDetailIns(self, key, val):
        pass

    def deleteGroupDetailIns(self, key):
        pass

    def reset(self):
        for gType in self.goalList:
            self.resetInsByType(gType, [])

        self.resetApplyJoining()

    def getLeftListMenuInfo(self):
        menuInfo = []
        for goalType in self.goalList:
            mData = self.goalIns[goalType].getMenuInfo()
            if goalType != const.GROUP_GOAL_DEFAULT and len(mData) == 0:
                continue
            menuInfo.append({'key': goalType,
             'keyName': GOAL_TYPE_DESEC[goalType],
             'data': mData})

        return uiUtils.array2GfxAarry(menuInfo, True)

    def resetInsByType(self, gType, details):
        self.goalIns.pop(gType, None)
        gIns = self.__createIns(gType, details)
        if gIns:
            self.goalIns[gType] = gIns
        else:
            gamelog.error('@hjx GroupDetailFactory#__createIns error: gIns is None!')

    def resetDetailByType(self, gType, details):
        if not self.goalIns.has_key(gType):
            return
        if gType == const.GROUP_GOAL_RELAXATION:
            self.goalIns[const.GROUP_HOT_TAGS].resetDetailByType(details)
        self.goalIns[gType].resetDetailByType(details)

    def getDropDownMenuInfo(self, goal):
        return uiUtils.array2GfxAarry(self.goalIns[goal].getDropDownMenuInfo(), True)

    def getDropDownMenuInfoV2(self, goal):
        return self.goalIns[goal].getDropDownMenuInfo()

    def getTeamDetailInfo(self, details):
        areaDetail = []
        fbDetail = []
        duelDetail = []
        questDetail = []
        relaxDetail = []
        for item in details:
            gType = item['teamGoal']
            if gType == const.GROUP_GOAL_DEFAULT or gType == const.GROUP_GOAL_WW_RAW or gType == const.GROUP_GOAL_WW_SOUL:
                areaDetail.append(item)
            elif gType == const.GROUP_GOAL_FB:
                fbDetail.append(item)
            elif gType == const.GROUP_GOAL_DUEL:
                duelDetail.append(item)
            elif gType == const.GROUP_GOAL_QUEST:
                questDetail.append(item)
            elif gType == const.GROUP_GOAL_RELAXATION:
                relaxDetail.append(item)

        self.resetDetailByType(const.GROUP_GOAL_DEFAULT, areaDetail)
        self.resetDetailByType(const.GROUP_GOAL_FB, fbDetail)
        self.resetDetailByType(const.GROUP_GOAL_DUEL, duelDetail)
        self.resetDetailByType(const.GROUP_GOAL_QUEST, questDetail)
        self.resetDetailByType(const.GROUP_GOAL_RELAXATION, relaxDetail)
        detailInfo = []
        cnt = 0
        for goalType, ins in self.goalIns.iteritems():
            if goalType == const.GROUP_HOT_TAGS:
                continue
            if ins.details:
                for item in ins.details:
                    item['cnt'] = cnt
                    cnt += 1

                detailInfo.extend(ins.details)

        return uiUtils.array2GfxAarry(detailInfo, True)

    def dropMenuVal2Index(self, goal):
        return self.goalIns[goal].dropMenuVal2Index()

    def getShareTeamInfoMsg(self, groupNUID = None):
        p = BigWorld.player()
        if hasattr(p, 'detailInfo') and p.detailInfo:
            msgName = uiUtils.getTextFromGMD(GMDD.data.TEAM_INVITE_MSG_TEAM_NAME, gameStrings.TEXT_GROUPDETAILFACTORY_1121)
            content = msgName % p.detailInfo['teamName']
        else:
            return ''
        leaderName = ''
        for memberGbId in p.members:
            if p.members[memberGbId]['isHeader']:
                leaderName = p.members[memberGbId]['roleName']

        groupId = groupNUID if groupNUID is not None else p.groupNUID
        event = groupId
        if p.detailInfo['goal'] not in self.goalIns:
            return ''
        else:
            goalType = p.detailInfo['goal']
            fKey, sKey, tKey = p.detailInfo['firstKey'], p.detailInfo['secondKey'], p.detailInfo['thirdKey']
            goalDesc = GOAL_TYPE_DESEC.get(goalType, '')
            goalDetailDesc = self.goalIns[goalType].getTeamGoalDesc(fKey, sKey, tKey)
            if goalDetailDesc:
                goalDesc = '%s-%s' % (goalDesc, goalDetailDesc)
            msgLv = str((p.detailInfo['lvMin'], p.detailInfo['lvMax']))
            msgJob = str(p.detailInfo['schoolReq'])
            msgInvite = uiUtils.getTextFromGMD(GMDD.data.TEAM_INVITE_MSG_BOARD_INVITE, gameStrings.TEXT_GROUPDETAILFACTORY_1144)
            enableNewSchool = gameglobal.rds.configData.get('enableNewSchoolYeCha', False)
            if enableNewSchool and len(p.detailInfo['schoolReq']) >= len(const.SCHOOL_SET) or not enableNewSchool and len(p.detailInfo['schoolReq']) >= len(const.SCHOOL_SET) - 1:
                msg = uiUtils.getTextFromGMD(GMDD.data.TEAM_INVITE_MSG_BOARD_1, '')
                msgJob = '[]'
            else:
                msg = uiUtils.getTextFromGMD(GMDD.data.TEAM_INVITE_MSG_BOARD, '')
            spr = uiConst.CHAT_MESSAGE_SEPARATOR
            msgData = [str(uiConst.CME_TYPE_SHARE_TEAM),
             msg,
             content,
             str(event),
             goalDesc,
             msgLv,
             msgJob,
             msgInvite,
             leaderName]
            msg = spr.join(msgData) + spr
            properties = {'teamId': groupId}
            msg = utils.encodeMsgHeader(msg, properties)
            return msg

    def getTeamGoalMultiDesc(self, goalType, fKey, sKey, tKey):
        if goalType not in uiConst.MENU_GOAL_TYPE_LIST:
            goalType = const.GROUP_GOAL_DEFAULT
        if goalType == const.GROUP_GOAL_DEFAULT:
            return (gameStrings.TEAM_GOAL_NO_LIMIT, '')
        ret = self.goalIns[goalType].getTeamGoalDesc(fKey, sKey, tKey)
        if ret.find('-') == -1:
            return (ret, '')
        return ret.split('-', 1)


def getInstance():
    return GroupDetailFactory.getInstance()
