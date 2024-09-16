#Embedded file name: I:/bag/tmp/tw2/res/entities\client\debug/particleDebugProxy.o
import BigWorld
import ResMgr
from Scaleform import GfxValue
import gamelog
import gameglobal
from sfx import sfx
from guis.ui import gbk2unicode
from guis.uiProxy import DataProxy
from guis import uiConst

class ParticleDebugProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(ParticleDebugProxy, self).__init__(uiAdapter)
        self.bindType = 'particleDebug'
        self.modelMap = {'ClickParticle': self.onClickParticle,
         'getSearchPaResult': self.onGetSearchAcResult}
        self.effectName = []

    def scanEffectFile(self):
        curPath = ['effect/com',
         'effect/char/com',
         'effect/char/buff',
         'effect/weapon',
         'effect/char/combat']
        for p in curPath:
            folderSection = ResMgr.openSection(p)
            if folderSection:
                for i in folderSection.keys():
                    i = i.lower()
                    if i.endswith('.xml') and i[:-4].isdigit():
                        self.effectName.append(i + ':' + p)

    def getEffectArray(self):
        i = 0
        ar = self.movie.CreateArray()
        if not self.effectName:
            self.scanEffectFile()
        for item in self.effectName:
            value = GfxValue(gbk2unicode(self.effectName[i]))
            ar.SetElement(i, value)
            i = i + 1

        return ar

    def getValue(self, key):
        if key == 'particleDebug.particleList':
            ar = self.getEffectArray()
            return ar

    def onClickParticle(self, *arg):
        effectName = arg[3][0].GetString().split(':')[0]
        effectId = int(effectName.split('.')[0])
        gamelog.debug('actiondebug onGetSearchAcResult', effectId)
        sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (BigWorld.player().getBasicEffectLv(),
         BigWorld.player().getBasicEffectPriority(),
         BigWorld.player().model,
         effectId,
         sfx.EFFECT_UNLIMIT,
         5))

    def onGetSearchAcResult(self, *arg):
        gamelog.debug('actiondebug onGetSearchAcResult')
        i = 0
        ar = self.movie.CreateArray()
        if not self.effectName:
            self.scanEffectFile()
        subString = arg[3][0].GetString()
        if not subString:
            return self.getEffectArray()
        for item in self.effectName:
            if item.find(subString) != -1:
                value = GfxValue(gbk2unicode(item))
                ar.SetElement(i, value)
                i = i + 1

        return ar

    def showParticleDebug(self):
        self.uiAdapter.movie.invoke(('_root.loadWidget', GfxValue(uiConst.WIDGET_DEBUG_PARTICLE)))
