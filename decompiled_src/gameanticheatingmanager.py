#Embedded file name: /WORKSPACE/data/entities/client/helpers/gameanticheatingmanager.o
import BigWorld
import os
import C_ui
import json
import gameglobal
import gamelog
import gametypes
import utils
import keys
import formula
import remoteInterface
from guis.ui import gbk2unicode
from gameclass import Singleton
from callbackHelper import Functor
from data import map_config_data as MCD
TEST_JSON_FILE_PATH = 'C:/Users/zhengmingkai/Desktop/gameAntiCheatingLogs'
TEST_JSON_FILE_NAME_PREFIX = 'antiCheating_'
TEST_JSON_FILE_NAME_POSTFIX = '.json'
KEY_FILE_PATH = 'C:/ZMKWorkPlace/TY/entities/client/helpers/certification/gameAntiCheating.key'
CERT_FILE_PATH = 'C:/ZMKWorkPlace/TY/entities/client/helpers/certification/gameAntiCheating.crt'
LOG_OPERATION_ID = '10010001'
TIME_FORMAT_STR = '%Y-%m-%d %H:%M:%S'
PROJECT_NAME = 'tianyu'
ANTI_CHEATING_ID = '1001'
KEY_STR_MAP = {(keys.KEY_MOUSE0, True): 'LDown',
 (keys.KEY_MOUSE0, False): 'LUp',
 (keys.KEY_MOUSE1, True): 'RDown',
 (keys.KEY_MOUSE1, False): 'RUp'}
GAME_RECORD_TIME_OFFSET = 0.4
GAME_RECORD_SEND_TIME_OFFSET = 20

def getInstance():
    return GameAntiCheatingManager.getInstance()


class GameAntiCheatingManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.isRecording = False
        self.curCallbackTime = 0
        self.recordCallbackId = 0
        self.mouseMoveData = list()
        self.mouseKeyData = list()
        self.keyboardKeyData = list()
        self.playerPosData = list()
        self.qinggongInfoData = list()
        self.isInQinggong = False
        self.isLoseFocus = False
        self.isCurLoseFocus = False
        self.isMinimize = False

    @property
    def playerMapID(self):
        p = BigWorld.player()
        return p.mapID

    def startRecordLog(self):
        gamelog.debug('@zmk antiCheating#startRecordLog', self.curCallbackTime)
        if not self.checkNeedRecordLog():
            self.stopRecordLog()
            return
        if self.isRecording:
            self.stopRecordLog()
        self.startRecordCallBack()

    def stopRecordLog(self):
        gamelog.debug('@zmk antiCheating#stopRecordLog', self.isRecording, self.curCallbackTime)
        if not self.isRecording or not self.curCallbackTime:
            return
        prefixResult, result = self.genMainData()
        jsonResult = self.genJsonData(result)
        result = self.genDictData('value', prefixResult + jsonResult)
        jsonResult = self.genJsonData(result)
        self.sendRecordLog(jsonResult)
        self.resetAllData()

    def sendRecordLog(self, jsonResult):
        remoteInterface.sendGameAntiCheatingInfo(jsonResult, KEY_FILE_PATH, CERT_FILE_PATH, self.onSendRecordLogCallback)

    def readStrFromFile(self, filePath):
        if not os.path.isfile(filePath):
            gamelog.error('@zmk  GameAntiCheatingManager - filePath is None: ', filePath)
        tempFile = open(filePath, 'r')
        fileStr = tempFile.read()
        tempFile.close()
        return fileStr

    def onSendRecordLogCallback(self, response, content):
        if response:
            gamelog.debug('@zmk antiCheating#onSendRecordLogCallback', response.status, content)
        else:
            gamelog.error('@zmk  antiCheating#onSendRecordLogCallback - response is None, send is error')
        if not content:
            return

    def testSaveJsonDataLocal(self, result):
        fileName = TEST_JSON_FILE_NAME_PREFIX + str(utils.getNow(True)) + TEST_JSON_FILE_NAME_POSTFIX
        filePath = os.path.join(TEST_JSON_FILE_PATH, fileName)
        if not os.path.exists(TEST_JSON_FILE_PATH):
            os.makedirs(TEST_JSON_FILE_PATH)
        with open(filePath, 'w') as jsonFile:
            json.dump(result, jsonFile, ensure_ascii=False, separators=(',', ':'), encoding='utf-8')

    def resetAllData(self):
        self.isRecording = False
        self.recordCallbackId and BigWorld.cancelCallback(self.recordCallbackId)
        self.curCallbackTime = 0
        self.mouseMoveData = list()
        self.mouseKeyData = list()
        self.keyboardKeyData = list()
        self.playerPosData = list()
        self.qinggongInfoData = list()
        self.isLoseFocus = False
        self.isMinimize = False

    def clearAll(self):
        self.resetAllData()

    def startRecordCallBack(self):
        if not self.checkNeedRecordLog():
            self.stopRecordLog()
            return
        self.isRecording = True
        self.recordCallbackId and BigWorld.cancelCallback(self.recordCallbackId)
        self.recordCallbackId = BigWorld.callback(GAME_RECORD_TIME_OFFSET, self.startRecordCallBack)
        self.curCallbackTime += GAME_RECORD_TIME_OFFSET
        if self.curCallbackTime >= GAME_RECORD_SEND_TIME_OFFSET:
            self.startRecordLog()
        else:
            self.genMouseMoveData(self.mouseMoveData)
            self.genPlayerPosData(self.playerPosData)

    def recordKeyData(self, key, down):
        if not self.isRecording:
            return
        if key in [keys.KEY_MOUSE0, keys.KEY_MOUSE1]:
            keyStr = KEY_STR_MAP.get((key, down), '')
            self.genMouseKeyData(self.mouseKeyData, keyStr)
        else:
            self.genKeyBoardKeyData(self.keyboardKeyData, key, down)

    def recordQinggongData(self, isInQinggong):
        if self.isInQinggong != isInQinggong:
            self.isInQinggong = isInQinggong
            if not self.isRecording:
                return
            self.genQinggongInfoData(self.qinggongInfoData, isInQinggong)

    def recordLoseFocusData(self, act):
        self.isCurLoseFocus = not act
        if not act:
            self.isLoseFocus = True

    def recordMinimizeData(self, isMinimize):
        if not self.isRecording:
            return
        if isMinimize:
            self.isMinimize = True

    def checkNeedRecordLog(self):
        if gameglobal.rds.GameState != gametypes.GS_PLAYGAME:
            return False
        p = BigWorld.player()
        if not p or p.__class__.__name__ == 'PlayerAccount':
            return False
        if not gameglobal.rds.configData.get('enableGameAntiCheatingLog', False):
            return False
        if p.life == gametypes.LIFE_DEAD:
            return False
        if not MCD.data.get(self.playerMapID, {}).get('needAntiCheatingLog', 0):
            return False
        antiCheatingLoopQuestList = MCD.data.get(self.playerMapID, {}).get('antiCheatingLoopQuestList', [])
        if antiCheatingLoopQuestList and not self.checkQuest(antiCheatingLoopQuestList):
            return False
        return True

    def checkQuest(self, antiCheatingLoopQuestList):
        p = BigWorld.player()
        questInfoCache = p.questInfoCache.get('unfinished_taskLoops', [])
        completeQuestInfoCache = p.questInfoCache.get('complete_taskLoops', [])
        isHaveQuest = False
        for antiCheatingQuest in antiCheatingLoopQuestList:
            if antiCheatingQuest in questInfoCache or antiCheatingQuest in completeQuestInfoCache:
                isHaveQuest = True
                break

        return isHaveQuest

    def genMainData(self):
        p = BigWorld.player()
        if not p or p.__class__.__name__ == 'PlayerAccount':
            return
        mapData = MCD.data.get(self.playerMapID, {})
        result = dict()
        prefixResult = '[%s][%s][%s]' % (utils.formatCustomTime(utils.getNow(True), TIME_FORMAT_STR), PROJECT_NAME, LOG_OPERATION_ID)
        result['server'] = utils.getCurrHostId()
        result['logTimeMs'] = utils.getNowMillisecond()
        result['roleId'] = p.gbId
        result['gameplayId'] = mapData.get('antiCheatingGamePlayId', 0)
        result['gameplayName'] = gbk2unicode(mapData.get('antiCheatingGamePlayName', ''))
        result['sceneId'] = self.playerMapID
        result['fubenId'] = str(p.spaceNo)
        result['keyboardPressValue'] = self.keyboardKeyData
        result['mouseMoveValue'] = self.mouseMoveData
        result['mouseKeyValue'] = self.mouseKeyData
        result['playerLocation'] = self.playerPosData
        result['qinggongInfo'] = self.qinggongInfoData
        result['cameraMode'] = p.getOperationMode()
        result['otherInfo'] = {'minimize': 1 if self.isMinimize else 0,
         'loseFocus': 1 if self.isLoseFocus else 0}
        return (prefixResult, result)

    def genJsonData(self, result):
        jsonResult = json.dumps(result, separators=(',', ':'))
        return jsonResult

    def genDictData(self, key, resultStr):
        resultDict = dict()
        resultDict[key] = resultStr
        return resultDict

    def genMouseKeyData(self, result, keyStr):
        if result is None:
            result = list()
        curTime = utils.getNowMillisecond()
        mousePos = C_ui.get_cursor_pos()
        if mousePos:
            result.append({'tm': curTime,
             'x': mousePos[0],
             'y': mousePos[1],
             'tp': keyStr})

    def genMouseMoveData(self, result):
        if result is None:
            result = list()
        curTime = utils.getNowMillisecond()
        mousePos = C_ui.get_cursor_pos()
        if mousePos:
            if not self.isCurLoseFocus:
                result.append({'tm': curTime,
                 'x': mousePos[0],
                 'y': mousePos[1]})
            else:
                result.append({})

    def genKeyBoardKeyData(self, result, keyCode, down):
        if result is None:
            result = list()
        curTime = utils.getNowMillisecond()
        result.append({'tm': curTime,
         'tp': 'd' if down else 'u',
         'code': keyCode})

    def genPlayerPosData(self, result):
        if result is None:
            result = list()
        p = BigWorld.player()
        curTime = utils.getNowMillisecond()
        result.append({'x': p.position[0],
         'y': p.position[2],
         'tm': curTime})

    def genQinggongInfoData(self, result, isInQinggong):
        if result is None:
            result = list()
        p = BigWorld.player()
        curTime = utils.getNowMillisecond()
        result.append({'x': p.position[0],
         'y': p.position[2],
         'z': p.position[1],
         'tm': curTime,
         'opType': 'enter' if isInQinggong else 'leave'})
