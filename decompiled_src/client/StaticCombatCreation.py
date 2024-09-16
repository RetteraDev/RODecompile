#Embedded file name: I:/bag/tmp/tw2/res/entities\client/StaticCombatCreation.o
from iCreation import ICreation
from data import creation_client_data as CCD

class StaticCombatCreation(ICreation):
    IsIsolatedCreation = False
    IsCombatCreation = True

    def __init__(self):
        self.data = CCD.data.get(self.cid, {})
        super(StaticCombatCreation, self).__init__()
