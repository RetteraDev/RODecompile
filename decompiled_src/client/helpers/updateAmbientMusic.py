#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/updateAmbientMusic.o
import BigWorld
import ResMgr
import C_ui
import Sound
import formula
import clientcom
import const
import gamelog
from data import map_config_data as MCD
_doUpdateAmbient = False

def startAmbientSound():
    global _doUpdateAmbient
    gamelog.debug('updateAmbientMusic: start ambient sound')
    if Sound.isSoundDisabled():
        return
    if _doUpdateAmbient:
        return
    _doUpdateAmbient = True
    checkAmbientSound()


def endAmbientSound():
    global _oldChunk
    global _oldSpace
    global _reverbTag
    global _isSpaceChanged
    global _doUpdateAmbient
    global _reverbRoom
    _doUpdateAmbient = False
    _oldSpace = None
    _oldChunk = None
    _reverbTag = None
    _reverbRoom = None
    _isSpaceChanged = True
    gamelog.debug('updateAmbientMusic: end ambient sound')


_hour = None
_minute = None
_lasthour = None
_lastminute = None
_lasttime = None
_timeleap = 0.365749657955
_timeflag = 0

def updateAmbientTod():
    global _timeleap
    global _lastminute
    global _minute
    global _lasthour
    global _lasttime
    global _hour
    global _timeflag
    tod = BigWorld.timeOfDay()
    if tod != '':
        hour = int(tod[0:2])
        minute = int(tod[3:5])
        if _hour != hour or minute != _minute:
            _timeflag += 1
            _hour = hour
            _minute = minute
            if _timeflag % 5 == 0:
                oldlasttime = _lasttime
                oldlasthour = _lasthour
                oldlastminute = _lastminute
                _lasthour = _hour
                _lastminute = _minute
                _lasttime = BigWorld.time()
                if oldlasthour is not None and oldlastminute is not None and oldlasttime is not None:
                    dtime = _lasttime - oldlasttime
                    dgametime = _hour * 60 + _minute - oldlasthour * 60 - oldlastminute
                    if dtime > 0 and dgametime > 0:
                        _timeleap = float(dgametime) / float(dtime)
            if _timeflag % 120 == 0:
                t = float(hour) + float(minute) / 60.0
                Sound.setMusicParam('hour', t)
                Sound.setAmbientParam('hour', t)
                Sound.updateTimeOfDay(t)


class SceneSound(object):

    def __init__(self):
        self.music = None
        self.ambient = None
        self.reverb = None
        self.room = 50


_soundMap = {}

def readSubzone(subzone, space):
    global _soundMap
    for i in subzone:
        name, data = i
        name = data.openSection('name').asString
        gamelog.debug('updateAmbientMusic:initSoundMap(): load sub zone %s' % name)
        if name in _soundMap:
            gamelog.error("initSoundMap:: duplicate zone name exists in \'sound/scene.xml\'")
        else:
            music = data.readString('music', space.music)
            ambient = data.readString('ambient', space.ambient)
            reverb = data.openSection('reverb')
            asnd = SceneSound()
            asnd.music = music
            asnd.ambient = ambient
            if reverb is not None:
                asnd.reverb = reverb.openSection('preset').asString
                asnd.room = reverb.openSection('room').asFloat
            _soundMap[name] = asnd


def initSoundMap():
    gamelog.debug('updateAmbientMusic:initSoundMap().')
    sec = ResMgr.openSection('sound/scene.xml')
    if sec is None:
        gamelog.error("updateAmbientMusic:init_sound_map(): no \'sound/scene.xml\' found!")
        return
    items = sec.items()
    for i in items:
        name, data = i
        if name == 'space':
            isSpace = True
        else:
            isSpace = False
        name = data.openSection('name').asString
        if name in _soundMap:
            gamelog.error("updateAmbientMusic:init_sound_map: duplicate zone name exists in \'sound/scene.xml\'")
        else:
            music = data.openSection('music')
            if music is not None:
                music = music.asString
            ambient = data.openSection('ambient')
            if ambient is not None:
                ambient = ambient.asString
            reverb = data.openSection('reverb')
            asnd = SceneSound()
            asnd.music = music
            asnd.ambient = ambient
            if reverb is not None:
                asnd.reverb = reverb.openSection('preset').asString
                asnd.room = reverb.openSection('room').asFloat
            _soundMap[name] = asnd
            if isSpace:
                subzone = data.openSection('subzone')
                if subzone:
                    readSubzone(subzone.items(), asnd)


