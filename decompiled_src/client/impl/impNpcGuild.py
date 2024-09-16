#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impNpcGuild.o
import BigWorld
import gameglobal

class ImpNpcGuild(object):

    def getOpacityValueByRunMan(self, opacityVal):
        if opacityVal[0] == gameglobal.OPACITY_HIDE:
            return opacityVal
        visibility = opacityVal[0]
        p = BigWorld.player()
        if not p.runMan.isMarkerVisible(self.npcId):
            visibility = gameglobal.OPACITY_HIDE
        return (visibility, opacityVal[1])
