#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/uiUtils.o
from gamestrings import gameStrings
import types
import re
import copy
import ResMgr
import math
import Math
import time
import BigWorld
import gameglobal
import gametypes
import const
import gamelog
import appSetting
import npcConst
import formula
import clientcom
import commcalc
import logicInfo
import qrcode
import base64
import utils
import uiConst
from Scaleform import GfxValue
from ui import gbk2unicode, unicode2gbk
from helpers import charRes
from helpers import avatarMorpher
from helpers import navigator
from friend import FriendVal
from callbackHelper import Functor
from item import Item
from gameStrings import gameStrings
import itemToolTipUtils
import pinyinConvert
import challengePassportUtils
from guis import richTextUtils
from asObject import ASUtils
from guis.asObject import TipManager
from data import fame_data as FAMED
from data import seeker_data as SD
from data import baodian_menu_data as BMD
from data import baodian_content_data as BCD
from data import item_data as ID
from data import monster_model_client_data as MMCD
from cdata import font_config_data as FCD
from data import npc_model_client_data as NMCD
from data import npc_action_data as NAD
from data import sys_config_data as SCD
from data import battle_field_data as BFD
from data import battle_field_mode_data as BFMD
from data import arena_mode_data as AMD
from data import sheng_si_chang_data as SSCD
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from data import consumable_item_data as CID
from cdata import dye_ref_data as DRD
from data import equip_data as ED
from data import quest_data as QD
from data import chunk_mapping_data as CMD
from data import fb_data as FD
from data import guild_config_data as GCD
from data import avatar_lv_data as ALD
from data import activity_basic_data as ABD
from cdata import group_match_tree_data as GMTD
from cdata import group_fb_menu_data as GFMD
from cdata import pos2Chunk_data as PCD
from data import prop_ref_data as PRD
from data import skill_effects_data as SED
from data import state_data as STAD
from cdata import pskill_data as PD
from data import skill_tip_formula_data as STD
from data import fkey_data as FKD
from data import map_config_data as MCD
from data import duel_config_data as DCD
from data import zaiju_data as ZD
from data import equip_prefix_prop_data as EPPD
from data import equip_enhance_refining_data as EERD
from cdata import equip_enhance_juexing_prop_data as EEJPD
from cdata import equip_star_factor_data as ESFCD
from cdata import equip_transform_dikou_data as ETDD
from cdata import equip_juexing_reforge_data as EJRD
from data import achievement_data as AD
from data import equip_enhance_juexing_data as EEJD
from data import arena_score_desc_data as ASDD
from data import group_label_data as GLD
from cdata import equip_quality_factor_data as EQFD
from data import activity_achieve_score_config_data as AASCFD
from data import activity_signin_type_data as ASTD
from cdata import yaopei_lv_exp_data as YLED
from cdata import home_config_data as HCD
from data import pvp_enhance_display_data as PEDD
from cdata import pursue_pvp_enhance_data as PPED
from cdata import pvp_enhance_lv_data as PELD
from cdata import pursue_server_config_data as PSCD
from data import summon_sprite_ability_display_data as SSADD
from data import school_data as SCOOLD
from data import item_name_data as IND
from data import summon_sprite_data as SSD
from data import summon_sprite_info_data as SSID
from data import horsewing_data as HWCD
from cdata import challenge_passport_season_data as CPSD
from data import challenge_passport_config_data as CPCD
from data import npc_data as ND
from data import nf_npc_data as NND
from cdata import equip_special_props_data as ESPD
ICON_FILE_EXT = '.dds'
XING_JI_TIME_WORD = [gameStrings.TEXT_UIUTILS_116,
 gameStrings.TEXT_UIUTILS_116_1,
 gameStrings.TEXT_UIUTILS_116_2,
 gameStrings.TEXT_UIUTILS_116_3,
 gameStrings.TEXT_UIUTILS_116_4,
 gameStrings.TEXT_UIUTILS_116_5,
 gameStrings.TEXT_UIUTILS_116_6,
 gameStrings.TEXT_UIUTILS_116_7,
 gameStrings.TEXT_UIUTILS_116_8,
 gameStrings.TEXT_UIUTILS_116_9,
 gameStrings.TEXT_UIUTILS_116_10,
 gameStrings.TEXT_UIUTILS_116_11,
 gameStrings.TEXT_UIUTILS_116,
 gameStrings.TEXT_UIUTILS_116_1,
 gameStrings.TEXT_UIUTILS_116_2]

def unLatchItem(item, kind, page, pos):
    p = BigWorld.player()
    if not item.isLatchOfTime():
        if not p.cipherOfPerson:
            gameglobal.rds.ui.inventoryPassword.show(kind, page, pos)
        else:
            p.cell.unLatchCipher(kind, page, pos, p.cipherOfPerson)
    else:
        p.showGameMsg(GMDD.data.LATCH_FORBIDDEN_HAS_LATCH, ())


def findTrackId(id):
    if type(id) == str:
        try:
            id = eval(id)
        except:
            return 0

    p = BigWorld.player()
    if type(id) == types.TupleType:
        idList = list(id)
        minDis = -1
        index = 0
        if idList:
            index = idList[0]
        for item in idList:
            data = SD.data.get(item, None)
            if data:
                pos = Math.Vector3(data['xpos'], data['ypos'], data['zpos'])
                tempDis = (p.position - pos).length
                if (minDis == -1 or minDis > tempDis) and formula.getMapId(data.get('spaceNo', 0) == p.mapID):
                    minDis = tempDis
                    index = item

        id = index
    return id


def findNearestNpcName(id):
    id = eval(id)
    p = BigWorld.player()
    if type(id) == types.TupleType:
        idList = list(id)
        minDis = -1
        spaceDelta = -1
        index = 0
        for item in idList:
            data = SD.data.get(item, None)
            if data:
                pos = Math.Vector3(data['xpos'], data['ypos'], data['zpos'])
                spaceNo = data['spaceNo']
                if p.mapID != spaceNo and p.mapID in data.get('sharedMaps', ()):
                    spaceNo = p.mapID
                tempDis = (p.position - pos).length
                tempSpaceDelta = math.fabs(p.mapID - formula.getMapId(spaceNo))
                if spaceDelta == -1 or spaceDelta > tempSpaceDelta or tempSpaceDelta == spaceDelta and (minDis == -1 or minDis > tempDis):
                    spaceDelta = tempSpaceDelta
                    minDis = tempDis
                    index = item

        id = index
        if index == 0:
            id = idList[0]
    sData = SD.data.get(id, {})
    npcName = sData.get('name', '')
    return npcName


def findPosWithAlert(seekId, message = gameStrings.TEXT_UIUTILS_181):
    seekId = findTrackId(seekId)
    if not seekId:
        return
    p = BigWorld.player()
    navigatorNeedLeaveSpace = SCD.data.get('navigatorNeedLeaveSpace', (1,))
    if p.mapID in navigatorNeedLeaveSpace:
        spaceNo = SD.data.get(seekId, {}).get('spaceNo', -1)
        mapId = formula.getMapId(spaceNo)
        if mapId != p.mapID and mapId == const.SPACE_NO_BIG_WORLD:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(message, Functor(findPosById, seekId))
            return
    findPosById(seekId)


def findPosById(seekId, resetNavigator = False, failedCallback = None):
    try:
        p = BigWorld.player()
        bestSeekId = findTrackId(seekId)
        if SD.data.has_key(bestSeekId):
            sd = SD.data[bestSeekId]
            spaceNo = sd['spaceNo']
            endDist = sd.get('distance', 1.5)
            pos = Math.Vector3(sd['xpos'], sd['ypos'], sd['zpos'])
            if p.mapID != spaceNo and p.mapID in sd.get('sharedMaps', ()):
                spaceNo = p.mapID
            dist = p.position.distTo(pos)
            if dist <= 60:
                ent, _ = searchEnt(bestSeekId, 80)
                if ent:
                    pos = ent.position
            if getattr(p, 'inForceNavigate', False) and p.bianshen[0] == gametypes.BIANSHEN_ZAIJU:
                return
            if p.canPathFindingWingWorld(spaceNo):
                from helpers import wingWorld
                wingWorld.pathFinding((pos.x,
                 pos.y,
                 pos.z,
                 spaceNo), endDist=endDist)
            else:
                navigator.getNav().pathFinding((pos.x,
                 pos.y,
                 pos.z,
                 spaceNo), None, failedCallback, True, endDist, Functor(BigWorld.callback, 0.2, Functor(findcallback, bestSeekId)), resetNavigator=resetNavigator)
        if p.inCombat:
            p.lastPathFindInfo = {'type': uiConst.RESTART_FIND_POS_TYPE_BY_ID,
             'seekId': seekId}
        else:
            p.lastPathFindInfo = {}
    except:
        pass


def findPosByPos(spaceNo, pos):
    if spaceNo is None or pos is None:
        return
    else:
        p = BigWorld.player()
        if getattr(p, 'inForceNavigate', False) and p.bianshen[0] == gametypes.BIANSHEN_ZAIJU:
            return
        navigator.getNav().pathFinding((pos.x,
         pos.y,
         pos.z,
         spaceNo), None, None, True, 1.5, Functor(BigWorld.callback, 0.2, findcallback))
        if p.inCombat:
            p.lastPathFindInfo = {'type': uiConst.RESTART_FIND_POS_TYPE_BY_POS,
             'spaceNo': spaceNo,
             'pos': pos}
        else:
            p.lastPathFindInfo = {}
        return


def cmpEnt(ent1, ent2):
    weight = {'Monster': 1,
     'Npc': 2,
     'QuestBox': 3,
     'Other': 4}
    clsName1 = ent1.__class__.__name__
    clsName2 = ent2.__class__.__name__
    w1 = weight.get(clsName1, 4)
    w2 = weight.get(clsName2, 4)
    if w1 != w2:
        return cmp(w1, w2)
    else:
        p = BigWorld.player()
        return cmp(ent1.position.distTo(p.position), ent2.position.distTo(p.position))


def searchEnt(seekDataId, searchDist = 20):
    sd = SD.data.get(seekDataId, {})
    npcId = sd.get('npcId', None)
    monsterId = sd.get('monsterId', None)
    multiTarget = sd.get('multiTarget', None)
    if not npcId and not monsterId and not multiTarget:
        return (None, uiConst.FIND_ENT_USE_TYPE_DEFAULT)
    else:
        if multiTarget:
            multiEnts = []
            for i in xrange(len(multiTarget)):
                multiEnts.append([multiTarget[i][0].lower(),
                 multiTarget[i][1],
                 multiTarget[i][2],
                 multiTarget[i][3]])

        else:
            multiEnts = [[sd.get('type', 'Npc').lower(),
              npcId,
              monsterId,
              sd.get('useType', 0)]]
        p = BigWorld.player()
        ents = [ ent for ent in BigWorld.entities.values() if ent.position.distTo(p.position) <= searchDist ]
        ents = sorted(ents, cmpEnt)
        for i in xrange(len(multiEnts)):
            npcType = multiEnts[i][0]
            npcId = multiEnts[i][1]
            monsterId = multiEnts[i][2]
            useType = multiEnts[i][3]
            for ent in ents:
                if hasattr(ent, 'beHide') and ent.beHide:
                    continue
                if not getattr(ent, 'life', gametypes.LIFE_ALIVE):
                    continue
                if ent.IsMonster and getattr(ent, 'visibleGbId', 0) == p.gbId and p.isEnemy(ent):
                    if hasattr(ent, 'canSelected') and ent.canSelected():
                        return (ent, useType)
                if npcType in ('monster', 'spawnpoint'):
                    if ent.IsMonster and ent.charType == monsterId:
                        return (ent, useType)
                elif npcType == 'npc':
                    if getattr(ent, 'npcId', 0) == npcId:
                        return (ent, useType)
                elif npcType == 'questbox':
                    if getattr(ent, 'questBoxType', 0) == npcId:
                        return (ent, useType)

        return (None, uiConst.FIND_ENT_USE_TYPE_DEFAULT)


def findcallback(seekDataId = 0, searchDist = 20):
    if seekDataId != 0:
        ent, useType = searchEnt(seekDataId, searchDist)
    else:
        ent, useType = None, uiConst.FIND_ENT_USE_TYPE_DEFAULT
    p = BigWorld.player()
    if ent:
        p.lockTarget(ent)
        dir = ent.position - p.position
        p.faceToDir(dir.yaw)
        if useType == uiConst.FIND_ENT_USE_TYPE_PICK_ITEM:
            p.pickNearByItems(True)
        else:
            p.startKeyModeFlow(ent)
    else:
        p.pickNearByItems(True)
    gameglobal.rds.ui.questTrack.showPathFindingIcon(False)
    p.topLogo.setAutoPathingVisible(False)


def genIconsAr(icon):
    iconAr = gameglobal.rds.ui.movie.CreateArray()
    path = 'item/icon64/' + str(ID.data.get(icon[0], {}).get('icon', 'notFound')) + '.dds'
    count = icon[1]
    itemId = icon[0]
    quality = ID.data.get(icon[0], {}).get('quality', 1)
    qualityColor = getColorByQuality(quality)
    iconAr.SetElement(0, GfxValue(path))
    iconAr.SetElement(1, GfxValue(count))
    iconAr.SetElement(2, GfxValue(itemId))
    iconAr.SetElement(3, GfxValue(qualityColor))
    return iconAr


def onQuit():
    gamelog.debug('hjx debug schedule#quit#onQueryClose:', gameglobal.rds.GameState, BigWorld.player())
    if gameglobal.rds.isSinglePlayer:
        BigWorld.quit()
        return
    gameglobal.rds.uiLog.sendLogs()
    p = BigWorld.player()
    if gameglobal.CURRENT_WINDOW_STYLE == gameglobal.WINDOW_STYLE_CHAT:
        p.setWindowStyle(gameglobal.WINDOW_STYLE_NORMAL)
        return
    if hasattr(p, 'soundRecordNum') and sum(p.soundRecordNum):
        p.base.genSoundRecordNum(p.soundRecordNum[0], p.soundRecordNum[1])
        p.soundRecordNum = [0, 0]
    if gameglobal.rds.GameState == gametypes.GS_LOGIN:
        p = BigWorld.player()
        if p and p.__class__.__name__ == 'PlayerAccount':
            p.base.logAccountOffline(str(gameglobal.rds.loginScene.stage), getattr(gameglobal.rds, 'gameCode', ''))
        BigWorld.quit()
    elif gameglobal.rds.GameState == gametypes.GS_PLAYGAME:
        p = BigWorld.player()
        if gameglobal.rds.configData.get('enableAntiIndulgenceLoginClient', False):
            indulgeCondition = p.indulgeState in const.INDULGE_PERMIT_STATES
        else:
            indulgeCondition = True
        if gameglobal.rds.ui.playRecommActivation.showDailyPanel() and not p._isSoul() and indulgeCondition:
            gameglobal.rds.ui.playRecomm.hide()
            gameglobal.rds.ui.playRecomm.isQuitGame = True
            gameglobal.rds.ui.playRecomm.show()
        else:
            gameglobal.rds.ui.playRecomm.exitGame()
        appSetting.GameSettingObj.saveHideValue()
        appSetting.Obj.save()
    else:
        p = clientcom.getPlayerAvatar()
        if p:
            p.base.setOfflineType(gametypes.PLAYER_OFFLINE_TYPE_LOADING)
            BigWorld.callback(const.QUIT_GAME_DELAY, BigWorld.quit)
        else:
            BigWorld.quit()


def doRealQuit():
    p = clientcom.getPlayerAvatar()
    if p:
        p.base.setOfflineType(gametypes.PLAYER_OFFLINE_TYPE_NORMAL)


