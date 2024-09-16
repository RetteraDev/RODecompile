#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impCollectItem.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
from sfx import sfx
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
from data import collect_item_data as CID
from callbackHelper import Functor

class ImpCollectItem(object):

    def handInItemFailed(self, activityId, pos):
        self.showGameMsg(GMDD.data.COLLECT_ITEM_ACTIVITY_HANDIN_FAIL, ())

    def handInItemSuccess(self, activityId, roundInfo, pos):
        gameglobal.rds.ui.xinmoBook.refreshView(roundInfo)
        gameglobal.rds.ui.xinmoRecord.updateRoundInfo(roundInfo)
        gameglobal.rds.ui.xinmoBook.playSucItem(pos)

    def handInItemReplaceCheck(self, activityId, originItem, replaceItem):
        pass

    def onQueryRoundInfo(self, activityId, roundInfo):
        gameglobal.rds.ui.xinmoBook.show(activityId, roundInfo)
        gameglobal.rds.ui.xinmoRecord.updateRoundInfo(roundInfo)

    def onNotifyRoundFinish(self, activityId, subId, roundInfo):
        gameglobal.rds.ui.xinmoBook.playAnimation(roundInfo)
        gameglobal.rds.ui.xinmoRecord.updateRoundInfo(roundInfo)
        self.showGameMsg(GMDD.data.COLLECT_ITEM_ACTIVITY_ROUND_FINISH, ())
        relatedNpcs = CID.data.get(subId, {}).get('relatedNpcs', {})
        for entity in BigWorld.entities.values():
            if hasattr(entity, 'npcId') and relatedNpcs.has_key(entity.npcId):
                sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (gameglobal.EFFECT_MID,
                 gameglobal.EFF_NPC_BASIC_PRIORITY,
                 entity.model,
                 relatedNpcs[entity.npcId],
                 sfx.EFFECT_LIMIT,
                 gameglobal.EFFECT_LAST_TIME))

    def sendCollectItemDict(self, info):
        if not hasattr(self, 'collectItemDict'):
            self.collectItemDict = info
        else:
            self.collectItemDict.update(info)
        gameglobal.rds.ui.xinmoRecord.updateView()
        if gameglobal.rds.ui.xinmoRecord._checkActivityTime() and gameglobal.rds.ui.xinmoRecord._checkCollectItemSignUp():
            gameglobal.rds.ui.xinmoRecord.pushXinmoRecordMsg()
        gameglobal.rds.ui.xinmoRecord.updateBossCountDown()

    def signupCollectItemSuccess(self, activityId):
        self.showGameMsg(GMDD.data.COLLECT_ITEM_ACTIVITY_SIGNUP_SUCC, ())

    def onNotifyActivityFinish(self, activityId, roundInfo):
        self.showGameMsg(GMDD.data.COLLECT_ITEM_ACTIVITY_FINISHED, ())
        gameglobal.rds.ui.xinmoRecord.pushXinmoRecordMsg()
        gameglobal.rds.ui.xinmoRecord.updateRoundInfo(roundInfo)
        gameglobal.rds.ui.xinmoRecord.cancelBossCountDown()

    def useQumoFameCheck(self, activityId, originQumoFame, canAdd):
        msg = GMD.data.get(GMDD.data.XINMO_FORCE_USE_QUMO_SCORE, {}).get('text', gameStrings.TEXT_IMPCOLLECTITEM_60)
        msg = msg % (canAdd, originQumoFame - canAdd)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.forceUseQumoFame))

    def refreshPanel(self, activityId, roundInfo):
        gameglobal.rds.ui.xinmoBook.refreshView(roundInfo)
        gameglobal.rds.ui.xinmoRecord.updateRoundInfo(roundInfo)

    def forceUseQumoFame(self):
        self.base.useQumoFame(10234, 1)

    def onUseCollectItemBonusSucc(self, activityId):
        self.showGameMsg(GMDD.data.COLLECT_ITEM_ACTIVITY_USE_BONUS_SUCC, ())

    def pushCollectItemBonusMsg(self, activityId):
        gameglobal.rds.ui.xinmoRecord.pushXinmoRecordMsg()
