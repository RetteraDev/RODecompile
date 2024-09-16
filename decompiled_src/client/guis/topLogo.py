#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/topLogo.o
from gamestrings import gameStrings
import random
import BigWorld
import Scaleform
import GUI
import Math
import gamelog
import utils
import const
import gameglobal
import gametypes
import const
import uiConst
import uiUtils
import formula
import keys
import groupUtils
import clientcom
import gameconfigCommon
from uiConst import emoteMap
from gameclass import Singleton
from appSetting import Obj as AppSettings
from guis import richTextUtils
from callbackHelper import Functor
from gamestrings import gameStrings
from data import monster_model_client_data as NMMD
from data import npc_model_client_data as NCD
from data import treasure_box_data as TBD
from data import emote_data as ED
from data import quest_box_data as QBD
from data import map_config_data as MCD
from data import sys_config_data as SCD
from data import booth_skin_data as BSD
from data import interactive_data as IAD
from data import effect_title_data as ETD
from data import world_war_army_data as WWAD
from data import summon_beast_data as SBD
from data import zaiju_data as ZD
from data import duel_config_data as DCD
from data import wing_world_config_data as WWCD
from data import clan_courier_config_data as CCCD
from data import summon_sprite_data as SSD
from data import hunt_ghost_config_data as HGCD
from guis.ui import gbk2unicode
EMOTE_PATH_PREFIX = 'emote/'
FINDLOGO_PATH_PREFIX = '../findLogo/'
BOOTH_PATH_PREFIX = '../booth/'
EFFECT_TITLE_PREFIX = 'dynamicTitle/'
UI_VIEW = 0
TOPLOGO_VIEW = 1
TOPLOGOANI_VIEW = 2
NEEDUPDATATIME = 50
NEEDUPDATATIME_MAX = 999999
DYNAMIC_MC_TYPE_NONE = 0
DYNAMIC_MC_TYPE_BLOOD_DOTA_ENEMY = 1
DYNAMIC_MC_TYPE_BLOOD_DOTA_TEAMMATE = 2
DMG_ABSORB_TYPE_NORMAL = 1
DMG_ABSORB_TYPE_MAGIC = 2

class TopLogoCache(object):

    def __init__(self, maxCacheCount):
        self.cache = []
        self.maxCacheCount = maxCacheCount

    def getFromCache(self):
        if len(self.cache) > 0:
            return self.cache.pop()
        else:
            return None

    def addToCache(self, obj):
        self.cache.append(obj)

    def getCacheCount(self):
        return len(self.cache)

    def clearCache(self):
        self.cache = []


class GuiFlashObj(object):

    def __init__(self):
        self._obj = None
        self.cache = TopLogoCache(0)

    def createObj(self, entity):
        pass

    def get_from_cache(self, entity):
        obj = self.cache.getFromCache()
        if obj:
            obj.reset(entity)
            obj.visible = True
            return obj
        else:
            return self.createObj(entity)

    def add_to_cache(self, topLogo):
        pass

    def clear_cache(self):
        self.cache.clearCache()


class TopLogoObj(GuiFlashObj):
    __metaclass__ = Singleton

    def __init__(self):
        self._obj = None
        self.cache = TopLogoCache(0)

    def createObj(self, entity):
        if gameglobal.rds.isSinglePlayer:
            return None
        else:
            en = BigWorld.entity(entity)
            obj = GUI.WorldFlash(entity, TOPLOGO_VIEW)
            obj.fadeStart = 15
            obj.fadeEnd = 40
            obj.maxDistance = 40
            try:
                obj.visibleControl = False
            except:
                pass

            obj.size = (256, 256)
            obj.visible = True
            alphaShader = GUI.AlphaShader('ALL')
            alphaShader.alpha = 1
            alphaShader.speed = 0
            obj.addShader(alphaShader, 'alphaShader')
            obj.autoAlphaShade = True
            obj.materialFX = 'BLEND'
            return obj

    def add_to_cache(self, topLogo):
        if topLogo and topLogo.gui:
            if self.cache.getCacheCount() < self.cache.maxCacheCount:
                self.cache.addToCache(topLogo.gui)
                topLogo.gui = None
            else:
                topLogo.gui = None


class TopLogoAniObj(GuiFlashObj):
    __metaclass__ = Singleton

    def __init__(self):
        self._obj = None
        self.cache = TopLogoCache(10)

    def createObj(self, entity):
        en = BigWorld.entity(entity)
        obj = GUI.WorldFlash(entity, TOPLOGOANI_VIEW)
        obj.fadeStart = 15
        obj.fadeEnd = 40
        obj.maxDistance = 40
        try:
            obj.visibleControl = False
        except:
            pass

        obj.size = (256, 256)
        obj.visible = True
        alphaShader = GUI.AlphaShader('ALL')
        alphaShader.alpha = 1
        alphaShader.speed = 0
        obj.addShader(alphaShader, 'alphaShader')
        obj.autoAlphaShade = True
        obj.materialFX = 'BLEND'
        return obj

    def add_to_cache(self, topLogo):
        if topLogo and topLogo.guiAni:
            if self.cache.getCacheCount() < self.cache.maxCacheCount:
                self.cache.addToCache(topLogo.guiAni)
                topLogo.guiAni = None
            else:
                topLogo.guiAni = None


class TopLogoManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        path = 'gui/widgets/TopLogo.swf'
        if gameglobal.rds.ui.isUIPublished():
            path = 'gui/widgets/TopLogo.gfx'
        self.moviedef = Scaleform.MovieDef(path)
        self.movie = self.moviedef.createInstance(True, TOPLOGO_VIEW)
        self.movie.backgroundAlpha = 0.0
        self.setFontSize(AppSettings.get(keys.SET_UI_SCALEDATA_TOPLOGO, uiConst.DEFAULT_FONT_SIZE))

    def setGuiStateChange(self, entityId, isChange):
        if entityId == 0:
            entityId = BigWorld.player().id
        en = BigWorld.entity(entityId)
        if en and en.inWorld:
            en.topLogoIsChange = isChange

    def setGuiAllStateChange(self, isChange):
        entities = BigWorld.entities.values()
        for en in entities:
            if en and en.inWorld:
                en.topLogoIsChange = isChange

    def setFontSize(self, size):
        self.movie.invoke(('_root.setFontSize', Scaleform.GfxValue(size)))
        self.setGuiAllStateChange(True)

    def addTopLogo(self, enId):
        self.movie.invoke(('_root.addTopLogo', Scaleform.GfxValue(enId)))
        self.setGuiStateChange(enId, True)

    def removeTopLogo(self, enId):
        self.movie.invoke(('_root.removeTopLogo', Scaleform.GfxValue(enId)))
        self.setGuiStateChange(enId, True)

    def getMc(self, enId):
        self.movie.invoke('getMc', Scaleform.GfxValue(self.entity))
        self.setGuiStateChange(enId, True)

    def refreshQuestIcon(self, idArr):
        params = idArr.split('&')
        for param in params:
            itemArr = param.split(',')
            eId = itemArr[0]
            if not eId:
                continue
            isShow = itemArr[1]
            en = BigWorld.entity(int(eId))
            if en and hasattr(en, 'topLogo'):
                en.topLogo.setQuestIconVisible(int(isShow))

    def callTopLogoInvokes(self, enId, args):
        entity = BigWorld.entity(enId)
        if not entity or not entity.inWorld or not entity.topLogo or not entity.topLogo.gui:
            return
        argsList = ['_root.callTopLogoInvokes', Scaleform.GfxValue(len(args))]
        for arg in args:
            argsList.append(Scaleform.GfxValue(len(arg)))
            for ag in arg:
                argsList.append(ag)

        argsList[1] = Scaleform.GfxValue(len(tuple(argsList)) - 1)
        self.movie.invoke(tuple(argsList))
        self.setGuiStateChange(enId, True)


class TopLogoAniManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        path = 'gui/widgets/TopLogoAni.swf'
        if gameglobal.rds.ui.isUIPublished():
            path = 'gui/widgets/TopLogoAni.gfx'
        self.moviedef = Scaleform.MovieDef(path)
        self.movie = self.moviedef.createInstance(True, TOPLOGOANI_VIEW)
        self.movie.backgroundAlpha = 0.0
        self.movie.setExternalInterfaceCallback(self._callback)

    def addTopLogoAni(self, enId):
        self.movie.invoke(('_root.addTopLogo', Scaleform.GfxValue(enId)))

    def removeTopLogoAni(self, enId):
        self.movie.invoke(('_root.removeTopLogo', Scaleform.GfxValue(enId)))

    def _callback(self, cmd, arg):
        if cmd == 'releaseTopLogoAni':
            ent = int(arg.GetNumber())
            en = BigWorld.entity(ent)
            if en and en.topLogo and en.topLogo.guiAni:
                en.topLogo.clearTopLogoAni()


HAVE_FRIEND_CLASS = ['Npc',
 'Dawdler',
 'ClientNpc',
 'GuildDawdler',
 'Monster',
 'MovableCombatCreation',
 'MovableIsolatedCreation',
 'StaticCombatCreation',
 'StaticIsolatedCreation',
 'FragileObject',
 'ICreation',
 'SummonedBeast',
 'AvatarMonster',
 'MovableNpc',
 'SummonedSprite']

