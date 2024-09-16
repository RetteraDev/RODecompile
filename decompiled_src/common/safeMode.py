#Embedded file name: I:/bag/tmp/tw2/res/entities\common/safeMode.o
from userSoleType import UserSoleType
from userType import MemberProxy

class SafeMode(UserSoleType):
    onSafeMode = MemberProxy('onSafeMode')
    labour = MemberProxy('labour')
    startTime = MemberProxy('startTime')

    def __init__(self, dic):
        super(SafeMode, self).__init__()
        self.fixedDict = dic
