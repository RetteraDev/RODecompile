#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/impFootFashion.o
import BigWorld
import gamelog

class ImpFootFashion(object):

    def overrideFootprintCallback(self, callback, keepTime):
        self.footTriggerMgr.overrideCallback(callback, keepTime)

    def setupFootTrigger(self):
        owner = BigWorld.entity(self.owner)
        if self.footTriggerMgr:
            self.footTriggerMgr.setupFootTrigger(owner, self.modelID, owner.model)

    def detachFootTrigger(self):
        gamelog.debug('detachFootTrigger................')
        if self.footTriggerMgr:
            self.footTriggerMgr.release()
