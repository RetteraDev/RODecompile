#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/regExpUtils.o
import re
import Scaleform
from guis import uiUtils

def replace(*arg):
    return Scaleform.GfxValue(re.sub(arg[3][1].GetString(), arg[3][2].GetString(), arg[3][0].GetString(), 0, int(round(arg[3][3].GetNumber()))))


def findAll(*arg):
    result = re.findall(arg[3][0].GetString(), arg[3][1].GetString(), int(round(arg[3][2].GetNumber())))
    return uiUtils.array2GfxAarry(result)
