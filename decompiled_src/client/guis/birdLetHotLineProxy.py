#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/birdLetHotLineProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import const
from ui import unicode2gbk
from guis import uiConst
from guis import uiUtils
from uiProxy import UIProxy
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD

class BirdLetHotLineProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BirdLetHotLineProxy, self).__init__(uiAdapter)
        self.modelMap = {'getDropData': self.onGetDropData,
         'confirmContent': self.onConfirmContent}
        self.mediator = None
        self.npcId = 0
        self.nameArray = SCD.data.get('BirdLetHotLineType', [gameStrings.TEXT_BIRDLETHOTLINEPROXY_26, gameStrings.TEXT_BIRDLETHOTLINEPROXY_26_1, gameStrings.TEXT_BIRDLETHOTLINEPROXY_26_2])
        uiAdapter.registerEscFunc(uiConst.WIDGET_BIRDLET_HOTLINE, self.clearWidget)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_BIRDLET_HOTLINE:
            self.mediator = mediator

    def clearWidget(self):
        self.mediator = None
        self.npcId = 0
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BIRDLET_HOTLINE)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def show(self, npcId):
        self.npcId = npcId
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BIRDLET_HOTLINE)

    def onGetDropData(self, *args):
        return uiUtils.array2GfxAarry(self.nameArray, True)

    def onConfirmContent(self, *args):
        index = int(args[3][0].GetNumber())
        content = args[3][1].GetString()
        npcEnt = BigWorld.entities.get(self.npcId)
        if npcEnt:
            if len(content):
                realContent = unicode2gbk(content)
                if len(realContent):
                    npcEnt.cell.feedBackToBirdlet(index, realContent)
                else:
                    BigWorld.player().showGameMsg(GMDD.data.FEEDBACK_BIRDLET_WRONG_CODE, ())
            else:
                BigWorld.player().showGameMsg(GMDD.data.FEEDBACK_BIRDLET_CONTENT_LENGTH_LIMIT, (const.FEEDBACK_BIRDLET_CONTENT_LIMIT_MIN, const.FEEDBACK_BIRDLET_CONTENT_LIMIT_MAX))
