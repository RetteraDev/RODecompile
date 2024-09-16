#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/npcAction.o
import random
import keys
import clientcom
import utils
from data import npc_model_client_data as NMCD
from data import npc_action_data as NAD

class NpcActionGroup(object):

    def __init__(self, owner, actGroupId = 1):
        super(NpcActionGroup, self).__init__()
        self.actGroupId = actGroupId
        self.owner = owner
        self.actionList = None

    def getActCaps(self):
        actCaps = NAD.data.get(self.actGroupId, {}).get('matchCaps', None)
        if not actCaps:
            return keys.CAPS_IDLE0
        return actCaps

    def getCollideAction(self, fashion):
        if NAD.data.has_key(self.actGroupId):
            collideActions = NAD.data[self.actGroupId].get('collideAct', None)
            return collideActions

    def getBoredAction(self, fashion):
        if NAD.data.has_key(self.actGroupId):
            boredActions = NAD.data[self.actGroupId].get('boredAct', None)
            boredProbability = NAD.data[self.actGroupId].get('boredPro', None)
            if not boredActions:
                return
            if not boredProbability:
                return boredActions
            return [clientcom.randomChoiceByProportion(boredActions, boredProbability)]

    def getTalkAction(self):
        if NAD.data.has_key(self.actGroupId):
            talkActions = NAD.data[self.actGroupId].get('talkAct', None)
            if not talkActions:
                return
            return random.choice(talkActions)

    def getAcceptAction(self):
        if NAD.data.has_key(self.actGroupId):
            acceptActions = NAD.data[self.actGroupId].get('acceptAct', None)
            if not acceptActions:
                return
            return random.choice(acceptActions)

    def getSubmitAction(self):
        if NAD.data.has_key(self.actGroupId):
            submitActions = NAD.data[self.actGroupId].get('submitAct', None)
            if not submitActions:
                return
            return random.choice(submitActions)

    def getLeaveAction(self):
        leaveActions = NAD.data.get(self.actGroupId, {}).get('leaveAct', None)
        if leaveActions:
            return random.choice(leaveActions)

    def getPhotoAction(self):
        photoAction = NAD.data.get(self.actGroupId, {}).get('photoAct', None)
        return photoAction


npcActionMap = {}

def getNpcActionGroup(owner):
    md = None
    if hasattr(owner, 'npcId'):
        md = NMCD.data.get(owner.npcId, None)
    elif hasattr(owner, 'typeID'):
        md = NMCD.data.get(owner.typeID, None)
    elif hasattr(owner, 'charType'):
        md = NMCD.data.get(owner.charType, None)
    elif hasattr(owner, 'questBoxType'):
        md = NMCD.data.get(owner.questBoxType, None)
    elif utils.instanceof(owner, 'MultiplayMovingPlatform'):
        md = NMCD.data.get(owner.getItemData().get('charType'), None)
    if md:
        actGroupId = getattr(owner, 'actGroupId', 0) if getattr(owner, 'actGroupId', 0) else md.get('actGroupid', None)
        return NpcActionGroup(owner, actGroupId)


global npcActionMap ## Warning: Unused global
