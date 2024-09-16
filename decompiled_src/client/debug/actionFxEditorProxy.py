#Embedded file name: I:/bag/tmp/tw2/res/entities\client\debug/actionFxEditorProxy.o
import copy
import Sound
import BigWorld
import ResMgr
from guis import uiConst
from Scaleform import GfxValue
import gamelog
import gameglobal
from callbackHelper import Functor
from guis.ui import gbk2unicode
from guis.uiProxy import DataProxy
from guis import uiUtils
from sfx import sfx
list1 = [2,
 5,
 8,
 11]
list2 = [14,
 17,
 20,
 23]
defaultData = [-1,
 -1,
 -1,
 -1,
 -1,
 -1,
 -1,
 -1,
 -1,
 -1,
 -1,
 -1,
 -1,
 -1,
 -1,
 -1,
 -1,
 -1,
 -1,
 -1,
 -1,
 -1,
 -1,
 -1,
 0,
 0]

class ActionFxEditorProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(ActionFxEditorProxy, self).__init__(uiAdapter)
        self.modelMap = {'fileControl': self.fileControl,
         'sceneControl': self.sceneControl,
         'register': self.onRegister,
         'isLoop': self.isLoop,
         'searchFileName': self.searchFileName,
         'chooseActionId': self.chooseActionId,
         'chooseFile': self.chooseFile,
         'remove': self.onRemove,
         'autoSave': self.onAutoSave,
         'playScaleTime': self.playScaleTime}
        self.actionFxXmlName = None
        self.fileNameList = []
        self.actionList = []
        self.eventMgr = EventMgr()
        self.choosedActionId = 0
        self.rootSect = None
        self.fileName = None
        self.attachFx = {}
        self.playSoundList = []
        self.isLoopAction = False
        self.loopAction = False
        self.isPressedStopBtn = False
        self.storeEventList = []
        self.playFxDelayTime = 0
        self.targetPlayer = None
        self.callback = None
        self.fxCallback = []
        self.audioCallback = []
        self.actionCallback = []
        self.storeMacthCaps = [1, 10]

    def showActionFxEditor(self):
        self.uiAdapter.movie.invoke(('_root.loadWidget', GfxValue(uiConst.WIDGET_ACTION_FX)))
        self.scanFile()

    def isLoop(self, *arg):
        isTrue = arg[3][1].GetBool()
        self.isLoopAction = int(isTrue)

    def onRemove(self, *arg):
        isClose = arg[3][0].GetBool()
        self.isPressedStopBtn = isClose
        self.storeEventList = None
        if self.targetPlayer:
            self.reset(self.targetPlayer)

    def onAutoSave(self, *arg):
        dataList = []
        i = 0
        while i < 24:
            if i in list1:
                dataList.append(int(arg[3][i].GetNumber()))
            else:
                dataList.append(arg[3][i].GetNumber())
            i += 1

        choosedActionId = self.choosedActionId
        playTime = arg[3][24].GetNumber()
        isLoop = arg[3][25].GetBool()
        event = self.eventMgr.getEventByIndex(choosedActionId)
        if event:
            dataList1 = []
            dataList1.append(int(isLoop))
            dataList1.append(playTime)
            event.addLoopAction(dataList1[0:])
            event.addFx(dataList[:12])
            event.addAudio(dataList[12:])
        self.saveFile()

    def playScaleTime(self, *arg):
        pass

    def fileControl(self, *arg):
        btnName = arg[3][0].GetString()
        gamelog.debug('@gjd--fileControl-btnName', btnName)
        if btnName == 'saveBtn':
            dataList = []
            i = 1
            while i < 25:
                if i in list1:
                    dataList.append(int(arg[3][i].GetNumber()))
                elif i in list2:
                    dataList.append(arg[3][i].GetString())
                else:
                    dataList.append(arg[3][i].GetNumber())
                i += 1

            choosedActionId = self.choosedActionId
            playTime = arg[3][25].GetNumber()
            isLoop = arg[3][26].GetBool()
            playScale = float(arg[3][27].GetNumber())
            event = self.eventMgr.getEventByIndex(choosedActionId)
            if event:
                dataList1 = []
                dataList1.append(int(isLoop))
                dataList1.append(playTime)
                dataList1.append(playScale)
                event.addLoopAction(dataList1[0:])
                event.addFx(dataList[:12])
                event.addAudio(dataList[12:])
            self.saveFile()
        elif btnName == 'newXmlBtn':
            self.actionFxXmlName = arg[3][1].GetString()
            suc = self.loadXmlData(self.actionFxXmlName, True)
            if suc:
                self.fileNameList.append(self.actionFxXmlName)
                return self.getFileArray()
        elif btnName == 'reloadBtn':
            sfx.gEffectMgr.effectCache.reloadAll()
            ResMgr.purgeAll()
            if self.targetPlayer:
                target = self.targetPlayer
                target.model.reload()
                target.model.reloadAnimCue()

    def sceneControl(self, *arg):
        btnName = arg[3][0].GetString()
        gamelog.debug('@gjd--sceneControl-btnName', btnName)
        if btnName == 'addBtn':
            actionId = arg[3][1].GetString()
            if not actionId:
                return
            self.actionId = actionId
            self.eventMgr.addEvent(self.actionId, self.choosedActionId)
            choosedActionId = self.choosedActionId
            event = self.eventMgr.getEventByIndex1(choosedActionId + 1)
            if event:
                dataList1 = defaultData[24:]
                event.addLoopAction(dataList1[0:])
                event.addFx(defaultData[:12])
                event.addAudio(defaultData[12:24])
            self.saveFile()
            return self.getActionIdArray()
        if btnName == 'deleteBtn':
            idx = self.choosedActionId
            isSuccess, event = self.eventMgr.delActionIdByIndex(idx)
            if isSuccess:
                if isinstance(event, Event):
                    if event.envEvent.has_key('Fx'):
                        fxData = event.envEvent['Fx']
                        self.ActionMC.Invoke('setFxData', uiUtils.array2GfxAarry(fxData))
                    if event.envEvent.has_key('Audio'):
                        audioData = event.envEvent['Audio']
                        self.ActionMC.Invoke('setAudioData', uiUtils.array2GfxAarry(audioData))
                    if event.envEvent.has_key('isLoop'):
                        isLoop = event.envEvent['isLoop']
                        para1 = int(isLoop[0])
                        isLoop1 = [para1, isLoop[1]]
                        self.ActionMC.Invoke('setLoopAndplayTimeData', uiUtils.array2GfxAarry(isLoop1))
                else:
                    self.clearFxAndAudio()
            return self.getActionIdArray()
        if btnName == 'playBtn':
            self.isPressedStopBtn = False
            isPlayer = arg[3][1].GetBool()
            self.clearCallBackList()
            target = BigWorld.player() if isPlayer else BigWorld.player().targetLocked
            target.am.matchCaps = [60]
            self.targetPlayer = target
            eventList = []
            for event in self.eventMgr.eventList:
                eventList.append(event)

            self.playActionByList(eventList, target, False)
        elif btnName == 'loopPlayBtn':
            self.isPressedStopBtn = False
            self.storeEventList = []
            isPlayer = arg[3][1].GetBool()
            self.clearCallBackList()
            target = BigWorld.player() if isPlayer else BigWorld.player().targetLocked
            self.targetPlayer = target
            target.am.matchCaps = [60]
            eventList = []
            for event in self.eventMgr.eventList:
                eventList.append(event)

            self.storeEventList = copy.deepcopy(eventList)
            self.playActionByList(eventList, target, True)
        elif btnName == 'changeBtn':
            curActionId = arg[3][1].GetString()
            self.eventMgr.addEvent1(curActionId, self.choosedActionId)
            self.ActionMC.Invoke('setActionData', self.getActionIdArray())
        elif btnName == 'stopBtn':
            self.isPressedStopBtn = True
            isPlayer = arg[3][1].GetBool()
            target = BigWorld.player() if isPlayer else BigWorld.player().targetLocked
            self.reset(target)

    def reset(self, target):
        target.am.matchCaps = self.storeMacthCaps
        if self.callback:
            BigWorld.cancelCallback(self.callback)
        l = len(self.fxCallback)
        for i in xrange(l):
            BigWorld.cancelCallback(self.fxCallback[i])

        l = len(self.audioCallback)
        for i in xrange(l):
            BigWorld.cancelCallback(self.audioCallback[i])

        l = len(self.actionCallback)
        for i in xrange(l):
            BigWorld.cancelCallback(self.actionCallback[i])

        self.clearCallBackList()
        self.stopModelAction(target.model)
        self.stopFxAndAudio(target)

    def clearCallBackList(self):
        self.fxCallback = []
        self.audioCallback = []
        self.actionCallback = []

    def stopFxAndAudio(self, target):
        if len(self.attachFx.keys()) > 0:
            for key in self.attachFx.keys():
                sfx.detachEffect(target.model, key, self.attachFx[key])
                del self.attachFx[key]

        if self.playSoundList:
            for sound in self.playSoundList:
                self.stopSound(sound)
                self.playSoundList.remove(sound)

    def stopModelAction(self, model):
        gamelog.debug('@gjd1--stopModelAction--model:', model.sources)
        if not hasattr(model, 'queue'):
            return
        actQueue = model.queue
        if len(actQueue) == 0:
            return
        model.unlockSpine()
        for i in actQueue:
            try:
                aq = model.action(i)
                if model.freezeTime <= 0:
                    aq.stop()
            except:
                pass

    def playActionByList(self, eventList, target, isLoopPlay = False):
        self.stopModelAction(target.model)
        gamelog.debug('@gjd--playActionByList-eventList', eventList)
        if self.isPressedStopBtn:
            target.am.matchCaps = self.storeMacthCaps
            return
        if len(eventList) < 1:
            if isLoopPlay:
                eventList = copy.deepcopy(self.storeEventList)
            else:
                self.stopModelAction(target.model)
                self.stopFxAndAudio(target)
                target.am.matchCaps = self.storeMacthCaps
                return
        isLoopAction = False
        childList = eventList.pop(0)
        if not childList:
            target.am.matchCaps = self.storeMacthCaps
            return
        if childList.envEvent.has_key('isLoop'):
            LoopData = childList.envEvent['isLoop']
        else:
            LoopData = [0, 0, 1.0]
        if int(LoopData[0]) == 1:
            isLoopAction = True
        else:
            isLoopAction = False
        if isLoopAction:
            self.playAction(childList, target, eventList, isLoopPlay)
        else:
            actionDuration = LoopData[1]
            actionList = []
            realFxData = []
            realAudioData = []
            actionList.append(childList.actionId)
            event = childList
            actionDurationSingle = target.model.action(event.actionId).duration
            a = target.model.action(event.actionId).track
            gamelog.debug('myTest9---else--event.actionId--actionDurationSingle--track', event.actionId, actionDurationSingle, a)
            if event.envEvent.has_key('Fx'):
                fxData = event.envEvent['Fx']
                siceFxData = fxData[::3]
                realFxData = self.getRealData(siceFxData, fxData)
            if event.envEvent.has_key('Audio'):
                audioData = event.envEvent['Audio']
                siceAudioData = audioData[::3]
                realAudioData = self.getRealData(siceAudioData, audioData)
            if len(realFxData) > 0:
                for item in realFxData:
                    fxHandle = BigWorld.callback(item[0] + actionDuration, Functor(self.playEffect, int(item[1]), target, item[2]))
                    self.fxCallback.append(fxHandle)

            if len(realAudioData) > 0:
                for item in realAudioData:
                    audioHandel = BigWorld.callback(item[0] + actionDuration, Functor(self.playSound, item[1], item[2], target))
                    self.audioCallback.append(audioHandel)

            if actionDuration <= 0:
                actionDuration += actionDurationSingle
            gamelog.debug('myTest9---else--actionList--actionDuration', actionList, actionDuration)
            target.fashion.playActionSequence(target.model, actionList, None, scale=float(LoopData[2]))
            actionHandel = BigWorld.callback(float(actionDuration), Functor(self.playActionByList, eventList, target, isLoopPlay))
            self.actionCallback.append(actionHandel)

    def stopSound(self, soundID):
        Sound.stopFx(soundID)

    def getRealData(self, siceData, Data):
        i = 0
        realData = []
        for it in siceData:
            if int(it) > -1:
                realData.append((Data[i], Data[i + 1], Data[i + 2]))
            i += 3

        return realData

    def playAction(self, childList, target, eventList, isLoopPlay):
        event = childList
        actionList = []
        realFxData = []
        realAudioData = []
        actionList.append(event.actionId)
        gamelog.debug('myTest9---IF-actionList', actionList)
        isLoopData = [1, 0.0, 1.0]
        if event.envEvent.has_key('isLoop'):
            isLoopData = event.envEvent['isLoop']
        if event.envEvent.has_key('Fx'):
            fxData = event.envEvent['Fx']
            siceFxData = fxData[::3]
            realFxData = self.getRealData(siceFxData, fxData)
        if event.envEvent.has_key('Audio'):
            audioData = event.envEvent['Audio']
            siceAudioData = audioData[::3]
            realAudioData = self.getRealData(siceAudioData, audioData)
        if len(realFxData) > 0:
            for item in realFxData:
                fxHandle = BigWorld.callback(item[0], Functor(self.playEffect, int(item[1]), target, item[2]))
                self.fxCallback.append(fxHandle)

        if len(realAudioData) > 0:
            for item in realAudioData:
                audioHandle = BigWorld.callback(item[0], Functor(self.playSound, item[1], item[2], target))
                self.audioCallback.append(audioHandle)

        delayTime = float(isLoopData[1])
        if delayTime:
            actionIsLoop = target.model.action(actionList[0]).loop
            self.playActionSequence(target.model, actionList, None, target)
            target.model.action(actionList[0]).loop = actionIsLoop
            self.callback = BigWorld.callback(delayTime, Functor(self.playActionByList, eventList, target, isLoopPlay))
        else:
            target.fashion.playActionSequence(target.model, actionList, Functor(self.playActionByList, eventList, target, isLoopPlay))

    def playActionSequence(self, model, actions, callback, target, scale = 1, keep = 0, blend = 0, releaseFx = True):
        if len(actions) == 0 or not model or not model.inWorld:
            return
        try:
            act = model.action(actions[0])
            if hasattr(act, 'loop'):
                act.loop = True
            if act.blended:
                act.enableAlpha(blend and (target.inMoving() or target.inRiding()))
        except:
            return

        for i in xrange(len(actions) - 1):
            if act != None:
                try:
                    act = getattr(act(0, None, 0, scale, keep), actions[i + 1])
                    if act.blended:
                        act.enableAlpha(blend and (target.inMoving() or target.inRiding()))
                except:
                    return

        if act != None:
            act(0, callback, 0, scale, keep)

    def playEffect(self, effId, target, maxDelayTime):
        gamelog.debug('myTest---effId,maxDelayTime:', effId, maxDelayTime)
        lv = BigWorld.player().getBasicEffectLv()
        priority = BigWorld.player().getBasicEffectPriority()
        fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (lv,
         priority,
         target.model,
         effId,
         sfx.EFFECT_UNLIMIT,
         maxDelayTime))
        if fxs:
            self.attachFx[effId] = fxs

    def playSound(self, soundpath, delayTime, target):
        gamelog.debug('myTest2---playSound--soundpath:', soundpath)
        soundValue = Sound.playFx(soundpath, 0, target.position, True, None, 1.0)
        self.playSoundList.append(soundValue)

    def saveFile(self):
        self.rootSect.deleteSection('Event')
        eventSect = self.rootSect.createSection('Event')
        self.eventMgr.save(eventSect)
        self.rootSect.save()

    def chooseActionId(self, *arg):
        self.choosedActionId = int(arg[3][0].GetNumber())
        event = Event()
        event = self.eventMgr.eventList[self.choosedActionId]
        if event.envEvent.has_key('Fx'):
            fxData = event.envEvent['Fx']
            self.ActionMC.Invoke('setFxData', uiUtils.array2GfxAarry(fxData))
        else:
            self.ActionMC.Invoke('setFxData', self.getNullObject())
        if event.envEvent.has_key('Audio'):
            audioData = event.envEvent['Audio']
            self.ActionMC.Invoke('setAudioData', uiUtils.array2GfxAarry(audioData))
        else:
            self.ActionMC.Invoke('setAudioData', self.getNullObject())
        if event.envEvent.has_key('isLoop'):
            isLoop = event.envEvent['isLoop']
            para1 = int(isLoop[0])
            isLoop1 = [para1, isLoop[1], isLoop[2]]
            self.ActionMC.Invoke('setLoopAndplayTimeData', uiUtils.array2GfxAarry(isLoop1))
        else:
            self.ActionMC.Invoke('setLoopAndplayTimeData', self.getNullObject1())

    def chooseFile(self, *arg):
        self.clear()
        fileName = arg[3][0].GetString()
        if fileName.endswith('.xml'):
            self.fileName = fileName[:-4]
        else:
            self.fileName = fileName
        self.loadXmlData(self.fileName, True)
        self.ActionMC.Invoke('setActionData', self.getActionIdArray())
        self.ActionMC.Invoke('setActionIdCanEdit', GfxValue(True))

    def clear(self):
        self.rootSect = None
        self.eventMgr.release()
        self.ActionMC.Invoke('setActionData', self.getNullObject())
        self.ActionMC.Invoke('setFxData', self.getNullObject())
        self.ActionMC.Invoke('setAudioData', self.getNullObject())

    def clearFxAndAudio(self):
        self.ActionMC.Invoke('setFxData', self.getNullObject())
        self.ActionMC.Invoke('setAudioData', self.getNullObject())

    def getNullObject(self):
        ar = self.movie.CreateArray()
        for i in xrange(12):
            ar.SetElement(i, GfxValue(-1))

        return ar

    def getNullObject1(self):
        ar = self.movie.CreateArray()
        return ar

    def scanActionIdList(self):
        self.actionList = []
        eList = self.eventMgr.eventList
        for e in eList:
            self.actionList.append(str(e.actionId))

    def getActionIdArray(self):
        i = 0
        ar = self.movie.CreateArray()
        self.scanActionIdList()
        for item in self.actionList:
            value = GfxValue(gbk2unicode(self.actionList[i]))
            ar.SetElement(i, value)
            i = i + 1

        return ar

    def onRegister(self, *arg):
        self.ActionMC = arg[3][0]

    def loadXmlData(self, oldName, mustExist = False):
        name = 'intro/debugskill/' + oldName + '.xml'
        ResMgr.purge(name)
        sect = ResMgr.openSection(name)
        if sect is None:
            if mustExist:
                sect = ResMgr.root.createSection(name)
                sect.save()
            else:
                return False
        self.rootSect = sect
        eventSect = sect.openSection('Event')
        if eventSect:
            self.eventMgr.load(eventSect)
        return True

    def searchFileName(self, *arg):
        prefix = arg[3][0].GetString()
        if prefix == '':
            return self.getFileArray()
        ret = []
        for item in self.fileNameList:
            if item.find(prefix) != -1:
                ret.append(item)

        return uiUtils.array2GfxAarry(ret, True)

    def getFileArray(self):
        i = 0
        ar = self.movie.CreateArray()
        if not self.fileNameList:
            self.scanFile()
        for item in self.fileNameList:
            value = GfxValue(gbk2unicode(self.fileNameList[i]))
            ar.SetElement(i, value)
            i = i + 1

        return ar

    def scanFile(self):
        curPath = ['intro/debugskill/']
        for p in curPath:
            folderSection = ResMgr.openSection(p)
            if folderSection:
                for i in folderSection.keys():
                    i = i.lower()
                    if i.endswith('.xml'):
                        self.fileNameList.append(i)


