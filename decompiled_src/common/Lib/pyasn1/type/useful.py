#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\pyasn1\type/useful.o
from pyasn1.type import char, tag

class GeneralizedTime(char.VisibleString):
    tagSet = char.VisibleString.tagSet.tagImplicitly(tag.Tag(tag.tagClassUniversal, tag.tagFormatSimple, 24))


class UTCTime(char.VisibleString):
    tagSet = char.VisibleString.tagSet.tagImplicitly(tag.Tag(tag.tagClassUniversal, tag.tagFormatSimple, 23))
