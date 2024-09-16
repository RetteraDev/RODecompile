#Embedded file name: I:/bag/tmp/tw2/res/entities\common/commOfflineIncome.o


class OfflineIncomeVal(object):

    def __init__(self, dbID = 0, mtype = 0, bindType = 0, amount = 0, extra1Amount = 0, extra2Amount = 0, tWhen = 0, tExpire = 0, opcode = 0, detail = ''):
        self.dbID = dbID
        self.mtype = mtype
        self.bindType = bindType
        self.amount = amount
        self.extra1Amount = extra1Amount
        self.extra2Amount = extra2Amount
        self.tWhen = tWhen
        self.tExpire = tExpire
        self.opcode = opcode
        self.detail = detail

    def getDTO(self):
        return (self.dbID,
         self.mtype,
         self.bindType,
         self.amount,
         self.tWhen,
         self.tExpire,
         self.opcode,
         self.detail,
         self.extra1Amount,
         self.extra2Amount)

    def fromDTO(self, dto):
        self.dbID, self.mtype, self.bindType, self.amount, self.tExpire, self.tWhen, self.opcode, self.detail, self.extra1Amount, self.extra2Amount = dto
        return self
