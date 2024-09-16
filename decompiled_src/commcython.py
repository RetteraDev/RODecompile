#Embedded file name: /WORKSPACE/data/entities/common/commcython.o
import BigWorld

def cythonfuncentry(f):
    if BigWorld.component != 'cell':
        return f
    import bwdecorator
    return bwdecorator.cythonfuncentry(f)
