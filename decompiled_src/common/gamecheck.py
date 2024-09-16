#Embedded file name: I:/bag/tmp/tw2/res/entities\common/gamecheck.o
from cdata import taboo_name_data as TND

def quanjiaoToBanjiao(ustring):
    """\xb0\xd1\xd7\xd6\xb7\xfb\xb4\xae\xc8\xab\xbd\xc7\xd7\xaa\xb0\xeb\xbd\xc7"""
    rstring = ''
    for uchar in ustring:
        ucode = ord(uchar)
        if not (65313 <= ucode <= 65338 or 65345 <= ucode <= 65370 or 65296 <= ucode <= 65305):
            rstring += uchar
            continue
        if ucode == 12288:
            ucode = 32
        else:
            ucode -= 65248
        if ucode < 32 or ucode > 126:
            rstring += uchar
        rstring += unichr(ucode)

    return rstring


def inTabooName(name):
    tName = quanjiaoToBanjiao(name)
    for t in TND.data:
        if tName.lower().find(t) != -1:
            return True

    return False
