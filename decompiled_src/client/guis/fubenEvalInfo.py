#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fubenEvalInfo.o
import BigWorld
from Scaleform import GfxValue
import const
import formula
import gamelog
import gameglobal
from ui import gbk2unicode
from data import monster_data as MD
from data import fb_eval_desc_data as FEDD
from data import sys_config_data as SCD

class IFubenEvalInfo(object):

    def __init__(self, evalInfo):
        self.evalInfo = evalInfo
        self.movie = gameglobal.rds.ui.movie

    def getBossDetail(self, bossList, bossCnt):
        ret = self.movie.CreateArray()
        return ret

    def getCombatInfo(self):
        ret = self.movie.CreateObject()
        ret.SetMember('dps', GfxValue(self.evalInfo.get('dps', 0)))
        hideRatio = self.evalInfo.get('hideRatio', 0.0)
        ret.SetMember('hideRatio', GfxValue(gbk2unicode('%.2f%%' % hideRatio)))
        bossList = self.evalInfo.get('bossList', ())
        bossCnt = self.evalInfo.get('bossCnt', 0)
        ret.SetMember('boss', self.getBossDetail(bossList, bossCnt))
        return ret

    def getKillMonster(self):
        ar = self.movie.CreateArray()
        return ar

    def getRecordInfo(self):
        ret = self.movie.CreateObject()
        ret.SetMember('dieCount', GfxValue(self.evalInfo.get('dieCount', 0)))
        ret.SetMember('killMonster', self.getKillMonster())
        ret.SetMember('cure', GfxValue(self.evalInfo.get('cure', 0)))
        ret.SetMember('damage', GfxValue(self.evalInfo.get('beDamage', 0)))
        return ret

    def getAllStatics(self):
        ret = self.movie.CreateObject()
        ret.SetMember('attack', GfxValue(int(self.evalInfo.get(const.FB_EVAL_TYPE_ATTACK, 0))))
        ret.SetMember('defense', GfxValue(int(self.evalInfo.get(const.FB_EVAL_TYPE_DEFENCE, 0))))
        ret.SetMember('skill', GfxValue(0))
        ret.SetMember('finish', GfxValue(self.evalInfo.get(const.FB_EVAL_TYPE_COMP, 0)))
        ret.SetMember('addedScore', GfxValue(self.evalInfo.get(const.FB_EVAL_TYPE_EXTRA, 0)))
        return ret

    def getLevelScore(self):
        scoreArr = [100,
         450,
         800,
         900,
         1000]
        ret = self.movie.CreateArray()
        for idx, item in enumerate(scoreArr):
            ret.SetElement(idx, GfxValue(item))

        return ret

    def getEvalLevel(self):
        return GfxValue(self.evalInfo.get('level', const.FB_EVAL_LEVEL[-1]))

    def getAllStaticsInfo(self):
        ret = self.movie.CreateArray()
        p = BigWorld.player()
        fbNo = formula.getFubenNo(p.spaceNo)
        visibleList = FEDD.data.get(fbNo, [])
        fbEvalDesc = SCD.data.get('fbEvalDesc', {})
        for index, value in enumerate(visibleList):
            desc = fbEvalDesc.get(value, '')
            obj = self.movie.CreateObject()
            obj.SetMember('visibleNum', GfxValue(value))
            obj.SetMember('desc', GfxValue(gbk2unicode(desc)))
            ret.SetElement(index, obj)

        return ret


class FubenEvalInfo(IFubenEvalInfo):

    def __init__(self, evalInfo):
        super(FubenEvalInfo, self).__init__(evalInfo)

    def getBossDetail(self, bossList, bossCnt):
        ret = self.movie.CreateArray()
        ret.SetElement(0, GfxValue(len(bossList)))
        ret.SetElement(1, GfxValue(bossCnt))
        ar = self.movie.CreateArray()
        for i, item in enumerate(bossList):
            bossCharType = item[0]
            bossDuration = item[1]
            md = MD.data.get(bossCharType)
            bossName = md.get('name', '') if md else ''
            itemAr = self.movie.CreateArray()
            itemAr.SetElement(0, GfxValue(gbk2unicode(bossName)))
            itemAr.SetElement(1, GfxValue(bossDuration))
            ar.SetElement(i, itemAr)

        ret.SetElement(2, ar)
        return ret

    def getKillMonster(self):
        ar = self.movie.CreateArray()
        ar.SetElement(0, GfxValue(self.evalInfo.get('killedMonsterCnt', 0)))
        ar.SetElement(1, GfxValue(self.evalInfo.get('totalMonsterCnt', 0)))
        return ar

    def getFubenName(self):
        fbNo = formula.getFubenNo(BigWorld.player().spaceNo)
        return GfxValue(gbk2unicode(formula.getFbDetailName(fbNo)))


class TrainingFubenEvalInfo(IFubenEvalInfo):

    def __init__(self, evalInfo):
        super(TrainingFubenEvalInfo, self).__init__(evalInfo)

    def getBossName(self):
        charType = gameglobal.rds.ui.trainingNpc.diedBossId
        bossName = MD.data.get(charType, {}).get('name', '')
        gamelog.debug('@hjx training#getBossName:', charType)
        return GfxValue(gbk2unicode(bossName))


class ChallengeFubenEvalInfo(TrainingFubenEvalInfo):

    def __init__(self, evalInfo, missionId):
        super(TrainingFubenEvalInfo, self).__init__(evalInfo)
        self.missionId = missionId

    def getAllStaticsInfo(self):
        ret = self.movie.CreateArray()
        visibleList = FEDD.data.get(self.missionId, [])
        fbEvalDesc = SCD.data.get('fbEvalDesc', {})
        for index, value in enumerate(visibleList):
            desc = fbEvalDesc.get(value, '')
            obj = self.movie.CreateObject()
            obj.SetMember('visibleNum', GfxValue(value))
            obj.SetMember('desc', GfxValue(gbk2unicode(desc)))
            ret.SetElement(index, obj)

        return ret

    def getCombatInfo(self):
        ret = self.movie.CreateObject()
        ret.SetMember('dps', GfxValue('--'))
        ret.SetMember('hideRatio', GfxValue('--'))
        bossList = self.evalInfo.get('bossList', ())
        bossCnt = self.evalInfo.get('bossCnt', 0)
        ret.SetMember('boss', self.getBossDetail(bossList, bossCnt))
        return ret

    def getRecordInfo(self):
        ret = self.movie.CreateObject()
        ret.SetMember('dieCount', GfxValue(self.evalInfo.get('dieCount', 0)))
        ret.SetMember('killMonster', self.getKillMonster())
        ret.SetMember('cure', GfxValue('--'))
        ret.SetMember('damage', GfxValue('--'))
        return ret
