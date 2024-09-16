#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impContract.o
from gamestrings import gameStrings
import gameglobal
from guis import ui
from guis import uiConst
from data import message_desc_data as MSGDD
from cdata import form_contract_data as FCD
from cdata import remove_contract_data as RCD
from data import intimacy_config_data as ICD
from callbackHelper import Functor

class ImpContract(object):

    @ui.checkInventoryLock()
    def formContract(self, npcId, friendId, style):
        msg = MSGDD.data.get('formContractDefault_msg', gameStrings.TEXT_IMPCONTRACT_19)
        cost = FCD.data.get(style, {}).get('cost', 0)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg % cost, Functor(self.doFormContract, npcId, friendId), yesBtnText=gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, noCallback=Functor(self.cancelFormContract, friendId), noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1)

    def doFormContract(self, npcId, friendId):
        self.cell.doFormContract(npcId, friendId, self.cipherOfPerson)

    def cancelFormContract(self, friendId):
        self.cell.onCancelFormContract(friendId)

    @ui.checkInventoryLock()
    def removeContract(self, npcId, friendId):
        msg = MSGDD.data.get('removeContractDefault_msg', gameStrings.TEXT_IMPCONTRACT_31)
        cost = RCD.data.get(1, {}).get('cost', 0)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg % cost, Functor(self.doRemoveContract, npcId, friendId), yesBtnText=gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, noCallback=Functor(self.cancelRemoveContract, friendId), noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1)

    def doRemoveContract(self, npcId, friendId):
        self.cell.doRemoveContract(npcId, friendId, self.cipherOfPerson)

    def cancelRemoveContract(self, friendId):
        self.cell.onCancelRemoveContract(friendId)

    @ui.checkInventoryLock()
    def onApplyIntimacyYearlyReward(self, npcEntId, friendId):
        msg = MSGDD.data.get('rewardIntimacyYearly_msg', gameStrings.TEXT_IMPCONTRACT_43)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onDoRewardIntimacyYearly, npcEntId, friendId), yesBtnText=gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, noCallback=Functor(self.cancelApplyIntimacyYearlyReward, friendId), noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1)

    def onDoRewardIntimacyYearly(self, npcId, friendId):
        self.cell.doRewardIntimacyYearly(npcId, friendId, self.cipherOfPerson)

    def onNotifyIntimacyYearly(self):
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_PUSH_INIMACY_YEARLY_REWARD)

    def gainIntimacyYearlyDone(self):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_PUSH_INIMACY_YEARLY_REWARD)

    def cancelApplyIntimacyYearlyReward(self, friendId):
        self.cell.doCancelApplyIntimacyYearlyReward(friendId)

    @ui.checkInventoryLock()
    def onApplyIntimacyRegister(self, npcEntId, friendId, registerType):
        msg = MSGDD.data.get('intimacyRegister_msg_%d' % registerType, gameStrings.TEXT_IMPCONTRACT_63)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onDoIntimacyRegister, npcEntId, friendId, registerType), yesBtnText=gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, noCallback=Functor(self.cancelApplyIntimacyRegister, friendId), noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1)

    def onDoIntimacyRegister(self, npcId, friendId, registerType):
        self.cell.doIntimacyRegister(npcId, friendId, registerType, self.cipherOfPerson)

    def cancelApplyIntimacyRegister(self, friendId):
        self.cell.doCancelApplyIntimacyRegister(friendId)

    @ui.checkInventoryLock()
    def onApplyIntimacyRegisterReward(self, npcEntId, friendId, registerType):
        msg = MSGDD.data.get('intimacyRegisterReward_msg_%d' % registerType, gameStrings.TEXT_IMPCONTRACT_77)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onDoIntimacyRegisterReward, npcEntId, friendId, registerType), yesBtnText=gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, noCallback=Functor(self.cancelApplyIntimacyRegisterReward, friendId), noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1)

    def onDoIntimacyRegisterReward(self, npcId, friendId, registerType):
        self.cell.doIntimacyRegisterReward(npcId, friendId, registerType, self.cipherOfPerson)

    def cancelApplyIntimacyRegisterReward(self, friendId):
        self.cell.doCancelApplyIntimacyRegisterReward(friendId)

    @ui.checkInventoryLock()
    def onUnbindFriendshipWithSingle(self):
        msg = MSGDD.data.get('unbindFriendMsg', gameStrings.TEXT_IMPCONTRACT_31)
        UNBIND_FRIENDSHIP_CASH = ICD.data.get('UNBIND_FRIENDSHIP_CASH', 300000)
        gameglobal.rds.ui.doubleCheckWithInput.show(msg % UNBIND_FRIENDSHIP_CASH, 'GOODBYE', title=gameStrings.TEXT_IMPCONTRACT_95, confirmCallback=self.doUnbindFriendshipWithSingle)

    def doUnbindFriendshipWithSingle(self):
        self.cell.doUnbindFriendshipWithSingle(self.cipherOfPerson)

    @ui.checkInventoryLock()
    def onUnbindFriendshipWithCoop(self):
        msg = MSGDD.data.get('unbindFriendMsgWithCoop', gameStrings.TEXT_IMPCONTRACT_103)
        UNBIND_FRIENDSHIP_CASH_WITH_COOP = ICD.data.get('UNBIND_FRIENDSHIP_CASH_WITH_COOP', 10000)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg % UNBIND_FRIENDSHIP_CASH_WITH_COOP, Functor(self.doApplyUnbindFriendshipWithCoop), yesBtnText=gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235)

    def doApplyUnbindFriendshipWithCoop(self):
        self.cell.doApplyUnbindFriendshipWithCoop(self.cipherOfPerson)

    def onCancelUnbindFriendshipWithCoop(self):
        msg = MSGDD.data.get('cancelUnbindFriendMsgWithCoop', gameStrings.TEXT_IMPCONTRACT_111)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.doCancelUnbindFriendshipWithCoop), yesBtnText=gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235)

    def doCancelUnbindFriendshipWithCoop(self):
        self.cell.doCancelUnbindFriendshipWithCoop()
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_APPLYED_UNBIND_FRIENDSHIP_WITH_COOP)

    def onAppliedUnbindFriendshipWithCoop(self):
        uiAdapter = gameglobal.rds.ui
        if uiAdapter:
            uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_APPLYED_UNBIND_FRIENDSHIP_WITH_COOP, {'click': self._appliedUnbindFriendshipPushIconClick})
            uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_APPLYED_UNBIND_FRIENDSHIP_WITH_COOP)

    def _appliedUnbindFriendshipPushIconClick(self):
        self.onCancelUnbindFriendshipWithCoop()
