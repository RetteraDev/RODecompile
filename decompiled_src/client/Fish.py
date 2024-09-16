#Embedded file name: I:/bag/tmp/tw2/res/entities\client/Fish.o
import BigWorld
import Math
import iBoids

class Fish(iBoids.IBoids):

    def __init__(self):
        super(Fish, self).__init__()
        self.fadeDistance = 100

    def getFilter(self):
        ft = BigWorld.FishFilter()
        ft.swimSpeed = self.speed
        ft.influenceRadius = self.outerradius
        ft.approachRadius = self.outerradius
        res = BigWorld.findWaterFromPoint(self.spaceID, self.position + Math.Vector3(0, 0.5, 0))
        if res != None:
            ft.waterHeight = res[0]
        return ft
