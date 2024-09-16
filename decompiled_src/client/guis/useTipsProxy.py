#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/useTipsProxy.o
from Scaleform import GfxValue
import gamelog
import gameglobal
from uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils
import hotkey as HK
SKILL_ICON_RES = 'skill/icon/'
SWF_RES = 'tutorialSwf/'

class UseTipsProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(UseTipsProxy, self).__init__(uiAdapter)
        self.modelMap = {'getData': self.onGetData}
        self.data = None

    def onGetData(self, *arg):
        if self.data is None:
            nullObj = GfxValue(1)
            nullObj.SetNull()
            return nullObj
        else:
            return uiUtils.array2GfxAarry(self._formatstr(self.data), True)

    def show(self, data):
        if data is None:
            return
        else:
            self.data = data
            self.uiAdapter.loadWidget(uiConst.WIDGET_USETIPS)
            return

    def clearWidget(self):
        self.data = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_USETIPS)

    def testFormat(self):
        test = 'AAAAAA$(2,766)$(1,10107,40)$BBBBBBBB'
        print 'testFormat', self._formatstr(test)

    def _formatstr(self, m):
        if m is None:
            return
        else:
            data = m.split('$')
            ret = []
            try:
                for item in data:
                    if item.find(',') != -1:
                        t = eval(item)
                        path = self._getPathByType(t)
                        if t[0] != uiConst.USE_TIPS_TYPE_SWF:
                            ret.append([t[0], path])
                        else:
                            ret.append([t[0],
                             path,
                             t[2],
                             t[3]])
                    else:
                        ret.append(item)

            except Exception as e:
                gamelog.info('error@useTipsProxy._formatstr ', e.message)

            return ret

    def _getPathByType(self, t):
        picType = t[0]
        if picType == uiConst.USE_TIPS_TYPE_ITEM:
            return uiConst.ITEM_ICON_IMAGE_RES_40 + str(t[1]) + '.dds'
        if picType == uiConst.USE_TIPS_TYPE_KEY:
            return self._getKeyName(t[1])
        if picType == uiConst.USE_TIPS_TYPE_SKILL:
            return SKILL_ICON_RES + str(t[1]) + '.dds'
        if picType == uiConst.USE_TIPS_TYPE_SWF:
            return SWF_RES + str(t[1]) + gameglobal.rds.ui.getUIExt()

    def _getKeyName(self, key):
        detial = HK.HKM[key]
        keyName = detial.getBrief()
        if not keyName:
            keyName = detial.getBrief(2)
        keyType = 'common'
        if keyName[:2] == 'S+':
            keyType = 'Shift'
            if keyName == 'S+S':
                keyName = ''
            else:
                keyName = keyName[2:]
        elif keyName[:2] == 'C+':
            keyType = 'Ctrl'
            if keyName == 'C+C':
                keyName = ''
            else:
                keyName = keyName[2:]
        elif keyName[:2] == 'A+':
            keyType = 'Alt'
            if keyName == 'A+A':
                keyName = ''
            else:
                keyName = keyName[2:]
        return (keyType, keyName)
