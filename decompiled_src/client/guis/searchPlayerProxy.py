#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/searchPlayerProxy.o
import BigWorld
import gametypes
import const
from uiProxy import UIProxy
from guis import uiConst
from ui import unicode2gbk
from guis import uiUtils

class SearchPlayerProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SearchPlayerProxy, self).__init__(uiAdapter)
        self.modelMap = {'searchPlayer': self.onSearchPlayer,
         'confirmOp': self.onConfirmOp}
        uiAdapter.registerEscFunc(uiConst.WIDGET_SEARCH_PLAYER, self.hide)
        self.reset()

    def show(self, *args):
        if args:
            self.initData = args[0]
        self.uiAdapter.loadWidget(uiConst.WIDGET_SEARCH_PLAYER)

    def reset(self):
        self.initData = None
        self.med = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SEARCH_PLAYER:
            self.med = mediator
            if self.initData:
                val = {'title': self.initData.get('title', ''),
                 'confirmLabel': self.initData.get('confirmLabel', '')}
                return uiUtils.dict2GfxDict(val, True)

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SEARCH_PLAYER)

    def onSearchPlayer(self, *args):
        txt = unicode2gbk(args[3][0].GetString())
        BigWorld.player().base.searchFriendByName(gametypes.SEARCH_PLAYER_FOR_ARMY_APPOINT, txt)

    def onConfirmOp(self, *args):
        gbId = int(args[3][0].GetString())
        roleName = unicode2gbk(args[3][1].GetString())
        if self.initData:
            callback = self.initData.get('callBack')
            if callback:
                callback(gbId, roleName)

    def setPlayerList(self, infoList):
        if self.med != None:
            info = []
            for gbId, name, level, spaceNo, areaId, school, isOnline, photo, sex, combatScore in infoList:
                spaceName = self.uiAdapter.friend._getLastPlace(spaceNo, areaId)
                info.append({'gbId': gbId,
                 'roleName': name,
                 'lv': level,
                 'location': spaceName,
                 'school': const.SCHOOL_DICT.get(school),
                 'state': '‘⁄œﬂ' if isOnline else '¿Îœﬂ'})

            self.med.Invoke('setResult', uiUtils.array2GfxAarry(info, True))
