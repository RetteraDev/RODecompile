#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/npcV2Proxy.o
from gamestrings import gameStrings
import BigWorld
import os
import gameglobal
from appSetting import Obj as AppSettings
import keys
import uiConst
import events
import const
import questTypeConst
import commQuest
import gametypes
import utils
import gamelog
import ui
from uiProxy import UIProxy
from gameStrings import gameStrings
from item import Item
from guis import uiUtils
from guis import messageBoxProxy
from guis import hotkeyProxy
from guis import hotkey as HK
from callbackHelper import Functor
from helpers import capturePhoto
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis.asObject import TipManager
from data import game_msg_data as GMD
from data import quest_data as QD
from data import fame_data as FD
from data import item_data as ID
from data import bonus_data as BD
from data import npc_model_client_data as NCD
from data import formula_client_data as FMLCD
from data import message_desc_data as MSGDD
from data import quest_loop_data as QLD
from data import npc_data as ND
from data import dawdler_data as DRD
from cdata import game_msg_def_data as GMDD
from cdata import quest_reward_data as QRD
from cdata import font_config_data as FCD
SWF_W = 1920.0
SWF_H = 1080.0
QUEST_BG_HEIGHT = 200
QUEST_MC_POSY = 400
MAX_NPC_NUM = 4
MAX_FUNC_NUM = 6
INTERVAL = 3
PLAY_NORMAL = 1
PLAY_SPEED = 2
PLAY_AUTO = 3
STATE_PLAY = 1
STATE_PAUSE = 0
POS_X = 23
BASE_REWARD_POS_X = [23, 159]
ITEM_REWARD_POS_X = [23,
 100,
 177,
 254]
TASK_TYPE = ['available_tasks',
 'unfinished_tasks',
 'complete_tasks',
 'available_taskLoops',
 'unfinished_taskLoops',
 'complete_taskLoops']
TASK_LOOP = [False,
 False,
 False,
 True,
 True,
 True]
BONUS_TYPE = {22: gameStrings.TEXT_NPCV2PROXY_64,
 21: gameStrings.TEXT_NPCV2PROXY_64_1,
 3: gameStrings.TEXT_NPCV2PROXY_64_2,
 4: gameStrings.TEXT_LIFESKILLFACTORY_1673,
 5: gameStrings.TEXT_NPCV2PROXY_64_3,
 6: gameStrings.TEXT_NPCV2PROXY_64_4}
NPC_ICON_PATH = 'npcHeadIcon/%d.dds'
KEYCODE_SPACE = 32
KEYCODE_1 = 49
KEYCODE_C = 67
KEYCODE_F = 70
KEYCODE_R = 82
KEYCODE_T = 84
KEYCODE_Z = 90
KEYCODE_NUMS_1 = 97
WHEEL_OFFSET = 750

