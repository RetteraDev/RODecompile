#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/chatRoom.o
import copy
import const
import gametypes

class Member(object):

    def __init__(self, gbId = 0, role = '', school = 0, level = 0, tJoin = 0, sex = const.SEX_MALE, roleId = gametypes.CHATROOM_ROLE_NORMAL):
        super(Member, self).__init__()
        self.gbId = gbId
        self.role = role
        self.school = school
        self.level = level
        self.tJoin = tJoin
        self.sex = sex
        self.roleId = roleId


class ChatRoom(object):

    def __init__(self, rHeader = 0, rBuild = 0, tBuild = 0, fName = '', fType = gametypes.CHATROOM_TYPE_ALL, member = {}):
        super(ChatRoom, self).__init__()
        self.rHeader = rHeader
        self.rBuild = rBuild
        self.tBuild = tBuild
        self.fName = fName
        self.fType = fType
        self.member = copy.deepcopy(member)
