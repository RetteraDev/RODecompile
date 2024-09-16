#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/soundVolGradient.o
import Sound
import BigWorld

class SoundVolFader(object):
    VolFaderList = []

    def __init__(self, restoreFunc, getFunc, setFunc, addToList = True):
        super(SoundVolFader, self).__init__()
        self.restoreFunc = restoreFunc
        self.getFunc = getFunc
        self.setFunc = setFunc
        self.dstVol = restoreFunc()
        self.hCallback = None
        self.step = 5
        self.interval = 0.1
        if addToList:
            SoundVolFader.VolFaderList.append(self)

    def fadeTo(self, dstVol, step = 5, interval = 0.1):
        if dstVol == -1:
            dstVol = self.restoreFunc()
        self.dstVol = dstVol
        self.step = step
        self.interval = interval
        if self.hCallback is None:
            self._fadeTo()

    def _fadeTo(self):
        goOnFlag = False
        self.hCallback = None
        curVol = self.getFunc()
        if curVol == self.dstVol:
            return
        if curVol > self.dstVol:
            curVol -= self.step
            if curVol <= self.dstVol:
                curVol = self.dstVol
            else:
                goOnFlag = True
        else:
            curVol += self.step
            if curVol >= self.dstVol:
                curVol = self.dstVol
            else:
                goOnFlag = True
        self.setFunc(curVol)
        if goOnFlag:
            self.hCallback = BigWorld.callback(self.interval, self._fadeTo)

    @staticmethod
    def restoreAll(self):
        for vf in SoundVolFader.VolFaderList:
            vf.fadeTo(-1)

    @staticmethod
    def release(self):
        SoundVolFader.restoreAll()
        SoundVolFader.VolFaderList = []


class AmbientVolFader(SoundVolFader):
    FaderObj = None

    def __init__(self):
        super(AmbientVolFader, self).__init__(Sound.getAmbientVolume, Sound.getAmbientVolume, Sound.setAmbientVolume)


class MusicVolFader(SoundVolFader):
    FaderObj = None

    def __init__(self):
        super(MusicVolFader, self).__init__(Sound.getMusicVolume, Sound.getMusicVolume, Sound.setMusicVolume)


class UIVolFader(SoundVolFader):
    FaderObj = None

    def __init__(self):
        super(UIVolFader, self).__init__(Sound.getUiVolume, Sound.getUiVolume, Sound.setUiVolume)


class StaticVolFader(SoundVolFader):
    FaderObj = None

    def __init__(self):
        super(StaticVolFader, self).__init__(Sound.getStaticVolume, Sound.getStaticVolume, Sound.setStaticVolume)


class EffectVolFader(SoundVolFader):
    FaderObj = None

    def __init__(self):
        super(EffectVolFader, self).__init__(Sound.getEffectVolume, Sound.getEffectVolume, Sound.setEffectVolume)


class CategoryVolFader(SoundVolFader):
    FaderObj = None

    def __init__(self):
        super(CategoryVolFader, self).__init__(Sound.getCategoryVolume, Sound.getCategoryVolume, Sound.setCategoryVolume)


def fadeAmbientVol(dstVol, step = 5, interval = 0.1):
    if AmbientVolFader.FaderObj is None:
        AmbientVolFader.FaderObj = AmbientVolFader()
    AmbientVolFader.FaderObj.fadeTo(dstVol, step, interval)


def fadeMusicVol(dstVol, step = 5, interval = 0.1):
    if MusicVolFader.FaderObj is None:
        MusicVolFader.FaderObj = MusicVolFader()
    MusicVolFader.FaderObj.fadeTo(dstVol, step, interval)


def fadeFxVol(dstVol, step = 5, interval = 0.1):
    if EffectVolFader.FaderObj is None:
        EffectVolFader.FaderObj = EffectVolFader()
    EffectVolFader.FaderObj.fadeTo(dstVol, step, interval)


def fadeUiVol(dstVol, step = 5, interval = 0.1):
    if UIVolFader.FaderObj is None:
        UIVolFader.FaderObj = UIVolFader()
    UIVolFader.FaderObj.fadeTo(dstVol, step, interval)


def fadeStaticVol(dstVol, step = 5, interval = 0.1):
    if StaticVolFader.FaderObj is None:
        StaticVolFader.FaderObj = StaticVolFader()
    StaticVolFader.FaderObj.fadeTo(dstVol, step, interval)


def fadeCategoryVol(dstVol, step = 5, interval = 0.1):
    if CategoryVolFader.FaderObj is None:
        CategoryVolFader.FaderObj = CategoryVolFader()
    CategoryVolFader.FaderObj.fadeTo(dstVol, step, interval)