class NpcV2Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NpcV2Proxy, self).__init__(uiAdapter)
        self.mc = []
        self.npcType = uiConst.NPC_QUEST
        self.npcAnimList = []
        self.selfAnimList = []
        self.exists = set([])
        self.noExists = set([])
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_NPC_V2, self.onClickExitBtn)

    def reset(self):
        self.isShow = False
        self.isQuest = False
        self.widget = None
        self.callback = None
        self.closeCallback = None
        self.spaceCallback = None
        self.idx2Func = {}
        self.largeHead = None
        self.twiceCheckBox = 0
        self.chooseRewardMsgBoxId = None
        self.questMc = None
        self.spaceCondition = False
        self.delta = 0
        self.start = 0
        self.end = -1
        self.interval = INTERVAL
        self.remainTime = 0
        self.time = 0
        self.wheelOffset = 0
        self.headId2Slots = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_NPC_V2:
            self.widget = widget
            self.initUI()

    def initUI(self):
        if not self.widget:
            return
        if hasattr(self.uiAdapter, 'tdHeadGen') and self.uiAdapter.tdHeadGen.headGenMode:
            if self.uiAdapter.tdHeadGen.headGen:
                self.uiAdapter.tdHeadGen.headGen.initFlashMesh()
            self.uiAdapter.tdHeadGen.startCapture()
            for i in xrange(MAX_NPC_NUM):
                npcSlot = getattr(self.widget.bottom.chatWindow, 'npcSlot%d' % i)
                if i:
                    npcSlot.visible = False
                else:
                    npcSlot.gotoAndStop('up')
                    self.loadImage(npcSlot.icon.photo2D, 629263)

            return
        self.setKeyDesc()
        self.registerEventListener()
        self.initVisible()
        self.initHeadGen()
        self.questMc = self.widget.right.quest
        if self.npcType == uiConst.NPC_QUEST:
            self.initQuestData()
            self.initAnimData()
            self.initQuest()
        elif self.npcType == uiConst.NPC_FUNC:
            self.initFunc()
        elif self.npcType == uiConst.NPC_DEBATE:
            self.initDebate()
        elif self.npcType == uiConst.NPC_MULTI:
            self.initMulti()
        elif self.npcType == uiConst.NPC_TELEPORT:
            self.initTeleport()
        elif self.npcType == uiConst.NPC_TOWER:
            self.initTower()
        elif self.npcType == uiConst.NPC_FUNC_DIRECTLY:
            self.initFuncDirectly()
        elif self.npcType == uiConst.NPC_PRIZE:
            self.initPrize()
        elif self.npcType == uiConst.NPC_EXPLAIN:
            self.initExplain()
        elif self.npcType == uiConst.NPC_AWARD:
            self.initAward()
        elif self.npcType == uiConst.NPC_FUBEN_DIFFICULTY:
            self.initFubenDifficulty()
        elif self.npcType == uiConst.NPC_FAME_SALARY:
            self.initFameSalary()
        elif self.npcType == uiConst.NPC_BUSINESS_SPY:
            self.initBusinessSpy()

    def setKeyDesc(self):
        ctrlBtnGroup = self.widget.bottom.controlBtnGroup
        HK_DATA = [{'index': HK.KEY_PICK_ITEM,
          'mc': [ctrlBtnGroup.nextBtn]}, {'index': HK.KEY_NPCV2_SPEED,
          'mc': [ctrlBtnGroup.speedBtn, ctrlBtnGroup.normalBtn]}, {'index': HK.KEY_NPCV2_QUICK,
          'mc': [ctrlBtnGroup.quickBtn]}]
        for data in HK_DATA:
            key, mod, desc = hotkeyProxy.getAsKeyContent(data['index'])
            if desc:
                for mc in data['mc']:
                    TipManager.addTip(mc, desc)

    def loadNpcPhoto(self, mc, npcId):
        npcData = NCD.data.get(npcId, {})
        if npcData.has_key('npcHeadIcon'):
            npcHeadIcon = npcData.get('npcHeadIcon', 0)
            mc.loadImage('npcHeadIcon/%s.dds' % npcHeadIcon)
        else:
            modelId = NCD.data.get(npcId, {}).get('model', 0)
            self.loadImage(mc, modelId)

    def loadImage(self, mc, modelId):
        if modelId in self.exists:
            mc.loadImage(NPC_ICON_PATH % modelId)
        elif modelId in self.noExists:
            mc.loadImage(NPC_ICON_PATH % -1)
        else:
            BigWorld.ayncFileExist('gui/%s' % (NPC_ICON_PATH % modelId), Functor(self.checkImageExist, mc, modelId))

    def checkImageExist(self, mc, modelId, isExist):
        if not self.widget:
            return
        if isExist and modelId not in self.exists:
            self.exists.add(modelId)
        elif not isExist and modelId not in self.noExists:
            self.noExists.add(modelId)
            modelId = -1
        mc.loadImage(NPC_ICON_PATH % modelId)

    def enableLargePhotoSize(self):
        return '64Bit' in BigWorld.getOSDesc() and gameglobal.rds.configData.get('enableLargePhotoSize', True)

    def initHeadGen(self):
        size = 1014
        if self.enableLargePhotoSize():
            size = 1920
        self.largeHead = capturePhoto.NpcV2LargePhotoGen.getInstance('gui/taskmask.tga', size, 1014)
        self.largeHead.initFlashMesh()

    def initVisible(self):
        bottomMc = self.widget.bottom
        bottomMc.controlBtnGroup.visible = False
        bottomMc.controlBtnGroup.playBtn.visible = False
        bottomMc.controlBtnGroup.normalBtn.visible = False
        for i in xrange(MAX_NPC_NUM):
            npcSlot = getattr(bottomMc.chatWindow, 'npcSlot%d' % i)
            npcSlot.visible = False

        if bottomMc.chatWindow.cutSlot:
            bottomMc.chatWindow.cutSlot.visible = False
        rightMc = self.widget.right
        rightMc.chatHistory.visible = False
        rightMc.funcBtnList.visible = False
        rightMc.quest.visible = False
        rightMc.commonBtn.visible = False
        self.widget.rightBg.visible = False

    def removeChild(self, questMc):
        if not questMc:
            return
        for i in xrange(len(self.mc) - 1, -1, -1):
            questMc.removeChild(self.mc[i])

        self.mc = []

    def initDebate(self, info = None):
        questMc = self.widget.right.quest
        questMc.y = QUEST_MC_POSY
        if info:
            self.removeChild(questMc)
        else:
            info = self.uiAdapter.debate.onGetDebateInfoPy()
        bottomMc = self.widget.bottom
        bottomMc.chatWindow.chatContent.htmlText = info['chat']
        bottomMc.chatWindow.chatName.text = info['roleName']
        questMc.visible = True
        questMc.questName.text = info['title']
        questMc.questDesc.text = ''
        questMc.btn.visible = False
        posY = questMc.questName.y + questMc.questName.height + 20
        self.debate = []
        self.debateOptionMap = []
        if info['debateOptions']:
            for i in xrange(len(info['debateOptions'])):
                item = self.widget.getInstByClsName('NpcV2_Selection')
                if info['debateType'] == 1:
                    item.radioBox.visible = False
                else:
                    item.radioIcon.visible = False
                item.textMc.textField.text = info['debateOptions'][i]['name']
                item.textMc.textField.height = item.textMc.textField.textHeight + 5
                item.radio.height = item.textMc.textField.height + 5
                item.radioBox.y = (item.radio.height - item.radioBox.height) / 2 + item.radio.y + 1
                item.radioIcon.y = (item.radio.height - item.radioIcon.height) / 2 + item.radio.y + 1
                ASUtils.setHitTestDisable(item.textMc, True)
                item.idx = i
                item.debateType = info['debateType']
                item.x = POS_X
                item.y = posY
                item.addEventListener(events.MOUSE_CLICK, self.onClickDebateBtn, False, 0, True)
                posY += item.height + 10
                questMc.addChild(item)
                self.debateOptionMap.append(info['debateOptions'][i]['res'])
                self.debate.append(item)
                self.mc.append(item)

        npc = BigWorld.entity(info['npcId'])
        uiUtils.takePhoto3D(self.largeHead, npc, npc.npcId)
        self.updateQuestPanelPos(posY, 320)
        if self.checkAutoQuest():
            self.speed = PLAY_AUTO
            if self.debate:
                BigWorld.callback(self.interval / self.speed, Functor(self.clickDebateBtn, self.debate[0]))

    def clickDebateBtn(self, mc):
        if not self.widget:
            return
        if mc.debateType == 2:
            for i in xrange(len(self.debate)):
                if self.debate[i].idx == mc.idx:
                    self.debate[i].radio.selected = True
                    self.debate[i].radioBox.selected = True
                else:
                    self.debate[i].radio.selected = False
                    self.debate[i].radioBox.selected = False

            return
        idx = self.debateOptionMap[mc.idx]
        info = self.uiAdapter.debate.onGetDebateInfoPy(idx)
        if info:
            self.initDebate(info)

    def onClickDebateBtn(self, *args):
        e = ASObject(args[3][0])
        self.clickDebateBtn(e.currentTarget)

    def initFubenDifficulty(self):
        info = self.uiAdapter.funcNpc.onGetFubenDifficultyPy()
        bottomMc = self.widget.bottom
        bottomMc.chatWindow.chatContent.htmlText = info['chat']
        bottomMc.chatWindow.chatName.text = info['roleName']
        questMc = self.widget.right.quest
        questMc.visible = True
        questMc.questName.text = info['title']
        questMc.questDesc.text = ''
        questMc.btn.visible = False
        posY = questMc.questName.y + questMc.questName.height + 20
        if info['options']:
            for i in xrange(len(info['options'])):
                item = self.widget.getInstByClsName('NpcV2_NormalButton')
                item.option = int(info['options'][i])
                item.selected = item.option == int(info['currentMode'])
                item.label = info['optionNames'][item.option]
                item.enabled = item.option <= int(info['currentMode'])
                item.x = POS_X
                item.y = posY
                item.addEventListener(events.MOUSE_CLICK, self.onClickFubenDifficultyBtn, False, 0, True)
                posY += item.height + 10
                questMc.addChild(item)
                self.mc.append(item)

        npc = BigWorld.entity(info['npcId'])
        uiUtils.takePhoto3D(self.largeHead, npc, npc.npcId)
        self.updateQuestPanelPos(posY)

    def onClickFubenDifficultyBtn(self, *args):
        e = ASObject(args[3][0])
        self.uiAdapter.npcPanel.chooseDifficulty(e.currentTarget.option)

    def initBusinessSpy(self):
        info = self.uiAdapter.funcNpc.onGetBusinessSpyInfoPy()
        bottomMc = self.widget.bottom
        bottomMc.chatWindow.chatContent.htmlText = info['chat']
        bottomMc.chatWindow.chatName.text = ''
        npc = BigWorld.entity(info['npcId'])
        uiUtils.takePhoto3D(self.largeHead, npc, npc.npcId)

    def updateBusinessSpy(self, info):
        if self.npcType != uiConst.NPC_BUSINESS_SPY:
            return
        bottomMc = self.widget.bottom
        bottomMc.chatWindow.chatContent.htmlText = info['chat']

    def initFameSalary(self):
        info = self.uiAdapter.funcNpc.onGetFameSalaryInfoPy()
        bottomMc = self.widget.bottom
        bottomMc.chatWindow.chatContent.htmlText = info['chat']
        bottomMc.chatWindow.chatName.text = info['roleName']
        questMc = self.widget.right.quest
        questMc.visible = True
        questMc.questName.text = info['title']
        questMc.questDesc.text = ''
        questMc.btn.visible = False
        BigWorld.player().cell.getFameRewardTime(info['fameId'])
        npc = BigWorld.entity(info['npcId'])
        uiUtils.takePhoto3D(self.largeHead, npc, npc.npcId)

    def updateFameSalary(self, info):
        if self.npcType != uiConst.NPC_FAME_SALARY:
            return
        questMc = self.widget.right.quest
        questMc.questName.text = info['title']
        posY = questMc.questName.y + questMc.questName.height + 20
        if info['option']:
            for i in xrange(len(info['option'])):
                item = self.widget.getInstByClsName('NpcV2_FameSalary')
                item.fameId = info['option'][i]['fameId']
                item.bonusId = info['option'][i]['bonusId']
                item.label = info['option'][i]['desc']
                item.x = POS_X
                item.y = posY
                item.addEventListener(events.MOUSE_CLICK, self.onClickFameSalaryBtn, False, 0, True)
                posY += item.height + 10
                questMc.addChild(item)
                self.mc.append(item)

        else:
            questMc.questDesc.htmlText = info['extraText']
            questMc.questDesc.height = questMc.questDesc.textHeight + 10
            posY = questMc.questDesc.y + questMc.questDesc.height + 10
        self.updateQuestPanelPos(posY)

    def onClickFameSalaryBtn(self, *args):
        e = ASObject(args[3][0])
        self.uiAdapter.funcNpc.clickFameSalaryOption(e.currentTarget.fameId, e.currentTarget.bonusId)
        self.widget.right.quest.visible = False
        self.showReturnBtn()

    def showReturnBtn(self):
        btn = self.widget.right.commonBtn
        btn.visible = True
        btn.label = gameStrings.RETURN
        btn.addEventListener(events.MOUSE_CLICK, self.onClickReturnBtn, False, 0, True)

    def onClickReturnBtn(self, *args):
        self.widget.right.commonBtn.visible = False
        self.uiAdapter.funcNpc.onDefaultState()
        self.npcType = uiConst.NPC_FUNC
        self.enterStage()

    def initExplain(self):
        info = self.uiAdapter.funcNpc.onGetExplanationPy()
        bottomMc = self.widget.bottom
        bottomMc.chatWindow.chatContent.htmlText = info['chat']
        bottomMc.chatWindow.chatName.text = info['roleName']
        questMc = self.widget.right.quest
        questMc.visible = True
        questMc.questName.text = info['title']
        questMc.questDesc.htmlText = info['details']
        questMc.questDesc.height = questMc.questDesc.textHeight + 10
        questMc.btn.visible = False
        posY = questMc.questDesc.y + questMc.questDesc.height + 10
        npc = BigWorld.entity(info['npcId'])
        uiUtils.takePhoto3D(self.largeHead, npc, npc.npcId)
        self.updateQuestPanelPos(posY)

    def initPrize(self):
        info = self.uiAdapter.funcNpc.onGetPrizeInfoPy()
        bottomMc = self.widget.bottom
        bottomMc.chatWindow.chatContent.htmlText = info['chat']
        bottomMc.chatWindow.chatName.text = info['roleName']
        posY = 0
        if info['option']:
            questMc = self.widget.right.quest
            questMc.visible = True
            questMc.questName.text = gameStrings.PRIZE_LIST
            questMc.questDesc.text = ''
            questMc.btn.visible = False
            posY = questMc.questName.y + questMc.questName.height + 20
            for i in xrange(len(info['option'])):
                item = self.widget.getInstByClsName('NpcV2_PrizeSelection')
                item.idx = i
                item.questDesc.text = info['option'][i]['name']
                item.x = POS_X
                item.y = posY
                item.addEventListener(events.MOUSE_CLICK, self.onClickPrizeBtn, False, 0, True)
                posY += item.height + 10
                questMc.addChild(item)
                self.mc.append(item)

        npc = BigWorld.entity(info['npcId'])
        uiUtils.takePhoto3D(self.largeHead, npc, npc.npcId)
        self.updateQuestPanelPos(posY)

    def onClickPrizeBtn(self, *args):
        e = ASObject(args[3][0])
        info = self.uiAdapter.funcNpc.onGetPrizeInfoPy()
        if len(info['option']) > e.currentTarget.idx:
            self.baseRewardIdx = 0
            self.prizeIdx = e.currentTarget.idx
            option = info['option'][e.currentTarget.idx]
            questMc = self.widget.right.quest
            self.removeChild(questMc)
            questMc.questName.text = option['name']
            questMc.questDesc.htmlText = option['questDesc']
            questMc.questDesc.height = questMc.questDesc.textHeight + 10
            posY = questMc.questDesc.y + questMc.questDesc.height + 10
            if option.has_key('bonus'):
                itemArr = []
                for i in xrange(len(option['bonus'])):
                    data = option['bonus'][i]
                    if BONUS_TYPE.has_key(data['bonusType']):
                        item = self.getBaseRewardMc()
                        item.rtype.visible = False
                        item.mText.visible = True
                        item.mText.text = BONUS_TYPE[data['bonusType']]
                        item.mText.width = item.mText.textWidth + 5
                        item.textField.text = data['count']
                        item.textField.x = item.mText.x + item.mText.width
                        posY = self.addBaseRewardMc(item, posY)
                    else:
                        itemArr.append(data)

                if self.baseRewardIdx % 2:
                    posY += 48
                if itemArr:
                    posY = self.addItemReward(posY, itemArr, False, False, True)
            questMc.btn.visible = True
            questMc.btn.label = gameStrings.ACCQUIRE
            questMc.btn.addEventListener(events.MOUSE_CLICK, self.onClickAccquirePrizeBtn, False, 0, True)
            self.spaceCallback = self.onClickAccquirePrizeBtn
            self.updateQuestPanelPos(posY)

    def onClickAccquirePrizeBtn(self, *args):
        info = self.uiAdapter.funcNpc.onGetPrizeInfoPy()
        if len(info['option']) > self.prizeIdx:
            option = info['option'][self.prizeIdx]
            self.uiAdapter.funcNpc.requirePrize(option['awardType'], option['awardTime'])
            self.spaceCallback = None

    def initTower(self):
        self.lastTDItem = None
        info = self.uiAdapter.npcPanel.onGetTowerDefenseInfoPy()
        bottomMc = self.widget.bottom
        bottomMc.chatWindow.chatContent.htmlText = info['chat']
        bottomMc.chatWindow.chatName.text = info['roleName']
        questMc = self.widget.right.quest
        questMc.visible = True
        questMc.questName.text = info['title']
        questMc.questDesc.text = ''
        questMc.btn.visible = False
        posY = questMc.questName.y + questMc.questName.height + 20
        if info['debateOptions']:
            for i in xrange(len(info['debateOptions'])):
                item = self.widget.getInstByClsName('NpcV2_Selection')
                item.radioBox.visible = False
                item.textMc.textField.text = '[%d]' % (i + 1) + info['debateOptions'][i]
                item.textMc.textField.height = item.textMc.textField.textHeight + 5
                item.radio.height = item.textMc.textField.height + 5
                ASUtils.setHitTestDisable(item.textMc, True)
                item.radioIcon.y = (item.radio.height - item.radioIcon.height) / 2 + item.radio.y + 1
                item.idx = i
                item.x = POS_X
                item.y = posY
                item.addEventListener(events.MOUSE_CLICK, self.onClickTowerBtn, False, 0, True)
                self.idx2Func[i + 1] = Functor(self.clickTowerBtn, item.idx)
                posY += item.height + 10
                if info.has_key('arrow') and info['arrow'][i]:
                    arrowMc = self.widget.getInstByClsName('NpcV2_Arrow')
                    arrowMc.x = item.radio.x - arrowMc.width - POS_X
                    arrowMc.y = item.radio.y - item.radio.height / 2
                    item.addChild(arrowMc)
                questMc.addChild(item)
                self.mc.append(item)

        npc = BigWorld.entity(info['npcId'])
        uiUtils.takePhoto3D(self.largeHead, npc, npc.npcId)
        self.updateQuestPanelPos(posY)

    def clickTowerBtn(self, idx):
        self.idx2Func = {}
        if self.lastTDItem:
            self.lastTDItem.radio.selected = False
        self.uiAdapter.npcPanel.npcTDClick(idx)

    def onClickTowerBtn(self, *args):
        e = ASObject(args[3][0])
        self.clickTowerBtn(e.currentTarget.idx)
        self.lastTDItem = e.currentTarget

    def initMulti(self):
        info = self.uiAdapter.multiNpcChat.onGetMultiNpcChatInfoPy()
        bottomMc = self.widget.bottom
        bottomMc.chatWindow.chatContent.htmlText = info['chat']
        bottomMc.chatWindow.chatName.text = info['name']
        npc = BigWorld.entity(info['npcId'])
        uiUtils.takePhoto3D(self.largeHead, npc, npc.npcId)
        if self.uiAdapter.multiNpcChat.onIsQuestChatPy():
            btn = self.widget.right.commonBtn
            btn.visible = True
            btn.label = gameStrings.COMPLETE_TASK
            btn.addEventListener(events.MOUSE_CLICK, self.onClickMultiBtn, False, 0, True)
            self.spaceCallback = self.onClickMultiBtn
        if self.checkAutoQuest():
            self.speed = PLAY_AUTO
            BigWorld.callback(self.interval / self.speed, self.autoQuest)

    def onClickMultiBtn(self, *args):
        self.uiAdapter.multiNpcChat.onAccMultiNpcQuest()
        self.spaceCallback = None

    def initAward(self):
        info = self.uiAdapter.funcNpc.onGetAwardPy()
        bottomMc = self.widget.bottom
        bottomMc.chatWindow.chatContent.htmlText = info['chat']
        bottomMc.chatWindow.chatName.text = info['roleName']
        questMc = self.widget.right.quest
        questMc.visible = True
        questMc.questName.text = info['title']
        questMc.questDesc.htmlText = info['details']
        questMc.questDesc.height = questMc.questDesc.textHeight + 10
        posY = 0
        if info.has_key('reward'):
            posY = questMc.questDesc.y + questMc.questDesc.height + 10
            itemDesc = info['itemDesc']
            posY = self.addAwardMc(posY, itemDesc, info['reward'])
        questMc.btn.visible = True
        questMc.btn.label = gameStrings.ACCQUIRE
        questMc.btn.addEventListener(events.MOUSE_CLICK, self.onClickAwardBtn, False, 0, True)
        self.spaceCallback = self.onClickAwardBtn
        npc = BigWorld.entity(info['npcId'])
        uiUtils.takePhoto3D(self.largeHead, npc, npc.npcId)
        self.updateQuestPanelPos(posY)

    def addAwardMc(self, posY, itemDesc, reward):
        questMc = self.widget.right.quest
        self.baseRewardIdx = 0
        questReward = self.widget.getInstByClsName('NpcV2_SubCompensate')
        questReward.questAwdLabel.text = itemDesc
        questReward.x = POS_X
        questReward.y = posY
        questMc.addChild(questReward)
        self.mc.append(questReward)
        posY += questReward.height + 20
        for i in BONUS_TYPE.keys():
            if reward.has_key(i):
                item = self.getBaseRewardMc()
                item.rtype.visible = False
                item.mText.visible = True
                item.mText.text = BONUS_TYPE[i]
                item.mText.width = item.mText.textWidth + 5
                item.textField.text = reward[i]
                item.textField.x = item.mText.x + item.mText.width
                posY = self.addBaseRewardMc(item, posY)

        for desc in reward.keys():
            if type(desc) != int:
                item = self.getBaseRewardMc()
                item.rtype.visible = False
                item.mText.visible = True
                item.mText.text = str(desc)
                item.mText.width = item.mText.textWidth + 5
                item.textField.text = reward[desc]
                item.textField.x = item.mText.x + item.mText.width
                posY = self.addBaseRewardMc(item, posY)

        if self.baseRewardIdx % 2:
            posY += 48
        if reward.has_key(1) and reward[1]:
            posY = self.addItemReward(posY, reward[1], False, False)
        return posY

    def onClickAwardBtn(self, *args):
        self.uiAdapter.funcNpc.onRequireAward()
        self.spaceCallback = None

    def initTeleport(self):
        info = self.uiAdapter.npcPanel.onGetTeleportInfoPy()
        bottomMc = self.widget.bottom
        bottomMc.chatWindow.chatContent.htmlText = info['chat']
        bottomMc.chatWindow.chatName.text = info['roleName']
        questMc = self.widget.right.quest
        questMc.visible = True
        questMc.btn.visible = False
        questMc.questName.text = info['title']
        questMc.questDesc.text = ''
        posY = questMc.questName.y + questMc.questName.height + 20
        if info['option']:
            for i in xrange(len(info['option'])):
                item = self.widget.getInstByClsName('NpcV2_Selection')
                item.radioBox.visible = False
                item.textMc.textField.text = info['option'][i]
                item.textMc.textField.height = item.textMc.textField.textHeight + 5
                item.radio.height = item.textMc.textField.height + 5
                ASUtils.setHitTestDisable(item.textMc, True)
                item.radioIcon.y = (item.radio.height - item.radioIcon.height) / 2 + item.radio.y + 1
                item.idx = i
                item.x = POS_X
                item.y = posY
                item.addEventListener(events.MOUSE_CLICK, self.onClickTeleportBtn, False, 0, True)
                posY += item.height + 10
                questMc.addChild(item)
                self.mc.append(item)

        npc = BigWorld.entity(info['npcId'])
        uiUtils.takePhoto3D(self.largeHead, npc, npc.npcId)
        self.updateQuestPanelPos(posY)

    def onClickTeleportBtn(self, *args):
        e = ASObject(args[3][0])
        self.uiAdapter.npcPanel.teloport(e.currentTarget.idx)

    def initFunc(self):
        rightMc = self.widget.right
        rightMc.funcBtnList.visible = True
        info = self.uiAdapter.funcNpc.onGetFuncNpcChatInfoPy()
        bottomMc = self.widget.bottom
        bottomMc.chatWindow.chatContent.htmlText = info['chat']
        bottomMc.chatWindow.chatName.text = info['name']
        if info['options']:
            for i in xrange(MAX_FUNC_NUM):
                funcBtn = getattr(rightMc.funcBtnList, 'funcBtn%d' % i)
                realIdx = i - MAX_FUNC_NUM + len(info['options'])
                if realIdx >= 0:
                    funcBtn.visible = True
                    funcBtn.idx = info['options'][realIdx][1]
                    funcBtn.label = '[' + str(realIdx + 1) + ']' + info['options'][realIdx][0]
                    funcBtn.addEventListener(events.MOUSE_CLICK, self.onClickFuncBtn, False, 0, True)
                    self.idx2Func[realIdx + 1] = Functor(self.clickFuncBtn, funcBtn.idx)
                else:
                    funcBtn.visible = False

        else:
            rightMc.funcBtnList.visible = False
        npc = BigWorld.entity(info['npcId'])
        if npc and hasattr(npc, 'npcId'):
            uiUtils.takePhoto3D(self.largeHead, npc, npc.npcId)

    def clickFuncBtn(self, idx):
        self.idx2Func = {}
        self.uiAdapter.funcNpc.click(idx)
        if self.widget:
            self.widget.right.funcBtnList.visible = False

    def onClickFuncBtn(self, *args):
        e = ASObject(args[3][0])
        self.clickFuncBtn(e.currentTarget.idx)

    def initFuncDirectly(self):
        bottomMc = self.widget.bottom
        msg = self.uiAdapter.funcNpc.onGetFuncNpcDirectlyInfoPy()
        bottomMc.chatWindow.chatContent.htmlText = msg
        bottomMc.chatWindow.chatName.text = ''

    def genNPCHeadPortraits(self):
        if not os.path.exists('.\\headPhoto'):
            os.mkdir('.\\headPhoto')
        self.cutoutIdx = 0
        if self.end >= 0:
            self.cutoutIdx = self.start
        self.npcHeadPortraitsCutOut()

    def npcHeadPortraitsCutOut(self):
        if self.cutoutIdx >= len(ND.data.keys()) and self.end < 0:
            return
        if self.cutoutIdx > self.end >= 0:
            return
        npcId = self.cutoutIdx if self.end >= 0 else ND.data.keys()[self.cutoutIdx]
        self.cutoutIdx += 1
        self.largeHead.endCapture()
        modelId = NCD.data.get(npcId, {}).get('model', 0)
        if modelId and len(str(modelId)) == 6 and not os.path.exists('.\\headPhoto\\%d.png' % modelId):
            self.largeHead.setModelFinishCallback(Functor(self.savePhoto, self.largeHead, npcId))
            uiUtils.takePhoto3D(self.largeHead, self.target, npcId)
            BigWorld.callback(5, self.npcHeadPortraitsCutOut)
        else:
            BigWorld.callback(0, self.npcHeadPortraitsCutOut)
        print 'ljb cutoutIdx, npcId, modelId', self.cutoutIdx, npcId, modelId

    def initQuest(self, curTaskType = '', curTaskIdx = 0):
        bottomMc = self.widget.bottom
        taskNum = 0
        for taskType in TASK_TYPE:
            taskNum += len(self.taskInfo.get(taskType, []))

        if taskNum == 1 or curTaskType != '':
            self.isQuest = True
            self.widget.right.chatHistory.visible = AppSettings.get(keys.SET_NPC_V2_QUICK_READ_STATE, 1)
            self.widget.rightBg.visible = self.widget.right.chatHistory.visible
            bottomMc.controlBtnGroup.visible = True
            ASUtils.setHitTestDisable(bottomMc.chatWindow.chatContent, True)
            ASUtils.setHitTestDisable(bottomMc.chatWindow.chatName, True)
            if curTaskType != '':
                self.curTaskType = curTaskType
                self.curTaskIdx = curTaskIdx
            else:
                for taskType in TASK_TYPE:
                    if len(self.taskInfo.get(taskType, [])) == 1:
                        self.curTaskType = taskType

                self.curTaskIdx = 0
            info = self.taskInfo[self.curTaskType][self.curTaskIdx]
            self.words = info['words']
            self.speakers = info['speakerName']
            self.npcIds = info['idList'] or []
            self.intervals = info['interval'] or []
            if not self.words or self.words and not self.words[0]:
                self.setContent(0)
                self.words = []
                self.speakers = []
                self.npcIds = []
                self.intervals = []
                self.interval = INTERVAL
            self.initMcData()
            self.wordIdx = 0
            self.initHeadIds(info['npcId'])
            npcIds = self.headId2Slots.keys()
            for i in xrange(MAX_NPC_NUM):
                npcSlot = getattr(bottomMc.chatWindow, 'npcSlot%d' % i)
                if not npcSlot:
                    continue
                if len(self.headId2Slots) <= i:
                    npcSlot.visible = False
                else:
                    npcId = npcIds[i]
                    self.headId2Slots[npcId] = npcSlot
                    npcSlot.visible = True
                    if npcId:
                        npcSlot.gotoAndStop('up')
                        npcSlot.icon.photo2D.visible = True
                        npcSlot.icon.photo2D.fitSize = True

            mainNpcId = self.getMainNpcId(info['npcId'])
            if mainNpcId:
                uiUtils.takePhoto3D(self.largeHead, self.target, mainNpcId)
            if self.checkAutoQuest():
                self.speed = PLAY_AUTO
            self.updateQuestBottom()
        else:
            bottomMc.chatWindow.chatContent.htmlText = self.taskInfo['chat']
            bottomMc.chatWindow.chatName.text = self.taskInfo['roleName']
            questDict = {}
            for i in xrange(1, 29):
                questDict[i] = []

            for i in xrange(len(TASK_TYPE)):
                for j in xrange(len(self.taskInfo[TASK_TYPE[i]])):
                    data = self.taskInfo[TASK_TYPE[i]][j]
                    data['taskType'] = TASK_TYPE[i]
                    data['curTaskIdx'] = j
                    questDict[data['displayType']].append(data)

            self.questIndex = 1
            questMc = self.widget.right.quest
            questMc.visible = True
            questMc.questName.text = gameStrings.TASK
            questMc.questDesc.text = ''
            questMc.btn.visible = False
            posY = questMc.questName.y + questMc.questName.height + 10
            for i in xrange(len(questTypeConst.QUEST_TYPE)):
                qt = questTypeConst.QUEST_TYPE[i]
                if questDict[qt]:
                    mcName = questTypeConst.QUEST_TITLE_MAP[qt]
                    titleMc = self.widget.getInstByClsName(mcName)
                    titleMc.x = POS_X
                    titleMc.y = posY
                    questMc.addChild(titleMc)
                    self.mc.append(titleMc)
                    posY += titleMc.height + 10
                    posY = self.addQuestMc(posY, questDict[qt])

            uiUtils.takePhoto3D(self.largeHead, self.target, int(self.taskInfo['targetId']))
            self.updateQuestPanelPos(posY)

    def addQuestMc(self, posY, data):
        questMc = self.widget.right.quest
        for i in xrange(len(data)):
            item = self.widget.getInstByClsName('NpcV2_QuestLogo')
            taskType = data[i]['taskType']
            displayType = data[i]['displayType']
            if questTypeConst.QUEST_OPT_ICON_MAP.has_key(displayType):
                optIcon = questTypeConst.QUEST_OPT_ICON_MAP[displayType]
            else:
                optIcon = questTypeConst.QUEST_OPT_ICON_DEFAULT
            if taskType == 'available_tasks' or taskType == 'available_taskLoops':
                item.optIcon.gotoAndStop(optIcon[0])
            elif taskType == 'complete_tasks' or taskType == 'complete_taskLoops':
                item.optIcon.gotoAndStop(optIcon[1])
            elif taskType == 'unfinished_tasks' or taskType == 'unfinished_taskLoops':
                item.optIcon.gotoAndStop(optIcon[2])
            curTaskIdx = data[i]['curTaskIdx']
            if taskType == 'complete_tasks' or taskType == 'complete_taskLoops':
                item.taskTick.visible = True
            else:
                item.taskTick.visible = False
            item.tag = taskType + '.' + str(curTaskIdx)
            item.textField.text = '[%d]' % self.questIndex + self.taskInfo[taskType][curTaskIdx]['name']
            self.idx2Func[self.questIndex] = Functor(self.clickQuestItem, item.tag)
            self.questIndex += 1
            item.x = POS_X
            item.y = posY
            posY += item.height + 10
            item.addEventListener(events.MOUSE_CLICK, self.onClickQuestItem, False, 0, True)
            item.addEventListener(events.MOUSE_ROLL_OVER, self.onRollOverQuestItem, False, 0, True)
            item.addEventListener(events.MOUSE_ROLL_OUT, self.onRollOutQuestItem, False, 0, True)
            questMc.addChild(item)
            self.mc.append(item)

        return posY

    def clickQuestItem(self, tag):
        self.idx2Func = {}
        questMc = self.widget.right.quest
        self.removeChild(questMc)
        questMc.visible = False
        curTaskType = tag.split('.')[0]
        curTaskIdx = int(tag.split('.')[1])
        self.initQuest(curTaskType, curTaskIdx)

    def onClickQuestItem(self, *args):
        e = ASObject(args[3][0])
        self.clickQuestItem(e.currentTarget.tag)

    def onRollOverQuestItem(self, *args):
        e = ASObject(args[3][0])
        e.target.gotoAndPlay('over')

    def onRollOutQuestItem(self, *args):
        e = ASObject(args[3][0])
        e.target.gotoAndPlay('normal')

    def savePhoto(self, headGen, npcId):
        headGen.take()
        BigWorld.callback(1, Functor(self._savePhoto, headGen, npcId))

    def _savePhoto(self, headGen, npcId):
        if hasattr(headGen.adaptor, 'saveFrame'):
            modelId = NCD.data.get(npcId, {}).get('model', 0)
            headGen.adaptor.saveFrame('.\\headPhoto\\%d.png' % modelId)

    def updateQuestBottom(self):
        if not self.widget:
            return
        if self.wordIdx > len(self.words):
            self.spaceCondition = False
            return
        if self.wordIdx != len(self.words):
            bottomMc = self.widget.bottom
            npcId = self.getNpcId()
            self.updateSlot(npcId)
            self.playAction()
            self.setContent(self.wordIdx)
            if self.intervals and self.wordIdx < len(self.intervals):
                self.interval = self.intervals[self.wordIdx]
            else:
                self.interval = INTERVAL
            self.playAnim()
            self.time = utils.getNow()
            self.callback = BigWorld.callback(self.interval / self.speed, self.updateQuestBottom)
        else:
            rightMc = self.widget.right
            if rightMc.chatHistory.visible:
                rightMc.chatHistory.canvas.addChild(self.questMc)
            else:
                rightMc.addChild(self.questMc)
            self.reAddQuestSlotTip()
            self.playAnim()
            self.spaceCondition = False
            BigWorld.callback(self.interval / self.speed, self.autoQuest)
        self.wordIdx += 1

    def autoQuest(self):
        if not self.widget:
            return
        if self.checkAutoQuest() and self.spaceCallback and not self.spaceCondition:
            self.spaceCallback()

    def checkAutoQuest(self):
        if not gameglobal.rds.configData.get('enableAutoQuest', False):
            return False
        p = BigWorld.player()
        isAutoQuest = False
        if self.npcType == uiConst.NPC_QUEST:
            if not p.checkInAutoQuest() and not p.checkInLastCompletedQuestTime():
                return False
            cata = self.curTaskType
            curTaskIdx = self.curTaskIdx
            if cata in ('available_taskLoops', 'unfinished_taskLoops', 'complete_taskLoops'):
                quests = self.taskInfo.get(cata, [])
                questLoopId = quests[curTaskIdx].get('questLoopId', 0) if curTaskIdx < len(quests) else 0
                isAutoQuest = QLD.data.get(questLoopId, {}).get('auto', 0)
            elif cata == 'complete_tasks':
                quests = self.taskInfo.get(cata, [])
                if curTaskIdx < len(quests):
                    questNpcId = quests[curTaskIdx].get('questNpcId', 0)
                    chatId = quests[curTaskIdx].get('chatId', 0)
                    questId = self.getQuestIdByQuestNpcId(questNpcId, chatId)
                    questLoopId = commQuest.getQuestLoopIdByQuestId(questId)
                    isAutoQuest = QLD.data.get(questLoopId, {}).get('auto', 0)
            if isAutoQuest:
                p.startAutoQuest()
        elif self.npcType in (uiConst.NPC_DEBATE, uiConst.NPC_MULTI):
            isAutoQuest = p.checkInAutoQuest()
        return isAutoQuest

    def playAnim(self):
        if self.wordIdx < len(self.offset):
            animMc = self.widget.right.chatHistory
            animMc.playAnimation(self.offset[self.wordIdx], self.interval / self.speed)

    def playAction(self, wordIdx = -1):
        if not self.speakEvents or not self.speakEvents.has_key(self.curTaskType) or self.curTaskIdx >= len(self.speakEvents[self.curTaskType]):
            return
        else:
            if wordIdx == -1:
                wordIdx = self.wordIdx
            if wordIdx >= len(self.speakEvents[self.curTaskType][self.curTaskIdx]) or wordIdx < 0:
                return
            data = self.speakEvents[self.curTaskType][self.curTaskIdx][wordIdx]
            try:
                for info in data:
                    if info[0] == gameglobal.ACT_FLAG and self.target:
                        acts = [ str(i) for i in info[1:] ]
                        self.target.fashion.playActionSequence(self.target.model, acts, None)
                    elif info[0] == gameglobal.VOICE_FLAG:
                        gameglobal.rds.sound.playSound(int(info[1]))

            except:
                gamelog.error('onSetUnitIndex', data)

            self.checkDialog(wordIdx)
            return

    def checkDialog(self, wordIdx):
        quests = self.taskInfo.get(self.curTaskType, [])
        questId = 0
        chatId = 0
        if self.curTaskIdx < len(quests):
            questInfo = quests[self.curTaskIdx]
            chatId = questInfo.get('chatId', 0)
            questId = questInfo.get('id', 0)
        player = BigWorld.player()
        if hasattr(player, 'sendQuestDialog'):
            player.sendQuestDialog(questId, chatId, wordIdx)

    def openQuestPanel(self, isComplete, isAccept):
        if not self.widget:
            return
        else:
            self.questMc = self.widget.getInstByClsName('NpcV2_Quest')
            questMc = self.questMc
            questMc.visible = True
            info = self.taskInfo[self.curTaskType][self.curTaskIdx]
            questMc.questName.text = info['questName']
            questMc.questDesc.htmlText = info['questDesc']
            questMc.questDesc.height = questMc.questDesc.textHeight + 10
            cashType = info['cashRewardType']
            itemArr = info['mReward']
            choiceArr = info['reward']
            groupLeaderArr = info['mGroupLeader']
            choiceDesc = gameStrings.TASK_CHOICE_REWARD_DESC
            itemDesc = gameStrings.TASK_REWARD_DESC
            gold = info['goldBonus']
            exp = info['expBonus']
            socExp = info['socExp']
            fames = info['compFame']
            guild = info['guildReward']
            showFameText = True if isComplete else info['showFameText']
            showText = True if isComplete else info['showText']
            posY = 0
            self.itemSlot = None
            if choiceArr:
                posY = questMc.questDesc.y + questMc.questDesc.height + 30
                posY = self.addRewardMc(posY, showText, cashType, isComplete, choiceDesc, choiceArr, gold, exp, socExp, fames, guild, True)
                if itemArr:
                    posY = self.addRewardMc(posY, False, cashType, isComplete, itemDesc, itemArr, 0, 0, 0, [], 0)
            elif itemArr or gold > 0 or exp > 0 or socExp > 0 or fames:
                posY = questMc.questDesc.y + questMc.questDesc.height + 30
                posY = self.addRewardMc(posY, showText, cashType, isComplete, itemDesc, itemArr, gold, exp, socExp, fames, guild, False, showFameText)
            if info.get('hasLoopReward', False):
                itemArr = info['loopReward']
                if itemArr:
                    posY = self.addRewardMc(posY, showText, cashType, isComplete, gameStrings.TASK_REWARD_CUR, itemArr, 0, 0, guild)
            if info.get('hasExtraReward', False) and isComplete:
                itemArr = info['extraReward']
                gold = info['extraGoldBonus']
                exp = info['extraExpBonus']
                if not itemArr:
                    itemArr = info['extraMReward']
                posY = self.addRewardMc(posY, showText, cashType, isComplete, gameStrings.TASK_REWARD_EXTRA, itemArr, gold, exp, guild)
            if groupLeaderArr:
                posY = self.addRewardMc(posY, showText, cashType, isComplete, gameStrings.TASK_REWARD_CAPTAIN, groupLeaderArr, 0, 0)
            if info.get('loopRewardItems', []):
                itemArr = info['loopRewardItems']
                loopRewardDesc = info['loopRewardDesc']
                if itemArr:
                    posY = self.addRewardMc(posY, False, cashType, isComplete, loopRewardDesc, itemArr, 0, 0)
            questMc.questBg.visible = True
            if isComplete:
                questMc.btn.visible = True
                questMc.btn.label = gameStrings.COMPLETE_TASK
                questMc.btn.addEventListener(events.MOUSE_CLICK, self.onClickCompleteBtn, False, 0, True)
                self.spaceCallback = self.onClickCompleteBtn
            elif not isAccept:
                questMc.btn.visible = True
                questMc.btn.label = gameStrings.ACCEPT_TASK
                questMc.btn.addEventListener(events.MOUSE_CLICK, self.onClickAcceptBtn, False, 0, True)
                self.spaceCallback = self.onClickAcceptBtn
            else:
                questMc.btn.visible = False
            if self.taskInfo.has_key('ignorePanel') and self.taskInfo['ignorePanel']:
                questMc.questBg.visible = False
                if questMc.btn.visible:
                    questMc.btn.addEventListener(events.MOUSE_CLICK, self.onClickExitBtn, False, 0, True)
                    self.spaceCallback = self.onClickExitBtn
            if self.taskInfo.has_key('ignoreButton') and self.taskInfo['ignoreButton']:
                questMc.btn.visible = False
            self.updateQuestPanelPos(posY)
            return

    def updateQuestPanelPos(self, posY, limitPosY = 0):
        questMc = self.questMc
        if not limitPosY:
            limitPosY = QUEST_BG_HEIGHT
        if posY > limitPosY:
            questMc.questBg.height = posY + 10
            questMc.btn.y = questMc.questBg.y + questMc.questBg.height + 20
            questMc.y -= posY - QUEST_BG_HEIGHT - 120
        if not questMc.questBg.visible:
            questMc.btn.y = 10

    @ui.callFilter(1)
    def onClickAcceptBtn(self, *args):
        info = self.taskInfo[self.curTaskType][self.curTaskIdx]
        id = int(info['id'])
        isLoop = True if self.curTaskType == 'available_taskLoops' else False
        p = BigWorld.player()
        gameglobal.rds.ui.messageBox.dismiss(uiConst.MESSAGEBOX_QUEST, False)
        if self.isNPC:
            if isLoop:
                if id in p.questLoopInfo:
                    questIds = p.questLoopInfo[id].getNextQuests(p)
                else:
                    questIds = commQuest.getAvaiNextQuestsInLoop(p, id, 0)
                isTeleport = False
                for questId in questIds:
                    if p.checkTeleport(questId, 1):
                        isTeleport = True
                        break

                if not p.checkQuestCompleteMsgBox(id, Functor(self.realAcceptQuestLoop, isTeleport, id)):
                    self.realAcceptQuestLoop(isTeleport, id)
            else:
                isteleport = p.checkTeleport(id, 1)
                if isteleport:
                    MBButton = messageBoxProxy.MBButton
                    buttons = [MBButton(gameStrings.CONFIRM, Functor(self.acceptQuest, self.target, id)), MBButton(gameStrings.CANCEL)]
                    msg = self.getMsg(GMDD.data.QUEST_ACCEPT_TELEPORT_CONFIRMATION, gameStrings.ACCEPT_TASK_TELEPORT_CONFIRM)
                    gameglobal.rds.ui.messageBox.show(True, '', msg, buttons, False, 0, uiConst.MESSAGEBOX_QUEST)
                elif p.checkAcZaijuQst(id):
                    MBButton = messageBoxProxy.MBButton
                    buttons = [MBButton(gameStrings.CONFIRM, Functor(self.acceptQuest, self.target, id)), MBButton(gameStrings.CANCEL)]
                    msg = self.getMsg(GMDD.data.QUEST_ACCEPT_ZAIJU_CONFIRMATION, gameStrings.ACCEPT_TASK_TRANSFORMATION_CONFIRM)
                    gameglobal.rds.ui.messageBox.show(True, '', msg, buttons, False, 0, uiConst.MESSAGEBOX_QUEST)
                elif p.checkAddBuff(id, 1):
                    MBButton = messageBoxProxy.MBButton
                    buttons = [MBButton(gameStrings.CONFIRM, Functor(self.acceptQuest, self.target, id)), MBButton(gameStrings.CANCEL)]
                    msg = self.getMsg(GMDD.data.QUEST_ACCEPT_ADD_BUFF_CONFIRMATION, gameStrings.ACCEPT_TASK_BUFF_CONFIRM)
                    gameglobal.rds.ui.messageBox.show(True, '', msg, buttons, False, 0, uiConst.MESSAGEBOX_QUEST)
                else:
                    self.acceptQuest(self.target, id)
        else:
            self.leaveStage()
            p.cell.acceptQuestByItem(self.page, self.pos)
        gameglobal.rds.sound.playSound(gameglobal.SD_96)
        self.spaceCallback = None

    def realAcceptQuestLoop(self, isTeleport, questLoopId):
        if isTeleport:
            MBButton = messageBoxProxy.MBButton
            buttons = [MBButton(gameStrings.CONFIRM, Functor(self.acceptQuestLoop, self.target, questLoopId)), MBButton(gameStrings.CANCEL)]
            msg = self.getMsg(GMDD.data.QUEST_ACCEPT_TELEPORT_CONFIRMATION, gameStrings.ACCEPT_TASK_TELEPORT_CONFIRM)
            gameglobal.rds.ui.messageBox.show(True, '', msg, buttons, False, 0, uiConst.MESSAGEBOX_QUEST)
        else:
            self.acceptQuestLoop(self.target, questLoopId)

    def acceptQuestLoop(self, target, id):
        p = BigWorld.player()
        if QLD.data.get(id, {}).get('teamQuest', 0) and p.groupHeader and p.groupHeader != p.id:
            if p.groupType == gametypes.GROUP_TYPE_TEAM_GROUP:
                self.confirmBeforeAcceptLoop(target, id)
                return
            if p.groupType == gametypes.GROUP_TYPE_RAID_GROUP:
                for _gbId, mVal in p.members.iteritems():
                    if mVal['id'] == p.groupHeader:
                        index1 = p.arrangeDict.get(_gbId, -1)
                        index2 = p.arrangeDict.get(p.gbId, -1)
                        if utils.isSameTeam(index1, index2):
                            self.confirmBeforeAcceptLoop(target, id)
                            return

        elif QLD.data.get(id, {}).get('teamQuest', 0) and p.groupHeader and p.groupHeader == p.id and len(p.members) > 1:
            if QLD.data.get(id, {}).get('needPushToHeader', 0) and not gameglobal.rds.ui.messageBox.hasChecked('pushLoop'):
                target.pushToHeaderB4DoWithQuestLoop(id, 1, {})
                return
        target.acceptQuestLoop(id)

    def confirmBeforeAcceptLoop(self, target, id):
        if QLD.data.get(id, {}).get('needPushToHeader', 0):
            BigWorld.player().cell.getHeaderLoopProgress(gametypes.QUEST_STAGE_ACCEPT, id, target.id, 0)
            return
        msg = MSGDD.data.get('confirmBeforeAcQstLoop_msg', gameStrings.ACCEPT_TASK_MYSELF)
        self.twiceCheckBox = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.doConfirmBeforeAcceptLoop, target, id), yesBtnText=gameStrings.CONFIRM, noCallback=Functor(self.cancelConfirmBeforeAcceptLoop), noBtnText=gameStrings.CANCEL)

    def onGetHeaderLoopProgress(self, questLoopId, npcId, info, checkStage, arg):
        myLoopCnt, myLoopStatus = info.get(BigWorld.player().id)
        headerLoopCnt, headerLoopStatus = info.get('header')
        msg = ''
        if headerLoopCnt > myLoopCnt:
            msg = gameStrings.TASK_PROGRESS_SLOW_TIP % (headerLoopCnt, myLoopCnt)
        elif headerLoopCnt < myLoopCnt:
            msg = gameStrings.TASK_PROGRESS_FAST_TIP % (headerLoopCnt, myLoopCnt)
        elif headerLoopStatus == gametypes.QUEST_STAGE_ACCEPT:
            msg = gameStrings.TASK_PROGRESS_WILL_FAST_TIP
        elif headerLoopStatus == gametypes.QUEST_STAGE_COMPLETE:
            if myLoopStatus == gametypes.QUEST_STAGE_ACCEPT:
                msg = gameStrings.TASK_PROGRESS_WILL_GET_TIP
            elif myLoopStatus == gametypes.QUEST_STAGE_COMPLETE:
                msg = gameStrings.TASK_PROGRESS_WILL_FAST_ACCEPT_TIP
        elif headerLoopStatus == myLoopStatus == 0:
            msg = gameStrings.TASK_PROGRESS_WILL_FAST_ACCEPT_TIP
        target = BigWorld.entities.get(npcId)
        if checkStage == gametypes.QUEST_STAGE_ACCEPT:
            self.twiceCheckBox = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.doConfirmBeforeAcceptLoop, target, questLoopId), yesBtnText=gameStrings.CONTINUE_TASK, noBtnText=gameStrings.CANCEL, isModal=False, msgType='pushLoop', textAlign='center')
        else:
            self.twiceCheckBox = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.doConfirmBeforeCompleteLoop, target, questLoopId, arg), yesBtnText=gameStrings.CONTINUE_TASK, noBtnText=gameStrings.CANCEL, isModal=False, msgType='pushLoop', textAlign='center')

    def doConfirmBeforeAcceptLoop(self, target, id):
        target and target.acceptQuestLoop(id)
        self.twiceCheckBox = 0

    def cancelConfirmBeforeAcceptLoop(self):
        self.twiceCheckBox = 0

    def acceptQuest(self, target, id):
        if target:
            target.acceptQuest(id)

    @ui.callFilter(1)
    def onClickCompleteBtn(self, *args):
        info = self.taskInfo[self.curTaskType][self.curTaskIdx]
        id = int(info['id'])
        choice = self.itemSlot.index if self.itemSlot else -1
        isLoop = True if self.curTaskType == 'complete_taskLoops' else False
        gameglobal.rds.ui.messageBox.dismiss(uiConst.MESSAGEBOX_QUEST, False)
        if isLoop:
            questId = BigWorld.player().questLoopInfo[id].getCurrentQuest()
            rewardData = commQuest.genQuestRewardChoice(self, questId) if questId else None
        else:
            questId = id
            rewardData = commQuest.genQuestRewardChoice(self, id)
        if rewardData:
            if choice == -1:
                MBButton = messageBoxProxy.MBButton
                buttons = [MBButton(gameStrings.CONFIRM)]
                msg = self.getMsg(GMDD.data.QUEST_REWARD_CHOICE_PROMPT, gameStrings.TASK_REWARD_CHOICE)
                self.chooseRewardMsgBoxId = gameglobal.rds.ui.messageBox.show(False, '', msg, buttons, False, 0, uiConst.MESSAGEBOX_QUEST)
                BigWorld.player().showGameMsg(GMDD.data.QUEST_NEED_SELECT_PRIZE, ())
                return
            if not BigWorld.player().checkRewardItems(int(questId), choice):
                MBButton = messageBoxProxy.MBButton
                buttons = [MBButton(gameStrings.CONFIRM, Functor(self.commitTask, id, choice)), MBButton(gameStrings.CANCEL)]
                msg = self.getMsg(GMDD.data.QUEST_REWARD_UNMATCH_CONFIRMATION, gameStrings.TASK_REWARD_CHOICE_NOT_SUITABLE)
                gameglobal.rds.ui.messageBox.show(True, '', msg, buttons, False, 0, uiConst.MESSAGEBOX_QUEST)
                return
        p = BigWorld.player()
        if gameglobal.rds.configData.get('enableSummonedSprite', False) and getattr(p, 'summonSpriteList', {}) and not getattr(p, 'spriteBattleIndex', 0):
            qdData = QD.data.get(int(questId), {})
            if qdData:
                rewardMode = qdData.get('reward', 0)
                qrdData = QRD.data.get(rewardMode, {})
                spriteExp = qrdData.get('spriteExp', 0)
                spriteFami = qrdData.get('spriteFami', 0)
                if spriteExp or spriteFami:
                    if not gameglobal.rds.ui.messageBox.getCheckOnceData(uiConst.CHECK_ONCE_TYPE_SPRITE_EXP_OR_FAMI_ADD):
                        msg = self.getMsg(GMDD.data.QUEST_SPRITE_REWARD_EXP_OR_FAMI, '')
                        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.commitTask, id, choice, isLoop), yesBtnText=gameStrings.COMPLETE_TASK_DESC, isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_SPRITE_EXP_OR_FAMI_ADD)
                        return
        self.commitTask(id, choice, isLoop)

    def getMsg(self, msgId, defaultMsg = ''):
        gmMsg = GMD.data.get(msgId, {})
        return gmMsg.get('text', defaultMsg)

    def commitTask(self, id, choice, isLoop = False):
        questId = None
        p = BigWorld.player()
        if isLoop and id in p.questLoopInfo:
            questId = p.questLoopInfo[id].getCurrentQuest()
        else:
            questId = id
        if questId is None:
            return
        else:
            qdd = QD.data.get(questId, {})
            if qdd.get('completeNeedComfirm', 0):
                msg = qdd.get('completeDoubleCheckMsg', gameStrings.COMPLETE_TASK_INPUT)
                label = qdd.get('completeDoubleCheckLabel', 'yes')
                title = gameStrings.TIP
                gameglobal.rds.ui.doubleCheckWithInput.show(msg, label, title, Functor(self.confirmCommitTask, id, choice, isLoop))
            else:
                self.confirmCommitTask(id, choice, isLoop)
            return

    def confirmCommitTask(self, id, choice, isLoop):
        questId = None
        if isLoop:
            if id in BigWorld.player().questLoopInfo:
                questId = BigWorld.player().questLoopInfo[id].getCurrentQuest()
            if not questId:
                return
        else:
            questId = id
        qd = QD.data.get(questId, {})
        commitItem = qd.get('submitItem', ())
        if commitItem:
            submitItemDesc = qd.get('submitItemDesc', '')
            itemIds = [ item[0] for item in commitItem ]
            itemNums = [ item[1] for item in commitItem ]
            gameglobal.rds.ui.payItem.show(itemIds, itemNums, id, choice, questId, isLoop, submitItemDesc)
        else:
            self.autoCommitItem(id, choice, questId, isLoop)

    def autoCommitItem(self, id, choice, questId, isLoop):
        completeFunc = self.completeTaskLoop if isLoop else self.completeTask
        isteleport = BigWorld.player().checkTeleport(questId, 2)
        if isteleport:
            MBButton = messageBoxProxy.MBButton
            buttons = [MBButton(gameStrings.CONFIRM, Functor(completeFunc, self.target, id, choice)), MBButton(gameStrings.CANCEL)]
            msg = self.getMsg(GMDD.data.QUEST_COMMIT_TELEPORT_CONFIRMATION, gameStrings.COMPLETE_TASK_TELEPORT_CONFIRM)
            gameglobal.rds.ui.messageBox.show(True, '', msg, buttons, False, 0, uiConst.MESSAGEBOX_QUEST)
        else:
            completeFunc(self.target, id, choice)

    def completeTask(self, target, id, choice):
        if choice == -1:
            target.completeQuest(id, {})
        else:
            target.completeQuest(id, {'rewardChoice': choice})

    def completeTaskLoop(self, target, id, choice):
        p = BigWorld.player()
        if QLD.data.get(id, {}).get('teamQuest', 0) and p.groupHeader and p.groupHeader != p.id:
            if p.groupType == gametypes.GROUP_TYPE_TEAM_GROUP:
                self.confirmBeforeCompleteLoop(target, id, choice)
                return
            if p.groupType == gametypes.GROUP_TYPE_RAID_GROUP:
                for _gbId, mVal in p.members.iteritems():
                    if mVal['id'] == p.groupHeader:
                        index1 = p.arrangeDict.get(_gbId, -1)
                        index2 = p.arrangeDict.get(p.gbId, -1)
                        if utils.isSameTeam(index1, index2):
                            self.confirmBeforeCompleteLoop(target, id, choice)
                            return

        elif QLD.data.get(id, {}).get('teamQuest', 0) and p.groupHeader and p.groupHeader == p.id and len(p.members) > 1:
            if QLD.data.get(id, {}).get('needPushToHeader', 0) and not gameglobal.rds.ui.messageBox.hasChecked('pushLoop'):
                options = {'rewardChoice': choice} if choice != -1 else {}
                target.pushToHeaderB4DoWithQuestLoop(id, 2, options)
                return
        if choice == -1:
            target.completeQuestLoop(id, {})
        else:
            target.completeQuestLoop(id, {'rewardChoice': choice})

    def confirmBeforeCompleteLoop(self, target, id, choice):
        if QLD.data.get(id, {}).get('needPushToHeader', 0):
            BigWorld.player().cell.getHeaderLoopProgress(gametypes.QUEST_STAGE_COMPLETE, id, target.id, choice)
            return
        msg = MSGDD.data.get('confirmBeforeCompQstLoop_msg', gameStrings.COMPLETE_TASK_MYSELF)
        self.twiceCheckBox = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.doConfirmBeforeCompleteLoop, target, id, choice), yesBtnText=gameStrings.CONFIRM, noCallback=Functor(self.cancelConfirmBeforeCompleteLoop), noBtnText=gameStrings.CANCEL)

    def doConfirmBeforeCompleteLoop(self, target, id, choice):
        if choice == -1:
            target.completeQuestLoop(id, {})
        else:
            target.completeQuestLoop(id, {'rewardChoice': choice})
        self.twiceCheckBox = 0

    def cancelConfirmBeforeCompleteLoop(self):
        self.twiceCheckBox = 0

    def addRewardMc(self, posY, showText, cashType, isComplete, itemDesc, itemArr, gold, exp, socExp = 0, fames = None, guild = 0, choice = False, showFameText = True):
        questMc = self.questMc
        self.baseRewardIdx = 0
        questReward = self.widget.getInstByClsName('NpcV2_QuestReward')
        questReward.textField.text = itemDesc
        questMc.addChild(questReward)
        self.mc.append(questReward)
        questReward.y = posY
        questReward.x = POS_X
        posY += questReward.height + 20
        if gold:
            goldReward = self.getBaseRewardMc()
            if cashType == 2:
                goldReward.rtype.bonusType = 'bindCash'
            else:
                goldReward.rtype.bonusType = 'cash'
            if showText:
                goldReward.textField.text = gold
            else:
                goldReward.starPanel.visible = True
                for i in xrange(gold):
                    starReward = self.widget.getInstByClsName('NpcV2_StarReward')
                    goldReward.starPanel.addChild(starReward)
                    starReward.x = i * starReward.width

                goldReward.textField.visible = False
            posY = self.addBaseRewardMc(goldReward, posY)
        if exp:
            expReward = self.getBaseRewardMc()
            expReward.rtype.bonusType = 'exp'
            if showText:
                expReward.textField.text = exp
            else:
                expReward.starPanel.visible = True
                for i in xrange(exp):
                    starReward = self.widget.getInstByClsName('NpcV2_StarReward')
                    expReward.starPanel.addChild(starReward)
                    starReward.x = i * starReward.width

                expReward.textField.visible = False
            posY = self.addBaseRewardMc(expReward, posY)
        if guild:
            guildReward = self.getBaseRewardMc()
            guildReward.rtype.bonusType = 'guildReward'
            guildReward.textField.text = guild
            posY = self.addBaseRewardMc(guildReward, posY)
        if socExp:
            socExpReward = self.getBaseRewardMc()
            socExpReward.rtype.bonusType = 'socialExp'
            socExpReward.textField.text = socExp
            posY = self.addBaseRewardMc(socExpReward, posY)
        if fames:
            for i in xrange(len(fames)):
                fameReward = self.getBaseRewardMc()
                fameReward.rtype.visible = False
                fameReward.mText.visible = True
                fameReward.mText.text = str(fames[i][0]) + ':'
                fameReward.mText.width = fameReward.mText.textWidth + 5
                fameReward.textField.x = fameReward.mText.x + fameReward.mText.width
                if showFameText:
                    fameReward.textField.text = fames[i][1]
                else:
                    fameReward.starPanel.visible = True
                    fameReward.starPanel.x = fameReward.textField.x
                    starNum = min(fames[i][1], 8)
                    for j in xrange(starNum):
                        starReward = self.widget.getInstByClsName('NpcV2_StarReward')
                        fameReward.starPanel.addChild(starReward)
                        starReward.x = j * starReward.width

                    fameReward.textField.visible = False
                posY = self.addBaseRewardMc(fameReward, posY)

        if self.baseRewardIdx % 2:
            posY += 48
        posY = self.addItemReward(posY, itemArr, isComplete, choice)
        return posY

    def addItemReward(self, posY, itemArr, isComplete, choice, isFuncTip = False):
        if len(itemArr):
            for i in xrange(len(itemArr)):
                itemReward = self.widget.getInstByClsName('NpcV2_ItemReward')
                slot = itemReward.slot
                slot.setItemSlotData(itemArr[i])
                slot.setSlotState(itemArr[i]['state'])
                slot.setSlotColor(itemArr[i]['qualitycolor'])
                slot.dragable = False
                slot.index = i
                slot.validateNow()
                if isFuncTip:
                    TipManager.addItemTipById(slot, itemArr[i]['bonusItemId'])
                    slot.itemId = itemArr[i]['bonusItemId']
                else:
                    TipManager.addItemTipById(slot, itemArr[i]['id'])
                    slot.itemId = itemArr[i]['id']
                self.questMc.addChild(itemReward)
                self.mc.append(itemReward)
                itemReward.x = ITEM_REWARD_POS_X[i % 4]
                itemReward.y = posY
                if i % 4 == 3 or i == len(itemArr) - 1:
                    posY += itemReward.height + 10
                if isComplete and choice:
                    slot.addEventListener(events.BUTTON_CLICK, self.onClickItemSlot, False, 0, True)
                    slot.addEventListener(events.MOUSE_ROLL_OUT, self.onRollOutItemSlot, False, 0, True)

        return posY

    def onClickItemSlot(self, *args):
        e = ASObject(args[3][0])
        if self.itemSlot:
            if self.itemSlot.index == e.currentTarget.index:
                return
            self.itemSlot.setSlotState(1)
        e.currentTarget.setSlotState(11)
        self.itemSlot = e.currentTarget

    def onRollOutItemSlot(self, *args):
        e = ASObject(args[3][0])
        if self.itemSlot and self.itemSlot.index == e.currentTarget.index:
            e.currentTarget.setSlotState(11)

    def getBaseRewardMc(self):
        rewardMc = self.widget.getInstByClsName('NpcV2_BaseReward')
        rewardMc.mText.visible = False
        rewardMc.starPanel.visible = False
        return rewardMc

    def addBaseRewardMc(self, mc, posY):
        questMc = self.questMc
        questMc.addChild(mc)
        self.mc.append(mc)
        mc.x = BASE_REWARD_POS_X[self.baseRewardIdx % 2]
        mc.y = posY
        if self.baseRewardIdx % 2 or mc.textField.x + mc.textField.width >= BASE_REWARD_POS_X[1]:
            posY += mc.height + 20
            if not self.baseRewardIdx % 2:
                self.baseRewardIdx -= 1
        self.baseRewardIdx += 1
        return posY

    def hideTwiceCheckBox(self):
        if self.twiceCheckBox:
            gameglobal.rds.ui.messageBox.dismiss(self.twiceCheckBox)
            self.twiceCheckBox = 0

    def setCallback(self, callback):
        self.closeCallback = callback

    def registerEventListener(self):
        self.widget.addEventListener(events.WIDGET_REFLOWED, self.handleResize, False, 0, True)
        self.widget.stage.addEventListener(events.KEYBOARD_EVENT_KEY_DOWN, self.handleKeyEvent, False, 0, True)
        ctrlBtnGroup = self.widget.bottom.controlBtnGroup
        self.widget.exitBtn.addEventListener(events.BUTTON_CLICK, self.onClickExitBtn, False, 0, True)
        ctrlBtnGroup.playBtn.addEventListener(events.BUTTON_CLICK, self.onClickPlayBtn, False, 0, True)
        ctrlBtnGroup.pauseBtn.addEventListener(events.BUTTON_CLICK, self.onClickPauseBtn, False, 0, True)
        ctrlBtnGroup.normalBtn.addEventListener(events.BUTTON_CLICK, self.onClickSpeedBtn, False, 0, True)
        ctrlBtnGroup.speedBtn.addEventListener(events.BUTTON_CLICK, self.onClickSpeedBtn, False, 0, True)
        ctrlBtnGroup.quickBtn.addEventListener(events.BUTTON_CLICK, self.onClickQuickBtn, False, 0, True)
        ctrlBtnGroup.nextBtn.addEventListener(events.BUTTON_CLICK, self.onClickNextBtn, False, 0, True)
        self.widget.bottom.chatWindow.bottomBg.addEventListener(events.MOUSE_CLICK, self.onClickNextBtn, False, 0, True)
        self.widget.right.chatHistory.canvas.addEventListener(events.MOUSE_WHEEL, self.handleWheel, False, 0, True)

    def needHandelOtherWnd(self):
        if gameglobal.rds.ui.ftbBind.widget:
            return True
        return False

    def handleKeyEvent(self, *args):
        if self.needHandelOtherWnd():
            return True
        if self.widget:
            e = ASObject(args[3][0])
            keyCode = e.keyCode
            mods = self.getComKey(e.shiftKey, e.ctrlKey, e.altKey)
            if keyCode == KEYCODE_SPACE and self.spaceCallback and not self.spaceCondition:
                self.spaceCallback()
            elif keyCode >= KEYCODE_1 and keyCode <= KEYCODE_1 + 8 or keyCode >= KEYCODE_NUMS_1 and keyCode <= KEYCODE_NUMS_1 + 8:
                num = keyCode - int(keyCode / 48) * 48
                if self.idx2Func.has_key(num):
                    self.idx2Func[num]()
            elif keyCode == KEYCODE_C:
                pass
            else:
                HK_DATA = [{'index': HK.KEY_PICK_ITEM,
                  'func': self.onClickNextBtn}, {'index': HK.KEY_NPCV2_SPEED,
                  'func': self.onClickSpeedBtn}, {'index': HK.KEY_NPCV2_QUICK,
                  'func': self.onClickQuickBtn}]
                for data in HK_DATA:
                    key, mod, desc = hotkeyProxy.getAsKeyContent(data['index'])
                    if key == keyCode and mod == mods:
                        data['func']()

    def getComKey(self, shiftKey, ctrlKey, altKey):
        if shiftKey:
            return 1
        if ctrlKey:
            return 2
        if altKey:
            return 4
        return 0

    def handleWheel(self, *args):
        if not self.isQuest:
            return
        e = ASObject(args[3][0])
        delta = -1 if e.delta > 0 else 1
        if self.delta == delta:
            return
        self.delta = delta
        animMc = self.widget.right.chatHistory
        offset = WHEEL_OFFSET
        if delta > 0:
            pos = self.targetPos[len(self.targetPos) - 1]
            limitPos = pos[len(pos) - 1]
            if self.questMc.y <= limitPos + 10:
                self.spaceCondition = False
                return
            if self.questMc.y - limitPos < WHEEL_OFFSET:
                self.spaceCondition = False
                offset = self.questMc.y - limitPos
        else:
            pos = self.targetPos[0]
            limitPos = pos[0]
            mc = self.animMCs[0]
            if mc.y >= limitPos:
                return
            if limitPos - mc.y < WHEEL_OFFSET:
                offset = limitPos - mc.y
        animMc.playAnimation(delta * offset, offset / WHEEL_OFFSET)
        BigWorld.callback(offset / WHEEL_OFFSET, self.handleWheelEnd)
        if self.state == STATE_PLAY:
            self.onClickPauseBtn()
            self.remainTime = 0

    def handleWheelEnd(self):
        if not self.widget:
            return
        self.wordIdx = len(self.animMCs) - 1
        for i, mc in enumerate(self.animMCs):
            if i and mc.y > 800:
                self.wordIdx = i - 1
                break

        itemMc = self.animMCs[self.wordIdx]
        for pos in self.targetPos[self.wordIdx]:
            if itemMc.y > pos + 10:
                self.wheelOffset = itemMc.y - pos
                break

        self.updateWheelQuestBottom()
        self.delta = 0

    def updateWheelQuestBottom(self):
        if self.wordIdx > len(self.words):
            return
        wordIdx = self.wordIdx if self.wordIdx != len(self.words) else self.wordIdx - 1
        if wordIdx < 0:
            return
        bottomMc = self.widget.bottom
        npcId = self.getNpcId()
        self.updateSlot(npcId)
        self.playAction(wordIdx)
        self.setContent(wordIdx)

    def setContent(self, wordIdx):
        bottomMc = self.widget.bottom
        if wordIdx >= len(self.words):
            bottomMc.chatWindow.chatContent.htmlText = ''
        else:
            bottomMc.chatWindow.chatContent.htmlText = self.words[wordIdx]
        if wordIdx < len(self.speakers):
            bottomMc.chatWindow.chatName.text = self.speakers[wordIdx]

    @ui.callFilter(0.15, False)
    def onClickNextBtn(self, *args):
        if not self.widget:
            return
        if not self.isQuest:
            return
        wordIdx = self.wordIdx - 1
        if wordIdx > len(self.words):
            self.spaceCondition = False
            return
        offset = 0
        if wordIdx < len(self.animMCs):
            itemMc = self.animMCs[wordIdx]
            for pos in self.targetPos[wordIdx]:
                if itemMc.y > pos + 10:
                    offset = itemMc.y - pos
                    break

        if offset:
            if self.state == STATE_PLAY:
                self.onClickPauseBtn()
                self.remainTime = 0
                self.playNextAnim(offset)
                if self.wordIdx == len(self.words):
                    self.spaceCondition = False
            else:
                self.updateNextQuestBottom(offset)
        else:
            self.spaceCondition = False

    def updateSlot(self, npcId):
        for id, slot in self.headId2Slots.iteritems():
            if not slot:
                continue
            if id == npcId:
                slot.gotoAndStop('up')
                if slot.icon:
                    self.loadNpcPhoto(slot.icon.photo2D, id)
            else:
                slot.gotoAndStop('disable')
                if slot.iconDisable:
                    self.loadNpcPhoto(slot.iconDisable.photo2D, id)

    def updateNextQuestBottom(self, offset):
        if not self.widget:
            return
        if self.wordIdx > len(self.words):
            self.spaceCondition = False
            return
        if self.wordIdx != len(self.words):
            bottomMc = self.widget.bottom
            npcId = self.getNpcId()
            self.updateSlot(npcId)
            self.playAction()
            self.setContent(self.wordIdx)
            self.playNextAnim(offset)
        else:
            rightMc = self.widget.right
            if rightMc.chatHistory.visible:
                rightMc.chatHistory.canvas.addChild(self.questMc)
            else:
                rightMc.addChild(self.questMc)
            self.reAddQuestSlotTip()
            self.playNextAnim(offset)
            self.spaceCondition = False
        self.wordIdx += 1

    def playNextAnim(self, offset):
        animMc = self.widget.right.chatHistory
        animMc.playAnimation(offset, 0.1)

    def onClickQuickBtn(self, *args):
        if not self.widget:
            return
        if not self.isQuest:
            return
        rightMc = self.widget.right
        rightMc.chatHistory.visible = not rightMc.chatHistory.visible
        self.widget.rightBg.visible = not self.widget.rightBg.visible
        if self.wordIdx > len(self.words):
            if rightMc.chatHistory.visible:
                rightMc.chatHistory.canvas.addChild(self.questMc)
            else:
                self.onClickNextBtn()
                rightMc.addChild(self.questMc)
            self.reAddQuestSlotTip()
            self.spaceCondition = False
        AppSettings[keys.SET_NPC_V2_QUICK_READ_STATE] = 1 if rightMc.chatHistory.visible else 0

    def onClickSpeedBtn(self, *args):
        if not self.widget:
            return
        if not self.isQuest:
            return
        if self.speed == PLAY_NORMAL:
            self.speed = PLAY_SPEED
            self.widget.bottom.controlBtnGroup.normalBtn.visible = True
            self.widget.bottom.controlBtnGroup.speedBtn.visible = False
        else:
            self.speed = PLAY_NORMAL
            self.widget.bottom.controlBtnGroup.speedBtn.visible = True
            self.widget.bottom.controlBtnGroup.normalBtn.visible = False

    def onClickPlayBtn(self, *args):
        if not self.isQuest:
            return
        btn = ASObject(args[3][0]).currentTarget
        btn.visible = False
        self.widget.bottom.controlBtnGroup.pauseBtn.visible = True
        if self.wheelOffset:
            if self.intervals:
                if self.wordIdx >= len(self.intervals):
                    self.interval = self.intervals[len(self.intervals) - 1]
                else:
                    self.interval = self.intervals[self.wordIdx]
            else:
                self.interval = INTERVAL
            animMc = self.widget.right.chatHistory
            animMc.playAnimation(self.wheelOffset, self.interval / self.speed)
            self.wheelOffset = 0
            self.callback = BigWorld.callback(self.interval / self.speed, self.updateQuestBottom)
            self.wordIdx += 1
        elif self.remainTime:
            self.callback = BigWorld.callback(self.remainTime / self.speed, self.updateQuestBottom)
        self.state = STATE_PLAY

    def onClickPauseBtn(self, *args):
        if not self.isQuest:
            return
        else:
            self.widget.bottom.controlBtnGroup.pauseBtn.visible = False
            self.widget.bottom.controlBtnGroup.playBtn.visible = True
            if self.callback:
                BigWorld.cancelCallback(self.callback)
            self.callback = None
            self.remainTime = max(self.interval - utils.getNow() + self.time, 0)
            self.state = STATE_PAUSE
            return

    def onClickExitBtn(self, *args):
        if gameglobal.rds.ui.puzzle.visible:
            gameglobal.rds.ui.puzzle.hidePuzzle()
            return
        else:
            if self.uiAdapter.funcNpc.isOnFuncState():
                self.uiAdapter.funcNpc.closeByInv()
            self.leaveStage()
            self.spaceCallback = None
            return

    def initHeadIds(self, questNpcId):
        self.headId2Slots = {}
        for id in self.npcIds:
            if id:
                if NCD.data.get(self.getMainNpcId(questNpcId), {}).get('model', 0) != NCD.data.get(id, {}).get('model', 0) and not self.headId2Slots.has_key(id):
                    self.headId2Slots[id] = None

    def getMainNpcId(self, questNpcId):
        npc = BigWorld.entities.get(questNpcId)
        npcId = None
        if npc and npc.inWorld:
            npcId = npc.npcId
        return npcId

    def isAsideText(self, asideIds):
        if self.wordIdx >= len(asideIds):
            return False
        if asideIds[self.wordIdx]:
            return True
        return False

    def getNpcId(self):
        npcId = -2
        if self.npcIds:
            if self.wordIdx >= len(self.words):
                npcId = self.npcIds[len(self.npcIds) - 1]
            elif self.wordIdx >= len(self.npcIds):
                npcId = self.npcIds[len(self.npcIds) - 1]
            else:
                npcId = self.npcIds[self.wordIdx]
        return npcId

    def initQuestData(self):
        if self.isNPC:
            roleName = ''
            npcId = 0
            if self.target and self.target.inWorld:
                roleName = getattr(self.target, 'roleName', '')
                npcId = self.target.npcId
            self.taskInfo['roleName'] = roleName
            self.taskInfo['itemaIcon'] = ''
            self.taskInfo['targetId'] = str(npcId)
        else:
            data = ID.data.get(self.target, {})
            self.taskInfo['roleName'] = data.get('name', '')
            self.taskInfo['itemaIcon'] = uiUtils.getItemIconFile64(self.target)
        for i, taskType in enumerate(TASK_TYPE):
            isLoop = TASK_LOOP[i]
            taskArr = self.taskInfo.get(taskType, {})
            p = BigWorld.player()
            self.speakEvents[taskType] = []
            for i, task in enumerate(taskArr):
                if task.get('speakEvents', None):
                    self.speakEvents[taskType].append(task.get('speakEvents', None))
                perfect = not (taskType == 'complete_tasks' or taskType == 'complete_taskLoops')
                exp, money, _, yuanshen = commQuest.calcRewardByProgress(p, task.get('id', 0), task.get('questLoopId', 0), perfect)
                randType = gametypes.QUEST_LOOP_SELECT_SEQUENCE
                tmpID = 0
                if isLoop:
                    questId = task['questLoopId']
                    randType = QLD.data.get(questId, {}).get('ranType', gametypes.QUEST_LOOP_SELECT_SEQUENCE)
                    tmpID = questId
                    task['randType'] = randType
                else:
                    questId = task['id']
                if QD.data.get(task['id'], {}).get('triggerPartial', 0):
                    task['expBonus'] = int(exp)
                    task['goldBonus'] = int(money)
                    task['socExp'] = 0
                    task['randType'] = gametypes.QUEST_LOOP_SELECT_SEQUENCE
                elif task.has_key('expBonus') and task.has_key('goldBonus') and task.has_key('socExp'):
                    pass
                else:
                    bonusFactor = p.getQuestData(task['id'], const.QD_BONUS_FACTOR, 1.0)
                    cash = p.getQuestData(task['id'], const.QD_QUEST_CASH, 0)
                    expBonus = self.getQuestCurExp(task['id'])
                    socExp = p.getQuestData(task['id'], const.QD_QUEST_SOCEXP, 0)
                    task['expBonus'] = int(expBonus * bonusFactor)
                    task['goldBonus'] = int(cash * bonusFactor)
                    task['socExp'] = int(socExp * bonusFactor)
                fame = task.get('compFame', [])
                fameArray = []
                showFameText = True
                qd = {}
                if isLoop:
                    if randType == gametypes.QUEST_LOOP_SELECT_SEQUENCE:
                        qd = QD.data.get(task['id'], {})
                    else:
                        qd = QLD.data.get(questId, {})
                else:
                    qd = QD.data.get(questId, {})
                if taskType == 'available_taskLoops' and randType != gametypes.QUEST_LOOP_SELECT_SEQUENCE and (task['displayType'] == gametypes.QUEST_DISPLAY_TYPE_SCHOOL_DAILY or not qd.get('showFameText', 1)):
                    showFameText = False
                    fame = qd.get('starTextFame', fame)
                for fameId, fameScore in fame:
                    fameName = FD.data.get(fameId, {}).get('name', '')
                    fameArray.append((fameName, fameScore))

                if yuanshen > 0:
                    fameArray.append((gameStrings.SPIRIT, yuanshen))
                cashRewardType = gametypes.QUEST_CASHREWARD_BIND
                rewardMode = QD.data.get(task['id'], {}).get('reward')
                if rewardMode:
                    cashRewardType = QRD.data.get(rewardMode, {}).get('cashRewardType', gametypes.QUEST_CASHREWARD_BIND)
                task['cashRewardType'] = cashRewardType
                guildReward = QD.data.get(task['id'], {}).get('guildReward', 0)
                task['guildReward'] = guildReward
                rewardList = []
                for it in task['rewardChoice']:
                    rewardList.append(self.createItemInfo(it))

                task['reward'] = rewardList
                mRewardList = []
                for it in task['rewardItems']:
                    mRewardList.append(self.createItemInfo(it))

                mGroupLeaderList = []
                groupHeaderItems = task.get('groupHeaderItems', [])
                for it in groupHeaderItems:
                    mGroupLeaderList.append(self.createItemInfo(it))

                task['mGroupLeader'] = mGroupLeaderList
                if QD.data.get(task['id'], {}).get('triggerPartial', 0):
                    progress, rewardId, prop = commQuest.getRewardByQuestProgress(p, task['id'], perfect)
                    fixedBonus = BD.data.get(rewardId, {}).get('fixedBonus', ())
                    fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
                    if fixedBonus and type(fixedBonus) in (tuple, list):
                        for bType, bId, bNum in fixedBonus:
                            if bType == gametypes.BONUS_TYPE_GUILD_CONTRIBUTION:
                                fameArray.append((gameStrings.CONTRIBUTION, bNum))
                            elif bType == gametypes.BONUS_TYPE_ITEM:
                                mRewardList.append(self.createItemInfo([bId, bNum]))

                task['mReward'] = mRewardList
                task['compFame'] = fameArray
                if task.get('hasExtraReward', False):
                    extraRewardList = []
                    for it in task['extraRewardChoice']:
                        extraRewardList.append(self.createItemInfo(it))

                    task['extraReward'] = extraRewardList
                    extraMRewardList = []
                    for it in task['extraRewardItems']:
                        extraMRewardList.append(self.createItemInfo(it))

                    task['extraMReward'] = extraMRewardList
                    extraCash = p.getQuestData(task['id'], const.QD_EXTRA_QUEST_CASH, 0)
                    extraExpBonus = p.getQuestData(task['id'], const.QD_EXTRA_QUEST_EXP, 0)
                    task['extraExpBonus'] = extraExpBonus
                    task['extraGoldBonus'] = extraCash
                    task['hasExtraReward'] = 1
                if task.get('questLoopId', -1) > 0:
                    loopItems = commQuest.getQuestLoopRewardItem(p, task.get('questLoopId', -1))
                    if loopItems:
                        loopReward = []
                        for loopItem in loopItems:
                            loopReward.append(self.createItemInfo(loopItem))

                        loopItems = commQuest.getQuestFirstLoopRewardItem(p, task.get('questLoopId', -1))
                        if loopItems:
                            for loopItem in loopItems:
                                loopReward.append(self.createItemInfo(loopItem))

                        task['hasLoopReward'] = True
                        task['loopReward'] = loopReward
                loopRewardItems = []
                if task.get('loopRewardItems', None):
                    for it in task['loopRewardItems']:
                        loopRewardItems.append(self.createItemInfo(it))

                    task['loopRewardItems'] = loopRewardItems
                nameArr = []
                idArr = []
                if self.isNPC:
                    for it in task['speaker_ids']:
                        if it == 0:
                            nameArr.append(p.schoolSwitchName)
                        else:
                            nameArr.append(NCD.data.get(it, {}).get('name', ''))
                        idArr.append(it)

                else:
                    nameArr.append(ID.data.get(self.target, {}).get('name', ''))
                asideId = []
                for it in task['aside']:
                    asideId.append(it)

                showText = True
                if taskType == 'available_taskLoops':
                    if randType != gametypes.QUEST_LOOP_SELECT_SEQUENCE and guildReward == 0:
                        showText = False
                    if p._isFirstClueQuest(task['id'], questId):
                        showText = False
                if tmpID:
                    task['id'] = tmpID
                questName = qd.get('name', '')
                questDesc = qd['shortDesc'] if qd.has_key('shortDesc') else qd.get('desc', '')
                task['speakerName'] = nameArr
                task['asideIds'] = asideId
                task['npcId'] = task['questNpcId']
                task['idList'] = idArr
                task['questName'] = questName
                task['questDesc'] = questDesc
                task['showText'] = showText
                task['showFameText'] = showFameText

    def initAnimData(self):
        animMc = self.widget.right.chatHistory
        animMc.enableAnim = True
        anim = animMc.canvas.anim
        anim.gotoAndStop(1)
        if self.npcAnimList and self.selfAnimList:
            animMc.setAnimationPath([self.npcAnimList, self.selfAnimList])
            return
        totalFrames = anim.totalFrames - 1
        preNpcPosX = -1
        preNpcPosY = -1
        preSelfPosX = -1
        preSelfPosY = -1
        npcOriginPosX = anim.npcMc.x
        npcOriginPosY = int(anim.npcMc.y)
        selfOriginPosX = anim.selfMc.x
        selfOriginPosY = int(anim.selfMc.y)
        for i in xrange(820, 0, -1):
            key = '%d_%d' % (npcOriginPosY + i, npcOriginPosY + i - 1)
            self.npcAnimList.append({'key': key,
             'x': npcOriginPosX,
             'y': npcOriginPosY,
             'alpha': 0,
             'scaleX': 0,
             'scaleY': 0})
            key = '%d_%d' % (selfOriginPosY + i, selfOriginPosY + i - 1)
            self.selfAnimList.append({'key': key,
             'x': selfOriginPosX,
             'y': selfOriginPosY,
             'alpha': 0,
             'scaleX': 0,
             'scaleY': 0})

        for i in xrange(1, totalFrames):
            anim.gotoAndStop(i)
            npcPosX = anim.npcMc.x
            npcPosY = anim.npcMc.y
            npcAlpha = anim.npcMc.alpha
            npcScaleX = anim.npcMc.scaleX
            npcScaleY = anim.npcMc.scaleY
            if preNpcPosY == -1:
                preNpcPosY = npcPosY
            key = '%f_%f' % (preNpcPosY, npcPosY)
            self.npcAnimList.append({'key': key,
             'x': npcPosX,
             'y': npcPosY,
             'alpha': npcAlpha,
             'scaleX': npcScaleX,
             'scaleY': npcScaleY})
            preNpcPosX = npcPosX
            preNpcPosY = npcPosY
            selfPosX = anim.selfMc.x
            selfPosY = anim.selfMc.y
            selfAlpha = anim.selfMc.alpha
            selfScaleX = anim.selfMc.scaleX
            selfScaleY = anim.selfMc.scaleY
            if preSelfPosY == -1:
                preSelfPosY = selfPosY
            key = '%f_%f' % (preSelfPosY, selfPosY)
            self.selfAnimList.append({'key': key,
             'x': selfPosX,
             'y': selfPosY,
             'alpha': selfAlpha,
             'scaleX': selfScaleX,
             'scaleY': selfScaleY})
            preSelfPosX = selfPosX
            preSelfPosY = selfPosY

        preNpcPosY = int(preNpcPosY)
        preSelfPosY = int(preSelfPosY)
        for i in xrange(0, -410, -1):
            key = '%d_%d' % (preNpcPosY + i, preNpcPosY + i - 1)
            self.npcAnimList.append({'key': key,
             'x': preNpcPosX,
             'y': preNpcPosY,
             'alpha': 0,
             'scaleX': 0,
             'scaleY': 0})
            key = '%d_%d' % (preSelfPosY + i, preSelfPosY + i - 1)
            self.selfAnimList.append({'key': key,
             'x': preSelfPosX,
             'y': preSelfPosY,
             'alpha': 0,
             'scaleX': 0,
             'scaleY': 0})

        animMc.setAnimationPath([self.npcAnimList, self.selfAnimList])

    def initMcData(self):
        self.animMCs = []
        self.offset = []
        self.targetPos = []
        animMc = self.widget.right.chatHistory
        itemMc = None
        posY = 791
        for idx, npcId in enumerate(self.npcIds):
            if npcId:
                itemMc = self.widget.getInstByClsName('NpcV2_NpcAnim')
                itemMc.idx = 0
                itemMc.icon.photo2D.fitSize = True
                self.loadNpcPhoto(itemMc.icon.photo2D, npcId)
            else:
                itemMc = self.widget.getInstByClsName('NpcV2_SelfAnim')
                itemMc.idx = 1
            if idx < len(self.words):
                itemMc.textField.htmlText = self.words[idx]
            itemMc.textField.height = itemMc.textField.textHeight + 5
            itemMc.bg.height = itemMc.textField.height + 25
            itemMc.y = posY
            itemMc.ignoreAlpha = 0
            posY += itemMc.bg.height + 40
            self.offset.append(itemMc.bg.height + 40)
            self.animMCs.append(itemMc)

        self.spaceCondition = True
        if self.curTaskType == 'complete_tasks' or self.curTaskType == 'complete_taskLoops':
            self.openQuestPanel(True, True)
        elif self.curTaskType == 'available_tasks' or self.curTaskType == 'available_taskLoops':
            self.openQuestPanel(False, False)
        else:
            self.openQuestPanel(False, True)
        questMc = self.questMc
        questMc.y = posY
        questMc.idx = 1
        questMc.ignoreAlpha = 1
        self.animMCs.append(questMc)
        if questMc.questBg.visible:
            self.offset.append(questMc.questBg.height + 40)
        else:
            self.offset.append(questMc.btn.height + 40)
        for i, itemMc in enumerate(self.animMCs):
            self.targetPos.append([itemMc.y])
            pos = self.targetPos[i]
            for offset in self.offset:
                pos.append(pos[len(pos) - 1] - offset)

        animMc.initAnimationMc(self.animMCs)

    def createItemInfo(self, item):
        p = BigWorld.player()
        it = Item(item[0])
        itemInfo = {}
        itemInfo['id'] = item[0]
        itemInfo['name'] = 'item'
        itemInfo['iconPath'] = uiUtils.getItemIconFile64(it.id)
        itemInfo['count'] = item[1]
        if not it.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p):
            itemInfo['state'] = uiConst.EQUIP_NOT_USE
        else:
            itemInfo['state'] = uiConst.ITEM_NORMAL
        quality = ID.data.get(item[0], {}).get('quality', 1)
        qualitycolor = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
        itemInfo['qualitycolor'] = qualitycolor
        return itemInfo

    def handleResize(self, *args):
        if not self.widget:
            return
        scalex = self.widget.stage.stageWidth / (SWF_W * self.widget.scaleX)
        scaley = self.widget.stage.stageHeight / (SWF_H * self.widget.scaleY)
        scale = scalex
        if scaley > scalex:
            scale = scaley
        if scale > 1:
            scale = 1
        self.widget.width = self.widget.stage.stageWidth
        self.widget.height = self.widget.stage.stageHeight
        self.widget.bottom.scaleX = scalex
        self.widget.bottom.scaleY = scalex
        ctrlBtnGroup = self.widget.bottom.controlBtnGroup
        x0, y0 = ASUtils.global2Local(self.widget.bottom, self.widget.width - ctrlBtnGroup.getRect(self.widget.stage).width - 30 * scale, 0)
        ctrlBtnGroup.x = x0
        self.widget.bottom.y = self.widget.height - self.widget.bottom.height
        x1, y1 = ASUtils.local2Global(self.widget.bottom.chatWindow, 0, self.widget.bottom.chatWindow.npcSlot0.y)
        x2, y2 = ASUtils.local2Global(self.widget.bottom.chatWindow, 0, self.widget.bottom.chatWindow.bottomBg.y)
        self.widget.rightBg.scaleX = scale
        self.widget.rightBg.scaleY = scale
        self.widget.rightBg.x = self.widget.width - self.widget.rightBg.width
        self.widget.rightBg.y = self.widget.height - self.widget.rightBg.height - self.widget.bottom.height + y2 - y1 + 5
        self.widget.right.scaleX = scale
        self.widget.right.scaleY = scale
        self.widget.right.x = self.widget.width - self.widget.right.width
        self.widget.right.y = self.widget.rightBg.y - 22 * scale
        self.widget.largePhoto.width = self.widget.width
        self.widget.largePhoto.height = self.widget.width
        self.widget.largePhoto.x = 0
        self.widget.largePhoto.y = -(self.widget.largePhoto.height - self.widget.height) * 0.5

    def getQuestCurExp(self, questId):
        expBase = BigWorld.player().getQuestData(questId, const.QD_QUEST_EXP, 0)
        qd = QD.data.get(questId, {})
        if qd.has_key('satisfactionClientFormula'):
            satisfunc = FMLCD.data.get(qd.get('satisfactionClientFormula'), {}).get('formula')
            if satisfunc:
                factor = satisfunc({'satisfaction': BigWorld.player().carrierSatisfaction})
                expTotal = expBase * factor
                return expTotal
        return expBase

    def enterStage(self):
        if self.isShow:
            self.removeChild(self.questMc)
            self.initUI()
        else:
            p = BigWorld.player()
            if p.inBooth():
                p.showGameMsg(GMDD.data.SHOW_NPC_PANEL_ERROR_IN_BOOTH, '')
                return
            if not self.uiAdapter.enableUI:
                p.showUI(True)
            if self.uiAdapter.autoQuest.isShow():
                self.uiAdapter.autoQuest.hide()
            if self.uiAdapter.map.isShow:
                self.uiAdapter.map.realClose()
            self.uiAdapter.hideAllUI()
            p.ap.stopMove(True)
            p.ap.forceAllKeysUp()
            p.lockKey(gameglobal.KEY_POS_UI)
            BigWorld.setDofTransitTime(0.5)
            BigWorld.setDepthOfField(True, 5, 0.15)
            p.hideTopLogo(True)
            if p.pkMode == const.PK_MODE_KILL or p.pkMode == const.PK_MODE_HOSTILE:
                p.topLogo.stopPKLogo()
            gameglobal.rds.sound.playSound(gameglobal.SD_92)
            self.isShow = True
            self.uiAdapter.loadWidget(uiConst.WIDGET_NPC_V2)

    def leaveStage(self):
        if self.closeCallback:
            self.closeCallback()
        if self.callback:
            BigWorld.cancelCallback(self.callback)
        if self.largeHead:
            self.largeHead.endCapture()
        p = BigWorld.player()
        p.unlockKey(gameglobal.KEY_POS_UI)
        if gameglobal.rds.ui.isHideAllUI():
            self.uiAdapter.restoreUI()
        self.uiAdapter.chat.showView()
        BigWorld.resetDepthOfField()
        p.hideTopLogo(False)
        if p.pkMode == const.PK_MODE_KILL or p.pkMode == const.PK_MODE_HOSTILE:
            p.topLogo.updatePkTopLogo()
        gameglobal.rds.sound.playSound(gameglobal.SD_93)
        gameglobal.rds.ui.messageBox.dismiss(uiConst.MESSAGEBOX_QUEST, False)
        if gameglobal.rds.ui.payItem.isShow:
            gameglobal.rds.ui.payItem.hide()
        self.hide()

    @ui.callFilter(1, False)
    def showQuest(self, taskInfo = None, target = None, isNPC = True, page = -1, pos = -1):
        if gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
            return
        if self.uiAdapter.npcInteractive.widget:
            return
        self.isNPC = isNPC
        self.taskInfo = taskInfo
        self.target = target
        self.page = page
        self.pos = pos
        self.speakEvents = {}
        self.speed = PLAY_NORMAL
        self.state = STATE_PLAY
        self.npcType = uiConst.NPC_QUEST
        self.enterStage()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_NPC_V2)

    def getQuestIdByQuestNpcId(self, questNpcId, chatId):
        npc = BigWorld.entities.get(questNpcId)
        if npc is None or not npc.inWorld:
            return 0
        else:
            drdData = DRD.data.get(npc.npcId, {})
            if not drdData.has_key('quests'):
                return 0
            questIds = drdData.get('quests', [])
            chatIds = drdData.get('chatIds', [])
            for i, questId in enumerate(questIds):
                if i < len(chatIds) and chatIds[i] == chatId:
                    return questId

            return 0

    def reAddQuestSlotTip(self):
        questMc = self.questMc
        if not questMc:
            return
        for i in xrange(questMc.numChildren):
            childMc = questMc.getChildAt(i)
            if childMc.slot:
                TipManager.addItemTipById(childMc.slot, childMc.slot.itemId)
