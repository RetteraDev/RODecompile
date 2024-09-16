#Embedded file name: /WORKSPACE/data/entities/client/questbox.o
import BigWorld
import const
import gameglobal
import utils
from iBox import IBox
import clientcom
from iDisplay import IDisplay
from helpers import tintalt
from sfx import sfx
from callbackHelper import Functor
from helpers import action as ACT
from guis import ui
from guis import cursor
from data import npc_model_client_data as NMCD
from data import item_data as ID
from data import quest_box_data as QBD
from data import sys_config_data as SCD
from cdata import font_config_data as FCD

class QuestBox(IBox, IDisplay):

    def __init__(self):
        super(QuestBox, self).__init__()

    def getItemData(self):
        md = NMCD.data.get(self.questBoxType, None)
        if not md:
            return {'model': gameglobal.defaultModelID,
             'dye': 'Default'}
        return md

    def getBoxTrapRange(self):
        pickNearDist = min(QBD.data.get(self.questBoxType, {}).get('useDist', 0), 10)
        if pickNearDist <= 0:
            pickNearDist = SCD.data.get('pickNearQuestBoxLength', 6)
        return pickNearDist

    def enterWorld(self):
        pickNearDist = min(QBD.data.get(self.questBoxType, {}).get('useDist', 0), 10)
        if pickNearDist <= 0:
            pickNearDist = SCD.data.get('pickNearQuestBoxLength', 6)
        self.trapId = BigWorld.addPot(self.matrix, pickNearDist, self.trapCallback)
        super(IBox, self).enterWorld()

    def set_visibility(self, old):
        if self.ownerID != 0 and self.ownerID != BigWorld.player().gbId:
            self.visibility = const.VISIBILITY_HIDE
        super(QuestBox, self).set_visibility(old)

    def afterModelFinish(self):
        super(QuestBox, self).afterModelFinish()
        self.refreshOpacityState()
        if QBD.data[self.questBoxType].get('collideRadius', False):
            self.collideWithPlayer = True
        self.updateBoxState()
        self.addLingShiExtraTint()

    def leaveWorld(self):
        super(QuestBox, self).leaveWorld()
        self.delLingShiExtraTint()

    def updateBoxState(self):
        if self.beHide:
            return
        self.setTargetCapsUse(self.isQuestValid())
        nmcd = NMCD.data.get(self.questBoxType, {})
        triggerEff = nmcd.get('triggerEff', [])
        if triggerEff:
            if self.isQuestValid():
                if triggerEff not in self.attachFx:
                    effScale = nmcd['effScale'] if nmcd.has_key('effScale') else nmcd.get('modelScale', 1)
                    fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
                     self.getEquipEffectPriority(),
                     self.model,
                     nmcd['triggerEff'],
                     sfx.EFFECT_UNLIMIT))
                    if fxs:
                        for fx in fxs:
                            fx.scale(effScale, effScale, effScale)

                        self.addFx(nmcd['triggerEff'], fxs)
            else:
                self.removeFx(triggerEff)
        if self.topLogo:
            if self.isQuestValid() and not QBD.data[self.questBoxType].get('topLogo', 0):
                self.topLogo.hide(False)
            else:
                self.topLogo.hide(True)

    def needBlackShadow(self):
        md = NMCD.data.get(self.questBoxType, {})
        noBlackUfo = md.get('noBlackUfo', False)
        return not noBlackUfo

    def use(self):
        p = BigWorld.player()
        if not self.isQuestValid():
            return
        if utils.isOccupied(self) and not utils.hasOccupiedRelation(p, self):
            return
        if p.checkCanDoAction():
            super(QuestBox, self).use()

    def showQuestBoxContent(self, content):
        itemList = []
        for itemId, wrap in content:
            icon = 'item/icon/%d.dds' % ID.data[itemId]['icon']
            name = ID.data[itemId]['name']
            itemList.append((icon,
             name,
             itemId,
             wrap))

    def closeQuestBox(self):
        pass

    def getModelScale(self):
        nd = NMCD.data.get(self.questBoxType, {})
        scale = nd.get('modelScale', 1.0)
        return (scale, scale, scale)

    def enterTopLogoRange(self, rangeDist = -1):
        if not self.firstFetchFinished:
            return
        super(QuestBox, self).enterTopLogoRange(rangeDist)
        if self.topLogo and self.isQuestValid():
            self.topLogo.setLogoColor(FCD.data['item', 0]['color'])
        self.refreshOpacityState()

    def refreshOpacityState(self):
        super(QuestBox, self).refreshOpacityState()
        self.updateBoxState()

    def onTargetCursor(self, enter):
        if enter and self.isQuestValid():
            if ui.get_cursor_state() == ui.NORMAL_STATE:
                ui.set_cursor_state(ui.TARGET_STATE)
                if (self.position - BigWorld.player().position).length > cursor.TALK_DISTANCE:
                    ui.set_cursor(cursor.usebox_dis)
                else:
                    ui.set_cursor(cursor.usebox)
                ui.lock_cursor()
        elif ui.get_cursor_state() == ui.TARGET_STATE:
            ui.reset_cursor()

    def hide(self, bHide, retainTopLogo = False):
        qbd = QBD.data.get(self.questBoxType, {})
        hideDelay = qbd.get('hideDelay', 0)
        beUsedAction = qbd.get('beUsedAction')
        if not self.beHide and bHide and hideDelay and beUsedAction:
            self.fashion.playAction((beUsedAction,), ACT.USE_ACTION)
            BigWorld.callback(hideDelay, Functor(self._realHide, bHide, retainTopLogo))
            return
        super(QuestBox, self).hide(bHide, retainTopLogo)

    def _realHide(self, bHide, retainTopLogo = False):
        super(QuestBox, self).hide(bHide, retainTopLogo)

    def showTargetUnitFrame(self):
        return False

    def getOpacityValue(self):
        if self.boxEmpty:
            return (gameglobal.OPACITY_HIDE, False)
        p = BigWorld.player()
        if self.ownerID != 0 and self.ownerID != getattr(p, 'gbId', 0):
            return (gameglobal.OPACITY_HIDE, False)
        qbd = QBD.data.get(self.questBoxType, {})
        if qbd.has_key('islingshi'):
            return clientcom.getEntityLingShiOpacityValue(qbd)
        return super(QuestBox, self).getOpacityValue()

    def isQuestValid(self):
        qbd = QBD.data.get(self.questBoxType, None)
        if not qbd:
            return False
        player = BigWorld.player()
        if qbd.has_key('quest'):
            questId = qbd['quest']
            if questId in player.quests and player.needQuestItems(qbd.get('questItems', ()), questId):
                return True
        if qbd.has_key('waQuest'):
            questId = qbd['waQuest']
            if questId in player.worldQuests and player.needWaQuestItems(qbd.get('questItems', ()), questId):
                return True
        return False

    def set_boxEmpty(self, old):
        self.refreshOpacityState()

    def getFKey(self):
        return QBD.data.get(self.questBoxType, {}).get('fKey', 0)

    def addLingShiExtraTint(self):
        p = BigWorld.player()
        if not getattr(p, 'lingShiFlag', False):
            return
        lingShiTintName = QBD.data.get(self.questBoxType, {}).get('lingShiTintName', '')
        if lingShiTintName:
            tintalt.ta_reset(self.allModels)
            tintalt.ta_add(self.allModels, lingShiTintName, tintType=tintalt.NPC_LINGSHI)

    def delLingShiExtraTint(self):
        tintalt.ta_reset(self.allModels)
