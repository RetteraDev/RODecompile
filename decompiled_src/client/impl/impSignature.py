#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impSignature.o
import gamelog

class ImpSignature(object):

    def initSignature(self, personalSignatureList):
        gamelog.debug('@hjx ps#initSignature:', personalSignatureList)
        self.personalSignatureList = personalSignatureList

    def onQuerySignatureCntInfo(self, signatureCntInfo):
        gamelog.debug('@hjx ps#onQuerySignatureCnt:', signatureCntInfo)

    def onSearchSameSignatureInfo(self, info):
        gamelog.debug('@hjx ps#onSearchSameSignatureInfo:', info)

    def onQuerySignatureMemberDetail(self, info):
        gamelog.debug('@hjx ps#onQuerySignatureMemberDetail:', info)
