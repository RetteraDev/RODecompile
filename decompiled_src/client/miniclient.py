#Embedded file name: I:/bag/tmp/tw2/res/entities\client/miniclient.o
import gamelog
try:

    def disableReport():
        try:
            minifile.disableReport()
        except:
            pass


    def setCharLevel(lv):
        try:
            minifile.setCharLevel(lv)
            gamelog.debug('yck: setCharLevel ', lv)
        except:
            pass


    def avatarLeaveWorld():
        try:
            minifile.setCharLevel(0)
            minifile.setGbId(0)
            gamelog.debug('yck: avatarLeaveWorld')
        except:
            pass


    def avatarEnterWorld(gbId, lv):
        try:
            minifile.setGbId(gbId)
            minifile.setCharLevel(lv)
            gamelog.debug('yck: avatarEnterWorld')
        except:
            pass


    def flushAllReports():
        try:
            minifile.flushAllReports()
        except:
            pass


except:

    def disableReport():
        pass


    def setCharLevel(lv):
        pass


    def avatarLeaveWorld():
        pass


    def avatarEnterWorld(gbId, lv):
        pass


    def flushAllReports():
        pass
