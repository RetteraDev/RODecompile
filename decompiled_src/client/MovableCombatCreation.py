#Embedded file name: I:/bag/tmp/tw2/res/entities\client/MovableCombatCreation.o
from iCreation import ICreation
from data import creation_client_data as CCD

class MovableCombatCreation(ICreation):
    IsIsolatedCreation = False
    IsCombatCreation = True

    def __init__(self):
        self.data = CCD.data.get(self.cid, {})
        super(MovableCombatCreation, self).__init__()
