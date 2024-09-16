#Embedded file name: /WORKSPACE/data/entities/common/guideutils.o
import const
import formula
import gameconfigCommon
from data import exp_space_data as ESD

def genMLGuideLowLv(mapId, mlLv):
    esd = ESD.data[mapId]
    if esd.has_key('guideLowLv'):
        guideLowLv = esd['guideLowLv']
    elif esd.has_key('guideLowLvFId'):
        guideLowLv = formula.calcFormulaById(esd['guideLowLvFId'], {'mlLv': mlLv})
    else:
        guideLowLv = None
    if esd.has_key('guideThresholdLv'):
        guideThresLv = esd['guideThresholdLv']
    elif esd.has_key('guideThresholdLvFId'):
        guideThresLv = formula.calcFormulaById(esd['guideThresholdLvFId'], {'mlLv': mlLv})
    else:
        guideThresLv = None
    return (guideLowLv, guideThresLv)


def genMLGuideLowXiuweiLevel(mapId, mlLv):
    import utils
    esd = ESD.data[mapId]
    formulaArgs = {'mlLv': mlLv,
     'openDay': utils.getServerOpenDays(),
     'maxXiuweiLv': utils.getPlayerMaxXiuweiLv()}
    if esd.has_key('guideLowXiuweiLv'):
        lowXiuweiLv = esd['guideLowXiuweiLv']
    elif esd.has_key('guideLowXiuweiLvFId'):
        lowXiuweiLv = formula.calcFormulaById(esd['guideLowXiuweiLvFId'], formulaArgs)
    else:
        lowXiuweiLv = None
    if esd.has_key('guideThresholdXiuweiLv'):
        thresXiuweiLv = esd['guideThresholdXiuweiLv']
    elif esd.has_key('guideThresholdXiuweiLvFId'):
        thresXiuweiLv = formula.calcFormulaById(esd['guideThresholdXiuweiLvFId'], formulaArgs)
    else:
        thresXiuweiLv = None
    return (lowXiuweiLv, thresXiuweiLv)


def getGuideConfigMode(mapId):
    esd = ESD.data.get(mapId)
    if not esd:
        return const.GUIDE_MODE_CHECK_NONE
    lvMargin = esd.get('guideLvMargin')
    lvLow = esd.has_key('guideLowLv') or esd.has_key('guideLowLvFId')
    lvThres = esd.has_key('guideThresholdLv') or esd.has_key('guideThresholdLvFId')
    lvNone = lvMargin is None or lvLow is None or lvThres is None
    if gameconfigCommon.enableGuideModeWithXiuweiLv():
        xiuweiLvMargin = esd.get('guideXiuweiLvMargin')
        xiuweiLvLow = esd.has_key('guideLowXiuweiLv') or esd.has_key('guideLowXiuweiLvFId')
        xiuweiLvThres = esd.has_key('guideThresholdXiuweiLv') or esd.has_key('guideThresholdLvFId')
        xiuweiLvNone = xiuweiLvMargin is None or xiuweiLvLow is None or xiuweiLvThres is None
    else:
        xiuweiLvNone = True
    if not lvNone and not xiuweiLvNone:
        return const.GUIDE_MODE_CHECK_LV_AND_XIUWEI_LV
    if lvNone and not xiuweiLvNone:
        return const.GUIDE_MODE_CHECK_XIUWEI_LV
    if not lvNone and xiuweiLvNone:
        return const.GUIDE_MODE_CHECK_LV
    return const.GUIDE_MODE_CHECK_NONE


def checkGuideByMarginWithLv(mapId, lv, minLv):
    esd = ESD.data.get(mapId)
    if not esd:
        return (False, False)
    guideLvMargin = esd.get('guideLvMargin')
    _, guideThresLv = genMLGuideLowLv(mapId, lv)
    if guideLvMargin is None or guideThresLv is None:
        return (False, False)
    if lv >= minLv + guideLvMargin and lv >= guideThresLv:
        return (True, True)
    return (True, False)


def checkGuideByMarginWithXiuweiLv(mapId, lv, xiuweiLv, minXiuweiLv):
    esd = ESD.data.get(mapId)
    if not gameconfigCommon.enableGuideModeWithXiuweiLv() or not esd:
        return (False, False)
    guideXiuweiLvMargin = esd.get('guideXiuweiLvMargin')
    _, guideThresXiuweiLv = genMLGuideLowXiuweiLevel(mapId, lv)
    if guideXiuweiLvMargin is None or guideThresXiuweiLv is None:
        return (False, False)
    if xiuweiLv >= minXiuweiLv + guideXiuweiLvMargin and xiuweiLv >= guideThresXiuweiLv:
        return (True, True)
    return (True, False)


def checkGuideByMargin(mapId, lv, minLv, xiuweiLevel, minXiuweiLevel):
    if not ESD.data.has_key(mapId):
        return False
    lvCfg, lvCheck = checkGuideByMarginWithLv(mapId, lv, minLv)
    xiuweiLvCfg, xiuweiLvCheck = checkGuideByMarginWithXiuweiLv(mapId, lv, xiuweiLevel, minXiuweiLevel)
    if lvCfg and xiuweiLvCfg:
        return lvCheck and xiuweiLvCheck
    elif lvCfg and not xiuweiLvCfg:
        return lvCheck
    elif not lvCfg and xiuweiLvCfg:
        return xiuweiLvCheck
    else:
        return False