def unlogoff():
    p = BigWorld.player()
    p.cell.unlogOff()
    gameglobal.isModalDlgShow = False
    p.base.setOfflineType(gametypes.PLAYER_OFFLINE_TYPE_ERROR)


def _checkItemNewFlag(page = 0, pos = 0, item = None):
    item = BigWorld.player().inv.getQuickVal(page, pos) if item == None else item
    if item and item.type == Item.BASETYPE_EQUIP:
        return True
    else:
        return False


def array2GfxAarry(source, toUnicode = False):
    target = gameglobal.rds.ui.movie.CreateArray()
    for index, item in enumerate(source):
        if item.__class__.__name__ == 'int' or item.__class__.__name__ == 'float':
            target.SetElement(index, GfxValue(item))
        elif isinstance(item, list) or isinstance(item, tuple):
            target.SetElement(index, array2GfxAarry(item, toUnicode))
        elif isinstance(item, dict):
            target.SetElement(index, dict2GfxDict(item, toUnicode))
        elif isinstance(item, GfxValue):
            target.SetElement(index, item)
        elif isinstance(item, str) and toUnicode:
            target.SetElement(index, GfxValue(gbk2unicode(item)))
        elif isinstance(item, long):
            target.SetElement(index, GfxValue(str(item)))
        elif item == None:
            nullObj = GfxValue(1)
            nullObj.SetNull()
            target.SetElement(index, nullObj)
        else:
            target.SetElement(index, GfxValue(item))

    return target


def array2GBKArray(sources):
    target = [None] * len(sources)
    for index, item in enumerate(sources):
        if item.__class__.__name__ == 'int' or item.__class__.__name__ == 'float' or item == None or isinstance(item, long):
            target[index] = sources[index]
        elif isinstance(item, list) or isinstance(item, tuple):
            target[index] = array2GBKArray(sources[index])
        elif isinstance(item, dict):
            target[index] = dict2GBKict(sources[index])
        elif isinstance(item, str):
            target[index] = unicode2gbk(sources[index])
        else:
            target[index] = sources[index]

    return target


def dict2GBKict(source):
    target = {}
    if isinstance(source, dict):
        for key, item in source.items():
            if item.__class__.__name__ == 'int' or item.__class__.__name__ == 'float' or item == None or isinstance(item, long):
                target[key] = item
            elif isinstance(item, list) or isinstance(item, tuple):
                target[key] = array2GBKArray(item)
            elif isinstance(item, dict):
                target[key] = dict2GBKict(item)
            elif isinstance(item, str):
                target[key] = unicode2gbk(item)
            else:
                target[key] = unicode2gbk(item)

    return target


def dict2GfxDict(source, toUnicode = False):
    target = gameglobal.rds.ui.movie.CreateObject()
    if isinstance(source, dict):
        for key, item in source.items():
            if item.__class__.__name__ == 'int' or item.__class__.__name__ == 'float':
                target.SetMember(key, GfxValue(item))
            elif isinstance(item, list) or isinstance(item, tuple):
                target.SetMember(key, array2GfxAarry(item, toUnicode))
            elif isinstance(item, dict):
                target.SetMember(key, dict2GfxDict(item, toUnicode))
            elif isinstance(item, GfxValue):
                target.SetMember(key, item)
            elif isinstance(item, str) and toUnicode:
                target.SetMember(key, GfxValue(gbk2unicode(item)))
            elif item == None:
                nullObj = GfxValue(1)
                nullObj.SetNull()
                target.SetMember(key, nullObj)
            elif isinstance(item, long):
                target.SetMember(key, GfxValue(str(item)))
            else:
                target.SetMember(key, GfxValue(item))

    return target


def gfxArray2Array(source):
    if isinstance(source, GfxValue) and source.GetArraySize() > 0:
        size = source.GetArraySize()
        result = []
        for i in range(size):
            result.append(source.GetElement(i))

        return result


def _isNeedShowBossBlood(charType):
    md = MMCD.data.get(charType, None)
    if md:
        showBlood = md.get('showBlood', 0)
        return showBlood
    else:
        return 0


def onTargetSelect(ent):
    p = BigWorld.player()
    isShowingEffect = BigWorld.player().chooseEffect.isShowingEffect
    if isShowingEffect:
        if ent:
            BigWorld.player().chooseEffect.run(ent)
            BigWorld.player().ap.reset()
            return
    if ent:
        p.lockTarget(ent, True, True)


def getEquipItemById(pos):
    p = BigWorld.player()
    if pos >= len(p.equipment):
        gamelog.debug('getEquipItemById equipment error: Exceed Length!')
        return
    return p.equipment[pos]


def npcType2npcPanelType(npcType):
    if npcType == npcConst.NPC_FUNC_TELEPORT:
        return uiConst.NPC_TELEPORT
    elif npcType in npcConst.NPC_FUNC_TYPE:
        return uiConst.NPC_FUNC
    elif npcType == npcConst.NPC_FUNC_QUEST:
        return uiConst.NPC_QUEST
    else:
        return uiConst.NPC_TELEPORT


def parseMsg(msg):
    msg = re.sub('</?TEXTFORMAT.*?>', '', msg, 0, re.DOTALL)
    msg = re.sub('</?P.*?>', '', msg, 0, re.DOTALL)
    msg = re.sub('</?B.*?>', '', msg, 0, re.DOTALL)
    fontFormat = re.compile('<FONT(.+?)COLOR=(.{9})(.+?)>', re.DOTALL)
    msg = fontFormat.sub(FontColorAdd, msg)
    msg = re.compile('#([0-9]{1})').sub('!$\\1', msg)
    msg = re.compile('!\\$([A-Fa-f0-9]{6})').sub('#\\1', msg)
    return msg


def getPinXing(idx):
    if ID.data.get(idx, {}).get('type', -1) == Item.BASETYPE_UNIDENTIFIED:
        return 'undef'
    elif ID.data.get(idx, {}).get('identifyQuality', 0) > 0:
        return 'spc'
    else:
        return 'nor'


def getItemData(itemId):
    iconPath = getItemIconFile64(itemId)
    color = getItemColor(itemId)
    return {'id': itemId,
     'itemId': itemId,
     'iconPath': iconPath,
     'quality': color}


def getColorByQuality(quality):
    color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
    return color


def getColorValueByQuality(quality):
    color = FCD.data.get(('item', quality), {}).get('color')
    return color


def getItemColor(itemId):
    quality = getItemQuality(itemId)
    color = getColorByQuality(quality)
    return color


def getItemQuality(itemId):
    itemData = ID.data.get(itemId, {})
    if itemData.has_key('dotaItemQuality') and BigWorld.player().isInBfDota():
        return itemData.get('dotaItemQuality', 1)
    return itemData.get('quality', 1)


def getItemColorByItem(item):
    color = 'nothing'
    if item:
        if hasattr(item, 'quality'):
            quality = item.quality
        else:
            quality = getItemQuality(item.id)
        color = getColorByQuality(quality)
    return color


def getItemColorName(itemId, itemCnt = 1):
    name = ID.data.get(itemId, {}).get('name', '')
    if itemCnt > 1:
        name = '%sx%d' % (name, itemCnt)
    quality = getItemQuality(itemId)
    color = FCD.data.get(('item', quality), {}).get('color', '0xFFFFE7')
    return "<font color=\'%s\'>%s</font>" % (color, name)


def getItemColorNameWithClickTips(itemId, itemCnt = 1):
    name = ID.data.get(itemId, {}).get('name', '')
    if itemCnt > 1:
        name = '%sx%d' % (name, itemCnt)
    quality = getItemQuality(itemId)
    color = FCD.data.get(('item', quality), {}).get('color', '0xFFFFE7')
    return "<font color=\'%s\'>[<a href = \'event:item%s\'><u>%s</u></a>]</font>" % (color, itemId, name)


def getItemQualityColor(itemId):
    quality = getItemQuality(itemId)
    return FCD.data.get(('item', quality), {}).get('qualitycolor', 'white')


def getItemColorNameByItem(item, withPrefix = True, length = -1, withEnhLv = False):
    itemName = ''
    color = ''
    if item:
        itemName = ID.data.get(item.id, {}).get('name', '')
        if withPrefix:
            itemName = getItemPreName(item) + itemName
        if withEnhLv and hasattr(item, 'enhLv'):
            enhLv = getattr(item, 'enhLv', 0)
            if enhLv > 0:
                itemName += '+%d' % enhLv
        if hasattr(item, 'quality'):
            quality = item.quality
        else:
            quality = getItemQuality(item.id)
        color = FCD.data.get(('item', quality), {}).get('color', 'nothing')
        if length > 0:
            try:
                tmpName = unicode(itemName, utils.defaultEncoding())
                if len(tmpName) > length:
                    tmpName = tmpName[0:length - 1]
                    itemName = tmpName.encode(utils.defaultEncoding()) + '...'
            except:
                pass

    return toHtml(itemName, color)


def FontColorAdd(matchobj):
    m = matchobj.group(2)
    return '<FONT COLOR=%s>' % m


def showWindowEffect():
    if gameglobal.gIsAppActive:
        return
    BigWorld.switchToThisWindow()
    BigWorld.flashWindow(10)
    gameglobal.rds.isFlashWindow = True


def _formatstr(m):
    return m.group(1) + "<font color = \'" + m.group(2) + "\'>" + m.group(3) + '</font>'


def pcharAdd(matchobj):
    m0 = matchobj.group(1)
    m1 = matchobj.group(2)
    m2 = matchobj.group(3)
    tempm0 = str(utils.strToUint64(m0))
    return "<font color=\'%s\'>[<a href = \'event:ret%s\'><u>%s</u></a>]</font>" % (m1, tempm0, m2)


def generateStr(msg):
    try:
        reg = re.compile('#\\[(.{8})\\](.{7})\\[(.+?)\\]#n#\\[0\\]', re.DOTALL)
        msg = reg.sub(pcharAdd, msg)
        reg = re.compile('(.*?)\\[(#[a-fA-F0-9]{6})](.+?)\\[/#\\]', re.DOTALL)
        ret = reg.sub(_formatstr, msg)
        return ret
    except:
        gamelog.error('hjx debug tutorial format string error!')
        return msg


def getHourMin(timeValue):
    m = re.match('\\(([0-9]{2}),([0-9]{2})\\)\\-\\(([0-9]{2}),([0-9]{2})\\)', timeValue)
    return (int(m.group(1)),
     int(m.group(2)),
     int(m.group(3)),
     int(m.group(4)))


def getNowTime():
    p = BigWorld.player()
    timeWrap = time.localtime(p.getServerTime())
    return (timeWrap.tm_hour, timeWrap.tm_min)


def getDate():
    p = BigWorld.player()
    timeWrap = time.localtime(p.getServerTime())
    return (timeWrap.tm_year,
     timeWrap.tm_mon,
     timeWrap.tm_mday,
     timeWrap.tm_hour,
     timeWrap.tm_min)


def getDayByOffset(offset):
    p = BigWorld.player()
    timeWrap = time.localtime(p.getServerTime() + offset * 24 * 60 * 60)
    return timeWrap.tm_mday


def getWeekDay():
    p = BigWorld.player()
    timeWrap = time.localtime(p.getServerTime() + 10)
    return timeWrap.tm_wday


def timeStrParse(timeInfo):
    startCrons, endCrons = timeInfo
    if len(startCrons) != len(endCrons):
        return ('*',)
    ret = []
    for i in xrange(len(startCrons)):
        start = utils.parseCrontabPattern(startCrons[i])
        end = utils.parseCrontabPattern(endCrons[i])
        ret.append((start, end))

    return ret


def getConfigSpaceNo(spaceNo):
    return formula.getMapId(spaceNo)


def getConfigSpaceNoCheckFbCopy(spaceNo):
    mapId = formula.getMapId(spaceNo)
    if BigWorld.player().inFuben(mapId):
        mapId = FD.data.get(mapId, {}).get('basicFbNo', mapId)
    return mapId


def getDetailNpc(npcId):
    data = NMCD.data.get(npcId, {})
    modelId = data.get('detailModel', None)
    if not modelId:
        modelId = data.get('model', None)
    tintMs = data.get('materials', ('Default', None))
    if type(tintMs) == tuple:
        tintMs = tintMs[0]
    photoAction = NAD.data.get(data.get('actGroupid', None), {}).get('photoAct', None)
    return (modelId, tintMs, photoAction)


def getDetailNpcWithAttach(npcId):
    data = NMCD.data.get(npcId, {})
    modelId = data.get('detailModel', None)
    if not modelId:
        modelId = data.get('model', None)
    tintMs = data.get('materials', ('Default', None))
    if type(tintMs) == tuple:
        tintMs = tintMs[0]
    p = BigWorld.player()
    addTint = None
    if p and getattr(p, 'lingShiFlag', False) and ND.data.get(npcId, {}).get('lingShiTintName', ''):
        addTint = ND.data.get(npcId, {}).get('lingShiTintName', '')
    elif NMCD.data.get(npcId, {}).get('extraTint', ''):
        addTint = NMCD.data.get(npcId, {}).get('extraTint', '')
    photoAction = NAD.data.get(data.get('actGroupid', None), {}).get('photoAct', None)
    attachesInPhoto = data.get('attachesInPhoto', True)
    attaches = data.get('attaches', None) if attachesInPhoto else None
    wingId = data.get('wingId', None)
    wingActionId = data.get('wingActionId', '21101')
    wingAttach = getWingAttach(ED.data.get(wingId, None), wingActionId)
    if wingAttach:
        if not attaches:
            attaches = []
        else:
            attaches = list(attaches)
        attaches.append(wingAttach)
    return (modelId,
     tintMs,
     photoAction,
     attaches,
     addTint)


def getWingAttach(data, wingAction):
    if not data:
        return
    else:
        modelId = data.get('modelId', None)
        if not modelId:
            return
        subId = data.get('subId', [0])
        if isinstance(subId, tuple) or isinstance(subId, list):
            subId = subId[0]
        horseData = HWCD.data.get(subId, None)
        if not horseData:
            return
        if isinstance(horseData, tuple) or isinstance(horseData, list):
            horseData = horseData[0]
        attachHP = horseData.get('attachHp', None)
        attachScale = 1.0
        return (attachHP,
         '%s/%s.model' % (modelId, modelId),
         0,
         attachScale,
         0.0,
         'char',
         wingAction)


def getAvatarPhotoAct():
    return SCD.data.get('avatarPhotoAct', None)


def takePhoto3D(headGen, target, npcId, isAddTint = False):
    if npcId == 0:
        headGen.startCapture(0, None, getAvatarPhotoAct())
    elif npcId != -1 and npcId != -2:
        modelId, tintMs, photoAction, attaches, addTint = getDetailNpcWithAttach(npcId)
        if not isAddTint:
            addTint = None
        if target and target.inWorld and target.npcId == npcId:
            if getattr(target, 'isMultiModel', False):
                headGen.startCaptureEnt(target, photoAction)
                return
            if getattr(target, 'fashionId', None):
                headGen.startCaptureEnt(target, photoAction)
                return
        if modelId:
            headGen.startCapture(modelId, tintMs, photoAction, attaches=attaches, addTint=addTint)


def getNpcName(npcId, default = ''):
    ret = ''
    if type(npcId) in (tuple, list):
        for id in npcId:
            ret += '%s ' % NMCD.data.get(id, {}).get('name', default)

    else:
        ret = NMCD.data.get(npcId, {}).get('name', default)
    return ret


