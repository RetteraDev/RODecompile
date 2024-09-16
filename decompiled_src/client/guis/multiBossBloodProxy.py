#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/multiBossBloodProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
from ui import gbk2unicode
from uiProxy import UIProxy

class MultiBossBloodProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MultiBossBloodProxy, self).__init__(uiAdapter)
        self.modelMap = {'initData': self.onInitData}
        self.mediator = None
        self.bossList = None
        self.bossCharType = []

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_MULTI_BOSSBLOOD:
            self.mediator = mediator

    def show(self, bossList):
        if not self.mediator:
            self.bossList = bossList
            for bossData in bossList:
                self.bossCharType.append(bossData[0])

            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_MULTI_BOSSBLOOD)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_MULTI_BOSSBLOOD)

    def reset(self):
        super(self.__class__, self).reset()
        self.bossList = None
        self.bossCharType = []

    def onInitData(self, *arg):
        movie = gameglobal.rds.ui.movie
        bossArray = movie.CreateArray()
        monsterEnt = tuple((ent for ent in BigWorld.entities.values() if ent.IsMonster and hasattr(ent, 'charType')))
        for i, bossData in enumerate(self.bossList):
            bossBlood = -1
            bossObj = movie.CreateObject()
            for monster in monsterEnt:
                if getattr(monster, 'charType', 0) == bossData[0]:
                    bossBlood = monster.hp * 100.0 / monster.mhp
                    break

            bossObj.SetMember('bossName', GfxValue(gbk2unicode(bossData[1])))
            bossObj.SetMember('bossBlood', GfxValue(bossBlood))
            bossArray.SetElement(i, bossObj)

        return bossArray

    def updateBlood(self, charType, hp, mhp):
        if self.mediator:
            self.mediator.Invoke('updateBlood', (GfxValue(self.bossCharType.index(charType)), GfxValue(hp * 100.0 / mhp)))
