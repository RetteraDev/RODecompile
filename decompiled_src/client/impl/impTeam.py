#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impTeam.o
from gamestrings import gameStrings
import copy
import BigWorld
import gametypes
import gameglobal
import const
import utils
import keys
from guis import uiUtils
from guis import uiConst
from appSetting import Obj as AppSettings
from cdata import game_msg_def_data as GMDD
from data import item_data as ID
from data import group_label_data as GLD
from data import quest_data as QD

class ImpTeam(object):

    def updatePublicTeamDetails(self, teamNUID, info):
        pass

    def onSetTemporaryGroupFollowOut(self, mGbId, flag):
        pass

    def updatePubTeamInfo(self, teamGoal, info):
        pass

    def onQueryLinkTeamInfo(self, info):
        pass

    def updateDiGongTeamInfo(self, info):
        pass

    def updateWorldWarTeamInfo(self, info):
        pass

    def onTeamGoalChanged(self, groupNUID):
        pass

    def onTeamGoalChangedByCall(self, groupNUID):
        pass

    def notifyInviteGroupFailedWithNoGroupAlready(self, roleName):
        pass

    def onApplyByGroupWithTgtNonGroup(self, srcName, srcLevel, srcSchool, srcGbId):
        pass

    def isInFullTeam(self):
        members = getattr(self, 'members', {})
        if self.isInGroup() and len(members) == const.GROUP_MAX_NUMBER:
            return True
        if self.isInTeam() and len(members) == const.TEAM_MAX_NUMBER:
            return True
        return False

    def isInTeam(self):
        if self.inWorld and self.groupNUID > 0 and hasattr(self, 'groupType') and self.groupType == gametypes.GROUP_TYPE_TEAM_GROUP:
            return True
        return False

    def isInGroup(self):
        if self.inWorld and self.groupNUID > 0 and hasattr(self, 'groupType') and self.groupType == gametypes.GROUP_TYPE_RAID_GROUP:
            return True
        return False

    def isInTeamOrGroup(self):
        if hasattr(self, 'groupNUID') and self.groupNUID > 0:
            return True
        else:
            return False

    def isTeamLeader(self):
        if hasattr(self, 'headerGbId'):
            if self.headerGbId and self.headerGbId == self.gbId:
                return True
        return False

    def isTeamLeaderByGbId(self, gbId):
        if hasattr(self, 'headerGbId'):
            if self.headerGbId and self.headerGbId == gbId:
                return True
        return False

    def isInMyTeam(self, e):
        if not e:
            return False
        members = getattr(self, 'members', {})
        if hasattr(e, 'gbId') and e.gbId in members:
            return True
        return False

    def onSyncHeaderClientPos(self, x, y, z, spaceNo, isPathFinding, isForcely):
        pass

    def delApplyerByGbId(self, gbId):
        pass

    def delAllApplyer(self):
        pass

    def resOthersInfo(self, memberGbId, info):
        pass

    def onApplyerFailed(self, groupNUID, msgId, msgArg):
        pass

    def applyGroupSucc(self, roleName, level, school, groupNUID):
        pass

    def receivePos(self, gbId, posX, posZ, mapNo):
        pass

    def setEntityMark(self, mark):
        pass

    def resetEntityMark(self):
        self.topLogo.removeTeamLogo()

    def addEntityMark(self, entityId, markFlag):
        pass

    def delEntityMark(self, entityId):
        del self.groupMark[entityId]
        ent = BigWorld.entities.get(entityId)
        if ent:
            ent.topLogo.removeTeamLogo()

    def onSetMapMark(self, groupMapMark, mapMarkStatus):
        pass

    def onResetMapMark(self):
        pass

    def onAddMapMark(self, effectId, extra, mapMarkStatus):
        pass

    def onDelMapMark(self, effectId):
        pass

    def askForGroupPrepare(self, groupNUID):
        pass

    def cancelAskForGroupPrepare(self):
        pass

    def updateGroupPrepare(self, result, isEnd):
        pass

    def onSetGroupType(self, groupType):
        print '@hjx group#onSetGroupType:', groupType

    def beginGroupAuctionTimer(self, groupNUID, itemUUID):
        if itemUUID == gameglobal.rds.ui.assign.curAuctionUUID:
            if not gameglobal.rds.ui.assign.auctionMediator and len(gameglobal.rds.ui.assign.auctionBag) and not gameglobal.rds.ui.assign.curGiveUp:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ASSIGN_AUCTION)
                BigWorld.player().justShowCipher()
            gameglobal.rds.ui.assign.startAuction()
        else:
            gameglobal.rds.ui.assign.closeAuction()
            self.showGameMsg(GMDD.data.GROUP_AUCTION_NOT_IN_ASSIGN_LIST, ())

    def stopGroupAuctionTimer(self, groupNUID, itemUUID):
        gameglobal.rds.ui.assign.stopAuction()

    def sendGroupBidding(self, gbId, price, itemUUID):
        roleName = self.members.get(gbId, {}).get('roleName', '')
        gameglobal.rds.ui.assign.setAuctionState(roleName, price, False, gbId != self.gbId)
        gameglobal.rds.ui.assign.setMaxAuctionTime()

    def resetAuctionAward(self, itemUUID):
        price = 1
        for item in gameglobal.rds.ui.assign.auctionBag:
            if item.uuid == itemUUID:
                price = ID.data.get(item.id, {}).get('auctionPrice', 1)
                break

        gameglobal.rds.ui.assign.curGiveUp = False
        gameglobal.rds.ui.assign.auctionStep = -1
        gameglobal.rds.ui.assign.curAuctionPrice = 0
        gameglobal.rds.ui.assign.curAuctionPlayer = ''
        gameglobal.rds.ui.assign.setAuctionState('', price, True)
        gameglobal.rds.ui.assign.setMaxAuctionTime()

    def giveUpAuctionSucc(self, itemUUID):
        gameglobal.rds.ui.assign.setBtnEnabled(False)

    def onUpdateGroupMatchInfo(self, groupMatchClass, matchMemberInfo, matchStartTime, extra):
        pass

    def onNotifyMatchGroupDone(self):
        pass

    def onDiscardMatchSeat(self):
        pass

    def refreshAssignMode(self):
        pass

    def onInviteGroupFollow(self):
        pass

    def onSyncInGroupFollow(self, info):
        pass

    def onQueryGroupHeaderFollowInfo(self, info):
        pass

    def oneKeyCreateTeamByGoal(self, key):
        if self.isInTeamOrGroup():
            self.showGameMsg(GMDD.data.ONE_KEY_TEAM_ALREAD_IN_TEAM, ())
        else:
            self._processOneKeyCreateTeam(key)

    def _processOneKeyCreateTeam(self, key):
        item = GLD.data.get(key, {})
        if not item:
            return
        else:
            lvData = item.get('lv', [0, 0])
            beginTime = item.get('timeStart', None)
            endTime = item.get('timeEnd', None)
            weekSet = item.get('weekSet', 0)
            if not lvData[0] <= self.lv <= lvData[1]:
                self.showGameMsg(GMDD.data.ONE_KEY_TEAM_NOT_RIGHT_LV, ())
                return
            if utils.isInvalidWeek(weekSet):
                self.showGameMsg(GMDD.data.ONE_KEY_TEAM_NOT_RIGHT_TIME, ())
                return
            if beginTime and endTime:
                if not utils.inCrontabRange(beginTime, endTime):
                    self.showGameMsg(GMDD.data.ONE_KEY_TEAM_NOT_RIGHT_TIME, ())
                    return
            teamName = gameStrings.TEXT_IMPTEAM_240 % self.realRoleName
            levelMin = 0
            levelMax = 0
            if item.get('recommendLv', []):
                levelMin, levelMax = item.get('recommendLv', [1, 79])
            elif item.get('lv', []):
                levelMin, levelMax = item.get('lv', [1, 79])
            needSchool = copy.deepcopy(const.ALL_SCHOOLS)
            if not gameglobal.rds.configData.get('enableNewSchoolYeCha', False) and const.SCHOOL_YECHA in needSchool:
                needSchool.remove(const.SCHOOL_YECHA)
            if not gameglobal.rds.configData.get('enableNewSchoolMiaoyin', False) and const.SCHOOL_MIAOYIN in needSchool:
                needSchool.remove(const.SCHOOL_MIAOYIN)
            if not gameglobal.rds.configData.get('enableNewSchoolTianZhao', False) and const.SCHOOL_TIANZHAO in needSchool:
                needSchool.remove(const.SCHOOL_TIANZHAO)
            isPublic = True
            firstKey = item.get('type', 0)
            secondKey = key
            thirdKey = 0
            info = (teamName,
             const.GROUP_GOAL_RELAXATION,
             levelMin,
             levelMax,
             needSchool,
             isPublic,
             firstKey,
             secondKey,
             thirdKey)
            self.buildGroup(info, gametypes.GROUP_TYPE_TEAM_GROUP)
            return

    def hideAllTeamTopLogo(self, bHide):
        p = BigWorld.player()
        if not p.members:
            return
        for gbId in p.members:
            tPlayerInfo = p.members[gbId]
            entityId = tPlayerInfo.get('id', 0)
            if not entityId:
                continue
            ent = BigWorld.entities.get(entityId)
            if ent:
                ent.topLogo.hideTeamLogo(bHide)
                ent.topLogo.removeTeamIdentity()
                if not bHide:
                    ent.topLogo.setTeamTopLogo(ent, AppSettings.get(keys.SET_TEAM_TOP_LOGO_MARK, 1))

    def set_groupActionState(self, old):
        if self.groupActionState == gametypes.GROUP_ACTION_STATE_PREPARE:
            p = BigWorld.player()
            if p.isInTeamOrGroup() and p.groupHeader != p.id and p.groupHeader == self.id and p.inGroupFollow:
                for questId in p.quests:
                    if QD.data.get(questId).get('teamWindowEffectNotify', 0):
                        BigWorld.flashWindow(5)
                        break

    def onSyncGroupInviteData(self, groupInviteType, groupInviteDictData):
        gameglobal.rds.ui.invitePlayer.onSyncGroupInviteData(groupInviteType, groupInviteDictData)

    def onSyncTeamHelp(self):
        pass

    def onSyncClientTeamCCInfo(self, clientTeamCCInfo):
        """
        \xe5\x85\xb7\xe4\xbd\x93\xe5\x8d\x8f\xe8\xae\xae\xe7\x9a\x84\xe6\xa0\xbc\xe5\xbc\x8f\xef\xbc\x8c\xe5\x8f\xaf\xe4\xbb\xa5\xe5\x8f\x82\xe8\x80\x83\xef\xbc\x9ahttp://km.netease.com/wiki/show?page_id=7918
        Args:
            clientTeamCCInfo:
        
        Returns:
        
        """
        pass