def getPNpcIcon(npcId):
    defaulutNpcId = NND.data.get(npcId, {}).get('defaultNpcId', npcId)
    if ND.data.get(defaulutNpcId, {}).has_key('npcHeadIcon'):
        npcHeadIcon = ND.data.get(defaulutNpcId, {}).get('npcHeadIcon', 0)
    else:
        npcHeadIcon = NMCD.data.get(defaulutNpcId, {}).get('model', 0)
    return 'npcHeadIcon/%s.dds' % str(npcHeadIcon)


def getNpcTrackId(questId, npcId, trackType = 'comNpc'):
    trackIds = QD.data.get(questId, {}).get(trackType + 'Tk', ())
    if trackType == 'comNpc':
        trackType = 'compNpc'
    npcs = QD.data.get(questId, {}).get(trackType, ())
    if type(npcId) in (tuple, list):
        return tuple(trackIds)
    if type(npcs) in (tuple, list):
        if npcId in npcs:
            idx = npcs.index(npcId)
            return trackIds[idx]
    else:
        return trackIds
    return 0


def getNpcNameAndTitle(npcId):
    data = NMCD.data.get(npcId, {})
    return (data.get('name', ''), data.get('title', ''))


def getBFReliveTime(item, gbId = 0):
    p = BigWorld.player()
    if item is None:
        return 0
    elif not hasattr(p, 'bfTimeRec'):
        return 0
    else:
        reliveTime = 0
        fbNo = formula.getFubenNo(p.spaceNo)
        mode = formula.fbNo2BattleFieldMode(fbNo)
        reliveMode = BFMD.data.get(mode, {}).get('reliveMode', gametypes.BATTLE_FIELD_RELIVE_TYPE_PLAYER)
        if reliveMode == gametypes.BATTLE_FIELD_RELIVE_TYPE_PLAYER:
            timePass = item['tConfirmRelive'] - p.bfTimeRec['tReady']
            intervalIndex = formula.getBattleFieldReliveInterval(p.getBattleFieldFbNo(), timePass / 60)
            reliveInterval = BFD.data.get(p.getBattleFieldFbNo(), {}).get('reliveTime', [])[intervalIndex]
            reliveTime = reliveInterval - int(p.getServerTime() - item['tConfirmRelive'])
        elif reliveMode == gametypes.BATTLE_FIELD_RELIVE_TYPE_SYSTEM:
            if not p.bfTimeRec.has_key('tRelive'):
                return 0
            interval = BFD.data.get(fbNo, {}).get('reliveTime')
            reliveTime = max(interval - (utils.getNow() - p.bfTimeRec['tRelive']), 0)
        elif reliveMode == gametypes.BATTLE_FIELD_RELIVE_TYPE_FORMULA:
            if formula.inDotaBattleField(p.mapID):
                reliveTime = getattr(p, 'reliveTimeRecord', {}).get(gbId, 0) - utils.getNow()
                reliveTime = max(0, reliveTime)
        return int(reliveTime)


def getDuelCountTime(timeName, duelId):
    if formula.inBattleField(duelId):
        duelData = BFD.data.get(duelId, {})
        if duelData:
            return duelData.get(timeName, 30)
    elif formula.inShengSiChang(duelId):
        duelData = SSCD.data.get(duelId, {})
        if duelData:
            return duelData.get(timeName, 30)
    elif formula.inTeamShengSiChang(duelId):
        duelData = SSCD.data.get(duelId, {})
        if duelData:
            return duelData.get(timeName, 30)
    else:
        if formula.inArena(duelId):
            return AMD.data.get(duelId, {}).get(timeName, 30)
        return 30


def gotoTrack(trackId):
    gameglobal.rds.ui.messageBox.showYesNoMsgBox(GMD.data.get(GMDD.data.GOTO_TRACK_PROMPT, {}).get('text'), lambda : _gotoTrack(trackId))


def _gotoTrack(trackId):
    p = BigWorld.player()
    if p.checkPathfinding():
        p.cancelPathfinding()
    canUse = logicInfo.isUseableGuildMemberSkill(const.GUILD_SKILL_XIAOFEIXIE)
    if canUse:
        p.cell.useGuildMemberSkillWithParam(const.GUILD_SKILL_XIAOFEIXIE, (str(trackId),))
    elif p.canResetCD(const.GUILD_SKILL_XIAOFEIXIE):
        msg = GMD.data.get(GMDD.data.CONFIRM_RESET_TRACK_CD, {}).get('text', gameStrings.TEXT_UIUTILS_914)
        itemFameData = {}
        resetCDItems = SCD.data.get('resetGuildTrackSkillCDItems', ())
        if resetCDItems:
            itemId, needNum = resetCDItems
            item = Item(itemId)
            currentCount = BigWorld.player().inv.countItemInPages(item.getParentId(), enableParentCheck=True)
            itemFameData['itemId'] = itemId
            itemFameData['deltaNum'] = needNum - currentCount
        func = Functor(p.cell.resetGuildSkillCD, const.GUILD_SKILL_XIAOFEIXIE, (str(trackId),))
        if not gameglobal.rds.ui.messageBox.getCheckOnceData(uiConst.CHECK_ONCE_TYPE_RESET_TRACK_CD):
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, func, isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_RESET_TRACK_CD, itemFameData=itemFameData)
        else:
            func()
    else:
        p.showGameMsg(GMDD.data.GUILD_SKILL_TRACK_CD, ())


def getAspectParts(equipId):
    player = BigWorld.player()
    ed = ED.data.get(equipId, {})
    slotParts = ed.get('slotParts', [])
    parts = [ player.equipment.FASHION_PARTS_MAP[i] for i in slotParts ]
    return parts


def preDyeModel(model, dyeItemPage, dyeItemPos, equipPage, equipPos, dyeMethod = const.DYE_COPY):
    if not model:
        return
    player = BigWorld.player()
    mpr, _, _ = getDyeModel(dyeItemPage, dyeItemPos, equipPage, equipPos, dyeMethod)
    dyesDict = mpr.dyesDict
    m = avatarMorpher.SimpleModelMorpher(model, player.realPhysique.sex, player.realPhysique.school, player.realPhysique.bodyType, mpr.face, mpr.hair, mpr.head, mpr.body, mpr.hand, mpr.leg, mpr.shoe, False, mpr.headType, dyesDict, cape=mpr.cape)
    m.readConfig(player.realAvatarConfig)
    m.applyDyeMorph(True)


def getDyeModel(dyeItemPage, dyeItemPos, equipPage, equipPos, dyeMethod = const.DYE_COPY):
    player = BigWorld.player()
    if equipPage == const.INV_PAGE_EQUIP:
        equip = player.equipment.get(equipPos)
    elif equipPage == const.INV_PAGE_WARDROBE:
        equip = player.wardrobeBag.getDrobeItem(equipPos)
    else:
        equip = BigWorld.player().inv.getQuickVal(equipPage, equipPos)
    equipCopy = Item(equip.id)
    if hasattr(equip, 'dyeList'):
        equipCopy.dyeList = equip.dyeList
    if not equip or not equip.isCanDye():
        return
    else:
        dyeItem = player.inv.getQuickVal(dyeItemPage, dyeItemPos)
        if not dyeItem or not dyeItem.isDye():
            return
        dyeType = dyeItem.getDyeType()
        dye = []
        if dyeType == Item.CONSUME_DYE_NORMAL:
            dye = CID.data.get(dyeItem.id, {}).get('color')
            dyeData = DRD.data.get(equip.id, {})
            dye = utils.getRealDye(equip, dyeItem, dye, dyeData)
            equipCopy.setDye(dye, dyeMethod)
        elif dyeType == Item.CONSUME_DYE_RANDOM:
            dye = dyeItem.consumeDyeList
            equipCopy.setDye(dye, dyeMethod)
        elif dyeType == Item.CONSUME_DYE_MAGIC:
            dye = dyeItem.consumeDyeList
            equipCopy.setDye(dye, dyeMethod)
        elif dyeType == Item.CONSUME_DYE_SUPER:
            dye = gameglobal.rds.ui.dyeColor.getDyeColor().split(':')
            equipCopy.setDye(dye, dyeMethod)
        elif dyeType == Item.CONSUME_DYE_CLEAN:
            equipCopy.dyeList = ED.data.get(equipCopy.id, {}).get('dyeList', [])
        elif dyeType == Item.CONSUME_DYE_TEXTURE:
            texture = CID.data.get(dyeItem.id, {}).get('texture', ['1', '0', '1'])
            equipCopy.setTexture(texture)
        aspect = copy.deepcopy(player.realAspect)
        aspect = createNewAspect(aspect, equipCopy)
        mpr = charRes.MultiPartRes()
        isShowFashion = False
        if getattr(equip, 'equipType', 0) == Item.EQUIP_BASETYPE_FASHION:
            isShowFashion = True
        mpr.queryByAttribute(player.realPhysique, aspect, isShowFashion, getattr(player, 'realAvatarConfig', None), player.isShowClanWar())
        return (mpr, aspect, isShowFashion)


def getRongGuangModel(dyeItemPage, dyeItemPos, equipPage, equipPos):
    player = BigWorld.player()
    if equipPage == const.INV_PAGE_EQUIP:
        equip = player.equipment.get(equipPos)
    elif equipPage == const.INV_PAGE_WARDROBE:
        equip = player.wardrobeBag.getDrobeItem(equipPos)
    else:
        equip = BigWorld.player().inv.getQuickVal(equipPage, equipPos)
    rongGuangItem = player.inv.getQuickVal(dyeItemPage, dyeItemPos)
    if not equip and not equip.isCanRongGuang():
        return
    else:
        dyeType = rongGuangItem.getRongGuangType()
        if dyeType == Item.CONSUME_RONGGUANG_CLEAN:
            rongGuang = []
        else:
            rongGuang = CID.data.get(rongGuangItem.id, {}).get('rongGuang', [])
        equipCopy = copy.copy(equip)
        equipCopy.rongGuang = rongGuang
        aspect = copy.deepcopy(player.realAspect)
        aspect = createNewAspect(aspect, equipCopy)
        mpr = charRes.MultiPartRes()
        isShowFashion = False
        if getattr(equip, 'equipType', 0) == Item.EQUIP_BASETYPE_FASHION:
            isShowFashion = True
        mpr.queryByAttribute(player.realPhysique, aspect, isShowFashion, getattr(player, 'realAvatarConfig', None), player.isShowClanWar())
        return (mpr, aspect, isShowFashion)


def createNewAspect(aspect, equip):
    if not equip:
        return aspect
    parts = list(equip.whereEquip())
    parts.extend(getAspectParts(equip.id))
    isShowFashion = equip.equipType == Item.EQUIP_BASETYPE_FASHION
    if isShowFashion:
        if getattr(equip, 'equipSType', 0) in (Item.EQUIP_FASHION_SUBTYPE_NEIYI, Item.EQUIP_FASHION_SUBTYPE_NEIKU):
            for part in charRes.PARTS_ASPECT_FASHION_SUB:
                setattr(aspect, part, 0)

        for part in charRes.PARTS_ASPECT_FASHION:
            equipId = getattr(aspect, part)
            if equipId:
                equItem = Item(equipId)
                equipParts = list(equItem.whereEquip())
                equipParts.extend(getAspectParts(equItem.id))
                for itemPart in parts:
                    if itemPart in equipParts:
                        setattr(aspect, part, 0)
                        break

    for part in parts:
        aspect.set(part, equip.id, getattr(equip, 'dyeList', []), getattr(equip, 'enhLv', 0), equip.rongGuang)

    return aspect


def recoveDyeModel(model):
    player = BigWorld.player()
    mpr = charRes.MultiPartRes()
    mpr.queryByAvatar(player)
    m = avatarMorpher.SimpleModelMorpher(model, player.realPhysique.sex, player.realPhysique.school, player.realPhysique.bodyType, mpr.face, mpr.hair, mpr.head, mpr.body, mpr.hand, mpr.leg, mpr.shoe, False, mpr.headType, mpr.dyesDict)
    m.readConfig(player.realAvatarConfig)
    m.applyDyeMorph(True)


def inNeedNotifyStates():
    p = BigWorld.player()
    for stateId in const.NEED_NOTIFY_STATES:
        if p.hasState(stateId):
            return True

    return False


def exitPhase():
    gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_UIUTILS_1072, _doExitPhase)


def _doExitPhase():
    p = BigWorld.player()
    if getattr(p, 'inGroupFollow', None) and not getattr(p, 'groupHeader', None) == p.id:
        p.cell.cancelGroupFollow()
    p.cell.teleportOutPhaseByIcon(const.SPACE_NO_BIG_WORLD)
    p.faceToDir(-3.02)


def groupMatchApplyCheck():
    p = BigWorld.player()
    if p.groupMatchStatus == gametypes.GROUP_MATCH_STATUS_MATCHING and gameglobal.rds.ui.pushMessage.hasMsgType(uiConst.MESSAGE_TYPE_GROUP_MATCHED) and gameglobal.rds.ui.teamComm.groupMatchMed is None:
        gameglobal.rds.ui.teamComm.groupMatchMini = False
        gameglobal.rds.ui.teamComm.showGroupMatch()
        return False
    elif p.groupMatchStatus != gametypes.GROUP_MATCH_STATUS_DEFAULT:
        p.showGameMsg(GMDD.data.GROUP_OP_FAILED_WITH_GROUP_MATCH, ())
        return False
    else:
        return True


def checkIsCanGroupMatch(isEnableGroupMatch):
    if not isEnableGroupMatch:
        return False
    return True


def checkFbGroupMatchCondition(fbNo):
    fbData = FD.data.get(fbNo, {})
    p = BigWorld.player()
    if p.lv > fbData['lvMax'] or p.lv < fbData['lvMin']:
        return False
    return True


def getFbGroupName(fbGroupNo):
    if not GMTD.data.has_key(fbGroupNo):
        return ''
    fbNo = GMTD.data[fbGroupNo].values()[0].values()[0]['fbNo']
    return FD.data[fbNo]['name']


def genGroupMatchSecondMode(secondLevelMode):
    if secondLevelMode == 0:
        return const.GROUP_MATCH_FB_SECOND_LEVEL_MODE_ALL
    return 1 << secondLevelMode


def calcGroupMatchId(itemId):
    if utils.isGroupMatchLvLimitAct(itemId):
        groupMatchLvs = ABD.data.get(itemId, {}).get('groupMatchLvs', ())
        p = BigWorld.player()
        index = -1
        for i, val in enumerate(groupMatchLvs):
            minLv, maxLv = val
            if p.lv >= minLv and p.lv <= maxLv:
                index = i
                break

        if index == -1:
            return itemId
        else:
            return itemId * 10 + index % 10
    else:
        return itemId


def getGroupMatchDesc():
    p = BigWorld.player()
    if not hasattr(p, 'groupMatchClass'):
        return
    desc = ''
    if p.groupMatchClass == gametypes.GROUP_MATCH_CLASS_ACT:
        actNo = p.groupMatchExtra['actNo']
        if utils.isGroupMatchLvLimitAct(actNo / 10):
            actNo = actNo / 10
        desc = ABD.data[actNo]['name']
    elif p.groupMatchClass == gametypes.GROUP_MATCH_CLASS_FB:
        if p.groupMatchExtra['secondLevelMode'] != const.GROUP_MATCH_FB_SECOND_LEVEL_MODE_ALL:
            try:
                thirdKey = int(math.log(p.groupMatchExtra['secondLevelMode'], 2))
                gamelog.debug('@hjx social#getGroupMatchDesc:', thirdKey)
            except:
                thirdKey = const.GROUP_MATCH_FB_SECOND_LEVEL_MODE_ALL
                gamelog.error('@hjx error getGroupMatchDesc:', p.groupMatchExtra['secondLevelMode'])

        else:
            thirdKey = const.GROUP_MATCH_FB_SECOND_LEVEL_MODE_ALL
        desc = getFbGroupMatchDesc(p.groupMatchExtra['fbMode'], p.groupMatchExtra['firstLevelMode'], thirdKey)
    return desc


