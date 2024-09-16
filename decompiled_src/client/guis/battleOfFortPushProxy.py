#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/battleOfFortPushProxy.o
import BigWorld
import gameglobal
from guis import generalPushProxy

class BattleOfFortPushProxy(generalPushProxy.GeneralPushItemProxy):

    def __init__(self, uiAdapter):
        super(BattleOfFortPushProxy, self).__init__(uiAdapter)
        self.battleId = 0

    def onClickItem(self, *args):
        gameglobal.rds.ui.battleOfFortSignUp.show(self.battleId)

    def isPushItemEnabled(self, state):
        enabled = gameglobal.rds.configData.get('enableNewFlagBF', False)
        return enabled
