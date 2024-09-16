#Embedded file name: I:/bag/tmp/tw2/res/entities\common/userType.o


class UserDispatch(object):

    def present(self):
        return self.box != None

    def callBase(self, methodName, args):
        try:
            getattr(self.box, methodName)(*args)
        except AttributeError:
            return False

        return True

    def dispatchBase(self, methodFlag, args):
        try:
            self.box.dispatchBase(methodFlag, args)
        except AttributeError:
            return False

        return True

    def callCell(self, methodName, args):
        try:
            getattr(self.box.cell, methodName)(*args)
        except AttributeError:
            return False

        return True

    def dispatchCell(self, methodFlag, args):
        try:
            self.box.cell.dispatchCell(methodFlag, args)
        except AttributeError:
            return False

        return True

    def callClient(self, methodName, args):
        try:
            getattr(self.box.client, methodName)(*args)
        except AttributeError:
            return False

        return True

    def dispatchClient(self, methodFlag, args):
        try:
            self.box.client.dispatchClient(methodFlag, args)
        except AttributeError:
            return False

        return True


class UserMultiDispatch(object):

    def callBase(self, methodName, args, exclude = ()):
        for k, v in self.iteritems():
            if k in exclude:
                continue
            v.callBase(methodName, args)

    def dispatchBase(self, methodFlag, args, exclude = ()):
        for k, v in self.iteritems():
            if k in exclude:
                continue
            v.dispatchBase(methodFlag, args)

    def callCell(self, methodName, args, exclude = ()):
        for k, v in self.iteritems():
            if k in exclude:
                continue
            v.callCell(methodName, args)

    def dispatchCell(self, methodFlag, args, exclude = ()):
        for k, v in self.iteritems():
            if k in exclude:
                continue
            v.dispatchCell(methodFlag, args)

    def callClient(self, methodName, args, exclude = ()):
        for k, v in self.iteritems():
            if k in exclude:
                continue
            v.callClient(methodName, args)

    def dispatchClient(self, methodFlag, args, exclude = ()):
        for k, v in self.iteritems():
            if k in exclude:
                continue
            v.dispatchClient(methodFlag, args)


class MemberProxy(object):

    def __init__(self, member):
        self.member = member

    def __get__(self, instance, owner):
        return instance.fixedDict[self.member]

    def __set__(self, instance, value):
        instance.fixedDict[self.member] = value

    def __delete__(self, instance):
        raise NotImplementedError(self.member)


class UserType(object):

    def introspect(self):
        pass

    def __str__(self):
        return str(vars(self))
