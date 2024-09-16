#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/redPotUtils.o
import BigWorld
from Scaleform import GfxValue
from guis import uiConst
import keys
import uiUtils
from appSetting import Obj as AppSettings
RED_POT_SHOW_TYPE_STATE = 1
RED_POT_SHOW_TYPE_ONCE = 2
redPotArr = None
redPotSet = set()

def onGetRedPotVisible(*args):
    global redPotSet
    global redPotArr
    if redPotArr == None:
        p = BigWorld.player()
        if p and p.gbId:
            tmpVal = AppSettings.get(keys.SET_DONE_RED_POT_UNIQUE_IDS % p.gbId, '')
        else:
            tmpVal = AppSettings.get(keys.SET_DONE_RED_POT_IDS, '')
        if tmpVal:
            redPotArr = tmpVal.split(',')
        else:
            redPotArr = []
        redPotSet = set(redPotArr)
    redPotId = int(args[3][0].GetNumber())
    return GfxValue(str(redPotId) not in redPotArr)


def onGetRedPotInfo(*args):
    redPotId = int(args[3][0].GetNumber())
    info = getPotData(redPotId)
    return uiUtils.dict2GfxDict(info, True)


def onHandleRedPot(*args):
    p = BigWorld.player()
    redPotId = int(args[3][0].GetNumber())
    info = getPotData(redPotId)
    if info['showType'] == RED_POT_SHOW_TYPE_ONCE:
        redPotIdStr = str(redPotId)
        if redPotIdStr not in redPotSet:
            redPotSet.add(redPotIdStr)
            redPotArr.append(redPotIdStr)
            if p and p.gbId:
                AppSettings[keys.SET_DONE_RED_POT_UNIQUE_IDS % p.gbId] = ','.join(redPotArr)
            else:
                AppSettings[keys.SET_DONE_RED_POT_IDS] = ','.join(redPotArr)


def getPotData(potId):
    if potId == uiConst.CARDSLOT_RESONANCE_RED_POT:
        return {'isExpired': False,
         'redPotType': 1,
         'redPotId': potId,
         'showType': RED_POT_SHOW_TYPE_ONCE}
    return {'isExpired': False,
     'redPotType': 1,
     'redPotId': potId,
     'showType': RED_POT_SHOW_TYPE_STATE}
