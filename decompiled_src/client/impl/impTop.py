#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impTop.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gametypes
import utils
import gamelog
from guis import uiConst
from guis import uiUtils
from data import bonus_data as BD
from cdata import game_msg_def_data as GMDD
from cdata import top_reward_data as TRD

class ImpTop(object):

    def onTopRewarded(self, rank, topType, fbNo):
        proxyId = gameglobal.rds.ui.ranking.topTypeDict.get(topType, 0)
        rankInfo = gameglobal.rds.ui.ranking._getRewardInfo(proxyId, fbNo)
        rankInfo = list(rankInfo)
        if rankInfo:
            rankInfo[3] = True
            gameglobal.rds.ui.ranking._setRewardInfo(proxyId, fbNo, tuple(rankInfo))
        if topType == gametypes.TOP_TYPE_FB and fbNo == gameglobal.rds.ui.ranking.awardStype:
            gameglobal.rds.ui.ranking.refreshAwardPanel()
        elif topType != gametypes.TOP_TYPE_FB and topType == gameglobal.rds.ui.ranking.awardType:
            gameglobal.rds.ui.ranking.refreshAwardPanel()
        self.onGetRewardBack(topType, fbNo)

    def onQueryAllCanGetRewardTop(self, info):
        if not hasattr(self, 'awardTopInfo'):
            self.awardTopInfo = []
        school = BigWorld.player().school
        awardTopInfo = []
        for topType, fbNo, (rank, val) in info:
            rankInfo = TRD.data.get((topType, fbNo, school))
            if not rankInfo:
                rankInfo = TRD.data.get((topType, fbNo, 0))
                if rankInfo:
                    school = 0
            for rankInfoItem in rankInfo:
                rankRange = rankInfoItem.get('rankRange')
                if rank >= rankRange[0] and rank <= rankRange[1]:
                    self.awardTopInfo.append({'fbNo': fbNo,
                     'topType': topType,
                     'rank': rank,
                     'awardInfo': rankInfoItem,
                     'school': school})
                    awardTopInfo.append({'fbNo': fbNo,
                     'topType': topType,
                     'rank': rank,
                     'awardInfo': rankInfoItem,
                     'school': school})
                    break

        callBackDict = {'click': self.onClickGetRewardTop}
        for data in awardTopInfo:
            itemInfo = {'data': data}
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_RANK_AWARD, itemInfo)

        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_RANK_AWARD, callBackDict)

    def onClickGetRewardTop(self):
        if hasattr(self, 'awardTopInfo') and len(self.awardTopInfo):
            info = self.awardTopInfo[0]
            awardInfo = info['awardInfo']
            bonusId = 0
            if awardInfo.get('schoolBonusIds'):
                bonusId = awardInfo['schoolBonusIds'].get(BigWorld.player().school)
            if not bonusId:
                bonusId = awardInfo.get('bonusId')
            msg = uiUtils.getTextFromGMD(GMDD.data.GET_REWARD_TOP, gameStrings.TEXT_IMPTOP_67) % (info['awardInfo']['titleName'], info['rank'])
            itemDataList = []
            if bonusId:
                fixedBonus = BD.data.get(bonusId, {}).get('fixedBonus', ())
                fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
                for i in range(0, len(fixedBonus)):
                    bonusType, bonusItemId, bonusNum = fixedBonus[i]
                    if bonusType == gametypes.BONUS_TYPE_ITEM:
                        itemDataInfo = uiUtils.getItemData(bonusItemId)
                        itemDataInfo['count'] = bonusNum
                        itemDataInfo['color'] = uiUtils.getItemColor(bonusItemId)
                        itemDataList.append(itemDataInfo)

            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.onClickConfirmGetRewardTop, yesBtnText=gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_192, noBtnText=gameStrings.TEXT_IMPTOP_80_1, title=gameStrings.TEXT_GROUPPROXY_192, itemData=itemDataList)
        else:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_RANK_AWARD)

    def onClickConfirmGetRewardTop(self):
        if not hasattr(self, 'awardTopInfo'):
            self.awardTopInfo = []
            return
        if len(self.awardTopInfo) == 0:
            return
        data = self.awardTopInfo[0]
        BigWorld.player().cell.getTopReward(data['topType'], data['fbNo'])

    def onGetRewardBack(self, topType, fbNo):
        if not hasattr(self, 'awardTopInfo'):
            self.awardTopInfo = []
            return
        for i in xrange(len(self.awardTopInfo)):
            data = self.awardTopInfo[i]
            if data['topType'] == topType and data['fbNo'] == fbNo:
                nowData = self.awardTopInfo.pop(i)
                gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_RANK_AWARD, {'data': nowData})
                break

    def onQueryTopDataMemberDetail(self, info):
        gameglobal.rds.ui.ranking.updateTeamDetail(info)

    def onQueryGroupFubenLastWeekRank(self, rank):
        gameglobal.rds.ui.ranking.myLastWeekRank = rank

    def onGetHallOfFameQuizTop(self, quizArgs):
        selectedTop, state, isQuiz, quizTopKey = quizArgs
        gameglobal.rds.ui.celebrityQuiz.onGetTopType(selectedTop, quizTopKey)

    def onHallOfFameSwitch(self, isStart):
        gameglobal.rds.ui.celebrityRank.recordHallOfFameState(isStart)

    def onGetMyHofRankValue(self, topType, value):
        """
        \xe8\x8e\xb7\xe5\xbe\x97\xe8\x87\xaa\xe8\xba\xab\xe7\x9a\x84\xe5\x90\x8d\xe4\xba\xba\xe5\xa0\x82\xe7\x9b\xb8\xe5\x85\xb3\xe5\x80\xbc\xef\xbc\x88\xe7\x9b\xae\xe5\x89\x8d\xe5\x8f\xaa\xe6\x94\xaf\xe6\x8c\x81\xe4\xbf\xae\xe4\xb8\xba\xe5\x92\x8c\xe7\xa5\x9e\xe5\x85\xb5\xef\xbc\x89
        :param topType:\xe6\x8e\x92\xe8\xa1\x8c\xe6\xa6\x9c\xe7\xb1\xbb\xe5\x9e\x8b 
        :param value: \xe4\xbf\xae\xe4\xb8\xba\xe5\x80\xbc\xe6\x88\x96\xe7\xa5\x9e\xe5\x85\xb5\xe5\x80\xbc
        """
        gamelog.debug('@xzh onGetMyHofRankValue', topType, value)
        if topType == gametypes.TOP_TYPE_HALL_OF_FAME_XIUWEI:
            gameglobal.rds.ui.celebrityXiuWeiRank.updateMyHofXiuWeiValue(value)
        elif topType == gametypes.TOP_TYPE_HALL_OF_FAME_SHENBING:
            gameglobal.rds.ui.celebrityEquipmentRank.updateMyHofShenBingValue(value)
        else:
            gameglobal.rds.ui.celebrityVoteRank.updateMyHofVoteValue(topType, value)

    def queryXiuWeiLastRankLv(self, callback):
        if abs(utils.getNow() - getattr(self, 'lastXiuWeiQueryTime', 0)) > 5:
            self.xiuweiQueryCallBack = callback
            self.lastXiuWeiQueryTime = utils.getNow()
            self.base.queryXiuWeiLastRankLv()
        else:
            callback()

    def onQueryXiuWeiLastRankLv(self, lastLv):
        self.xiuweiLastRankLv = lastLv
        if getattr(self, 'xiuweiQueryCallBack', None):
            self.xiuweiQueryCallBack()
            self.xiuweiQueryCallBack = None
