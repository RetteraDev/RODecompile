#Embedded file name: /WORKSPACE/data/entities/client/helpers/preload.o
import BigWorld
import gamelog
import clientcom
import clientUtils
from helpers import cgPlayer
gPreloadMap = {}
gPreloadTemp = []

def getWeaponList():
    fileList = []
    return fileList


alreadyRun = False

def getPreloadList():
    global alreadyRun
    if alreadyRun:
        return []
    alreadyRun = True
    preloadExtraInfo()
    preloadList = _getLogonScenePM() + PRE_Picture + getWeaponList() + _getPreloadRole() + PRE_OtherModel
    preloadList.extend(_getPreloadRoleNew())
    gamelog.debug('================getPreloadList end=================')
    return preloadList


def preloadExtraInfo():
    if clientcom.enableBinkLogoCG():
        cgPlayer.preloadBinkMovie('logo')
        cgPlayer.preloadBinkMovie('login')
    else:
        cgPlayer.preloadMovie('logo')


def preloadModel(filename):
    global gPreloadTemp
    global gPreloadMap
    try:
        m = clientUtils.model(filename)
    except:
        gamelog.error('ERR can not preload model')
        return

    if filename[:6] == 'scene/':
        gPreloadTemp.append(m)
    else:
        gPreloadMap[filename] = m


def _getPreloadRole():
    alist = []
    for k in PRE_NewRole:
        path = clientcom.getNewXrjmModelPath(k).get('fullPath')
        alist += [path]

    return alist


def _getPreloadRoleNew():
    ret = []
    for school in PRE_NewRole:
        path = clientcom.getLoginModelNewPath(school).get('fullPath')
        ret.append(path)

    return ret


def _getLogonScenePM():
    alist = ['scene/common/jz/jztj/tjcs/nslj_jztj_cs1000_wb.model',
     'scene/common/jz/jztj/tjcs/nslj_jztj_cs2120_wb_lod1.model',
     'scene/common/zw/zwshu/ycj_zwshu0010_1201.model',
     'scene/common/zw/zwshu/nslj_zwshu1010_wb_lod2.model',
     'scene/common/jz/jzsj/sjcs/slj_jzsj_cs0910_wb.model',
     'scene/common/jz/jztj/tjcs/nslj_jztj_cs1060_01_wb.model',
     'scene/common/jz/jztj/tjcs/nslj_jztj_cs1230_wb.model',
     'scene/common/jz/jztj/tjyw/nslj_jztj_yw1020_2642.model',
     'scene/common/jz/jztj/tjcs/nslj_jztj_cs1370_wb.model',
     'scene/common/jz/jztj/tjcs/nslj_jztj_cs1150_wb.model',
     'scene/common/wj/wjgy/nslj_wjgy2010_wb.model']
    return alist


def freeTempPreload():
    global gPreloadTemp
    global gPreloadMap
    gPreloadTemp = []
    gPreloadMap = {}


PRE_Picture = []
PRE_Scene = []
PRE_NewRole = [3,
 4,
 5,
 6,
 7,
 8,
 9]
PRE_OtherModel = []
PRE_BaseModel = []
PRE_BaseModel_Game = []
