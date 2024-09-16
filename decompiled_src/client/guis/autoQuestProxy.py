#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/autoQuestProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import const
import gamelog
import clientcom
from ui import gbk2unicode
from uiProxy import UIProxy
from helpers import capturePhoto
from guis import uiUtils
from data import item_data as ID
from data import npc_model_client_data as NMCD
from data import quest_data as QD
from data import quest_loop_data as QLD
from cdata import font_config_data as FCD
from data import dialogs_data as DD

class AutoQuestProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(AutoQuestProxy, self).__init__(uiAdapter)
        self.taskInfo = []
        self.modelMap = {'getAutoQuestInfo': self.onGetAutoQuestInfo,
         'setUnitType': self.onSetUnitType,
         'setUnitIndex': self.onSetUnitIndex,
         'clickFieldEvent': self.onClickFieldEvent}
        self.speakEvents = {}
        self.headGen = None
        self.isNPC = True
        self.isAccept = True
        self.target = None
        self.mediator = None
        self.destroyOnHide = True
        self.simpleWord = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_AUTO_QUEST, self.hide)
        uiAdapter.registerEscFunc(uiConst.WIDGET_SMALL_AUTO_QUEST, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId in (uiConst.WIDGET_AUTO_QUEST, uiConst.WIDGET_SMALL_AUTO_QUEST):
            self.mediator = mediator
            if widgetId == uiConst.WIDGET_AUTO_QUEST:
                self.initHeadGen()
            else:
                self.initFubenHeadGen()
            if hasattr(self.uiAdapter, 'tdHeadGen') and self.uiAdapter.tdHeadGen.headGenMode:
                self.uiAdapter.tdHeadGen.startCapture()

    def openQuestWindow(self, taskInfo = None, target = None, isAccept = True, isNPC = True):
        gamelog.debug('openQuestWindow', taskInfo)
        if gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
            return
        questNum = 0
        for value in taskInfo.itervalues():
            if isinstance(value, list):
                questNum += len(value)

        if questNum == 0:
            return
        self.clearWidget()
        self.isAccept = isAccept
        self.isNPC = isNPC
        self.speakEvents = {}
        self.taskInfo = taskInfo
        self.target = target
        self.uiAdapter.loadWidget(uiConst.WIDGET_AUTO_QUEST)

    def onGetAutoQuestInfo(self, *arg):
        if self.simpleWord:
            return uiUtils.dict2GfxDict(self.simpleWord, True)
        elif self.taskInfo == None:
            self.hide()
            return
        else:
            movie = self.movie
            obj = movie.CreateObject()
            obj.SetMember('chat', GfxValue(gbk2unicode(self.taskInfo.get('chat', ''))))
            atArray = self.setTaskArray('available_tasks')
            utArray = self.setTaskArray('unfinished_tasks')
            ctArray = self.setTaskArray('complete_tasks')
            atlArray = self.setTaskArray('available_taskLoops', True)
            utlArray = self.setTaskArray('unfinished_taskLoops', True)
            ctlArray = self.setTaskArray('complete_taskLoops', True)
            obj.SetMember('available_tasks', atArray)
            obj.SetMember('unfinished_tasks', utArray)
            obj.SetMember('complete_tasks', ctArray)
            obj.SetMember('available_taskLoops', atlArray)
            obj.SetMember('unfinished_taskLoops', utlArray)
            obj.SetMember('complete_taskLoops', ctlArray)
            return obj

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_AUTO_QUEST)
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SMALL_AUTO_QUEST)
        self.resetHeadGen()

    def reset(self):
        self.taskInfo = None
        self.target = None
        self.isAccept = True
        self.mediator = None
        self.simpleWord = None

    def takePhoto3D(self, npcId):
        if not self.headGen:
            self.headGen = capturePhoto.SmallPhotoGen.getInstance('gui/taskmask.tga', 300)
        uiUtils.takePhoto3D(self.headGen, self.target, npcId, True)

    def resetHeadGen(self):
        if self.headGen:
            self.headGen.endCapture()
            self.headGen = None

    def initHeadGen(self):
        if not self.headGen:
            self.headGen = capturePhoto.SmallPhotoGen.getInstance('gui/taskmask.tga', 300)
        self.headGen.initFlashMesh()

    def initFubenHeadGen(self):
        if not self.headGen:
            self.headGen = capturePhoto.FubenSmallPhotoGen.getInstance('gui/taskmask.tga', 300)
        self.headGen.initFlashMesh()

    def onSetUnitType(self, *arg):
        npcId = int(arg[3][0].GetString())
        gamelog.debug('wy:onSetUnitType', npcId)
        self.takePhoto3D(npcId)

    def onSetUnitIndex(self, *arg):
        cata = arg[3][0].GetString()
        curTaskIdx = int(arg[3][1].GetString())
        index = int(arg[3][2].GetString())
        gamelog.debug('onSetUnitIndex', cata, curTaskIdx, index)
        if not self.speakEvents or not self.speakEvents.has_key(cata) or curTaskIdx >= len(self.speakEvents[cata]):
            return
        else:
            if index >= len(self.speakEvents[cata][curTaskIdx]):
                index = len(self.speakEvents[cata][curTaskIdx]) - 1
            data = self.speakEvents[cata][curTaskIdx][index]
            gamelog.debug('wy:onSetUnitIndex', data)
            if data == 0:
                return
            for info in data:
                if info[0] == gameglobal.ACT_FLAG and self.target.inWorld:
                    acts = [ str(i) for i in info[1:] ]
                    self.target.fashion.playActionSequence(self.target.model, acts, None)
                elif info[0] == gameglobal.VOICE_FLAG:
                    gameglobal.rds.sound.playSound(int(info[1]))

            return

    def setTaskArray(self, typeName, isLoop = False):
        taskArr = self.taskInfo.get(typeName, {})
        ret = self.movie.CreateArray()
        gamelog.debug('wy:setTaskArray', taskArr)
        self.speakEvents[typeName] = []
        for i, item in enumerate(taskArr):
            if item.get('speakEvents', None):
                self.speakEvents[typeName].append(item.get('speakEvents', None))
            gamelog.debug('wy:setTaskArray', item, self.speakEvents)
            objat = self.movie.CreateObject()
            objat.SetMember('name', GfxValue(gbk2unicode(item['name'])))
            if isLoop:
                questId = item['questLoopId']
                objat.SetMember('id', GfxValue(item['questLoopId']))
                objat.SetMember('randType', GfxValue(QLD.data[item['questLoopId']].get('ranType', 1)))
            else:
                questId = item['id']
                objat.SetMember('id', GfxValue(item['id']))
            wordList = self.movie.CreateArray()
            k = 0
            if self.isNPC:
                for it in item['words']:
                    wordList.SetElement(k, GfxValue(gbk2unicode(it)))
                    k += 1

            else:
                nameStr = item['words']
                wordList.SetElement(k, GfxValue(gbk2unicode(nameStr)))
            objat.SetMember('words', wordList)
            if item.has_key('expBonus') and item.has_key('goldBonus'):
                objat.SetMember('expBonus', GfxValue(int(item['expBonus'])))
                objat.SetMember('goldBonus', GfxValue(int(item['goldBonus'])))
            else:
                cash = BigWorld.player().getQuestData(item['id'], const.QD_QUEST_CASH)
                if cash is None:
                    cash = 0
                expBonus = BigWorld.player().getQuestData(item['id'], const.QD_QUEST_EXP)
                if expBonus is None:
                    expBonus = 0
                objat.SetMember('expBonus', GfxValue(int(expBonus)))
                objat.SetMember('goldBonus', GfxValue(int(cash)))
            rewardList = self.movie.CreateArray()
            k = 0
            for it in item['rewardChoice']:
                ii = ID.data.get(it[0], {})
                ar = self.movie.CreateArray()
                ar.SetElement(0, GfxValue(uiConst.ITEM_ICON_IMAGE_RES_40 + str(ii.get('icon', 'notFound')) + '.dds'))
                ar.SetElement(1, GfxValue(it[1]))
                quality = ii.get('quality', 1)
                color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                ar.SetElement(2, GfxValue(color))
                rewardList.SetElement(k, ar)
                k += 1

            objat.SetMember('reward', rewardList)
            mRewardList = self.movie.CreateArray()
            k = 0
            for it in item['rewardItems']:
                ii = ID.data.get(it[0], {})
                ar = self.movie.CreateArray()
                ar.SetElement(0, GfxValue(uiConst.ITEM_ICON_IMAGE_RES_40 + str(ii.get('icon', 'notFound')) + '.dds'))
                ar.SetElement(1, GfxValue(it[1]))
                quality = ii.get('quality', 1)
                color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                ar.SetElement(2, GfxValue(color))
                mRewardList.SetElement(k, ar)
                k += 1

            nameArr = self.movie.CreateArray()
            idArr = self.movie.CreateArray()
            if self.isNPC:
                k = 0
                for it in item['speaker_ids']:
                    if it == 0:
                        nameArr.SetElement(k, GfxValue(gbk2unicode(BigWorld.player().realRoleName)))
                    else:
                        nameArr.SetElement(k, GfxValue(gbk2unicode(NMCD.data[it]['name'])))
                    idArr.SetElement(k, GfxValue(it))
                    k += 1

            else:
                nameArr.SetElement(k, GfxValue(gbk2unicode(ID.data.get(self.target, {}).get('name', ''))))
            asideId = self.movie.CreateArray()
            for k, it in enumerate(item['aside']):
                asideId.SetMember(k, GfxValue(it))

            interval = self.movie.CreateArray()
            for k, it in enumerate(item['interval']):
                interval.SetMember(k, GfxValue(it))

            if isLoop:
                qd = QLD.data.get(questId, {})
            else:
                qd = QD.data.get(questId, {})
            questName = qd.get('name', '')
            questDesc = qd.get('desc', '')
            gamelog.debug('questName', questName, questDesc)
            objat.SetMember('speakerName', nameArr)
            objat.SetMember('asideIds', asideId)
            objat.SetMember('interval', interval)
            objat.SetMember('mReward', mRewardList)
            objat.SetMember('idList', idArr)
            objat.SetMember('questName', GfxValue(gbk2unicode(questName)))
            objat.SetMember('questDesc', GfxValue(gbk2unicode(questDesc)))
            ret.SetElement(i, objat)

        return ret

    def isShow(self):
        if self.mediator:
            return True
        return False

    def onClickFieldEvent(self, *arg):
        eventDesc = arg[3][0].GetString()
        eventData = arg[3][1].GetString()
        if eventDesc == 'NpcTk':
            uiUtils.findPosById(eventData)

    def show(self, msg, npcId, duration, normalSize = True, target = None):
        if self.mediator:
            self.hide()
        roleName = ''
        p = clientcom.getPlayerAvatar()
        if npcId:
            roleName = uiUtils.getNpcName(npcId, '')
        elif p:
            roleName = p.realRoleName
        self.simpleWord = {'chat': '',
         'roleName': '',
         'available_tasks': [],
         'unfinished_tasks': [],
         'complete_tasks': [{'id': 1,
                             'idList': [npcId],
                             'asideIds': [0],
                             'interval': [duration],
                             'name': '',
                             'words': [msg],
                             'goldBonus': 0,
                             'expBonus': 0,
                             'mReward': [],
                             'reward': [],
                             'speakerName': [roleName],
                             'questName': '',
                             'questDesc': ''}],
         'available_taskLoops': [],
         'unfinished_taskLoops': [],
         'complete_taskLoops': [],
         'scale': 1}
        self.target = target
        if normalSize:
            self.uiAdapter.loadWidget(uiConst.WIDGET_AUTO_QUEST)
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SMALL_AUTO_QUEST)

    def openDirectly(self, npcId, chatId, normalSize = True):
        dd = DD.data.get(chatId, {})
        msg = dd.get('details', '')
        duration = dd.get('interval', 5)
        self.show(msg, npcId, duration, normalSize)
