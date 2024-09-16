#Embedded file name: I:/bag/tmp/tw2/res/entities\client/Sheep.o
import random
import BigWorld
import iClientOnly

class Sheep(iClientOnly.IClientOnly):

    def __init__(self):
        super(Sheep, self).__init__()
        self.initFold()
        self.sheeps = []

    def initFold(self):
        halfWidth = self.sheepfoldWidth / 2.0
        self.sheepfoldAnchor = self.position - (halfWidth, 0, halfWidth)
        self.sheepfoldSlotWidth = int(self.sheepfoldWidth // self.sheepWidth)
        self.fold = list(xrange(self.sheepfoldSlotWidth * self.sheepfoldSlotWidth))

    def enterWorld(self):
        pass

    def leaveWorld(self):
        pass

    def createSheep(self, modelName, number):
        for index in xrange(number):
            slot = self.getFoldSlot()
            position = self.getSlotPosition(slot)
            scale = random.random() * (self.scaleMax - self.scaleMin) + self.scaleMin
            attrs = {'foldSlot': slot,
             'modelName': modelName,
             'scale': scale}
            sheep = BigWorld.createEntity('Sheepy', self.spaceID, 0, position, (0, 0, 0), {'attrs': attrs})
            self.sheeps.append(sheep)

    def getSlotPosition(self, slot):
        row = slot // self.sheepfoldSlotWidth
        col = slot % self.sheepfoldSlotWidth
        center = self.sheepfoldAnchor + (row * self.sheepWidth, 0, col * self.sheepWidth)
        offset = self.sheepWidth / 3.0
        return center + (random.random() * offset, 0, random.random() * offset)

    def getFoldSlot(self):
        slot = random.choice(self.fold)
        self.fold.remove(slot)
        return slot

    def destroySheep(self):
        for sheep in self.sheeps:
            BigWorld.destroyEntity(sheep)

    def boring(self):
        if not self.inWorld:
            return
        if not self.sheeps:
            return
        sheep = BigWorld.entity(random.choice(self.sheeps))
        if not sheep:
            return
        state = random.random()
        if state < 0.5:
            sheep.eatGrass()
        else:
            self.movePlace(sheep)
        BigWorld.callback(random.random() + 1.0, self.boring)

    def movePlace(self, sheep):
        foldSlot = self.getFoldSlot()
        self.fold.append(sheep.foldSlot)
        destination = self.getSlotPosition(foldSlot)
        sheep.foldSlot = foldSlot
        sheep.seekTo(destination, 1)

    def enterTopLogoRange(self, distance):
        self.sheeps = []
        self.createSheep(self.modelFile1, self.modelNumber1)
        self.createSheep(self.modelFile2, self.modelNumber2)
        self.boring()

    def leaveTopLogoRange(self, distance):
        self.destroySheep()
