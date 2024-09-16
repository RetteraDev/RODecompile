#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPhotoBorder.o
import BigWorld
import gameglobal
from photoBorder import PhotoBorder, PhotoBorderVal

class ImpPhotoBorder(object):

    def syncPhotoBorder(self, pbData):
        p = BigWorld.player()
        p.photoBorder = PhotoBorder().fromDTO(pbData)
        gameglobal.rds.ui.player.updateBorderIcon()

    def onSwitchPhotoBorder(self, bId):
        p = BigWorld.player()
        if not hasattr(p, 'photoBorder'):
            p.photoBorder = PhotoBorder()
        p.photoBorder.borderId = bId
        gameglobal.rds.ui.player.updateBorderIcon()

    def onUnlockPhotoBorder(self, pbData):
        val = PhotoBorderVal().fromDTO(pbData)
        p = BigWorld.player()
        if not hasattr(p, 'photoBorder'):
            p.photoBorder = PhotoBorder()
        p.photoBorder.push(val)

    def friendPhotoBorderUpdated(self, gbId, borderId):
        res = self.friend.updatePhotoBorderId(gbId, borderId)
        if res:
            self._refreshFriendList()
        return res

    def set_photoBorderId(self, old):
        if self.id == BigWorld.player().id:
            gameglobal.rds.ui.player.updateBorderIcon()
