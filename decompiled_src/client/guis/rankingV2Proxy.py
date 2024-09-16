#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/rankingV2Proxy.o
import BigWorld
import gameglobal
import uiConst
from uiProxy import UIProxy

class RankingV2Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RankingV2Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        pass

    def clearWidget(self):
        pass

    def show(self, *args):
        gameglobal.rds.ui.rankingV2 = gameglobal.rds.ui.ranking
        gameglobal.rds.ui.ranking.show()

    def initUI(self):
        pass

    def refreshInfo(self):
        pass
