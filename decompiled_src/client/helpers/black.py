#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/black.o
import GUI
import Math
import BigWorld
from callbackHelper import Functor

def genMask(black):
    if black:
        return GUI.Simple('gui/intro/blackScreenMask.dds')
    else:
        return GUI.Simple('gui/intro/whtieScreenMask.dds')


def bo(black = True):
    black = genMask(black)
    black.materialFX = 'BLEND'
    black.horizontalAnchor = 'LEFT'
    black.verticalAnchor = 'TOP'
    aShader = GUI.AlphaShader('ALL')
    black.addShader(aShader, 'as')
    black.shader = aShader
    aShader.alpha = 1
    black.height = 2.02
    black.width = 2.02
    black.position = Math.Vector3(-1.01, 1.01, 0.05)
    GUI.addRoot(black, 2)
    black.visible = False
    return black


BLACK = bo()
WHITE = bo(False)

def clear(mask = BLACK):
    mask.visible = False


def fadein(t = 1.0, mask = BLACK, callback = None):
    mask.visible = True
    _start = BigWorld.time()
    _end = _start + t
    _f1(_end, mask, _start, callback, t)


def _f1(_end, mask, _start, callback, t):
    f_t = BigWorld.time()
    if f_t >= _end:
        mask.shader.alpha = 1.0
        callback() if callback else None
        return
    BigWorld.callback(0, Functor(_f1, _end, mask, _start, callback, t))
    _perc = (f_t - _start) / t
    mask.shader.alpha = _perc


def fadeout(t = 1.0, mask = BLACK, callback = None):
    _start = BigWorld.time()
    _end = _start + t
    _f2(_end, mask, _start, callback, t)


def _f2(_end, mask, _start, callback, t):
    f_t = BigWorld.time()
    if f_t >= _end:
        mask.visible = False
        callback() if callback else None
        return
    BigWorld.callback(0, Functor(_f2, _end, mask, _start, callback, t))
    _perc = (f_t - _start) / t
    mask.shader.alpha = 1 - _perc


def fade(fadeInTime = 0.1, duration = 1.0, fadeOutTime = 0.1, isWhite = False):
    global WHITE
    global BLACK
    mask = isWhite and WHITE or BLACK
    fadein(fadeInTime, mask)
    BigWorld.callback(fadeInTime + duration, Functor(_f3, fadeOutTime, mask))


def _f3(fadeOutTime, mask):
    fadeout(fadeOutTime, mask)
