#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impSimpleQte.o
import gamelog
import gameglobal
from data import simple_qte_data as SQD

class ImpSimpleQte(object):

    def startChickenQte(self):
        gamelog.debug('@zq impSimpleQte/startChickenQte')
        gameglobal.rds.ui.chickenFoodEating.show()

    def endChickenQte(self, chickenQteResult):
        gamelog.debug('@zq impSimpleQte/endChickenQte ', chickenQteResult)
        gameglobal.rds.ui.chickenFoodEating.onEnd(chickenQteResult)

    def syncChickenQteClickCount(self, chickenQteInfo):
        gamelog.debug('@zq impSimpleQte/syncChickenQteClickCount ', chickenQteInfo)
        gameglobal.rds.ui.chickenFoodEating.onSyncChickenQteClickCount(chickenQteInfo)
