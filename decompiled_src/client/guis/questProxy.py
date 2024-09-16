#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/questProxy.o
from gamestrings import gameStrings
import time
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import const
import commQuest
import gamelog
import gametypes
import utils
import ui
from ui import gbk2unicode
from uiProxy import UIProxy
from guis import messageBoxProxy
from callbackHelper import Functor
from helpers import capturePhoto
from item import Item
from guis import hotkeyProxy
from guis import uiUtils
from guis import tipUtils
from data import dawdler_data as DRD
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
from data import item_data as ID
from data import npc_model_client_data as NCD
from data import quest_data as QD
from data import quest_loop_data as QLD
from cdata import font_config_data as FCD
from data import formula_client_data as FMLCD
from cdata import quest_reward_data as QRD
from data import fame_data as FD
from data import bonus_data as BD
from data import message_desc_data as MSGDD

class QuestProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(QuestProxy, self).__init__(uiAdapter)
        self.taskInfo = []
        self.modelMap = {'getQuestNames': self.onGetQuestNames,
         'acceptQuest': self.onAcceptQuest,
         'commitQuest': self.onCommitQuest,
         'clickCloseBtn': self.onClickCloseBtn,
         'setUnitType': self.onSetUnitType,
         'getTooltip': self.onGetToolTip,
         'setUnitIndex': self.onSetUnitIndex,
         'getNpcType': self.onGetNpcType,
         'registerQuest': self.onRegisterQuest,
         'chooseRewardClick': self.onChooseRewardClick,
         'checkAutoQuest': self.onCheckAutoQuest}
        self.modelId = 0
        self.firstLoad = False
        self.headGen = None
        self.isShow = False
        self.speakEvents = None
        self.target = None
        self.npcType = uiConst.NPC_QUEST
        self.mc = None
        self.openTime = 0
        self.callback = None
        self.twiceCheckBox = 0
        self.chooseRewardMsgBoxId = None

    def setCallback(self, callback):
        self.callback = callback

    def openQuestWindow(self, taskInfo = None, target = None, isNPC = True, page = -1, pos = -1):
        if gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
            return
        self.isNPC = isNPC
        self.taskInfo = taskInfo
        self.target = target
        self.page = page
        self.pos = pos
        self.speakEvents = {}
        self._openQuestWindow()

    def _openQuestWindow(self):
        self.uiAdapter.openQuestWindow(uiConst.NPC_QUEST)
        self.openTime = time.time()

    def takePhoto3D(self, npcId):
        if not self.headGen:
            self.headGen = capturePhoto.LargePhotoGen.getInstance('gui/taskmask.tga', 700)
        uiUtils.takePhoto3D(self.headGen, self.target, npcId)

    def onGetQuestNames(self, *arg):
        obj = self.movie.CreateObject()
        if gameglobal.rds.isSinglePlayer:
            obj.SetMember('chat', GfxValue('offline'))
            return obj
        obj.SetMember('chat', GfxValue(gbk2unicode(self.taskInfo.get('chat', ''))))
        obj.SetMember('hotkey', self.getHotkey())
        if self.isNPC:
            roleName = ''
            npcId = 0
            if self.target:
                roleName = self.target.roleName
                npcId = self.target.npcId
            obj.SetMember('roleName', GfxValue(gbk2unicode(roleName)))
            obj.SetMember('itemaIcon', GfxValue(''))
            obj.SetMember('targetId', GfxValue(str(npcId)))
        else:
            data = ID.data.get(self.target, {})
            obj.SetMember('roleName', GfxValue(gbk2unicode(data.get('name', ''))))
            obj.SetMember('itemaIcon', GfxValue(uiUtils.getItemIconFile64(self.target)))
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
        if self.taskInfo.has_key('ignoreButton'):
            obj.SetMember('ignoreButton', GfxValue(self.taskInfo['ignoreButton']))
        if self.taskInfo.has_key('ignorePanel'):
            obj.SetMember('ignorePanel', GfxValue(self.taskInfo['ignorePanel']))
        return obj

    def setTaskArray(self, typeName, isLoop = False):
        taskArr = self.taskInfo.get(typeName, {})
        player = BigWorld.player()
        ret = self.movie.CreateArray()
        self.speakEvents[typeName] = []
        for i, item in enumerate(taskArr):
            if item.get('speakEvents', None):
                self.speakEvents[typeName].append(item.get('speakEvents', None))
            objat = self.movie.CreateObject()
            objat.SetMember('name', GfxValue(gbk2unicode(item['name'])))
            objat.SetMember('displayType', GfxValue(item['displayType']))
            randType = gametypes.QUEST_LOOP_SELECT_SEQUENCE
            if isLoop:
                questId = item['questLoopId']
                randType = QLD.data.get(questId, {}).get('ranType', gametypes.QUEST_LOOP_SELECT_SEQUENCE)
                objat.SetMember('id', GfxValue(questId))
                objat.SetMember('randType', GfxValue(randType))
            else:
                questId = item['id']
                objat.SetMember('id', GfxValue(questId))
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
            perfect = not (typeName == 'complete_tasks' or typeName == 'complete_taskLoops')
            exp, money, _, yuanshen = commQuest.calcRewardByProgress(player, item.get('id', 0), item.get('questLoopId', 0), perfect)
            if QD.data.get(item['id'], {}).get('triggerPartial', 0):
                objat.SetMember('expBonus', GfxValue(int(exp)))
                objat.SetMember('goldBonus', GfxValue(int(money)))
                objat.SetMember('socExp', GfxValue(int(0)))
                objat.SetMember('randType', GfxValue(gametypes.QUEST_LOOP_SELECT_SEQUENCE))
            elif item.has_key('expBonus') and item.has_key('goldBonus') and item.has_key('socExp'):
                objat.SetMember('expBonus', GfxValue(int(item['expBonus'])))
                objat.SetMember('goldBonus', GfxValue(int(item['goldBonus'])))
                objat.SetMember('socExp', GfxValue(int(item['socExp'])))
            else:
                bonusFactor = player.getQuestData(item['id'], const.QD_BONUS_FACTOR, 1.0)
                cash = player.getQuestData(item['id'], const.QD_QUEST_CASH, 0)
                expBonus = self.getQuestCurExp(item['id'])
                socExp = player.getQuestData(item['id'], const.QD_QUEST_SOCEXP, 0)
                objat.SetMember('expBonus', GfxValue(int(expBonus * bonusFactor)))
                objat.SetMember('goldBonus', GfxValue(int(cash * bonusFactor)))
                objat.SetMember('socExp', GfxValue(int(socExp * bonusFactor)))
            fame = item.get('compFame', [])
            fameArray = []
            for fameId, fameScore in fame:
                fameName = FD.data.get(fameId, {}).get('name', '')
                fameArray.append((fameName, fameScore))

            if yuanshen > 0:
                fameArray.append((gameStrings.TEXT_GETSKILLPOINTPROXY_174, yuanshen))
            cashRewardType = gametypes.QUEST_CASHREWARD_BIND
            rewardMode = QD.data.get(item['id'], {}).get('reward')
            if rewardMode:
                cashRewardType = QRD.data.get(rewardMode, {}).get('cashRewardType', gametypes.QUEST_CASHREWARD_BIND)
            objat.SetMember('cashRewardType', GfxValue(cashRewardType))
            guildReward = QD.data.get(item['id'], {}).get('guildReward', 0)
            objat.SetMember('guildReward', GfxValue(guildReward))
            rewardList = []
            for it in item['rewardChoice']:
                rewardList.append(self.createItemInfo(it))

            objat.SetMember('reward', uiUtils.array2GfxAarry(rewardList, True))
            mRewardList = []
            for it in item['rewardItems']:
                mRewardList.append(self.createItemInfo(it))

            mGroupLeaderList = []
            groupHeaderItems = item.get('groupHeaderItems', [])
            for it in groupHeaderItems:
                mGroupLeaderList.append(self.createItemInfo(it))

            objat.SetMember('mGroupLeader', uiUtils.array2GfxAarry(mGroupLeaderList, True))
            if QD.data.get(item['id'], {}).get('triggerPartial', 0):
                progress, rewardId, prop = commQuest.getRewardByQuestProgress(player, item['id'], perfect)
                fixedBonus = BD.data.get(rewardId, {}).get('fixedBonus', ())
                fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
                if fixedBonus and type(fixedBonus) in (tuple, list):
                    for bType, bId, bNum in fixedBonus:
                        if bType == gametypes.BONUS_TYPE_GUILD_CONTRIBUTION:
                            fameArray.append((gameStrings.TEXT_CONST_7558, bNum))
                        elif bType == gametypes.BONUS_TYPE_ITEM:
                            mRewardList.append(self.createItemInfo([bId, bNum]))

            objat.SetMember('mReward', uiUtils.array2GfxAarry(mRewardList, True))
            objat.SetMember('compFame', uiUtils.array2GfxAarry(fameArray, True))
            if item.get('hasExtraReward', False):
                extraRewardList = []
                for it in item['extraRewardChoice']:
                    extraRewardList.append(self.createItemInfo(it))

                objat.SetMember('extraReward', uiUtils.array2GfxAarry(extraRewardList, True))
                extraMRewardList = []
                for it in item['extraRewardItems']:
                    extraMRewardList.append(self.createItemInfo(it))

                objat.SetMember('extraMReward', uiUtils.array2GfxAarry(extraMRewardList, True))
                extraCash = player.getQuestData(item['id'], const.QD_EXTRA_QUEST_CASH, 0)
                extraExpBonus = player.getQuestData(item['id'], const.QD_EXTRA_QUEST_EXP, 0)
                objat.SetMember('extraExpBonus', GfxValue(extraExpBonus))
                objat.SetMember('extraGoldBonus', GfxValue(extraCash))
                objat.SetMember('hasExtraReward', GfxValue(1))
            if item.get('questLoopId', -1) > 0:
                loopItems = commQuest.getQuestLoopRewardItem(player, item.get('questLoopId', -1))
                if len(loopItems) > 0:
                    loopReward = []
                    for loopItem in loopItems:
                        loopReward.append(self.createItemInfo(loopItem))

                    loopItems = commQuest.getQuestFirstLoopRewardItem(player, item.get('questLoopId', -1))
                    if len(loopItems) > 0:
                        for loopItem in loopItems:
                            loopReward.append(self.createItemInfo(loopItem))

                    objat.SetMember('hasLoopReward', GfxValue(True))
                    objat.SetMember('loopReward', uiUtils.array2GfxAarry(loopReward, True))
            loopRewardItems = []
            if item.get('loopRewardItems', None):
                for it in item['loopRewardItems']:
                    loopRewardItems.append(self.createItemInfo(it))

                objat.SetMember('loopRewardItems', uiUtils.array2GfxAarry(loopRewardItems, True))
                objat.SetMember('loopRewardDesc', GfxValue(gbk2unicode(item.get('loopRewardDesc', ''))))
            nameArr = self.movie.CreateArray()
            idArr = self.movie.CreateArray()
            if self.isNPC:
                k = 0
                for it in item['speaker_ids']:
                    if it == 0:
                        nameArr.SetElement(k, GfxValue(gbk2unicode(player.schoolSwitchName)))
                    else:
                        nameArr.SetElement(k, GfxValue(gbk2unicode(NCD.data.get(it, {}).get('name', ''))))
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
                if randType == gametypes.QUEST_LOOP_SELECT_SEQUENCE:
                    qd = QD.data.get(item['id'], {})
                else:
                    qd = QLD.data.get(questId, {})
            else:
                qd = QD.data.get(questId, {})
            showText = True
            if typeName == 'available_taskLoops':
                if randType != gametypes.QUEST_LOOP_SELECT_SEQUENCE and guildReward == 0:
                    showText = False
                if player._isFirstClueQuest(item['id'], questId):
                    showText = False
            showFameText = True
            if typeName == 'available_taskLoops' and randType != gametypes.QUEST_LOOP_SELECT_SEQUENCE and item['displayType'] == gametypes.QUEST_DISPLAY_TYPE_SCHOOL_DAILY:
                showFameText = False
            questName = qd.get('name', '')
            questDesc = qd['shortDesc'] if qd.has_key('shortDesc') else qd.get('desc', '')
            objat.SetMember('speakerName', nameArr)
            objat.SetMember('asideIds', asideId)
            objat.SetMember('interval', interval)
            objat.SetMember('npcId', GfxValue(item['questNpcId']))
            objat.SetMember('idList', idArr)
            objat.SetMember('questName', GfxValue(gbk2unicode(questName)))
            objat.SetMember('questDesc', GfxValue(gbk2unicode(questDesc)))
            objat.SetMember('showText', GfxValue(showText))
            objat.SetMember('showFameText', GfxValue(showFameText))
            ret.SetElement(i, objat)

        return ret

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

    def _getMsg(self, msgId, defaultMsg = ''):
        gmMsg = GMD.data.get(msgId, {})
        return gmMsg.get('text', defaultMsg)

    @ui.callFilter(1)
    def onAcceptQuest(self, *arg):
        idNum = arg[3][0].GetNumber()
        isLoop = arg[3][1].GetBool()
        p = BigWorld.player()
        gameglobal.rds.ui.messageBox.dismiss(uiConst.MESSAGEBOX_QUEST, False)
        if self.isNPC:
            if isLoop:
                if int(idNum) in p.questLoopInfo:
                    questIds = p.questLoopInfo[int(idNum)].getNextQuests(p)
                else:
                    questIds = commQuest.getAvaiNextQuestsInLoop(p, int(idNum), 0)
                isTeleport = False
                for questId in questIds:
                    if p.checkTeleport(questId, 1):
                        isTeleport = True
                        break

                if not p.checkQuestCompleteMsgBox(int(idNum), Functor(self.realAcceptQuestLoop, isTeleport, int(idNum))):
                    self.realAcceptQuestLoop(isTeleport, int(idNum))
            else:
                isteleport = p.checkTeleport(int(idNum), 1)
                if isteleport:
                    MBButton = messageBoxProxy.MBButton
                    buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(self.acceptQuest, self.target, int(idNum))), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1)]
                    msg = self._getMsg(GMDD.data.QUEST_ACCEPT_TELEPORT_CONFIRMATION, gameStrings.TEXT_QUESTPROXY_402)
                    gameglobal.rds.ui.messageBox.show(True, '', msg, buttons, False, 0, uiConst.MESSAGEBOX_QUEST)
                elif p.checkAcZaijuQst(int(idNum)):
                    MBButton = messageBoxProxy.MBButton
                    buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(self.acceptQuest, self.target, int(idNum))), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1)]
                    msg = self._getMsg(GMDD.data.QUEST_ACCEPT_ZAIJU_CONFIRMATION, gameStrings.TEXT_QUESTPROXY_407)
                    gameglobal.rds.ui.messageBox.show(True, '', msg, buttons, False, 0, uiConst.MESSAGEBOX_QUEST)
                elif p.checkAddBuff(int(idNum), 1):
                    MBButton = messageBoxProxy.MBButton
                    buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(self.acceptQuest, self.target, int(idNum))), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1)]
                    msg = self._getMsg(GMDD.data.QUEST_ACCEPT_ADD_BUFF_CONFIRMATION, gameStrings.TEXT_QUESTPROXY_412)
                    gameglobal.rds.ui.messageBox.show(True, '', msg, buttons, False, 0, uiConst.MESSAGEBOX_QUEST)
                else:
                    self.acceptQuest(self.target, int(idNum))
        else:
            gameglobal.rds.ui.quest.close(showCursor=True)
            p.cell.acceptQuestByItem(self.page, self.pos)

    def realAcceptQuestLoop(self, isTeleport, questLoopId):
        if isTeleport:
            MBButton = messageBoxProxy.MBButton
            buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(self.acceptQuestLoop, self.target, questLoopId)), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1)]
            msg = self._getMsg(GMDD.data.QUEST_ACCEPT_TELEPORT_CONFIRMATION, gameStrings.TEXT_QUESTPROXY_402)
            gameglobal.rds.ui.messageBox.show(True, '', msg, buttons, False, 0, uiConst.MESSAGEBOX_QUEST)
        else:
            self.acceptQuestLoop(self.target, questLoopId)

    @ui.callFilter(1)
    def onCommitQuest(self, *arg):
        idNum = int(arg[3][0].GetNumber())
        rewardChoice = int(arg[3][2].GetNumber())
        isLoop = arg[3][3].GetBool()
        gameglobal.rds.ui.messageBox.dismiss(uiConst.MESSAGEBOX_QUEST, False)
        if isLoop:
            questId = BigWorld.player().questLoopInfo[int(idNum)].getCurrentQuest()
            rewardData = commQuest.genQuestRewardChoice(self, questId) if questId else None
        else:
            questId = idNum
            rewardData = commQuest.genQuestRewardChoice(self, idNum)
        if rewardData:
            if rewardChoice == -1:
                MBButton = messageBoxProxy.MBButton
                buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235)]
                msg = self._getMsg(GMDD.data.QUEST_REWARD_CHOICE_PROMPT, gameStrings.TEXT_QUESTLOGPROXY_1583)
                self.chooseRewardMsgBoxId = gameglobal.rds.ui.messageBox.show(False, '', msg, buttons, False, 0, uiConst.MESSAGEBOX_QUEST)
                BigWorld.player().showGameMsg(GMDD.data.QUEST_NEED_SELECT_PRIZE, ())
                return
            if not BigWorld.player().checkRewardItems(int(questId), rewardChoice):
                MBButton = messageBoxProxy.MBButton
                buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(self.commitQuest, int(idNum), rewardChoice)), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1)]
                msg = self._getMsg(GMDD.data.QUEST_REWARD_UNMATCH_CONFIRMATION, gameStrings.TEXT_QUESTPROXY_456)
                gameglobal.rds.ui.messageBox.show(True, '', msg, buttons, False, 0, uiConst.MESSAGEBOX_QUEST)
                return
        p = BigWorld.player()
        if gameglobal.rds.configData.get('enableSummonedSprite', False) and getattr(p, 'summonSpriteList', {}) and not getattr(p, 'spriteBattleIndex', 0) and not getattr(p, 'summonedSpriteInWorld', None):
            qdData = QD.data.get(int(questId), {})
            if qdData:
                rewardMode = qdData.get('reward', 0)
                qrdData = QRD.data.get(rewardMode, {})
                spriteExp = qrdData.get('spriteExp', 0)
                spriteFami = qrdData.get('spriteFami', 0)
                if spriteExp or spriteFami:
                    if not gameglobal.rds.ui.messageBox.getCheckOnceData(uiConst.CHECK_ONCE_TYPE_SPRITE_EXP_OR_FAMI_ADD):
                        msg = self._getMsg(GMDD.data.QUEST_SPRITE_REWARD_EXP_OR_FAMI, '')
                        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.commitQuest, idNum, rewardChoice, isLoop), yesBtnText=gameStrings.TEXT_QUESTPROXY_473, isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_SPRITE_EXP_OR_FAMI_ADD)
                        return
        self.commitQuest(idNum, rewardChoice, isLoop)

    def commitQuest(self, idNum, rewardChoice, isLoop = False):
        questId = None
        p = BigWorld.player()
        if isLoop and int(idNum) in p.questLoopInfo:
            questId = p.questLoopInfo[int(idNum)].getCurrentQuest()
        else:
            questId = idNum
        if questId is None:
            return
        else:
            qdd = QD.data.get(questId, {})
            if qdd.get('completeNeedComfirm', 0):
                msg = qdd.get('completeDoubleCheckMsg', gameStrings.TEXT_QUESTPROXY_493)
                label = qdd.get('completeDoubleCheckLabel', 'yes')
                title = gameStrings.TEXT_QUESTPROXY_495
                gameglobal.rds.ui.doubleCheckWithInput.show(msg, label, title, Functor(self.confirmCommitQuest, idNum, rewardChoice, isLoop))
            else:
                self.confirmCommitQuest(idNum, rewardChoice, isLoop)
            return

    def confirmCommitQuest(self, idNum, rewardChoice, isLoop):
        idNum = int(idNum)
        questId = None
        if isLoop:
            if idNum in BigWorld.player().questLoopInfo:
                questId = BigWorld.player().questLoopInfo[idNum].getCurrentQuest()
            if not questId:
                return
        else:
            questId = idNum
        qd = QD.data.get(questId, {})
        commitItem = qd.get('submitItem', ())
        if commitItem:
            submitItemDesc = qd.get('submitItemDesc', '')
            itemIds = [ item[0] for item in commitItem ]
            itemNums = [ item[1] for item in commitItem ]
            gameglobal.rds.ui.payItem.show(itemIds, itemNums, idNum, rewardChoice, questId, isLoop, submitItemDesc)
        else:
            self.autoCommitItem(idNum, rewardChoice, questId, isLoop)

    def delayConfirmTeleport(self, idNum, rewardChoice):
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(self.completeQuest, self.target, int(idNum), rewardChoice)), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1)]
        msg = self._getMsg(GMDD.data.QUEST_COMMIT_TELEPORT_CONFIRMATION, gameStrings.TEXT_QUESTPROXY_527)
        gameglobal.rds.ui.messageBox.show(True, '', msg, buttons, False, 0, uiConst.MESSAGEBOX_QUEST)

    def close(self, showCursor = False):
        gameglobal.rds.ui.messageBox.dismiss(uiConst.MESSAGEBOX_QUEST, False)
        if gameglobal.rds.ui.payItem.isShow:
            gameglobal.rds.ui.payItem.hide()
        self.uiAdapter.closeQuestWindow(showCursor)
        if self.callback:
            self.callback()
            self.callback = None
        self.chooseRewardMsgBoxId = None

    def onClickCloseBtn(self, *arg):
        gamelog.debug('onClickCloseBtn')
        if gameglobal.rds.ui.puzzle.visible:
            gameglobal.rds.ui.puzzle.hidePuzzle()
            return
        if self.npcType == uiConst.NPC_MULTI:
            self.uiAdapter.multiNpcChat.close()
            return
        if self.uiAdapter.funcNpc.isOnFuncState():
            self.uiAdapter.funcNpc.closeByInv()
        self.close()
        gameglobal.rds.sound.playSound(gameglobal.SD_97)

    def resetHeadGen(self):
        if not self.headGen:
            self.headGen = capturePhoto.LargePhotoGen.getInstance('gui/taskmask.tga', 700)
        self.headGen.endCapture()

    def initHeadGen(self):
        if not self.headGen:
            self.headGen = capturePhoto.LargePhotoGen.getInstance('gui/taskmask.tga', 700)
        self.headGen.initFlashMesh()

    def onSetUnitType(self, *arg):
        npcId = int(arg[3][0].GetString())
        self.takePhoto3D(npcId)

    def autoCommitItem(self, idNum, rewardChoice, questId, isLoop):
        completeFunc = self.completeQuestLoop if isLoop else self.completeQuest
        isteleport = BigWorld.player().checkTeleport(questId, 2)
        if isteleport:
            MBButton = messageBoxProxy.MBButton
            buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(completeFunc, self.target, int(idNum), rewardChoice)), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1)]
            msg = self._getMsg(GMDD.data.QUEST_COMMIT_TELEPORT_CONFIRMATION, gameStrings.TEXT_QUESTPROXY_527)
            gameglobal.rds.ui.messageBox.show(True, '', msg, buttons, False, 0, uiConst.MESSAGEBOX_QUEST)
        else:
            completeFunc(self.target, int(idNum), rewardChoice)

    def completeQuestLoop(self, target, idNum, rewardChoice):
        p = BigWorld.player()
        if QLD.data.get(idNum, {}).get('teamQuest', 0) and p.groupHeader and p.groupHeader != p.id:
            if p.groupType == gametypes.GROUP_TYPE_TEAM_GROUP:
                self.confirmBeforeCompleteLoop(target, idNum, rewardChoice)
                return
            if p.groupType == gametypes.GROUP_TYPE_RAID_GROUP:
                for _gbId, mVal in p.members.iteritems():
                    if mVal['id'] == p.groupHeader:
                        index1 = p.arrangeDict.get(_gbId, -1)
                        index2 = p.arrangeDict.get(p.gbId, -1)
                        if utils.isSameTeam(index1, index2):
                            self.confirmBeforeCompleteLoop(target, idNum, rewardChoice)
                            return

        elif QLD.data.get(idNum, {}).get('teamQuest', 0) and p.groupHeader and p.groupHeader == p.id and len(p.members) > 1:
            if QLD.data.get(idNum, {}).get('needPushToHeader', 0) and not gameglobal.rds.ui.messageBox.hasChecked('pushLoop'):
                options = {'rewardChoice': rewardChoice} if rewardChoice != -1 else {}
                target.pushToHeaderB4DoWithQuestLoop(idNum, 2, options)
                return
        if rewardChoice == -1:
            target.completeQuestLoop(idNum, {})
        else:
            target.completeQuestLoop(idNum, {'rewardChoice': rewardChoice})

    def confirmBeforeCompleteLoop(self, target, idNum, rewardChoice):
        if QLD.data.get(idNum, {}).get('needPushToHeader', 0):
            BigWorld.player().cell.getHeaderLoopProgress(gametypes.QUEST_STAGE_COMPLETE, idNum, target.id, rewardChoice)
            return
        msg = MSGDD.data.get('confirmBeforeCompQstLoop_msg', gameStrings.TEXT_QUESTPROXY_618)
        self.twiceCheckBox = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.doConfirmBeforeCompleteLoop, target, idNum, rewardChoice), yesBtnText=gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, noCallback=Functor(self.cancelConfirmBeforeCompleteLoop), noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1)

    def doConfirmBeforeCompleteLoop(self, target, idNum, rewardChoice):
        if rewardChoice == -1:
            target.completeQuestLoop(idNum, {})
        else:
            target.completeQuestLoop(idNum, {'rewardChoice': rewardChoice})
        self.twiceCheckBox = 0

    def cancelConfirmBeforeCompleteLoop(self):
        self.twiceCheckBox = 0

    def completeQuest(self, target, idNum, rewardChoice):
        if rewardChoice == -1:
            target.completeQuest(idNum, {})
        else:
            target.completeQuest(idNum, {'rewardChoice': rewardChoice})

    def acceptQuestLoop(self, target, idNum):
        p = BigWorld.player()
        if QLD.data.get(idNum, {}).get('teamQuest', 0) and p.groupHeader and p.groupHeader != p.id:
            if p.groupType == gametypes.GROUP_TYPE_TEAM_GROUP:
                self.confirmBeforeAcceptLoop(target, idNum)
                return
            if p.groupType == gametypes.GROUP_TYPE_RAID_GROUP:
                for _gbId, mVal in p.members.iteritems():
                    if mVal['id'] == p.groupHeader:
                        index1 = p.arrangeDict.get(_gbId, -1)
                        index2 = p.arrangeDict.get(p.gbId, -1)
                        if utils.isSameTeam(index1, index2):
                            self.confirmBeforeAcceptLoop(target, idNum)
                            return

        elif QLD.data.get(idNum, {}).get('teamQuest', 0) and p.groupHeader and p.groupHeader == p.id and len(p.members) > 1:
            if QLD.data.get(idNum, {}).get('needPushToHeader', 0) and not gameglobal.rds.ui.messageBox.hasChecked('pushLoop'):
                target.pushToHeaderB4DoWithQuestLoop(idNum, 1, {})
                return
        target.acceptQuestLoop(idNum)

    def onGetHeaderLoopProgress(self, questLoopId, npcId, info, checkStage, arg):
        myLoopCnt, myLoopStatus = info.get(BigWorld.player().id)
        headerLoopCnt, headerLoopStatus = info.get('header')
        msg = ''
        if headerLoopCnt > myLoopCnt:
            msg = gameStrings.TEXT_QUESTPROXY_669 % (headerLoopCnt, myLoopCnt)
        elif headerLoopCnt < myLoopCnt:
            msg = gameStrings.TEXT_QUESTPROXY_671 % (headerLoopCnt, myLoopCnt)
        elif headerLoopStatus == gametypes.QUEST_STAGE_ACCEPT:
            msg = gameStrings.TEXT_QUESTPROXY_673
        elif headerLoopStatus == gametypes.QUEST_STAGE_COMPLETE:
            if myLoopStatus == gametypes.QUEST_STAGE_ACCEPT:
                msg = gameStrings.TEXT_QUESTPROXY_676
            elif myLoopStatus == gametypes.QUEST_STAGE_COMPLETE:
                msg = gameStrings.TEXT_QUESTPROXY_678
        elif headerLoopStatus == myLoopStatus == 0:
            msg = gameStrings.TEXT_QUESTPROXY_678
        target = BigWorld.entities.get(npcId)
        if checkStage == gametypes.QUEST_STAGE_ACCEPT:
            self.twiceCheckBox = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.doConfirmBeforeAcceptLoop, target, questLoopId), yesBtnText=gameStrings.TEXT_QUESTPROXY_686, noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1, isModal=False, msgType='pushLoop', textAlign='center')
        else:
            self.twiceCheckBox = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.doConfirmBeforeCompleteLoop, target, questLoopId, arg), yesBtnText=gameStrings.TEXT_QUESTPROXY_686, noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1, isModal=False, msgType='pushLoop', textAlign='center')

    def confirmBeforeAcceptLoop(self, target, idNum):
        if QLD.data.get(idNum, {}).get('needPushToHeader', 0):
            BigWorld.player().cell.getHeaderLoopProgress(gametypes.QUEST_STAGE_ACCEPT, idNum, target.id, 0)
            return
        msg = MSGDD.data.get('confirmBeforeAcQstLoop_msg', gameStrings.TEXT_QUESTPROXY_696)
        self.twiceCheckBox = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.doConfirmBeforeAcceptLoop, target, idNum), yesBtnText=gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, noCallback=Functor(self.cancelConfirmBeforeAcceptLoop), noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1)

    def doConfirmBeforeAcceptLoop(self, target, idNum):
        target and target.acceptQuestLoop(idNum)
        self.twiceCheckBox = 0

    def cancelConfirmBeforeAcceptLoop(self):
        self.twiceCheckBox = 0

    def hideTwiceCheckBox(self):
        if self.twiceCheckBox:
            gameglobal.rds.ui.messageBox.dismiss(self.twiceCheckBox)
            self.twiceCheckBox = 0

    def acceptQuest(self, target, idNum):
        gamelog.debug('zt: acceptQuest', idNum, target.id)
        target.acceptQuest(idNum)

    def logQuestDialog(self, questId, isAccept):
        pass

    def onGetToolTip(self, *arg):
        taskId = int(arg[3][0].GetNumber())
        idx = int(arg[3][1].GetNumber())
        isLoop = arg[3][2].GetBool()
        p = BigWorld.player()
        itemId = 0
        if isLoop:
            questId = None
            if taskId in p.questLoopInfo:
                questId = p.questLoopInfo[taskId].getCurrentQuest()
                if not questId:
                    questIds = p.questLoopInfo[taskId].getNextQuests(p)
                    if len(questIds) > 0:
                        questId = questIds[0]
            else:
                questIds = commQuest.getAvaiNextQuestsInLoop(p, taskId, 0)
                if len(questIds) > 0:
                    questId = questIds[0]
            if not questId:
                return
            loopItems = commQuest.getQuestLoopRewardItem(BigWorld.player(), taskId)
            if QD.data.get(questId, {}).has_key('rewardChoice'):
                rewardChoiceItems = commQuest.genQuestRewardChoice(p, questId)
                itemId = rewardChoiceItems[idx][0]
            elif QD.data.get(questId, {}).has_key('rewardItems'):
                rewardItems = commQuest.genQuestRewardItems(p, questId, questId not in p.quests)
                itemId = rewardItems[idx][0]
            elif loopItems:
                itemId = loopItems[idx][0]
        else:
            rewardChoiceItems = commQuest.genQuestRewardChoice(p, taskId)
            rewardItems = commQuest.genQuestRewardItems(p, taskId)
            extraRwardChoiceItems = commQuest.genQuestExtraRewardChoice(p, taskId)
            extraRewardItems = commQuest.genQuestExtraRewardItems(p, taskId)
            items = []
            if rewardChoiceItems:
                items.extend(rewardChoiceItems)
            else:
                items.extend(rewardItems)
            if extraRwardChoiceItems:
                items.extend(extraRwardChoiceItems)
            else:
                items.extend(extraRewardItems)
            if idx < len(items):
                itemId = items[idx][0]
        if itemId == 0:
            return
        else:
            return tipUtils.getItemTipById(itemId)

    def onSetUnitIndex(self, *arg):
        cata = arg[3][0].GetString()
        curTaskIdx = int(arg[3][1].GetString())
        index = int(arg[3][2].GetString())
        if not self.speakEvents or not self.speakEvents.has_key(cata) or curTaskIdx >= len(self.speakEvents[cata]):
            return
        elif index >= len(self.speakEvents[cata][curTaskIdx]) or index < 0:
            return
        else:
            data = self.speakEvents[cata][curTaskIdx][index]
            try:
                for info in data:
                    if info[0] == gameglobal.ACT_FLAG and self.target:
                        acts = [ str(i) for i in info[1:] ]
                        self.target.fashion.playActionSequence(self.target.model, acts, None)
                    elif info[0] == gameglobal.VOICE_FLAG:
                        gameglobal.rds.sound.playSound(int(info[1]))

            except:
                gamelog.error('onSetUnitIndex', data)

            self.notfyQuestInfo(cata, curTaskIdx, index)
            return

    def notfyQuestInfo(self, cata, curTaskIdx, index):
        quests = self.taskInfo.get(cata, [])
        questId = 0
        chatId = 0
        if curTaskIdx < len(quests):
            questInfo = quests[curTaskIdx]
            chatId = questInfo.get('chatId', 0)
            questId = questInfo.get('id', 0)
        player = BigWorld.player()
        if hasattr(player, 'sendQuestDialog'):
            player.sendQuestDialog(questId, chatId, index)

    def getHotkey(self):
        key, mod, desc = hotkeyProxy.getPickAsKeyContent()
        gamelog.debug('getHotkey', key, mod, desc)
        hotkey = self.movie.CreateObject()
        hotkey.SetMember('key', GfxValue(key))
        hotkey.SetMember('mod', GfxValue(mod))
        hotkey.SetMember('desc', GfxValue(gbk2unicode(desc)))
        return hotkey

    def onGetNpcType(self, *arg):
        return GfxValue(self.npcType)

    def onRegisterQuest(self, *arg):
        self.mc = arg[3][0]
        self.initHeadGen()
        if hasattr(self.uiAdapter, 'tdHeadGen') and self.uiAdapter.tdHeadGen.headGenMode:
            self.uiAdapter.tdHeadGen.startCapture()

    def onChooseRewardClick(self, *arg):
        if self.chooseRewardMsgBoxId:
            gameglobal.rds.ui.messageBox.dismiss(self.chooseRewardMsgBoxId)

    def onCheckAutoQuest(self, *arg):
        if not gameglobal.rds.configData.get('enableAutoQuest', False):
            return GfxValue(False)
        p = BigWorld.player()
        isAutoQuest = False
        if self.npcType == uiConst.NPC_QUEST:
            if not p.checkInAutoQuest() and not p.checkInLastCompletedQuestTime():
                return GfxValue(False)
            cata = arg[3][0].GetString()
            curTaskIdx = int(arg[3][1].GetNumber())
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
        return GfxValue(isAutoQuest)

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
