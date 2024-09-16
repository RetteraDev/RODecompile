#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cefUIManager.o
import BigWorld
CEFModule = None
try:
    import CEFManager as CEFModule
except:
    CEFModule = None

from gameclass import Singleton
from cdata import game_msg_def_data as GMDD

def getInstance():
    return CefUIManager.getInstance()


class CefUIManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.curCefUI = 0
        self.closeFunc = None

    def registerCefUI(self, wid, closeFunc = None, forceOpen = False):
        if self.curCefUI:
            if not forceOpen:
                self.showCommonMsg()
                return False
            if self.closeFunc:
                self.closeFunc()
            else:
                self.showCommonMsg()
                return False
        self.curCefUI = wid
        self.closeFunc = closeFunc
        return True

    def unregisterCefUI(self, wid):
        if self.curCefUI == wid:
            self.curCefUI = None
            self.closeFunc = None

    def showCommonMsg(self):
        BigWorld.player().showGameMsg(GMDD.data.WEBUI_FORCE_CLOSE_MSG, ())
