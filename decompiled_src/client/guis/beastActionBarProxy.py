#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/beastActionBarProxy.o
from gamestrings import gameStrings
import BigWorld
import Math
from Scaleform import GfxValue
import gameglobal
import uiConst
import utils
import const
from guis import uiUtils
from uiProxy import SlotDataProxy
from data import summon_beast_data as SBD
from data import sys_config_data as SCD
from data import pet_skill_data as PSD
from cdata import game_msg_def_data as GMDD
import gamelog
CALLBACK_TIME = 0.1
ACTION_NUM = 5
IDX_ACTION_CHAT = ACTION_NUM
IDX_ACTION_ATTACH = ACTION_NUM + 1
IDX_ACTION_RECLAIM = ACTION_NUM + 2

class BeastActionBarProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(BeastActionBarProxy, self).__init__(uiAdapter)
        self.mediator = None
        self.modelMap = {'closeWidget': self.onClose,
         'getKeyText': self.onGetKeyText,
         'notifySlotUse': self.onNotifySlotUse}
        self.type = 'beastActionBar'
        self.bindType = 'beastActionBar'
        self.actions = [[0, 0]] * 8
        self.binding = {}

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BEAST_ACTINO_BAR)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_BEAST_ACTINO_BAR:
            self.mediator = mediator
            self.refreshActionBar()

    def getSlotID(self, key):
        _idCon, idItem = key.split('.')
        return (0, int(idItem[4:]))

    def onGetKeyText(self, *arg):
        keyArr = self._createKeyText()
        return uiUtils.array2GfxAarry(keyArr, True)

    def onNotifySlotUse(self, *arg):
        key = arg[3][0].GetString()
        _, slotId = self.getSlotID(key)
        actionId = self.actions[slotId][0]
        if slotId == IDX_ACTION_CHAT:
            self.chat()
        elif slotId == IDX_ACTION_ATTACH:
            self.attachBeastt()
        elif slotId == IDX_ACTION_RECLAIM:
            self.reclaimBeast()
        else:
            self.useSkill(actionId)

    def getMoveToPos(self, petSkillData):
        p = BigWorld.player()
        actionPostionData = petSkillData.get('actionPosition', {}).get(p.fashion.modelID, (0, 0, 0))
        radius = actionPostionData[0]
        theta = actionPostionData[1]
        dstPos = utils.getRelativePosition(p.position, p.yaw, theta, radius)
        y_offset = actionPostionData[2]
        dstpos = Math.Vector3(dstPos[0], dstPos[1] + y_offset + p.getModelHeight(), dstPos[2])
        pos = BigWorld.findDropPoint(p.spaceID, dstpos)
        if pos:
            dstpos = pos[0]
        return dstpos

    def useSkill(self, actionId):
        petSkillData = PSD.data.get(actionId, {})
        if not petSkillData:
            return
        moveToPos = self.getMoveToPos(petSkillData)
        p = BigWorld.player()
        pet = p._getPet()
        if pet:
            tNext = pet.petSkills.get(actionId, {}).get('tNext', 0)
            gamelog.debug('-----m.l@beastActionBarProxy.useSkill', tNext, utils.getNow())
            if utils.getNow() < tNext:
                p.showGameMsg(GMDD.data.PET_ACTION_IN_CD, ())
                return
            if p.stateMachine.checkStatus(const.CT_USING_PET_SKILL):
                p.cell.usePetSkill(actionId, moveToPos)

    def getSlotValue(self, movie, idItem, idCon):
        dataObj = self.movie.CreateObject()
        iconPath = self.getActionIcon(self.actions[idItem][0], self.actions[idItem][1], idItem)
        dataObj.SetMember('name', GfxValue(iconPath))
        dataObj.SetMember('iconPath', GfxValue(iconPath))
        return dataObj

    def getBeastActions(self):
        pet = BigWorld.player()._getPet()
        if pet and pet.inWorld:
            beastId = pet.beastId
            return SBD.data.get(beastId, {}).get('petActions', ())
        else:
            return []

    def refreshActionBar(self):
        interactiveActions = self.getBeastActions()
        self.actions = []
        tips = []
        for action in interactiveActions:
            self.actions.append([action, 0])
            tips.append(PSD.data.get(action, {}).get('tip', ''))

        self.actions = self.actions[:ACTION_NUM]
        if len(self.actions) < ACTION_NUM:
            for _ in xrange(ACTION_NUM - len(self.actions)):
                self.actions.append([0, 0])
                tips.append('')

        self.actions.extend([[0, 0], [0, 0], [0, 0]])
        petChatTip = SCD.data.get('petChatTip', '')
        petAttachTip = SCD.data.get('petAttachTip', '')
        petReclaimTips = SCD.data.get('petReclaimTips', gameStrings.TEXT_BEASTACTIONBARPROXY_134)
        tips.extend([petChatTip, petAttachTip, petReclaimTips])
        if self.mediator:
            self.mediator.Invoke('refreshActionBar', uiUtils.array2GfxAarry(tips, True))

    def getActionIcon(self, actionId, level, idx):
        if idx == IDX_ACTION_CHAT:
            icon = SCD.data.get('BeastActionBarChatIcon', 0)
            if not icon:
                return 'notFound'
            else:
                return 'skill/icon/' + str(icon) + '.dds'
        elif idx == IDX_ACTION_ATTACH:
            icon = SCD.data.get('BeastActionBarAttachIcon', 0)
            if not icon:
                return 'notFound'
            else:
                return 'skill/icon/' + str(icon) + '.dds'
        elif idx == IDX_ACTION_RECLAIM:
            icon = SCD.data.get('BeastActionBarReclaimIcon', 1120)
            if not icon:
                return 'notFound'
            else:
                return 'skill/icon/' + str(icon) + '.dds'
        else:
            if actionId == 0:
                return 'notFound'
            petSkillData = PSD.data.get(actionId, {})
            icon = str(petSkillData.get('icon'))
            return 'skill/icon/' + icon + '.dds'

    def reclaimBeast(self):
        BigWorld.player().cell.unsummonPet()

    def attachBeastt(self):
        pass

    def chat(self):
        pass

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BEAST_ACTINO_BAR)
        if self.mediator:
            self.mediator.Invoke('show')
        self.refreshActionBar()

    def onClose(self, *arg):
        self.close()

    def close(self):
        self.clearWidget()
