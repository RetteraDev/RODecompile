#Embedded file name: I:/bag/tmp/tw2/res/entities\client/actionCallback.o
import gamelog
import gameglobal
from guis import topLogo

class callbackClass(object):

    def __init__(self, model):
        self.model = model

    def callback(self, cueId, data, actionName):
        if cueId == 1:
            gameglobal.rds.sound.playFx(data, self.model.position, False)
        else:
            gamelog.error('not support other cueId so far')


class CallbackClassEx(object):

    def __init__(self, matrix):
        self.matrix = matrix

    def callback(self, cueId, data, actionName):
        params = data.split(':')
        soundPath = str(params[0])
        if cueId == 1:
            gameglobal.rds.sound.playFx(soundPath, self.matrix.position, False)
        else:
            gamelog.error('not support other cueId so far')


def callTopLogoInvokes(enId, args):
    topLogo.TopLogoManager.getInstance().callTopLogoInvokes(enId, args)
