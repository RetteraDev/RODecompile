#Embedded file name: /WORKSPACE/data/entities/client/clanwarcourier.o
from Monster import Monster

class ClanWarCourier(Monster):
    IsCourierEnemy = False
    InClanCourier = True

    def __init__(self):
        super(ClanWarCourier, self).__init__()
