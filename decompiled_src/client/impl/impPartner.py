#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPartner.o
from gamestrings import gameStrings
import BigWorld
import gamelog
import gameglobal
import const
from callbackHelper import Functor
from guis import ui
from guis import uiUtils
from guis import uiConst
from gamestrings import gameStrings
from data import partner_config_data as PCD
from data import title_data as TD
from cdata import game_msg_def_data as GMDD

class ImpPartner(object):

    def beApplyPartnerTeamName(self):
        gamelog.debug('@zq#partner beApplyPartnerTeamName')
        gameglobal.rds.ui.partnerTitleName.show()
        gameglobal.rds.ui.funcNpc.onFuncState()

    def _applyPartnerTeamName(self, preFixName, subfixName, middleStyle):
        gamelog.debug('@zq#partner _applyPartnerTeamName')
        self.cell.applyPartnerTeamName(preFixName, subfixName, middleStyle)

    def beComfirmPartnerTeamName(self, preFixName, subfixName, middleStyle):
        gamelog.debug('@zq#partner beComfirmPartnerTeamName')
        gameglobal.rds.ui.partnerTitleName.hide()
        if self.isHeader():
            self.cell.comfirmPartnerTeamName()
        else:
            self.getCipher(self._beComfirmPartnerTeamName, tuple((preFixName, subfixName, middleStyle)), self.cell.refusePartnerTeamName)

    def _beComfirmPartnerTeamName(self, cipher, preFixName, subfixName, middleStyle):
        name = self.connectPartnerTitleName(preFixName, subfixName, middleStyle, len(self.members))
        partnerTitleId = PCD.data.get('partnerTitleId', 0)
        tData = TD.data.get(partnerTitleId, {})
        name = uiUtils.toHtml(name, uiConst.TITLE_COLOR_DIC.get(tData.get('style', 0), ''))
        msg = gameStrings.PARTNER_TITLE_NAME_CONFIRM % name
        lmId = self.partnerMsgBox.get('beComfirmPartnerTeamName', None)
        if gameglobal.rds.ui.messageBox.isShow(lmId):
            gameglobal.rds.ui.messageBox.dismiss(lmId, needDissMissCallBack=False)
        mId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self.cell.comfirmPartnerTeamName, noCallback=self.cell.refusePartnerTeamName, yesBtnText=gameStrings.COMMON_CONFIRM, noBtnText=gameStrings.COMMON_CANCEL, canEsc=False)
        self.partnerMsgBox['beComfirmPartnerTeamName'] = mId

    def beComfirmAddPartner(self, newPartner):
        gamelog.debug('@zq#partner beComfirmAddPartner', newPartner)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()
        self.getCipher(self._beComfirmAddPartner, tuple((newPartner,)), self.cell.refuseAddPartner)

    def _beComfirmAddPartner(self, cipher, newPartner):
        nameArr = []
        for k, v in newPartner.iteritems():
            partnerNUID, gbId, roleName = v
            roleName = uiUtils.toHtml(roleName, uiConst.PARTNER_NAME_COLOR)
            nameArr.append(roleName)

        nameStr = gameStrings.TEXT_CHATPROXY_403.join(nameArr)
        msg = gameStrings.PARTNER_ADD_CONFIRM_TEXT % (nameStr,)
        lmId = self.partnerMsgBox.get('beComfirmAddPartner', None)
        if gameglobal.rds.ui.messageBox.isShow(lmId):
            gameglobal.rds.ui.messageBox.dismiss(lmId, needDissMissCallBack=False)
        mId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self.cell.comfirmAddPartner, noCallback=self.cell.refuseAddPartner, yesBtnText=gameStrings.COMMON_CONFIRM, noBtnText=gameStrings.COMMON_CANCEL, canEsc=False)
        self.partnerMsgBox['beComfirmAddPartner'] = mId

    def beApplyExitPartner(self):
        gamelog.debug('@zq#partner beApplyExitPartner')
        gameglobal.rds.ui.funcNpc.onFuncState()
        self.getCipher(self._beApplyExitPartner, tuple(()), self._cancelApplyExitPartner)

    def _beApplyExitPartner(self, cipher):
        curPartnerNum = len(self.partner)
        msg = ''
        if curPartnerNum <= const.PARTNER_MIN_NUM:
            msg = gameStrings.PARTNER_ACTIVE_QUIT_MINNUM % const.PARTNER_MIN_NUM
        else:
            msg = gameStrings.PARTNER_ACTIVE_QUIT
        lmId = self.partnerMsgBox.get('beApplyExitPartner', None)
        if gameglobal.rds.ui.messageBox.isShow(lmId):
            gameglobal.rds.ui.messageBox.dismiss(lmId, needDissMissCallBack=False)
        mId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self._comfirmApplyExitPartner, noCallback=self._cancelApplyExitPartner, yesBtnText=gameStrings.COMMON_CONFIRM, noBtnText=gameStrings.COMMON_CANCEL)
        self.partnerMsgBox['beApplyExitPartner'] = mId

    def _comfirmApplyExitPartner(self):
        gamelog.debug('@zq#partner _comfirmApplyExitPartner')
        self.cell.comfirmApplyExitPartner()
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.onDefaultState()

    def _cancelApplyExitPartner(self):
        gamelog.debug('@zq#partner _comfirmApplyExitPartner')
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.onDefaultState()

    def beChooseKickoutPartner(self):
        gamelog.debug('@zq#partner beChooseKickoutPartner')
        gameglobal.rds.ui.partnerRemove.show()
        gameglobal.rds.ui.funcNpc.onFuncState()

    def beKickoutPartner(self, kickoutRoleName):
        gamelog.debug('@zq#partner beKickoutPartner', kickoutRoleName)
        gameglobal.rds.ui.partnerRemove.hide()
        curPartnerNum = len(self.partner)
        msg = ''
        if curPartnerNum <= const.PARTNER_MIN_NUM:
            msg = gameStrings.PARTNER_REMOVE_CONFIRM_MINNUM_TEXT % (const.PARTNER_MIN_NUM, kickoutRoleName)
        else:
            msg = gameStrings.PARTNER_REMOVE_CONFIRM_TEXT % (kickoutRoleName,)
        lmId = self.partnerMsgBox.get('beKickoutPartner', None)
        if gameglobal.rds.ui.messageBox.isShow(lmId):
            gameglobal.rds.ui.messageBox.dismiss(lmId, needDissMissCallBack=False)
        mId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self.cell.comfirmKickoutPartner, noCallback=self.cell.refuseKickoutPartner, yesBtnText=gameStrings.COMMON_CONFIRM, noBtnText=gameStrings.COMMON_CANCEL, canEsc=False)
        self.partnerMsgBox['beKickoutPartner'] = mId

    def partnerQuery(self, partnerInfo):
        """
        \xe7\xbb\x93\xe4\xbc\xb4\xe5\xb0\x8f\xe9\x98\x9f\xe5\x8f\x98\xe5\x8a\xa8\xe6\x97\xb6\xef\xbc\x8c\xe4\xbc\x9a\xe9\x80\x9a\xe8\xbf\x87\xe8\xbf\x99\xe4\xb8\xaa\xe6\x8e\xa5\xe5\x8f\xa3\xe9\x80\x9a\xe7\x9f\xa5\xe7\xbb\x99\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf
        Args:
            partnerInfo:
            info[mGbId] = {
                'roleName':mVal.roleName,
                'school': mVal.school,
                'orderIndex': mVal.orderIndex,
                'level': mVal.level,
                'activation': mVal.activation,
                'isOn':mVal.box != None
            }
        Returns:
        
        """
        gamelog.debug('@zq#partner partner#partnerQuery:', partnerInfo)
        self.partner = partnerInfo
        gameglobal.rds.ui.systemButton.showPartnerNotify()

    def onAddPartnerSucc(self, mGbId, roleName):
        """
        \xe5\xa2\x9e\xe5\x8a\xa0\xe7\xbb\x93\xe4\xbc\xb4\xe4\xbc\x99\xe4\xbc\xb4\xe7\x9a\x84\xe6\x88\x90\xe5\x8a\x9f\xe5\x90\x8e\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        Args:
            mGbId:\xe6\x96\xb0\xe5\x8a\xa0\xe5\x85\xa5\xe6\x88\x90\xe5\x91\x98\xe7\x9a\x84gbId
            roleName:\xe6\x96\xb0\xe5\x8a\xa0\xe5\x85\xa5\xe6\x88\x90\xe5\x91\x98\xe7\x9a\x84roleName
        
        Returns:
        
        """
        gamelog.debug('@zq#partner partner#onAddPartnerSucc:', mGbId, roleName)

    def onAllComfirmPartnerName(self, entTime):
        gamelog.debug('@zq#partner partner#onAllComfirmPartnerName')
        gameglobal.rds.ui.partnerTips.show(entTime)

    def onBuildPartnerSucc(self):
        gamelog.debug('@zq#partner partner#onBuildPartnerSucc')
        gameglobal.rds.ui.partnerTips.hide()
        self.showGameMsg(GMDD.data.BUILD_PARTNER_SUCCESS, ())
        BigWorld.callback(1, Functor(self.partnerScenarioPlay))

    def onExitPartnerSucc(self):
        gamelog.debug('@zq#partner partner#onExitPartnerSucc')

    def onKickoutPartner(self, roleName):
        pass

    def onQueryPartnerMemberInfo(self, memberList):
        gamelog.debug('@hjx partner#onQueryPartnerMemberInfo:', memberList)
        self.getPersonalSysProxy().onGetPartnerInfo(memberList)

    def onPartnerEventFailByCause(self, msgId, msgArgs):
        """
        \xe9\x98\x9f\xe4\xbc\x8d\xe4\xb8\xad\xe7\x8e\xa9\xe5\xae\xb6\xe7\xa6\xbb\xe7\xba\xbf \xe8\xa2\xab\xe8\xb8\xa2 \xe7\xa6\xbb\xe5\xbc\x80\xe9\x98\x9f\xe4\xbc\x8d \xe7\x9a\x84\xe6\x97\xb6\xe5\x80\x99, \xe4\xbc\x9a\xe5\x8f\x96\xe6\xb6\x88part\xe4\xba\x8b\xe4\xbb\xb6\xe4\xbf\xa1\xe6\x81\xaf, \xe7\x84\xb6\xe5\x90\x8e\xe8\xb0\x83\xe7\x94\xa8\xe6\xaf\x8f\xe4\xb8\xaa\xe4\xba\xba\xe7\x9a\x84\xe8\xbf\x99\xe4\xb8\xaa\xe6\x96\xb9\xe6\xb3\x95
        Args:
            cause:\xe5\x8f\x8d\xe9\xa6\x88id, \xe5\xa6\x82\xe6\x9e\x9c\xe4\xbc\xa00 \xe8\xa1\xa8\xe7\xa4\xba\xe4\xb8\x8d\xe9\x9c\x80\xe8\xa6\x81\xe5\x8f\x8d\xe9\xa6\x88
            fRoleName:\xe7\xa6\xbb\xe7\xba\xbf\xe7\x9a\x84\xe7\x8e\xa9\xe5\xae\xb6
        
        Returns:
        """
        if msgId:
            self.showGameMsg(msgId, msgArgs)
        self.closePartnerConfirm()

    def closePartnerConfirm(self):
        for k, v in self.partnerMsgBox.iteritems():
            if v:
                gameglobal.rds.ui.messageBox.dismiss(v, needDissMissCallBack=False)

        gameglobal.rds.ui.partnerTips.hide()

    def getPartnerTitleNumStyle(self, midType, num):
        numStyle = ''
        middleType = PCD.data.get('partTitleNumStyle', {})
        try:
            numStyle = middleType.get(midType, ('', '', '', '', ''))[num - 1]
        except:
            numStyle = ''

        return numStyle

    def connectPartnerTitleName(self, pre, post, midType, num):
        name = ''.join((gameStrings.PARTNER_PRE_TITLE,
         gameStrings.COMMON_DIAN,
         pre,
         self.getPartnerTitleNumStyle(midType, num),
         post))
        return name

    def getCurPartnerTitleName(self):
        return self.connectPartnerTitleName(self.partnerSigPrefix, self.partnerSigPostfix, self.partnerSigMidType, self.partnerMemberCnt)

    @ui.callAfterTime()
    def refreshPartnerTitle(self):
        self.refreshToplogoTitle()
