#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/menuManager.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import const
import uiConst
import formula
import gametypes
import gamelog
import utils
import ui
import mapGameCommon
from callbackHelper import Functor
from guis import asObject
from guis import messageBoxProxy
from gameclass import Singleton
from guis import uiUtils
from ui import unicode2gbk
from helpers import editorHelper
from gamestrings import gameStrings
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from data import menu_config_data as MCD
from data import menu_item_data as MID
from data import menu_group_data as MGD
from data import sys_config_data as SCD
from data import map_game_config_data as MGCD
from data import apprentice_config_data as ACD
from data import yabiao_config_data as YCD
from data import fb_data as FD
from data import world_war_army_data as WWAD
from data import couple_emote_basic_data as CEBD
from data import marriage_config_data as MCDD
from data import wing_world_config_data as WWCD
from data import fight_for_love_config_data as FFLCD
from data import map_config_data as MACD

def sort_menu(a, b):
    if a.get('blockId', 0) > b.get('blockId', 0):
        return 1
    if a.get('blockId', 0) < b.get('blockId', 0):
        return -1
    if a.get('sortId', 0) > b.get('sortId', 0):
        return 1
    if a.get('sortId', 0) < b.get('sortId', 0):
        return -1
    return 0


def getInstance():
    return MenuManager.getInstance()


def onGetMenuById(*args):
    menuId = args[3][0].GetNumber()
    gfxRoleName = args[3][1].GetMember('roleName')
    gfxEntityId = args[3][1].GetMember('entityId')
    gfxGbId = args[3][1].GetMember('gbId')
    gfxLv = args[3][1].GetMember('lv')
    gfxSchool = args[3][1].GetMember('school')
    gfxFid = args[3][1].GetMember('fid')
    gfxHostId = args[3][1].GetMember('hostId')
    gfxMenuData = asObject.ASObject(args[3][1].GetMember('data'))
    roleName = unicode2gbk(gfxRoleName.GetString()) if gfxRoleName else None
    entityId = gfxEntityId.GetNumber() if gfxEntityId else None
    gbId = long(gfxGbId.GetString()) if gfxGbId else None
    lv = gfxLv.GetNumber() if gfxLv else None
    school = gfxSchool.GetNumber() if gfxSchool else None
    fid = int(gfxFid.GetString()) if gfxFid else None
    hostId = int(gfxHostId.GetNumber()) if gfxHostId else None
    extraInfo = {}
    if menuId == uiConst.MENU_ARENA_PLAYOFFS_BET:
        tId = int(args[3][1].GetMember('tId').GetString())
        lvKey = args[3][1].GetMember('lvKey').GetString()
        extraInfo = {'tId': tId,
         'lvKey': lvKey}
    if not extraInfo:
        extraInfo = gfxMenuData
    getInstance().menuTarget.apply(roleName, None, entityId, gbId, lv, school, fid, menuId, hostId, extraInfo=extraInfo)
    menuList = getInstance().getMenuListById(menuId)
    return uiUtils.dict2GfxDict(menuList, True)


