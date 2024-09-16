#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/chahuaProxy.o
import BigWorld
from Scaleform import GfxValue
import gamelog
from ui import gbk2unicode
from uiProxy import UIProxy
from guis import uiConst
from data import chahua_data as CHD
from data import npc_data as ND

class ChahuaProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ChahuaProxy, self).__init__(uiAdapter)
        self.modelMap = {'getChaHua': self.onGetChaHua,
         'closeChaHua': self.onCloseChaHua}

    def onCloseChaHua(self, *arg):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CHAHUA)

    def onGetChaHua(self, *arg):
        gamelog.debug('chahua onGetChaHua', self.chahua)
        data = CHD.data.get(self.chahua)
        if data == None:
            raise Exception('chahua is not found: %d' % self.chahua)
            return
        ar = self.movie.CreateArray()
        j = 0
        npcGroup = []
        for npc in data['npcId']:
            if npc == 0:
                name = BigWorld.player().realRoleName
            else:
                name = ND.data[npc]['name']
            npcGroup.append(name)

        values = [data['chId'], npcGroup, data['chat']]
        for item in values:
            arr = self.movie.CreateArray()
            i = 0
            for subItem in item:
                if type(subItem) == type(''):
                    arr.SetElement(i, GfxValue(gbk2unicode(subItem)))
                else:
                    arr.SetElement(i, GfxValue(subItem))
                i = i + 1

            ar.SetElement(j, arr)
            j = j + 1

        return ar

    def show(self, chaHuaId):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CHAHUA)
        self.chahua = chaHuaId
        gamelog.debug('chahua', self.chahua)
        self.uiAdapter.loadWidget(uiConst.WIDGET_CHAHUA)
