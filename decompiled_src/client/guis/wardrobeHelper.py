#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wardrobeHelper.o
import BigWorld
import gameglobal
import uiConst
from helpers import aspectHelper
from helpers import blackEffectManager
from cdata import game_msg_def_data as GMDD

class WardrobeHelper(object):

    def __init__(self):
        super(WardrobeHelper, self).__init__()
        self.oldScroll = None

    def open(self, showCate = None):
        p = BigWorld.player()
        if not gameglobal.rds.configData.get('enableWardrobe', False):
            p.showGameMsg(GMDD.data.EXCITEMENT_FORBIDDEN_FUNC, ())
            return
        gameglobal.rds.ui.wardrobe.show(showCate)
        gameglobal.rds.ui.myCloth.show()

    def addWardrobeBg(self):
        self.setBlackScreenEff(blackEffectManager.SRC_WARDROBE, True)
        self.oldScroll = aspectHelper.getInstance().configCamera(3)

    def removeWardrobeBg(self):
        self.setBlackScreenEff(blackEffectManager.SRC_WARDROBE, False)

    def setBlackScreenEff(self, srcId, enable):
        blackEffMgr = blackEffectManager.getInstance()
        blackEffMgr.setBlackScreenEff(srcId, enable)

    def close(self):
        gameglobal.rds.ui.wardrobe.hide()
        gameglobal.rds.ui.myCloth.hide()
        gameglobal.rds.ui.dyeList.hide()
        self.resetCamera()

    def resetCamera(self):
        if hasattr(self, 'oldScroll') and self.oldScroll != None:
            aspectHelper.getInstance().configCamera(self.oldScroll)
            self.oldScroll = None


_ins = None

def getInstance():
    global _ins
    if not _ins:
        _ins = WardrobeHelper()
    return _ins
