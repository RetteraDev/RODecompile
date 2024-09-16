#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impInteractive.o
import BigWorld
import gameglobal
import random
import gamelog
from helpers import modelServer
from helpers import action
from data import interactive_action_data as ACAD
from data import interactive_chat_data as IACD
from data import interactive_emote_data as IAED
from data import interactive_data as ID
from data import interactive_type_data as ITD

class ImpInteractive(object):

    def interactiveSucc(self, objectId, entId):
        gamelog.debug('@hjx interactive#interactiveSucc:', objectId, entId)

    def interactiveTimeout(self, objectId):
        gamelog.debug('@hjx interactive#interactiveTimeout:', objectId)

    def onQuitInteractive(self, objectId):
        gamelog.debug('@hjx interactive#onQuitInteractive:', objectId)
        miniGameId = ID.data.get(objectId, {}).get('miniGameId', None)
        if miniGameId:
            gameglobal.rds.ui.miniGame.hide()

    def quitInteractiveObj(self):
        leaveAction = self.modelServer.getBindLeaveAction(modelServer.BIND_TYPE_INTERACTIVE_OBJ)
        self.realQuitInteractive()

    def realQuitInteractive(self):
        if self == BigWorld.player():
            ent = BigWorld.entities.get(self.interactiveObjectEntId, None)
            if ent and ent.inWorld:
                miniGameId = ID.data.get(ent.objectId, {}).get('miniGameId', None)
                if miniGameId:
                    gameglobal.rds.ui.miniGame.hide()
            self.cell.quitInteractive()

    def playInteractiveAction(self, interactiveActionId):
        self.cell.playInteractiveAction(interactiveActionId)

    def onPlayInteractiveAction(self, interactiveActionId):
        self.interactiveActionId = interactiveActionId
        actionData = ACAD.data.get(interactiveActionId, {})
        interactiveAction = actionData.get('interactiveAction')
        if interactiveAction:
            self.fashion.stopModelAction(self.modelServer.bodyModel)
            actions = []
            actions.append((interactiveAction,
             self.resetInteractiveIdleAction,
             0,
             action.INTERACTIVE_ACTION))
            self.fashion.playActionSequence2(self.modelServer.bodyModel, actions, action.INTERACTIVE_ACTION)
        interactiveChatId = actionData.get('interactiveChatId')
        chatData = IACD.data.get(interactiveChatId, {})
        msg = chatData.get('details', None)
        duration = chatData.get('duration', 1)
        if msg:
            self.topLogo.setChatMsg(msg, duration)
        interactiveEmote = actionData.get('interactiveEmote')
        emoteData = IAED.data.get(interactiveEmote, {})
        res = emoteData.get('res', None)
        if res:
            self.doEmote(res)
        scenarioName = actionData.get('scenarioName', '')
        if scenarioName:
            BigWorld.player().scenarioPlay(scenarioName, 0)
        gameglobal.rds.ui.interactiveActionBar.setCoolDown()

    def resetInteractiveIdleAction(self):
        if not self.inWorld:
            return
        if self.inInteractiveObject():
            self.modelServer.playInteractiveIdleAction()

    def playInteractiveSpecialIdle(self):
        if not self.inWorld:
            return
        else:
            if self.interactiveSpecialIdleCB:
                BigWorld.cancelCallback(self.interactiveSpecialIdleCB)
            if not self.inInteractiveObject():
                return
            boredIdleProb = self.fashion.boredIdleProbability
            if random.randint(0, 100) < boredIdleProb:
                interaciveSpecialIdle = self.fashion.getInteractiveSpecialIdle()
                if interaciveSpecialIdle:
                    self.fashion.playActionSequence(self.modelServer.bodyModel, (interaciveSpecialIdle,), self.resetInteractiveIdleAction)
                specialIdleChatId = self.fashion.getInteractiveSpecialIdleChatId()
                if specialIdleChatId:
                    chatData = IACD.data.get(specialIdleChatId, {})
                    msg = chatData.get('details', None)
                    duration = chatData.get('duration', 1)
                    if msg:
                        self.topLogo.setChatMsg(msg, duration)
                specialIdleEmote = self.fashion.getInteractiveSpecialIdleEmote()
                if specialIdleEmote:
                    self.doEmote(specialIdleEmote)
            self.interactiveSpecialIdleCB = BigWorld.callback(5, self.playInteractiveSpecialIdle)
            return

    def initInteractive(self, interactiveInfo):
        gamelog.debug('@hjx interactive#initInteractive:', interactiveInfo)
        self.interactiveInfo = interactiveInfo

    def updateInteractive(self, key, val):
        gamelog.debug('@hjx interactive#updateInteractive:', key, val)
        if not hasattr(self, 'interactiveInfo'):
            self.interactiveInfo = {}
        if not isinstance(self.interactiveInfo, dict):
            return
        oldVal = self.interactiveInfo.get(key, {})
        self.interactiveInfo[key] = val
        if self == BigWorld.player():
            gameglobal.rds.ui.interactiveObj.playRewardGain(val.get('index', 0))
            hideLetter = ITD.data.get(key, {}).get('hideLetter', 0)
            if not oldVal.get('hasDone') and val.get('index', 0) == 3 and not hideLetter:
                gameglobal.rds.ui.interactiveObj.showLetterWidget(key)
