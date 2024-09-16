#Embedded file name: I:/bag/tmp/tw2/res/entities\common/commonDecorator.o
import BigWorld
import sys
if BigWorld.component in ('base', 'cell'):
    import gameengine

def callonserver(f):

    def fwrap(*args, **kwargs):
        if BigWorld.component == 'client':
            raise AttributeError('%s cannot call on client' % (f.func_name,))
        return f(*args, **kwargs)

    return fwrap


def assetReturnValueNotEquals(cond):

    def assetReturnValueInner(f):

        def fwrap(*args, **kwargs):
            ret = f(*args, **kwargs)
            if BigWorld.component in ('base', 'cell'):
                try:
                    if isinstance(cond, (tuple, list)):
                        condList = cond
                    else:
                        condList = [cond]
                    for x in condList:
                        if ret == x:
                            gameengine.reportSevereCritical('assertion return value failed: func[%s] args[%s]' % (f, (args, kwargs)))
                            break

                except:
                    gameengine.exceptHook(*sys.exc_info())

            return ret

        return fwrap

    return assetReturnValueInner
