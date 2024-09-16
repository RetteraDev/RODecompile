#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/ftbWalletHelper.o
import BigWorld
import gameglobal
from gameclass import Singleton
from guis import ui

def getInstance():
    return FtbWalletHelper.getInstance()


class FtbWalletHelper(object):
    __metaclass__ = Singleton

    def __init__(self):
        super(FtbWalletHelper, self).__init__()
        self.checkPasswordCallback = {}
        self.getPrivateKeyCallback = {}

    def isWalletCreated(self):
        p = BigWorld.player()
        return getattr(p, 'isFtbWalletCreated', False)

    @ui.checkInventoryLock()
    def openWallet(self):
        p = BigWorld.player()
        p.base.queryFtbWallet(p.cipherOfPerson)

    def onGetWalletData(self):
        if self.isWalletCreated():
            gameglobal.rds.ui.ftbWallet.show()
        elif self.isBindGame():
            gameglobal.rds.ui.ftbWalletSubWnd.showOpenWnd()
        else:
            gameglobal.rds.ui.ftbWalletSubWnd.showCreateWnd()

    def isBindGame(self):
        p = BigWorld.player()
        if hasattr(p, 'ftbWalletData'):
            return p.ftbWalletData.get('isWalletCreated', False)
        return False

    def onCheckCallback(self, result, tag):
        callback = self.checkPasswordCallback.get(tag, None)
        if callback:
            callback(result)

    def checkPassword(self, passwd, callback, tag):
        self.checkPasswordCallback[tag] = callback
        p = BigWorld.player()
        p.base.verifyFtbWalletPasswd(passwd, tag)

    def onGetPrivateKey(self, data, tag):
        callback = self.getPrivateKeyCallback.get(tag, None)
        if callback:
            callback(data)

    def queryPrivateKey(self, passwd, callback, tag):
        self.getPrivateKeyCallback[tag] = callback
        p = BigWorld.player()
        p.base.queryFtbPrivateKey(passwd, tag)

    def modifyPass(self, passwd, callback):
        pass
