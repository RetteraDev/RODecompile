#Embedded file name: I:/bag/tmp/tw2/res/entities\common/mapMarkerInfo.o
from mapMarker import MapMarker, MapMarkerVal
from userInfo import UserInfo

class MapMarkerInfo(UserInfo):

    def createObjFromDict(self, dict):
        marker = MapMarker()
        for val in dict['markers']:
            marker[val['index']] = MapMarkerVal(val['index'], val['pos'], val['title'], val['desc'])

        return marker

    def getDictFromObj(self, obj):
        vals = []
        for v in obj.itervalues():
            vals.append({'index': v.index,
             'pos': v.pos,
             'title': v.title,
             'desc': v.desc})

        return {'markers': vals}

    def isSameType(self, obj):
        return type(obj) is MapMarker


instance = MapMarkerInfo()
