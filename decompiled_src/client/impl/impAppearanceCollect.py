#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impAppearanceCollect.o
import zlib
import cPickle
import gameglobal

class ImpAppearanceCollect(object):

    def sendFriendRankResult(self, rankResult):
        result = cPickle.loads(zlib.decompress(rankResult))
        gameglobal.rds.ui.guibaoge.refreshRankView(result)
