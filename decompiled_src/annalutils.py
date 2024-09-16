#Embedded file name: /WORKSPACE/data/entities/client/helpers/annalutils.o
import BigWorld
import zlib
import const
import cPickle
import urllib
import json
import base64
import Queue
import threading
import game
import utils
import gamelog
import gameglobal
import pyBgTask
from struct import unpack
from callbackHelper import Functor
MAX_TIME_AFTER_DATA_FINISHED = 30

class AnnalReader(object):

    def __init__(self, server, uuid, host = '', port = '', index = 0, live = False):
        self.server = server
        self.uuid = uuid
        self.host = host
        self.port = port
        self.index = index
        self.live = live
        self.finished = False
        self.stopByForce = False
        self.decompressobj = zlib.decompressobj()
        self.data = Queue.Queue()
        self.lock = threading.Lock()
        self.dataFinishedTime = 0
        self.stopTime = 0

    def isFinished(self):
        return self.finished

    def _fetchData(self, snapshot = False):
        index = self.index
        args = {'server': self.server,
         'uuid': self.uuid,
         'index': index}
        if snapshot:
            args['snapshot'] = 1
        url = 'http://%s:%s/annal/getAnnalR?' % (self.host, self.port) + urllib.urlencode(args)
        handler = urllib.urlopen(url)
        if handler.getcode() != 200:
            return
        responseData = json.loads(handler.read())
        if not responseData:
            return
        self.lock.acquire()
        if not snapshot and index != self.index:
            self.lock.release()
            return
        if self.live:
            annal_data = zlib.decompress(base64.b64decode(responseData['data']))
        else:
            annal_data = self.decompressobj.decompress(base64.b64decode(responseData['data']))
        if responseData.get('finished', False):
            self.dataFinishedTime = utils.getNow()
        self.data.put(annal_data)
        if snapshot:
            self.index = int(responseData.get('index', 0)) + 1
        else:
            self.index += 1
        self.lock.release()

    def fetchDataAsync(self):
        mgr = pyBgTask.getMgr()
        mgr.add_task(self._fetchData, ())

    def fetchDataSync(self, snapshot = False):
        self._fetchData(snapshot=snapshot)
        return self.read()

    def read(self):
        try:
            return self.data.get(False)
        except:
            return ''


ANNAL_READER = None
ANNAL_TIMER_ID = 0

def feedAnnal():
    global ANNAL_READER
    if gameglobal.ANNAL_STATE == gameglobal.ANNAL_STATE_END:
        BigWorld.player().onAnnalReplayFinished(ANNAL_READER.stopByForce)
        return
    reaming_time = BigWorld.getServerAnnalRemainingTime()
    BigWorld.callback(0.5, feedAnnal)
    if reaming_time > 10:
        if ANNAL_READER.live:
            BigWorld.setServerAnnalSpeed(reaming_time)
        return
    BigWorld.setServerAnnalSpeed(10)
    if ANNAL_READER.dataFinishedTime:
        if reaming_time <= 0 or utils.getNow() - ANNAL_READER.dataFinishedTime > MAX_TIME_AFTER_DATA_FINISHED:
            if not ANNAL_READER.stopTime:
                ANNAL_READER.stopTime = utils.getNow() + 5
        if ANNAL_READER.stopTime and utils.getNow() - ANNAL_READER.stopTime > 0:
            gameglobal.ANNAL_STATE = gameglobal.ANNAL_STATE_END
            ANNAL_READER.finished = True
        return
    ANNAL_READER.fetchDataAsync()
    data = ANNAL_READER.read()
    if data:
        BigWorld.feedServerAnnalData(data)


def playAnnal(serverId, uuid, host = '', port = '', index = 0, live = False, fromStart = False, bTimeout = False):
    global ANNAL_READER
    global ANNAL_TIMER_ID
    gamelog.debug('-----m.l@.playAnnal', serverId, uuid)
    if not bTimeout:
        gameglobal.ANNAL_STATE = gameglobal.ANNAL_STATE_PREPARE
    if not bTimeout and ANNAL_TIMER_ID:
        BigWorld.cancelCallback(ANNAL_TIMER_ID)
        ANNAL_TIMER_ID = 0
    ANNAL_READER = AnnalReader(serverId, uuid, host=host, port=port, index=index, live=live)
    data = ANNAL_READER.fetchDataSync(snapshot=live and not fromStart)
    gamelog.debug('-----m.l@.playAnnal dataLen:', len(data))
    if not data:
        if live and not fromStart and BigWorld.player().inWorld:
            gamelog.info('playAnnal live not ready', uuid)
            ANNAL_TIMER_ID = BigWorld.callback(2, Functor(playAnnal, serverId, uuid, host, port, index, live, fromStart, True))
            return
        BigWorld.player().chatToEventEx('无法读取录像', const.CHANNEL_COLOR_RED)
        gameglobal.ANNAL_STATE = gameglobal.ANNAL_STATE_END
        return
    if gameglobal.ANNAL_STATE != gameglobal.ANNAL_STATE_PREPARE:
        return
    gameglobal.ANNAL_STATE = gameglobal.ANNAL_STATE_START
    header_len = unpack('I', data[:4])[0]
    header = cPickle.loads(data[4:header_len + 4])
    gamelog.debug('-----m.l@.playAnnal headerLen:', header_len, ' :header', header)
    BigWorld.loadServerAnnalData(data[header_len + 4:])
    BigWorld.playbackServerAnnal(10, 1.0)
    BigWorld.callback(0.5, feedAnnal)


def setAnnalSpeed(command, func):
    argList = command.split()[1:]
    if len(argList) < 1:
        BigWorld.player().chatToEventEx('参数不足', const.CHANNEL_COLOR_RED)
        return
    BigWorld.setServerAnnalSpeed(float(argList[0]))


def stopPlay():
    global ANNAL_TIMER_ID
    if ANNAL_TIMER_ID:
        BigWorld.cancelCallback(ANNAL_TIMER_ID)
        ANNAL_TIMER_ID = 0
    gameglobal.ANNAL_STATE = gameglobal.ANNAL_STATE_END
    if ANNAL_READER and not ANNAL_READER.isFinished():
        ANNAL_READER.finished = True
        ANNAL_READER.stopByForce = True
        return True
    return False


def testAnnal():
    """http: // 10.246.14.127:8085 /?server = pg_log_26126 & uuid = 6be7b386 - 0e08 - 11e7 - a172 - d8d385e31898 & index = 1"""
    playAnnal('pg_log_26126', '6be7b386-0e08-11e7-a172-d8d385e31898')
