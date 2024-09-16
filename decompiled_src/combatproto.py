#Embedded file name: /WORKSPACE/data/entities/common/combatproto.o
from proto import skillresult_pb2
import gamelog

def parseResultRecorder(r):
    rrr = []
    if r.results:
        for prs in r.results:
            rrs = PBResultSet(prs.eid)
            if prs.moveId > 0:
                rrs.moveId = prs.moveId
                rrs.moveTime = prs.moveTime
            if prs.moveParam:
                rrs.moveParam = parseMoveParam(prs.moveParam)
            rrs.kill = prs.kill
            rrs.realDmg = prs.realDmg
            if prs.controllStateData:
                for v in prs.controllStateData:
                    rrs.controllStateData.append((v.controllStateId, v.controllStateHit))

            if prs.addFlagStates:
                for v in prs.addFlagStates:
                    rrs.addFlagStates.append((v.flagStateId, v.lastTime))

            if prs.dispellFlagStates:
                rrs.dispellFlagStates.extend(prs.dispellFlagStates)
            if prs.fenshen:
                for v in prs.fenshen:
                    if v.tgtPos:
                        tgtPos = (v.tgtPos.x, v.tgtPos.y, v.tgtPos.z)
                    rrs.fenshenVal.extend((v.id,
                     (v.fenshenPos.x, v.fenshenPos.y, v.fenshenPos.z),
                     tgtPos,
                     v.yaw))

            if prs.results:
                for prr in prs.results:
                    rr = PBResult()
                    rr.dmgs = prr.dmgs
                    rr.hps = prr.hps
                    rr.mps = prr.mps
                    rr.eps = prr.eps
                    rr.ars = prr.ars
                    rr.seId = prr.seId
                    rr.srcId = prr.srcid
                    rr.labours = prr.labours
                    rr.comboNum = prr.comboNum
                    rr.comboDmg = prr.comboDmg
                    if prr.dmgAbsorb:
                        dmgAbsorb = []
                        for dmgAbsorbVal in prr.dmgAbsorb.elements:
                            dmgAbsorb.append([dmgAbsorbVal.value, dmgAbsorbVal.source, dmgAbsorbVal.srcid])

                        rr.damageAbsorb = dmgAbsorb
                    if prr.healAbsorb:
                        rr.healAbsorb = [ [dmgAbsorbVal.value, dmgAbsorbVal.source, dmgAbsorbVal.srcid] for dmgAbsorbVal in prr.healAbsorb.elements ]
                    rrs.results.append(rr)

            gamelog.debug('jorsef: rrs:realDmg ', rrs.realDmg)
            rrr.append(rrs)

    return rrr


gSkillResult = skillresult_pb2.SkillResult()

def getSkillResultProto(tgtId, num, lv, isInstantSkill, skillCD, skillGCD, guideCastTime, playAction = True, pos = None, timeStamp = 0):
    global gSkillResult
    r = gSkillResult
    r.Clear()
    r.tgtId, r.num, r.lv = tgtId, num, lv
    if skillCD:
        r.cd = skillCD
    if skillGCD:
        r.gcd = skillGCD
    if guideCastTime:
        r.guideCastTime = guideCastTime
    if r.isInstantSkill != isInstantSkill:
        r.isInstantSkill = isInstantSkill
    if pos:
        r.pos.extend(pos)
    if r.dontPlayAction == playAction:
        r.dontPlayAction = not playAction
    if timeStamp:
        r.timeStamp = timeStamp
    return r


def parseMoveParam(moveParam):
    if moveParam:
        moveId = moveParam.refId
        srcPos = None
        if moveParam.srcPos:
            srcPos = tuple(moveParam.srcPos)
        distFixType = moveParam.distFixType
        distFixValue = moveParam.distFixVal
        if distFixValue or distFixValue:
            return (moveId, srcPos, (distFixType, distFixValue))
        else:
            return (moveId, srcPos, None)
    else:
        return ()


def skillResultProtoClient(bytes):
    r = gSkillResult
    try:
        r.ParseFromString(bytes)
    except:
        return None

    prr = parseResultRecorder(r)
    skillResult = SkillResult()
    skillResult.tgtId = r.tgtId
    skillResult.skillId = r.num
    skillResult.skillLv = r.lv
    skillResult.resultType = 0
    skillResult.isInstantSkill = r.isInstantSkill
    skillResult.skillCD = r.cd
    skillResult.skillGCD = r.gcd
    skillResult.guideCastTime = r.guideCastTime
    skillResult.targetPos = r.pos
    skillResult.playAction = not r.dontPlayAction
    skillResult.timeStamp = r.timeStamp
    skillResult.resultSet = prr
    gamelog.debug('jorsef: get skill client', skillResult)
    return skillResult


gAttackResult = skillresult_pb2.AttackResult()

def getAttackResultProto(tgtId):
    global gAttackResult
    r = gAttackResult
    r.Clear()
    r.tgtId = tgtId
    return r


def attackResultProtoClient(bytes):
    gamelog.debug('attackResultProtoClient')
    r = gAttackResult
    r.ParseFromString(bytes)
    prr = parseResultRecorder(r)
    gamelog.debug('jorsef:', r.tgtId, r.resultType, prr, r.nextAtkDelay)
    return (r.tgtId,
     r.resultType,
     prr,
     r.nextAtkDelay)


gCombatMessage = skillresult_pb2.CombatMessage()