class MenuTarget(object):

    def __init__(self):
        self.entity = None
        self.entityId = None
        self.roleName = None
        self.roleNameDisplay = ''
        self.gbId = None
        self.lv = None
        self.school = None
        self.menuId = None
        self.fid = None
        self.hostId = None
        self.channelId = 0
        self.extraInfo = {}

    def apply(self, roleName = None, entity = None, entityId = None, gbId = None, lv = None, school = None, fid = None, menuId = 0, hostId = None, channelId = 0, extraInfo = {}):
        if fid:
            if fid != const.XINYI_MANAGER_ID:
                fVal = BigWorld.player().getFValByGbId(fid)
                if fVal:
                    roleName = fVal.name
                    gbId = fVal.gbId
                    lv = fVal.level
                    school = fVal.school
                    if not hostId:
                        hostId = getattr(fVal, 'server', None)
            else:
                p = BigWorld.player()
                xinYi = p.xinYiManager
                if xinYi:
                    roleName = xinYi['name']
        self.entity = entity
        if roleName and entity == None and entityId == None:
            entityId = uiUtils.getIdByRoleName(roleName)
        if entityId:
            ent = BigWorld.entities.get(int(entityId))
            if ent:
                self.entity = ent
        self.fid = fid
        self.entityId = self.entity.id if hasattr(self.entity, 'id') else entityId
        self.roleName = self.entity.roleName if hasattr(self.entity, 'roleName') else roleName
        self.roleNameDisplay = BigWorld.player().anonymNameMgr.checkNeedAnonymousName(self.entity, self.roleName)
        self.gbId = self.entity.gbId if hasattr(self.entity, 'gbId') else gbId
        self.lv = self.entity.lv if hasattr(self.entity, 'lv') else lv
        self.school = self.entity.school if hasattr(self.entity, 'school') else school
        self.menuId = menuId
        self.hostId = self.entity.crossFromHostId if hasattr(self.entity, 'crossFromHostId') else hostId
        self.channelId = channelId
        self.extraInfo = extraInfo

    def isSelf(self):
        return self.entity == BigWorld.player() or self.roleName == BigWorld.player().roleName or self.gbId == BigWorld.player().gbId or self.entityId == BigWorld.player().id

    def isOtherAvatar(self):
        return self.hasEntity() and self.isAvatar() and not self.isSelf()

    def isOtherRoleName(self):
        return self.roleName and not self.isSelf()

    def isFriendName(self):
        if not self.roleName:
            return False
        for gbId, friendVal in BigWorld.player().friend.iteritems():
            if friendVal.name == self.roleName and friendVal.group != 0:
                return True

        return False

    def hasEntity(self):
        return self.entity != None and self.entity.inWorld

    def isAvatar(self):
        return self.hasEntity() and (self.entity.IsAvatar or utils.instanceof(self.entity, 'Puppet'))

    def canApplyRideTogether(self, p):
        if self.hasEntity():
            if not self.isAvatar():
                return False
            ret = True
            ret &= not self.isSelf()
            ret &= not p.inRiding()
            ret &= not p.tride.inRide()
            ret &= self.entity.isOnRideTogetherHorse() or self.entity.tride.inRide()
            return ret
        else:
            return False

    def canInviteRideTogether(self, p):
        if self.hasEntity():
            if not self.isAvatar():
                return False
            ret = True
            ret &= not self.isSelf()
            ret &= p.isOnRideTogetherHorse()
            ret &= not self.entity.inRiding()
            ret &= not self.entity.tride.inRide()
            return ret
        else:
            return False

    def canUnBlock(self, p):
        if self.roleName in gameglobal.rds.ui.chat.blockList:
            return True
        return False

    def canBlock(self, p):
        if self.hasEntity() and not self.isOtherAvatar():
            return False
        if self.roleName and self.isOtherRoleName() and self.roleName not in gameglobal.rds.ui.chat.blockList:
            return True
        return False

    def canBlockTeam(self, p):
        if self.extraInfo.get('teamId', 0):
            return True
        else:
            return False

    def canInviteGuild(self, p):
        if self.hasEntity() and not self.isOtherAvatar():
            return False
        if not p.guild or self.isSelf() or self.hasEntity() and getattr(self.entity, 'guildNUID'):
            return False
        return gameglobal.rds.ui.guild.checkAuthorization(gametypes.GUILD_ACTION_INVITE_MEMBER)

    def canCopyName(self, p):
        return True

    def canSendMail(self, p):
        if self.hasEntity():
            return self.isOtherAvatar()
        return self.isOtherRoleName()

    def canChangeAlloc(self, p):
        if self.isSelf():
            if p.groupHeader == p.id:
                return True
        return False

    def canFollowMan(self, p):
        spaceNo = formula.getMapId(p.spaceNo)
        if MACD.data.get(spaceNo, {}).get('disableFollowMan', False):
            return False
        return self.isOtherAvatar()

    def canPrivateChat(self, p):
        if self.hasEntity():
            return self.isOtherAvatar()
        return self.isOtherRoleName()

    def canFocusTarget(self, p):
        if self.hasEntity() and not self.isSelf():
            return True

    def canViewEquip(self, p):
        if self.hasEntity():
            return self.isOtherAvatar()
        return self.isOtherRoleName()

    def canAddFriend(self, p):
        if self.gbId:
            if not self.isSelf():
                fVal = p.getFValByGbId(self.gbId)
                return not (fVal and p.friend.isFriendGroup(fVal.group))
        if self.hasEntity():
            return self.isOtherAvatar()
        if self.isFriendName():
            return False
        if self.isOtherRoleName():
            return True
        return False

    def canInviteTeam(self, p):
        if self.hasEntity() and not self.isOtherAvatar():
            return False
        if self.hasEntity() and self.isOtherAvatar():
            return not (p.groupNUID and p.groupNUID == self.entity.groupNUID)
        if self.roleName and not self.isSelf():
            isTeamMember = False
            for member in p._getMembers().values():
                if self.roleName == member['roleName']:
                    isTeamMember = True
                    break

            return not isTeamMember
        return False

    def canApplyTeam(self, p):
        if self.hasEntity() and self.isOtherAvatar():
            return not (p.groupNUID and p.groupNUID == self.entity.groupNUID)
        if self.isOtherRoleName():
            if not (p.isInTeam() or p.isInGroup()):
                if self.hasEntity():
                    if self.isOtherAvatar():
                        return self.entity.isInTeamOrGroup()
                    else:
                        return False
                return True
        return False

    def canApplyTeamInChat(self, p):
        if self.hasEntity() and self.isOtherAvatar():
            return not (p.groupNUID and p.groupNUID == self.entity.groupNUID)
        if self.isOtherRoleName():
            return True
        return False

    def canKickTeam(self, p):
        if self.gbId and not self.isSelf():
            isTeamMember = False
            for id in p._getMembers().keys():
                if id == self.gbId:
                    isTeamMember = True
                    break

            if (p.isInTeam() or p.isInGroup()) and p.groupHeader == p.id and isTeamMember:
                return True
        else:
            if self.hasEntity():
                return self.isOtherAvatar()
            if self.isOtherRoleName():
                return True
        return False

    def canChangeTeamLeader(self, p):
        if p.isInPUBG():
            return False
        if self.gbId and not self.isSelf():
            isTeamMember = False
            membersInfo = p._getMembers()
            if p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
                membersInfo = getattr(p, 'battleFieldTeam', {})
            if membersInfo:
                for id in membersInfo.keys():
                    if id == self.gbId:
                        isTeamMember = True
                        break

            if p.inFubenType(const.FB_TYPE_BATTLE_FIELD_FORT) and p.bfHeaderGbId == p.gbId and isTeamMember:
                return True
            if (p.isInTeam() or p.isInGroup()) and p.groupHeader == p.id and isTeamMember:
                return True
        else:
            if self.hasEntity():
                return self.isOtherAvatar()
            if self.isOtherRoleName():
                return True
        return False

    def canLeaveTeam(self, p):
        if self.isSelf():
            if p.isInPUBG():
                return False
            if (p.isInTeam() or p.isInGroup()) and not p.inFubenTypes(const.FB_TYPE_ARENA):
                return True
        return False

    def canLeaveFuben(self, p):
        if self.isSelf():
            if p.isInPUBG():
                return False
            if p.inFuben() and not p.inFubenTypes(const.FB_TYPE_ARENA):
                return True
        return False

    def canTrade(self, p):
        return self.isOtherAvatar()

    def canBindItemTrade(self, p):
        if not gameglobal.rds.configData.get('enableGroupTrade', False):
            return False
        return self.isOtherAvatar()

    def canWatchEquipment(self, p):
        return self.canViewEquip(p)

    def canFollowAvatarWatch(self, p):
        return p.inLiveOfGuildTournament or utils.inLiveOfArenaPlayoffs(p)

    def canCompareAchive(self, p):
        if self.hasEntity():
            return self.isOtherAvatar()
        return self.isOtherRoleName()

    def canQieCuo(self, p):
        if p.inFuben():
            return False
        if not p.stateMachine.checkStatus_check(const.CT_QIECUO, bMsg=False) and formula.getFubenNo(p.spaceNo) != const.FB_NO_MARRIAGE_GREAT_HALL:
            return False
        return self.isOtherAvatar()

    def canLeaveDiGong(self, p):
        lineNo, _ = formula.getMLInfo(p.spaceNo)
        if self.isSelf():
            if lineNo >= 0 and p.inBossRoom():
                return True
        return False

    def canProsecute(self, p):
        if self.isOtherAvatar() if self.hasEntity() else self.isOtherRoleName():
            return True
        elif self.gbId:
            return self.gbId != str(p.gbId)
        else:
            return False

    def canCarrierHeaderExchangeSeat(self, p):
        if p.isOnCarrier():
            if not p.isTeamLeader():
                return False
            if p.id not in p.carrier:
                return False
        elif p.isOnWingWorldCarrier():
            if not self.entityId:
                return False
            if p.wingWorldCarrier.getCarrierHeaderEntId() != p.id:
                return False
        return True

    def canCarrierKickOffMember(self, p):
        if p.isOnCarrier():
            if not p.isTeamLeader():
                return False
            if not self.entityId:
                return False
        elif p.isOnWingWorldCarrier():
            if p.wingWorldCarrier.getCarrierHeaderEntId() != p.id:
                return False
            if not self.entityId:
                return False
        return True

    def canCarrierExchangeCarrierSeat(self, p):
        if p.isOnCarrier():
            if p.isTeamLeader():
                return False
            if not self.entityId:
                return False
            if self.entityId == p.id:
                return False
        elif p.isOnWingWorldCarrier():
            if not self.entityId:
                return False
            if p.wingWorldCarrier.getCarrierHeaderEntId() == p.id:
                return False
            if self.extraInfo.carrierIndex == const.CARRIER_MAJOR_IDX:
                return False
        return True

    def canCarrierMoveToEmpty(self, p):
        if self.entityId:
            return False
        if self.extraInfo.carrierIndex == const.CARRIER_MAJOR_IDX:
            return False
        return True

    def canCarrierRequestDrive(self, p):
        if p.isOnCarrier():
            if p.isTeamLeader():
                return False
        elif p.isOnWingWorldCarrier():
            if p.wingWorldCarrier.getCarrierHeaderEntId() == p.id:
                return False
        if self.extraInfo.carrierIndex != const.CARRIER_MAJOR_IDX:
            return False
        return True

    def canShoutu(self, p):
        if gameglobal.rds.ui.mentor.enableApprentice():
            if not p.checkMentorCondition():
                return False
            if not (hasattr(p, 'canbeMentor') and p.canbeMentor):
                return False
            if self.lv:
                if self.lv > ACD.data.get('maxApprenticeLv', 50) or self.lv < ACD.data.get('minApprenticeLv', 19):
                    return False
            if self.hasEntity():
                if self.isOtherAvatar():
                    if not self.entity.checkApprenticeCondition():
                        return False
                    if hasattr(p, 'apprenticeGbIds'):
                        for gbId, _ in p.apprenticeGbIds:
                            if gbId == self.gbId:
                                return False

                    return True
                else:
                    return False
            return self.isOtherRoleName()
        if p.enableNewApprentice():
            if not p.checkMentorConditionEx():
                return False
            if self.hasEntity():
                if self.isOtherAvatar():
                    if not self.entity.checkApprenticeConditionEx():
                        return False
                    if hasattr(p, 'apprenticeGbIds'):
                        for gbId, _ in p.apprenticeGbIds:
                            if gbId == self.gbId:
                                return False

                    return True
                else:
                    return False
            return self.isOtherRoleName()

    def canBaishi(self, p):
        if gameglobal.rds.ui.mentor.enableApprentice():
            if not p.checkApprenticeCondition():
                return False
            if hasattr(p, 'mentorGbId') and p.mentorGbId:
                return False
            if self.hasEntity():
                if self.isOtherAvatar():
                    return self.entity.checkMentorCondition()
                else:
                    return False
            if self.lv:
                if self.lv < ACD.data.get('minMentorLv', 50):
                    return False
            return self.isOtherRoleName()
        if p.enableNewApprentice():
            if not p.checkApprenticeConditionEx():
                return False
            if self.gbId and self.gbId in p.apprenticeInfo.keys():
                return False
            if self.hasEntity():
                if self.isOtherAvatar():
                    return self.entity.checkMentorConditionEx()
                else:
                    return False
            return self.isOtherRoleName()

    def canChuangong(self, p):
        if gameglobal.rds.ui.mentor.enableApprentice():
            if self.isOtherAvatar():
                if not p.checkMentorCondition():
                    return False
                if hasattr(p, 'apprenticeGbIds'):
                    for gbId, graduate in p.apprenticeGbIds:
                        if gbId == self.gbId and not graduate:
                            return True

        if p.enableNewApprentice():
            if self.isOtherAvatar():
                if not p.checkMentorConditionEx():
                    return False
                if hasattr(p, 'apprenticeGbIds'):
                    for gbId, graduate in p.apprenticeGbIds:
                        if gbId == self.gbId and not graduate:
                            return True

        return False

    def canMark(self, p):
        if self.entity and self.entity.__class__.__name__ == 'HomeFurniture':
            return False
        ret = False
        if self.entityId:
            if p.isInPUBG():
                ret = False
            elif p.isInGroup():
                isHeader = p.members.get(p.gbId, {}).get('isHeader', 0)
                isAssistant = p.members.get(p.gbId, {}).get('isAssistant', 0)
                if isHeader or isAssistant:
                    ret = True
            elif p.isInTeam():
                if p.groupHeader == p.id:
                    ret = True
        return ret

    def canAddBlack(self, p):
        return self.isOtherRoleName()

    def canSingleChat(self, p):
        return self.isOtherRoleName()

    def getTargetInfo(self):
        schoolColor = SCD.data.get('schoolColor', {}).get(self.school, '#000000')
        schoolName = const.SCHOOL_DICT.get(self.school, '')
        return (uiUtils.toHtml(self.roleNameDisplay, schoolColor), uiUtils.toHtml('%s[%d]' % (schoolName, self.lv), schoolColor))

    def canBeginChat(self, p):
        return self.fid

    def canMoveToBlack(self, p):
        if self.gbId:
            if not self.isSelf():
                fVal = p.getFValByGbId(self.gbId)
                return not (fVal and p.friend.isBlockGroup(fVal.group))
        return self.fid

    def canRemoveFriend(self, p):
        return self.fid

    def canViewChatLog(self, p):
        return self.fid

    def canMoveOutBlack(self, p):
        return self.fid

    def canDeletePeople(self, p):
        return self.fid

    def canInvitedCC(self, p):
        return self.fid and gameglobal.rds.configData.get('isCCVersion', False)

    def canAddYixinFriend(self, p):
        return gameglobal.rds.configData.get('enableYixin', False)

    def canViewFriendProfile(self, p):
        return self.fid

    def canMoveFriend(self, p):
        return self.fid

    def canShowFriendWish(self, p):
        return self.fid

    def canAccreditAssistant(self, p):
        if self.hasEntity() and not self.isOtherAvatar():
            return False
        elif self.isSelf():
            return False
        else:
            if p.isInGroup() and p.groupHeader == p.id:
                tmpGbId = None
                if self.gbId:
                    tmpGbId = self.gbId
                elif self.roleName:
                    tmpGbId = getInstance()._getGbIdByRoleName(self.roleName)
                if tmpGbId in p.members.keys():
                    memberData = p.members.get(tmpGbId, {})
                    isAssistant = memberData.get('isAssistant', False)
                    return not isAssistant and memberData.get('isOn', False)
            return False

    def canRelieveAssistant(self, p):
        if self.hasEntity() and not self.isOtherAvatar():
            return False
        elif self.isSelf():
            return False
        else:
            if p.isInGroup() and p.groupHeader == p.id:
                tmpGbId = None
                if self.gbId:
                    tmpGbId = self.gbId
                elif self.roleName:
                    tmpGbId = getInstance()._getGbIdByRoleName(self.roleName)
                if tmpGbId in p.members.keys():
                    memberData = p.members.get(tmpGbId, {})
                    isAssistant = memberData.get('isAssistant', False)
                    return isAssistant and memberData.get('isOn', False)
            return False

    def canApprenticeDimiss(self, p):
        if p.enableNewApprentice():
            if not self.gbId or self.isSelf():
                return False
            if self.gbId in p.apprenticeInfo.keys():
                return True
            apprenticeInfo = p.getApprenticeInfo(self.gbId)
            if apprenticeInfo:
                return True
        else:
            if not gameglobal.rds.ui.mentor.enableApprentice():
                return False
            if not self.gbId or self.isSelf():
                return False
            if getattr(p, 'mentorGbId', None) == self.gbId:
                return True
            apprenticeInfo = p.getApprenticeInfo(self.gbId)
            if apprenticeInfo:
                return True
        return False

    def canKickoutChatRoom(self, p):
        if not p.chatRoomName:
            return False
        if self.hasEntity() and not self.isOtherAvatar():
            return False
        return self.isOtherRoleName()

    def canAddBusiness(self, p):
        if not gameglobal.rds.configData.get('enableGuildBusiness', False):
            return False
        if not gameglobal.rds.ui.guild.checkAuthorization(gametypes.GUILD_ACTION_APPOINT):
            return False
        guild = p.guild
        if not guild:
            return False
        for gbId, member in guild.member.iteritems():
            if member.role == self.roleName:
                if gbId in guild.businessMan:
                    return False
                else:
                    return True

        return False

    def canRemoveBusiness(self, p):
        if not gameglobal.rds.configData.get('enableGuildBusiness', False):
            return False
        if not gameglobal.rds.ui.guild.checkAuthorization(gametypes.GUILD_ACTION_APPOINT):
            return False
        guild = p.guild
        if not guild:
            return False
        for gbId, member in guild.member.iteritems():
            if member.role == self.roleName:
                if gbId in guild.businessMan:
                    return True
                else:
                    return False

        return False

    def canAddRemark(self, p):
        if self.fid and self.menuId == uiConst.MENU_FRIEND:
            fVal = p.friend.get(self.fid)
            if fVal:
                return not fVal.remarkName
        return False

    def canModifyRemark(self, p):
        if self.fid and self.menuId == uiConst.MENU_FRIEND:
            fVal = p.friend.get(self.fid)
            if fVal:
                return fVal.remarkName
        return False

    def canCallFriend(self, p):
        if self.fid in gameglobal.rds.ui.friend.inviteList:
            return True
        else:
            return False

    def canResignWWArmyPost(self, p):
        if self.gbId == p.gbId:
            postId = p.worldWar.getPostByGbId()
            if postId:
                return not WWAD.data.get(postId, {}).get('byVote', 0)
        return False

    def canCreateTeam(self, p):
        if p.isInPUBG():
            return False
        if self.gbId == p.gbId and not p.groupNUID:
            return True
        return False

    def canOpenZoneOther(self, p):
        p = BigWorld.player()
        if not self.gbId and not self.roleName:
            return False
        if self.entity and not self.isAvatar():
            return False
        if p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            return False
        return True

    def canRefreshPartnerPhoto(self, p):
        if self.gbId and p.partner:
            return True
        return False

    def canVisitHome(self, p):
        if not self.gbId and not self.roleName:
            return False
        if self.entity and not self.isAvatar():
            return False
        return True

    def canQuitSprite(self, p):
        return True

    def canCloseBloodTips(self, p):
        return True

    def canOpenBloodTips(self, p):
        return True

    def canRemovePlayoffsMember(self, p):
        if self.gbId in p.getArenaPlayoffsMember() and p.getArenaPlayoffsTeamHeader() == p.gbId and self.gbId != p.gbId:
            return True
        return False

    def canViewModelFitting(self, p):
        return True

    def canDressUpModelFitting(self, p):
        if not self.entity or not self.entity.inWorld:
            return False
        if not hasattr(self.entity, 'ownerUUID'):
            return False
        if editorHelper.instance().ownerGbID == BigWorld.player().gbId:
            info = editorHelper.instance().findBWObject(self.entity.ownerUUID)
            if info and info.ownerGbID == BigWorld.player().gbId:
                return True
        if editorHelper.instance().ownerGbID == BigWorld.player().friend.intimacyTgt:
            info = editorHelper.instance().findBWObject(self.entity.ownerUUID)
            if info and info.ownerGbID == BigWorld.player().gbId:
                return True
        return False

    def canTryOnModelFitting(self, p):
        return True

    def canShowAPTeamInfo(self, p):
        return True

    def canApplyCoupleEmote_1(self, p):
        return self.canApplyCoupleEmote(1, p)

    def canApplyCoupleEmote_10004(self, p):
        return self.canApplyCoupleEmote(10004, p)

    def canApplyCoupleEmote_10005(self, p):
        return self.canApplyCoupleEmote(10005, p)

    def canApplyCoupleEmote_10006(self, p):
        return self.canApplyCoupleEmote(10006, p)

    def canApplyCoupleEmote_10007(self, p):
        return self.canApplyCoupleEmote(10007, p)

    def canApplyCoupleEmote(self, coupleEmoteId, p):
        cebd = CEBD.data.get(coupleEmoteId)
        if cebd.get('needFlag') and not p.getEmoteEnableFlags(coupleEmoteId):
            return False
        return True

    def canBeApplyCoupleEmote_1(self, p):
        return True

    def canBeApplyCoupleEmote_10004(self, p):
        return True

    def canBeApplyCoupleEmote_10005(self, p):
        return True

    def canBeApplyCoupleEmote_10006(self, p):
        return True

    def canBeApplyCoupleEmote_10007(self, p):
        return True

    def canInviteGroupFollow(self, p):
        return p.isTeamLeader() and not p.getIsAllFollow()

    def canCancelGroupFollow(self, p):
        return p.isTeamLeader() and not p.getIsAllNotFollow()

    def canChangeTeam2Group(self, p):
        return p.isTeamLeader()

    def canSendToTeamChannel(self, p):
        return True

    def canSendToGuildChannel(self, p):
        return p.guildNUID > 0

    def canSendToSchoolChannel(self, p):
        return True

    def canMapGameWorldChannel(self, p):
        return True

    def canMapGameGuildChannel(self, p):
        return p.guildNUID > 0

    def canMapGameTeamChannel(self, p):
        return True

    def canMapGameCrossChannel(self, p):
        return True

    def canMapGameAreaChannel(self, p):
        return True

    def canMapGameActivityChannel(self, p):
        return True

    def canChangeTeamInfo(self, p):
        return True

    def canOpenSummonSprite(self, p):
        return True

    def canOpenHotKey(self, p):
        return True

    def canQuestTrackSetting(self, p):
        return True

    def canQuestTrackAlpha(self, p):
        return True

    def canBeginGroupChat(self, p):
        return True

    def canAddGroupFriend(self, p):
        return True

    def canOpenNotDisturb(self, p):
        groupNUID = self.extraInfo.get('groupNUID', 0)
        members = p.groupChatData.get(groupNUID, {}).get('members', {})
        msgAcceptOp = 0
        if p.gbId in members:
            msgAcceptOp = members[p.gbId][3]
        if msgAcceptOp:
            return False
        return True

    def canCloseNotDisturb(self, p):
        groupNUID = self.extraInfo.get('groupNUID', 0)
        members = p.groupChatData.get(groupNUID, {}).get('members', {})
        msgAcceptOp = 0
        if p.gbId in members:
            msgAcceptOp = members[p.gbId][3]
        if msgAcceptOp:
            return True
        return False

    def canQuitGroupChat(self, p):
        return True

    def canSeparateChat(self, p):
        return True

    def canMergeChat(self, p):
        return True

    def canIssueAssassination(self, p):
        if not gameglobal.rds.configData.get('enableAssassination', False):
            return False
        if p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            return False
        if not self.gbId and not self.roleName:
            return False
        if self.entity and not self.isAvatar():
            return False
        if self.isSelf():
            return False
        if self.hostId and self.hostId != utils.getHostId():
            return False
        return True


class MenuManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.MsgBoxId = None
        self.menuTarget = MenuTarget()
        self.funcMenuTarget = MenuTarget()
        self.clickMenuItemLabel = None

    def openZoneOther(self):
        if self.menuTarget.gbId or self.menuTarget.roleName:
            p = BigWorld.player()
            p.getPersonalSysProxy().hide()
            srcId = self.menuTarget.menuId if self.menuTarget.menuId else 0
            hostId = 0 if not self.menuTarget.hostId else int(self.menuTarget.hostId)
            p.getPersonalSysProxy().openZoneOther(self.menuTarget.gbId, self.menuTarget.roleName, srcId, hostId)

    def refreshPartnerPhoto(self):
        p = BigWorld.player()
        if self.menuTarget.gbId and p.partner:
            if self.menuTarget.gbId == p.gbId:
                gameglobal.rds.ui.partnerMain.refreshPhotoByGbId(self.menuTarget.gbId)
            else:
                p.cell.querySinglePartnerEquipment(self.menuTarget.gbId)

    def visitHome(self):
        if self.menuTarget.gbId or self.menuTarget.roleName:
            msg = gameStrings.MSG_TELEPORT_HOME % self.menuTarget.roleName
            p = BigWorld.player()
            gbId = self.menuTarget.gbId
            roleName = self.menuTarget.roleName if self.menuTarget.roleName else ''
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.visitRoom, gbId, roleName, self.menuTarget.hostId))

    def getJudgeFuncName(self, name):
        ff = list(name)
        ff[0] = ff[0].upper()
        ff = 'can' + ''.join(ff)
        return ff

    def onMenuItemClick(self, menuName, menuId, menuLabel):
        self.menuTarget.menuId = menuId
        self.clickMenuItemLabel = uiUtils.textToHtml(menuLabel)
        if menuName:
            func = getattr(self, menuName, None)
            if func:
                func()
            else:
                gamelog.warning('@zhp not menu Func', menuName, menuId, menuLabel)
        elif self.menuTarget.gbId and menuName:
            func = getattr(self, menuName, None)
            if func:
                func()

    def defaultFunc(self):
        p = BigWorld.player()
        p.showGameMsg(GMDD.data.STILL_UNDER_DEVELOPING, ())

    def copyName(self):
        BigWorld.setClipBoardText(self.menuTarget.roleName)

    def sendMail(self):
        gameglobal.rds.ui.mail.receiverName = self.menuTarget.roleName
        if gameglobal.rds.ui.mail.mediator:
            gameglobal.rds.ui.mail.gotoSendPanel(self.menuTarget.roleName)
        else:
            gameglobal.rds.ui.mail.show(mailBoxType=1)

    def applyRideTogether(self):
        p = BigWorld.player()
        if self.menuTarget.isOtherAvatar():
            if hasattr(self.menuTarget.entity, 'tride') and self.menuTarget.entity.tride.inRide():
                p.applyForRideTogether(self.menuTarget.entity.tride.header)
            else:
                p.applyForRideTogether(self.menuTarget.entity.id)

    def inviteRideTogether(self):
        if self.menuTarget.isOtherAvatar():
            p = BigWorld.player()
            p.inviteRideTogether(self.menuTarget.entity.id)

    def unBlock(self):
        if self.menuTarget.roleName in gameglobal.rds.ui.chat.blockList:
            gameglobal.rds.ui.chat.blockList.remove(self.menuTarget.roleName)

    def inviteGuild(self):
        if self.menuTarget.roleName:
            BigWorld.player().cell.inviteGuildMember(self.menuTarget.roleName)

    def changeAlloc(self):
        gamelog.debug('changeAlloc')
        p = BigWorld.player()
        if p.isInTeam():
            gameglobal.rds.ui.memberDetailsV2.show()
        elif p.isInGroup():
            gameglobal.rds.ui.group.showGroupInfoPanel()

    def followMan(self):
        p = BigWorld.player()
        if p.inGroupFollow:
            p.showGameMsg(GMDD.data.GROUPFOLLOW_FORBIDDEN_FOLLOW, ())
            return
        if self.menuTarget.isOtherAvatar():
            gamelog.debug('followMan')
            p.followOtherAvatar(self.menuTarget.entity)

    def privateChat(self):
        gamelog.debug('privateChat')
        gameglobal.rds.ui.chat.showView()
        gameglobal.rds.ui.chat.updateChatTarge(self.menuTarget.roleNameDisplay)
        gameglobal.rds.ui.chat.setCurChannel(const.CHAT_CHANNEL_SINGLE, '', True)

    def focusTarget(self):
        gamelog.debug('focusTarget')
        gameglobal.rds.ui.focusTarget.menuShowFocus(self.menuTarget.entity.id)

    def viewEquip(self):
        gamelog.debug('viewEquip')
        if self.menuTarget.roleName != gameglobal.rds.ui.targetRoleInfo.roleName:
            p = BigWorld.player()
            p.cell.getEquipment(self.menuTarget.roleName)

    def addFriend(self, srcId = 0):
        gamelog.debug('addFriend')
        p = BigWorld.player()
        if not self.menuTarget.gbId:
            self.menuTarget.gbId = p.friend.roleName2GbId(self.menuTarget.roleName)
        if self.menuTarget.gbId:
            fVal = p.getFValByGbId(self.menuTarget.gbId)
            if fVal and (not p.friend.has_key(self.menuTarget.gbId) or p.friend.isFriend(self.menuTarget.gbId)):
                p.showGameMsg(GMDD.data.HAS_FRIEND, ())
                return
        if not self.menuTarget.hostId or self.menuTarget.hostId == utils.getHostId():
            try:
                srcId = srcId or int(self.menuTarget.channelId if self.menuTarget.channelId > 0 else self.menuTarget.menuId)
                group = p.friend.defaultGroup if p.friend.defaultGroup else gametypes.FRIEND_GROUP_FRIEND
                if self.menuTarget.roleName:
                    p.base.addContact(str(self.menuTarget.roleName), group, srcId)
                elif self.menuTarget.gbId:
                    p.base.addContactByGbId(self.menuTarget.gbId, group, srcId)
            except:
                srcId = 0
                group = 0
                msg = gameStrings.TEXT_MENUMANAGER_1095 % (self.menuTarget.channelId,
                 self.menuTarget.menuId,
                 p.friend.defaultGroup,
                 self.menuTarget.roleName)
                BigWorld.player().reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_CRITICAL, [msg], 0, {})

        else:
            if not gameglobal.rds.configData.get('enableGlobalFriend', False):
                return
            if self.menuTarget.gbId:
                p.base.addRemoteFriendRequest(self.menuTarget.hostId, self.menuTarget.gbId)
            elif self.menuTarget.roleName:
                p.base.addRemoteFriendRequestByName(self.menuTarget.hostId, self.menuTarget.roleName)

    def inviteTeam(self):
        gamelog.debug('inviteTeam')
        if self.menuTarget.roleName == None:
            return
        else:
            p = BigWorld.player()
            tgtRoleName = self.menuTarget.roleName
            if p.inFubenTypes(const.FB_TYPE_ARENA):
                BigWorld.player().showTopMsg(gameStrings.TEXT_MENUMANAGER_1116)
                return
            if tgtRoleName == p.realRoleName:
                p.chatToEventEx(gameStrings.TEXT_MENUMANAGER_1120, const.CHANNEL_COLOR_GREEN)
                return
            if not (p.isInTeam() or p.isInGroup()) or p.isHeader() or p.isAssistant():
                p.inviteGroup(tgtRoleName)
            else:
                p.recommendGroup(tgtRoleName)
            return

    def applyTeam(self):
        p = BigWorld.player()
        tgtRoleName = self.menuTarget.roleName
        if tgtRoleName == p.realRoleName:
            return
        elif p.inFubenTypes(const.FB_TYPE_ARENA):
            p.showGameMsg(GMDD.data.ARENA_FORBIDDEN_WITH_TEAM, ())
            return
        elif p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            p.showGameMsg(GMDD.data.BATTLE_FIELD_FORBIDDEN_WITH_TEAM, ())
            return
        else:
            if self.menuTarget.roleName != None:
                p.applyGroup(self.menuTarget.roleName)
            return

    def kickTeam(self):
        gamelog.debug('kickTeam')
        p = BigWorld.player()
        if self.menuTarget.gbId != None:
            p.deleteMemFromTeam(self.menuTarget.gbId, self.menuTarget.roleName)
        elif self.menuTarget.roleName:
            gbId = self._getGbIdByRoleName(self.menuTarget.roleName)
            if gbId:
                p.deleteMemFromTeam(gbId, self.menuTarget.roleName)

    def changeTeamLeader(self):
        gamelog.debug('applyTeamHeader')
        p = BigWorld.player()
        if self.menuTarget.gbId:
            if p.inFubenType(const.FB_TYPE_BATTLE_FIELD_FORT):
                p.cell.abdicatedBattleFieldGroup(self.menuTarget.gbId)
            else:
                p.cell.abdicatedGroup(self.menuTarget.gbId)
        elif self.menuTarget.roleName:
            gbId = self._getGbIdByRoleName(self.menuTarget.roleName)
            if gbId:
                if p.inFubenType(const.FB_TYPE_BATTLE_FIELD_FORT):
                    p.cell.abdicatedBattleFieldGroup(self.menuTarget.gbId)
                else:
                    p.cell.abdicatedGroup(gbId)

    def leaveTeam(self):
        gamelog.debug('leaveTeam')
        p = BigWorld.player()
        if p.yabiaoData:
            msg = YCD.data.get('yabiaoLeaveTeamMsg', gameStrings.TEXT_MENUMANAGER_1176)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, p.quitGroup)
            return
        fbNo = formula.getFubenNo(p.spaceNo)
        if p.inFuben() and formula.whatFubenType(fbNo) in (const.FB_TYPE_GROUP,):
            MBButton = messageBoxProxy.MBButton
            buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(p.quitGroup)), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1)]
            gameglobal.rds.ui.messageBox.show(True, '', gameStrings.TEXT_MENUMANAGER_1184, buttons)
        elif gameglobal.rds.ui.questTrack.needShowConfirmView():
            MBButton = messageBoxProxy.MBButton
            buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(p.quitGroup)), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1)]
            msg = uiUtils.getTextFromGMD(GMDD.data.QUEST_CHAIN_LEAVE_TEAM_WARNING)
            gameglobal.rds.ui.messageBox.show(True, '', msg, buttons)
        else:
            p.quitGroup()

    def leaveFuben(self):
        gamelog.debug('leaveFuben')
        p = BigWorld.player()
        fbNo = formula.getFubenNo(p.spaceNo)
        fbType = formula.whatFubenType(fbNo)
        MBButton = messageBoxProxy.MBButton
        gamelog.debug('zt: show quitFuben confirm', fbType)
        buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(self.confirmOK, fbType)), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1)]
        fd = FD.data.get(fbNo, {})
        if fbType == const.FB_TYPE_FIGHT_FOR_LOVE:
            txt = gameStrings.FIGHT_FOR_LOVE_LEAVE_FUBEN
            if p.fightForLovePhase in (gametypes.FIGHT_FOR_LOVE_PHASE_PREPARE, gametypes.FIGHT_FOR_LOVE_PHASE_END):
                pass
            elif p.fightForLoveCreaterRole == const.FIGHT_FOR_LOVE_CREATER:
                txt = FFLCD.data.get('createrLeaveFubenMsg', '')
            else:
                txt = FFLCD.data.get('fighterLeaveFubenMsg', '')
            fbExitMsgBoxId = gameglobal.rds.ui.messageBox.show(True, '', txt, buttons)
        elif fd.get('leaveDestroy'):
            txt = GMD.data.get(GMDD.data.FB_EXIT_CONFIRM_WITH_DESTROY, {}).get('text')
            fbExitMsgBoxId = gameglobal.rds.ui.messageBox.show(True, '', txt, buttons)
        elif gameglobal.rds.configData.get('enableNewMatchRuleSSC', False) and fbType in (const.FB_TYPE_SHENGSICHANG, const.FB_TYPE_TEAM_SHENGSICHANG):
            msg = SCD.data.get('sscQuitConfirmText', gameStrings.SSC_QUIT_FB_CONFIRM)
            buttons = [MBButton(gameStrings.SSC_QUIT_BTN_CONFIRM, Functor(self.confirmOK, fbType)), MBButton(gameStrings.SSC_QUIT_BTN_CANCEL)]
            fbExitMsgBoxId = gameglobal.rds.ui.messageBox.show(True, '', msg, buttons)
        else:
            fbExitMsgBoxId = gameglobal.rds.ui.messageBox.show(True, '', gameStrings.TEXT_MENUMANAGER_1222, buttons)
        p.fbExitMsgBoxIds = getattr(p, 'fbExitMsgBoxIds', [])
        p.fbExitMsgBoxIds.append(fbExitMsgBoxId)

    def confirmOK(self, fbType):
        p = BigWorld.player()
        p.clearInDyingEntity()
        if fbType in (const.FB_TYPE_GROUP,):
            p.cell.exitFuben()
        elif fbType in const.FB_TYPE_SINGLE_SET:
            enableTeleportSpell = gameglobal.rds.configData.get('enableTeleportSpell', False)
            if enableTeleportSpell:
                p.enterTeleportSpell(gameglobal.TELEPORT_SPELL_LEAVE_FUBEN, p.cell.exitSingleFuben)
            else:
                p.cell.exitSingleFuben()
        elif fbType in const.FB_TYPE_BATTLE_FIELD:
            p.cell.quitBattleField()
        elif fbType == const.FB_TYPE_SHENGSICHANG:
            p.cell.leaveShengSiChang()
        elif fbType == const.FB_TYPE_TEAM_SHENGSICHANG:
            p.cell.leaveTeamShengSiChang()
        elif fbType in const.FB_TYPE_GUILD_CHALLENGE:
            p.cell.leaveGuildChallenge()
        elif fbType == const.FB_TYPE_FIGHT_FOR_LOVE:
            p.cell.leaveFightForLove()
        elif fbType == const.FB_TYPE_SCHOOL_TOP_MATCH:
            p.cell.leaveSchoolTopMatch()
        if getattr(p, 'inGroupFollow', None) and not getattr(p, 'groupHeader', None) == p.id:
            p.cell.cancelGroupFollow()

    def trade(self):
        enableTradeMode = gameglobal.rds.configData.get('enableTradeMode', False)
        if not enableTradeMode:
            return
        gamelog.debug('trade')
        BigWorld.player().checkSetPassword(self.trueTrade)

    def bindItemTrade(self):
        BigWorld.player().checkSetPassword(self.trueBindItemTrade)

    def trueTrade(self):
        if self.menuTarget.isOtherAvatar():
            p = BigWorld.player()
            p.cell.tradeRequest(self.menuTarget.entity.id)

    def trueBindItemTrade(self):
        if self.menuTarget.isOtherAvatar():
            p = BigWorld.player()
            p.cell.itemGiveRequest(self.menuTarget.entity.id)

    def qieCuo(self):
        p = BigWorld.player()
        if self.menuTarget.isOtherAvatar():
            p.sendQieCuoRequest(self.menuTarget.entity.id)

    def leaveDiGong(self):
        p = BigWorld.player()
        lineNo, _ = formula.getMLInfo(p.spaceNo)
        if not p.inBossRoom() or lineNo < 0:
            return
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, self.confirmLeaveDiGong), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1, self.cancelLeaveDiGong)]
        spaceName = const.ML_SPACE[formula.getMLNo(p.spaceNo)].get('name', '')
        self.MsgBoxId = gameglobal.rds.ui.messageBox.show(True, '', gameStrings.TEXT_MENUMANAGER_1290 % spaceName, buttons)

    def prosecute(self):
        if self.menuTarget.menuId == uiConst.MENU_CHAT:
            gameglobal.rds.ui.prosecute.show(self.menuTarget.roleName, self.menuTarget.menuId)
        elif self.menuTarget.menuId == uiConst.MENU_ANONYMOUS:
            gameglobal.rds.ui.prosecute.show(self.menuTarget.gbId, self.menuTarget.menuId)
        elif self.menuTarget.isOtherAvatar():
            gameglobal.rds.ui.prosecute.show(self.menuTarget.roleName, uiConst.MENU_TARGET, getattr(self.menuTarget.entity, 'boothName', ''))
        else:
            gameglobal.rds.ui.prosecute.show(self.menuTarget.roleName, self.menuTarget.menuId)

    def shoutu(self):
        if self.menuTarget.roleName:
            p = BigWorld.player()
            if gameglobal.rds.ui.mentor.enableApprentice():
                p.cell.applyApprentice(self.menuTarget.roleName)
            elif p.enableNewApprentice():
                p.base.applyApprenticeEx(self.menuTarget.roleName)

    def baishi(self):
        p = BigWorld.player()
        if self.menuTarget.roleName:
            if gameglobal.rds.ui.mentor.enableApprentice():
                p.cell.applyMentor(self.menuTarget.roleName)
            elif p.enableNewApprentice():
                p.base.applyMentorEx(self.menuTarget.roleName)

    def chuangong(self):
        p = BigWorld.player()
        if (gameglobal.rds.ui.mentor.enableApprentice() or p.enableNewApprentice()) and self.menuTarget.isOtherAvatar():
            p.applyTraining(self.menuTarget.entityId)

    def confirmLeaveDiGong(self):
        BigWorld.player().cell.leaveBossRoom(0)
        self.MsgBoxId = None

    def cancelLeaveDiGong(self):
        self.MsgBoxId = None

    def inviteGuildCC(self):
        if self.menuTarget.roleName:
            p = BigWorld.player()
            selMember = None
            for mid in BigWorld.player().guild.member:
                member = BigWorld.player().guild.member[mid]
                if member.role == self.menuTarget.roleName and member.role != p.realRoleName:
                    selMember = member

            if not selMember:
                return
            if selMember.online:
                p.doInviteOtherCCGuild(self.menuTarget.roleName)
            else:
                p.showGameMsg(GMDD.data.CC_PLAYER_OFFLINE, self.menuTarget.roleName)

    def addBlack(self):
        if self.menuTarget.roleName:
            p = BigWorld.player()
            p.base.addContact(self.menuTarget.roleName, gametypes.FRIEND_GROUP_BLOCK, 0)

    def singleChat(self):
        if self.menuTarget.roleName:
            gameglobal.rds.ui.chat.updateChatTarge(self.menuTarget.roleName)
            gameglobal.rds.ui.chat.setCurChannel(const.CHAT_CHANNEL_SINGLE, '', True)

    def inviteJoin(self):
        if self.menuTarget.roleName:
            p = BigWorld.player()
            if p.inFubenTypes(const.FB_TYPE_ARENA):
                BigWorld.player().showTopMsg(gameStrings.TEXT_MENUMANAGER_1116)
                return
            if self.menuTarget.roleName == p.realRoleName:
                p.chatToEventEx(gameStrings.TEXT_MENUMANAGER_1120, const.CHANNEL_COLOR_GREEN)
                return
            if not (p.isInTeam() or p.isInGroup()) or p.isHeader() or p.isAssistant():
                p.inviteGroup(self.menuTarget.roleName)
            else:
                p.recommendGroup(self.menuTarget.roleName)

    def applyJoin(self):
        if self.menuTarget.roleName:
            p = BigWorld.player()
            if p.inFubenTypes(const.FB_TYPE_ARENA):
                p.showGameMsg(GMDD.data.ARENA_FORBIDDEN_WITH_TEAM, ())
                return
            if p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
                p.showGameMsg(GMDD.data.BATTLE_FIELD_FORBIDDEN_WITH_TEAM, ())
                return
            p.applyGroup(self.menuTarget.roleName)

    def watchEquipment(self):
        if self.menuTarget.roleName:
            p = BigWorld.player()
            p.cell.getEquipment(self.menuTarget.roleName)

    def followAvatarWatch(self):
        if self.menuTarget.roleName:
            p = BigWorld.player()
            if utils.isCrossArenaPlayoffsFb(formula.getFubenNo(p.spaceNo)):
                p.cell.followAvatarWithLiveInArena(self.menuTarget.roleName)
            else:
                p.cell.followAvatarWithLiveInBattleField(self.menuTarget.roleName)

    def carrierHeaderExchangeSeat(self):
        gamelog.debug('-----m.l@MenuManager.carrierHeaderExchangeSeat', self.menuTarget.entityId, self.menuTarget.extraInfo.carrierIndex)
        p = BigWorld.player()
        if p.isOnCarrier():
            p.cell.applyExchangeCarrierSeat(self.menuTarget.extraInfo.carrierIndex)
        elif p.isOnWingWorldCarrier():
            p.cell.applyExchangeWingWorldCarrierSeat(self.menuTarget.extraInfo.carrierIndex)

    def carrierKickOffMember(self):
        gamelog.debug('-----m.l@MenuManager.carrierKickOffMember', self.menuTarget, self.menuTarget.entityId)
        p = BigWorld.player()
        if p.isOnCarrier():
            p.cell.kickoutTeamMateByHeader(self.menuTarget.entityId)
        elif p.isOnWingWorldCarrier():
            p.cell.applyKickoutWingWorldCarrierPlayer(self.menuTarget.extraInfo.carrierIndex)

    def carrierExchangeCarrierSeat(self):
        gamelog.debug('-----m.l@MenuManager.carrierExchangeCarrierSeat', self.menuTarget.entityId, self.menuTarget.extraInfo.carrierIndex)
        p = BigWorld.player()
        if p.isOnCarrier():
            p.cell.applyExchangeCarrierSeat(self.menuTarget.extraInfo.carrierIndex)
        elif p.isOnWingWorldCarrier():
            p.cell.applyExchangeWingWorldCarrierSeat(self.menuTarget.extraInfo.carrierIndex)

    def carrierMoveToEmpty(self):
        gamelog.debug('-----m.l@MenuManager.carrierMoveToEmpty', self.menuTarget.entityId, self.menuTarget.extraInfo.carrierIndex)
        p = BigWorld.player()
        if p.isOnCarrier():
            p.cell.applyEnterCarrierByIdx(self.menuTarget.extraInfo.carrierIndex)
        elif p.isOnWingWorldCarrier():
            dist = p.qinggongMgr.getDistanceFromGround()
            if dist != p.flyHeight and dist < WWCD.data.get('heightForLeaveCarrier', 5):
                p.cell.applyExchangeWingWorldCarrierSeat(self.menuTarget.extraInfo.carrierIndex)
            else:
                p.showGameMsg(GMDD.data.UNABLE_TO_MOVE_EMPTY_SEAT, ())

    def carrierRequestDrive(self):
        gamelog.debug('-----m.l@MenuManager.carrierRequestDrive', self.menuTarget.entityId, self.menuTarget.extraInfo.carrierIndex)
        p = BigWorld.player()
        if p.isOnCarrier():
            p.cell.applyExchangeCarrierSeat(self.menuTarget.extraInfo.carrierIndex)
        elif p.isOnWingWorldCarrier():
            p.cell.applyExchangeWingWorldCarrierSeat(self.menuTarget.extraInfo.carrierIndex)

    def compareAchive(self):
        if self.menuTarget.isOtherRoleName():
            gameglobal.rds.ui.achvmentDiff.otherName = self.menuTarget.roleName
            gameglobal.rds.ui.achvment.getAchieveData(True)
            BigWorld.player().base.inquiryOtherAchieveByRole(self.menuTarget.roleName)

    def block(self):
        if self.menuTarget.roleName not in gameglobal.rds.ui.chat.blockList:
            gameglobal.rds.ui.chat.blockList.append(self.menuTarget.roleName)
            BigWorld.player().showGameMsg(GMDD.data.CHAT_BLOCK_ADD, ())

    def blockTeam(self):
        teamId = self.menuTarget.extraInfo.get('teamId', 0)
        if teamId:
            if teamId not in gameglobal.rds.ui.chat.teamBlockList:
                gameglobal.rds.ui.chat.teamBlockList.append(teamId)
                BigWorld.player().showGameMsg(GMDD.data.CHAT_SHARE_TEAM_BLOCK_ADD, ())

    def kickoutChatRoom(self):
        p = BigWorld.player()
        if not p.chatRoomName:
            p.showGameMsg(GMDD.data.CHATROOM_AUTHORIZATION_FAILED, ())
            return
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_MENUMANAGER_1467 % self.menuTarget.roleName, Functor(self.dokickoutChatRoom, self.menuTarget.roleName))

    def dokickoutChatRoom(self, roleName):
        BigWorld.player().cell.kickoutChatRoom(roleName)

    def beginChat(self):
        gameglobal.rds.ui.friend.beginChat(self.menuTarget.fid)

    def moveToBlack(self):
        gameglobal.rds.ui.friend.moveToBlack(self.menuTarget.fid)

    def removeFriend(self):
        gameglobal.rds.ui.friend.removeFriend(self.menuTarget.fid)

    def viewChatLog(self):
        gameglobal.rds.ui.friend.viewChatLog(self.menuTarget.fid)

    def moveOutBlack(self):
        gameglobal.rds.ui.friend.moveOutBlack(self.menuTarget.fid)

    def deletePeople(self):
        group = 0
        if self.menuTarget.menuId == uiConst.MENU_FRIEND_ENEMY:
            group = gametypes.FRIEND_GROUP_ENEMY
        elif self.menuTarget.menuId == uiConst.MENU_FRIEND_BLOCK:
            group = gametypes.FRIEND_GROUP_BLOCK
        gameglobal.rds.ui.friend.deletePeople(self.menuTarget.fid, group=group)

    def invitedCC(self):
        gameglobal.rds.ui.friend.invitedCC(self.menuTarget.fid)

    def addYixinFriend(self):
        gameglobal.rds.ui.friend.addYixinFriend(self.menuTarget.fid)

    def moveFriend(self):
        if self.clickMenuItemLabel == gameStrings.TEXT_FRIENDPROXY_362:
            gameglobal.rds.ui.friend.showNewGroupBox(True, self.menuTarget.fid)
        else:
            gameglobal.rds.ui.friend.moveToGroup(self.menuTarget.fid, self.clickMenuItemLabel)

    def viewFriendProfile(self):
        gameglobal.rds.ui.friend.viewFriendProfile(self.menuTarget.fid)

    def showFriendWish(self):
        BigWorld.player().base.queryFriendWish(self.menuTarget.fid)

    def quitSprite(self):
        gameglobal.rds.ui.spriteAni.disappear()

    def closeBloodTips(self):
        gameglobal.rds.ui.spriteAni.isOpenBloodTips = False
        gameglobal.rds.ui.spriteAni.refreshMenu()

    def openBloodTips(self):
        gameglobal.rds.ui.spriteAni.isOpenBloodTips = True
        gameglobal.rds.ui.spriteAni.refreshMenu()

    def accreditAssistant(self):
        p = BigWorld.player()
        if self.menuTarget.isOtherRoleName():
            p.cell.accreditAssistant(self.menuTarget.roleName)

    def relieveAssistant(self):
        p = BigWorld.player()
        if self.menuTarget.isOtherRoleName():
            p.cell.relieveAssistant(self.menuTarget.roleName)

    def apprenticeDimiss(self):
        if self.menuTarget.gbId and not self.menuTarget.isSelf():
            gbId = self.menuTarget.gbId
            p = BigWorld.player()
            if p.enableNewApprentice():
                if gbId in p.apprenticeInfo.keys():
                    p.kickMentorCheckSoleEx(gbId)
                    return
                apprenticeInfo = p.getApprenticeInfo(gbId)
                if apprenticeInfo:
                    gbId, gradute = apprenticeInfo
                    p.kickApprenticeCheckSoleEx(gbId)
            else:
                if gbId == getattr(p, 'mentorGbId', None):
                    p.cell.kickMentor()
                    return
                apprenticeInfo = p.getApprenticeInfo(gbId)
                if apprenticeInfo:
                    gbId, gradute = apprenticeInfo
                    p.base.kickApprentice(gbId)

    def addRemark(self):
        gameglobal.rds.ui.friend.showAddRemark(self.menuTarget.fid)

    def modifyRemark(self):
        gameglobal.rds.ui.friend.showModifyRemark(self.menuTarget.fid)

    def callFriend(self):
        gameglobal.rds.ui.callFriend.show(self.menuTarget.fid)

    def resignWWArmyPost(self):
        msg = uiUtils.getTextFromGMD(GMDD.data.WW_ARMY_RESIGN_MSG, '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, BigWorld.player().cell.resignWWArmyPost)

    def createTeam(self):
        gameglobal.rds.ui.team.onQuickCreateClick()

    def openSummonSprite(self):
        gameglobal.rds.ui.summonedWarSprite.show(uiConst.WAR_SPRITE_TAB_INDEX0)

    def openHotKey(self):
        gameglobal.rds.ui.gameSetting.show(uiConst.GAME_SETTING_BG_V2_TAB_KEY)

    def _getGbIdByRoleName(self, name):
        p = BigWorld.player()
        if not p.isInTeamOrGroup():
            return
        else:
            if hasattr(p, 'arrangeDict'):
                for item in p.arrangeDict.keys():
                    info = p.members.get(item)
                    if info == None:
                        continue
                    roleName = info['roleName']
                    if roleName == name:
                        return item

            return

    def _getGroup(self, fid):
        p = BigWorld.player()
        fVal = p.friend.get(fid)
        if not fVal:
            return
        groups = p.getFriendGroupOrder()
        ret = []
        for group in groups:
            if group == fVal.group or not p.friend.isFriendGroup(group):
                continue
            name = p.friend.groups.get(group)
            if not name:
                continue
            ret.append(uiUtils.htmlToText(name))

        if len(groups) < const.FRIEND_CUSTOM_GROUP_MAX:
            ret.append(gameStrings.TEXT_FRIENDPROXY_362)
        return ret

    def addBusiness(self):
        p = BigWorld.player()
        guild = p.guild
        if not guild:
            return
        for gbId, member in guild.member.iteritems():
            if member.role == self.menuTarget.roleName:
                p.cell.addGuildBusinessMan(gbId)
                return

    def removeBusiness(self):
        p = BigWorld.player()
        guild = p.guild
        if not guild:
            return
        for gbId, member in guild.member.iteritems():
            if member.role == self.menuTarget.roleName:
                p.cell.removeGuildBusinessMan(gbId)
                return

    def removePlayoffsMember(self):
        p = BigWorld.player()
        if self.menuTarget.gbId in p.getArenaPlayoffsMember().keys():
            msg = uiUtils.getTextFromGMD(GMDD.data.KICK_OUT_ARENA_PLAYOFFS_TEAM_MSG, '%s') % self.menuTarget.roleName
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.kickoutArenaPlayoffsTeam, self.menuTarget.gbId, self.menuTarget.roleName))

    def viewModelFitting(self):
        target = self.menuTarget.entity
        if not target or not getattr(target, 'ownerUUID', 0):
            return
        equips, aspect, physique, avatarConfig, actionId, itemPlusInfo = editorHelper.instance().getPhysiqueInfo(target.ownerUUID)
        equipment = target.equips
        uiUtils.setItemPlusInfo(equipment, itemPlusInfo)
        gameglobal.rds.ui.modelRoleInfo.showRoleInfo(target, target.equips, target.realSchool, target.realAspect, target.realPhysique, target.avatarConfig, False, '')

    def dressUpModelFitting(self):
        gameglobal.rds.ui.modelFittingRoom.show(self.menuTarget.entity)

    def tryOnModelFitting(self):
        target = self.menuTarget.entity
        if not target:
            return
        if hasattr(target, 'equips'):
            BigWorld.player().tryOnModel(target.equips)

    def showAPTeamInfo(self):
        tId = self.menuTarget.extraInfo.get('tId', 0)
        lvKey = self.menuTarget.extraInfo.get('lvKey', '')
        gameglobal.rds.ui.arenaPlayoffs.showArenaPlayoffsTeamInfo(tId, self.menuTarget.hostId, '', 0, lvKey)

    def getMenuListById(self, menuId):
        p = BigWorld.player()
        if menuId == uiConst.MENU_TARGET and p.inLiveOfGuildTournament:
            menuId = uiConst.MENU_IN_LIVE
        self.menuTarget.menuId = menuId
        if menuId in (uiConst.MENU_TARGET, uiConst.MENU_ENTITY) and (p.isInSSCorTeamSSC() or p.inFightForLoveFb() and self.menuTarget.entity.IsAvatar and not self.menuTarget.entity.isFightForLoveCreator()):
            return {}
        if self.menuTarget and self.menuTarget.entity and getattr(self.menuTarget.entity, 'jctSeq', 0):
            return {}
        anonymousType = p.anonymNameMgr.checkNeedAnonymity(entity=self.menuTarget.entity)
        if anonymousType != gametypes.AnonymousType_None:
            if p.anonymNameMgr.getAnonymousData(anonymousType, gametypes.ANONYMOUS_MENU_HIDE, False):
                return {}
        mcdData = MCD.data.get(menuId, {})
        if gameglobal.rds.configData.get('enableNewMenu', False) and mcdData.get('useNewMenu', 0):
            return self.getNewMenuListById(menuId)
        targetInfo = []
        if (menuId == uiConst.MENU_CHAT or mcdData.get('showRoleInfo', False)) and self.menuTarget.lv and self.menuTarget.school:
            targetInfo = self.menuTarget.getTargetInfo()
        menuList = self.createMenuList(menuId)
        canMark = self.menuTarget.canMark(p) and not mcdData.get('noAppendMarkMenu', 0)
        return {'targetInfo': targetInfo,
         'canMark': canMark,
         'menuList': menuList,
         'menuId': menuId,
         'useNewMenu': False}

    def getNewMenuListById(self, menuId):
        p = BigWorld.player()
        mcdData = MCD.data.get(menuId, {})
        targetInfo = {}
        if (menuId == uiConst.MENU_CHAT or mcdData.get('showRoleInfo', False)) and self.menuTarget.lv and self.menuTarget.school:
            schoolColor = SCD.data.get('schoolColor', {}).get(self.menuTarget.school, '#000000')
            playerName = '%s[%d]' % (self.menuTarget.roleNameDisplay, self.menuTarget.lv)
            playerName = uiUtils.toHtml(playerName, schoolColor)
            targetInfo['playerName'] = playerName
            targetInfo['school'] = self.menuTarget.school
        elif mcdData.get('showItemInfo', False):
            targetInfo['itemName'] = ''
        groupMap = {}
        resultList = []
        menuList = self.createMenuList(menuId)
        for menuInfo in menuList:
            midData = MID.data.get(menuInfo['funcName'], {})
            menuInfo['iconPath'] = 'menu/%d.dds' % midData.get('icon', 0) if midData.get('icon', 0) else ''
            if midData.get('specialBlockId', {}).has_key(menuId):
                menuInfo['blockId'] = midData.get('specialBlockId', {}).get(menuId, 0)
            else:
                menuInfo['blockId'] = midData.get('blockId', 0)
            if midData.get('specialSortId', {}).has_key(menuId):
                menuInfo['sortId'] = midData.get('specialSortId', {}).get(menuId, 0)
            else:
                menuInfo['sortId'] = midData.get('sortId', 0)
            if midData.get('specialGroupId', {}).has_key(menuId):
                groupId = midData.get('specialGroupId', {}).get(menuId, 0)
            else:
                groupId = midData.get('groupId', 0)
            mgdData = MGD.data.get(groupId, {})
            if mgdData:
                if groupId in groupMap:
                    groupInfo = groupMap[groupId]
                else:
                    groupInfo = {'label': mgdData.get('groupName', ''),
                     'funcName': '',
                     'childMenu': [],
                     'blockId': mgdData.get('blockId', 0),
                     'sortId': mgdData.get('sortId', 0),
                     'iconPath': 'menu/%d.dds' % mgdData.get('icon', 0) if mgdData.get('icon', 0) else ''}
                    groupMap[groupId] = groupInfo
                    resultList.append(groupInfo)
                childMenu = groupInfo.get('childMenu', [])
                childMenu.append(menuInfo)
            else:
                resultList.append(menuInfo)

        resultList.sort(cmp=sort_menu)
        for menuInfo in groupMap.itervalues():
            childMenu = menuInfo.get('childMenu', [])
            childMenu.sort(cmp=sort_menu)

        canMark = self.menuTarget.canMark(p) and not mcdData.get('noAppendMarkMenu', 0)
        return {'targetInfo': targetInfo,
         'canMark': canMark,
         'menuList': resultList,
         'menuId': menuId,
         'useNewMenu': True}

    def createMenuList(self, menuId):
        p = BigWorld.player()
        if formula.spaceInWorldWar(p.spaceNo):
            if self.menuTarget.roleName:
                sameServer = int(utils.fromSameServerByName(p.roleName, self.menuTarget.roleName))
            else:
                sameServer = True
            if sameServer and not p._isSoul():
                worldWarMenuBlack = ()
            else:
                worldWarMenuBlack = SCD.data.get('worldWarMenuBlack', {}).get(sameServer, ())
        else:
            worldWarMenuBlack = ()
        if formula.spaceInWingCity(p.spaceNo):
            if self.menuTarget.roleName:
                sameServer = int(utils.fromSameServerByName(p.roleName, self.menuTarget.roleName))
            else:
                sameServer = True
            if sameServer:
                wingCityMenuBlack = ()
                if p.isWingWorldCampMode() and p.inWingWarCity() and self.menuTarget.entity:
                    if p.wingWorldCamp != getattr(self.menuTarget.entity, 'wingWorldCamp', 0):
                        wingCityMenuBlack = ('inviteTeam', 'applyTeam')
            else:
                wingCityMenuBlack = SCD.data.get('worldWarMenuBlack', {}).get(sameServer, ())
                if p.isWingWorldCampMode() and p.inWingWarCity() and self.menuTarget.entity:
                    if p.wingWorldCamp == getattr(self.menuTarget.entity, 'wingWorldCamp', 0):
                        wingCityMenuBlack = [ funcName for funcName in wingCityMenuBlack if funcName not in ('inviteTeam', 'applyTeam') ]
                elif p.isWingWorldCampMode() and p.inWingWarCity() and not self.menuTarget.entity:
                    wingCityMenuBlack = [ funcName for funcName in wingCityMenuBlack if funcName not in ('inviteTeam', 'applyTeam') ]
        else:
            wingCityMenuBlack = ()
        marriageCrossMenuBlack = ()
        if p.inMarriageHall() and (p._isSoul() or utils.getHostId() != self.menuTarget.hostId):
            marriageCrossMenuBlack = MCDD.data.get('marriageCrossMenuBlack', ())
        crossServerRankMenuBlack = ()
        if menuId == uiConst.MENU_RANK and self.menuTarget.hostId:
            if utils.getHostId() != self.menuTarget.hostId:
                crossServerRankMenuBlack = SCD.data.get('crossServerRankMenuBlack', ())
        yanWuTangMenuBlack = SCD.data.get('yanWuTangMenuBlack', ())
        crossServerMenuBlack = SCD.data.get('crossServerMenuBlack', ())
        mcdData = MCD.data.get(menuId, {})
        menuList = []
        menuData = mcdData.get('menuList', {})
        for name, label in menuData:
            if name in marriageCrossMenuBlack:
                continue
            if name in worldWarMenuBlack:
                continue
            if name in wingCityMenuBlack:
                continue
            if name in crossServerRankMenuBlack:
                continue
            if formula.isCrossServerML(formula.getMLGNo(p.spaceNo)):
                if name in yanWuTangMenuBlack:
                    continue
            elif getattr(p, 'crossServerFlag', None) == const.CROSS_SERVER_STATE_IN:
                if name in crossServerMenuBlack:
                    if name == 'qieCuo' and p.crossServerGoal == gametypes.SOUL_OUT_GOAL_BY_NPC_FOR_ACTIVITY:
                        pass
                    elif not p.inWorldWarEx() and not p.inWingCity() and not p.crossServerGoal == gametypes.SOUL_OUT_GOAL_CROSS_CLAN_WAR:
                        continue
                    elif name.find('Team') == -1:
                        continue
            if name == 'moveFriend':
                groups = self._getGroup(self.menuTarget.fid)
                if groups:
                    childMenu = [ {'label': groupName,
                     'funcName': 'moveFriend'} for groupName in groups ]
                    menuList.append({'label': label,
                     'funcName': name,
                     'childMenu': childMenu})
                continue
            func = getattr(self.menuTarget, self.getJudgeFuncName(name), None)
            if not func:
                gamelog.warning('@zhp createMenuList func no define', menuId, self.menuTarget, self.getJudgeFuncName(name))
            elif func(p):
                menuList.append({'label': label,
                 'funcName': name})

        return menuList

    def applyCoupleEmote_1(self):
        self.applyCoupleEmote(1)

    def applyCoupleEmote_10004(self):
        self.applyCoupleEmote(10004)

    def applyCoupleEmote_10005(self):
        self.applyCoupleEmote(10005)

    def applyCoupleEmote_10006(self):
        self.applyCoupleEmote(10006)

    def applyCoupleEmote_10007(self):
        self.applyCoupleEmote(10007)

    def applyCoupleEmote(self, coupleEmoteId):
        target = self.menuTarget.entity
        if not target:
            return
        p = BigWorld.player()
        if target.coupleEmote:
            p.showGameMsg(GMDD.data.INTERACTIVE_FAILED_FULL, ())
            return
        if p.coupleEmote:
            return
        p.ap.seekPath(target.position, Functor(self._applyCoupleEmote, coupleEmoteId, target.id))

    def _applyCoupleEmote(self, coupleEmoteId, targetId, result):
        p = BigWorld.player()
        p.ap.forwardMagnitude = 0
        p.ap.updateVelocity()
        target = BigWorld.entity(targetId)
        if not target or not target.inWorld:
            return
        p.ap.setYaw(target.yaw)
        p.cell.testApplyCoupleEmote(coupleEmoteId, targetId)

    def beApplyCoupleEmote_1(self):
        self.beApplyCoupleEmote(1)

    def beApplyCoupleEmote_10004(self):
        self.beApplyCoupleEmote(10004)

    def beApplyCoupleEmote_10005(self):
        self.beApplyCoupleEmote(10005)

    def beApplyCoupleEmote_10006(self):
        self.beApplyCoupleEmote(10006)

    def beApplyCoupleEmote_10007(self):
        self.beApplyCoupleEmote(10007)

    def beApplyCoupleEmote(self, coupleEmoteId):
        target = self.menuTarget.entity
        if not target or not target.inWorld:
            return
        p = BigWorld.player()
        if target.coupleEmote:
            p.showGameMsg(GMDD.data.INTERACTIVE_FAILED_FULL, ())
            return
        if p.coupleEmote:
            return
        p.ap.seekPath(target.position, Functor(self._beApplyCoupleEmote, coupleEmoteId, target.id))

    def _beApplyCoupleEmote(self, coupleEmoteId, targetId, result):
        p = BigWorld.player()
        p.ap.forwardMagnitude = 0
        p.ap.updateVelocity()
        target = BigWorld.entity(targetId)
        if not target or not target.inWorld:
            return
        p.ap.setYaw(target.yaw)
        p.cell.testBeApplyCoupleEmote(coupleEmoteId, targetId)

    def inviteGroupFollow(self):
        gameglobal.rds.ui.teamComm.onInviteGroupFollow()

    def cancelGroupFollow(self):
        gameglobal.rds.ui.teamComm.onCancelGroupFollow()

    def changeTeam2Group(self):
        p = BigWorld.player()
        if p.lv >= SCD.data.get('team2GroupLv', 35):
            gameglobal.rds.ui.team.onChangeToGroup()
        else:
            p.showGameMsg(GMDD.data.TEAM2GROUP_DISABLE_MSG, ())

    @ui.callFilter(5)
    def sendToTeamChannel(self):
        p = BigWorld.player()
        msg = gameglobal.rds.ui.team.getShareTeamInfoMsg()
        p.cell.chatToGroupInfo(msg)

    @ui.callFilter(5)
    def sendToGuildChannel(self):
        p = BigWorld.player()
        msg = gameglobal.rds.ui.team.getShareTeamInfoMsg()
        p.cell.chatToGuild(msg, True)

    @ui.callFilter(5)
    def sendToSchoolChannel(self):
        p = BigWorld.player()
        msg = gameglobal.rds.ui.team.getShareTeamInfoMsg()
        p.cell.chatToSchool(msg)

    @ui.callFilter(30)
    def mapGameWorldChannel(self):
        p = BigWorld.player()
        gridId = self.menuTarget.extraInfo.gridId
        serverName = self.menuTarget.extraInfo.serverName
        playerName = self.menuTarget.extraInfo.playerName
        gridType = mapGameCommon.getConfigVal(gridId, 'type', 0)
        msgId = MGCD.data.get('mapGameCallAttackMsgId', {}).get(gridType, 0)
        msg = GMD.data.get(msgId).get('text', 'test') % (serverName, playerName, gridId)
        p.cell.chatToWorld(msg, False)

    @ui.callFilter(30)
    def mapGameGuildChannel(self):
        p = BigWorld.player()
        gridId = self.menuTarget.extraInfo.gridId
        serverName = self.menuTarget.extraInfo.serverName
        playerName = self.menuTarget.extraInfo.playerName
        gridType = mapGameCommon.getConfigVal(gridId, 'type', 0)
        msgId = MGCD.data.get('mapGameCallAttackMsgId', {}).get(gridType, 0)
        msg = GMD.data.get(msgId).get('text', 'test') % (serverName, playerName, gridId)
        p.cell.chatToGuild(msg, True)

    @ui.callFilter(10)
    def mapGameTeamChannel(self):
        p = BigWorld.player()
        gridId = self.menuTarget.extraInfo.gridId
        serverName = self.menuTarget.extraInfo.serverName
        playerName = self.menuTarget.extraInfo.playerName
        gridType = mapGameCommon.getConfigVal(gridId, 'type', 0)
        msgId = MGCD.data.get('mapGameCallAttackMsgId', {}).get(gridType, 0)
        msg = GMD.data.get(msgId).get('text', 'test') % (serverName, playerName, gridId)
        p.cell.chatToGroupInfo(msg)

    @ui.callFilter(30)
    def mapGameAreaChannel(self):
        p = BigWorld.player()
        gridId = self.menuTarget.extraInfo.gridId
        serverName = self.menuTarget.extraInfo.serverName
        playerName = self.menuTarget.extraInfo.playerName
        gridType = mapGameCommon.getConfigVal(gridId, 'type', 0)
        msgId = MGCD.data.get('mapGameCallAttackMsgId', {}).get(gridType, 0)
        msg = GMD.data.get(msgId).get('text', 'test') % (serverName, playerName, gridId)
        p.cell.chatToSpace(msg)

    @ui.callFilter(60)
    def mapGameActivityChannel(self):
        p = BigWorld.player()
        gridId = self.menuTarget.extraInfo.gridId
        p.cell.callAttackMapGame(gridId)

    @ui.callFilter(60)
    def mapGameCrossChannel(self):
        p = BigWorld.player()
        gridId = self.menuTarget.extraInfo.gridId
        p.cell.callAttackMapGame(gridId)

    def changeTeamInfo(self):
        gameglobal.rds.ui.createTeamV2.show()

    def questTrackSetting(self):
        gameglobal.rds.ui.questTrack.handleClickTabSetting()

    def questTrackAlpha(self):
        gameglobal.rds.ui.questTrack.handleClickAlpha()

    def beginGroupChat(self):
        groupNUID = self.menuTarget.extraInfo.get('groupNUID', 0)
        gameglobal.rds.ui.friend.openGroupChat(groupNUID)

    def addGroupFriend(self):
        groupNUID = self.menuTarget.extraInfo.get('groupNUID', 0)
        gameglobal.rds.ui.groupChatMembers.show(uiConst.GROUP_CHAT_MEMBERS_TYPE_INVITE, groupNUID)

    def openNotDisturb(self):
        groupNUID = self.menuTarget.extraInfo.get('groupNUID', 0)
        p = BigWorld.player()
        p.base.setChatGroupAcceptOp(groupNUID, gametypes.CHAT_GROUP_AVOID_ACCEPT_OP_OPEN, utils.getHostId())

    def closeNotDisturb(self):
        groupNUID = self.menuTarget.extraInfo.get('groupNUID', 0)
        p = BigWorld.player()
        p.base.setChatGroupAcceptOp(groupNUID, gametypes.CHAT_GROUP_AVOID_ACCEPT_OP_CLOSE, utils.getHostId())

    def quitGroupChat(self):
        groupNUID = self.menuTarget.extraInfo.get('groupNUID', 0)
        gamelog.info('@yj .. quitGroupChat .. groupNUID=', groupNUID)
        gameglobal.rds.ui.groupChatRoom.quitGroupChatRoom(groupNUID)

    def separateChat(self):
        gbId = self.menuTarget.gbId
        groupNUID = self.menuTarget.extraInfo.get('groupNUID', 0)
        gamelog.info('@yj .. separateChat .. gbId, groupNUID=', gbId, groupNUID)
        gameglobal.rds.ui.groupChat.sureSeparateChat(gbId, groupNUID)

    def mergeChat(self):
        gbId = self.menuTarget.gbId
        groupNUID = self.menuTarget.extraInfo.get('groupNUID', 0)
        if gbId:
            gameglobal.rds.ui.chatToFriend.surePlayerMergeChat(gbId)
        elif groupNUID:
            gameglobal.rds.ui.groupChatRoom.sureGroupMergeChat(groupNUID)

    def issueAssassination(self):
        p = BigWorld.player()
        gbId = self.menuTarget.gbId
        roleName = self.menuTarget.roleName
        if gbId:
            p.base.searchAssassinationTarget(gbId)
        elif roleName:
            p.base.searchFriendByName(gametypes.SEARCH_PLAYER_FOR_FRIEND, roleName)
        gameglobal.rds.ui.assassinationMain.showAssIssuePanel()
