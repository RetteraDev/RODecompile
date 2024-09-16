#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/exceptChannel.o
import sys
import socket
import traceback
import time
import BigWorld
import utils
import gamelog
import gametypes
import gameglobal
import subprocess
import gameconfigCommon
import ui
g_offline_exception = []
from data import region_server_config_data as RSCD

class ExceptChannel(object):
    EIGEN_DUMB = '<string>'

    def __init__(self, bFile, bChannel):
        sys.excepthook = self.__excepthook__
        self.bFile = bFile
        self.bChannel = bChannel
        self.article = {}
        self.is_enable_EIGEN_DUMB = True

    def clear(self):
        self.article = {}

    def uploadTB(self, content):
        cmdList = []
        cmdList.append('cport.exe')
        content = ''.join(content)
        cmdList.append('\"\"%s\"\"' % content)
        cmdList.append(RSCD.data.get(utils.getHostId(), {}).get('serverName', 'serverName'))
        p = BigWorld.player()
        if p:
            cmdList.append(getattr(p, 'roleName', 'roleName'))
            cmdList.append(str(getattr(p, 'gbId', 0)))
        else:
            cmdList.append('no Player')
            cmdList.append('no GBId')
        cmdList.append(str(utils.getHostId()))
        cmdList.append('-isPostTB')
        subprocess.Popen(cmdList)

    def reportExcept(self, digest, paragraph):
        global g_offline_exception
        gamelog.error('jorsef: reportExcept', digest, paragraph)
        p = BigWorld.player()
        if not p and g_offline_exception != None:
            for sentence in paragraph:
                g_offline_exception.append(sentence)

            return
        else:
            if BigWorld.isPublishedVersion():
                if g_offline_exception != None and len(g_offline_exception) > 0:
                    paragraph = g_offline_exception + paragraph
                    g_offline_exception = None
            if type(paragraph) in (tuple, list):
                p = BigWorld.player()
                user = p.realRoleName if p and hasattr(p, 'roleName') else ''
                localIP = socket.gethostbyname(socket.gethostname())
                if p and utils.instanceof(p, 'PlayerAvatar'):
                    p.reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_SCRIPT, list(paragraph), 0, {'digest': digest,
                     'clientUser': user,
                     'clientIP': localIP})
            gamelog.debug('jorsef: start writing to file', paragraph)
            if self.bFile:
                fileEX = open('../game/exception.log', 'a+')
                for sentence in paragraph:
                    fileEX.write('%s	%s' % (time.ctime(), sentence))
                    fileEX.flush()

                fileEX.close()
            return

    def traceError(self):
        p = BigWorld.player()
        p and p.base.chatToTrace('---------- BEGIN:%s ----------' % (p.realRoleName,))
        for digest, part in self.article.iteritems():
            for ex in part:
                p and p.base.chatToTrace(ex)

        p and p.base.chatToTrace('---------- END:%s ----------' % (p.realRoleName,))

    def enable_EIGEN_DUMB(self):
        self.is_enable_EIGEN_DUMB = True

    def __excepthook__(self, ty, val, tb):
        localVars = None
        if gameglobal.rds.configData.get('enableClientLogPrintLoacalVars', False) or not BigWorld.isPublishedVersion():
            try:
                tag = tb.tb_frame.f_locals.get('__name__')
                if tag and tag == '__main__':
                    gamelog.error('~~~~~~~ TELNET Exception ~~~~~~')
                else:
                    gamelog.error('~~~~~~~ SCRIPT Exception ~~~~~~')
                tbNext = tb
                while tbNext.tb_next:
                    tbNext = tbNext.tb_next

                if tbNext.tb_frame.f_locals:
                    varDict = {}
                    for k, v in tbNext.tb_frame.f_locals.iteritems():
                        if v.__class__.__name__ == 'ASObject':
                            continue
                        sv = str(v)
                        if len(sv) > 100:
                            varDict[k] = sv[:100] + '...(more)'
                        else:
                            varDict[k] = sv

                    varMsg = str(varDict)
                    if len(varMsg) > 1000:
                        varMsg = varMsg[:1000] + '...(more)'
                    localVars = 'Locals (only top stack frame):%s' % varMsg
            except:
                gamelog.error('~~~~~~~ UNKNOW Exception ~~~~~~')

            if localVars:
                gamelog.error(localVars)
        sys.__excepthook__(ty, val, tb)
        gamelog.error('jorsef: begin __excepthook__: ')
        paragraph = traceback.format_exception(ty, val, tb)
        content = ''
        for idx, sentence in enumerate(paragraph[:-1]):
            if self.is_enable_EIGEN_DUMB and idx < 2:
                if sentence.find(self.EIGEN_DUMB) != -1:
                    return
            content += sentence

        gamelog.debug('jorsef: content: ', content)
        digest = utils.calcExceptionDigest(content)
        if self.article.has_key(digest):
            gamelog.debug('jorsef: article has digest, return')
            return
        else:
            self.article[digest] = paragraph
            if not gameconfigCommon.enableUploadTBToAppdump():
                self.reportExcept(digest, paragraph)
            else:
                gamelog.error('jorsef: reportExcept', digest, paragraph)
                self.uploadTB(paragraph)
            return
