#Embedded file name: I:/bag/tmp/tw2/res/entities\common/checkResult.o


class CheckResult(object):

    def __init__(self, result, param = None):
        self.__dict__['result'] = result
        self.__dict__['param'] = param

    def __nonzero__(self):
        return self.result

    def __eq__(self, other):
        if type(other) is bool:
            return self.result == other
        raise ()

    def __str__(self):
        return str(self.result)

    def __repr__(self):
        return 'CR_' + str(self.result)

    def __setattr__(self, key, value):
        raise ()
