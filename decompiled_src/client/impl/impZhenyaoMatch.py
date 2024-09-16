#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impZhenyaoMatch.o
import zlib
import cPickle
import gameglobal

class ImpZhenyaoMatch(object):

    def onGetZhenyaoMatchRank(self, rankResult, score, usedTime):
        self.zhenyaoProgressData = rankResult
        gameglobal.rds.ui.zhenyao.updateProgressPanel(rankResult, score)

    def onGetZhenyaoMatchFinalRank(self, groupRank, result):
        result = cPickle.loads(zlib.decompress(result))
        gameglobal.rds.ui.zhenyao.updateRankData(result, groupRank)

    def onGetZhenyaoGroupInfo(self, groupNUID, groupInfo):
        gameglobal.rds.ui.ranking.updateTeamDetail(groupInfo)

    def pushFubenScoreDetail(self, detail):
        gameglobal.rds.ui.zhenyao.setResultDetail(detail)
        gameglobal.rds.ui.zhenyao.showFbResult()

    def onGetZhenyaoMatchFinalGbIdRank(self, rank):
        gameglobal.rds.ui.zhenyao.updateSelfRank(rank)
        gameglobal.rds.ui.zhenyao.setResultRank(rank)
        gameglobal.rds.ui.zhenyao.showFbResult()