def getFbGroupMatchDesc(firstKey, secondKey, thirdKey):
    try:
        desc = ''
        if secondKey == 0:
            treeData = GMTD.data[firstKey]
            fbNo = treeData.values()[0].values()[0].values()[0]
            fbData = FD.data[fbNo]
            desc = desc + fbData['name'] + '-' + gameStrings.TEXT_ACTIVITYFACTORY_107
            return desc
        treeData = GMTD.data[firstKey][secondKey]
        fbNo = treeData.values()[0].values()[0]
        fbData = FD.data[fbNo]
        desc = desc + fbData['name'] + '-' + fbData['primaryLevelName'] + '-'
        if thirdKey == const.GROUP_MATCH_FB_SECOND_LEVEL_MODE_ALL:
            desc = desc + gameStrings.TEXT_ACTIVITYFACTORY_107
        else:
            fbNo = treeData[thirdKey].values()[0]
            fbData = FD.data[fbNo]
            desc = desc + fbData['modeName']
        return desc
    except:
        return ''


def getFbGroupDesc(firstKey, secondKey, thirdKey):
    try:
        desc = ''
        if secondKey == 0:
            treeData = GFMD.data[firstKey]
            fbNo = treeData.values()[0].values()[0].values()[0]
            fbData = FD.data[fbNo]
            desc = desc + fbData['name'] + '-' + gameStrings.TEXT_ACTIVITYFACTORY_107
            return desc
        treeData = GFMD.data[firstKey][secondKey]
        fbNo = treeData.values()[0].values()[0]
        fbData = FD.data[fbNo]
        desc = desc + fbData['name'] + '-' + fbData['primaryLevelName'] + '-'
        if thirdKey == const.GROUP_MATCH_FB_SECOND_LEVEL_MODE_ALL:
            desc = desc + gameStrings.TEXT_ACTIVITYFACTORY_107
        else:
            fbNo = treeData[thirdKey].values()[0]
            fbData = FD.data[fbNo]
            desc = desc + fbData['modeName']
        return desc
    except:
        return ''


def getCurLifeSkill(lifeSkillId):
    p = BigWorld.player()
    if hasattr(p, 'lifeSkill') and p.lifeSkill.has_key(lifeSkillId):
        return (lifeSkillId, p.lifeSkill[lifeSkillId]['level'])
    else:
        return (None, None)


def getLifeSkillEquipAdd(subType):
    p = BigWorld.player()
    equipIds = utils.getLifeSkillEquipIdsBySubType(p, subType)
    addLv = utils.calcLifeSkillEquipLvUps(equipIds)
    return addLv


def whereLifeEquip(itemId):
    p = BigWorld.player()
    for key, val in p.lifeEquipment.iteritems():
        if val and val.id == itemId:
            return (key[0], key[1], False)

    for i in xrange(3):
        if p.fishingEquip[i] and p.fishingEquip[i].id == itemId:
            return (gametypes.LIFE_SKILL_TYPE_FISHING, i, True)

    if p.exploreEquip[0] and p.exploreEquip[0].id == itemId:
        return (gametypes.LIFE_SKILL_TYPE_EXPLORE, 0, True)
    else:
        return (None, None, False)


def lifeSkillType2PanelType(lType):
    return lType + 1


def setClanWarArmorMode(force = False):
    p = BigWorld.player()
    if p.inWingCity():
        gameglobal.WING_WORLD_ARMER_SETTING = p.operation['commonSetting'][17]
    for en in BigWorld.entities.values():
        if en.IsSummonedSprite:
            en.refreshOpacityState()
            continue
        if not en.IsAvatar:
            continue
        if en.modelServer.isReady() and getattr(en, 'firstFetchFinished', False):
            en.modelServer.bodyPartsUpdate(False, True)
        elif force and en.isRealModel:
            en.modelServer.bodyUpdate()
        en.modelServer.horseUpdate()
        en.modelServer.wingFlyModelUpdate()
        en.modelServer.weaponUpdate()
        if en.isShowClanWar():
            en.modelServer.showOtherwears(False)
        else:
            en.modelServer.showOtherwears(True)
        en.modelServer.refreshYuanLing(en.isShowYuanLing())

    gameglobal.rds.avatarModelCnt = appSetting.VideoQualitySettingObj.getAvatarCntWithVQ() * gameglobal.MODEL_IN_WARARMOR_RATE


def setClanWarArmorSelfMode(disable):
    p = BigWorld.player()
    if disable:
        p.operation['commonSetting'][18] = 0
    else:
        p.operation['commonSetting'][18] = 1
    if not p.operation['commonSetting'][17]:
        return
    if p.modelServer.isReady():
        p.modelServer.bodyPartsUpdate(False, True)
    p.modelServer.horseUpdate()
    p.modelServer.wingFlyModelUpdate()
    if p.isShowClanWar():
        p.modelServer.showOtherwears(False)
    else:
        p.modelServer.showOtherwears(True)


def enabledClanWarArmorMode():
    p = BigWorld.player()
    p.operation['commonSetting'][17] = 1
    gameglobal.rds.ui.fangkadian.setArmorBtnSelect(True)
    setClanWarArmorMode(True)


def genGuildFlag(val, color):
    if type(val) != type(''):
        val = str(val)
    if type(color) != type(''):
        color = str(color)
    return val + const.SYMBOL_GUILD_FLAG_SPLIT + color


def getGuildFlag(flag):
    if not utils.isOldGuildFlag(flag):
        gcdData = GCD.data
        index, colorIndex = flag.split(const.SYMBOL_GUILD_FLAG_SPLIT)
        if isDownloadImage(index):
            icon = index
            color = ''
        else:
            zhanQiHuiJiPic = gcdData.get('zhanQiHuiJiPic', ())
            try:
                index = int(index) if index != '' else 0
            except:
                index = 0

            if index < len(zhanQiHuiJiPic):
                icon = zhanQiHuiJiPic[index]
            else:
                icon = 0
            zhanQiHuiJiColor = gcdData.get('zhanQiHuiJiColor', ())
            colorIndex = int(colorIndex)
            if len(zhanQiHuiJiColor) > colorIndex:
                color = str(gcdData.get('zhanQiHuiJiColor', ())[colorIndex][4])
        return (icon, color)
    else:
        return getGuildFlag_old(flag)


def getGuildFlag_old(flag):
    try:
        flag = int(flag)
    except:
        return (0, uiConst.ZHAN_QI_HUIJI_DEFAULT_COLOR)

    index = flag / gametypes.ZHAN_QI_MORPHER_HUIJI_TIMES
    icon = index
    gcdData = GCD.data
    color = ''
    if index < uiConst.ZHAN_QI_HUIJI_PIC_LIMIT:
        zhanQiHuiJiPic = gcdData.get('zhanQiHuiJiPic', ())
        if index < len(zhanQiHuiJiPic):
            icon = zhanQiHuiJiPic[index]
        else:
            icon = 0
        zhanQiHuiJiColor = gcdData.get('zhanQiHuiJiColor', ())
        colorIndex = flag % gametypes.ZHAN_QI_MORPHER_HUIJI_TIMES
        if len(zhanQiHuiJiColor) > colorIndex:
            color = str(gcdData.get('zhanQiHuiJiColor', ())[colorIndex][4])
    return (icon, color)


def getGuildIconPath(key):
    if isDownloadImage(key):
        return '../' + const.IMAGES_DOWNLOAD_DIR + '/' + key + '.dds'
    else:
        return uiConst.GUILD_FLAG_ICON_IMAGE_RES + str(key) + '.dds'


def calTextureVal(val):
    if type(val) != int:
        val = 0
    if val < uiConst.ZHAN_QI_HUIJI_PIC_LIMIT:
        return val + 1
    else:
        return val


def isDownloadImage(val):
    if type(val) == str and val.startswith(const.IMAGES_DOWNLOAD_PREFIX):
        return True
    return False


def isZhanQiShowImage(val):
    if type(val) == str and val.startswith(const.IMAGES_SHOW_PREFIX):
        return True
    return False


def onFullExpTrigger(owner):
    upExp = ALD.data.get(owner.lv, {}).get('upExp', 0)
    if not upExp:
        gamelog.error('@hjx onFullExpTrigger error, lv%d' % owner.lv)
        return
    if owner.exp >= upExp:
        gameglobal.rds.tutorial.onFullExp(owner.lv)


def getLocationByGbId(gbId):
    p = BigWorld.player()
    defalultName = gameStrings.TEXT_UIUTILS_1406
    chunkName = ''
    spaceNo = 0
    if p.gbId == gbId:
        spaceNo = p.spaceNo
        chunkName = BigWorld.ChunkInfoAt(p.position)
    else:
        if hasattr(p, 'members') and not p.members.get(gbId, {}).get('isOn', True):
            return gameStrings.TEXT_UIUTILS_1414
        if not hasattr(p, 'membersPos'):
            return defalultName
        if not p.membersPos.has_key(gbId):
            return defalultName
        spaceNo = p.membersPos[gbId][0]
        chunkName = p.membersPos[gbId][3]
    mapName = gameStrings.TEXT_UIUTILS_1424 % formula.whatLocationName(spaceNo, chunkName, includeMLInfo=True)
    return mapName


def copyToImagePath(path):
    BigWorld.copyToGamePath(path, const.IMAGES_DOWNLOAD_RELATIVE_DIR)


def getChunkName(xpos, zpos):
    return PCD.data.get((int(int(xpos) / 100), int(int(zpos) / 100)), {}).get('name', '')


def getChunkNameBySeekId(seekId):
    if not SD.data.has_key(seekId):
        return ''
    sData = SD.data[seekId]
    spaceNo = sData.get('spaceNo')
    if spaceNo != const.SPACE_NO_BIG_WORLD:
        return MCD.data.get(spaceNo, {}).get('name', '')
    xPos = sData['xpos']
    zPos = sData['zpos']
    chunkName = getChunkName(xPos, zPos)
    if not CMD.data.has_key(chunkName):
        return ''
    else:
        return CMD.data[chunkName]['chunkNameZhongwen']


NO_PARAM = 0
SKILL_EFFECT_PARAM = 1
STATE_ID_PARAM = 2
PSKILL_PARAM = 3

def calTipVal(formulaName, formulaArgs, skLv):
    p = BigWorld.player()
    data = STD.data.get(formulaName, {})
    formulaStr = data.get('formula', ())
    params = data.get('param', ())
    inputType = data.get('input', 0)
    for i, param in enumerate(params):
        if type(param) == str:
            if param == 'extraDmgRefId':
                if inputType == NO_PARAM:
                    propId = 0
                elif inputType == SKILL_EFFECT_PARAM:
                    propId = SED.data.get(formulaArgs, {}).get('extraDmgRefId')
                elif inputType == STATE_ID_PARAM:
                    propId = STAD.data.get(formulaArgs, {}).get('extraDmgRefId')
                elif inputType == PSKILL_PARAM:
                    propId = PD.data.get(formulaArgs, {}).get('extraDmgRefId')
                if type(propId) in (tuple, list):
                    propId = propId[0]
                val = commcalc.getAvatarPropValueByIdEx(p, propId) if propId else 0
            else:
                if inputType == NO_PARAM:
                    val = 0
                elif inputType == SKILL_EFFECT_PARAM:
                    val = SED.data.get(formulaArgs, {}).get(param)
                elif inputType == STATE_ID_PARAM:
                    val = STAD.data.get(formulaArgs, {}).get(param)
                elif inputType == PSKILL_PARAM:
                    val = PD.data.get(formulaArgs, {}).get(param)
                val = val[skLv - 1] if val and type(val) in (tuple, list) and skLv - 1 < len(val) else 0
        else:
            val = commcalc.getAvatarPropValueById(p, param) if param else 0
        formulaStr = formulaStr.replace('p' + str(i + 1).zfill(2), str(val))

    try:
        res = eval(formulaStr)
    except:
        res = 0

    return int(res)


def regularExpDesc(desc, expression, skLv):
    m = re.search(expression, desc)
    while m:
        param = m.group(0)
        formulaName, formulaArgs = param.split('.')
        val = calTipVal(formulaName, int(formulaArgs), skLv)
        desc = re.sub(expression, str(val), desc, 1)
        m = re.search(expression, desc)

    return desc


def calSkillTipValue(desc, skLv):
    keys = STD.data.keys()
    for key in keys:
        expression = key + '\\.[0-9]+'
        desc = regularExpDesc(desc, expression, skLv)

    return desc


def getEntDist(ent):
    if not ent:
        return -1
    p = BigWorld.player()
    try:
        ret = int((ent.position - p.position).length)
    except:
        ret = -1

    return ret


def canCastSkill(ent):
    if ent is None:
        return False
    elif getEntDist(ent) <= uiConst.CAST_KILL_MAX_DIS:
        return True
    else:
        return False


def getIcon(type, id):
    if type == uiConst.ICON_TYPE_ITEM:
        return 'item/icon/%d.dds' % id
    elif type == uiConst.ICON_TYPE_EMOTE:
        return 'emote/%d.dds' % id
    elif type == uiConst.ICON_TYPE_LIFE_SKILL:
        return 'lifeSkill/icon40/%d.dds' % id
    else:
        return None


def getLevelDesc(adjustPrice, curPrice):
    if adjustPrice == curPrice:
        return 'normal'
    elif adjustPrice < curPrice:
        return 'up'
    else:
        return 'down'


def getFKeyPathDesc(idx):
    data = FKD.data.get(idx, {})
    type = data.get('fKeyIconType', 0)
    id = data.get('fKeyIcon', 0)
    desc = data.get('fKeyDesc', gameStrings.TEXT_UIUTILS_1565)
    return (getIcon(type, id), desc)


def getParentId(itemId):
    if ID.data.get(itemId, {}).has_key('parentId'):
        return ID.data[itemId]['parentId']
    return itemId


def getItemCountInInvAndMaterialAndHierogramBag(entityId, itemId):
    p = BigWorld.entities.get(entityId, None)
    if not p:
        return 0
    else:
        parentId = getParentId(itemId)
        myItemNumInv = p.inv.countItemInPages(parentId, enableParentCheck=True)
        myItemNumMaterial = p.materialBag.getBagItemCount(parentId, enableParentCheck=True)
        myItemNumHierogram = p.hierogramBag.getBagItemCount(parentId, enableParentCheck=True)
        return myItemNumInv + myItemNumMaterial + myItemNumHierogram


def dealNpcSpeakEvents(data, entId, needInterrupt = True):
    npc = BigWorld.entity(entId)
    if not npc:
        return
    else:
        if data:
            for info in data:
                if info[0] == gameglobal.ACT_FLAG:
                    acts = [ str(i) for i in info[1:] ]
                    npc.fashion.playActionSequence(npc.model, acts, None)
                elif info[0] == gameglobal.VOICE_FLAG:
                    gameglobal.rds.sound.playSound(int(info[1]), interrupt=needInterrupt)

        return


def checkTopIconValid(type):
    if type == 'WorkBoard':
        if BigWorld.player().lv < SCD.data.get('openJobBoardLv', 0):
            return False
    return True


def replaceWhiteSpace(str):
    return unicode2gbk(re.sub(gbk2unicode(gameStrings.TEXT_UIUTILS_1606), gbk2unicode('  '), gbk2unicode(str)))


