#Embedded file name: /WORKSPACE/data/entities/common/lzydteamseat.o
from userSoleType import UserSoleType
from userDictType import UserDictType
from userType import UserDispatch
import copy
import utils
import gamebase
import gamelog
import const
import func
import gameutils

class HumanVal(UserSoleType, UserDispatch):

    def __init__(self, arenaScore = 0, roleName = '', school = const.SCHOOL_SHENTANG, sex = 0, bodyType = 0, level = 20, box = None, isBlockWarning = False, founderNUID = 0, fromHostId = 0, rewardFlag = 0):
        super(HumanVal, self).__init__()
        self.box = box
        self.ready = False
        self.roleName = roleName
        self.school = school
        self.sex = sex
        self.bodyType = bodyType
        self.level = level
        self.arenaScore = arenaScore
        self.isBlockWarning = isBlockWarning
        self.fromHostName = box.hostName if utils.instanceof(box, 'GlobalMailBox') else ''
        self.founderNUID = founderNUID
        self.fromHostId = fromHostId
        self.rewardFlag = rewardFlag

    def note(self, msg, chEvent = const.CHANNEL_COLOR_GREEN, chSystem = None):
        if self.box == None:
            return
        if self.box.client == None:
            return
        if chEvent:
            self.box.client.chatToEventEx(msg, chEvent)
        if chSystem:
            self.box.client.chatToEventEx(msg)

    def _lateReload(self):
        super(HumanVal, self)._lateReload()
        if self.box != None and self.box.__class__.__name__ == 'GlobalMailBox':
            self.box.reloadScript()


class SeatHuman(UserDictType):

    def _lateReload(self):
        super(SeatHuman, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def note(self, msg, chEvent = const.CHANNEL_COLOR_GREEN, chSystem = None):
        for hVal in self.itervalues():
            hVal.note(msg, chEvent, chSystem)


class SeatVal(UserSoleType):

    def __init__(self, arenaLv, tQueue = 0, arenaMode = 0, human = SeatHuman()):
        super(SeatVal, self).__init__()
        self.arenaLv = arenaLv
        self.tQueue = tQueue
        self.arenaMode = arenaMode
        self.human = copy.deepcopy(human)

    def _lateReload(self):
        super(SeatVal, self)._lateReload()
        self.human.reloadScript()

    def same(self, arenaMode):
        return self.arenaMode == arenaMode

    def howManyH(self):
        return len(self.human)

    def avgLv(self):
        cnt = len(self.human)
        sumLv = 0
        for gbId, val in self.human.items():
            sumLv = sumLv + val.level

        if cnt > 0:
            return int(sumLv / cnt)

    def avgScore(self):
        cnt = len(self.human)
        sumScore = 0
        for gbId, val in self.human.items():
            sumScore = sumScore + val.arenaScore

        if cnt > 0:
            return int(sumScore / cnt)
        return 0

    def schoolList(self):
        schList = []
        for gbId, val in self.human.items():
            schList.append(val.school)

        return schList

    def gbIdList(self):
        return self.human.keys()

    def boxList(self):
        boxList = []
        for gbId, val in self.human.items():
            boxList.append(val.box)

        return boxList

    def hasH(self, gbId):
        return self.human.has_key(gbId)

    def popH(self, gbId):
        return self.human.pop(gbId, None)

    def getH(self, gbId):
        return self.human.get(gbId, None)

    def pushH(self, gbId, roleName, sch, sex, bodyType, lv, box, arenaScore, isBlockWarning, founderNUID = 0, fromHostId = 0, rewardFlag = 0):
        self.human[gbId] = HumanVal(box=box, roleName=roleName, school=sch, sex=sex, bodyType=bodyType, level=lv, arenaScore=arenaScore, isBlockWarning=isBlockWarning, founderNUID=founderNUID, fromHostId=fromHostId, rewardFlag=rewardFlag)


class LzydTeamSeat(UserDictType):

    def _lateReload(self):
        super(LzydTeamSeat, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def inQueue(self, gbId):
        for t in self.keys():
            sVal = self[t]
            if sVal.hasH(gbId):
                return True

        return False

    def popQueue(self, gbId):
        gamelog.debug('@hjx arena#popQueue:', gbId, self.keys())
        for t in self.keys():
            self.desertT(gbId, t, True)

    def insertT(self, gbId, role, box, lv, sch, ticket, extra, arenaMode):
        gamelog.info('czf insertT', ticket)
        for t, sVal in self.items():
            gbIdList = sVal.gbIdList()
            if gbId in gbIdList:
                sVal.human[gbId].box = box
                return

        now = utils.getNow()
        arenaFakeScore = extra.get('arenaFakeScore', 0)
        sex = extra.get('sex', 0)
        bodyType = extra.get('bodyType', 0)
        isBlockWarning = extra.get('isBlockWarning', False)
        founderNUID = extra.get('founderNUID', 0)
        fromHostId = extra.get('fromHostId')
        rewardFlag = extra.get('rewardFlag', 0)
        sVal = SeatVal(tQueue=now, arenaMode=arenaMode, arenaLv=arenaFakeScore)
        sVal.pushH(gbId, role, sch, sex, bodyType, lv, box, arenaFakeScore, isBlockWarning, founderNUID, fromHostId, rewardFlag)
        self[ticket] = sVal
        member = {}
        member[gbId] = {'roleName': role,
         'school': sch,
         'sex': sex,
         'bodyType': bodyType,
         'arenaFakeScore': arenaFakeScore,
         'box': box,
         'lv': lv}
        box.cell.onArenaLzydApply(arenaMode)

    def insertTeamT(self, agentGbId, ticket, members, arenaMode):
        for t, sVal in self.items():
            gbIdList = sVal.gbIdList()
            if agentGbId in gbIdList:
                return

        now = utils.getNow()
        gamelog.info('insertTeamT', members)
        sVal = SeatVal(tQueue=now, arenaMode=arenaMode, arenaLv=gameutils.calcTeamAvgArenaScore(members))
        for gbId, mVal in members.iteritems():
            box = mVal['box']
            founderNUID = 0
            sVal.pushH(gbId, mVal['roleName'], mVal['school'], mVal['sex'], mVal['bodyType'], mVal['lv'], mVal['box'], mVal['arenaFakeScore'], False, founderNUID, mVal['fromHostId'], 0)
            box.cell.onArenaTeamLzydApply(arenaMode)

        self[ticket] = sVal

    def updateBox(self, box, gbId, ticket):
        sVal = self.get(ticket, None)
        if sVal:
            if sVal.hasH(gbId):
                sVal.human[gbId].box = box

    def deleteBox(self, gbId, ticket):
        sVal = self.get(ticket, None)
        if sVal:
            if sVal.hasH(gbId) and sVal.howManyH() <= 1:
                sVal.human[gbId].box = None

    def enlargeT(self, way, tutor, ticket, role, box, xiuwei):
        pass
