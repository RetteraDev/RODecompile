#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/httpHelper.o
import BigWorld
import gamelog
import urllib2
import time
import hashlib
import httplib
import urllib

class HttpMessage(object):

    def __init__(self, method, params, header, body, bodyParams, address, port, url):
        self.method = method
        self.params = params
        self.header = header
        self.body = body
        self.bodyParams = bodyParams
        self.address = address
        self.port = port
        self.boundary = ''
        if self.params.has_key('md5'):
            self.params['md5'] = hashlib.md5(self.body).hexdigest()
        self.url = url + urllib.urlencode(self.params)
        self.messageHeader = ''
        self.bodyPrefix = ''
        self.endBoundary = ''
        self.contentLength = len(self.body)

    def genHeader1(self):
        ret = '%s %s HTTP/1.1\r\n' % (self.method, self.url)
        for key, value in self.header.iteritems():
            if value == 'multipart/form-data':
                self.boundary = '----------%s' % hex(int(time.time() * 1000))
                ret += '%s: %s; boundary=%s\r\n' % (key, value, self.boundary)
            else:
                ret += '%s: %s\r\n' % (key, value)

        if not self.header.has_key('Host'):
            ret += 'Host: %s:%s\r\n' % (self.address, self.port)
        if not self.header.has_key('Accept'):
            ret += 'Accept: */*\r\n'
        self.messageHeader = ret

    def genHeader2(self):
        if self.method == 'POST':
            self.messageHeader += 'Content-Length: %d\r\n\r\n' % self.contentLength
        else:
            self.messageHeader += '\r\n'

    def genBodyPrefix(self):
        if self.boundary:
            data = []
            data.append('--%s' % self.boundary)
            disposition = 'Content-Disposition: form-data'
            if self.bodyParams:
                dispositionDetail = '; '.join(("%s=\'%s\'" % (key, value) for key, value in self.bodyParams.iteritems()))
                disposition = '%s; %s' % (disposition, dispositionDetail)
            data.append(disposition)
            data.append('Content-Type: application/octet-stream\r\n\r\n')
            self.bodyPrefix = '\r\n'.join(data)
            self.endBoundary = '\r\n--%s--\r\n' % self.boundary
            self.contentLength = len(self.bodyPrefix) + len(self.body) + len(self.endBoundary)

    def build(self):
        self.genHeader1()
        self.genBodyPrefix()
        self.genHeader2()


def test():
    file = open('10.amr', 'rb')
    data = file.read()
    ins = HttpMessage('POST', {'md5': 0,
     'host': '1234',
     'tousers': '_1_',
     'usernum': '5678'}, {'User-Agent': 'pg',
     'Content-Type': 'multipart/form-data',
     'Connection': 'close'}, data, {'name': 'upload',
     'filename': '10.amr'}, 'voice.x.netease.com', 8020, '/pg/upload?')
    ins.build()
    BigWorld.httpUploadFile(ins.address, ins.port, ins.url, '../game/10.amr', callback, ins.messageHeader, ins.bodyPrefix, ins.endBoundary)


key = '0fd63a1238eca8dddf7f93d49629c6c2'
key1 = 'd7be285fa521b28f18c2e5ec88b10b93'

def testVoice():
    ins = HttpMessage('GET', {'key': key1}, {'User-Agent': 'pg',
     'Connection': 'close'}, '', {}, 'voice.x.netease.com', 8020, '/pg/get_translation?')
    ins.build()
    BigWorld.httpDownloadToMem(ins.address, ins.port, ins.url, callback, ins.messageHeader)


def testAmr():
    ins = HttpMessage('GET', {'key': key,
     'host': '1234',
     'usernum': '5678'}, {'User-Agent': 'pg',
     'Connection': 'close'}, '', {}, 'voice.x.netease.com', 8020, '/pg/getfile?')
    ins.build()
    BigWorld.httpDownloadToMem(ins.address, ins.port, ins.url, callback, ins.messageHeader)


ret = None

def callback(data):
    global ret
    gamelog.debug('callback', data)
    ret = data