def setAvatarPhysics(flag, init = False, forceChagne = False):
    p = BigWorld.player()
    if p.getOperationMode() == flag and not forceChagne:
        return
    else:
        if appSetting.GameSettingObj.switchAvatarPhysics(flag):
            if hasattr(p, 'ap'):
                p.ap.reset()
            p.applyModeOperation(flag)
            p.setSavedOperationMode(flag)
            if init and flag == gameglobal.ACTION_MODE:
                p.operation['commonSetting'][2] = 0
                p.operation['commonSetting'][3] = 0
                p.operation['commonSetting'][15] = 0
            p.sendOperation()
            if flag != gameglobal.ACTION_MODE:
                BigWorld.player().optionalTargetLocked = None
        return


def checkBindCashEnough(cost, bindCash, cash, yesCallback, isModal = False):
    if bindCash < cost:
        gameglobal.rds.ui.moneyConvertConfirm.show(yesCallback, isModal)
        return False
    return True


def getIdByRoleName(roleName):
    p = BigWorld.player()
    if not p.members:
        return None
    else:
        for val in p.members.values():
            if val['roleName'] == roleName:
                return val['id']

        return None


def getXingJiWordIdx(xingJi):
    intTime = int(xingJi)
    idx = (intTime + 1) / 2
    return idx


def convertToXingJiWord(idx):
    if idx >= len(XING_JI_TIME_WORD):
        return ''
    return XING_JI_TIME_WORD[idx]


def setApState(flag):
    p = BigWorld.player()
    if flag:
        if hasattr(p, 'getOperationMode') and p.getOperationMode() == gameglobal.ACTION_MODE:
            p.ap.restore()
    elif hasattr(p, 'getOperationMode') and p.getOperationMode() == gameglobal.ACTION_MODE:
        p.ap.reset()


def buildJuexingContentList(item):
    contentList = []
    if not item:
        return contentList
    elif not hasattr(item, 'equipType') or not hasattr(item, 'equipSType') or not hasattr(item, 'enhanceType'):
        return contentList
    elif not item.isItemCanRebuild():
        return contentList
    else:
        juexingDataList = getattr(item, 'enhJuexingData', {})
        if not juexingDataList:
            return contentList
        if gameglobal.rds.configData.get('enableEquipChangeJuexingStrength', False):
            juexingAddRatio = getattr(item, 'enhJuexingAddRatio', {})
        else:
            juexingAddRatio = None
        customPropColor = getattr(item, 'customPropColor', {})
        if not isinstance(customPropColor, dict):
            customPropColor = {}
        sortedKeys = juexingDataList.keys()
        sortedKeys.sort()
        for key in sortedKeys:
            juexingDataListOnLv = juexingDataList[key]
            basicProp = ''
            propDataList = []
            propDataReasonList = []
            dataForEj = utils.getEquipEnhJuexingPropData(item.equipType, item.equipSType, key, item.enhanceType)
            juexingLv = 0
            if juexingDataListOnLv:
                juexingLv = utils.getJuexingDataStep(item, key, juexingDataListOnLv[0], utils.getEquipEnhJuexingPyData())
            for juexingData in juexingDataListOnLv:
                reason = ''
                if juexingData:
                    info = PRD.data[juexingData[0]]
                    isGray = False
                    if juexingData[0] not in dataForEj or key > item.getMaxEnhLv(BigWorld.player()) or key > getattr(item, 'enhLv', 1):
                        isGray = True
                        if key > getattr(item, 'enhLv', 1):
                            reason = gameStrings.TEXT_UIUTILS_1713
                        if juexingData[0] not in dataForEj:
                            reason = gameStrings.TEXT_UIUTILS_1715
                        if key > item.getMaxEnhLv(BigWorld.player()):
                            reason = gameStrings.TEXT_UIUTILS_1717
                    jueXingNum = juexingData[2]
                    if juexingAddRatio and key in juexingAddRatio:
                        addRatio = juexingAddRatio[key]
                    else:
                        addRatio = 0
                    if juexingData[0] in itemToolTipUtils.PROPS_SHOW_SHRINK:
                        jueXingNum = round(juexingData[2] / 100.0, 1)
                    if isGray == True:
                        if basicProp == '':
                            basicProp += toHtml(info['name'] + '  ', '#808080')
                        else:
                            basicProp += toHtml('  ' + info['name'] + '  ', '#808080')
                        if info['showType'] == 0:
                            basicProp += toHtml(str(itemToolTipUtils.float2Int(jueXingNum)), '#808080')
                        elif info['showType'] == 2:
                            basicProp += toHtml(str(round(jueXingNum, 1)), '#808080')
                        else:
                            basicProp += toHtml(str(round(jueXingNum * 100, 1)) + '%', '#808080')
                    else:
                        basicStr = ''
                        if basicProp == '':
                            basicStr += info['name'] + '  '
                        else:
                            basicStr += '  ' + info['name'] + '  '
                        if info['showType'] == 0:
                            basicStr += str(itemToolTipUtils.float2Int(jueXingNum))
                        elif info['showType'] == 2:
                            basicStr += str(round(jueXingNum, 1))
                        else:
                            basicStr += str(round(jueXingNum * 100, 1)) + '%'
                        if key in customPropColor.get('baseProp', {}):
                            basicProp += toHtml(basicStr, customPropColor['baseProp'][key])
                        else:
                            basicProp += basicStr
                    if addRatio > 0:
                        if key in customPropColor.get('ratioProp', {}):
                            ratioStr = toHtml(' (+%i%%)' % int(addRatio * 100), customPropColor['ratioProp'][key])
                        else:
                            ratioStr = toHtml(' (+%i%%)' % int(addRatio * 100), itemToolTipUtils.getJuexingStrengthColor(addRatio)) if not isGray else ' (+%i%%)' % int(addRatio * 100)
                        basicProp += ratioStr
                    propDataList.append(isGray)
                    propDataReasonList.append(reason)

            if basicProp != '':
                contentList.append([key,
                 basicProp,
                 propDataList,
                 juexingLv,
                 propDataReasonList])

        return contentList


def toHtml(txt, color = None, linkEventTxt = None, fontSize = None, underLine = True):
    msg = txt
    if color:
        if not fontSize:
            msg = "<font color = \'%s\'>%s</font>" % (color, msg)
        else:
            msg = "<font color = \'%s\' size = \'%d\'>%s</font>" % (color, fontSize, msg)
    if linkEventTxt:
        msg = "<a href=\'event:%s\'>%s</a>" % (linkEventTxt, msg)
        if underLine:
            msg = '<u>%s</u>' % msg
    return msg


def getRoleNameWithSeverName(roleName, hostId, ignoreSameServer = True):
    if not hostId:
        return roleName
    if ignoreSameServer:
        mHostId = utils.getHostId()
        if mHostId == int(hostId):
            return roleName
    serverName = utils.getServerName(hostId)
    return gameStrings.ROLENAME_WITH_SERVERNAME_TXT % (roleName, serverName)


def toMenuName(roleName, gbId = 0, menuId = 1, underLine = False, hostId = 0):
    if not hostId:
        hostId = utils.getHostId()
    nameTxt = "<a href=\'event:menuName:%s,%s,%s,%s\'>%s</a>" % (roleName,
     gbId,
     menuId,
     hostId,
     roleName)
    if underLine:
        nameTxt = '<u>%s</u>' % nameTxt
    return nameTxt


def getTextFromGMD(gameMsgID, default = ''):
    return GMD.data.get(gameMsgID, {}).get('text', default)


def formatTime(sec):
    timeText = ''
    if sec >= 86400:
        timeText += gameStrings.TEXT_FASHIONPROPTRANSFERPROXY_229 % (sec / 86400)
        sec %= 86400
    if sec >= 3600:
        timeText += gameStrings.TEXT_GUILDWWTOURNAMENTRESULTPROXY_116 % (sec / 3600)
        sec %= 3600
    if sec >= 60:
        timeText += gameStrings.TEXT_UIUTILS_1818 % (sec / 60)
        sec %= 60
    timeText += gameStrings.TEXT_UIUTILS_1821 % sec
    return timeText


def formatTimeShort(sec):
    timeText = ''
    if sec >= 86400:
        timeText += gameStrings.TEXT_FASHIONPROPTRANSFERPROXY_229 % (sec / 86400)
        sec %= 86400
        return timeText
    if sec >= 3600:
        timeText += gameStrings.TEXT_GUILDWWTOURNAMENTRESULTPROXY_116 % (sec / 3600)
        sec %= 3600
        return timeText
    if sec >= 60:
        timeText += gameStrings.TEXT_UIUTILS_1818 % (sec / 60)
        sec %= 60
        return timeText
    timeText += gameStrings.TEXT_UIUTILS_1821 % sec
    return timeText


def convertNumStr(own, need, showOwnStr = True, needThousand = False, enoughColor = '#FFFFE7', notEnoughColor = '#CC2929'):
    if needThousand:
        ownStr = format(own, ',')
        needStr = format(need, ',')
    else:
        ownStr = str(own)
        needStr = str(need)
    if showOwnStr:
        numStr = '%s/%s' % (ownStr, needStr)
    else:
        numStr = '%s' % needStr
    if own >= need:
        if enoughColor:
            numStr = toHtml(numStr, enoughColor)
        else:
            return numStr
    else:
        numStr = toHtml(numStr, notEnoughColor)
    return numStr


def getItemIconPath(itemId, picSize = uiConst.ICON_SIZE64):
    iconPath = getItemIconFile64(itemId)
    if picSize == uiConst.ICON_SIZE40:
        iconPath = getItemIconFile40(itemId)
    elif picSize == uiConst.ICON_SIZE110:
        iconPath = getItemIconFile110(itemId)
    else:
        iconPath = getItemIconFile64(itemId)
    return iconPath


def getGfxItemById(itemId, count = 1, picSize = uiConst.ICON_SIZE64, appendInfo = None, overPicSize = uiConst.ICON_SIZE64, srcType = '', stateFlag = False):
    data = {}
    data['id'] = itemId
    data['itemId'] = itemId
    data['iconPath'] = getItemIconPath(itemId, picSize)
    data['overIconPath'] = getItemIconPath(itemId, overPicSize)
    data['count'] = count
    quality = getItemQuality(itemId)
    color = getColorByQuality(quality)
    data['color'] = color
    data['pinXing'] = getPinXing(itemId)
    if srcType != '':
        data['srcType'] = srcType
    if stateFlag:
        data['state'] = getItemStateById(itemId)
    if appendInfo:
        data.update(appendInfo)
    return data


def getGfxItem(item, picSize = uiConst.ICON_SIZE64, appendInfo = None, location = None, overPicSize = uiConst.ICON_SIZE64):
    data = {}
    data['id'] = item.id
    data['iconPath'] = getItemIconPath(item.id, picSize)
    data['overIconPath'] = getItemIconPath(item.id, overPicSize)
    data['count'] = item.cwrap
    if hasattr(item, 'quality'):
        quality = item.quality
    else:
        quality = getItemQuality(item.id)
    color = getColorByQuality(quality)
    data['color'] = color
    data['pinXing'] = getPinXing(item.id)
    data['cornerMark'] = itemToolTipUtils.getCornerMark(item)
    if appendInfo:
        data.update(appendInfo)
    if location != None:
        data['uuid'] = item.uuid.encode('hex')
        data['location'] = location
    data['specialPropLen'] = item.getSpecialPropLevel()
    return data


def getItemStateById(itemId):
    p = BigWorld.player()
    item = Item(itemId)
    if not item.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p):
        return uiConst.EQUIP_NOT_USE
    else:
        return uiConst.ITEM_NORMAL


def getSkillIconFile40(skillInfo):
    name = skillInfo.getSkillData('icon', 'notFound')
    return uiConst.SKILL_ICON_IMAGE_RES_40 + str(name) + '.dds'


def getSkillIconFile64(skillInfo):
    name = skillInfo.getSkillData('icon', 'notFound')
    return uiConst.SKILL_ICON_IMAGE_RES_64 + str(name) + '.dds'


def getSkillIconPath(skillInfo, picSize = uiConst.ICON_SIZE40):
    iconPath = getSkillIconFile40(skillInfo)
    if picSize == uiConst.ICON_SIZE64:
        iconPath = getSkillIconFile64(skillInfo)
    return iconPath


def getGfxSkill(skillInfo, picSize = uiConst.ICON_SIZE40, appendInfo = None):
    data = {}
    data['id'] = skillInfo.num
    data['iconPath'] = getSkillIconPath(skillInfo, picSize)
    data['overIconPath'] = getSkillIconPath(skillInfo, picSize)
    return data


def getTempSkill(skillId, iconPath):
    data = {}
    data['id'] = skillId
    path = uiConst.TEMP_SKILL_ICON_IMAGE + str(iconPath) + '.dds'
    data['iconPath'] = path
    data['overIconPath'] = path
    return data


def recoverArrange(arrangeDict):
    arrange = [ 0 for x in range(const.GROUP_MAX_NUMBER) ]
    for mGbId, index in arrangeDict.iteritems():
        arrange[index] = mGbId

    return arrange


def getItemIconFile40(itemId):
    name = ID.data.get(itemId, {}).get('icon', 'notFound')
    return uiConst.ITEM_ICON_IMAGE_RES_40 + str(name) + '.dds'


def getItemIconFile64(itemId):
    name = ID.data.get(itemId, {}).get('icon', 'notFound')
    return uiConst.ITEM_ICON_IMAGE_RES_64 + str(name) + '.dds'


def getItemIconFile110(itemId):
    name = ID.data.get(itemId, {}).get('icon', 'notFound')
    return uiConst.ITEM_ICON_IMAGE_RES_110 + str(name) + '.dds'


def getItemIconFile150(itemId):
    name = ID.data.get(itemId, {}).get('icon', 'notFound')
    return uiConst.ITEM_ICON_IMAGE_RES_150 + str(name) + '.dds'


def getItemMaxNumById(itemId):
    maxNum = ID.data.get(itemId, {}).get('mwrap', 999)
    return maxNum


def getItemDataByItemId(itemId):
    iconPath = getItemIconFile64(itemId)
    quality = getItemQuality(itemId)
    color = getColorByQuality(quality)
    return (iconPath, color)


def getConstellation(month, day):
    d = ((1, 20),
     (2, 19),
     (3, 21),
     (4, 20),
     (5, 21),
     (6, 22),
     (7, 23),
     (8, 23),
     (9, 23),
     (10, 24),
     (11, 23),
     (12, 22))
    return uiConst.CONSTELLATIONS[len(filter(lambda y: y <= (month, day), d)) % 12]


def checkEnhlvCanJuexing(enhlv):
    return enhlv in EJRD.data.keys()


def getEnhlvJuexingRefiningLimit(enhlv):
    return EERD.data.get(enhlv, {}).get('needRefiningLv', 0)


def isEnhlvRefiningShowLock(enhlv):
    return getEnhlvJuexingRefiningLimit(enhlv) > 0


def hasJuexingNew(enhlv):
    return EERD.data.get(enhlv, {}).get('newJuexingNew', 0) != 0


def isItemHasJuexingNew(item):
    if not item or not hasattr(item, 'enhanceRefining'):
        return False
    if item.enhanceRefining:
        for lv in item.enhanceRefining.iterkeys():
            if hasJuexingNew(lv):
                return True

    return False