class TopLogo(object):
    EMOTE_M_HAPPY = 0
    EMOTE_M_SAD = 1
    EMOTE_M_SURPRISE = 2
    EMOTE_P_HAPPY = 0
    EMOTE_P_SAD = 1
    EMOTE_P_SURPRISE = 2
    TOPLOGUPDATE_FPS = 15
    TOPLOGUPDATE_DIST = 20

    def __init__(self, entity, hasSchool = True):
        super(TopLogo, self).__init__()
        self.entity = entity
        en = BigWorld.entity(self.entity)
        if en.model == None:
            return
        else:
            self.castbarCBHandler = None
            self.castBarTotaltick = None
            self.castBarStarttick = None
            self.titleName = ''
            self.titleStyle = 1
            self.lastTileName = None
            self.lastName = None
            self.lastTitleStyle = None
            self.nameClolor = None
            self.bloodColor = None
            self.xinmoColor = None
            self.nameTxt = None
            self.bloodNum = -1
            self.absorbNum = -1
            self.absorbHealNum = -1
            self.visibleAttachModel = None
            self.titleEffectHeight = 0
            h = en.getTopLogoHeight()
            biasPos = Math.Vector3(0, h + 0.3, 0)
            self.aniBiasPos = Math.Vector3(0, h + 0.5, 0)
            self.aniBiasOffset = 0
            self.aniMovie = None
            self.guiAni = None
            self.gui = TopLogoObj.getInstance().get_from_cache(entity)
            if clientcom.enableTopLogoOptimize():
                self.gui.entity = en
                self.gui.needUpdateTime = NEEDUPDATATIME
            TopLogoManager.getInstance().addTopLogo(self.entity)
            self.movie = TopLogoManager.getInstance().movie
            self.gui.source = en.matrix
            self.gui.biasPos = biasPos
            self.gui.screenOffset = (0, 30)
            if getattr(en, 'hp', None) and getattr(en, 'mhp', None):
                self.onUpdateHp()
            if utils.instanceof(en, 'PlayerAvatar'):
                self.gui.infront = True
            else:
                self.gui.infront = False
            if en.IsAvatar:
                self.gui.minAlpha = en.inClanWar
            GUI.addRoot(self.gui)
            self.setInitOffestH()
            self.lastPkLv = -1
            self.lastPkMode = -1
            self.nameVisible = True
            self.nameCountDownTimer = None
            self.qualityColor = ''
            self.updateTopLogoInfo()
            return

    def updateTopLogoInfo(self):
        en = BigWorld.entity(self.entity)
        isSoul = en.IsAvatar and en._isSoul()
        if hasattr(en, 'roleName'):
            if utils.instanceof(en, 'DroppedItem') and en._checkPickItem(BigWorld.player()):
                self.setDropItemIconVisible(True)
            nameString = self.__getNameString(en)
            if gameglobal.showEntityID and not BigWorld.isPublishedVersion():
                nameString += ':' + str(en.id)
                if hasattr(en, 'campOwner'):
                    self.nameString += ':' + str(en.campOwner)
            self.name = nameString
            self.updateRoleName(self.name)
            self.bindVisible()
            self.showTopIcon(en)
        p = BigWorld.player()
        if not p.isInBfDota() and hasattr(en, 'inCombat'):
            if utils.instanceof(en, 'Monster'):
                self.showMonsterBlood(en.inCombat)
            else:
                self.showBlood(en.inCombat)
        if utils.instanceof(en, 'Monster'):
            self.setMonsterBloodColor()
        elif utils.instanceofTypes(en, ('Avatar', 'PlayerAvatar', 'Puppet')):
            self.setAvatarTitle(self.titleName, self.titleStyle)
            (not isSoul or formula.spaceInWorldWarEx(p.spaceNo) or formula.spaceInWingCity(p.spaceNo) or BigWorld.player().isInCrossClanWarStatus) and self.addGuildIcon(en.guildFlag)
            self.updatePkTopLogo()
            self.updateBorderIconAndOtherIcon()
        if hasattr(en, 'boothStat') and en.boothStat == const.BOOTH_STAT_OPEN:
            self.setBoothVisible(True)
            self.setBoothName(en.boothName)
        if hasattr(en, 'chatRoomName') and en.chatRoomName:
            self.setChatRoomVisible(True)
            self.setChatRoomName(en.chatRoomName)
        if hasattr(en, 'fishingStatus') and en.fishingStatus == const.ST_AUTO_FISHING:
            self.setAutoFishingVisible(True)
        if hasattr(en, 'inScriptFlag') and p.id != en.id and en.isInPlayScenario():
            self.setAutoPlayScenarioVisible(True)
        self.setTeamTopLogo(en, AppSettings.get(keys.SET_TEAM_TOP_LOGO_MARK, 1))
        if (hasattr(en, 'IsMonster') and en.IsMonster or hasattr(en, 'IsSummonedBeast') and en.IsSummonedBeast) and en.charType in BigWorld.player().questMonsterInfo.keys():
            self.setQuestIconVisible(True)
        if hasattr(en, 'guildActivityIcon') and en.guildActivityIcon > 0:
            self.setFindLogo(en.guildActivityIcon)
        if gameglobal.rds.configData.get('enableEffectTitle') and hasattr(en, 'curEffectTitleId') and en.curEffectTitleId:
            self.showTitleEffect(en.curEffectTitleId)
        hideName = p.bHideFightForLoveFighterName(en)
        if hideName:
            if utils.instanceofTypes(en, ('Avatar', 'PlayerAvatar', 'Puppet')):
                nameInfo = p.getFightForLoveNameInfo()
                name = nameInfo.get('name', '')
                title = nameInfo.get('title', '')
                self.name = name
                self.updateRoleName(self.name)
                self.setAvatarTitle(title, 1)
        inSSC = p.isInSSCorTeamSSC()
        if inSSC:
            isSummonedAvatarMonster = SBD.data.get(getattr(en, 'beastId', None), {}).get('isSummonedAvatarMonster', None)
            if isSummonedAvatarMonster:
                self.name = const.SSC_ROLENAME
                self.updateRoleName(self.name)
                self.setAvatarTitle(const.SSC_TITLENAME, 1)
        if hasattr(self.gui, 'updateTotalFrameCount'):
            if clientcom.needDoOptimize() and gameglobal.rds.configData.get('enableToplogoTotalOptimize', 0):
                self.gui.updateTotalFrameCount = random.randint(gameglobal.TOPLOGO_FRAME_MIN, gameglobal.TOPLOGO_FRAME_MAX)
            else:
                self.gui.updateTotalFrameCount = 0
        if getattr(en, 'jctSeq', 0) and p.inClanCourier():
            self.setAvatarTitle('', 1)
        self.initDotaBlood()
        self.refreshCountDown()
        self.setHideBloodNumState(getattr(en, 'isHideBloodNum', False))

    def setInitOffestH(self):
        self.invokeMethod('setInitOffestH', Scaleform.GfxValue(60))

    def initDotaBlood(self):
        entity = BigWorld.entity(self.entity)
        p = BigWorld.player()
        if p.isInBfDota() and getattr(entity, 'IsAvatar', False):
            type = self.getDynamicMcType(entity)
            energyType = ZD.data.get(entity.bianshen[1], {}).get('bfDotaZaijuEnergyType', 1)
            energyColor = DCD.data.get('zaiju_energyType_map', {}).get(energyType, 'lanse')
            bloodDensity = DCD.data.get('bfDotaBloodDensity', 2000)
            bfDotaBloodMaxLimit = DCD.data.get('bfDotaBloodMaxLimit', 50000)
            self.invokeMethod('initDotaBlood', (Scaleform.GfxValue(type),
             Scaleform.GfxValue(energyColor),
             Scaleform.GfxValue(bloodDensity),
             Scaleform.GfxValue(bfDotaBloodMaxLimit)))
            self.setLv(entity.battleFieldDotaLv)
            self.setDotaHpMax(entity.mhp)
            self.setWuDi(entity.isWuDiState())
            self.showBlood(True)
            self.onUpdateMp()
            self.onUpdateHp()
            self.setGuiStateChange(True)

    def removeDotaBlood(self):
        self.invokeMethod('removeDotaBlood')
        self.setGuiStateChange(True)

    def setDotaHpMax(self, hpMaxNumber):
        p = BigWorld.player()
        if p.isInBfDota():
            self.invokeMethod('setDotaHpMax', Scaleform.GfxValue(hpMaxNumber))
            self.setGuiStateChange(True)

    def getDynamicMcType(self, entity):
        p = BigWorld.player()
        if p.isEnemy(entity):
            type = DYNAMIC_MC_TYPE_BLOOD_DOTA_ENEMY
        else:
            type = DYNAMIC_MC_TYPE_BLOOD_DOTA_TEAMMATE
        return type

    def setTeamTopLogo(self, en, isHide):
        if hasattr(BigWorld.player(), 'groupMark'):
            markId = BigWorld.player().groupMark.get(en.id, uiConst.MENU_SPECIAL_MARK)
            markFlag = gameglobal.rds.ui.getGroupIdentityType(en.id, isHide)
            self.setTitleEffectHeight()
            if markId == uiConst.MENU_SPECIAL_MARK:
                self.removeTeamLogo()
                if markFlag:
                    self.setTeamIdentity(markFlag)
                else:
                    self.removeTeamIdentity()
            else:
                self.removeTeamIdentity()
                self.setTeamLogo(markId)

    def showTopIcon(self, en):
        icon = None
        if utils.instanceofTypes(en, ('Npc', 'MovableNpc', 'Dawdler')):
            icon = en.getTopIcon()
            if self.topIconSpecialCheck(en):
                icon = None
        elif utils.instanceof(en, 'InteractiveObject'):
            icon = IAD.data.get(en.objectId, {}).get('topIcon')
        elif utils.instanceof(en, 'Monster'):
            icon = NMMD.data.get(getattr(en, 'charType', None), {}).get('topIcon')
        if icon != None:
            iconPath = '../npcIcon/' + icon + '.dds'
            self.setTaskIndicator(iconPath)
            self.showTaskIndicator(True)
        else:
            self.showTaskIndicator(False)

    def topIconSpecialCheck(self, en):
        if hasattr(en, 'npcId'):
            p = BigWorld.player()
            fengWuZhiLevel = NCD.data.get(en.npcId, {}).get('fengWuZhiLevel', None)
            if fengWuZhiLevel:
                if p.lv < fengWuZhiLevel:
                    return True
            roleCardClueId = NCD.data.get(en.npcId, {}).get('roleCardClueId', None)
            if roleCardClueId:
                if not p.getClueFlag(roleCardClueId):
                    return True
            finishClueId = NCD.data.get(en.npcId, {}).get('finishClueId', None)
            if finishClueId:
                if p.getClueFlag(finishClueId):
                    return True
        return False

    def invokeMethod(self, *args):
        if not self.movie:
            return
        method = args[0]
        argsList = ['_root.invokeMethod', Scaleform.GfxValue(self.entity), Scaleform.GfxValue(method)]
        if len(args) == 1:
            if clientcom.enableTopLogoOptimize() and self.gui and hasattr(self.gui, 'addInvokMethods'):
                self.gui.addInvokMethods(tuple(argsList))
            else:
                self.movie.invoke(tuple(argsList))
            return
        actArgs = args[1]
        if type(actArgs) == tuple:
            argsList.extend(actArgs)
        else:
            argsList.append(actArgs)
        if clientcom.enableTopLogoOptimize() and self.gui and hasattr(self.gui, 'addInvokMethods'):
            self.gui.addInvokMethods(tuple(argsList))
        else:
            self.movie.invoke(tuple(argsList))

    def invokeAniMethod(self, *args):
        if not self.aniMovie:
            return
        method = args[0]
        argsList = ['_root.invokeMethod', Scaleform.GfxValue(self.entity), Scaleform.GfxValue(method)]
        if len(args) == 1:
            self.aniMovie.invoke(tuple(argsList))
            return
        actArgs = args[1]
        if type(actArgs) == tuple:
            argsList.extend(actArgs)
        else:
            argsList.append(actArgs)
        self.aniMovie.invoke(tuple(argsList))

    def _initPkLogo(self, en):
        p = BigWorld.player()
        if p.inFuben():
            self.hidePkTopLogo()
            return
        self.updatePkTopLogo()

    def __getModelHeight(self, en):
        h = None
        if hasattr(en, 'charType'):
            data = NMMD.data.get(en.charType, None)
            if data:
                h = data.get('topLogoHeight', en.model.height)
        elif hasattr(en, 'npcId'):
            data = NCD.data.get(en.npcId, None)
            if data:
                h = data.get('topLogoHeight', en.model.height)
        elif utils.instanceof(en, 'TreasureBox'):
            data = TBD.data.get(en.treasureBoxId, None)
            if data:
                h = data.get('topLogoHeight', en.model.height)
        if h == None:
            h = en.model.height
        return h

    def __getNameString(self, en):
        nameString = ''
        p = BigWorld.player()
        if hasattr(en, 'titleName'):
            self.titleName = en.titleName
        if utils.instanceof(en, 'DroppedItem'):
            if en.itemId in [gametypes.CASH_ITEM, gametypes.BIND_CASH_ITEM]:
                nameString = gameStrings.TEXT_TOPLOGO_601 % (en.roleName, en.itemNum)
            else:
                if en.itemNum == 1:
                    nameString = str(en.roleName)
                else:
                    nameString = gameStrings.TEXT_TOPLOGO_601 % (en.roleName, en.itemNum)
                if en.belongName:
                    self.titleName = en.belongName + gameStrings.TEXT_TOPLOGO_608
        elif hasattr(en, 'npcId') and not utils.instanceof(en, 'HomeFurniture'):
            data = NCD.data.get(en.npcId, None)
            if data:
                title = data.get('title', None)
                if title:
                    self.titleName = title
                    nameString = en.roleName
                else:
                    nameString = en.roleName
            else:
                nameString = en.roleName
        elif utils.instanceof(en, 'QuestBox'):
            data = QBD.data.get(en.questBoxType)
            if data:
                nameString = data.get('name', '')
            else:
                nameString = str(en.roleName)
        elif hasattr(en, 'schoolSwitchName'):
            nameString = en.schoolSwitchName
        elif utils.instanceof(en, 'HomeFurniture'):
            nameString = ''
        else:
            nameString = en.roleName
        if en.IsMonster and hasattr(en, 'belongName'):
            if not gameglobal.gHideMonsterName:
                if en.belongName and en.camp != const.CAMP_WORLD_AVATAR:
                    self.titleName = en.belongName + gameStrings.TEXT_TOPLOGO_637
                elif hasattr(en, 'titleName'):
                    self.titleName = en.titleName
                if not self.titleName:
                    self.titleName = en.getItemData().get('title', '')
            nameString = en.roleName
        elif en.IsBox and hasattr(en, 'belongName'):
            if en.belongName:
                self.titleName = gameStrings.TEXT_TOPLOGO_645 % en.belongName
            elif hasattr(en, 'titleName'):
                self.titleName = en.titleName
            if not self.titleName:
                self.titleName = en.getItemData().get('title', '')
            nameString = en.roleName
        elif en.IsSummoned and BigWorld.player().isInSSCorTeamSSC():
            self.titleName = ''
        elif utils.instanceofTypes(en, ('Avatar', 'PlayerAvatar', 'Puppet')):
            if p.bHideFightForLoveFighterName(en):
                nameInfo = p.getFightForLoveNameInfo()
                self.titleName = nameInfo.get('title', '')
            else:
                self.titleName, self.titleStyle = en.getActivateTitleStyle()
        if utils.instanceofTypes(en, ('SummonedSprite', 'Avatar', 'SummonedBeast', 'SummonedAvatarMonster', 'Puppet')):
            if hasattr(p, 'isBianShenZaiJuInPUBG') and p.isBianShenZaiJuInPUBG(en):
                self.titleName = ''
                nameString = ''
            nameString = p.anonymNameMgr.checkNeedAnonymousName(en, nameString)
            self.titleName = p.anonymNameMgr.checkNeedAnonymousTitle(en, self.titleName)
        if utils.instanceofTypes(en, 'SummonedSprite') and BigWorld.entities.get(en.ownerId) and getattr(BigWorld.entities[en.ownerId], 'jctSeq', 0):
            nameString = SSD.data.get(en.spriteId, {}).get('name', '')
            self.titleName = ''
        return nameString

    def initTopLogoAni(self, heightOffset = 0):
        en = BigWorld.entity(self.entity)
        h = en.getTopLogoHeight()
        if heightOffset != self.aniBiasOffset:
            biasPos = Math.Vector3(0, h + 0.5 + heightOffset, 0)
            self.aniBiasOffset = heightOffset
        else:
            biasPos = self.aniBiasPos
        TopLogoAniManager.getInstance().addTopLogoAni(self.entity)
        self.aniMovie = TopLogoAniManager.getInstance().movie
        source = en.matrix
        if hasattr(en, 'getTopLogoSource'):
            source = en.getTopLogoSource()
        if self.guiAni:
            self.guiAni.source = source
            self.guiAni.biasPos = biasPos
            self.guiAni.screenOffset = (20, 150)
            GUI.addRoot(self.guiAni)
        else:
            self.guiAni = TopLogoAniObj.getInstance().get_from_cache(self.entity)
            self.guiAni.source = source
            self.guiAni.biasPos = biasPos
            self.guiAni.screenOffset = (20, 150)
            if utils.instanceof(en, 'PlayerAvatar'):
                self.guiAni.infront = True
            else:
                self.guiAni.infront = False
            GUI.addRoot(self.guiAni)

    def clearTopLogoAni(self):
        if self.aniMovie:
            self.aniMovie = None
            TopLogoAniManager.getInstance().removeTopLogoAni(self.entity)
        if self.guiAni:
            GUI.delRoot(self.guiAni)

    def releaseTopLogoAni(self):
        if self.aniMovie:
            self.aniMovie = None
            TopLogoAniManager.getInstance().removeTopLogoAni(self.entity)
            if self.guiAni:
                GUI.delRoot(self.guiAni)
        TopLogoAniObj.getInstance().add_to_cache(self)

    def setHeight(self, height, x = 0, z = 0):
        self.gui.biasPos = Math.Vector3(x, height + 0.3, z)
        self.gui.screenOffset = (0, 30)
        self.aniBiasPos = Math.Vector3(x, height + 0.5 + self.aniBiasOffset, z)

    def showEntityId(self, show):
        gameglobal.showEntityID = show
        ent = BigWorld.entities.values()
        if gameglobal.gmShowEntityID or gameglobal.showEntityID and not BigWorld.isPublishedVersion():
            for e in ent:
                if not hasattr(e, 'topLogo'):
                    continue
                if e.topLogo and (e.topLogo.name.find(':') == -1 or e.topLogo.name.split(':')[1] != str(e.id)):
                    e.topLogo.name += ':' + str(e.id)
                    e.topLogo.updateRoleName(e.topLogo.name)

        else:
            for e in ent:
                if not hasattr(e, 'topLogo'):
                    continue
                if e.topLogo and e.topLogo.name.find(':') != -1:
                    nameArr = e.topLogo.name.split(':')
                    nameArr.pop()
                    e.topLogo.name = ':'.join(nameArr)
                    e.topLogo.updateRoleName(e.topLogo.name)

    def release(self):
        self.removeDotaBlood()
        self.setHideBloodNumState(False)
        self.movie = None
        TopLogoManager.getInstance().removeTopLogo(self.entity)
        self._detachVisible()
        GUI.delRoot(self.gui)
        if clientcom.enableTopLogoOptimize():
            self.gui.clearInvokMethods()
            self.gui.entity = None
            self.gui.needUpdateTime = NEEDUPDATATIME_MAX
        TopLogoObj.getInstance().add_to_cache(self)
        self.releaseTopLogoAni()
        self.moviedef = None
        self.entity = 0

    def showMonsterBlood(self, show):
        en = BigWorld.entity(self.entity)
        if en:
            if utils.instanceof(en, 'Monster') and gameglobal.gHideMonsterBlood:
                pass
            else:
                self.setGuiStateChange(True)
                self.invokeMethod('showBlood', Scaleform.GfxValue(show))
        bSelected = hasattr(BigWorld.player(), 'targetLocked') and BigWorld.player().targetLocked == en
        if utils.instanceof(en, 'Monster') and en.monsterStrengthType == gametypes.MONSTER_NORMAL and not gameglobal.gHideMonsterName and not bSelected:
            self.hideName(gameglobal.gHideMonsterName)

    def showBlood(self, show):
        self.invokeMethod('showBlood', Scaleform.GfxValue(show))
        self.setGuiStateChange(True)

    def setBloodColor(self, color):
        en = BigWorld.entities.get(self.entity)
        if not en:
            return
        else:
            if en.IsSummonedSprite:
                owner = en.getOwner()
                if owner and owner.topLogo:
                    color = owner.topLogo.bloodColor
            if self.movie and self.bloodColor != color:
                self.bloodColor = color
                self.invokeMethod('setBloodColor', Scaleform.GfxValue(color))
                self.setGuiStateChange(True)
            if utils.instanceof(en, 'Avatar') or en == BigWorld.player():
                sprite = en.getSpriteInWorld()
                if sprite and getattr(sprite, 'topLogo', None):
                    sprite.topLogo.setBloodColor(color)
            return

    def showSpellBar(self, show):
        if self.movie:
            self.invokeMethod('showSpellBar', Scaleform.GfxValue(show))
            self.setGuiStateChange(True)

    def setSpellBarName(self, skillNameTip):
        if self.movie:
            self.invokeMethod('setSpellBarName', Scaleform.GfxValue(skillNameTip))
            self.setGuiStateChange(True)

    def setSpellTime(self, remain, scale):
        if self.movie:
            self.invokeMethod('setSpellTime', (Scaleform.GfxValue(remain), Scaleform.GfxValue(scale)))
            self.setGuiStateChange(True)

    def setTitleName(self, text):
        en = BigWorld.entity(self.entity)
        if utils.instanceofTypes(en, ('Avatar', 'PlayerAvatar', 'Puppet')):
            return
        else:
            if utils.instanceof(en, 'SummonedAvatarMonster'):
                inSSC = BigWorld.player().isInSSCorTeamSSC()
                isSummonedAvatarMonster = SBD.data.get(getattr(en, 'beastId', None), {}).get('isSummonedAvatarMonster', None)
                if isSummonedAvatarMonster:
                    text = '' if not inSSC else const.SSC_TITLENAME
            if getattr(en, 'jctSeq', 0) and BigWorld.player().inClanCourier():
                text = ''
            self.invokeMethod('setPreText', Scaleform.GfxValue(gbk2unicode(text)))
            self.setGuiStateChange(True)
            return

    def setAvatarTitle(self, name, style):
        if self.lastTileName != name or self.lastTitleStyle != style:
            en = BigWorld.entity(self.entity)
            if getattr(en, 'jctSeq', 0) and BigWorld.player().inClanCourier():
                name = ''
            self.lastTileName = name
            self.lastTitleStyle = style
            self.titleName = name
            self.titleStyle = style
            self.invokeMethod('setAvatarTitle', (Scaleform.GfxValue(gbk2unicode(name)), Scaleform.GfxValue(int(style))))
            self.setGuiStateChange(True)

    def hideTitleName(self, isHide):
        en = BigWorld.entity(self.entity)
        if not isHide and hasattr(en, 'hideTopLogoOutCombat') and en.hideTopLogoOutCombat() and not en.inCombat:
            return
        if not isHide and MCD.data.get(BigWorld.player().mapID, {}).get('isHideAvatarTitle', 0):
            isHide = True
        if isHide:
            self.setTitleName('')
        else:
            self.setTitleName(self.titleName)

    def onUpdateHp(self):
        en = BigWorld.entity(self.entity)
        absorbType = DMG_ABSORB_TYPE_NORMAL
        absorbNum = 0
        absorbHealNum = 0
        if getattr(en, 'isDmgMode', False):
            bloodNum = 1.0
        elif hasattr(en, 'dmgAbsorbClient') and en.dmgAbsorbClient or hasattr(en, 'hpHole') and en.hpHole:
            extraVal = 0
            if en.dmgAbsorbClient:
                extraVal += en.dmgAbsorbClient[0]
            if en.hpHole:
                extraVal += en.hpHole
            if en.mhp >= en.hp + extraVal:
                total = en.mhp
            else:
                total = en.hp + extraVal
            bloodNum = float(en.hp) / total
            if en.dmgAbsorbClient:
                absorbNum = float(en.dmgAbsorbClient[0]) / total
                absorbType = en.dmgAbsorbClient[-1]
                absorbType = DMG_ABSORB_TYPE_MAGIC if absorbType in (gametypes.SKILL_STATE_SE_ABSORB_MAG_DMG, gametypes.SKILL_STATE_SE_ABSORB_MAGDMG_BUFFSRC) else DMG_ABSORB_TYPE_NORMAL
            if en.hpHole:
                absorbHealNum = float(en.hpHole) / total
        else:
            bloodNum = float(en.hp) / en.mhp
        if self.needUpdate() and (self.bloodNum != bloodNum or self.absorbNum != absorbNum or self.absorbHealNum != absorbHealNum):
            self.setGuiStateChange(True)
            self.invokeMethod('updateBlood', (Scaleform.GfxValue(bloodNum),
             Scaleform.GfxValue(absorbNum),
             Scaleform.GfxValue(absorbType),
             Scaleform.GfxValue(absorbHealNum)))
            self.bloodNum = bloodNum
            self.absorbNum = absorbNum
            self.absorbHealNum = absorbHealNum

    def onUpdateMp(self):
        en = BigWorld.entity(self.entity)
        p = BigWorld.player()
        if p.isInBfDota() and getattr(en, 'IsAvatar', False):
            mpPercent = en.mp * 1.0 / en.mmp if en.mmp else 0
            self.invokeMethod('updateMp', Scaleform.GfxValue(mpPercent))
            self.setGuiStateChange(True)

    def setLv(self, lv):
        p = BigWorld.player()
        en = BigWorld.entity(self.entity)
        if p.isInBfDota() and getattr(en, 'IsAvatar', False):
            self.invokeMethod('setLv', Scaleform.GfxValue(lv))
            self.setGuiStateChange(True)

    def setWuDi(self, isWuDi):
        p = BigWorld.player()
        en = BigWorld.entity(self.entity)
        if p.isInBfDota() and getattr(en, 'IsAvatar', False):
            self.invokeMethod('setWuDi', Scaleform.GfxValue(isWuDi))
            self.setGuiStateChange(True)

    def updateDmgAbsorb(self, num):
        self.invokeMethod('updateDmgAbsorb', Scaleform.GfxValue(num))

    def showDmgAbsorb(self, vis):
        self.invokeMethod('showDmgAbsorb', Scaleform.GfxValue(vis))

    def bindVisible(self):
        pass

    def _detachVisible(self):
        pass

    def hide(self, isHide):
        if not self.gui:
            return
        if isHide and self.gui.visible:
            self.gui.visible = False
        elif not isHide and not self.gui.visible:
            self.gui.visible = True
        self.hideTitleEffect(isHide)

    def showMonsterIcon(self, isShow):
        self.invokeMethod('showMonsterIcon', Scaleform.GfxValue(isShow))
        self.setGuiStateChange(True)

    def hideName(self, isHide):
        en = BigWorld.entity(self.entity)
        if not isHide and hasattr(en, 'hideTopLogoOutCombat') and en.hideTopLogoOutCombat() and not en.inCombat:
            return
        if not isHide and hasattr(en, 'needHideName') and en.needHideName():
            isHide = True
        if not isHide and en.IsAvatar and MCD.data.get(BigWorld.player().mapID, {}).get('isHideAvatarName', 0):
            isHide = True
        self.nameVisible = not isHide
        self.invokeMethod('hideName', Scaleform.GfxValue(isHide))
        self.setGuiStateChange(True)

    def hideChatMsg(self, isHide):
        self.invokeAniMethod('hideChatMsg', Scaleform.GfxValue(isHide))

    def _getPkTopLogoColor(self, pkStatus, lastPkTime):
        pkStatus = formula.whatRealPkStatus(pkStatus, lastPkTime)
        return const.PK_STATUS_COLOR_DICT.get(pkStatus, 'normal')

    def _getOtherAvatarTopLogoColor(self, avatar):
        p = BigWorld.player()
        if p.isInSSCorTeamSSC():
            if BigWorld.player().isEnemy(avatar):
                return 'red'
            else:
                return 'blue'
        if p.isInClanWar() and avatar.isInClanWar():
            if BigWorld.player().isEnemy(avatar):
                return 'red'
            else:
                return 'blue'
        if avatar.guildNUID in p.declareWarGuild:
            return 'red'
        if p.isQieCuoWith(avatar.id):
            return const.PK_STATUS_COLOR_DICT.get(const.PK_STATUS_RED, 'normal')
        if p.isInMyTeam(avatar) and groupUtils.isInSameTeam(p.gbId, avatar.gbId):
            return 'darkBlue'
        if p.isInMyTeam(avatar) and not groupUtils.isInSameTeam(p.gbId, avatar.gbId):
            return 'blue'
        mapId = formula.getMapId(p.spaceNo)
        mapData = MCD.data.get(mapId)
        if hasattr(p, 'tCamp') and hasattr(avatar, 'tCamp') and p.tCamp != 0 and avatar.tCamp != 0 or mapData and mapData.get('usePvpTempCamp'):
            if BigWorld.player().isEnemy(avatar):
                return 'red'
            else:
                return 'blue'
        else:
            if BigWorld.player().isEnemy(avatar):
                return 'red'
            return self._getPkTopLogoColor(avatar.pkStatus, avatar.lastPkTime)

    def _getPlayerAvatarTopLogoColor(self):
        p = BigWorld.player()
        if p.isInQieCuo():
            return const.PK_STATUS_COLOR_DICT.get(const.PK_STATUS_RED, 'normal')
        if p.isInTeamOrGroup():
            return 'darkBlue'
        if p.isInClanWar():
            return const.PK_STATUS_COLOR_DICT.get(const.PK_STATUS_WHITE, 'normal')
        if hasattr(p, 'tCamp') and p.tCamp != 0:
            return 'normal'
        return self._getPkTopLogoColor(p.pkStatus, p.lastPkTime)

    def _getClanWarTopLogoColor(self, entity):
        p = BigWorld.player()
        if entity.beAtkType == gametypes.BE_ATK_TYPE_NOBODY:
            return 'blue'
        elif p.isEnemy(entity):
            return 'red'
        else:
            return 'blue'

    def updateRoleName(self, newName, preName = ''):
        if not self.movie:
            return
        p = BigWorld.player()
        en = BigWorld.entity(self.entity)
        if not en or not en.inWorld:
            return
        nameVal = self.genFullName(newName)
        if self.lastName != nameVal:
            self.lastName = nameVal
            self.invokeMethod('setName', Scaleform.GfxValue(gbk2unicode(nameVal)))
            self.setGuiStateChange(True)
        if gameglobal.rds.ui.battleOfFortProgressBar.checkBattleFortNewFlag() and en.IsAvatar:
            if utils.instanceof(en, 'PlayerAvatar') or not p.isEnemy(en):
                self.setColor('blue')
                self.setBloodColor('blue')
            else:
                self.setColor('red')
                self.setBloodColor('red')
        elif utils.instanceof(en, 'PlayerAvatar'):
            color = self._getPlayerAvatarTopLogoColor()
            if en.life == gametypes.LIFE_DEAD:
                self.setColor('gray')
            else:
                self.setColor(color)
            self.setBloodColor('player')
        elif utils.instanceofTypes(en, gametypes.CLAN_WAR_CLASS):
            color = self._getClanWarTopLogoColor(en)
            self.setColor(color)
            self.setBloodColor(color)
        elif not BigWorld.player().isEnemy(en) and utils.instanceofTypes(en, HAVE_FRIEND_CLASS):
            self.setColor('npcyellow')
            self.setBloodColor('blue')
        elif en.IsMonster:
            self.setMonsterNameColor(en.atkType)
            self.setBloodColor('red')
        elif utils.instanceofTypes(en, ('Avatar', 'Puppet')):
            self.updateAvatarBloodColor(en)
            self._initPkLogo(en)
        elif utils.instanceofTypes(en, ('DroppedItem', 'QuestBox')):
            self.setColor('item')
        elif utils.instanceofTypes(en, ('EmptyZaiju',)):
            if BigWorld.player().isEnemy(en):
                self.setColor('red')
                self.setBloodColor('red')
            else:
                self.setColor('normal')
                self.setBloodColor('blue')
        elif utils.instanceofTypes(en, ('MultiplayMovingPlatform',)):
            self.setBloodColor('green')
        elif getattr(en, 'IsWingWorldCarrier', False):
            if BigWorld.player().isEnemy(en):
                self.setColor('red')
                self.setBloodColor('red')
            else:
                self.setColor('darkBlue')
        else:
            self.setColor('normal')
        if hasattr(p, 'checkAssassination') and p.checkAssassination(p) and utils.instanceofTypes(en, ('Avatar',)):
            if p.getAssTargetEntId() == en.id:
                self.setColor('red')
        self.setTitleName(self.titleName)
        if utils.instanceofTypes(en, ('Avatar', 'PlayerAvatar', 'Puppet')):
            self.setAvatarTitle(self.titleName, self.titleStyle)

    def genFullName(self, newName):
        p = BigWorld.player()
        en = BigWorld.entity(self.entity)
        if en.IsAvatar and en._isInBianyao():
            nameVal = gameStrings.TEXT_TOPLOGO_1111 + newName
        elif en.IsAvatar or utils.instanceof(en, 'Puppet'):
            if gameglobal.rds.ui.battleCQZZProgressBar.checkBattleCQZZ():
                nameVal = gameglobal.rds.ui.battleCQZZProgressBar.getAvatarCampName(en)
            elif en._isSoul() and en.crossFromHostId:
                if formula.spaceInWorldWar(p.spaceNo):
                    nameVal = en.realRoleName
                else:
                    nameVal = en.roleName
            elif gameglobal.rds.ui.battleOfFortProgressBar.checkBattleFortNewFlag():
                nameVal = gameglobal.rds.ui.battleOfFortProgressBar.getAvatarCampName(en)
            else:
                nameVal = newName
        else:
            nameVal = newName
        if getattr(en, 'jctSeq', 0) and BigWorld.player().inClanCourier():
            nameVal = en.getJCTRoleName()
        nameVal = p.anonymNameMgr.checkNeedAnonymousName(en, nameVal)
        return nameVal

    def updateAvatarBloodColor(self, en):
        p = BigWorld.player()
        color = self._getOtherAvatarTopLogoColor(en)
        if en.life == gametypes.LIFE_DEAD:
            self.setColor('gray')
        else:
            self.setColor(color)
        if p.isInSSCorTeamSSC():
            if p.inFubenType(const.FB_TYPE_SHENGSICHANG):
                self.setBloodColor('red')
            elif BigWorld.player().isEnemy(en):
                self.setBloodColor('red')
            else:
                self.setBloodColor('blue')
        elif self.isSameTeamOrGroup(en):
            self.setBloodColor('green')
        elif not BigWorld.player().isEnemy(en):
            self.setBloodColor('blue')
        else:
            self.setBloodColor('red')
        if formula.getFubenNo(formula.getAnnalSrcSceneNo(p.spaceNo)) in const.FB_NO_CROSS_2V2_ROUND_DOUBLE_ARENA_PLAYOFF and en != p:
            if en.tempCamp == 1:
                self.setBloodColor('red')
            elif en.tempCamp == 2:
                self.setBloodColor('blue')
            elif en.tempCamp == 0:
                self.setBloodColor('green')
        if formula.spaceInWingWorldXinMoArena(formula.getAnnalSrcSceneNo(p.spaceNo)) and en != p:
            if en.tempCamp == 1 or en.tempCamp == 2:
                xinmoColor = getattr(self, 'xinmoColor', None)
                if xinmoColor:
                    self.setBloodColor(xinmoColor)

    def isSameTeamOrGroup(self, en):
        p = BigWorld.player()
        ret = p.isInTeam() and p.isInMyTeam(en) or p.isInGroup() and p.isInMyTeam(en)
        return ret

    def setIconBorder(self, borderType):
        self.invokeMethod('setIconBorder', (Scaleform.GfxValue(str(borderType)),))
        self.setGuiStateChange(True)

    def addOtherIcon(self, path):
        self.invokeMethod('addOtherIcon', (Scaleform.GfxValue(str(path)), Scaleform.GfxValue(self.entity)))
        self.setGuiStateChange(True)
        BigWorld.callback(5.0, Functor(self.setGuiStateChange, True))
        BigWorld.callback(15.0, Functor(self.setGuiStateChange, True))

    def removeOtherIcon(self):
        self.invokeMethod('removeOtherIcon')
        self.setGuiStateChange(True)

    def hideOtherIcon(self, vis):
        self.invokeMethod('hideOtherIcon', Scaleform.GfxValue(vis))
        self.setGuiStateChange(True)

    def addGuildIcon(self, flag):
        p = BigWorld.player()
        if p.inWorldWarEx():
            self.refreshGuildIconInWorldWarEx()
            return None
        elif flag == '':
            return None
        else:
            en = BigWorld.entity(self.entity)
            opValue = en.getOpacityValue()[0]
            if en.IsAvatar and (opValue == gameglobal.OPACITY_HIDE_INCLUDE_ATTACK or opValue == gameglobal.OPACITY_HIDE):
                return None
            icon, color = uiUtils.getGuildFlag(flag)
            if uiUtils.isDownloadImage(icon):
                if p._isSoul() and hasattr(en, 'getOriginHostId') and gameconfigCommon.enableCrossServerGuildIcon():
                    p.downloadCrossNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, icon, en.getOriginHostId(), gametypes.NOS_FILE_PICTURE, self.onDownloadGuildIcon, (None,))
                else:
                    p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, icon, gametypes.NOS_FILE_PICTURE, self.onDownloadGuildIcon, (None,))
            else:
                path = '../zhanqi/' + str(icon) + '.dds'
                self.setGuildImage(path, color)
            return None

    def onDownloadGuildIcon(self, status, callbackArgs):
        en = BigWorld.entity(self.entity)
        if not en:
            return
        if not en.inWorld:
            return
        if status != gametypes.NOS_FILE_STATUS_APPROVED:
            return
        en = BigWorld.entity(self.entity)
        if en.guildFlag:
            icon, color = uiUtils.getGuildFlag(en.guildFlag)
            path = '../../' + const.IMAGES_DOWNLOAD_DIR + '/' + icon + '.dds'
            self.setGuildImage(path, color)

    def setGuildImage(self, imagePath, color, force = False):
        p = BigWorld.player()
        en = BigWorld.entity(self.entity)
        if p.isInSSCorTeamSSC():
            return
        if p.inFightForLoveFb():
            return
        if hasattr(p, 'isBianShenZaiJuInPUBG') and p.isBianShenZaiJuInPUBG(en):
            return
        if getattr(en, 'jctSeq', 0) and BigWorld.player().inClanCourier():
            imagePath = '../clanWarYaBiao/%s.dds' % CCCD.data.get('clanWarYaBiaoHuntGuild', 'hunterGuild')
            color = ''
        anonymousType = p.anonymNameMgr.checkNeedAnonymity(entity=en)
        if anonymousType != gametypes.AnonymousType_None:
            if p.anonymNameMgr.getAnonymousData(anonymousType, gametypes.ANONYMOUS_GUILD_IMAGE_HIDE, False):
                return
        if utils.instanceof(en, 'PlayerAvatar'):
            if en.guildNUID or p.inWorldWarEx():
                self.invokeMethod('addGuildIcon', (Scaleform.GfxValue(str(imagePath)), Scaleform.GfxValue(self.entity), Scaleform.GfxValue(color)))
                self.setGuiStateChange(True)
        elif utils.instanceof(en, 'Avatar') or utils.instanceof(en, 'AvatarRobot'):
            if en.guildNUID or p.inWorldWarEx():
                self.invokeMethod('addGuildIcon', (Scaleform.GfxValue(str(imagePath)), Scaleform.GfxValue(self.entity), Scaleform.GfxValue(color)))
                self.setGuiStateChange(True)
        BigWorld.callback(15.0, Functor(self.setGuiStateChange, True))

    def setGuiStateChange(self, isChange):
        en = BigWorld.entity(self.entity)
        if not hasattr(en, 'topLogoIsChange'):
            return
        en.topLogoIsChange = isChange

    def setGuiStateAdvance(self, isAdvance):
        en = BigWorld.entity(self.entity)
        if not hasattr(en, 'topLogoIsAdvance'):
            return
        en.topLogoIsAdvance = isAdvance

    def setCustomGuildIcon(self, flag):
        if flag == '':
            return
        en = BigWorld.entity(self.entity)
        icon, color = uiUtils.getGuildFlag(flag)
        path = '../' + const.IMAGES_DOWNLOAD_DIR + str(icon)
        if utils.instanceof(en, 'PlayerAvatar'):
            if en.guildNUID and not gameglobal.gHidePlayerGuild:
                self.setGuiStateAdvance(True)
                self.invokeMethod('addGuildIcon', (Scaleform.GfxValue(str(path)), Scaleform.GfxValue(self.entity), Scaleform.GfxValue(color)))
        elif utils.instanceof(en, 'Avatar'):
            if en.guildNUID and not gameglobal.gHideAvatarGuild:
                self.setGuiStateAdvance(True)
                self.invokeMethod('addGuildIcon', (Scaleform.GfxValue(str(path)), Scaleform.GfxValue(self.entity), Scaleform.GfxValue(color)))

    def setQuestIconVisible(self, vis):
        self.invokeMethod('setQuestIconVisible', Scaleform.GfxValue(vis))
        self.setGuiStateChange(True)

    def removeGuildIcon(self):
        self.invokeMethod('removeGuildIcon')
        self.setGuiStateChange(True)

    def hideGuildIcon(self, vis):
        self.invokeMethod('hideGuildIcon', Scaleform.GfxValue(vis))
        self.setGuiStateChange(True)

    def setMonsterNameColor(self, atkType):
        if atkType == const.MONSTER_ATK_TYPE_PASSIVE_DMG_ATK or atkType == const.MONSTER_ATK_TYPE_PASSIVE_SPELL_ATK:
            self.setColor('jingjie')
        elif atkType == const.MONSTER_ATK_TYPE_PASSIVE_GUARD_ATK or atkType == const.MONSTER_ATK_TYPE_TIMER_GUARD_ATK:
            self.setColor('jingjie')
        elif atkType == const.MONSTER_ATK_TYPE_ACTIVE_RANGE_ATK:
            self.setColor('zhudong')
        else:
            self.setColor('normal')

    def updateAvatarPkColor(self):
        en = BigWorld.entity(self.entity)
        if not self.movie:
            return
        if utils.instanceof(en, 'PlayerAvatar'):
            color = self._getPlayerAvatarTopLogoColor()
            self.setColor(color)
        elif utils.instanceof(en, 'Avatar') or utils.instanceof(en, 'Puppet'):
            color = self._getOtherAvatarTopLogoColor(en)
            self.setColor(color)

    def setMonsterColorInDota(self, tgt):
        p = BigWorld.player()
        if p.isEnemy(tgt):
            self.setBloodColor('red')
        else:
            self.setBloodColor('blue')
        self.onUpdateHp()

    def setMonsterColor(self, mine):
        if mine:
            self.setBloodColor('red')
            self.onUpdateHp()
        else:
            self.setBloodColor('purple')
            self.onUpdateHp()

    def setMonsterBloodColor(self):
        en = BigWorld.entity(self.entity)
        if utils.instanceof(en, 'Monster'):
            if getattr(en, 'firstAttacker', None) and en.firstAttacker[1]:
                player = BigWorld.player()
                if formula.inDotaBattleField(getattr(player, 'mapID', 0)):
                    self.setMonsterColorInDota(en)
                else:
                    isMine = player.gbId == en.firstAttacker[1] or en.monsterOwnerGroupNUID != 0 and player.groupNUID == en.monsterOwnerGroupNUID or player.inFightForLoveFb()
                    self.setMonsterColor(isMine)

    def setColor(self, color):
        en = BigWorld.entities.get(self.entity)
        if not en:
            return
        else:
            if en.IsSummonedSprite:
                owner = en.getOwner()
                if owner and owner.topLogo:
                    color = owner.topLogo.nameClolor
            if self.movie and self.nameClolor != color:
                self.nameClolor = color
                colorVal = Scaleform.GfxValue(gbk2unicode(color))
                self.invokeMethod('setColor', colorVal)
                self.setGuiStateChange(True)
            if utils.instanceof(en, 'Avatar') or en == BigWorld.player() or utils.instanceof(en, 'Puppet'):
                sprite = en.getSpriteInWorld()
                if sprite and getattr(sprite, 'topLogo', None):
                    sprite.topLogo.setColor(color)
            return

    def setLogoColor(self, color):
        if self.movie:
            en = BigWorld.entity(self.entity)
            if utils.instanceofTypes(en, ('DroppedItem', 'QuestBox')):
                self.setColor('item')
            self.qualityColor = color
            newName = "<font color=\'" + color + "\'>" + self.name + '</font>'
            nameVal = Scaleform.GfxValue(gbk2unicode(newName))
            self.invokeMethod('setName', nameVal)
            self.setGuiStateChange(True)

    def setChatMsg(self, msg, time = 5, isFromSprite = False):
        if utils.isRedPacket(msg) or richTextUtils.isVoice(msg) or richTextUtils.isSoundRecord(msg):
            return
        elif not self.needUpdate():
            return
        elif self.gui == None:
            return
        else:
            self.initTopLogoAni()
            en = BigWorld.entity(self.entity)
            if hasattr(en, 'getOpacityValue') and en.getOpacityValue()[0] in (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, gameglobal.OPACITY_HIDE):
                return
            elif hasattr(en, 'carrier') and en.carrier.isReadyState():
                return
            p = BigWorld.player()
            roleName = en.roleName
            if p.bHideFightForLoveFighterName(en):
                nameInfo = p.getFightForLoveNameInfo()
                fightForLoveName = nameInfo.get('name', '')
                roleName = fightForLoveName
            elif getattr(en, 'jctSeq', 0) and p.inClanCourier():
                roleName = en.getJCTRoleName()
            roleName = p.anonymNameMgr.checkNeedAnonymousName(en, roleName)
            name = uiUtils.replaceWhiteSpace(roleName)
            if msg[-5:] == ':role':
                msg = uiUtils.replaceWhiteSpace(msg[:-5])
            if self.aniMovie:
                self.invokeAniMethod('setChatMsg', (Scaleform.GfxValue(gbk2unicode(name)),
                 Scaleform.GfxValue(gbk2unicode(msg)),
                 Scaleform.GfxValue(time),
                 Scaleform.GfxValue(isFromSprite)))
            return

    def showTitleEffect(self, titleEffectId):
        en = BigWorld.entity(self.entity)
        p = BigWorld.player()
        if utils.instanceof(en, 'PlayerAvatar') and gameglobal.gHidePlayerTitle:
            return
        elif not utils.instanceof(en, 'PlayerAvatar') and gameglobal.gHideAvatarTitle:
            return
        elif p.inFubenType(const.FB_TYPE_SHENGSICHANG):
            return
        elif p.bHideFightForLoveFighterName(en) or p.isFightForLoveRunning() or p.isPlayingFightForLoveScenario():
            return
        elif hasattr(p, 'isBianShenZaiJuInPUBG') and p.isBianShenZaiJuInPUBG(en):
            return
        else:
            anonymousType = p.anonymNameMgr.checkNeedAnonymity(entity=en)
            if anonymousType != gametypes.AnonymousType_None:
                if p.anonymNameMgr.getAnonymousData(anonymousType, gametypes.ANONYMOUS_TOP_TITLE_EFFECT_HIDE, False):
                    return
            if not self.needUpdate():
                return
            elif getattr(en, 'jctSeq', 0) and p.inClanCourier():
                return
            mapData = MCD.data.get(BigWorld.player().mapID, {})
            if mapData.get('isEffectTitleHide', 0):
                self.hideTitleEffect(True)
                return
            elif self.gui == None:
                return
            self.initTopLogoAni()
            if hasattr(en, 'getOpacityValue') and en.getOpacityValue()[0] in (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, gameglobal.OPACITY_HIDE):
                return
            path = EFFECT_TITLE_PREFIX + ETD.data.get(titleEffectId, {}).get('preShowSwfName', '') + '.swf'
            if self.aniMovie:
                self.invokeAniMethod('showTitleEffect', Scaleform.GfxValue(path))
                if hasattr(en, 'id') and hasattr(en, 'isInTeamOrGroup') and en.isInTeamOrGroup():
                    effectH = ETD.data.get(titleEffectId, {}).get('titleEffectH', 0)
                    self.titleEffectHeight = effectH
                    gameglobal.rds.ui.refreshTeamLogoOrIdentity(en.id)
            return

    def removeTitleEffect(self):
        en = BigWorld.entity(self.entity)
        if self.aniMovie:
            self.invokeAniMethod('removeTitleEffect')
            if hasattr(en, 'id') and hasattr(en, 'isInTeamOrGroup') and en.isInTeamOrGroup() and self.titleEffectHeight:
                self.titleEffectHeight = 0
                gameglobal.rds.ui.refreshTeamLogoOrIdentity(en.id)

    def hideTitleEffect(self, bHide):
        en = BigWorld.entity(self.entity)
        if not bHide and gameglobal.rds.configData.get('enableEffectTitle') and hasattr(en, 'curEffectTitleId') and en.curEffectTitleId:
            self.showTitleEffect(en.curEffectTitleId)
        else:
            self.removeTitleEffect()

    def showBigEmote(self, msg, heightOffset = 0):
        if self.gui == None or msg not in emoteMap:
            return
        else:
            self.showEmoteByPath(emoteMap[msg] + gameglobal.rds.ui.getUIExt(), heightOffset)
            return

    def showEmoteByPath(self, path, heightOffset = 0):
        en = BigWorld.entity(self.entity)
        if not en or not en.inWorld:
            return
        if hasattr(en, 'getOpacityValue') and en.getOpacityValue()[0] in (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, gameglobal.OPACITY_HIDE):
            return
        self.initTopLogoAni(heightOffset)
        if self.aniMovie:
            self.invokeAniMethod('showBigEmote', Scaleform.GfxValue(path))

    def stopBigEmote(self):
        if self.aniMovie:
            self.invokeAniMethod('overEmote')

    def showPKLogo(self, isKillMode, lv):
        if lv == self.lastPkLv and isKillMode == self.lastPkMode:
            return
        self.lastPkLv = lv
        self.lastPkMode = isKillMode
        self.invokeMethod('showLogoPK', (Scaleform.GfxValue(isKillMode), Scaleform.GfxValue(lv)))
        self.setGuiStateChange(True)

    def stopPKLogo(self):
        self.lastPkLv = -1
        self.lastPkMode = -1
        self.invokeMethod('removeLogoPK')
        self.setGuiStateChange(True)

    def setTaskIndicator(self, state):
        self.setGuiStateAdvance(True)
        self.invokeMethod('setTaskIndicator', (Scaleform.GfxValue(state), Scaleform.GfxValue(self.entity)))
        BigWorld.callback(5.0, Functor(self.setGuiStateChange, True))
        BigWorld.callback(15.0, Functor(self.setGuiStateChange, True))

    def showTaskIndicator(self, show):
        self.invokeMethod('showTaskIndicator', Scaleform.GfxValue(show))
        self.setGuiStateChange(True)

    def setDropItemIconVisible(self, show):
        self.invokeMethod('setDropItemIconVisible', Scaleform.GfxValue(show))
        self.setGuiStateChange(True)

    def showSkillIndicator(self):
        self.initTopLogoAni()
        if self.aniMovie:
            self.invokeAniMethod('loadSkillIndicator')
            self.setGuiStateChange(True)

    def removeSkillIndicator(self):
        if self.aniMovie:
            self.invokeAniMethod('removeSkillIndicator')
            self.setGuiStateChange(True)

    def showMvp(self):
        self.initTopLogoAni()
        if self.aniMovie:
            self.invokeAniMethod('loadMvp')

    def removeMvp(self):
        if self.aniMovie:
            self.invokeAniMethod('removeMvp')

    def updateWingCampIcon(self):
        en = BigWorld.entity(self.entity)
        p = BigWorld.player()
        if not p.isWingWorldCampMode() or not en or not en.inWorld:
            self.removeOtherIcon()
            self.setIconBorder('')
            return
        if formula.spaceInWingWarCity(p.spaceNo):
            wingCamp = getattr(en, 'wingWorldCamp', 0)
            if wingCamp == 1:
                campIconName = WWCD.data.get('wingCampIcons', gameStrings.WING_WORLD_CAMP_ICONS).get(1, '1010')
                self.addOtherIcon('../wingWorld/wingWorldFlag/%s.dds' % campIconName)
                self.setIconBorder('camp11')
            elif wingCamp == 2:
                campIconName = WWCD.data.get('wingCampIcons', gameStrings.WING_WORLD_CAMP_ICONS).get(1, '1009')
                self.addOtherIcon('../wingWorld/wingWorldFlag/%s.dds' % campIconName)
                self.setIconBorder('camp21')
            else:
                self.removeOtherIcon()
                self.setIconBorder('')
        else:
            self.removeOtherIcon()
            self.setIconBorder('')

    def updateBorderIconAndOtherIcon(self):
        en = BigWorld.entity(self.entity)
        p = BigWorld.player()
        if not en or not en.inWorld:
            self.removeOtherIcon()
            self.setIconBorder('')
            return
        if formula.spaceInWingWarCity(p.spaceNo) and p.isWingWorldCampMode():
            self.updateWingCampIcon()
        elif gameglobal.rds.configData.get('enableNewGuildTournament', False):
            guildRankLevelType = en.getGuildRankLevelType()
            self.removeOtherIcon()
            if guildRankLevelType and guildRankLevelType >= 3:
                self.setIconBorder('tournament%d' % (guildRankLevelType - 2))
            else:
                self.setIconBorder('')
        else:
            self.removeOtherIcon()
            self.setIconBorder('')
            return

    def updatePkTopLogo(self):
        en = BigWorld.entity(self.entity)
        if not en or not en.inWorld:
            return
        isKillMode = en.pkMode == const.PK_MODE_KILL or en.pkMode == const.PK_MODE_HOSTILE
        pkLv = self._getPKLv(en)
        if isKillMode and not BigWorld.player().inFuben():
            self.showPKLogo(en.pkMode == const.PK_MODE_KILL, pkLv)
        else:
            self.stopPKLogo()

    def _getPKLv(self, en):
        pkVal = getattr(en, 'pkPunishTime', 0)
        pkLvSplit = SCD.data.get('pkLvSplit', [120, 9000, 87000])
        if pkVal <= 0:
            return uiConst.PK_VAL_LV0
        if 0 < pkVal <= pkLvSplit[0]:
            return uiConst.PK_VAL_LV1
        if pkLvSplit[0] < pkVal <= pkLvSplit[1]:
            return uiConst.PK_VAL_LV2
        if pkLvSplit[1] < pkVal <= pkLvSplit[2]:
            return uiConst.PK_VAL_LV3
        if pkLvSplit[2] < pkVal:
            return uiConst.PK_VAL_LV4

    def hidePkTopLogo(self):
        self.stopPKLogo()

    def hideAvatarTitle(self, hide):
        if not hide and MCD.data.get(BigWorld.player().mapID, {}).get('isHideAvatarTitle', 0):
            hide = True
        self.invokeMethod('hideAvatarTitle', Scaleform.GfxValue(hide))
        self.setGuiStateChange(True)
        en = BigWorld.entity(self.entity)
        if en.curEffectTitleId > 0:
            self.hideTitleEffect(hide)

    def showSelector(self, isShow, showType = 'green'):
        if isShow:
            self.invokeMethod('showSelector', (Scaleform.GfxValue(True), Scaleform.GfxValue(showType)))
            self.setGuiStateChange(True)
            self.hideName(not self.nameVisible)
        else:
            self.invokeMethod('showSelector', (Scaleform.GfxValue(False), Scaleform.GfxValue(showType)))
            self.setGuiStateChange(True)
            self.hideName(not self.nameVisible)
        self.setGuiStateChange(True)

    def setBoothName(self, name):
        self.invokeMethod('setBoothName', Scaleform.GfxValue(gbk2unicode(name)))
        self.setGuiStateChange(True)

    def setBoothBg(self):
        en = BigWorld.entity(self.entity)
        if not en or not en.inWorld:
            return
        picName = BSD.data.get(en.curBoothToplogoId, {}).get('PicName', '')
        boothBgPath = BOOTH_PATH_PREFIX + picName + '.dds'
        self.setGuiStateAdvance(True)
        self.invokeMethod('setBoothBg', (Scaleform.GfxValue(boothBgPath), Scaleform.GfxValue(self.entity)))
        BigWorld.callback(5.0, Functor(self.setGuiStateChange, True))
        BigWorld.callback(15.0, Functor(self.setGuiStateChange, True))

    def setBoothVisible(self, visible):
        if visible:
            self.gui.canFocus = True
        else:
            self.gui.canFocus = False
        self.invokeMethod('setBoothVisible', Scaleform.GfxValue(visible))
        self.setGuiStateChange(True)
        if visible:
            self.setBoothBg()
        gameglobal.rds.ui.refreshTeamLogoOrIdentity(self.entity)

    def setFindLogo(self, logoId):
        path = FINDLOGO_PATH_PREFIX + str(logoId) + '.dds'
        self.setGuiStateAdvance(True)
        self.invokeMethod('setFindLogo', (Scaleform.GfxValue(path), Scaleform.GfxValue(self.entity)))
        BigWorld.callback(5.0, Functor(self.setGuiStateChange, True))
        BigWorld.callback(15.0, Functor(self.setGuiStateChange, True))

    def removeFindLogo(self):
        self.invokeMethod('removeFindLogo')
        self.setGuiStateChange(True)

    def setChatRoomName(self, name):
        self.invokeMethod('setChatRoomName', Scaleform.GfxValue(gbk2unicode(name)))
        self.setGuiStateChange(True)

    def setChatRoomVisible(self, visible):
        self.invokeMethod('setChatRoomVisible', Scaleform.GfxValue(visible))
        self.setGuiStateChange(True)

    def setAutoFishingVisible(self, visible):
        self.invokeMethod('setAutoFishingVisible', Scaleform.GfxValue(visible))
        self.setGuiStateChange(True)

    def setMakingVisible(self, visible):
        self.invokeMethod('setMakingVisible', Scaleform.GfxValue(visible))
        self.setGuiStateChange(True)

    def setProducingVisible(self, visible):
        self.invokeMethod('setProducingVisible', Scaleform.GfxValue(visible))
        self.setGuiStateChange(True)

    def setCollectingVisible(self, visible):
        self.invokeMethod('setCollectingVisible', Scaleform.GfxValue(visible))
        self.setGuiStateChange(True)

    def setAutoPathingVisible(self, visible):
        self.invokeMethod('setAutoPathingVisible', Scaleform.GfxValue(visible))
        self.setGuiStateChange(True)

    def setAutoPlayScenarioVisible(self, visible):
        self.invokeMethod('setAutoPlayScenarioVisible', Scaleform.GfxValue(visible))
        self.setGuiStateChange(True)

    def setTeamLogo(self, showType):
        self.invokeMethod('setTeamLogo', Scaleform.GfxValue('a' + str(showType)))
        self.setGuiStateChange(True)

    def removeTeamLogo(self):
        self.invokeMethod('removeTeamLogo')
        self.setGuiStateChange(True)

    def hideTeamLogo(self, bHide):
        self.invokeMethod('hideTeamLogo', Scaleform.GfxValue(bHide))
        self.setGuiStateChange(True)

    def setTeamIdentity(self, showType):
        self.invokeMethod('setTeamIdentity', Scaleform.GfxValue(str(showType)))
        self.setGuiStateChange(True)

    def removeTeamIdentity(self):
        self.invokeMethod('removeTeamIdentity')
        self.setGuiStateChange(True)

    def setFFLScore(self, score):
        self.invokeMethod('setFFLScore', Scaleform.GfxValue(score))
        self.setGuiStateChange(True)

    def removeFFLScore(self):
        self.invokeMethod('removeFFLScore')
        self.setGuiStateChange(True)

    def setTitleEffectHeight(self):
        self.invokeMethod('setTitleEffectHeight', Scaleform.GfxValue(self.titleEffectHeight))

    def showEmote(self, emoteId, forece = False):
        en = BigWorld.entity(self.entity)
        if not en or not en.inWorld:
            return False
        if hasattr(en, 'carrier') and en.carrier.isReadyState() and not forece:
            return
        data = ED.data.get(int(emoteId))
        if data:
            stype = data.get('type')
            if stype == const.EMOTE_TYPE_EMOTION:
                path = EMOTE_PATH_PREFIX + '%s%s' % (data.get('res'), gameglobal.rds.ui.getUIExt())
                self.showEmoteByPath(path)

    def needUpdate(self):
        en = BigWorld.entity(self.entity)
        if not en or not en.inWorld:
            return False
        if en.IsMonster:
            return True
        fps = BigWorld.getFps()
        pos = BigWorld.player().position
        distToPlayer = (en.position - pos).length
        if fps < self.TOPLOGUPDATE_FPS:
            if distToPlayer > self.TOPLOGUPDATE_DIST:
                return False
        return True

    def refreshGuildIconInWorldWarEx(self):
        en = BigWorld.entity(self.entity)
        p = BigWorld.player()
        postId = getattr(en, 'wwArmyPostId', 0)
        imgPath = WWAD.data.get(postId, {}).get('topLogoIcon')
        if p.inWorldWarEx() and postId and imgPath:
            isSameCamp = en._isSoul() == p._isSoul()
            camp = p.worldWar.getCurrCamp() if isSameCamp else p.worldWar.getCurrEnemyCamp()
            self.setGuildImage('../' + uiConst.WW_ARMY_POST_TOPLOGO_ICON_PATH + '%s_%s.dds' % (imgPath, camp), '', True)
        else:
            self.removeGuildIcon()

    def startCastbar(self, castName, keepTime, countDown = False):
        self.castBarKeepTime = keepTime
        self.showSpellBar(True)
        self.setSpellBarName(gbk2unicode(castName))
        self.castBarTotaltick = keepTime
        self.castBarStarttick = BigWorld.time()
        if self.castbarCBHandler:
            BigWorld.cancelCallback(self.castbarCBHandler)
            self.castbarCBHandler = None
        self.castbarCBHandler = BigWorld.callback(0.05, Functor(self._updateCastBar, countDown))

    def _updateCastBar(self, countDown):
        pastTime = BigWorld.time() - self.castBarStarttick
        leftTime = self.castBarTotaltick - pastTime
        if leftTime > 0:
            self.setSpellTime('%.1f' % leftTime, pastTime / self.castBarTotaltick)
            self.castbarCBHandler = BigWorld.callback(0.05, Functor(self._updateCastBar, countDown))
        else:
            self.notifyCastbarInterrupt()

    def notifyCastbarInterrupt(self):
        self.showSpellBar(False)
        if self.castbarCBHandler:
            BigWorld.cancelCallback(self.castbarCBHandler)
            self.castbarCBHandler = None

    def setHideBloodNumState(self, isHideBloodNum):
        self.invokeMethod('setHideBloodNumState', Scaleform.GfxValue(isHideBloodNum))
        self.setGuiStateChange(True)

    def refreshCountDown(self):
        if gameglobal.rds.ui.huntGhost.isOpen():
            ghostInfos = gameglobal.rds.ui.huntGhost.bigBoxInfo
            for entId, boxInfo in ghostInfos.iteritems():
                bornTime, _ = boxInfo
                if BigWorld.entity(self.entity).id == entId:
                    existTime = bornTime + HGCD.data.get('BigBoxExistTime', 120) - utils.getNow()
                    self.startNameCountDown(existTime)

    def startNameCountDown(self, countDown):
        if self.nameCountDownTimer:
            BigWorld.cancelCallback(self.nameCountDownTimer)
            self.nameCountDownTimer = None
        treasureBox = BigWorld.entity(self.entity)
        if not treasureBox:
            return
        else:
            boxData = treasureBox.getItemData()
            if countDown > 0:
                treasureBox.addEffects(boxData.get('effectBeforeEnableOpen'))
            else:
                treasureBox.addEffects(boxData.get('effectAfterEnableOpen'))
            self._updateNameCountDown(countDown)
            return

    def _updateNameCountDown(self, countDown):
        en = BigWorld.entity(self.entity)
        if not en:
            return
        else:
            name = self.genFullName(self.name)
            if self.qualityColor:
                name = "<font color=\'" + self.qualityColor + "\'>" + name + '</font>'
            if countDown > 0:
                name = name + "<font color=\'#FF0000\'>%s</font>" % utils.formatTimeStr(countDown, 'm:s', zeroShow=True, sNum=2, mNum=2)
                self.invokeMethod('setName', Scaleform.GfxValue(gbk2unicode(name)))
                self.setGuiStateChange(True)
                self.setColor(self.nameClolor)
                countDown -= 1
                self.nameCountDownTimer = BigWorld.callback(1, Functor(self._updateNameCountDown, countDown))
            else:
                self.invokeMethod('setName', Scaleform.GfxValue(gbk2unicode(name)))
                self.setGuiStateChange(True)
                self.setColor(self.nameClolor)
                treasureBox = BigWorld.entity(self.entity)
                boxData = treasureBox.getItemData()
                treasureBox.removeEffects(boxData.get('effectBeforeEnableOpen'))
                treasureBox.addEffects(boxData.get('effectAfterEnableOpen'))
                if self.nameCountDownTimer:
                    BigWorld.cancelCallback(self.nameCountDownTimer)
                    self.nameCountDownTimer = None
            return
