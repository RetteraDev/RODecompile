#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impItemCommit.o
import gamelog
import gameglobal

class ImpItemCommit(object):

    def onItemCommit(self, res):
        gamelog.info('@szh onItemCommit', res)
        gameglobal.rds.ui.worldWar.onItemCommitResult(res)
