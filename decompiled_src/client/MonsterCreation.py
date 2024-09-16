#Embedded file name: I:/bag/tmp/tw2/res/entities\client/MonsterCreation.o
import BigWorld
import utils
import gameglobal
import gametypes
from helpers import action
from iCreation import ICreation
from data import creation_client_data as CCD

class MonsterCreation(ICreation):
    IsIsolatedCreation = False
    IsCombatCreation = False
    IsMonsterCreation = True
    IsCombatUnit = True

    def __init__(self):
        self.data = CCD.data.get(self.cid, {})
        super(MonsterCreation, self).__init__()
