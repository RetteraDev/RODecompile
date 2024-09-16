#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/queryLocationProxy.o
from gamestrings import gameStrings
import BigWorld
import const
import formula
import gameglobal
from guis import uiConst
from uiProxy import UIProxy
from ui import unicode2gbk
from guis import uiUtils
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD

class QueryLocationProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(QueryLocationProxy, self).__init__(uiAdapter)
        self.modelMap = {'queryLocation': self.onQueryLocation}
        uiAdapter.registerEscFunc(uiConst.WIDGET_QUERY_LOCATION, self.hide)
        self.reset()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_QUERY_LOCATION:
            self.mediator = mediator

    def show(self, *args):
        if args:
            self.npc = args[0]
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_QUERY_LOCATION)

    def clearWidget(self):
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_QUERY_LOCATION)

    def reset(self):
        self.mediator = None
        self.npc = None

    def onQueryLocation(self, *args):
        name = unicode2gbk(args[3][0].GetString()).strip()
        if self.npc:
            self.npc.cell.queryPlayerLocation(name)
        else:
            BigWorld.player().cell.queryPlayerLocation(name)

    def setQueryResutl(self, spaceNo, mapAreaId, chunkName, position, error):
        if self.mediator:
            result = {}
            if error == const.QUERY_PLAYER_SUCC:
                result['succ'] = True
                result['area'] = gameStrings.TEXT_QUERYLOCATIONPROXY_62 % formula.whatLocationName(spaceNo, chunkName, includeMLInfo=True)
                location = '(%s, %s, %s)' % (round(position[0]), round(position[2]), round(position[1]))
                eventTxt = 'findPos:%s, %s,%s,%s' % (spaceNo,
                 position[0],
                 position[1],
                 position[2])
                result['location'] = gameStrings.TEXT_QUERYLOCATIONPROXY_65 + uiUtils.toHtml(location, linkEventTxt=eventTxt)
            else:
                result['succ'] = False
                if error == const.QUERY_PLAYER_NOT_EXIST:
                    errorMsg = GMD.data.get(GMDD.data.QUERY_PLAYER_NOT_EXIST, {}).get('text', '')
                elif error == const.QUERY_PLAYER_NOT_ONLINE:
                    errorMsg = GMD.data.get(GMDD.data.QUERY_PLAYER_NOT_ONLINE, {}).get('text', '')
                elif error == const.QUERY_PLAYER_NOT_ALLOW:
                    errorMsg = GMD.data.get(GMDD.data.QUERY_PLAYER_NOT_ALLOW, {}).get('text', '')
                result['errorMsg'] = errorMsg
            self.mediator.Invoke('setQueryResult', uiUtils.dict2GfxDict(result, True))
