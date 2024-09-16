#Embedded file name: /WORKSPACE/data/entities/client/clancourierguard.o
from Monster import Monster

class ClanCourierGuard(Monster):
    IsCourierEnemy = False
    InClanCourier = True

    def __init__(self):
        super(ClanCourierGuard, self).__init__()
