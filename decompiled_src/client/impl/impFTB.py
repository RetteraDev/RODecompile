#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impFTB.o
from gamestrings import gameStrings
import gameglobal
import gamelog
import utils
import math
import BigWorld
from guis.ui import turnUnicodeDict2Gbk
from guis import uiUtils
from guis import events
from guis import ftbWalletHelper
from gamestrings import gameStrings
from data import ftb_config_data as FCD
from cdata import game_msg_def_data as GMDD

class ImpFTB(object):
    """\xe4\xbc\x8f\xe7\xbe\xb2\xe9\x80\x9a\xe5\xae\x9d"""

    def onSignFTBLicense(self):
        """\xe7\xad\xbe\xe7\xbd\xb2\xe8\xae\xb8\xe5\x8f\xaf\xe8\xaf\x81"""
        gamelog.debug('@zhangkuo onSignFTBLicense')
        self.ftbDataDetail.updateLicenseData({'hasSigned': True})

    def onQueryFTBCondition(self, hasLicense, hasHome):
        """
        \xe6\x9f\xa5\xe8\xaf\xa2\xe5\x89\x8d\xe7\xbd\xae\xe6\x9d\xa1\xe4\xbb\xb6
        :param hasLicense: \xe6\x98\xaf\xe5\x90\xa6\xe6\x8b\xa5\xe6\x9c\x89\xe8\xae\xb8\xe5\x8f\xaf\xe8\xaf\x81 bool
        :param hasHome: \xe6\x98\xaf\xe5\x90\xa6\xe6\x8b\xa5\xe6\x9c\x89\xe5\xae\xb6\xe5\x9b\xad bool
        """
        gamelog.debug('@zhangkuo onQueryFTBCondition', hasLicense, hasHome)
        self.ftbDataDetail.updateConditionData(hasLicense, hasHome)
        if not hasHome:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.FTB_WARNING_BUY_HOME, self._confirmGotoBuyHome)
            return
        if not hasLicense:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.FTB_WARNING_GOTO_FTB_NPC, self._confirmGotoFtbNpc)
            return
        gameglobal.rds.ui.ftbExcavate.show()

    def onQueryFTBLicense(self, licenseNo, hasSigned, site):
        """
        \xe6\x9f\xa5\xe8\xaf\xa2\xe8\xae\xb8\xe5\x8f\xaf\xe8\xaf\x81\xe7\x9b\xb8\xe5\x85\xb3\xe4\xbf\xa1\xe6\x81\xaf
        :param licenseNo: \xe8\xae\xb8\xe5\x8f\xaf\xe8\xaf\x81\xe5\x8f\xb7 UINT64
        :param hasSigned: \xe6\x98\xaf\xe5\x90\xa6\xe5\xb7\xb2\xe7\xad\xbe\xe7\xbd\xb2 bool
        :param site: \xe9\x87\x87\xe6\x8e\x98\xe5\x9c\xb0\xe5\x9d\x80 str
        :return:
        """
        gamelog.debug('@zhangkuo onQueryFTBLicense', licenseNo, hasSigned, site)
        self.ftbDataDetail.updateLicenseData({'licenseNo': licenseNo,
         'hasSigned': hasSigned,
         'ftbSite': site})

    def onPushFtbTaskDetail(self, data):
        """
        \xe4\xbb\xbb\xe5\x8a\xa1\xe8\xaf\xa6\xe6\x83\x85
        :param data: {'curTasks':{taskId:value}, 'taskHistory': [(taskId, value, expire)]}
        :return:
        """
        gamelog.debug('@zhangkuo onQueryDigPowerDetail', data)
        self.ftbDataDetail.updateTaskList(data)

    def onPushDigState(self, isDigging):
        """
        \xe6\x8c\x96\xe7\x9f\xbf\xe7\x8a\xb6\xe6\x80\x81\xe5\x8f\x91\xe7\x94\x9f\xe5\x8f\x98\xe5\x8c\x96
        :param isDigging: \xe6\x98\xaf\xe5\x90\xa6\xe6\xad\xa3\xe5\x9c\xa8\xe6\x8c\x96\xe7\x9f\xbf bool
        :return:
        """
        gamelog.debug('@zhangkuo onPushDigState', isDigging)
        self.ftbDataDetail.updateIsDigging(isDigging, utils.getNow())
        if not isDigging:
            pointTicket = math.modf(self.ftbDataDetail.yaojingTicket)[0] * 100
            self.ftbDataDetail.updateEarningData({'totalNowEarning': 0.0,
             'yaojingTicket': pointTicket})

    def onFTBBonus(self, total, point):
        """
        \xe6\x8c\x96\xe7\x9f\xbf\xe4\xba\xa7\xe7\x94\x9f\xe7\x9a\x84\xe4\xbc\x8f\xe7\xbe\xb2\xe9\x80\x9a\xe5\xae\x9d\xe6\x94\xb6\xe7\x9b\x8a
        :param total: \xe6\x9c\xac\xe6\xac\xa1\xe6\x8c\x96\xe7\x9f\xbf\xe6\x80\xbb\xe6\x94\xb6\xe7\x9b\x8a float
        :param point: \xe6\x9c\xac\xe6\xac\xa1\xe7\xbb\x93\xe7\xae\x97\xe6\x94\xb6\xe7\x9b\x8a float
        :return:
        """
        gamelog.debug('@zhangkuo onFTBBonus', total, point)
        self.showGameMsg(GMDD.data.FTB_GIVE_BONUS, ())
        self.ftbDataDetail.updateEarningData({'totalNowEarning': total,
         'nowEarning': point})

    def onYaojinTicketBonus(self, total):
        """
        \xe6\x8c\x96\xe7\x9f\xbf\xe4\xba\xa7\xe7\x94\x9f\xe7\x9a\x84\xe5\xa6\x96\xe7\xb2\xbe\xe8\xb4\xb5\xe5\xae\xbe\xe5\x88\xb8\xe6\x94\xb6\xe7\x9b\x8a
        :param total: \xe6\x9c\xac\xe6\xac\xa1\xe6\x8c\x96\xe7\x9f\xbf\xe6\x80\xbb\xe6\x94\xb6\xe7\x9b\x8a int
        :return:
        """
        gamelog.debug('@zhangkuo onYaojinTicketBonus', total)
        self.ftbDataDetail.updateEarningData({'yaojingTicket': total})

    def onPushDigPower(self, power):
        """
        \xe7\xbe\xb2\xe9\xb8\x9f\xe6\x8c\x87\xe5\xbc\x95 \xe9\x87\x87\xe6\x8e\x98\xe5\x8a\x9b\xe5\x8f\x98\xe5\x8c\x96
        :param power: \xe7\xbe\xb2\xe9\xb8\x9f\xe6\x8c\x87\xe5\xbc\x95\xe9\x87\x87\xe6\x8e\x98\xe5\x8a\x9b int
        :return:
        """
        gamelog.debug('@zhangkuo onPushDigPower', power)
        self.ftbDataDetail.updateDigPower(power)

    def onPushFTBVipRewardState(self, hasTaken):
        """
        \xe6\x88\x90\xe9\x95\xbf\xe5\x8a\xa9\xe5\x8a\x9b\xe6\x9c\x8d\xe5\x8a\xa1 \xe8\xb5\xa0\xe9\x80\x81\xe7\x9a\x84\xe6\x8c\x96\xe7\x9f\xbf\xe6\x97\xb6\xe9\x97\xb4\xe9\xa2\x86\xe5\x8f\x96\xe7\x8a\xb6\xe6\x80\x81
        :param hasTaken: \xe6\x98\xaf\xe5\x90\xa6\xe5\xb7\xb2\xe7\xbb\x8f\xe9\xa2\x86\xe5\x8f\x96 bool
        :return:
        """
        gamelog.debug('@zhangkuo onFTBVipRewardStateChange', hasTaken)
        self.ftbDataDetail.updateHasVipRewardTaken(hasTaken)

    def onPushDiggingTime(self, timeOfConsumed, availTime):
        """
        \xe5\x8f\xaf\xe6\x8c\x96\xe7\x9f\xbf\xe6\x97\xb6\xe9\x97\xb4\xe5\x8f\x91\xe7\x94\x9f\xe5\x8f\x98\xe5\x8c\x96
        :param timeOfConsumed: \xe6\x9c\xac\xe5\x91\xa8\xe7\xb4\xaf\xe8\xae\xa1\xe6\xb6\x88\xe8\xb4\xb9\xe8\x8e\xb7\xe5\xbe\x97\xe7\x9a\x84\xe6\x8c\x96\xe7\x9f\xbf\xe6\x97\xb6\xe9\x97\xb4(\xe7\xa7\x92\xef\xbc\x89 int
        :param availTime: \xe5\x89\xa9\xe4\xbd\x99\xe5\x8f\xaf\xe7\x94\xa8\xe7\x9a\x84\xe6\x8c\x96\xe7\x9f\xbf\xe6\x97\xb6\xe9\x97\xb4\xef\xbc\x88\xe7\xa7\x92\xef\xbc\x89 int
        :return:
        """
        gamelog.debug('@zhangkuo onPushDiggingTime', timeOfConsumed, availTime)
        self.ftbDataDetail.updateTimeData(timeOfConsumed, availTime)

    def onPushFTBTotalIncome(self, income):
        """
        \xe4\xbc\x8f\xe7\xbe\xb2\xe5\xb8\x81\xe7\xb4\xaf\xe8\xae\xa1\xe6\x94\xb6\xe7\x9b\x8a
        :param income: float
        :return:
        """
        gamelog.debug('@zhangkuo onPushFTBTotalIncome', income)

    def onPushFTBPoint(self, balance):
        """\xe4\xbc\x8f\xe7\xbe\xb2\xe5\xb8\x81\xe4\xbd\x99\xe9\xa2\x9d int """
        gamelog.debug('@zhangkuo onPushFTBPoint', balance)
        self.ftbDataDetail.updateEarningData({'totalEarning': balance})

    def onPushFTBTotalOutput(self, output, dailyOutput):
        """
        \xe4\xbc\x8f\xe7\xbe\xb2\xe9\x80\x9a\xe5\xae\x9d\xe4\xba\xa7\xe5\x87\xba
        :param output: \xe7\xb4\xaf\xe8\xae\xa1\xe4\xba\xa7\xe5\x87\xba float
        :param dailyOutput: \xe5\xbd\x93\xe5\x89\x8d\xe6\xaf\x8f\xe6\x97\xa5\xe4\xba\xa7\xe5\x87\xba float
        :return:
        """
        gamelog.debug('@zhangkuo onPushFTBTotalOutput', output, dailyOutput)
        self.ftbDataDetail.updateOutputData(output, dailyOutput)

    def onPushFTBAddr(self, addr):
        """
        \xe5\x8c\xba\xe5\x9d\x97\xe9\x93\xbe\xe5\x9c\xb0\xe5\x9d\x80 str
        """
        gamelog.debug('@zhangkuo onPushFTBAddr', addr)
        self.ftbDataDetail.updateLicenseData({'ftbAddr': addr})

    def onCompleteFTBQuest(self):
        """
        \xe5\xae\x8c\xe6\x88\x90\xe5\x89\x8d\xe7\xbd\xae\xe4\xbb\xbb\xe5\x8a\xa1
        """
        gamelog.debug('@zhangkuo onCompleteFTBQuest')
        gameglobal.rds.ui.topBar.onUpdateClientCfg()
        gameglobal.rds.ui.ftbLicense.show()

    def _confirmGotoBuyHome(self):
        seekId = FCD.data.get('homeNpcSeekID', 0)
        uiUtils.findPosById(seekId)

    def _confirmGotoFtbNpc(self):
        seekId = FCD.data.get('ftbNpcSeekID', 0)
        uiUtils.findPosById(seekId)

    def onTakeFTBVipRewardTime(self):
        """\xe9\xa2\x86\xe5\x8f\x96\xe6\x88\x90\xe9\x95\xbf\xe6\x9c\x8d\xe5\x8a\xa1\xe5\xa5\x96\xe5\x8a\xb1\xe7\x9a\x84\xe6\x8c\x96\xe7\x9f\xbf\xe6\x97\xb6\xe9\x97\xb4"""
        gamelog.debug('@zhangkuo onTakeFTBVipRewardTime')
        self.onPushFTBVipRewardState(True)

    def onPushPlayerCrossFTB(self, availTime, timeWeekly, hasTaken, hasCreatedWallet):
        gamelog.debug('@zhangkuo onPushPlayerCrossFTB', availTime, timeWeekly, hasTaken, hasCreatedWallet)
        self.onPushFTBVipRewardState(hasTaken)
        self.onPushDiggingTime(timeWeekly, availTime)
        self.isFtbWalletCreated = hasCreatedWallet

    def onPushFTBCondition(self, hasLicense, hasHome):
        """
        \xe6\x9f\xa5\xe8\xaf\xa2\xe5\x89\x8d\xe7\xbd\xae\xe6\x9d\xa1\xe4\xbb\xb6
        :param hasLicense: \xe6\x98\xaf\xe5\x90\xa6\xe6\x8b\xa5\xe6\x9c\x89\xe8\xae\xb8\xe5\x8f\xaf\xe8\xaf\x81 bool
        :param hasHome: \xe6\x98\xaf\xe5\x90\xa6\xe6\x8b\xa5\xe6\x9c\x89\xe5\xae\xb6\xe5\x9b\xad bool
        """
        gamelog.debug('@zhangkuo onPushFTBCondition', hasLicense, hasHome)

    def onPushDigPowerDetail(self, power, taskDetail):
        """
        \xe9\x87\x87\xe6\x8e\x98\xe5\x8a\x9b\xe7\x9b\xb8\xe5\x85\xb3
        :param power:\xe7\xbe\xb2\xe9\xb8\x9f\xe6\x8c\x87\xe5\xbc\x95\xe9\x87\x87\xe6\x8e\x98\xe5\x8a\x9b
        :param taskDetail: \xe4\xbb\xbb\xe5\x8a\xa1\xe8\xaf\xa6\xe6\x83\x85
        :return:
        """
        gamelog.debug('@zhangkuo onPushDigDetail', power, taskDetail)
        self.onPushDigPower(power)
        self.onPushFtbTaskDetail(taskDetail)

    def onPushDigSwitchState(self, isOpen):
        """\xe7\xac\xac\xe4\xb8\x89\xe6\x96\xb9\xe6\x9c\x8d\xe5\x8a\xa1\xe6\x8c\x96\xe7\x9f\xbf\xe5\xbc\x80\xe5\x85\xb3\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba\xe5\x85\xb3"""
        gamelog.debug('@zhangkuo onPushDigSwitchState', isOpen)
        self.ftbDataDetail.updateDigStateSwitch(isOpen)
        if isOpen:
            msgId = GMDD.data.FTB_OPEN_DIG
            self.showGameMsg(msgId, ())

    def onPushAutoDigState(self, isAuto):
        """\xe8\x87\xaa\xe5\x8a\xa8\xe6\x8c\x96\xe7\x9f\xbf\xe7\x8a\xb6\xe6\x80\x81"""
        gamelog.debug('@zhangkuo onPushAutoDigState', isAuto)
        self.ftbDataDetail.updateAutoDigState(isAuto)

    def onFtbCrossBack(self, isDigging, tLastDig, ticket, ftbPoint):
        """
        \xe8\xb7\xa8\xe6\x9c\x8d\xe5\x9b\x9e\xe6\x9d\xa5\xe7\x8a\xb6\xe6\x80\x81\xe5\x90\x8c\xe6\xad\xa5
        :param isDigging: \xe6\x98\xaf\xe5\x90\xa6\xe6\xad\xa3\xe5\x9c\xa8\xe6\x8c\x96\xe7\x9f\xbf
        :param tLastDig: \xe4\xb8\x8a\xe6\xac\xa1\xe5\xbc\x80\xe5\xa7\x8b\xe6\x8c\x96\xe7\x9f\xbf\xe6\x97\xb6\xe9\x97\xb4
        :return:
        """
        gamelog.debug('@zhangkuo onFtbCrossBack', isDigging, tLastDig, ticket, ftbPoint)
        self.ftbDataDetail.updateCrossbackState(isDigging, tLastDig)
        self.ftbDataDetail.updateEarningData({'totalNowEarning': ftbPoint,
         'yaojingTicket': ticket})

    def onPushFtbSysTotalOutput(self, totalOutput):
        gamelog.debug('@zhangkuo onPushFtbSysTotalOutput', totalOutput)
        dailyOutput = self.ftbDataDetail.dailyOutput or 0
        self.ftbDataDetail.updateOutputData(totalOutput, dailyOutput)

    def onPushIsAuthed(self, isAuthed):
        """\xe6\x98\xaf\xe5\x90\xa6\xe6\x8e\x88\xe6\x9d\x83\xe8\xbf\x87"""
        gamelog.debug('@zhangkuo onPushIsAuthed', isAuthed)
        self.ftbAuctionAuthed = isAuthed

    def isFtbAuctionAuthed(self):
        return getattr(self, 'ftbAuctionAuthed', False)

    def onGetFtbAuthCode(self, data):
        """
        \xe8\x8e\xb7\xe5\x8f\x96\xe6\x8e\x88\xe6\x9d\x83\xe7\xa0\x81\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param data: {"authorizationCode":"6f2dec37e642c307b3ff58098c2877ff","authExpireTime":1556787230000,
                        "accessId":"6a6b9cedc9234b4a662d7f9c5bf88691","accessToken":"e5ba75c0d53c04375374d0cb9ffb19f1",
                        "accessExpireTime":195552279000, 'sign':'xxxx'}
        :return:
        """
        gamelog.debug('@zhangkuo onGetFtbAuthCode', data)
        self.ftbAuctionData = data
        gameglobal.rds.ui.ftbExcavate.onGetFtbAuthCode()

    def isAuctionTokenExpired(self):
        if hasattr(self, 'ftbAuctionData') and self.ftbAuctionData:
            return utils.getNow() * 1000 < self.ftbAuctionData.get('accessExpireTime', 0)
        return True

    def onQueryFtbWallet(self, data, showPanel):
        """
        \xe6\x9f\xa5\xe8\xaf\xa2\xe9\x92\xb1\xe5\x8c\x85\xe8\xb4\xa6\xe5\x8f\xb7\xe4\xbf\xa1\xe6\x81\xaf
        :param data {'isWalletCreated':\xe8\xaf\xa5urs\xe6\x98\xaf\xe5\x90\xa6\xe5\x88\x9b\xe5\xbb\xba\xe8\xbf\x87\xe9\x92\xb1\xe5\x8c\x85, "bcAddress": \xe5\x8c\xba\xe5\x9d\x97\xe9\x93\xbe\xe5\x9c\xb0\xe5\x9d\x80, "privateKey": \xe7\xa7\x81\xe9\x92\xa5\xef\xbc\x8c'balance':\xe4\xbd\x99\xe9\xa2\x9d}
        """
        gamelog.debug('@zhangkuo onQueryFtbWallet', data)
        self.ftbWalletData = turnUnicodeDict2Gbk(data)
        if showPanel:
            ftbWalletHelper.getInstance().onGetWalletData()

    def onCreateFtbWallet(self, data):
        """
        \xe5\x88\x9b\xe5\xbb\xba\xe9\x92\xb1\xe5\x8c\x85\xe6\x88\x90\xe5\x8a\x9f
        """
        gamelog.debug('@zhangkuo onCreateFtbWallet', data)
        self.isFtbWalletCreated = True
        gameglobal.rds.ui.ftbWallet.show()
        gameglobal.rds.ui.ftbWalletSubWnd.onCreateFTBWallet()

    def onQueryFtbPrivateKey(self, data, ctxID):
        """
        \xe6\x9f\xa5\xe8\xaf\xa2\xe9\x92\xb1\xe5\x8c\x85\xe7\xa7\x81\xe9\x92\xa5
        :param data: {\xe2\x80\x98privateKey': \xe7\xa7\x81\xe9\x92\xa5, "mnemonicList": \xe7\xbb\x91\xe5\xae\x9a\xe7\xa0\x81}
        :param ctxID: \xe8\x87\xaa\xe5\xae\x9a\xe4\xb9\x89\xe4\xb8\x8a\xe4\xb8\x8b\xe6\x96\x87ID
        :return:
        """
        gamelog.debug('@zhangkuo onQueryFtbPrivateKey', data, ctxID)
        self.ftbPrivateKey = turnUnicodeDict2Gbk(data)
        ftbWalletHelper.getInstance().onGetPrivateKey(data, ctxID)

    def onVerifyFtbWalletPasswd(self, isOk, ctxID):
        """
        \xe9\xaa\x8c\xe8\xaf\x81\xe9\x92\xb1\xe5\x8c\x85\xe5\xaf\x86\xe7\xa0\x81
        :param isOk: \xe6\x98\xaf\xe5\x90\xa6\xe6\x88\x90\xe5\x8a\x9f
        :param ctxID: \xe8\x87\xaa\xe5\xae\x9a\xe4\xb9\x89\xe4\xb8\x8a\xe4\xb8\x8b\xe6\x96\x87ID
        :return:
        """
        gamelog.debug('@zhangkuo onVerifyFtbWalletPasswd', isOk, ctxID)
        if not isOk:
            BigWorld.player().showGameMsg(GMDD.data.COMMON_MSG, (gameStrings.TEXT_IMPFTB_301,))
        else:
            ftbWalletHelper.getInstance().onCheckCallback(isOk, ctxID)

    def onModifyFtbWalletPasswd(self, isOk):
        """\xe4\xbf\xae\xe6\x94\xb9\xe5\xaf\x86\xe7\xa0\x81"""
        gamelog.debug('@zhangkuo onModifyFtbWalletPasswd', isOk)
        gameglobal.rds.ui.ftbWalletSubWnd.onModifyPasswdCallback(isOk)

    def onQueryFtbTransaction(self, data):
        """
        \xe6\x9f\xa5\xe8\xaf\xa2\xe5\x8e\x86\xe5\x8f\xb2\xe4\xba\xa4\xe6\x98\x93
        """
        gamelog.debug('@zhangkuo onQueryFtbTransaction', data)
        gameglobal.rds.ui.ftbWallet.onGetDealList(turnUnicodeDict2Gbk(data))

    def onQueryFtbBindGame(self, data):
        """
        urs\xe7\xbb\x91\xe5\xae\x9a\xe4\xba\x86\xe5\x93\xaa\xe4\xba\x9b\xe6\xb8\xb8\xe6\x88\x8f
        tianyu: \xe5\xa4\xa9\xe8\xb0\x95\xef\xbc\x8cnsh\xef\xbc\x9a\xe9\x80\x86\xe6\xb0\xb4\xe5\xaf\x92\xef\xbc\x8cqn\xef\xbc\x9a\xe6\x96\xb0\xe5\x80\xa9\xe5\xa5\xb3\xe5\xb9\xbd\xe9\xad\x82OL\xef\xbc\x8cl12:\xe6\xb5\x81\xe6\x98\x9f\xe8\x9d\xb4\xe8\x9d\xb6\xe5\x89\x91
        :param data {'tianyu': True}
        """
        gamelog.debug('@zhangkuo onQueryFtbBindGame', data)
        gameglobal.rds.ui.ftbWallet.onGetBindInfo(data)

    def notifyCreateOrBindFtbAddr(self):
        """\xe9\x80\x9a\xe7\x9f\xa5\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe9\x80\x89\xe6\x8b\xa9\xe5\x88\x9b\xe5\xbb\xba\xe6\x96\xb0\xe5\x9c\xb0\xe5\x9d\x80\xe6\x88\x96\xe8\x80\x85\xe7\xbb\x91\xe5\xae\x9a\xe5\xb7\xb2\xe6\x9c\x89\xe5\x9c\xb0\xe5\x9d\x80"""
        gamelog.debug('@zhangkuo notifyCreateOrBindFtbAddr')
        gameglobal.rds.ui.ftbBind.show()

    def onBindFtbAddrByWords(self, data):
        """
        \xe6\x88\x90\xe5\x8a\x9f\xe7\xbb\x91\xe5\xae\x9a\xe5\xb7\xb2\xe6\x9c\x89\xe5\x8c\xba\xe5\x9d\x97\xe9\x93\xbe\xe5\x9c\xb0\xe5\x9d\x80
        :param data: {'addr': \xe5\x9c\xb0\xe5\x9d\x80}
        """
        gamelog.debug('@zhangkuo onBindFtbAddrByWords', data)
        self.ftbDataDetail._ftbAddr = data.get('addr', '')
        gameglobal.rds.ui.ftbBind.hide()
        self.showGameMsg(GMDD.data.FTB_ADDR_BIND_OK, ())
        gameglobal.rds.ui.dispatchEvent(events.EVNET_FTB_LICENSEDATA_CHANGE, {})

    def onGetFtbUserApiAuthFail(self):
        """
        \xe6\x9f\xa5\xe8\xaf\xa2\xe5\x8c\xba\xe5\x9d\x97\xe9\x93\xbe\xe6\x8e\x88\xe6\x9d\x83\xe5\xa4\xb1\xe8\xb4\xa5
        :return:
        """
        gameglobal.rds.ui.ftbWalletSubWnd.showActivityPasswordWnd()

    def onUpdateFtbEphemeralPower(self, power):
        """
        \xe6\x9b\xb4\xe6\x96\xb0\xe4\xb8\xb4\xe6\x97\xb6\xe7\xae\x97\xe5\x8a\x9b
        :return:
        """
        self.ftbDataDetail.updateEphemeralPower(power)

    def queryFtbWallectBeforeAuth(self, isWallect):
        gamelog.debug('xjw## queryFtbWallectBeforeAuth', isWallect)
        if not isWallect:
            ftbWalletHelper.getInstance().openWallet()