def getAreaInfo():
    p = clientcom.getPlayerAvatar()
    st = ''
    if p:
        st = BigWorld.ChunkInfoAt((p.position.x, p.position.y + 1, p.position.z))
    return st


def getSpaceInfo():
    p = clientcom.getPlayerAvatar()
    if p is not None:
        spaceNo = p.spaceNo
        spaceName = formula.whatSpaceName(spaceNo)
    else:
        zone = C_ui.get_map_name()
        spaceNo = formula.getSpaceNo(zone[0])
        spaceName = formula.whatSpaceName(spaceNo, True)
    return spaceName


_oldChunk = None
_oldSpace = None
_isSpaceChanged = True

def doCheckAmbientSound():
    global _isSpaceChanged
    if not _doUpdateAmbient:
        gamelog.debug('updateAmbientMusic: stop')
        return
    p = clientcom.getPlayerAvatar()
    if not p or not p.inWorld:
        return
    mapId = formula.getMapId(p.spaceNo)
    if mapId == const.SPACE_NO_BIG_WORLD or MCD.data.get(mapId, {}).get('updateAmbientTod', 0):
        updateAmbientTod()
    newSpace = getSpaceInfo()
    newChunk = getAreaInfo()
    if _oldSpace != newSpace:
        _isSpaceChanged = True
    elif _isSpaceChanged:
        _isSpaceChanged = False
    if _isSpaceChanged or _oldChunk != newChunk:
        changeAmbientSound(newSpace, newChunk)


def checkAmbientSound():
    TIME_SPAN = 6
    if not _doUpdateAmbient:
        return
    doCheckAmbientSound()
    BigWorld.callback(TIME_SPAN, checkAmbientSound)


def changeAmbientSound(space, chunk):
    global _oldChunk
    global _oldSpace
    if _oldSpace != space:
        changeSpace = True
    else:
        changeSpace = False
    if _oldChunk != chunk:
        changeChunk = True
    else:
        changeChunk = False
    gamelog.debug('updateAmbientMusic: zone changed (%s/%s) old - (%s/%s) ' % (space,
     chunk,
     _oldSpace,
     _oldChunk))
    _oldChunk = chunk
    _oldSpace = space
    if space == '':
        gamelog.error('updateAmbientMusic: null space')
        return
    zoneChangeCallback(space, chunk, changeSpace, changeChunk)


_reverbTag = None
_reverbRoom = None

def zoneChangeCallback(space, chunk, changeSpace, changeChunk):
    global _reverbTag
    global _reverbRoom
    if space != _oldSpace or chunk != _oldChunk:
        gamelog.debug('updateAmbientMusic: zone change cancelled')
        return
    if space not in _soundMap:
        Sound.changeSpace('', '')
        Sound.changeZone('', '')
        Sound.turnoffReverb()
        gamelog.debug("updateAmbientMusic: sound map doesn\'t contains space key %s" % space)
        return
    space_asnd = _soundMap[space]
    music = space_asnd.music
    ambient = space_asnd.ambient
    gamelog.debug('updateAmbientMusic: -space music ', music)
    if chunk in _soundMap:
        chunk_asnd = _soundMap[chunk]
        music = chunk_asnd.music
        ambient = chunk_asnd.ambient
        _reverbTag = chunk_asnd.reverb
        _reverbRoom = chunk_asnd.room
    else:
        _reverbTag = space_asnd.reverb
        _reverbRoom = space_asnd.room
    chunk_music = music
    chunk_ambient = ambient
    gamelog.debug('updateAmbientMusic: change ambient & music (%s/%s) - %s' % (space, chunk, music))
    if music is None:
        music = space_asnd.music
        if music is None:
            music = ''
    if ambient is None:
        ambient = space_asnd.ambient
        if ambient is None:
            ambient = ''
    if changeSpace:
        gamelog.debug('updateAmbientMusic: change space music ', music)
        Sound.changeSpace(music, ambient)
        if not changeChunk:
            Sound.changeZone(chunk_music, chunk_ambient)
    if changeChunk:
        gamelog.debug('updateAmbientMusic: change zone music ', music)
        Sound.changeZone(chunk_music, chunk_ambient)
    if _reverbTag is None:
        gamelog.debug('updateAmbientMusic: turn off reverb')
        Sound.turnoffReverb()
    else:
        gamelog.debug("updateAmbientMusic: change reverb to \'%s\'" % _reverbTag)
        Sound.setReverb(_reverbTag, _reverbRoom)


def restoreReverb():
    if _reverbTag is not None and _reverbRoom is not None:
        Sound.setReverb(_reverbTag, _reverbRoom)
    else:
        Sound.turnoffReverb()
