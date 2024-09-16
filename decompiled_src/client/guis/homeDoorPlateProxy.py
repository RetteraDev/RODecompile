#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/homeDoorPlateProxy.o
from gamestrings import gameStrings
import BigWorld
import Math
import gameglobal
import clientcom
from guis.uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils

class HomeDoorPlateProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(HomeDoorPlateProxy, self).__init__(uiAdapter)
        self.modelMap = {'getDoorPlateInfo': self.onGetDoorPlateInfo}
        self.reset()

    def show(self, entId):
        ent = BigWorld.entity(entId)
        if not ent or not ent.inWorld:
            return
        if not getattr(ent, 'roleName', 0):
            return
        multiId = gameglobal.rds.ui.loadWidget(uiConst.WIDGET_HOME_DOOR_PLATE)
        self.loading[multiId] = entId

    def dismiss(self, entId):
        if entId in self.loaded:
            multiId, mc = self.loaded.pop(entId)
            gameglobal.rds.ui.unLoadWidget(multiId)
        else:
            for multiId, _entId in self.loading.iteritems():
                if entId == _entId:
                    self.loading.pop(multiId)
                    break

    def clearWidget(self):
        for entId in self.loaded.keys():
            self.dismiss(entId)

    def reset(self):
        self.loading = {}
        self.loaded = {}
        self.callbackHandle = None

    def onGetDoorPlateInfo(self, *arg):
        multiId = int(arg[3][0].GetNumber())
        mc = arg[3][1]
        if multiId in self.loading:
            entId = self.loading.pop(multiId)
            self.loaded[entId] = (multiId, mc)
            info = self.getDoorPlateInfo(entId)
            if info:
                self.startRefresh()
                return uiUtils.dict2GfxDict(info, True)
        gameglobal.rds.ui.unLoadWidget(multiId)

    def getDoorPlateInfo(self, entId):
        ent = BigWorld.entity(entId)
        if ent:
            pos = Math.Vector3(ent.position)
            pos.y += 4
            x, y = clientcom.worldPointToScreen(pos)
            player = BigWorld.player()
            dist = (ent.position - player.position).length
            scale = self.linerFunc(dist, 1.0, 1.0, 35, 0.5)
            alpha = self.linerFunc(dist, 8.0, 1.0, 50, 0.1)
            wealth = getattr(ent, 'wealth', 0)
            wealthLv = gameglobal.rds.ui.homeCheckHouses.getWealthLv(wealth)
            _name = ''
            if ent.intimacyName:
                _name = gameStrings.TEXT_HOMEDOORPLATEPROXY_80 % (ent.roleName, ent.intimacyName)
            else:
                _name = ent.roleName
            return {'name': _name,
             'x': x,
             'y': y,
             'scale': scale,
             'alpha': alpha,
             'wealthLv': wealthLv}
        else:
            return None

    def linerFunc(self, x, x0, y0, x1, y1):
        if x <= x0:
            return y0
        if x >= x1:
            return y1
        return (y1 - y0) / (x1 - x0) * (x - x0) + y0

    def startRefresh(self):
        if self.callbackHandle:
            BigWorld.cancelCallback(self.callbackHandle)
        if not self.loaded:
            return
        for entId, (multiId, mc) in self.loaded.items():
            info = self.getDoorPlateInfo(entId)
            if info:
                mc.Invoke('refresh', uiUtils.dict2GfxDict(info, True))
            else:
                self.dismiss(entId)

        self.callbackHandle = BigWorld.callback(0.02, self.startRefresh)