def isItemHasTempJuexingNewGoldProp(item):
    if not isItemHasJuexingNew(item):
        return False
    if not hasattr(item, 'enhJuexingData') or not hasattr(item, 'tempJXStrength'):
        return False
    newItem = copy.deepcopy(item)
    newItem.enhJuexingData = newItem.tempJXStrength
    content = buildJuexingContentList(newItem)
    for value in content:
        if hasJuexingNew(value[0]) and value[3] >= 3:
            return True
    else:
        if not hasattr(item, 'tempJXAddRatio'):
            return False
        allcolors = SCD.data.get('juexingStrengthColor', {})
        if len(allcolors) < 2:
            return False
        goldLimit = sorted(allcolors.keys())[-2]
        for ratio in item.tempJXAddRatio.itervalues():
            if int(ratio * 100) > goldLimit:
                return True

    return False


def getEquipTotalRefining(item):
    if not item or not hasattr(item, 'enhanceRefining'):
        return 0
    lvRange = SCD.data.get('refiningLimitLvRange', (1, 16))
    refiningSum = 0.0
    try:
        for i in xrange(lvRange[0], lvRange[1] + 1):
            refiningSum += item.enhanceRefining.get(i, 0)

    except:
        gamelog.error('refining config error!')
        return 0

    return int(refiningSum * 100)


def checkEquipRefiningLimitLv(totalLv, needRefining):
    return totalLv >= needRefining


def getEquipSortIdxByPart(item):
    if not item:
        return 0
    we = item.whereEquip()
    if we and we[0] in gametypes.EQU_PART_TO_SORT_IDX:
        return gametypes.EQU_PART_TO_SORT_IDX[we[0]]
    return 0


def getEquipTotalRefine(item):
    maxEnhlv = item.getMaxEnhLv(BigWorld.player())
    enhanceRefining = getattr(item, 'enhanceRefining', {})
    totalNum = 0
    lostNum = 0
    for key in enhanceRefining:
        totalNum += int(enhanceRefining[key] * 100)
        if key > maxEnhlv:
            lostNum += int(enhanceRefining[key] * 100)

    _, _, enh, _, _ = itemToolTipUtils.calAttrVal(item)
    contentDict = {}
    for enhItem in enh:
        contentDict[enhItem[0]] = enhItem

    title = ''
    content = ''
    for key, value in contentDict.iteritems():
        if key == itemToolTipUtils.PHYSICAL_ATTACK_DOWN and contentDict.has_key(itemToolTipUtils.PHYSICAL_ATTACK_UP):
            if value[5] > 0:
                down = contentDict[itemToolTipUtils.PHYSICAL_ATTACK_DOWN][2] - contentDict[itemToolTipUtils.PHYSICAL_ATTACK_DOWN][5]
                up = contentDict[itemToolTipUtils.PHYSICAL_ATTACK_UP][2] - contentDict[itemToolTipUtils.PHYSICAL_ATTACK_UP][5]
            else:
                down = contentDict[itemToolTipUtils.PHYSICAL_ATTACK_DOWN][2]
                up = contentDict[itemToolTipUtils.PHYSICAL_ATTACK_UP][2]
            content = '%d-%d' % (down, up)
            title = gameStrings.TEXT_EQUIPENHANCERESULTPROXY_157
        elif key == itemToolTipUtils.SPELL_ATTACK_DOWN and contentDict.has_key(itemToolTipUtils.SPELL_ATTACK_UP):
            if value[5] > 0:
                down = contentDict[itemToolTipUtils.SPELL_ATTACK_DOWN][2] - contentDict[itemToolTipUtils.SPELL_ATTACK_DOWN][5]
                up = contentDict[itemToolTipUtils.SPELL_ATTACK_UP][2] - contentDict[itemToolTipUtils.SPELL_ATTACK_UP][5]
            else:
                down = contentDict[itemToolTipUtils.SPELL_ATTACK_DOWN][2]
                up = contentDict[itemToolTipUtils.SPELL_ATTACK_UP][2]
            content = '%d-%d' % (down, up)
            title = gameStrings.TEXT_EQUIPCHANGESTARLVUPPROXY_324
        elif key not in itemToolTipUtils.ATTACK_PROP:
            prd = PRD.data.get(key, {})
            content = ''
            if prd.get('type', 0) == 2:
                content += '+'
            elif prd.get('type', 0) == 1:
                content += '-'
            content += formatProp(value[2], value[1], prd.get('showType', 0), value[5])
            title = prd.get('name', '')

    if title != '' and content != '':
        enhProp = title + ' ' + content
    else:
        enhProp = ''
    return (totalNum, lostNum, enhProp)


def getEquipStar(item):
    star = 0
    if getattr(item, 'enhLv', 0) > 0 and hasattr(item, 'enhanceRefining'):
        find = False
        sumRef = sum(item.enhanceRefining.values())
        prefectionDiv = EERD.data.get(item.enhLv, {}).get('prefectionDiv', ())
        for i in xrange(0, len(prefectionDiv)):
            if prefectionDiv[i] >= sumRef:
                star = i
                find = True
                break

        if find == False:
            star = 10
    return star


def getTimesProvider():
    t = []
    for x in xrange(24):
        for y in ('00', '30'):
            t.append('%s:%s' % (x, y))

    return t


def getCCHyperLink(roomIdStr, isTmp = True, style = 0, msg = None):
    color = FCD.data['cc', style]['color']
    if isTmp:
        event = 'rtcd' + roomIdStr
    else:
        event = 'rcd' + roomIdStr
    msg = "<font color=\'%s\'>[<a href = \'event:cclink%s\'><u>%s</u></a>]</font>" % (color, event, msg)
    return msg


def getCCRoom():
    titleName = gameglobal.rds.loginManager.titleName()
    roomId, channelId = SCD.data.get('CCHostRoom', {}).get(titleName, [1314, 0])
    return (roomId, channelId)


def getDefaultCCRoom():
    return SCD.data.get('CCDefaultRoom', (1314, 4006143))


def getArenaBadge(arenaScore):
    tmpASDD = ASDD.data.keys()
    for minS, maxS in tmpASDD:
        if arenaScore >= minS and arenaScore <= maxS:
            curFrame = ASDD.data[minS, maxS].get('frameName', 'orange1')
            return curFrame

    return 'orange1'


def isInFubenShishenLow():
    try:
        return gameglobal.rds.ui.currentShishenMode == gametypes.FB_SHISHEN_MODE_LOW
    except:
        return False


def genDuelCrossName(preName, fromHostName):
    if fromHostName == '':
        return preName
    else:
        return preName + '-' + fromHostName


def formatProp(propNum, pType, showType, delNum = 0):
    propStr = ''
    if pType == 1:
        propStr = str(round(propNum * 100, 1)) + '%'
    elif pType == 0:
        if showType == 0:
            if delNum > 0:
                propStr = str(int(propNum) - int(delNum))
            else:
                propStr = str(int(propNum))
        elif showType == 2:
            if delNum > 0:
                propStr = str(round(propNum, 1) - round(delNum, 1))
            else:
                propStr = str(round(propNum, 1))
        elif delNum > 0:
            propStr = str(round(propNum * 100, 1) - round(delNum * 100, 1)) + '%'
        else:
            propStr = str(round(propNum * 100, 1)) + '%'
    return propStr


def isMemoryLoaded():
    performInfo = BigWorld.getPerformanceInfo()
    commitedmem = float(performInfo.get('commitedmem', 0))
    phymem = float(performInfo.get('phymem', 0))
    if phymem == 0:
        return False
    elif commitedmem / phymem > 1.2:
        return True
    else:
        return False


def getItemPreName(item):
    preName = ''
    if hasattr(item, 'prefixInfo'):
        for prefixItem in EPPD.data.get(item.prefixInfo[0], []):
            if prefixItem['id'] == item.prefixInfo[1]:
                preName = prefixItem['name']
                break

    return preName


def getItemPreprops(i, starFactor = False):
    prefixProp = ''
    if hasattr(i, 'preprops'):
        if hasattr(i, 'starLv'):
            starLevel = i.starLv
        else:
            starLevel = 0
        if starFactor == False:
            starFactor = ESFCD.data.get(starLevel, {}).get('factor', 1.0)
        else:
            starFactor = 1
        quality = getattr(i, 'quality', 1)
        if not quality:
            quality = 1
        qualityFactor = EQFD.data.get(quality, {}).get('factor', 1.0)
        preprops = i.preprops
        preprops = [ tuple(list(pp) + [PRD.data.get(pp[0], {}).get('priorityLevel', ''), PRD.data.get(pp[0], {}).get('showColor', '')]) for pp in preprops ]
        preprops.sort(key=lambda k: k[3])
        for item in preprops:
            pType = item[1]
            info = PRD.data.get(item[0], {})
            if prefixProp != '':
                prefixProp += '<br>'
            prefixProp += info['name'] + ' '
            if info['type'] == 2:
                prefixProp += '+'
            elif info['type'] == 1:
                prefixProp += '-'
            prefixProp += formatProp(item[2] * starFactor * qualityFactor, pType, info.get('showType', 0))

    return prefixProp


def getQRCodeBuff(code, boxSize = 2):
    codeMaker = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=boxSize, border=1)
    codeMaker.add_data(code)
    codeMaker.make(fit=True)
    img = codeMaker.make_image()
    codeBuff = img.convert('RGB').tostring('jpeg', 'RGB', 90)
    buffer = base64.encodestring(codeBuff)
    return buffer


def getActivitySignId():
    signId = 0
    enableActivityAttend = gameglobal.rds.configData.get('enableActivityAttend', False)
    if not enableActivityAttend:
        return 0
    p = BigWorld.player()
    if not hasattr(p, 'newSignInInfo'):
        return 0
    for key in p.newSignInInfo.keys():
        data = ASTD.data.get(key)
        if data and data.get('activityType') == 1:
            continue
        if key != const.ACTIVITY_NEW_SERVER_ACHIEVE:
            signId = key
            break

    startDay = ASTD.data.get(signId, {}).get('startDay', 20150801)
    duration = ASTD.data.get(signId, {}).get('duration', 7)
    signInEndSec = _getSec(_getDay(startDay, duration)) - 2
    if int(utils.getNow()) > int(signInEndSec):
        return 0
    return signId


def getActivityScoreId():
    scoreId = 0
    enableActivityScore = gameglobal.rds.configData.get('enableActivityScore', False)
    if not enableActivityScore:
        return 0
    p = BigWorld.player()
    if not hasattr(p, 'currentWorkingAchieveScoreActivities'):
        return 0
    for key in p.currentWorkingAchieveScoreActivities:
        if key != const.ACTIVITY_NEW_SERVER_ACHIEVE:
            scoreId = key
            break

    startDay = AASCFD.data.get(scoreId, {}).get('startDay', 20150801)
    duration = AASCFD.data.get(scoreId, {}).get('duration', 7)
    scoreEndSec = _getSec(_getDay(startDay, duration)) - 2
    if int(utils.getNow()) > int(scoreEndSec):
        return 0
    return scoreId


def _getTodayDate():
    daySec = utils.getNow()
    date = time.strftime('%Y%m%d', time.localtime(daySec))
    return date


def needShowByServer(configId):
    if utils.getEnableCheckServerConfig() and not utils.checkInCorrectServer(configId):
        return False
    return True


def _getDay(startDay, index):
    toDaySec = _getSec(startDay) + index * uiConst.ONE_DAT_TIME
    date = time.strftime('%Y%m%d', time.localtime(toDaySec))
    return int(date)


def zonetime(timeStamp, zone, tformat = '%Y%m%d'):
    zls = {'0': 0,
     '-12': -12,
     '-11': -11,
     '-10': -10,
     '-9:30': -9.5,
     '-9': -9,
     '-8': -8,
     '-7': -7,
     '-6': -6,
     '-5': -5,
     '-4:30': -4.5,
     '-4': -4,
     '-3:30': -3.5,
     '-3': -3,
     '-2': -2,
     '-1': -1,
     '1': 1,
     '2': 2,
     '3': 3,
     '3:30': 3.5,
     '4': 4,
     '4:30': 4.5,
     '5': 5,
     '5:30': 5.5,
     '5:45': 5.75,
     '6': 6,
     '6:30': 6.5,
     '7': 7,
     '8': 8,
     '9': 9,
     '9:30': 9.5,
     '10': 10,
     '10:30': 10.5,
     '11': 11,
     '11:30': 11.5,
     '12': 12,
     '12:45': 12.75,
     '13': 13,
     '14': 14}
    t2 = time.localtime(time.mktime(time.gmtime(timeStamp)) + 3600 * zls[zone])
    return time.strftime(tformat, t2)


def _getSec(dayStr):
    dayStr = str(dayStr)
    tmlist = [0] * 9
    tmlist[0] = int(dayStr[:4])
    tmlist[1] = int(dayStr[4:6])
    tmlist[2] = int(dayStr[6:])
    timeSec = time.mktime(tmlist)
    return timeSec


def getShortStr(val, length = 0):
    if length <= 0 or len(val) <= length:
        return val
    try:
        tmpStr = unicode(val, utils.defaultEncoding())
        if len(tmpStr) > length:
            tmpName = tmpStr[0:length]
            result = tmpName.encode(utils.defaultEncoding()) + '...'
            return result
    except:
        pass

    return val


def checkStrOverLen(val, length = 0):
    if length <= 0 or not val or len(val) <= length:
        return False
    try:
        tmpStr = unicode(val, utils.defaultEncoding())
        if len(tmpStr) > length:
            return True
    except:
        pass

    return False


def hasVipBasic():
    p = BigWorld.player()
    return p.vipBasicPackage.get('packageID', 0) in gametypes.VIP_BASIC_PACKAGE_ID_SET and p.vipBasicPackage.get('tExpire', 0) > p.getServerTime()


def hasVipBasicSimple():
    p = BigWorld.player()
    return p.vipBasicPackage.get('packageID', 0) == gametypes.VIP_BASIC_SIMPLE_PACKAGE_ID and p.vipBasicPackage.get('tExpire', 0) > p.getServerTime()


def hasVipBasicFirst():
    p = BigWorld.player()
    return p.vipBasicPackage.get('packageID', 0) == gametypes.VIP_BASIC_FIRST_PACKAGE_ID and p.vipBasicPackage.get('tExpire', 0) > p.getServerTime()


def IsVipBasicSimple(packageID):
    return packageID == gametypes.VIP_BASIC_SIMPLE_PACKAGE_ID


def globalFriend2FriendVal(gVal):
    fVal = FriendVal(name=gVal.roleName, dbID=0, gbId=gVal.gbId, pally=0, group=gametypes.FRIEND_GROUP_GLOBAL_FRIEND, box=None, school=gVal.extraInfo.get('school', 0), sex=gVal.extraInfo.get('sex', 1), level=gVal.extraInfo.get('level', 0), signature=gVal.extraInfo.get('signature', ''), acknowledge=True, state=gVal.online, spaceNo=0, areaId=0, showsig=False, hatred=0, offlineMsgCnt=0, photo=gVal.extraInfo.get('photo', ''), opNuid=0, apprentice=False, yixinOpenId='', deleted=False, toHostID=0, flowbackType=0, intimacy=0, intimacySrc={}, intimacyLv=1, remarkName='', mingpaiId=gVal.extraInfo.get('mingpaiId', 0))
    fVal.temp = False
    fVal.recent = False
    fVal.time = utils.getNow()
    fVal.eid = 0
    fVal.server = gVal.server
    return fVal


def getNameWithMingPain(name, mpId, w = 0, h = 0):
    return name + richTextUtils.mingPaiRichText(mpId, w, h)


def getCharLenth(txt):
    cs = 0
    es = 0
    i = 0
    while i < len(txt):
        if ord(txt[i]) > 128:
            cs += 1
            i += 2
        else:
            es += 1
            i += 1

    return cs + es


