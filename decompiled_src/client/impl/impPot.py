#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPot.o
import random
import BigWorld
import gameglobal
import utils
import formula
import clientcom
import const
from callbackHelper import Functor
from sfx import sfx
from data import dialogs_data as DD
TRAP_MAX_NUM = 3
POT_KEEP_EFF_INFO = 'potKeepEffInfo'

class ImpPot(object):

    def __init__(self):
        super(ImpPot, self).__init__()
        self.curPlayIngEvent = {}

    def dealTrapInEvent(self, trapLengthType = 1):
        data = self.getItemData()
        eventName = 'trapEvent'
        trapRateTypeName = 'trapRateType'
        if trapLengthType != 1:
            eventName = eventName + str(trapLengthType)
            trapRateTypeName = 'trapRateType' + str(trapLengthType)
        trapEvent = data.get(eventName, [])
        if trapEvent == []:
            return
        else:
            trapPos = trapLengthType - 1
            if trapEvent.__class__ == tuple:
                self.curPlayIngEvent[trapPos] = []
                self.curPlayIngEvent[trapPos].append(trapEvent)
                self.playEvent(trapEvent, trapLengthType)
            elif trapEvent.__class__ == list:
                rateType = data.get(trapRateTypeName, 0)
                rollPoint = random.uniform(0, 1)
                curRate = 0
                for trapGroup in trapEvent:
                    playRate = trapGroup[0]
                    if playRate.__class__ != int and playRate.__class__ != float:
                        continue
                    if rateType == 0 or rateType == None:
                        if rollPoint < playRate:
                            curEvent = trapGroup[1:]
                            if self.curPlayIngEvent.has_key(trapPos):
                                if self.curPlayIngEvent[trapPos] == None:
                                    self.curPlayIngEvent[trapPos] = []
                            else:
                                self.curPlayIngEvent[trapPos] = []
                            self.curPlayIngEvent[trapPos].append(curEvent)
                            self.playEvent(curEvent, trapLengthType)
                        rollPoint = random.uniform(0, 1)
                    else:
                        curRate = playRate + curRate
                        if rollPoint < curRate:
                            curEvent = trapGroup[1:]
                            if self.curPlayIngEvent.has_key(trapPos):
                                if self.curPlayIngEvent[trapPos] == None:
                                    self.curPlayIngEvent[trapPos] = []
                            else:
                                self.curPlayIngEvent[trapPos] = []
                            self.curPlayIngEvent[trapPos].append(curEvent)
                            self.playEvent(curEvent, trapLengthType)
                            return

            return

    def playEvent(self, trapEvent, trapLengthType):
        p = BigWorld.player()
        trapSoundHandleName = 'trapSoundHandle'
        if trapLengthType != 1:
            trapSoundHandleName = trapSoundHandleName + str(trapLengthType)
        try:
            for item in trapEvent:
                if not self.checkTrapEventValid(item):
                    continue
                if item[0] in (gameglobal.ACT_FLAG, gameglobal.EMOTION_FLAG):
                    self.faceTo(p) if hasattr(self, 'faceTo') else None
                    acts = [ str(i) for i in item[1:] ]
                    self.fashion.playActionSequence(self.model, acts, None)
                elif item[0] == gameglobal.VOICE_FLAG:
                    self.faceTo(p) if hasattr(self, 'faceTo') else None
                    gameglobal.rds.sound.playSound(int(item[1]))
                elif item[0] == gameglobal.POPO_FLAG:
                    dd = DD.data.get(int(item[1]), {})
                    msg = dd.get('details', '')
                    duration = item[2] if len(item) >= 3 else const.POPUP_MSG_SHOW_DURATION
                    duration = dd.get('interval', duration)
                    msg and self.topLogo and self.topLogo.setChatMsg(msg, duration)
                elif item[0] == gameglobal.SOUND_FLAG:
                    handle = gameglobal.rds.sound.playSound(int(item[1]), self)
                    setattr(self, trapSoundHandleName, handle)
                elif item[0] == gameglobal.UI_PUSH:
                    gameglobal.rds.ui.fubenMessage.show(int(item[1]), int(item[2]))
                elif item[0] == gameglobal.FAME_ACT_FLAG:
                    for fameId, lvs, act in item[1:]:
                        fameLv = p.getFameLv(fameId)
                        if fameLv in lvs:
                            if act:
                                self.faceTo(p) if hasattr(self, 'faceTo') else None
                                self.fashion.playActionSequence(self.model, [str(act)], None)
                            break

                elif item[0] == gameglobal.FAME_POPO_FLAG:
                    for fameId, lvs, dialogId in item[1:]:
                        fameLv = p.getFameLv(fameId)
                        if fameLv in lvs:
                            if dialogId:
                                dd = DD.data.get(int(dialogId), {})
                                msg = dd.get('details', '')
                                duration = dd.get('interval', const.POPUP_MSG_SHOW_DURATION)
                                msg and self.topLogo and self.topLogo.setChatMsg(msg, duration)
                            break

                elif item[0] == gameglobal.XJS_ACT_FLAG:
                    self.dealXJSAct(item[1:])
                elif item[0] == gameglobal.XJS_POPO_FLAG:
                    self.dealXJSPoPo(item[1:])
                elif item[0] == gameglobal.FAME_XJS_ACT_FLAG:
                    for fameId, lvs, act in item[1:]:
                        fameLv = p.getFameLv(fameId)
                        if fameLv in lvs:
                            if act:
                                self.dealXJSAct(act)
                            break

                elif item[0] == gameglobal.FAME_XJS_POPO_FLAG:
                    for fameId, lvs, dialogId in item[1:]:
                        fameLv = p.getFameLv(fameId)
                        if fameLv in lvs:
                            if dialogId:
                                self.dealXJSPoPo(dialogId)
                            break

                elif item[0] == gameglobal.ACT_FLAG_NOT_CHANGE_YAW:
                    acts = [ str(i) for i in item[1:] ]
                    self.fashion.playActionSequence(self.model, acts, None)
                elif item[0] in (gameglobal.CHANGE_MODEL_FLAG, gameglobal.CHANGE_MODEL2_FLAG):
                    if getattr(self, 'firstFetchFinished', False):
                        modelId = item[1]
                        clientcom.fetchModel(gameglobal.URGENT_THREAD, Functor(self.afterModelFinished, item[1:]), modelId)
                elif item[0] == gameglobal.GUILD_MANAGER_VOICE_FLAG:
                    if not hasattr(self, 'fashionId'):
                        continue
                    if self.fashionId in item[1]:
                        gameglobal.rds.sound.playSound(int(item[2]))
                elif item[0] == gameglobal.KEEP_EFFECT_FLAG:
                    self.playPotKeepEffect(trapLengthType, item)
                elif item[0] == gameglobal.SIGNATURE_POPO_FLAG:
                    dd = DD.data.get(int(item[1]), {})
                    sign = getattr(self, 'personalZoneSignature', '')
                    msg = sign if sign else dd.get('details', '')
                    duration = item[2] if len(item) >= 3 else const.POPUP_MSG_SHOW_DURATION
                    duration = duration if sign else dd.get('interval', duration)
                    msg and self.topLogo and self.topLogo.setChatMsg(msg, duration)
                elif item[0] == gameglobal.SIGNATURE_TALK_FLAG:
                    dd = DD.data.get(int(item[1]), {})
                    sign = getattr(self, 'personalZoneSignature', '')
                    msg = sign if sign else dd.get('details', '')
                    duration = item[2] if len(item) >= 3 else const.POPUP_MSG_SHOW_DURATION
                    duration = duration if sign else dd.get('interval', duration)
                    msg and gameglobal.rds.ui.autoQuest.show(msg, getattr(self, 'npcId', 0), duration, simpleNpc=self)

        except:
            pass

    def getPotKeepEffsName(self, trapLengthType):
        potKeepEffsName = 'potKeepEffs'
        if trapLengthType != 1:
            potKeepEffsName = potKeepEffsName + str(trapLengthType)
        return potKeepEffsName

    def playPotKeepEffect(self, trapLengthType, item):
        self.releasePotKeepEffs(trapLengthType)
        setattr(self, POT_KEEP_EFF_INFO, (trapLengthType, item))
        p = BigWorld.player()
        potKeepEffsName = self.getPotKeepEffsName(trapLengthType)
        lockedId = getattr(self, 'lockedId', None)
        effectId = item[1]
        if not p.isEnemy(self):
            return
        else:
            if lockedId and lockedId == p.id:
                effectId = item[2]
            if effectId:
                effs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getEquipEffectLv(),
                 self.getEquipEffectPriority(),
                 self.model,
                 effectId,
                 sfx.EFFECT_LIMIT_MISC))
                if effs:
                    setattr(self, potKeepEffsName, effs)
            if len(item) > 3:
                soundId = item[3]
                gameglobal.rds.sound.playSound(soundId, position=self.position)
            return

    def refreshPotKeepEffect(self):
        potKeepEffInfo = getattr(self, POT_KEEP_EFF_INFO, None)
        if potKeepEffInfo:
            self.playPotKeepEffect(potKeepEffInfo[0], potKeepEffInfo[1])

    def afterModelFinished(self, info, model):
        if not self.inWorld:
            return
        actGroupId = info[1] if len(info) >= 2 else 0
        effectId = info[2] if len(info) >= 3 else 0
        if actGroupId:
            self.oldActGroupId = self.actGroupId
            self.actGroupId = actGroupId
        self.oldModel = self.model
        self.fashion.setupModel(model, False)
        if effectId:
            sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getEquipEffectLv(),
             self.getEquipEffectPriority(),
             model,
             effectId,
             sfx.EFFECT_LIMIT_MISC))

    def dealXJSAct(self, data):
        p = BigWorld.player()
        for beginTime, endTime, act in data:
            if formula.isInXingJiTimeInterval(beginTime, endTime):
                if act:
                    self.faceTo(p) if hasattr(self, 'faceTo') else None
                    self.fashion.playActionSequence(self.model, [str(act)], None)

    def dealXJSPoPo(self, data):
        for beginTime, endTime, dialogId in data:
            if formula.isInXingJiTimeInterval(beginTime, endTime):
                if dialogId:
                    dd = DD.data.get(int(dialogId), {})
                    msg = dd.get('details', '')
                    duration = dd.get('interval', const.POPUP_MSG_SHOW_DURATION)
                    msg and self.topLogo and self.topLogo.setChatMsg(msg, duration)

    def checkTrapEventValid(self, eventData):
        return True

    def playOutEvent(self, trapEvent, trapLengthType):
        trapSoundHandleName = 'trapSoundHandle'
        p = BigWorld.player()
        if trapLengthType != 1:
            trapSoundHandleName = trapSoundHandleName + str(trapLengthType)
        try:
            for item in trapEvent:
                if item[0] in (gameglobal.OUT_ACT_FLAG,):
                    self.faceTo(p) if hasattr(self, 'faceTo') else None
                    acts = [ str(i) for i in item[1:] ]
                    if self.fashion != None:
                        if self.fashion.opacity:
                            self.fashion.playActionSequence(self.model, acts, None)
                elif item[0] == gameglobal.SOUND_FLAG and hasattr(self, trapSoundHandleName):
                    handle = getattr(self, trapSoundHandleName)
                    gameglobal.rds.sound.stopSound(int(item[1]), handle)
                    setattr(self, trapSoundHandleName, None)
                elif item[0] == gameglobal.CHANGE_MODEL_FLAG:
                    if hasattr(self, 'oldActGroupId'):
                        self.actGroupId = self.oldActGroupId
                    if hasattr(self, 'oldModel'):
                        self.fashion.setupModel(self.oldModel)
                elif item[0] == gameglobal.KEEP_EFFECT_FLAG:
                    self.releasePotKeepEffs(trapLengthType)

        except:
            pass

    def releasePotKeepEffs(self, trapLengthType):
        potKeepEffsName = self.getPotKeepEffsName(trapLengthType)
        if hasattr(self, potKeepEffsName):
            effs = getattr(self, potKeepEffsName, None)
            if effs:
                for eff in effs:
                    if eff:
                        eff.stop()

            setattr(self, potKeepEffsName, None)
            setattr(self, POT_KEEP_EFF_INFO, None)

    def dealTrapOutEvent(self, trapLengthType = 1):
        data = self.getItemData()
        eventName = 'trapEvent'
        trapRateTypeName = 'trapRateType'
        if trapLengthType != 1:
            eventName = eventName + str(trapLengthType)
            trapRateTypeName = 'trapRateType' + str(trapLengthType)
        trapPos = trapLengthType - 1
        playIngEvents = self.curPlayIngEvent.get(trapPos)
        if playIngEvents == None or len(playIngEvents) == 0:
            trapEvent = data.get(eventName, [])
            if trapEvent.__class__ == tuple:
                self.playOutEvent(trapEvent, trapLengthType)
            elif trapEvent.__class__ == list:
                rateType = data.get(trapRateTypeName, 0)
                rollPoint = random.uniform(0, 1)
                curRate = 0
                for trapGroup in trapEvent:
                    playRate = trapGroup[0]
                    if playRate.__class__ != int and playRate.__class__ != float:
                        continue
                    if rateType == 0 or rateType == None:
                        if rollPoint < playRate:
                            curPlayIngEvent = trapGroup[1:]
                            self.playOutEvent(curPlayIngEvent, trapLengthType)
                            self.curPlayIngEvent[trapPos] = []
                        rollPoint = random.uniform(0, 1)
                    else:
                        curRate = playRate + curRate
                        if rollPoint < curRate:
                            curPlayIngEvent = trapGroup[1:]
                            self.playOutEvent(curPlayIngEvent, trapLengthType)
                            self.curPlayIngEvent[trapPos] = []
                            return

        else:
            for playIngEvent in playIngEvents:
                self.playOutEvent(playIngEvent, trapLengthType)

        self.curPlayIngEvent[trapPos] = []

    def addTrapEvent(self):
        for i in xrange(1, TRAP_MAX_NUM):
            trapLengthName = 'trapLength'
            trapEventIdName = 'trapEventId'
            if i != 1:
                trapLengthName = trapLengthName + str(i)
                trapEventIdName = trapEventIdName + str(i)
            if not hasattr(self, trapLengthName) or not getattr(self, trapLengthName):
                setattr(self, trapLengthName, self.getItemData().get(trapLengthName, 0))
            trapLength = getattr(self, trapLengthName)
            if trapLength:
                tid = BigWorld.addPot(self.matrix, trapLength, self.trapEventCallback)
                setattr(self, trapEventIdName, tid)

    def delTrapEvent(self):
        for i in xrange(1, TRAP_MAX_NUM):
            trapLengthName = 'trapLength'
            trapEventIdName = 'trapEventId'
            if i != 1:
                trapLengthName = trapLengthName + str(i)
                trapEventIdName = trapEventIdName + str(i)
            if hasattr(self, trapEventIdName):
                trapId = getattr(self, trapEventIdName)
                if trapId != None:
                    BigWorld.delPot(trapId)
                    setattr(self, trapEventIdName, None)
                    setattr(self, trapLengthName, 0)

    def trapEventCallback(self, enteredTrap, handle):
        for i in xrange(1, TRAP_MAX_NUM):
            trapEventIdName = 'trapEventId'
            trapCDName = 'trapCD'
            if i != 1:
                trapEventIdName = trapEventIdName + str(i)
                trapCDName = trapCDName + str(i)
            if hasattr(self, trapEventIdName):
                if handle == getattr(self, trapEventIdName):
                    if self.fashion.opacity:
                        data = self.getItemData()
                        trapCD = data.get(trapCDName, 0)
                        p = BigWorld.player()
                        playerTrapCD = {}
                        if hasattr(p, trapCDName):
                            playerTrapCD = getattr(p, trapCDName)
                        else:
                            setattr(p, trapCDName, {})
                        lastTime = [0, 0]
                        if playerTrapCD == None:
                            setattr(p, trapCDName, {})
                        else:
                            lastTime = playerTrapCD.get(self.id, [0, 0])
                        if trapCD:
                            if utils.getNow() < lastTime[enteredTrap] + trapCD:
                                return
                        lastTime[enteredTrap] = utils.getNow()
                        playerTrapCD[self.id] = lastTime
                        setattr(p, trapCDName, playerTrapCD)
                        if enteredTrap:
                            self.dealTrapInEvent(i)
                        else:
                            self.dealTrapOutEvent(i)
                    elif self.__class__.__name__ in ('Npc', 'MovableNpc') and self._isQuestNpc():
                        self.autoDelQuestNearBy()
                    break
