#Embedded file name: /WORKSPACE/data/entities/common/lzydteamseatinfo.o
from userInfo import UserInfo
from lzydTeamSeat import LzydTeamSeat, SeatVal, SeatHuman, HumanVal

class lzydTeamSeatInfo(UserInfo):

    def createObjFromDict(self, dict):
        bt = LzydTeamSeat()
        for child in dict['seat']:
            human = SeatHuman()
            for subChild in child['human']:
                hVal = HumanVal(box=subChild['box'], arenaScore=subChild['arenaScore'], roleName=subChild['roleName'], school=subChild['school'], sex=subChild['sex'], bodyType=subChild['bodyType'], level=subChild['level'], isBlockWarning=subChild['isBlockWarning'])
                human[subChild['gbId']] = hVal

            sVal = SeatVal(tQueue=child['tQueue'], fbNo=child['fbNo'], human=human)
            bt[child['ticketNo']] = sVal

        return bt

    def getDictFromObj(self, obj):
        sVals = []
        for tNo, sVal in obj.iteritems():
            hVals = []
            for hGbId, hVal in sVal.human.iteritems():
                hVals.append({'gbId': hGbId,
                 'box': hVal.box,
                 'roleName': hVal.roleName,
                 'school': hVal.school,
                 'level': hVal.level,
                 'sex': hVal.sex,
                 'bodyType': hVal.bodyType,
                 'arenaScore': hVal.arenaScore,
                 'isBlockWarning': hVal.isBlockWarning,
                 'fromHostName': hVal.fromHostName})

            sVals.append({'ticketNo': tNo,
             'tQueue': sVal.tQueue,
             'fbNo': sVal.fbNo,
             'human': hVals})

        return {'seat': sVals}

    def isSameType(self, obj):
        return type(obj) is LzydTeamSeat


instance = lzydTeamSeatInfo()
