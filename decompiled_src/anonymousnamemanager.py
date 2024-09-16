#Embedded file name: /WORKSPACE/data/entities/client/helpers/anonymousnamemanager.o
import BigWorld
import gameglobal
import gamelog
import gametypes
import utils
from gameclass import Singleton
from callbackHelper import Functor
from guis import worldBossHelper
from cdata import anonymous_name_manager_data as ANMD

def getInstance():
    return AnonymousNameManager.getInstance()


class AnonymousNameManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.entity = None
        self.entId = 0
        self.entGbId = 0

    def checkNeedAnonymousName(self, entity, defaultName = ''):
        anonymousType = self.checkNeedAnonymity(entity=entity)
        if anonymousType != gametypes.AnonymousType_None:
            if not entity:
                return defaultName
            if hasattr(entity, 'IsAvatar') and entity.IsAvatar:
                return self.getAnonymousData(anonymousType, gametypes.ANONYMOUS_NAME, defaultName)
            if hasattr(entity, 'IsSummonedSprite') and entity.IsSummonedSprite:
                return self.getAnonymousData(anonymousType, gametypes.ANONYMOUS_SPRITE_NAME, defaultName)
            if hasattr(entity, 'IsSummonedBeast') and entity.IsSummonedBeast:
                return self.getAnonymousData(anonymousType, gametypes.ANONYMOUS_BEAST_NAME, defaultName)
            if hasattr(entity, 'IsPuppet') and entity.IsPuppet:
                return self.getAnonymousData(anonymousType, gametypes.ANONYMOUS_NAME, defaultName)
        return defaultName

    def checkNeedAnonymousTitle(self, entity, defaultTitle = ''):
        anonymousType = self.checkNeedAnonymity(entity=entity)
        if anonymousType != gametypes.AnonymousType_None:
            if self.getAnonymousData(anonymousType, gametypes.ANONYMOUS_TOP_TITLE_HIDE, False):
                return ''
            else:
                return self.getAnonymousData(anonymousType, gametypes.ANONYMOUS_TOP_TITLE, defaultTitle)
        return defaultTitle

    def checkNeedAnonymity(self, entity = None, entId = 0, gbId = 0):
        self.entity = entity
        self.entId = entId
        self.entGbId = gbId
        for anonymousType in ANMD.data.iterkeys():
            if self._checkCanAnonymityByType(anonymousType):
                return anonymousType

        return gametypes.AnonymousType_None

    def getAnonymousData(self, anonymousType, anonymousDataType, defaultData = None):
        anonymousData = ANMD.data.get(anonymousType, {})
        if anonymousDataType == gametypes.ANONYMOUS_NAME:
            avatarEntity = self._getRealAvatarEntity(self.entity)
            if avatarEntity:
                chatAnonymity = getattr(avatarEntity, 'chatAnonymity', {})
                if anonymousType in chatAnonymity:
                    return '%s%s' % (anonymousData.get('anonymousName', defaultData), ''.join(chatAnonymity[anonymousType]))
            return anonymousData.get('anonymousName', defaultData)
        if anonymousDataType == gametypes.ANONYMOUS_SPRITE_NAME:
            return anonymousData.get('anonymousSpriteName', defaultData)
        if anonymousDataType == gametypes.ANONYMOUS_BEAST_NAME:
            return anonymousData.get('anonymousBeastName', defaultData)
        if anonymousDataType == gametypes.ANONYMOUS_TOP_TITLE:
            return anonymousData.get('anonymousTopTitle', defaultData)
        if anonymousDataType == gametypes.ANONYMOUS_TOP_TITLE_HIDE:
            return anonymousData.get('anonymousTopTitleHide', defaultData)
        if anonymousDataType == gametypes.ANONYMOUS_TOP_TITLE_EFFECT_HIDE:
            return anonymousData.get('anonymousTopTitleEffectHide', defaultData)
        if anonymousDataType == gametypes.ANONYMOUS_SKILL_EFFECT_HIDE:
            return anonymousData.get('anonymousSkillEffectHide', defaultData)
        if anonymousDataType == gametypes.ANONYMOUS_ACT_APPEARANCE_HIDE:
            return anonymousData.get('anonymousActAppearanceHide', defaultData)
        if anonymousDataType == gametypes.ANONYMOUS_MENU_HIDE:
            return anonymousData.get('anonymousMenuHide', defaultData)
        if anonymousDataType == gametypes.ANONYMOUS_GUILD_IMAGE_HIDE:
            return anonymousData.get('anonymousGuildImageHide', defaultData)
        if anonymousDataType == gametypes.ANONYMOUS_CHAT_PROXY_HIDE:
            return anonymousData.get('anonymousChatProxyHide', defaultData)
        return defaultData

    def _checkCanAnonymityByType(self, anonymousType):
        p = BigWorld.player()
        if not p:
            return False
        elif anonymousType == gametypes.AnonymousType_None:
            return False
        name = gametypes.AnonymousTypeFuncMap.get(anonymousType, None)
        if name:
            func = getattr(self, name, None)
        else:
            func = None
        if func:
            return func(anonymousType)
        else:
            return self._checkAnonymousTypeDefault(anonymousType)

    def _getRealAvatarEntity(self, entity):
        avatarEntity = entity
        if hasattr(entity, 'IsAvatar') and entity.IsAvatar:
            avatarEntity = entity
        elif hasattr(entity, 'IsSummonedSprite') and entity.IsSummonedSprite and hasattr(entity, 'getOwner'):
            avatarEntity = entity.getOwner()
        elif hasattr(entity, 'IsSummonedBeast') and entity.IsSummonedBeast and hasattr(entity, 'ownerId'):
            avatarEntity = BigWorld.entity(entity.ownerId)
        return avatarEntity

    def _checkAnonymousTypeInPUBG(self, anonymousType):
        p = BigWorld.player()
        if not p.isInPUBG():
            return False
        if self.entId:
            if self.entId == p.id:
                return False
            return not p.checkTeamMateInPUBGByEndId(self.entId)
        if self.entGbId:
            if self.entGbId == p.gbId:
                return False
            return not p.checkTeamMateInPUBG(self.entGbId)
        if self.entity:
            if self.entity.id == p.id:
                return False
            avatarEntity = self._getRealAvatarEntity(self.entity)
            if utils.instanceof(avatarEntity, 'Puppet'):
                return True
            elif hasattr(avatarEntity, 'gmMode') and avatarEntity.gmMode:
                return False
            elif avatarEntity and not p.checkTeamMateInPUBGByEndId(avatarEntity.id):
                return True
            else:
                return False
        return False

    def _checkAnonymousTypeInAssassination(self, anonymousType):
        if not gameglobal.rds.configData.get('enableAssassination', False):
            return False
        elif not self.entity:
            return False
        avatarEntity = self._getRealAvatarEntity(self.entity)
        if avatarEntity and hasattr(avatarEntity, 'assassinationKillTargetStamp') and avatarEntity.assassinationKillTargetStamp:
            return True
        else:
            return False

    def _checkAnonymousTypeWorldBoss(self, anonymousType):
        if not gameglobal.rds.configData.get('enableWorldBoss', False):
            return False
        return self._checkAnonymousTypeDefault(anonymousType)

    def _checkAnonymousTypeHuntGhost(self, anonymousType):
        if not gameglobal.rds.configData.get('enableHuntGhost', False):
            return False
        return self._checkAnonymousTypeDefault(anonymousType)

    def _checkAnonymousTypeDefault(self, anonymousType):
        if not self.entity:
            return False
        p = BigWorld.player()
        avatarEntity = self._getRealAvatarEntity(self.entity)
        anonymousData = ANMD.data.get(anonymousType, {})
        if not avatarEntity or not getattr(avatarEntity, 'chatAnonymity', {}):
            return False
        if not avatarEntity.chatAnonymity.has_key(anonymousType):
            return False
        if anonymousData.get('selfVisible', True):
            if p.id == avatarEntity.id:
                return False
        if anonymousData.get('guildMemberVisible', True):
            if p.guild and p.guild.member.has_key(getattr(avatarEntity, 'gbId', 0)):
                return False
        if anonymousData.get('gmVisible', True):
            if hasattr(avatarEntity, 'gmMode') and avatarEntity.gmMode:
                return False
        return True

    def checkCanRecvAnonyChanel(self):
        p = BigWorld.player()
        return bool(p.chatAnonymity)

    def updateEntityShowInfo(self, entity):
        if entity:
            entity.refreshTopLogo()
        if getattr(entity, 'spriteObjId', None):
            entity.refreshAvatarSummonedSpriteTopLogo()
