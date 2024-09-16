#Embedded file name: I:/bag/tmp/tw2/res/entities\common/titleInfo.o
import BigWorld
if BigWorld.component != 'database':
    from title import Title, TitleVal
from userInfo import UserInfo
if BigWorld.component == 'client':
    from iStreamInfoCommon import bindStream
else:
    from iStreamInfo import bindStream

class TitleInfo(UserInfo):

    def createObjFromDict(self, dict):
        titles = Title()
        for val in dict['titles']:
            titles[val['title']] = TitleVal(title=val['title'], tGain=val['tGain'], tAttr=val['tAttr'], tOutdate=val['tOutdate'])

        return titles

    def getDictFromObj(self, obj):
        vals = []
        for v in obj.itervalues():
            vals.append({'title': v.title,
             'tGain': v.tGain,
             'tAttr': v.tAttr,
             'tOutdate': v.tOutdate})

        return {'titles': vals}

    def _createObjFromStream(self, stream):
        titles = Title()
        for title, tGain, tAttr, tOutdate in stream:
            tVal = TitleVal(title=title, tGain=tGain, tAttr=tAttr, tOutdate=tOutdate)
            titles[title] = tVal

        return titles

    def _getStreamFromObj(self, obj):
        return [ (v.title,
         v.tGain,
         v.tAttr,
         v.tOutdate) for v in obj.itervalues() ]

    def isSameType(self, obj):
        return type(obj) is Title


instance = TitleInfo()
bindStream(instance)
