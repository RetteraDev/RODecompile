#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impWingWorldForge.o
import gameglobal
import gamelog
import copy
from guis import uiConst
from gameStrings import gameStrings
import wingWorldForgeInfo

class ImpWingWorldForge(object):

    def onForgeStartToGuildMembers(self, wingWorldForgeData):
        gamelog.debug('ypc@ onForgeStartToGuildMembers, ', wingWorldForgeInfo.instance.getDictFromObj(wingWorldForgeData))
        self.wingWorldForgeData = copy.deepcopy(wingWorldForgeData)
        self.wingWorldForgeData.genItems = wingWorldForgeData.clientItems
        if not gameglobal.rds.ui.wingWorldRonglu.widget:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.WING_WORLD_RONGLU_GOTO, self.handleShowRongluCallBack, title=gameStrings.WING_WORLD_RONGLU_GOTO_TITLE)
        else:
            gameglobal.rds.ui.wingWorldRonglu.refreshState()
        if gameglobal.rds.ui.wingWorldResource.countryPanel:
            gameglobal.rds.ui.wingWorldResource.countryPanel.refreshRongluInfo()

    def handleShowRongluCallBack(self, *args):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_WING_WORLD_RONGLU)

    def onForgeEndToGuildMembers(self, state):
        gamelog.debug('ypc@ onForgeEndToGuildMembers!!!')
        if hasattr(self, 'wingWorldForgeData'):
            self.wingWorldForgeData.state = state
        gameglobal.rds.ui.wingWorldRonglu.onForgeEnd()

    def onForgeBonusToGuildMembers(self, round, count, startTime):
        if hasattr(self, 'wingWorldForgeData'):
            gamelog.debug('ypc@ onForgeBonusToGuildMembers round=%s, count=%s, startTime=%s' % (round, count, startTime))
            self.wingWorldForgeData.round = round
            self.wingWorldForgeData.count = count
            gameglobal.rds.ui.wingWorldRonglu.onUpdateRound()

    def onForgeBonusEndToGuildMembers(self, round):
        pass

    def onGetWingWorldForgeData(self, wingWorldForgeData):
        gamelog.debug('ypc@ onGetWingWorldForgeData, ', wingWorldForgeInfo.instance.getDictFromObj(wingWorldForgeData))
        self.wingWorldForgeData = copy.deepcopy(wingWorldForgeData)
        self.wingWorldForgeData.genItems = wingWorldForgeData.clientItems
        if gameglobal.rds.ui.wingWorldRonglu.widget:
            gameglobal.rds.ui.wingWorldRonglu.refreshState()
        if gameglobal.rds.ui.wingWorldResource.countryPanel:
            gameglobal.rds.ui.wingWorldResource.countryPanel.refreshRongluInfo()
