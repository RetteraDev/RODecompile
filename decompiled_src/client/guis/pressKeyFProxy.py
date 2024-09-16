#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pressKeyFProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import const
import gameglobal
import hotkey as HK
import formula
from ui import gbk2unicode
from guis import uiConst
from guis import uiUtils
from sfx import keyboardEffect
from uiProxy import UIProxy
from data import sys_config_data as SCD
from data import quest_marker_data as QMD
from data import fkey_data as FD
from data import npc_data as ND
from data import duel_config_data as DCD

class PressKeyFProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PressKeyFProxy, self).__init__(uiAdapter)
        self.modelMap = {'handleClick': self.onHandleClick}
        self.tipName = [gameStrings.TEXT_PRESSKEYFPROXY_29_5,
         gameStrings.TEXT_PRESSKEYFPROXY_29_1,
         gameStrings.TEXT_PRESSKEYFPROXY_29_2,
         gameStrings.TEXT_PRESSKEYFPROXY_29_3,
         gameStrings.TEXT_PRESSKEYFPROXY_29_4,
         gameStrings.TEXT_PRESSKEYFPROXY_29_4,
         gameStrings.TEXT_PRESSKEYFPROXY_29_5,
         gameStrings.TEXT_PRESSKEYFPROXY_29_6,
         gameStrings.TEXT_PRESSKEYFPROXY_29_7,
         gameStrings.TEXT_PRESSKEYFPROXY_29_8,
         gameStrings.TEXT_ACTIONBARPROXY_1901,
         gameStrings.TEXT_PRESSKEYFPROXY_29_9,
         gameStrings.TEXT_DIGONGPROXY_207_4,
         gameStrings.TEXT_CLANWARPROXY_217,
         gameStrings.TEXT_PRESSKEYFPROXY_29_2,
         gameStrings.TEXT_PRESSKEYFPROXY_29_12,
         gameStrings.TEXT_CLANWARPROXY_217,
         gameStrings.TEXT_PRESSKEYFPROXY_29_7,
         gameStrings.TEXT_PRESSKEYFPROXY_29_13,
         gameStrings.TEXT_PRESSKEYFPROXY_29_14,
         gameStrings.TEXT_PRESSKEYFPROXY_29_15,
         gameStrings.TEXT_UIUTILS_1565]
        self.isMarkerNpc = False
        self.isDroppedItem = False
        self.isQuestBox = False
        self.isTreasureBox = False
        self.isNormalNpc = False
        self.isTransport = False
        self.isJiguan = False
        self.isInteractiveAvatar = False
        self.isFind = False
        self.isExplore = False
        self.isClanWarCreation = False
        self.isClanWarMarker = False
        self.isGuildBuildingMarker = False
        self.isGuildEntity = False
        self.isDestroyable = False
        self.isZaiju = False
        self.isLifeCsmItem = False
        self.isKiss = False
        self.isMonster = False
        self.isBattleFieldFlag = False
        self.isMovingPlatform = False
        self.isRoundTable = False
        self.isInteractive = False
        self.isBusinessItem = False
        self.isBattleFieldCqzzFlag = False
        self.isOccupy = False
        self.type = const.F_NONE
        self.npcEnt = set([])
        self.markers = set([])
        self.interactiveAvatars = set([])
        self.itemEnt = set([])
        self.clanWarCreationId = None
        self.guildBuildingMarkerId = None
        self.guildEntityId = None
        self.mediator = None
        self.npcCallback = None
        self.lastNpcName = None
        self.lifeCsmItem = None
        self.questBox = None
        self.treasureBox = None
        self.zaiju = None
        self.monster = None
        self.oreSpawnPoint = None
        self.battleFieldFlag = None
        self.movingPlatform = None
        self.roundTable = None
        self.trideSpecialAction = None
        self.interactiveObj = None
        self.targetId = None
        self.wingWorldReliveBoardId = None
        self.entIdSet = set([])
        self.entTypeDict = {}

    def reset(self):
        self.isMarkerNpc = False
        self.isDroppedItem = False
        self.isQuestBox = False
        self.isTreasureBox = False
        self.isNormalNpc = False
        self.isTransport = False
        self.isInteractiveAvatar = False
        self.isFind = False
        self.isExplore = False
        self.isClanWarCreation = False
        self.isClanWarMarker = False
        self.isGuildBuildingMarker = False
        self.isGuildEntity = False
        self.isDestroyable = False
        self.isZaiju = False
        self.isLifeCsmItem = False
        self.isMonster = False
        self.isBattleFieldFlag = False
        self.isMovingPlatform = False
        self.isKiss = False
        self.isOccupy = False
        self.type = const.F_NONE
        self.npcEnt = set([])
        self.markers = set([])
        self.interactiveAvatars = set([])
        self.itemEnt = set([])
        self.lifeCsmItem = None
        self.questBox = None
        self.treasureBox = None
        self.zaiju = None
        self.monster = None
        self.oreSpawnPoint = None
        self.battleFieldFlag = None
        self.movingPlatform = None
        self.trideSpecialAction = None
        self.interactiveObj = None
        self.targetId = 0
        self.entIdSet = set([])
        self.entTypeDict = {}
        self.wingWorldReliveBoardId = None
        keyboardEffect.removeKeyboardEffect('effect_pickItem')

    @property
    def prioritys(self):
        p = BigWorld.player()
        if p.isInPUBG():
            return DCD.data.get('pubgFKeyPriority', [])
        else:
            return SCD.data.get('fKeyPriority', [])

    def show(self):
        detial = HK.HKM[HK.KEY_PICK_ITEM]
        if self.type == const.F_NONE or detial.getBrief() == '' and detial.getBrief(2) == '':
            return
        else:
            p = BigWorld.player()
            if formula.getFubenNo(p.obSpaceNo) in const.GUILD_FUBEN_ELITE_NOS:
                return
            keyName = detial.getBrief()
            if not keyName:
                keyName = detial.getBrief(2)
            if self.mediator:
                desc = None
                path = None
                extraDesc = None
                idx = 0
                bHoldP = False
                bIndirectP = False
                if self.type == const.F_MARKERNPC:
                    npcSlot = gameglobal.rds.ui.npcSlot
                    if npcSlot.params:
                        markId = npcSlot.params[0]
                        idx = QMD.data.get(markId, {}).get('fKey', 0)
                    elif npcSlot.path:
                        path = npcSlot.path
                    holdTime = QMD.data.get(markId, {}).get('holdTime', 0)
                    indirectTime = QMD.data.get(markId, {}).get('indirectTime', ())
                    if holdTime:
                        bHoldP = True
                    if indirectTime:
                        bIndirectP = True
                elif self.type == const.F_LifeCsmItem and self.lifeCsmItem and self.lifeCsmItem.inWorld:
                    idx = self.lifeCsmItem.getFKey()
                elif self.type == const.F_MONSTER and hasattr(self, 'monster') and self.monster and self.monster.inWorld:
                    idx = self.monster.getFKey()
                elif self.type == const.F_BATTLE_FIELD_FLAG and self.battleFieldFlag and self.battleFieldFlag.inWorld:
                    idx = self.battleFieldFlag.getFKey()
                elif self.type == const.F_ZAIJU and self.zaiju and self.zaiju.inWorld:
                    idx = self.zaiju.getFKey()
                elif self.type == const.F_INTERACTIVE and self.interactiveObj and self.interactiveObj.inWorld:
                    idx = self.interactiveObj.getFKey()
                elif self.type == const.F_MOVING_PLATFORM and self.movingPlatform and self.movingPlatform.inWorld:
                    idx = self.movingPlatform.getFKey()
                elif self.type == const.F_ORE_SPAWN_POINT and self.oreSpawnPoint and self.oreSpawnPoint.inWorld:
                    if self.oreSpawnPoint:
                        idx = self.oreSpawnPoint.getFKey()
                    else:
                        idx = 0
                elif self.type == const.F_TRANSPORT and BigWorld.player().inWingWarCity() and self.wingWorldReliveBoardId and BigWorld.entities.has_key(self.wingWorldReliveBoardId):
                    idx = BigWorld.entities[self.wingWorldReliveBoardId].getFKey()
                elif self.type == const.F_NORMALNPC:
                    npc = self.getTalkNpc()
                    if npc:
                        fKeyIdx = ND.data.get(npc.npcId, {}).get('fKey', 0)
                        if fKeyIdx:
                            idx = fKeyIdx
                if not idx:
                    ent = self.getEnt()
                    idx = ent.getFKey() if hasattr(ent, 'getFKey') else 0
                trapAvar = self.getHuntBFTrapInfo()
                if trapAvar:
                    idx = uiConst.HUNT_TRAP_FKEY_INDEX
                isBig = False
                if idx:
                    path, desc = uiUtils.getFKeyPathDesc(idx)
                    isBig = FD.data.get(idx, {}).get('isBig', False)
                if not desc:
                    fKeyTips = SCD.data.get('fKeyTips', self.tipName)
                    if self.type < len(fKeyTips):
                        desc = fKeyTips[self.type]
                if not path:
                    fKeyIcons = SCD.data.get('fKeyIcons', [])
                    if self.type < len(fKeyIcons):
                        path = fKeyIcons[self.type]
                    else:
                        path = fKeyIcons[0]
                    path = 'lifeskill/icon40/' + str(path) + '.dds'
                if self.type == const.F_NORMALNPC:
                    if desc.find('%s') != -1:
                        desc = desc % self.lastNpcName
                    else:
                        desc = gameStrings.TEXT_PRESSKEYFPROXY_224 % (keyName, desc)
                else:
                    self.lastNpcName = None
                    if not idx:
                        desc = gameStrings.TEXT_PRESSKEYFPROXY_224 % (keyName, desc)
                extraDesc = FD.data.get(idx, {}).get('extraDesc', '')
                if isBig:
                    self.hide()
                    if self.type == const.F_MONSTER:
                        gameglobal.rds.ui.buffSkill.addFKeyInfo(self.type, self.monster.id)
                    else:
                        gameglobal.rds.ui.buffSkill.addFKeyInfo(self.type, None, (path, desc, extraDesc))
                else:
                    gameglobal.rds.ui.buffSkill.clearFKeyInfo()
                    self.mediator.Invoke('showMc', (GfxValue(keyName),
                     GfxValue(gbk2unicode(desc)),
                     GfxValue(path),
                     GfxValue(bHoldP),
                     GfxValue(bIndirectP)))
                keyboardEffect.addKeyboardEffect('effect_pickItem')
            return

    def getHuntBFTrapInfo(self):
        trapAvatar = None
        p = BigWorld.player()
        if formula.inHuntBattleField(p.mapID):
            for ava in self.interactiveAvatars:
                if p.isEnemy(ava) or not ava.inWorld:
                    continue
                if p._isHasState(ava, const.BATTLE_FIELD_HUNT_IN_TRAP_BUFF):
                    trapAvatar = ava
                    break

        return trapAvatar

    def hide(self, destroy = False):
        if destroy:
            self.reset()
        if self.mediator:
            self.mediator.Invoke('hideMc')
            if gameglobal.rds.ui.dynamicFCastBar.widget:
                gameglobal.rds.ui.dynamicFCastBar.hide()

    def getPriority(self, type):
        if type == const.F_NONE:
            return const.F_NONE
        if self.prioritys and type < len(self.prioritys):
            return self.prioritys[type]
        return type

    def setType(self, type):
        if formula.inDotaBattleField(BigWorld.player().mapID):
            return
        else:
            oldPriority = self.getPriority(self.type)
            newPriority = self.getPriority(type)
            if newPriority < oldPriority or self.type == const.F_NONE:
                self.type = type
                if self.type == const.F_NORMALNPC:
                    self.startNpcCheck()
                else:
                    self.lastNpcName = None
                    self.show()
            return

    def startNpcCheck(self):
        if self.npcCallback:
            BigWorld.cancelCallback(self.npcCallback)
        self._checkNpcName()

    def _checkNpcName(self):
        if self.type != const.F_NORMALNPC:
            return
        npc = self.getTalkNpc()
        if npc and npc.roleName != self.lastNpcName:
            self.lastNpcName = npc.roleName
            self.show()
        if not npc:
            self.isNormalNpc = False
            self.removeType(const.F_NORMALNPC)
        self.npcCallback = BigWorld.callback(0.2, self._checkNpcName)

    def removeType(self, type):
        if self.type == const.F_NONE:
            return
        else:
            if self.type == type:
                minPriority = 1000
                minType = const.F_NONE
                tags = {const.F_MARKERNPC: self.isMarkerNpc,
                 const.F_DROPPEDITEM: self.isDroppedItem,
                 const.F_QUESTBOX: self.isQuestBox,
                 const.F_NORMALNPC: self.isNormalNpc,
                 const.F_TREASUREBOX: self.isTreasureBox,
                 const.F_TRANSPORT: self.isTransport,
                 const.F_JIGUAN: self.isJiguan,
                 const.F_AVATAR: self.isInteractiveAvatar,
                 const.F_CLANWARMARKER: self.isClanWarMarker,
                 const.F_FIND: self.isFind,
                 const.F_EXPLORE: self.isExplore,
                 const.F_CLANWARCREATION: self.isClanWarCreation,
                 const.F_DESTROYABLE: self.isDestroyable,
                 const.F_ZAIJU: self.isZaiju,
                 const.F_LifeCsmItem: self.isLifeCsmItem,
                 const.F_KISS: self.isKiss,
                 const.F_MONSTER: self.isMonster,
                 const.F_GUILDBUILDINGMARKER: self.isGuildBuildingMarker,
                 const.F_GUILDSIT: self.isGuildEntity,
                 const.F_BATTLE_FIELD_FLAG: self.isBattleFieldFlag,
                 const.F_ROUND_TABLE: self.isRoundTable,
                 const.F_BUSINESS_ITEM: self.isBusinessItem,
                 const.F_OCCUPY: self.isOccupy,
                 const.F_INTERACTIVE: self.isInteractive,
                 const.F_BATTLE_FIELD_CQZZ_FLAG: self.isBattleFieldCqzzFlag}
                for i, tag in tags.iteritems():
                    if tag:
                        if self.getPriority(i) < minPriority:
                            minType = i
                            minPriority = self.getPriority(i)

                entMinType, entMinPriority = self.getEntMinPriority()
                if minType == const.F_NONE or entMinPriority < minPriority:
                    minType = entMinType
                    minPriority = entMinPriority
                if minType != const.F_NONE:
                    self.type = minType
                    if self.type == const.F_NORMALNPC:
                        self.startNpcCheck()
                    else:
                        self.show()
                    return
                self.hide(True)
                gameglobal.rds.ui.buffSkill.clearFKeyInfo()
                self.lastNpcName = None
                self.type = const.F_NONE
            return

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_PRESS_KEYF:
            self.mediator = mediator
        if self.type != const.F_NONE and HK.HKM[HK.KEY_PICK_ITEM].getBrief() != '':
            if self.type == const.F_NORMALNPC:
                self.startNpcCheck()
            else:
                self.show()

    def getTalkNpc(self):
        npcEnt = list(self.npcEnt)
        chooseNpc = None
        dist = 10000
        npcPriority = gameglobal.NPC_WITH_UNCOMPLETE_QUEST
        if npcEnt:
            p = BigWorld.player()
            for npc in npcEnt:
                if npc.inWorld:
                    tempPriority = gameglobal.NPC_WITH_UNCOMPLETE_QUEST
                    if hasattr(npc, 'getNpcPriority'):
                        tempPriority = npc.getNpcPriority()
                    tempDist = (p.position - npc.position).length
                    if tempPriority == npcPriority and tempDist < dist or tempPriority > npcPriority:
                        dist = tempDist
                        npcPriority = tempPriority
                        chooseNpc = npc
                else:
                    npcEnt.remove(npc)

        return chooseNpc

    def addMarker(self, entId):
        self.markers.add(entId)
        self._refreshMarker()

    def removeMarker(self, entId):
        if entId in self.markers:
            self.markers.remove(entId)
        self._refreshMarker()

    def _refreshMarker(self):
        if self.isMarkerNpc == len(self.markers) > 0:
            return
        self.isMarkerNpc = len(self.markers) > 0
        if self.isMarkerNpc:
            self.setType(const.F_MARKERNPC)
        else:
            self.removeType(const.F_MARKERNPC)

    def onHandleClick(self, *arg):
        p = BigWorld.player()
        p.pickNearByItems(True)

    def addEnt(self, entId, type):
        self.entIdSet.add(entId)
        self.entTypeDict[entId] = type
        self.setType(type)

    def delEnt(self, entId, type):
        if entId in self.entIdSet:
            self.entIdSet.remove(entId)
            self.removeType(type)
            if self.entTypeDict.has_key(entId):
                del self.entTypeDict[entId]

    def delEntByType(self, type):
        delList = []
        for entId in self.entTypeDict:
            if self.entTypeDict[entId] == type:
                delList.append(entId)

        for entId in delList:
            self.delEnt(entId, type)

    def getEnt(self):
        minPriority = 1000
        ret = None
        for entId in list(self.entIdSet):
            ent = BigWorld.entity(entId)
            if ent:
                type = const.F_TYPE_CLASS_NAME.get(ent.__class__.__name__, const.F_NONE)
                if type != const.F_NONE:
                    priority = self.getPriority(type)
                    if priority < minPriority:
                        minPriority = priority
                        ret = ent
                elif self.entTypeDict.has_key(entId):
                    priority = self.getPriority(self.entTypeDict[entId])
                    if priority < minPriority:
                        minPriority = priority
                        ret = ent
            else:
                self.entIdSet.remove(entId)
                if self.entTypeDict.has_key(entId):
                    del self.entTypeDict[entId]

        return ret

    def getEntMinPriority(self):
        minPriority = 1000
        minType = const.F_NONE
        for entId in list(self.entIdSet):
            ent = BigWorld.entity(entId)
            if ent:
                type = const.F_TYPE_CLASS_NAME.get(ent.__class__.__name__, const.F_NONE)
                if type != const.F_NONE:
                    priority = self.getPriority(type)
                    if priority < minPriority:
                        minPriority = priority
                        minType = type
                elif self.entTypeDict.has_key(entId):
                    priority = self.getPriority(self.entTypeDict[entId])
                    if priority < minPriority:
                        minPriority = priority
                        minType = self.entTypeDict[entId]
            else:
                self.entIdSet.remove(entId)
                if self.entTypeDict.has_key(entId):
                    del self.entTypeDict[entId]

        return (minType, minPriority)
