#Embedded file name: I:/bag/tmp/tw2/res/entities\common/commGuildTournament.o
from userSoleType import UserSoleType

class TournamentGuildVal(UserSoleType):

    def __init__(self, guildNUID = 0, guildName = '', deleted = False):
        self.guildNUID = guildNUID
        self.guildName = guildName
        self.deleted = deleted
