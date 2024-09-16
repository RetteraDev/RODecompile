#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\pyasn1\codec\ber/eoo.o
from pyasn1.type import base, tag

class EndOfOctets(base.AbstractSimpleAsn1Item):
    defaultValue = 0
    tagSet = tag.initTagSet(tag.Tag(tag.tagClassUniversal, tag.tagFormatSimple, 0))


endOfOctets = EndOfOctets()
