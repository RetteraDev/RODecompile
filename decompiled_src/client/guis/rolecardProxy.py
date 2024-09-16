#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/rolecardProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gametypes
import time
import commcalc
from Scaleform import GfxValue
import clientUtils
import utils
from guis import uiConst
from guis import uiUtils
from ui import gbk2unicode
from callbackHelper import Functor
from uiProxy import UIProxy
from data import item_data as ID
from data import bonus_data as BD
from data import qiren_role_data as QRD
from data import qiren_role_group_data as QRGD
from data import qiren_biography_data as QBD
from data import qiren_story_data as QSD
from data import qiren_story_group_data as QSGD
from data import qiren_clue_data as QCLD
from data import qiren_config_data as QCD
from data import qiren_pandect_data as QDD
from data import qiren_reward_data as QRWD
from data import qiren_pandect_column_data as QDCD
from cdata import game_msg_def_data as GMDD
TAB_PANDECT = 0
TAB_ROLE = 1
TAB_BOSS = 2
TAB_OTHER = 3
TAB_LIST = [TAB_ROLE, TAB_BOSS, TAB_OTHER]
STATE_INVISIBLE = 'invisible'
STATE_PROCESS = 'process'
STATE_BONUS = 'bonus'
STATE_OVER = 'over'
PHOTO_COLOR_TEMPLATE = 'roleCard/color/%s.dds'
PHOTO_GRAY_TEMPLATE = 'roleCard/gray/%s.dds'
CLUE_IMAGE_PATH = 'roleCard/clue/%s.dds'

class RolecardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RolecardProxy, self).__init__(uiAdapter)
        self.modelMap = {'openRoleCardCollect': self.onOpenRoleCardCollect,
         'getPandectInfo': self.onGetPandectInfo,
         'getPandectDetail': self.onGetPandectDetail,
         'getCollectInfoByTab': self.onGetCollectInfoByTab,
         'takeCollectBonus': self.onTakeCollectBonus,
         'closeCollect': self.onCloseCollect,
         'openRoleDetail': self.onOpenRoleDetail,
         'enterStory': self.onEnterStory,
         'getRoleDetailInfo': self.onGetRoleDetailInfo,
         'getBiographyInfo': self.onGetBiographyInfo,
         'getTheaterInfo': self.onGetTheaterInfo,
         'closeDetail': self.onCloseDetail,
         'closeNewCluePush': self.onCloseNewCluePush,
         'closeNewRolePush': self.onCloseNewRolePush,
         'closeNewTheaterPush': self.onCloseNewTheaterPush,
         'getBonus': self.onGetBonus,
         'checkNewClueFlag': self.onCheckNewClueFlag,
         'getConfigInfo': self.onGetConfigInfo,
         'getRewardInfo': self.onGetRewardInfo,
         'acceptPrize': self.onAcceptPrize,
         'enableReward': self.onEnableReward}
        self.collectWidgetId = uiConst.WIDGET_ROLE_CARD_COLLECT
        self.detailWidgetId = uiConst.WIDGET_ROLE_CARD_DETAIL
        self.newRolePushWidgetId = uiConst.WIDGET_ROLE_CARD_NEW_ROLE_PUSH
        self.newCluePushWidgetId = uiConst.WIDGET_ROLE_CARD_NEW_CLUE_PUSH
        self.newTheaterPushWidgetId = uiConst.WIDGET_ROLE_CARD_NEW_THEATER_PUSH
        self.collectMediator = None
        self.detailMediator = None
        self.rolePushMediator = None
        self.cluePushMediator = None
        self.theaterPushMediator = None
        self.pushClueId = 0
        self.pushRoleId = 0
        self.pushRoleGroupId = 0
        self.storyId = 0
        self.strangerList = []
        self.unknownCardGroupList = []
        self.clueToTheaterMap = {}
        self.newCluesList = []
        self.hideClueDoneNumber = 0
        self.rewardArray = []
        uiAdapter.registerEscFunc(self.collectWidgetId, self.onCloseCollect)
        uiAdapter.registerEscFunc(self.detailWidgetId, self.onCloseDetail)
        self.reset()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == self.collectWidgetId:
            self.collectMediator = mediator
        else:
            if widgetId == self.detailWidgetId:
                self.detailMediator = mediator
                return GfxValue(self.detailRoleId)
            if widgetId == self.newRolePushWidgetId:
                self.rolePushMediator = mediator
                return uiUtils.dict2GfxDict(self.getPushRoleInfo(), True)
            if widgetId == self.newCluePushWidgetId:
                self.cluePushMediator = mediator
                return uiUtils.dict2GfxDict(self.getPushClueInfo(), True)
            if widgetId == self.newTheaterPushWidgetId:
                self.theaterPushMediator = mediator
                return uiUtils.dict2GfxDict(self.getPushTheaterInfo(), True)

    def showConfig(self):
        return gameglobal.rds.configData.get('enableRoleCardCollect', False)

    def show(self):
        if not self.showConfig():
            return
        gameglobal.rds.ui.loadWidget(self.collectWidgetId)

    def newCluePush(self, clueId):
        if not self.showConfig():
            return
        self.pushClueId = clueId
        gameglobal.rds.ui.loadWidget(self.newCluePushWidgetId)

    def newRolePush(self, roleId):
        if not self.showConfig():
            return
        self.pushRoleId = roleId
        self.pushRoleGroupId = 0
        gameglobal.rds.ui.loadWidget(self.newRolePushWidgetId)

    def newRoleGroupPush(self, groupId):
        if not self.showConfig():
            return
        self.pushRoleId = 0
        self.pushRoleGroupId = groupId
        gameglobal.rds.ui.loadWidget(self.newRolePushWidgetId)

    def newRoleTheaterPush(self, storyId):
        if not self.showConfig():
            return
        self.storyId = storyId
        gameglobal.rds.ui.loadWidget(self.newTheaterPushWidgetId)

    def onClueInfoUpdate(self, newClues):
        if not newClues:
            return
        for clueId in newClues:
            pushRoleId = QCLD.data.get(clueId, {}).get('pushRoleId', 0)
            stories = QRD.data.get(pushRoleId, {}).get('stories', ())
            for sId in stories:
                clues = QSGD.data.get(sId, {}).get('cond', ())
                if clueId in clues:
                    self.newCluesList.append(clueId)
                    break

        cid = newClues[-1]
        if QCLD.data.get(cid, {}).get('clueType', 0) == uiConst.CLUE_TYPE_ROLECARD:
            self.newCluePush(cid)
        cursor = 0
        strangerNum = len(self.strangerList)
        for i in range(strangerNum):
            roleData = self.strangerList[cursor]
            recognizeClues = roleData.get('recognizeClues', ())
            _, _, progress = self.getClueProgress(recognizeClues)
            if progress >= 1:
                self.newRolePush(roleData['id'])
                self.strangerList.pop(cursor)
                cursor -= 1
            cursor += 1

        cursor = 0
        cardGroupNum = len(self.unknownCardGroupList)
        for i in range(cardGroupNum):
            cardData = self.unknownCardGroupList[cursor]
            groupCondition = cardData.get('groupCondition', ())
            _, _, progress = self.getClueProgress(groupCondition)
            if progress > 0:
                self.newRoleGroupPush(cardData['groupId'])
                self.unknownCardGroupList.pop(cursor)
                cursor -= 1
            cursor += 1

        self.checkTheaterPush(newClues)
        self.checkAndPushBonus()
        self.refreshNewClueFlag()

    def checkTheaterPush(self, newClues):
        p = BigWorld.player()
        for cid in newClues:
            storyList = self.clueToTheaterMap.get(cid, [])
            if not storyList:
                continue
            for storyId in storyList:
                enableClues = QSD.data.get(storyId, {}).get('enableClues', ())
                needTheaterPush = True
                for clue in enableClues:
                    if not p.getClueFlag(clue):
                        needTheaterPush = False
                        break

                if needTheaterPush:
                    self.newRoleTheaterPush(storyId)
                    return

    def onClueInfoInit(self):
        for id, roleData in QRD.data.iteritems():
            recognizeClues = roleData.get('recognizeClues', ())
            _, _, progress = self.getClueProgress(recognizeClues)
            if progress < 1:
                roleData['id'] = id
                self.strangerList.append(roleData)

        for groupId, groupData in QRGD.data.iteritems():
            groupCondition = groupData.get('groupCondition', ())
            if not groupCondition:
                continue
            _, _, progress = self.getClueProgress(groupCondition)
            if progress == 0:
                groupData['groupId'] = groupId
                self.unknownCardGroupList.append(groupData)

        if not self.clueToTheaterMap:
            for storyId, storyData in QSD.data.iteritems():
                enableClues = storyData.get('enableClues', ())
                if not enableClues:
                    continue
                for clue in enableClues:
                    if not self.clueToTheaterMap.has_key(clue):
                        self.clueToTheaterMap[clue] = []
                    self.clueToTheaterMap[clue].append(storyId)

        self.checkAndPushBonus()

    def checkAndPushBonus(self):
        if not self.showConfig():
            return
        timeBegin = time.time()
        p = BigWorld.player()
        pushMsg = gameglobal.rds.ui.pushMessage
        callBackDict = {'click': self.openGetBonusDialog}
        dataList = pushMsg.getDataList(uiConst.MESSAGE_TYPE_ROLE_CARD)
        pushMsg.setCallBack(uiConst.MESSAGE_TYPE_ROLE_CARD, callBackDict)
        for groupId, groupData in QRGD.data.iteritems():
            groupBonusClues = groupData.get('groupBonusClues', ())
            if not groupBonusClues:
                continue
            _, _, bonusFlag = self.getClueProgress(groupBonusClues)
            if bonusFlag < 1:
                continue
            data = {'data': {'type': 'role',
                      'id': groupId}}
            takeFlag = p.getCharGroupBonusFlag(groupId)
            pushFlag = False
            for itemData in dataList:
                if itemData == data:
                    pushFlag = True
                    break

            if not takeFlag and not pushFlag:
                pushMsg.addPushMsg(uiConst.MESSAGE_TYPE_ROLE_CARD, data)
            elif takeFlag and pushFlag:
                pushMsg.removeData(uiConst.MESSAGE_TYPE_ROLE_CARD, data)

        timeEnd = time.time()
        timePass = timeEnd - timeBegin
        if not BigWorld.isPublishedVersion() and timePass > 0.025:
            msg = gameStrings.TEXT_ROLECARDPROXY_321
            p.reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_CRITICAL, [msg], 0, {})
        if self.detailMediator:
            self.detailMediator.Invoke('refreshInfo')

    def openGetBonusDialog(self):
        data = gameglobal.rds.ui.pushMessage.getLastData(uiConst.MESSAGE_TYPE_ROLE_CARD).get('data', {})
        if not data:
            return
        self.showGetBonusMsgBox(data.get('type', ''), data.get('id', 0))

    def showGetBonusMsgBox(self, type, id):
        if not type or not id:
            return
        if type == 'story':
            bonusId = QSGD.data.get(id, {}).get('storyBonusId', 0)
        elif type == 'role':
            bonusId = QRGD.data.get(id, {}).get('groupBonusId', 0)
        else:
            return
        itemList = []
        fixedBonus = BD.data.get(bonusId, {}).get('fixedBonus', ())
        fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
        for bonusType, bonusItemId, bonusNum in fixedBonus:
            if bonusType == gametypes.BONUS_TYPE_ITEM:
                itemList.append(uiUtils.getGfxItemById(bonusItemId, bonusNum))

        msg = QCD.data.get('getBonusConfirm', gameStrings.TEXT_ROLECARDPROXY_350)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onConfirmGetBonus, type, id), itemData=itemList)

    def onConfirmGetBonus(self, type, id):
        if not type or not id:
            return
        p = BigWorld.player()
        if type == 'story':
            p.cell.getStoryBonus(id)
        elif type == 'role':
            p.cell.getCharGroupBonus(id)

    def reset(self):
        self.detailRoleId = 0

    def clearAll(self):
        self.strangerList = []
        self.unknownCardGroupList = []
        self.newCluesList = []

    def genRoleCardCateInfo(self, cateId):
        ret = {}
        cateData = QRGD.data.get(cateId, {})
        groupStoryData = QSD.data.get(cateData.get('groupQuest', 0), {})
        _, _, progress = self.getClueProgress(groupStoryData.get('enableClues', ()))
        showCateClues = cateData.get('groupCondition', ())
        showBonusClues = cateData.get('showBonusClues', ())
        groupBonusClues = cateData.get('groupBonusClues', ())
        _, _, showFlag = self.getClueProgress(showBonusClues)
        _, _, bonusFlag = self.getClueProgress(groupBonusClues)
        _, _, showCateFlag = self.getClueProgress(showCateClues)
        if showCateFlag == 0:
            return ret
        if showFlag == 0:
            ret['cateState'] = STATE_INVISIBLE
        elif bonusFlag < 1:
            ret['cateState'] = STATE_PROCESS
        elif BigWorld.player().getCharGroupBonusFlag(cateId):
            ret['cateState'] = STATE_OVER
        else:
            ret['cateState'] = STATE_BONUS
        bonusId = cateData.get('groupBonusId', 0)
        if not bonusId:
            ret['cateState'] = STATE_INVISIBLE
            ret['bonusTips'] = ''
        else:
            ret['bonusTips'] = self.genBonusTips(bonusId)
        ret['cateId'] = cateId
        ret['storyId'] = cateData.get('groupQuest', 0)
        ret['cateName'] = cateData.get('groupName', '')
        ret['roleList'] = self.genRoleList(cateId)
        ret['hasTheater'] = bool(groupStoryData)
        ret['theaterName'] = gameStrings.TEXT_ROLECARDPROXY_410 + groupStoryData.get('storyName', '')
        ret['theaterOpen'] = progress >= 1
        ret['tipsInfo'] = groupStoryData.get('storyDesc', '')
        return ret

    def genBonusTips(self, bonusId):
        nameMap = {gametypes.BONUS_TYPE_MONEY: gameStrings.TEXT_INVENTORYPROXY_3297,
         gametypes.BONUS_TYPE_FAME: gameStrings.TEXT_CHALLENGEPROXY_199_1,
         gametypes.BONUS_TYPE_EXP: gameStrings.TEXT_GAMETYPES_6408,
         gametypes.BONUS_TYPE_FISHING_EXP: gameStrings.TEXT_ARENARANKAWARDPROXY_213,
         gametypes.BONUS_TYPE_SOC_EXP: gameStrings.TEXT_IMPL_IMPACTIVITIES_663}
        ret = "<font size = \'14\' color = \'#f2ab0d\'>" + gameStrings.TEXT_ROLECARDPROXY_424 + '</font><br>'
        fixedBonus = BD.data.get(bonusId, {}).get('fixedBonus', ())
        fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
        for bonusType, bonusItemId, bonusNum in fixedBonus:
            if bonusType == gametypes.BONUS_TYPE_ITEM:
                ret += "<font size = \'12\'>" + gameStrings.TEXT_ROLECARDPROXY_430 + ID.data.get(bonusItemId, {}).get('name', gameStrings.TEXT_GAMETYPES_6409) + gameStrings.TEXT_HISTORYCONSUMEDPROXY_256 + str(bonusNum) + '</font><br>'
            else:
                ret += "<font size = \'12\'>" + gameStrings.TEXT_ROLECARDPROXY_430 + nameMap.get(bonusType) + gameStrings.TEXT_HISTORYCONSUMEDPROXY_256 + str(bonusNum) + '</font><br>'

        ret += '<br>'
        return ret

    def genRoleList(self, cateId):
        ret = []
        cateData = QRGD.data.get(cateId, {})
        roleIdList = cateData.get('roleIdList', ())
        for roleId in roleIdList:
            ret.append(self.genRoleDetailInfo(roleId))

        return ret

    def genRoleDetailInfo(self, roleId):
        roleInfo = {}
        roleData = QRD.data.get(roleId, {})
        roleInfo['newFlag'] = roleData.get('newFlag', 0)
        roleInfo['name'] = roleData.get('name', gameStrings.TEXT_ROLECARDPROXY_452)
        roleInfo['roleId'] = roleId
        commClues = roleData.get('commClues', ())
        commComp, commAll, _ = self.getClueProgress(commClues)
        roleInfo['curValue'] = commComp
        roleInfo['maxValue'] = commAll
        rareClues = roleData.get('rareClues', ())
        rareComp, rareAll, _ = self.getClueProgress(rareClues)
        roleInfo['golden'] = rareComp >= rareAll and commComp >= commAll
        recognizeClues = roleData.get('recognizeClues', ())
        _, _, recProgress = self.getClueProgress(recognizeClues)
        roleInfo['unknown'] = recProgress < 1
        if roleInfo['unknown']:
            roleInfo['photo'] = PHOTO_COLOR_TEMPLATE % 'unknown'
            roleInfo['tipsInfo'] = roleData.get('unknownDesc', gameStrings.TEXT_ROLECARDPROXY_470)
            roleInfo['curValue'] = 0
            roleInfo['maxValue'] = 1
            roleInfo['name'] = QCD.data.get('unRecognizedRoleName', '???')
        elif roleInfo['curValue'] >= roleInfo['maxValue']:
            roleInfo['photo'] = PHOTO_COLOR_TEMPLATE % roleData.get('icon', 'unknown')
            if roleInfo['golden']:
                roleInfo['tipsInfo'] = roleData.get('rareDesc', '')
            else:
                prefix = QCD.data.get('goldenProgressPrefix', gameStrings.TEXT_ROLECARDPROXY_481) % (rareComp, rareAll) + '\n'
                roleInfo['tipsInfo'] = prefix + roleData.get('commDesc', '')
        else:
            roleInfo['photo'] = PHOTO_GRAY_TEMPLATE % roleData.get('icon', 'unknown')
            roleInfo['tipsInfo'] = roleData.get('unfinishedDesc', '')
        roleInfo['showBiogrophyTab'] = roleData.get('showBiographyTabs', 0)
        return roleInfo

    def genTheaterList(self, sgId):
        theaterList = []
        groupData = QSGD.data.get(sgId, {})
        stories = groupData.get('stories', ())
        for sId in stories:
            theaterInfo = {}
            sData = QSD.data.get(sId, {})
            theaterInfo['name'] = sData.get('storyName', gameStrings.TEXT_GAMECONST_1261)
            theaterInfo['theaterId'] = sId
            theaterInfo['theaterTip'] = sData.get('storyDesc', gameStrings.TEXT_ROLECARDPROXY_502)
            enableClues = sData.get('enableClues', ())
            _, _, enableFlag = self.getClueProgress(enableClues)
            theaterInfo['enableFlag'] = enableFlag >= 1
            if theaterInfo['enableFlag']:
                gameglobal.rds.tutorial.onOpenTheater(sId)
            theaterList.append(theaterInfo)

        return theaterList

    def getClueProgress(self, clueList):
        if not clueList:
            return (1, 1, 1)
        allNum = 0
        compNum = 0
        p = BigWorld.player()
        for clueId in clueList:
            allNum += 1
            compNum += 1 if p.getClueFlag(clueId) else 0

        return (compNum, allNum, float(compNum) / allNum)

    def getPushClueInfo(self):
        qcld = QCLD.data.get(self.pushClueId, {})
        ret = {}
        ret['title'] = QCD.data.get('newClueTitle', gameStrings.TEXT_ROLECARDPROXY_533)
        ret['text'] = qcld.get('conditionName', gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_1083)
        pushRoleId = qcld.get('pushRoleId', 0)
        roleName = QRD.data.get(pushRoleId, {}).get('name', '')
        storyId = qcld.get('storyId', 0)
        storyName = QSD.data.get(storyId, {}).get('storyName', '')
        if roleName != '' and storyName != '':
            BigWorld.player().showGameMsg(GMDD.data.ROLE_CARD_PUSH_CLUE, (roleName, storyName))
        return ret

    def getPushRoleInfo(self):
        ret = {}
        if self.pushRoleGroupId:
            ret['iconType'] = 'two'
            ret['title'] = QCD.data.get('newRoleGroupTitle', gameStrings.TEXT_ROLECARDPROXY_551)
            ret['text'] = QRGD.data.get(self.pushRoleGroupId, {}).get('groupName', gameStrings.TEXT_ROLECARDPROXY_552)
        else:
            ret['iconType'] = 'one'
            ret['title'] = QCD.data.get('newRoleTitle', gameStrings.TEXT_ROLECARDPROXY_555)
            ret['text'] = QRD.data.get(self.pushRoleId, {}).get('name', gameStrings.TEXT_ROLECARDPROXY_452)
        return ret

    def getPushTheaterInfo(self):
        ret = {}
        ret['title'] = QCD.data.get('newTheaterTitle', gameStrings.TEXT_ROLECARDPROXY_561)
        ret['text'] = QSD.data.get(self.storyId, {}).get('storyName', gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_1083)
        return ret

    def onOpenRoleCardCollect(self, *arg):
        self.show()

    def onGetPandectInfo(self, *arg):
        dataList = []
        for key, value in QDD.data.iteritems():
            dataItem = {}
            dataItem['key'] = key
            dataItem['label'] = value.get('name', '')
            dataItem['children'] = []
            groupIdList = value.get('groupIdList', ())
            if groupIdList:
                for groupId in groupIdList:
                    dataItem['children'].append(self.getPandectColumnInfo(groupId))

            dataList.append(dataItem)

        dataList.sort(key=lambda x: x['key'], reverse=False)
        return uiUtils.array2GfxAarry(dataList, True)

    def getPandectColumnInfo(self, groupId):
        gdcd = QDCD.data.get(groupId, {})
        info = {}
        info['key'] = groupId
        info['label'] = gdcd.get('name', '')
        return info

    def onGetPandectDetail(self, *arg):
        key = int(arg[3][0].GetNumber())
        isColumn = arg[3][1].GetBool()
        self.refreshonPandectDetail(key, isColumn)

    def refreshonPandectDetail(self, key, isColumn):
        if self.collectMediator:
            if isColumn:
                data = QDCD.data.get(key, {})
            else:
                data = QDD.data.get(key, {})
            info = {}
            info['title'] = data.get('name', '')
            cardList = []
            idList = data.get('idList', ())
            if idList:
                for roleId in idList:
                    cardList.append(self.genRoleDetailInfo(roleId))

            info['cardList'] = cardList
            self.collectMediator.Invoke('refreshonPandectDetail', uiUtils.dict2GfxDict(info, True))

    def onGetCollectInfoByTab(self, *arg):
        tabId = int(arg[3][0].GetNumber())
        cateArray = []
        for cateId, cateData in QRGD.data.iteritems():
            if cateData.get('groupType', TAB_ROLE) != tabId:
                continue
            cateInfo = self.genRoleCardCateInfo(cateId)
            if cateInfo:
                cateArray.append(cateInfo)

        return uiUtils.array2GfxAarry(cateArray, True)

    def onGetRewardInfo(self, *arg):
        self.rewardArray = self.getRewardData()
        return uiUtils.array2GfxAarry(self.rewardArray, True)

    def getRewardData(self):
        ret = []
        p = BigWorld.player()
        for key, value in QRWD.data.items():
            itemInfo = {}
            itemInfo['id'] = key
            itemInfo['rewardName'] = value.get('rewardName', '')
            itemInfo['rewardDesc'] = value.get('rewardDesc', '')
            clues = value.get('clue', ())
            itemInfo['clues'] = clues
            itemInfo['maxVal'] = len(clues)
            currentVal = 0
            for i in clues:
                if p.getClueFlag(i):
                    currentVal = currentVal + 1

            itemInfo['accepted'] = commcalc.getBit(p.qirenBonusFlags, key)
            itemInfo['currentVal'] = currentVal
            bonusId = value.get('bonusId', 100001)
            itemList = clientUtils.genItemBonus(bonusId)
            itemTips = gameStrings.TEXT_ROLECARDPROXY_652
            for id in itemList:
                itemName = ID.data.get(id, {}).get('name', '')
                itemTips += "<font size = \'12\' color=\'#ffffff\'>" + gameStrings.TEXT_HELPPROXY_512 + itemName + gameStrings.TEXT_HISTORYCONSUMEDPROXY_256 + str(id[1]) + '</font> <br>'

            itemInfo['itemTips'] = itemTips
            itemInfo['bounsPath'] = uiUtils.getGfxItemById(value.get('bounsPath', 100001))
            itemInfo['weightId'] = value.get('weightId', 0)
            ret.append(itemInfo)

        ret.sort(key=lambda x: x['weightId'])
        return ret

    def refreshRewardInfo(self):
        p = BigWorld.player()
        for index in range(len(self.rewardArray)):
            self.rewardArray[index]['accepted'] = commcalc.getBit(p.qirenBonusFlags, index)
            currentVal = 0
            for i in self.rewardArray[index]['clues']:
                if p.getClueFlag(i):
                    currentVal = currentVal + 1

            self.rewardArray[index]['currentVal'] = currentVal

        if self.collectMediator:
            self.collectMediator.Invoke('refreshRewardInfo', uiUtils.array2GfxAarry(self.rewardArray, True))

    def onEnableReward(self, *arg):
        ret = gameglobal.rds.configData.get('enableQiRenReward', False)
        return GfxValue(ret)

    def onAcceptPrize(self, *arg):
        id = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        p.cell.getQirenBonus(id)

    def onTakeCollectBonus(self, *arg):
        pass

    def onCloseCollect(self, *arg):
        gameglobal.rds.ui.unLoadWidget(self.collectWidgetId)
        self.collectMediator = None

    def onOpenRoleDetail(self, *arg):
        if not self.showConfig():
            return
        roleId = int(arg[3][0].GetNumber())
        self.detailRoleId = roleId
        if self.detailMediator:
            self.detailMediator.Invoke('swapPanelToFront')
            self.detailMediator.Invoke('refreshRoleInfo', GfxValue(self.detailRoleId))
            self.detailMediator.Invoke('refreshInfo')
        else:
            gameglobal.rds.ui.loadWidget(self.detailWidgetId)

    def onEnterStory(self, *arg):
        storyId = int(arg[3][0].GetNumber())
        msg = QSD.data.get(storyId, {}).get('enterStoryTips', gameStrings.TEXT_ROLECARDPROXY_707)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onConfirmEnterStory, storyId))

    def onEnterStorySucc(self):
        self.onCloseCollect()
        self.onCloseDetail()

    def onConfirmEnterStory(self, storyId):
        BigWorld.player().cell.startCharStory(storyId)

    def onGetRoleDetailInfo(self, *arg):
        roleId = int(arg[3][0].GetNumber())
        return uiUtils.dict2GfxDict(self.genRoleDetailInfo(roleId), True)

    def onGetBiographyInfo(self, *arg):
        bioArray = []
        roleId = int(arg[3][0].GetNumber())
        roleData = QRD.data.get(roleId, {})
        bioGroup = roleData.get('bioGroup', ())
        for bioId in bioGroup:
            bioInfo = {}
            bioData = QBD.data.get(bioId, {})
            bioInfo['title'] = bioData.get('title', gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_1083)
            bioInfo['text'] = bioData.get('text', gameStrings.TEXT_STYLIST_1571)
            bioInfo['index'] = bioData.get('index', 1)
            visibleClues = bioData.get('visibleClues', ())
            _, _, progress = self.getClueProgress(visibleClues)
            if progress < 1:
                bioInfo['title'] = QCD.data.get('invisibleBioTitle', gameStrings.TEXT_ROLECARDPROXY_737)
                bioInfo['text'] = QCD.data.get('invisibleBioText', gameStrings.TEXT_ROLECARDPROXY_737)
            bioArray.append(bioInfo)

        bioArray.sort(key=lambda value: value['index'])
        return uiUtils.array2GfxAarry(bioArray, True)

    def onGetTheaterInfo(self, *arg):
        theaterArray = []
        roleId = int(arg[3][0].GetNumber())
        roleData = QRD.data.get(roleId, {})
        stories = roleData.get('stories', ())
        effectDict = {}
        for sId in stories:
            theaterGroup = {}
            storyGroupData = QSGD.data.get(sId, {})
            showGroupClue = storyGroupData.get('storyGroupClue', ())
            _, _, showGroupFlag = self.getClueProgress(showGroupClue)
            if showGroupFlag < 1:
                continue
            theaterGroup['newFlag'] = storyGroupData.get('newFlag', 0)
            theaterGroup['name'] = storyGroupData.get('storyGroupName', gameStrings.TEXT_ROLECARDPROXY_764)
            theaterGroup['groupTip'] = storyGroupData.get('storyGroupDesc', gameStrings.TEXT_ROLECARDPROXY_765)
            theaterGroup['cateId'] = sId
            theaterGroup['theaterList'] = self.genTheaterList(sId)
            showBonusClue = storyGroupData.get('storyBonusEnableClue', ())
            storyBonusClue = storyGroupData.get('storyBonusClue', ())
            _, _, showFlag = self.getClueProgress(showBonusClue)
            _, _, bonusFlag = self.getClueProgress(storyBonusClue)
            if showFlag < 1:
                theaterGroup['state'] = STATE_INVISIBLE
            elif bonusFlag < 1:
                theaterGroup['state'] = STATE_PROCESS
                theaterGroup['btnLabel'] = gameStrings.TEXT_ACTIVITYSALEPOINTSREWARDPROXY_106
                theaterGroup['btnEnabled'] = False
            elif BigWorld.player().getStoryBonusFlag(sId):
                theaterGroup['state'] = STATE_OVER
                theaterGroup['btnLabel'] = gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_187
                theaterGroup['btnEnabled'] = False
                if storyGroupData.get('storyGroupClue', ()):
                    self.hideClueDoneNumber += 1
            else:
                theaterGroup['state'] = STATE_BONUS
                theaterGroup['btnLabel'] = gameStrings.TEXT_ROLECARDPROXY_791
                theaterGroup['btnEnabled'] = True
                if storyGroupData.get('storyGroupClue', ()):
                    self.hideClueDoneNumber += 1
            bonusId = storyGroupData.get('storyBonusId', 0)
            storyBonusPathId = storyGroupData.get('storyBonusPathId', 0)
            storyBonusPath = ''
            if storyBonusPathId != 0:
                storyBonusPath = uiUtils.getIcon(uiConst.ICON_TYPE_ITEM, storyBonusPathId)
            if not bonusId:
                theaterGroup['state'] = STATE_INVISIBLE
                theaterGroup['bonusTips'] = ''
            else:
                theaterGroup['storyId'] = sId
                theaterGroup['bonusTips'] = self.genBonusTips(bonusId)
                theaterGroup['storyBonusPath'] = storyBonusPath
            clueInfos = []
            clueOutputInfos = []
            clues = storyGroupData.get('cond', ())
            clueClues = storyGroupData.get('condCondition', ())
            clueOutput = storyGroupData.get('condOutput', ())
            minLen = min(len(clues), len(clueClues))
            for i, cid in enumerate(clues):
                if i >= minLen:
                    break
                info = {}
                cc = clueClues[i]
                _, _, cFlag = self.getClueProgress([cid])
                _, _, ccFlag = self.getClueProgress(cc)
                clueData = QCLD.data.get(cid, {})
                clueName = clueData.get('conditionName', '')
                clueDesc = clueData.get('desc', '')
                clueOrig = clueData.get('origin', '')
                if ccFlag < 1:
                    info['state'] = 'unknown'
                    unknownIcon = str(clueData.get('unknownIcon', ''))
                    info['stateIcon'] = CLUE_IMAGE_PATH % unknownIcon if unknownIcon != '' else ''
                    info['clueTips'] = QCD.data.get('unknownClueTips', '')
                elif cFlag < 1:
                    info['state'] = 'process'
                    processIcon = str(clueData.get('processIcon', ''))
                    info['stateIcon'] = CLUE_IMAGE_PATH % processIcon if processIcon != '' else ''
                    info['clueTips'] = '%s<br>%s' % (clueName, clueOrig)
                else:
                    info['state'] = 'complete'
                    completeIcon = str(clueData.get('completeIcon', ''))
                    info['stateIcon'] = CLUE_IMAGE_PATH % completeIcon if completeIcon != '' else ''
                    info['clueTips'] = '%s<br>%s' % (clueName, clueDesc)
                if cid in self.newCluesList:
                    info['effectVisible'] = True
                    effectDict[cid] = True
                else:
                    info['effectVisible'] = False
                if cid in clueOutput:
                    clueOutputInfos.append(info)
                else:
                    clueInfos.append(info)

            theaterGroup['clueInfo'] = clueInfos
            theaterGroup['clueInfoOutput'] = clueOutputInfos
            theaterArray.append(theaterGroup)

        for cid in effectDict.iterkeys():
            if cid in self.newCluesList:
                self.newCluesList.remove(cid)

        return uiUtils.array2GfxAarry(theaterArray, True)

    def onCloseDetail(self, *arg):
        self.detailRoleId = 0
        self.detailMediator = None
        self.hideClueDoneNumber = 0
        gameglobal.rds.ui.unLoadWidget(self.detailWidgetId)

    def onCloseNewCluePush(self, *arg):
        self.cluePushMediator = None
        gameglobal.rds.ui.unLoadWidget(self.newCluePushWidgetId)

    def onCloseNewRolePush(self, *arg):
        self.rolePushMediator = None
        gameglobal.rds.ui.unLoadWidget(self.newRolePushWidgetId)

    def onCloseNewTheaterPush(self, *arg):
        self.theaterPushMediator = None
        gameglobal.rds.ui.unLoadWidget(self.newTheaterPushWidgetId)

    def onGetBonus(self, *arg):
        type = arg[3][0].GetString()
        storyId = int(arg[3][1].GetNumber())
        self.showGetBonusMsgBox(type, storyId)

    def onCheckNewClueFlag(self, *arg):
        self.refreshNewClueFlag()

    def refreshNewClueFlag(self):
        if self.collectMediator:
            collectInfo = {}
            newRoleMap = {}
            for clueId in self.newCluesList:
                pushRoleId = QCLD.data.get(clueId, {}).get('pushRoleId', 0)
                newRoleMap[pushRoleId] = True

            for tabId in TAB_LIST:
                for cateData in QRGD.data.itervalues():
                    if cateData.get('groupType', TAB_ROLE) != tabId:
                        continue
                    roleIdList = cateData.get('roleIdList', ())
                    for roleId in roleIdList:
                        if tabId not in collectInfo:
                            collectInfo[tabId] = {}
                        if roleId in newRoleMap:
                            collectInfo[tabId]['tabFlag'] = True
                            collectInfo[tabId][roleId] = True
                        else:
                            collectInfo[tabId][roleId] = False

            self.collectMediator.Invoke('refreshNewClueFlag', uiUtils.dict2GfxDict(collectInfo, True))

    def onGetConfigInfo(self, *arg):
        ret = ''
        ret = QCD.data.get('hideClueDoneText', gameStrings.TEXT_ROLECARDPROXY_924) + str(self.hideClueDoneNumber)
        return GfxValue(gbk2unicode(ret))
