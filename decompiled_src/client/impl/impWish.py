#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impWish.o
import gamelog
import cPickle
import zlib
import gameglobal
from guis import uiConst

class ImpWish(object):

    def makeWishSucc(self, wType, dbId, msg, singleWishCnt):
        gamelog.debug('@hjx wish#makeWishSucc:', wType, dbId, msg, singleWishCnt)
        self.myWishMsg = [0, msg, dbId]
        gameglobal.rds.ui.wishMadeView.updateMyWish(self.myWishMsg)
        gameglobal.rds.ui.wishMade.updateSpecialWish(singleWishCnt)

    def onQuerySingleWishCnt(self, singleWishCnt):
        gameglobal.rds.ui.wishMade.updateSpecialWish(singleWishCnt)

    def onQueryLatestWish(self, info, version):
        info = cPickle.loads(zlib.decompress(info))
        gamelog.debug('@hjx wish#onQueryLatestWish:', info, version)
        gameglobal.rds.ui.wishMadeView.updateWishData(uiConst.WISH_NOW, info, version)

    def onQueryHotestWish(self, info, version):
        info = cPickle.loads(zlib.decompress(info))
        gamelog.debug('@hjx wish#onQueryHotestWish:', info, version)
        gameglobal.rds.ui.wishMadeView.updateWishData(uiConst.WISH_HOT, info, version)

    def onQueryWishAwardRecord(self, info, version):
        info = cPickle.loads(zlib.decompress(info))
        gamelog.debug('@hjx wish#onQueryWishAwardRecord:', info, version)
        gameglobal.rds.ui.wishMadeView.updateAwardRecord(info, version)

    def onQueryFriendWish(self, info):
        gamelog.debug('@hjx wish#onQueryFriendWish:', info)
        gameglobal.rds.ui.wishMadeView.showFriendWish(info)

    def onUpvoteWishSucc(self, dbId, cnt):
        gamelog.debug('@hjx wish#onUpvoteWishSucc:', dbId, cnt)
        gameglobal.rds.ui.wishMadeView.updateVote(dbId, cnt)

    def resetWishInfoDaily(self):
        gamelog.debug('@hjx wish#resetWishInfoDaily')
        self.myWishMsg = []

    def onQueryMyWishMsg(self, info, version):
        gamelog.debug('@hjx wish#onQueryMyWishMsg:', info, version)
        self.myWishMsg = [info['cnt'], info['msg'], info['dbId']]
        gameglobal.rds.ui.wishMadeView.updateMyWish(self.myWishMsg, version)
