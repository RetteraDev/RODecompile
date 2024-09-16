#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impStraightLvUp.o
import gameglobal
import gamelog

class ImpStraightLvUp(object):

    def beginStraightLvUp(self, straightLvUpType):
        self.isStraightLvUp = True
        self.lvBeforeStraight = self.lv

    def endStraightLvUp(self, straightLvUpType):
        gameglobal.rds.ui.playRecomm.initIncompleteNotifyHandler(True)
        self.isStraightLvUp = False
        if hasattr(self, 'lvBeforeStraight'):
            self.set_lv(self.lvBeforeStraight)

    def setStraightLvUpFlag(self, flag):
        self.newAvatarStraightLvUpFlag = flag

    def onStraightUpDone(self, cfgID):
        """
        \xe7\x9b\xb4\xe5\x8d\x87\xe5\xae\x8c\xe6\x88\x90
        :param cfgID:
        :return:
        """
        gamelog.debug('@zhangkuo onStraightUpDone', cfgID)
        self.showStrightUpPop = True

    def sendStraightUpTask(self, data):
        """
        \xe7\x9b\xb4\xe5\x8d\x87\xe4\xbb\xbb\xe5\x8a\xa1\xe4\xbf\xa1\xe6\x81\xaf
        :param data: {taskId:{'state':\xe7\x8a\xb6\xe6\x80\x81}}
        :return:
        """
        gamelog.debug('@zhangkuo sendStraightUpTask', data)
        self.straightUpTask = data
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
        gameglobal.rds.ui.straightUp.refreshInfo()

    def onStraightTaskChange(self, taskId, state):
        gamelog.debug('@zhangkuo onStraightTaskChange', taskId, state)
        self.straightUpTask.update({taskId: {'state': state}})
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
        gameglobal.rds.ui.straightUp.refreshInfo()
