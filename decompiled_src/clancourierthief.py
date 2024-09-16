#Embedded file name: /WORKSPACE/data/entities/client/clancourierthief.o
from Monster import Monster

class ClanCourierThief(Monster):
    IsCourierEnemy = True
    InClanCourier = True

    def __init__(self):
        super(ClanCourierThief, self).__init__()
