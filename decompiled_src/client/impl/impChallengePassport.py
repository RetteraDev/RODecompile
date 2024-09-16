#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impChallengePassport.o


class ImpChallengePassport(object):

    def challengePassportOnSyncInfo(self, info):
        """
        :param info:
        info = {
            'lv': self.lv,
            'exp': self.exp,
            'isCharge': self.isCharge,
            'bonusPool': self.bonusPool,
            'dayTarget': self.dayTarget,
            'weekTarget': self.weekTarget,
            'seasonTarget': self.seasonTarget,
            'version': self.version,
        }
        :return:
        """
        self.challengePassportData.updateInfo(info)

    def challengePassportNotify(self):
        self.challengePassportData.challengePassportNotify()