def combatMessageProto(num, data, dmg = None, toall = False):
    global gCombatMessage
    r = gCombatMessage
    r.Clear()
    r.num = num
    for x in data:
        if isinstance(x, int) or isinstance(x, float):
            r.args.add(d=int(x))
        else:
            r.args.add(s=x)

    if dmg:
        if dmg[0] > 0:
            r.dmg0 = dmg[0]
        if dmg[1] > 0:
            r.dmg1 = dmg[1]
        if dmg[2] > 0:
            r.dmg2 = dmg[2]
        if dmg[3] > 0:
            r.dmg3 = dmg[3]
        if dmg[4] > 0:
            r.dmg4 = dmg[4]
        if dmg[5] > 0:
            r.dmg5 = dmg[5]
        if dmg[6] > 0:
            r.dmg6 = dmg[6]
        if dmg[7] > 0:
            r.dmg7 = dmg[7]
        r.dmg = True
    if r.toall != toall:
        r.toall = toall
    return r.SerializePartialToString()


def combatMessageProtoClient(bytes):
    r = gCombatMessage
    r.ParseFromString(bytes)
    args = []
    for x in r.args:
        if x.HasField('d'):
            args.append(int(x.d))
        else:
            args.append(x.s)

    if r.dmg:
        dmg = (r.dmg0,
         r.dmg1,
         r.dmg2,
         r.dmg3,
         r.dmg4,
         r.dmg5,
         r.dmg6,
         r.dmg7)
    else:
        dmg = None
    return (r.num,
     tuple(args),
     dmg,
     r.toall)


gMfResult = skillresult_pb2.MFResult()

def getMfResultProto(magicfieldId, num, lv, sid = -1, slv = -1, rPosList = []):
    global gMfResult
    r = gMfResult
    r.Clear()
    r.magicfieldId, r.num, r.lv = magicfieldId, num, lv
    if sid > 0:
        r.skillId = sid
    if slv > 0:
        r.skillLv = slv
    if rPosList:
        for pos in rPosList:
            tp = r.rPosList.add()
            tp.x, tp.y, tp.z = pos[0], pos[1], pos[2]

    return r


def mfResultProtoClient(bytes):
    r = gMfResult
    r.ParseFromString(bytes)
    magicfieldId, num, lv = r.magicfieldId, r.num, r.lv
    skillId = r.skillId if r.skillId else -1
    skillLv = r.skillLv if r.skillLv else -1
    prr = parseResultRecorder(r)
    rPosList = []
    for p in r.rPosList:
        rPosList.append((p.x, p.y, p.z))

    return (magicfieldId,
     num,
     int(lv),
     prr,
     skillId,
     int(skillLv),
     rPosList)


gFenshenResult = skillresult_pb2.FenshenResult()

def getFenShenResultProto(fenshenId, skillId, skillLv):
    global gFenshenResult
    r = gFenshenResult
    r.Clear()
    r.fenshenId = fenshenId
    r.skillId = skillId
    r.skillLv = skillLv
    return r


def fenshenResultProtoClient(bytes):
    r = gFenshenResult
    r.ParseFromString(bytes)
    prr = parseResultRecorder(r)
    return (r.fenshenId, prr)


gPskillResult = skillresult_pb2.PSkillResult()

def getPSkillResultProto(pskillNum, pskillLv):
    global gPskillResult
    r = gPskillResult
    r.Clear()
    r.pskillId, r.pskillLv = pskillNum, pskillLv
    return r


def PSkillResultProtoClient(bytes):
    r = gPskillResult
    r.ParseFromString(bytes)
    pskillNum, pskillLv = r.pskillId, r.pskillLv
    prr = parseResultRecorder(r)
    return (pskillNum, pskillLv, prr)


gGuideSkillResult = skillresult_pb2.GuideSkillResult()

def getGuideSkillResultProto(tgtId, num, lv, pos = None):
    global gGuideSkillResult
    r = gGuideSkillResult
    r.Clear()
    r.tgtId, r.num, r.lv = tgtId, num, lv
    if pos:
        r.pos.extend(pos)
    return r


def guideSkillResultProtoClient(bytes):
    r = gGuideSkillResult
    r.ParseFromString(bytes)
    tgtId, num, lv, rs_tmp, pos = (r.tgtId,
     r.num,
     r.lv,
     r.results,
     r.pos)
    prr = parseResultRecorder(r)
    gamelog.debug('jorsef: guideSkillResultProtoClient', tgtId, num, int(lv), prr, tuple(pos))
    return (tgtId,
     num,
     int(lv),
     prr,
     tuple(pos))


class SkillResult(object):

    def __init__(self):
        super(SkillResult, self).__init__()
        self.tgtId = 0
        self.skillId = 0
        self.skillLv = 0
        self.resultType = 0
        self.skillCD = 0.0
        self.skillGCD = 0.0
        self.guideCastTime = 0.0
        self.isInstantSkill = False
        self.targetPos = None
        self.playAction = True
        self.timeStamp = 0.0
        self.resultSet = []

    def initData(self, x):
        pass

    def __str__(self):
        return str(vars(self))


class PBResult(object):

    def __init__(self):
        super(PBResult, self).__init__()
        self.srcId = 0
        self.dmgSource = 0
        self.dmgSourceId = 0
        self.dmgs = []
        self.hps = 0
        self.mps = 0
        self.eps = 0
        self.ars = 0
        self.seId = 0
        self.damageAbsorb = []
        self.labours = 0
        self.comboNum = 0
        self.comboDmg = 0
        self.healAbsorb = []

    def __str__(self):
        return str(vars(self))


class PBResultSet(object):

    def __init__(self, eid):
        self.eid = eid
        self.results = []
        self.moveId = 0
        self.moveTime = 0.0
        self.moveParam = None
        self.kill = False
        self.realDmg = 0
        self.controllStateData = []
        self.addFlagStates = []
        self.dispellFlagStates = []
        self.fenshenVal = []

    def __str__(self):
        return str(vars(self))