def calcYaoPeiLv(quality, exp):
    maxYaoPeiLv = SCD.data.get('maxYaoPeiLv', 0)
    for lv in range(1, maxYaoPeiLv + 1):
        if exp < YLED.data.get((quality, lv), {}).get('exp', 0):
            return lv - 1

    return maxYaoPeiLv


def getItemUseNum(itemId, limitType):
    p = BigWorld.player()
    group = CID.data.get(itemId, {}).get('useLimitGroup', 0)
    key = (gametypes.ITEM_USE_CHECK_GROUP, group) if group > 0 else (gametypes.ITEM_USE_CHECK_SINGLE, itemId)
    history = p.itemUseHistory.get(key)
    if history:
        t = getItemUseLimitTime(limitType)
        data = history.get(limitType, (0, 0))
        if t == data[0]:
            value = data[1]
        else:
            value = 0
    else:
        value = 0
    return value


def getitemUseLimitNum(itemId):
    p = BigWorld.player()
    cdata = CID.data.get(itemId, {})
    if cdata:
        useLimit = cdata.get('useLimit', [])
        group = cdata.get(itemId, {}).get('useLimitGroup', 0)
    key = (gametypes.ITEM_USE_CHECK_GROUP, group) if group > 0 else (gametypes.ITEM_USE_CHECK_SINGLE, itemId)
    history = p.itemUseHistory.get(key)
    rest = []
    for limitType, limitNum in useLimit:
        num = min(utils.getUseLimitByLv(itemId, p.lv, limitType, limitNum), limitNum)
        if limitType == gametypes.ITEM_USE_LIMIT_TYPE_FOREVER:
            if history:
                history.setdefault(limitType, 0)
                used = history.get(limitType, 0)
            else:
                used = 0
            restNum = num - used
            rest.append((limitType, restNum))
        else:
            if limitType == gametypes.ITEM_USE_LIMIT_TYPE_DAY:
                time = utils.getDaySecond()
            elif limitType == gametypes.ITEM_USE_LIMIT_TYPE_WEEK:
                time = utils.getWeekSecond()
            elif limitType == gametypes.ITEM_USE_LIMIT_TYPE_MONTH:
                time = utils.getMonthSecond()
            elif limitType == gametypes.ITEM_USE_LIMIT_TYPE_QUARTER:
                time = utils.getQuarterSecond()
            else:
                time = None
            if history:
                history.setdefault(limitType, [time, 0])
                data = history[limitType]
                used = data[1] if time == data[0] else 0
            else:
                used = 0
            restNum = num - used
            rest.append((limitType, restNum))

    data = ()
    if rest:
        data = min(rest)
    return data


def getFriendSrcDesc(srcId):
    remarkSrcNames = SCD.data.get('remarkSrcNames', {})
    if srcId in remarkSrcNames:
        return remarkSrcNames[srcId]
    else:
        return const.FRIEND_SRC_DICT.get(srcId, gameStrings.TEXT_GAME_1747)


def getItemUseLimit(itemId, limitType):
    val = CID.data.get(itemId)
    if val:
        useLimit = val.get('useLimit', [])
        for lType, num in useLimit:
            if lType == limitType:
                return num

    return 0


def getItemUseLimitTime(limitType):
    if limitType == gametypes.ITEM_USE_LIMIT_TYPE_DAY:
        return utils.getDaySecond()
    elif limitType == gametypes.ITEM_USE_LIMIT_TYPE_WEEK:
        return utils.getWeekSecond()
    elif limitType == gametypes.ITEM_USE_LIMIT_TYPE_MONTH:
        return utils.getMonthSecond()
    elif limitType == gametypes.ITEM_USE_LIMIT_TYPE_QUARTER:
        return utils.getQuarterSecond()
    else:
        return None


def checkEquipMaterialDiKou(itemDict):
    p = BigWorld.player()
    dkFlag, yunChuiNeed, coinNeed, _ = utils.calcEquipMaterialDiKou(p, itemDict)
    if not dkFlag:
        return False
    if yunChuiNeed > p.getFame(const.YUN_CHUI_JI_FEN_FAME_ID):
        return False
    if hasattr(p, 'unbindCoin') and hasattr(p, 'bindCoin') and hasattr(p, 'freeCoin'):
        coinOwn = p.unbindCoin + p.bindCoin + p.freeCoin
    else:
        coinOwn = 0
    if coinNeed > coinOwn:
        return False
    return True


def getEquipMaterialDiKouInfo(itemDict):
    p = BigWorld.player()
    _, yunChuiNeed, coinNeed, _ = utils.calcEquipMaterialDiKou(p, itemDict)
    info = {}
    yunChuiOwn = p.getFame(const.YUN_CHUI_JI_FEN_FAME_ID)
    info['yunChui'] = convertNumStr(yunChuiOwn, yunChuiNeed, needThousand=True)
    info['yunChuiBtnEnabled'] = yunChuiOwn < yunChuiNeed
    if hasattr(p, 'unbindCoin') and hasattr(p, 'bindCoin') and hasattr(p, 'freeCoin'):
        coinOwn = p.unbindCoin + p.bindCoin + p.freeCoin
    else:
        coinOwn = 0
    info['coin'] = convertNumStr(coinOwn, coinNeed, needThousand=True)
    info['coinBtnEnabled'] = coinOwn < coinNeed
    needShowCoin = coinNeed > 0
    for itemId in itemDict:
        if ETDD.data.get(itemId, {}).get('coin', 0):
            needShowCoin = True

    info['needShowCoin'] = needShowCoin
    return info


def isItemHasDiKouInfo(itemId):
    return itemId in ETDD.data


def parseBubbleMsg(msg):
    p = BigWorld.player()
    guildName = getattr(p, 'guildName', '')
    msg = msg.replace('$g', guildName)
    roleName = getattr(p, 'roleName', '')
    msg = msg.replace('$p', roleName)
    if p.guild:
        msg = msg.replace('$mnfst', p.guild.menifest)
    return msg


def getWWArmyRichTextByName(name):
    txt = ''
    if gameglobal.rds.configData.get('enableWorldWarArmy', False):
        army = BigWorld.player().worldWar.army
    elif gameglobal.rds.configData.get('enableWingWorld', False):
        army = BigWorld.player().wingWorld.army
    else:
        return txt
    postId = 0
    for _, postVal in army.iteritems():
        if postVal.name == name:
            postId = postVal.postId
            break

    if postId:
        txt = richTextUtils.wwArmyPostRichText(postId)
    return txt


def getSimpleDaysAgo(tWhen):
    days = [gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_1931, gameStrings.TEXT_UIUTILS_2682, gameStrings.TEXT_UIUTILS_2682_1]
    now = utils.getNow()
    x = int((now - tWhen) / 86400)
    if x > 6:
        x = 6
    if x < len(days):
        return days[x]
    return gameStrings.TEXT_UIUTILS_2689 % x


def getLastOnlineTxt(interval):
    if interval == 0:
        return gameStrings.TEXT_FRIENDPROXY_293_1
    elif interval < 3600:
        return gameStrings.TEXT_GUILDPROXY_756
    elif interval < 86400:
        return str(interval / 3600) + gameStrings.TEXT_GUILDPROXY_758
    elif interval < 2592000:
        return str(interval / 86400) + gameStrings.TEXT_GUILDPROXY_760
    elif interval < 946080000:
        return str(interval / 2592000) + gameStrings.TEXT_GUILDPROXY_762
    else:
        return str(interval / 31536000) + gameStrings.TEXT_GUILDPROXY_764


def getFameLv(fameId, fameVal):
    val = FAMED.data.get(fameId, {})
    fameLv = 0
    maxLv = 1
    for lv, fameValue in val.get('lvUpNeed', {}).items():
        if fameVal >= fameValue:
            fameLv = lv
        maxLv = lv

    fameLv = min(maxLv, fameLv)
    return fameLv


def getProjectId():
    try:
        sec = ResMgr.openSection('../game/tianyu.xml')
        projectId = sec.readString('projectId')
        if not projectId:
            return '13.2000026'
        return projectId
    except Error:
        return '13.2000026'


def lv2ArenaPlayoffsTeamGroup(lv):
    if lv >= 1 and lv <= 59:
        return '50~59'
    if lv >= 60 and lv <= 69:
        return '60~69'
    if lv >= 70 and lv <= 79:
        return '70~79'
    return gameStrings.TEXT_UIUTILS_2734


def textToHtml(text):
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    return text


def htmlToText(html):
    html = html.replace('<', '&lt;')
    html = html.replace('>', '&gt;')
    return html


def getBackHomeCoolDown():
    lastTime = BigWorld.player().myHome.lastUseBackHomeSkillTime
    total = HCD.data.get('backHomeSkillCD', 1800)
    passTime = utils.getNow() - lastTime
    return (total, passTime)


def noNeedBackHomeCoolDown():
    p = BigWorld.player()
    return formula.spaceInHomeRoom(p.spaceNo) or formula.spaceInHomeFloor(p.spaceNo) or formula.spaceInHomeCommunity(p.spaceNo) or formula.spaceInHome(p.spaceNo)


def setItemPlusInfo(equipment, itemPlusInfo):
    if itemPlusInfo and equipment:
        for part, info in itemPlusInfo.iteritems():
            equip = equipment[part]
            if equip and info:
                for attrName, value in info.iteritems():
                    if value:
                        setattr(equip, attrName, value)


def checkShareTeamLvLimit():
    p = BigWorld.player()
    teamInfoUseLv = SCD.data.get('teamInfoUseLv', 20)
    if p.lv < teamInfoUseLv:
        return False
    else:
        return True


def checkLevelAndTime(key):
    item = GLD.data.get(key, {})
    if not item:
        return False
    else:
        p = BigWorld.player()
        lvData = item.get('lv', [0, 0])
        beginTime = item.get('timeStart', None)
        endTime = item.get('timeEnd', None)
        weekSet = item.get('weekSet', 0)
        if not lvData[0] <= p.lv <= lvData[1]:
            p.showGameMsg(GMDD.data.TEAMROOM_NOT_RIGHT_LV, ())
            return False
        if utils.isInvalidWeek(weekSet):
            p.showGameMsg(GMDD.data.TEAMROOM_NOT_RIGHT_TIME, ())
            return False
        if beginTime and endTime:
            if not utils.inCrontabRange(beginTime, endTime):
                p.showGameMsg(GMDD.data.TEAMROOM_NOT_RIGHT_TIME, ())
                return False
        return True


def isZhenChuanTgt(gbId):
    p = BigWorld.player()
    if p.soleMentorGbId == gbId or p.soleApprenticeGbId == gbId:
        return True
    return False


def isJieQiTgt(gbId):
    p = BigWorld.player()
    return gbId == p.friend.intimacyTgt


def isSameGuild(gbId):
    p = BigWorld.player()
    guild = p.guild
    if not guild:
        return False
    return gbId in guild.member


def isPartner(gbId):
    p = BigWorld.player()
    return gbId in p.partner


def isMentor(gbId):
    p = BigWorld.player()
    apprenticeInfo = getattr(p, 'apprenticeInfo', {})
    return gbId in apprenticeInfo


def isApprentice(gbId):
    p = BigWorld.player()
    apprenticeInfo = getattr(p, 'apprenticeGbIds', [])
    if apprenticeInfo:
        for mateGbId, isGraduate in apprenticeInfo:
            if mateGbId == gbId:
                return True

    return False


def isSameMentor(gbId):
    p = BigWorld.player()
    apprenticeInfo = getattr(p, 'apprenticeInfo', {})
    for k, v in apprenticeInfo.iteritems():
        mates = v.get('mates')
        if mates:
            for mateGbId, isGraduate in mates:
                if mateGbId == gbId:
                    return True

    return False


def getPvpAverageValue(averageExp, school, eType):
    lvPre = 0
    lvLast = 0
    lvMax = PEDD.data.get((eType, school), {}).get('lvMax', 0)
    for lv in range(1, lvMax + 1):
        if averageExp < PELD.data.get((lv, eType, school), {}).get('exp', 0):
            lvPre = lv - 1
            lvLast = lv
            break

    if lvPre == 0 and lvLast == 0:
        lvPre = lvMax
        point = 0
    else:
        expPre = PELD.data.get((lvPre, eType, school), {}).get('exp', 0)
        expLast = PELD.data.get((lvLast, eType, school), {}).get('exp', 0)
        point = 0
        if expLast - expPre != 0:
            point = (averageExp - expPre) / float(expLast - expPre)
    arverageValue = round(lvPre + point, 2)
    return arverageValue


def getPvpAllExp(schoolList):
    expSum = 0
    pvpEnhanceList = gameglobal.rds.ui.pvpEnhance.getPvpEnhanceList()
    for school in schoolList:
        if school in pvpEnhanceList:
            singlePvpEnhance = pvpEnhanceList.get(school)
            expSum += singlePvpEnhance[0] + singlePvpEnhance[2]

    return expSum


def getCatchUpWeekDiff(key):
    sd = PSCD.data.get(utils.getHostId(), {})
    if sd.has_key(key):
        delayTime = sd.get(key, 0) * const.TIME_INTERVAL_WEEK
    else:
        delayTime = 0
    weekDiff = utils.getIntervalWeek(utils.getNow(), utils.getServerOpenTime() + delayTime)
    return weekDiff


def getPvpMasteryAverageValue(school, eType):
    schoolList = list(const.SCHOOL_SET)
    if not gameglobal.rds.configData.get('enableNewSchoolYeCha', False):
        schoolList.remove(const.SCHOOL_YECHA)
    weekDiff = getCatchUpWeekDiff('pvpInterval')
    targetExp = PPED.data.get(weekDiff, {}).get('standard', 0)
    if targetExp != 0:
        targetExpAverage = targetExp / (len(schoolList) * 2)
        targetAverage = getPvpAverageValue(targetExpAverage * 1.0, school, eType)
    else:
        targetAverage = 0
    myAllExp = getPvpAllExp(schoolList)
    myExpAverage = myAllExp / (len(schoolList) * 2)
    myAverage = getPvpAverageValue(myExpAverage * 1.0, school, eType)
    return (myAverage, targetAverage)


def getZaijuLittleHeadIconPath(name):
    return 'zaijuLittleHeadIcon/%s.dds' % name


def getZaijuLittleHeadIconPathById(zaijuId):
    return getZaijuLittleHeadIconPath(ZD.data.get(zaijuId, {}).get('littleHeadIcon', ''))


def isQuestComplete(questId):
    completeList = BigWorld.player().questInfoCache.get('complete_tasks', [])
    return questId in completeList


def getDefaultSchemeName(panelType, schemeNo):
    return gameStrings.SCHEME_SWITCH_DEFAULT_SCHEME_NAME.get(panelType, {}).get(schemeNo, '')


def getWSSkillShortCut(clientShortCut):
    ret = {}
    for key, value in clientShortCut.iteritems():
        if isinstance(key, tuple) and isinstance(value, tuple) and key[0] == uiConst.SKILL_ACTION_BAR and key[1] >= uiConst.WUSHUANG_SKILL_START_POS_LEFT and key[1] < uiConst.WUSHUANG_SKILL_END_POS:
            ret[key] = value

    return ret