class Event(object):

    def __init__(self):
        super(Event, self).__init__()
        self.envEvent = {}
        self.actionId = 0
        self.loopAction = 0
        self.loopPlayTime = 0

    def addLoopAction(self, dataList):
        if not self.envEvent.has_key('isLoop'):
            self.envEvent['isLoop'] = [0, 0.0, 1.0]
        self.envEvent['isLoop'] = dataList

    def addFx(self, data):
        if not self.envEvent.has_key('Fx'):
            self.envEvent['Fx'] = []
        self.envEvent['Fx'] = data

    def release(self):
        pass

    def addAudio(self, data):
        if not self.envEvent.has_key('Audio'):
            self.envEvent['Audio'] = []
        self.envEvent['Audio'] = data

    def load(self, actionIdSect):
        self.actionId = actionIdSect.readString('id')
        fxSect = actionIdSect.openSection('Fx')
        if fxSect:
            self.envEvent['Fx'] = []
            fxMetaData1 = fxSect.readString('1').split(',')
            fxMetaData2 = fxSect.readString('2').split(',')
            fxMetaData3 = fxSect.readString('3').split(',')
            fxMetaData4 = fxSect.readString('4').split(',')
            self.envEvent['Fx'] = [float(fxMetaData1[0]),
             float(fxMetaData1[1]),
             float(fxMetaData1[2]),
             float(fxMetaData2[0]),
             float(fxMetaData2[1]),
             float(fxMetaData2[2]),
             float(fxMetaData3[0]),
             float(fxMetaData3[1]),
             float(fxMetaData3[2]),
             float(fxMetaData4[0]),
             float(fxMetaData4[1]),
             float(fxMetaData4[2])]
        audioSect = actionIdSect.openSection('Audio')
        if audioSect:
            self.envEvent['Audio'] = {}
            audioMetaData1 = audioSect.readString('1').split(',')
            audioMetaData2 = audioSect.readString('2').split(',')
            audioMetaData3 = audioSect.readString('3').split(',')
            audioMetaData4 = audioSect.readString('4').split(',')
            self.envEvent['Audio'] = [float(audioMetaData1[0]),
             audioMetaData1[1],
             float(audioMetaData1[2]),
             float(audioMetaData2[0]),
             audioMetaData2[1],
             float(audioMetaData2[2]),
             float(audioMetaData3[0]),
             audioMetaData3[1],
             float(audioMetaData3[2]),
             float(audioMetaData4[0]),
             audioMetaData4[1],
             float(audioMetaData4[2])]
        playTimeData = actionIdSect.readString('isLoop')
        if playTimeData:
            audioData = playTimeData.split(',')
            self.envEvent['isLoop'] = [audioData[0], audioData[1], audioData[2]]


