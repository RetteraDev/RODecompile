#Embedded file name: I:/bag/tmp/tw2/res/entities\common/homePersonInfo.o
from userInfo import UserInfo
from homePerson import HomePerson

class HomePersonInfo(UserInfo):

    def createObjFromDict(self, dict):
        obj = HomePerson(roomId=dict['roomId'], state=dict['state'], tcreate=dict['tcreate'], ownerGbID=dict['ownerGbID'], ownerName=dict['ownerName'])
        obj.curLineNo = dict['curLineNo']
        obj.curFloorNo = dict['curFloorNo']
        obj.curRoomNo = dict['curRoomNo']
        obj.curRoomId = dict['curRoomId']
        obj.lineNo = dict['lineNo']
        obj.floorNo = dict['floorNo']
        obj.roomNo = dict['roomNo']
        obj.roomBox = dict['roomBox']
        obj.roomAccessRecord = dict['roomAccessRecord']
        obj.lastUseBackHomeSkillTime = dict['lastUseBackHomeSkillTime']
        obj.fittingRoomLv = dict['fittingRoomLv']
        obj.erooms = dict['erooms']
        obj.eRoomAuthDict = dict['eRoomAuthDict']
        obj.roomSpaceType = dict['roomSpaceType']
        obj.eroomAuthType = dict['eroomAuthType']
        if obj.roomAccessRecord == None:
            obj.roomAccessRecord = []
        if obj.erooms == None:
            obj.erooms = []
        if obj.eRoomAuthDict == None:
            obj.eRoomAuthDict = {}
        return obj

    def getDictFromObj(self, obj):
        return {'roomId': obj.roomId,
         'state': obj.state,
         'tcreate': obj.tcreate,
         'ownerGbID': obj.ownerGbID,
         'ownerName': obj.ownerName,
         'curLineNo': obj.curLineNo,
         'curFloorNo': obj.curFloorNo,
         'curRoomNo': obj.curRoomNo,
         'curRoomId': obj.curRoomId,
         'lineNo': obj.lineNo,
         'floorNo': obj.floorNo,
         'roomNo': obj.roomNo,
         'roomBox': obj.roomBox,
         'roomAccessRecord': obj.roomAccessRecord,
         'lastUseBackHomeSkillTime': obj.lastUseBackHomeSkillTime,
         'fittingRoomLv': obj.fittingRoomLv,
         'erooms': obj.erooms,
         'eRoomAuthDict': obj.eRoomAuthDict,
         'roomSpaceType': obj.roomSpaceType,
         'eroomAuthType': obj.eroomAuthType}

    def isSameType(self, obj):
        return type(obj) is HomePerson


instance = HomePersonInfo()