def getItemByKind(page, pos, resKind, player):
    it = None
    if resKind == const.RES_KIND_INV:
        it = player.inv.getQuickVal(page, pos)
    elif resKind == const.RES_KIND_EQUIP:
        it = player.equipment.get(pos)
    elif resKind == const.RES_KIND_INV_BAR:
        it = player.inv.getInvBarVal(pos)
    elif resKind == const.RES_KIND_MATERIAL_BAG:
        it = player.materialBag.getQuickVal(page, pos)
    elif resKind == const.RES_KIND_CART:
        it = player.cart.getQuickVal(page, pos)
    elif resKind == const.RES_KIND_BUY_BACK_LIST:
        if page in player.buyBackDict:
            it = player.buyBackDict[page].getItem(player, pos)
    elif resKind == const.RES_KIND_STORAGE:
        it = player.storage.getQuickVal(page, pos)
    elif resKind == const.RES_KIND_RIDE_WING_BAG:
        it = player.rideWingBag.getQuickVal(page, pos)
    return it


def getReliveCountDownTime():
    if not gameglobal.rds.configData.get('enableCalcAvatarReliveIntervalDynamicAdjust', False):
        return const.DEFAULT_RELIVE_TIME
    p = BigWorld.player()
    mapId = formula.getMapId(p.spaceNo)
    mcd = MCD.data.get(mapId)
    relivePunishInterval = mcd.get('relivePunishInterval')
    if not relivePunishInterval:
        return const.DEFAULT_RELIVE_TIME
    reliveTime = mcd.get('reliveTime')
    if not reliveTime:
        return const.DEFAULT_RELIVE_TIME
    lastReliveTime, lastReliveStep = p.lastReliveInfo.get(p.spaceNo, (0, 0))
    now = utils.getNow()
    if lastReliveTime + relivePunishInterval > now:
        reliveStep = min(lastReliveStep + 1, len(reliveTime) - 1)
    else:
        step = (now - lastReliveTime) / relivePunishInterval
        reliveStep = max(0, lastReliveStep - step)
    p.cell.setReliveTimeInfo(now, reliveStep)
    return const.DEFAULT_RELIVE_TIME + reliveTime[reliveStep]


def getMCTopBottomOnWidget(widget, mc):
    topLeftPosX, topLeftPosY = ASUtils.local2Global(widget, mc.x, mc.y)
    bottomRightPosX, bottomRightPosY = ASUtils.local2Global(widget, mc.x + mc.width, mc.y + mc.height)
    return ((topLeftPosX, topLeftPosY), (bottomRightPosX, bottomRightPosY))


def getSpritePropsArray(type):
    ret = []
    for key, val in SSADD.data.items():
        if val.get('type', 0) == type:
            ret.append(val)

    ret.sort(key=lambda k: k.get('displayOrder', 0))
    return ret


def calcSpriteAttr(spriteProp, showType, idParam):
    for i, propInfo in enumerate(idParam):
        params, formulaVal = propInfo
        for idx in xrange(len(params)):
            prop = params[idx]
            pVal = commcalc.getSummonedSpritePropValueById(spriteProp, prop)
            formulaVal = formulaVal.replace('p' + str(idx + 1), str(pVal))

        if showType.find('p' + str(i + 1)) < 0:
            continue
        val = eval(formulaVal)
        placeHolder = '[1.p' + str(i + 1) + ']'
        showType = showType.replace(placeHolder, str(int(val)))
        placeHolder = '[2.p' + str(i + 1) + ']'
        showType = showType.replace(placeHolder, str(round(val * 100, 1)) + '%')
        placeHolder = '[3.p' + str(i + 1) + ']'
        showType = showType.replace(placeHolder, str(round(val, 1)))

    return showType


def createSpriteArr(spriteProp, info, isExtra):
    ret = []
    for idx, item in enumerate(info):
        try:
            attrStr = ''
            attrStr = calcSpriteAttr(spriteProp, item.get('showType', ''), item.get('idParam', []))
            key = str(item['type']) + ',' + str(item.get('displayOrder', 0))
            ret.append([item['name'],
             attrStr,
             str(item['type']),
             str(item.get('displayOrder', 0))])
        except Exception as e:
            gamelog.debug('m.l@uiUtils.createSpriteArr error', e.message)

    return ret


def getSpritePropsTooltip(spriteProp, propType, displayOrder):
    key = (propType, displayOrder)
    p = BigWorld.player()
    ret = ''
    data = SSADD.data.get(key, {})
    if data:
        detail = data.get('detail1', '')
        i = 1
        formulaDate = data.get('formula' + str(i), '')
        while formulaDate:
            for idx, item in enumerate(data.get('formual' + str(i) + 'Params', [])):
                formulaDate = formulaDate.replace('p' + str(idx + 1), str(commcalc.getSummonedSpritePropValueById(spriteProp, item)))

            try:
                val = eval(formulaDate)
            except:
                val = 0

            detail = detail.replace('[1.p' + str(i) + ']', str(int(val)))
            detail = detail.replace('[2.p' + str(i) + ']', str(round(val * 100, 1)) + '%')
            detail = detail.replace('[3.p' + str(i) + ']', str(round(val, 1)))
            i += 1
            formulaDate = data.get('formula' + str(i), '')

        ret = detail
    return ret


def addItemTipById(itemMc, itemId):
    if itemMc.tipItemId != itemId:
        itemMc.tipItemId = itemId
        TipManager.addItemTipById(itemMc, itemId)


def getSchoolNameById(schoolId):
    return SCOOLD.data.get(schoolId, {}).get('name', '')


def getRedPacketSourceName(pType, subType):
    if pType == const.RED_PACKET_TYPE_GUILD:
        return GCD.data.get('redPacketSignInNameDict', {}).get(subType, '')
    if pType == const.RED_PACKET_TYPE_ACHIEVE:
        return AD.data.get(subType, {}).get('name', '')
    if pType == const.RED_PACKET_TYPE_GUILD_MERGER_CLAP:
        return GCD.data.get('guildMergeRedPacketSourceName', 'guildMergeRedPacketSourceName')
    return ''


def getGuideLv():
    p = BigWorld.player()
    if hasattr(p, 'carrerGuideData'):
        lv = p.lv
        lvKey = gametypes.MIN_GUIDE_LV
        if lv < lvKey:
            lvTxt = '%d-%d' % (1, lvKey)
        else:
            while lv > lvKey:
                lvKey += gametypes.GUIDE_OFFSET

            lvTxt = '%d-%d' % (lvKey - gametypes.GUIDE_OFFSET + 1, lvKey)
        return (lvKey, lvTxt)
    else:
        return (0, '')


def getRankEndTimeString():
    t = time.localtime(BigWorld.player().getServerTime())
    timeTxt = gameStrings.RANK_END_TIME_TEXT % (t.tm_year, t.tm_mon, t.tm_mday)
    return timeTxt


def filterPinYin(searchKey, name):
    pinYin = pinyinConvert.strPinyin(searchKey)
    if not pinYin:
        return False
    pinYin = pinYin.lower()
    sName = pinyinConvert.strPinyinFirst(name).lower()
    fName = pinyinConvert.strPinyin(name).lower()
    return pinYin in sName or pinYin in fName


def searchItemNames(name, consignType = uiConst.CONSIGN_TYPE_COMMON, searchHistory = None):
    name = name.strip()
    ret = []
    if name == '':
        return ret
    name = name.lower()
    isPinyinAndHanzi = utils.isPinyinAndHanzi(name)
    historyList = searchHistory.getHistoryList() if searchHistory else []
    if isPinyinAndHanzi == const.STR_HANZI_PINYIN:
        return ret
    pinyin = pinyinConvert.strPinyinFirst(name)
    if consignType == uiConst.CONSIGN_TYPE_COMMON:
        names = IND.data.get(uiConst.ITEM_NAME_CONSIGN, {}).get(pinyin[0], [])
    else:
        names = IND.data.get(uiConst.ITEM_NAME_COIN_CONSIGN, {}).get(pinyin[0], [])
    if len(name) == 1:
        namesCp = list(copy.deepcopy(names))
        for history in historyList:
            if history in namesCp:
                namesCp.remove(history)
                namesCp.insert(0, history)

        return namesCp
    if isPinyinAndHanzi == const.STR_ONLY_PINYIN:
        ret = [ x for x in names if name in str(pinyinConvert.strPinyinFirst(x)) ]
    else:
        ret = [ x for x in names if name in str(x) ]
    for history in historyList:
        if history in ret:
            ret.remove(history)
            ret.insert(0, history)

    return ret


def isContainString(str, subStr):
    return subStr.decode(utils.defaultEncoding()) in str.decode(utils.defaultEncoding())


def getSummonSpriteIconPath(spriteId):
    iconId = SSID.data.get(spriteId, {}).get('spriteIcon', 0)
    if not iconId:
        iconId = SSD.data.get(spriteId, {}).get('icon', '000')
    return 'summonedSprite/icon/%s.dds' % str(iconId)


def closeCompositeShop():
    ui = gameglobal.rds.ui
    if ui.compositeShop.mediator:
        ui.compositeShop.closeShop()
    if ui.yunChuiShop.mediator:
        ui.combineMall.hide()
        ui.yunChuiShop.hide()
    else:
        ui.yunChuiShop.hide()


def getCurrentChallengePassportSeason():
    return BigWorld.player().challengePassportData.season


def isInChallengePassport():
    season = getCurrentChallengePassportSeason()
    return challengePassportUtils.challengePassportIsInSeason(season)


def getNewServerSeasonBegin():
    startTime = utils.getServerOpenTime()
    return time.strftime('%Y.%m.%d', time.localtime(startTime))


def getNewServerSeasonEnd():
    startTime = utils.getServerOpenTime()
    weekPassDay = time.localtime(startTime).tm_wday + 1
    oneDayStep = 86400
    weekDays = 7 * oneDayStep
    lastWeek = CPCD.data.get('challengePassportNewServerWeeks', 0)
    lastTime = lastWeek * weekDays
    endTime = utils.getServerOpenTime() + lastTime - weekPassDay * oneDayStep
    return time.strftime('%Y.%m.%d', time.localtime(endTime))


def getCurrentChallengePassportWeek():
    currentSeason = getCurrentChallengePassportSeason()
    if currentSeason == -1:
        openWeek = utils.getServerOpenWeeks()
        if 0 <= openWeek < len(gametypes.CHALLENGE_PASSPORT_TYPE_WEEK):
            return gametypes.CHALLENGE_PASSPORT_TYPE_WEEK[openWeek]
        else:
            return -1
    else:
        oneDayStep = 86400
        wholeWeekStep = oneDayStep * 7
        weekDayNum = 7
        seasonData = CPSD.data.get(currentSeason, {})
        if seasonData:
            beginTime = seasonData.get('beginTime', 0)
            beginTime = '.'.join(beginTime.split('.')[0:3] + ['0'] * 3)
            beginTimeInt = utils.getTimeSecondFromStr(beginTime)
            endTime = seasonData.get('endTime', 0)
            endTime = '.'.join(endTime.split('.')[0:3] + ['0'] * 3)
            endTimeInt = utils.getTimeSecondFromStr(endTime)
            now = utils.getNow()
            weekLeftDay = weekDayNum - utils.localtimeEx(beginTimeInt).tm_wday
            firstWeekStep = weekLeftDay * oneDayStep
            weekStart = beginTimeInt
            weekIdx = 0
            while weekStart < endTimeInt and weekIdx < len(gametypes.CHALLENGE_PASSPORT_TYPE_WEEK):
                addStep = firstWeekStep if weekIdx == 0 else wholeWeekStep
                if weekStart <= now <= weekStart + addStep:
                    return gametypes.CHALLENGE_PASSPORT_TYPE_WEEK[weekIdx]
                weekStart += addStep
                weekIdx += 1

    return -1


def convertIntToChn(n):
    CN_NUM = [gameStrings.TEXT_UIUTILS_3247,
     gameStrings.TEXT_PLAYRECOMMPROXY_848,
     gameStrings.TEXT_PLAYRECOMMPROXY_848_1,
     gameStrings.TEXT_PLAYRECOMMPROXY_848_2,
     gameStrings.TEXT_PLAYRECOMMPROXY_848_3,
     gameStrings.TEXT_PLAYRECOMMPROXY_848_4,
     gameStrings.TEXT_PLAYRECOMMPROXY_848_5,
     gameStrings.TEXT_UIUTILS_3247_1,
     gameStrings.TEXT_UIUTILS_3247_2,
     gameStrings.TEXT_UIUTILS_3247_3]
    CN_UNIT = [gameStrings.TEXT_UIUTILS_3247,
     gameStrings.TEXT_UIUTILS_3248,
     gameStrings.TEXT_UIUTILS_3248_1,
     gameStrings.TEXT_UIUTILS_3248_2,
     gameStrings.TEXT_CBGMAINPROXY_273,
     gameStrings.TEXT_UIUTILS_3248,
     gameStrings.TEXT_UIUTILS_3248_1]

    def turn(x, y):
        if y >= 1:
            a = x // pow(10, y)
            b = x % pow(10, y)
            c = CN_NUM[a] + CN_UNIT[y]
            if y > 4 and b < pow(10, 4):
                c += CN_UNIT[4]
            if len(str(x)) - len(str(b)) >= 2 and b != 0:
                c += CN_UNIT[0]
        else:
            a = x
            b = 0
            c = CN_NUM[a]
        return (c, b)

    def tstr(x):
        c = turn(x, len(str(x)) - 1)
        a = c[0]
        b = c[1]
        while b != 0:
            a += turn(b, len(str(b)) - 1)[0]
            b = turn(b, len(str(b)) - 1)[1]

        return a

    numStr = tstr(n)
    if 10 <= n <= 19:
        numStr = numStr[2:]
    return numStr


def formatLinkZone(txt, gbId = 0, hostId = 0, color = '#174C66', underLine = True, zoneEvent = True, addServerName = False):
    txt = '' if not txt else txt
    gbId = 0 if not gbId else gbId
    hostId = 0 if not hostId else hostId
    if addServerName and hostId and hostId != utils.getHostId():
        txt += '-%s' % utils.getServerName(hostId)
    if underLine:
        txt = '<u>%s</u>' % txt
    if zoneEvent:
        txt = "<a href = \'event:shareZone-%d-%d\'>%s</a>" % (gbId, hostId, txt)
    msg = "<font color= \'%s\'>%s</font>" % (color, txt)
    return msg


def formatPersonalZoneNameColor(txt, color = '#174C66'):
    txt = '' if not txt else txt
    msg = formatLinkZone(txt, underLine=False, zoneEvent=False)
    return msg


def formatLinkZoneMoment(txt, momentId, color = '#217AA6'):
    txt = '' if not txt else txt
    momentId = 0 if not momentId else momentId
    msg = "<font color= \'%s\'><a href = \'event:shareMoment-%d\'><u>%s</u></a></font>" % (color, momentId, txt)
    return msg


def getHeadIconPath(school, gender):
    return 'headIcon/%s.dds' % str(school * 10 + gender)


def getSchoolLabelString(school):
    return uiConst.JOB_LABELS[school]


def getPlayerTopRankKey():
    p = BigWorld.player()
    if 1 <= p.lv <= 59:
        return '1_59'
    if 60 <= p.lv <= 69:
        return '60_69'
    if 70 <= p.lv <= 89:
        return '70_79'
    return '1_59'


def intToRoman(num):
    """
    :type num: int
    :rtype: str
    """
    c = {0: ('', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX'),
     1: ('', 'X', 'XX', 'XXX', 'XL', 'L', 'LX', 'LXX', 'LXXX', 'XC'),
     2: ('', 'C', 'CC', 'CCC', 'CD', 'D', 'DC', 'DCC', 'DCCC', 'CM'),
     3: ('', 'M', 'MM', 'MMM')}
    roman = []
    roman.append(c[3][num / 1000 % 10])
    roman.append(c[2][num / 100 % 10])
    roman.append(c[1][num / 10 % 10])
    roman.append(c[0][num % 10])
    s = ''
    for i in roman:
        s = s + i

    return s