class EventMgr(object):

    def __init__(self):
        self.eventListOld = []
        self.eventList = []

    def addEvent(self, actionId, choosedActionId):
        event = Event()
        event.actionId = actionId
        self.eventList.insert(choosedActionId + 1, event)

    def addEvent1(self, actionId, choosedActionId):
        event = Event()
        event.actionId = actionId
        self.eventList[choosedActionId] = event

    def getEventByIndex(self, idx):
        if len(self.eventList) > idx:
            return self.eventList[idx]

    def getEventByIndex1(self, idx):
        if len(self.eventList) == 0:
            return self.eventList[idx - 1]
        if len(self.eventList) > idx:
            return self.eventList[idx]

    def delActionIdByIndex(self, idx):
        nextEvent = []
        if len(self.eventList) > idx:
            if len(self.eventList) == 1:
                self.eventList.pop(idx)
            elif len(self.eventList) == idx + 1:
                nextEvent = self.eventList[idx - 1]
                self.eventList.pop(idx)
            else:
                nextEvent = self.eventList[idx + 1]
                self.eventList.pop(idx)
            return (True, nextEvent)
        else:
            return (False, nextEvent)

    def release(self):
        for event in self.eventList:
            event.release()

        self.eventList = []

    def getNullObjectEvent(self):
        ar = self.movie.CreateArray()
        return ar

    def load(self, eventSect):
        for actionSect in eventSect.values():
            event = Event()
            event.load(actionSect)
            self.eventList.append(event)

    def save(self, eventSect):
        for event in self.eventList:
            actionIDSect = eventSect.createSection('ActionID')
            actionIDSect.writeString('id', '%s' % event.actionId)
            if len(event.envEvent) > 0:
                fxsect = actionIDSect.createSection('Fx')
                envEff = event.envEvent.get('Fx', None)
                if envEff:
                    list1 = envEff[:3]
                    list2 = envEff[3:6]
                    list3 = envEff[6:9]
                    list4 = envEff[9:12]
                    fxsect.writeString('1', ','.join([ '%s' % x for x in list1 ]))
                    fxsect.writeString('2', ','.join([ '%s' % x for x in list2 ]))
                    fxsect.writeString('3', ','.join([ '%s' % x for x in list3 ]))
                    fxsect.writeString('4', ','.join([ '%s' % x for x in list4 ]))
                audioSect = actionIDSect.createSection('Audio')
                audioData = event.envEvent.get('Audio', None)
                if audioData:
                    list5 = audioData[:3]
                    list6 = audioData[3:6]
                    list7 = audioData[6:9]
                    list8 = audioData[9:12]
                    audioSect.writeString('1', ','.join([ '%s' % x for x in list5 ]))
                    audioSect.writeString('2', ','.join([ '%s' % x for x in list6 ]))
                    audioSect.writeString('3', ','.join([ '%s' % x for x in list7 ]))
                    audioSect.writeString('4', ','.join([ '%s' % x for x in list8 ]))
                playTimeData = event.envEvent.get('isLoop')
                if playTimeData:
                    if len(playTimeData) < 3:
                        playTimeData.append(1.0)
                    actionIDSect.writeString('isLoop', '%s,%s,%s' % (playTimeData[0], playTimeData[1], playTimeData[2]))
