#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPlayerJingJie.o


class ImpPlayerJingJie(object):

    def getWSSlotsNumWithJingJie(self, slotNum):
        cnt = 0
        for sVal in self.wsSkills.itervalues():
            slotCnt = 0
            for slot in sVal.slots:
                if slot[1]:
                    slotCnt += 1

            if slotCnt >= slotNum:
                cnt += 1

        return cnt
