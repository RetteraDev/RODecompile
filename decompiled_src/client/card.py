#Embedded file name: I:/bag/tmp/tw2/res/entities\client/card.o
from commonCard import CommonCard

class Card(CommonCard):

    def __init__(self, cardId, actived = False, progress = 0, advanceLv = 0, slot = None):
        super(Card, self).__init__(cardId, actived, progress, advanceLv, slot)
