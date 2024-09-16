#Embedded file name: I:/bag/tmp/tw2/res/entities\common/homeFittingRoomInfo.o
from userInfo import UserInfo
from homeFittingRoom import HomeFittingRoom, HomeFittingRoomVal

class HomeFittingRoomInfo(UserInfo):

    def createObjFromDict(self, dict):
        froom = HomeFittingRoom()
        for cd in dict['fittingRoomData']:
            val = HomeFittingRoomVal(cd['equips'])
            val.aspect = cd['aspect']
            val.physique = cd['physique']
            val.hairColor = cd['hairColor']
            val.actionId = cd['actionId']
            val.avatarConfig = cd['avatarConfig']
            froom[cd['uuid']] = val

        return froom

    def getDictFromObj(self, obj):
        data = []
        for uuid, val in obj.iteritems():
            data.append({'uuid': uuid,
             'equips': val.equips,
             'aspect': val.aspect,
             'physique': val.physique,
             'avatarConfig': val.avatarConfig,
             'hairColor': val.hairColor,
             'actionId': val.actionId})

        return {'fittingRoomData': data}

    def isSameType(self, obj):
        return type(obj) is HomeFittingRoom


instance = HomeFittingRoomInfo()
