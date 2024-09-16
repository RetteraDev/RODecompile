#Embedded file name: I:/bag/tmp/tw2/res/entities\client/ClanWarAirDefender.o
from Monster import Monster
from iClanWarCreation import IClanWarCreation

class ClanWarAirDefender(Monster, IClanWarCreation):
    IsMonster = False
    IsClanWarUnit = True

    def __init__(self):
        super(ClanWarAirDefender, self).__init__()
        self.applyTints = []

    def canOutline(self):
        return False

    def needAttachUFO(self):
        return False
