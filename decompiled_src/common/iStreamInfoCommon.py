#Embedded file name: I:/bag/tmp/tw2/res/entities\common/iStreamInfoCommon.o
import cPickle
import utils
from data import sys_config_data as SCD
REQUIRED_METHODS = ['_createObjFromStream', '_getStreamFromObj']

class IStreamInfoCommon(object):

    def createFromStream(self, stream):
        return self._createObjFromStream(cPickle.loads(stream))

    def addToStream(self, obj):
        return cPickle.dumps(self._getStreamFromObj(obj), -1)


def bindStreamCommon(instance, cls):
    oldbases = instance.__class__.__bases__
    if cls in oldbases:
        return False
    for method in REQUIRED_METHODS:
        if not hasattr(instance, method):
            return -1

    newbases = list(oldbases)
    newbases.append(cls)
    newbases = tuple(newbases)
    instance.__class__.__bases__ = newbases
    return True


def bindStream(instance):
    bindStreamCommon(instance, IStreamInfoCommon)