def checkBeGuideByMarginWithLv(mapId, lv, maxLv):
    esd = ESD.data.get(mapId)
    if not gameconfigCommon.enableGuideModeWithXiuweiLv() or not esd:
        return (False, False)
    guideLvMargin = esd.get('guideLvMargin')
    _, guideThresLv = genMLGuideLowLv(mapId, lv)
    if guideLvMargin is None or guideThresLv is None:
        return (False, False)
    if maxLv >= guideThresLv and maxLv - lv >= guideThresLv:
        return (True, True)
    return (True, False)


def checkBeGuideByMarginWithXiuweiLv(mapId, lv, xiuweiLv, maxXiuweiLv):
    esd = ESD.data.get(mapId)
    if not esd:
        return (False, False)
    guideXiuweiLvMargin = esd.get('guideXiuweiLvMargin')
    _, guideThresXiuweiLv = genMLGuideLowXiuweiLevel(mapId, lv)
    if guideXiuweiLvMargin is None or guideThresXiuweiLv is None:
        return (False, False)
    if maxXiuweiLv >= guideThresXiuweiLv and maxXiuweiLv - xiuweiLv >= guideThresXiuweiLv:
        return (True, True)
    return (True, False)


def checkBeGuideByMargin(mapId, lv, maxLv, xiuweiLevel, maxXiuweiLevel):
    esd = ESD.data.get(mapId)
    if not esd:
        return (False, False)
    lvCfg, lvCheck = checkBeGuideByMarginWithLv(mapId, lv, maxLv)
    xiuweiLvCfg, xiuweiLvCheck = checkBeGuideByMarginWithXiuweiLv(mapId, lv, xiuweiLevel, maxXiuweiLevel)
    if lvCfg and xiuweiLvCfg:
        return lvCheck and xiuweiLvCheck
    elif lvCfg and not xiuweiLvCfg:
        return lvCheck
    elif not lvCfg and xiuweiLvCfg:
        return xiuweiLvCheck
    else:
        return False


def getGuideModeWithLv(mapId, lv, minLv, maxLv = None):
    esd = ESD.data.get(mapId)
    if not esd:
        return (False, const.GUIDE_NONE_MODE)
    guideLvMargin = esd.get('guideLvMargin')
    guideLowLv, guideThresLv = genMLGuideLowLv(mapId, lv)
    if guideLvMargin is None or guideLowLv is None or guideThresLv is None:
        return (False, const.GUIDE_NONE_MODE)
    mode = const.GUIDE_NONE_MODE
    if lv <= guideLowLv:
        if maxLv is None:
            mode = const.GUIDE_ROOKIE_MODE
        elif maxLv - lv >= guideLvMargin and maxLv >= guideThresLv:
            mode = const.GUIDE_ROOKIE_MODE
    if lv - minLv >= guideLvMargin and lv >= guideThresLv:
        mode = const.GUIDE_MASTER_AND_ROOKIE_MODE if mode == const.GUIDE_ROOKIE_MODE else const.GUIDE_MASTER_MODE
    return (True, mode)


def getGuideModeWithXiuweiLv(mapId, lv, xiuweiLv, minXiuweiLv, maxXiuweiLevel = None):
    esd = ESD.data.get(mapId)
    if not gameconfigCommon.enableGuideModeWithXiuweiLv() or not esd:
        return (False, const.GUIDE_NONE_MODE)
    guideXiuweiLvMargin = esd.get('guideXiuweiLvMargin')
    guideLowXiuweiLv, guideThresXiuweiLv = genMLGuideLowXiuweiLevel(mapId, lv)
    if guideXiuweiLvMargin is None or guideLowXiuweiLv is None or guideThresXiuweiLv is None:
        return (False, const.GUIDE_NONE_MODE)
    mode = const.GUIDE_NONE_MODE
    if xiuweiLv <= guideLowXiuweiLv:
        if maxXiuweiLevel is None:
            mode = const.GUIDE_ROOKIE_MODE
        elif maxXiuweiLevel - xiuweiLv >= guideXiuweiLvMargin and maxXiuweiLevel >= guideThresXiuweiLv:
            mode = const.GUIDE_ROOKIE_MODE
    if xiuweiLv - minXiuweiLv >= guideXiuweiLvMargin and xiuweiLv >= guideThresXiuweiLv:
        mode = const.GUIDE_MASTER_AND_ROOKIE_MODE if mode == const.GUIDE_ROOKIE_MODE else const.GUIDE_MASTER_MODE
    return (True, mode)


def getGuideMode(mapId, lv, minLv, xiuweiLevel, minXiuweiLevel, maxLv = None, maxXiuweiLevel = None):
    esd = ESD.data.get(mapId)
    if not esd:
        return const.GUIDE_NONE_MODE
    lvCfg, lvMode = getGuideModeWithLv(mapId, lv, minLv, maxLv)
    xiuweiLvCfg, xiuweiLvMode = getGuideModeWithXiuweiLv(mapId, lv, xiuweiLevel, minXiuweiLevel, maxXiuweiLevel)
    if lvCfg and not xiuweiLvCfg:
        return lvMode
    if not lvCfg and xiuweiLvCfg:
        return xiuweiLvMode
    if lvCfg and xiuweiLvCfg:
        if lvMode == xiuweiLvMode:
            return lvMode
        else:
            return max(lvMode, xiuweiLvMode)
    else:
        return const.GUIDE_NONE_MODE
