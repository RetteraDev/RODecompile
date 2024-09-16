#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impQuestion.o
import gamelog
import gameglobal

class ImpQuestion(object):

    def showQuestion(self, pushQuestionIdList):
        gamelog.debug('@zq question showQuestion', pushQuestionIdList)
        gameglobal.rds.ui.questionnaire.addQuestionMessage(pushQuestionIdList)

    def onFinishedQuestion(self, isSuccess):
        gamelog.debug('@zq question onFinishedQuestion', isSuccess)
        if isSuccess:
            gameglobal.rds.ui.questionnaire.removeQuestionMessage()
            gameglobal.rds.ui.questionnaire.hide()
            gameglobal.rds.ui.questionnaire.isFinished = False
