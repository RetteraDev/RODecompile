#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impSignIn.o
import gameglobal
import gamelog

class ImpSignIn(object):

    def onResetSignIn(self, now):
        if not self.inWorld:
            return
        gameglobal.rds.ui.welfareEveryDayReward.refresh()

    def onResetSignInV2(self, signInfo):
        self.newSignInInfo = signInfo
        enableActivityAttend = gameglobal.rds.configData.get('enableActivityAttend', False)
        if enableActivityAttend:
            gameglobal.rds.ui.topBar.refreshActivityIcon()
            gameglobal.rds.ui.welfareSummer.refreAvtivityPanel()
            gameglobal.rds.ui.welfareSummer.notifyActivityAttendSignInMsg()
            if gameglobal.rds.ui.activityReSignIn.mediator and gameglobal.rds.ui.activityReSignIn.isClickConfirm:
                gameglobal.rds.ui.activityReSignIn.refresh()
        enableNewActivitySignin = gameglobal.rds.configData.get('enableNewActivitySignin', False)
        if enableNewActivitySignin:
            gameglobal.rds.ui.welfareSignIn.refreshInfo()
            if gameglobal.rds.ui.activityReSignIn.mediator and gameglobal.rds.ui.activityReSignIn.isClickConfirm:
                gameglobal.rds.ui.activityReSignIn.refresh()

    def applyNoviceSigninRewardSucc(self):
        gameglobal.rds.ui.welfareSevenDayLogin.applyRewardSucc()

    def applyNoviceOnlineRewardSucc(self):
        gameglobal.rds.ui.welfareOnlineReward.applyRewardSucc()
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()

    def applyNoviceCheckInRewardSucc(self):
        gameglobal.rds.ui.welfare.refreshInfo()
        gameglobal.rds.ui.welfareAccumulatedSignIn.refreshPanel()

    def onGetSignInBonus(self, randomRewardItems, exactRewardItems):
        """
        \xe7\xad\xbe\xe5\x88\xb0\xe8\x8e\xb7\xe5\xbe\x97\xe6\x8c\x87\xe5\xae\x9a\xe6\x97\xa5\xe5\xa5\x96\xe5\x8a\xb1\xe5\x92\x8c\xe9\x9a\x8f\xe6\x9c\xba\xe5\xa5\x96\xe5\x8a\xb1\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param randomRewardItems: \xe9\x9a\x8f\xe6\x9c\xba\xe5\xa5\x96\xe5\x8a\xb1 [(itemId\xef\xbc\x8cnum),...]
        :param exactRewardItems: \xe6\x8c\x87\xe5\xae\x9a\xe6\x97\xa5\xe5\xa5\x96\xe5\x8a\xb1 [(itemId, num),...]
        :return:
        """
        gameglobal.rds.ui.welfareSignIn.onGetSignInBonus(randomRewardItems, exactRewardItems)
        gamelog.debug('@zhangkuo onGetSignInBonus', str(randomRewardItems), str(exactRewardItems))
