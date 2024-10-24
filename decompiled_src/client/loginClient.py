#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client/loginClient.o
from gamestrings import gameStrings
import sys
import cPickle
import random
import uuid
import base64
import gameglobal
import gamelog
import utils
from gt import gtService
from proto import login_pb2
import Crypto.Util
Crypto.Util.strxor = sys.modules['strxor']
Crypto.Util._counter = sys.modules['_counter']
import clientUtils
pub_crypt = cPickle.loads("�ckeyczar.keyczar\nEncrypter\nq)�q}q(Uprimary_versionqckeyczar.keydata\nKeyVersion\nq)�q}q(Uversion_numberqKU_KeyVersion__statusq	ckeyczar.keyinfo\nKeyStatus\nq\n)�q}q(Unameq\rUPRIMARYqUidqK ubU\nexportableq�ubUdefault_sizeqM U_keysq}q(hckeyczar.keys\nRsaPublicKey\nq)�q}q(Uparamsq}q(UpublicExponentqU  qUmodulusqU� �E;�EYB�S`x\rtGA51��ZQ,�@��S��7�/���l�\r>��*�\'�a����@4Ϸ����,NeuE�\r��re����Ƹ�h7�0{Ⱦ�e`���6vƝ���<����sPc�Ť�XY��BTwEquU\n_Key__sizeqM Utypeqckeyczar.keyinfo\nKeyType\nq)�q }q!(hM U_KeyType__sizesq\"]q#(M M M M M eh\rURSA_PUBq$Uoutput_sizeq%M hKubUkeyq&(cCrypto.PublicKey.RSA\n_RSAobj\nq\'oq(}q)(Ue� Un��EwTḄYX��ŹcPs����<��ޝ�v6���`eԾ�{0�7h����ђ�er��\r�EueN,�����4@���a�\'�*��>\r�l���/�7����S��@�,QZ��15AGt\rx`S�BYE�;E� ubU_paramsq*hubU8o7K5wq+huUmetadataq,ckeyczar.keydata\nKeyMetadata\nq-)�q.}q/(U	encryptedq0�U_KeyMetadata__versionsq1}q2Khshh h\rUloginq3Upurposeq4ckeyczar.keyinfo\nKeyPurpose\nq5)�q6}q7(h\rUENCRYPTq8hKububub.")

def getRandomStr():
    return '%06d' % int(random.random() * 1000000)


class loginClient(login_pb2.LoginClient):
    ST_INIT = 0
    ST_CONNECTING = 1
    ST_FETCH_CONNECTION_SESSION = 2
    ST_CAN_LOGON = 3
    ST_PASSWD_SEND = 4
    ST_NEED_EKEY = 5
    ST_EKEY_SEND = 6
    ST_NEED_MIMAKA = 7
    ST_MIMAKA_SEND = 8
    ST_FEIHUO_COOKIE_SEND = 9
    ST_LOGINED = 10
    ST_QUERYUSER = 11
    ST_CHOSE_SERVER = 12
    ST_LOGIN_PRE = 13
    ST_EKEY_ERR = 14
    ST_MIMAKA_ERR = 15
    ST_MIMAKA_ERR_LIMIT = 16
    ST_QUERY_QRCODE = 17
    ST_YIYOU_TOKEN_SEND = 18
    ST_REAL_NAME_PASS = 19
    ST_REAL_NAME_WAIT = 20
    ST_REAL_NAME_NO = 21
    ST_REAL_NAME_FAIL = 22
    ST_REAL_NAME_FINISH = 23
    LogonRequest = login_pb2.LogonRequest()
    EkeyRequest = login_pb2.EkeyRequest()
    MimakaRequest = login_pb2.MimakaRequest()
    QueryRequest = login_pb2.QueryRequest()
    QueryRequest2 = login_pb2.QueryRequest()
    FetchKeyRequest = login_pb2.FetchKeyRequest()
    QRCodeRequest = login_pb2.QRCodeRequest()
    FeihuoLogonRequest = login_pb2.FeihuoLogonRequest()
    TokenLogonRequest = login_pb2.TokenLogonRequest()
    YiyouLogonRequest = login_pb2.YiyouLogonRequest()
    FinishRealNameRequest = login_pb2.FinishRealNameRequest()

    def __init__(self):
        super(loginClient, self).__init__()
        self.status = loginClient.ST_INIT
        self.channel = gtService.gtRpcChannel(self)
        self.service_stub = login_pb2.LoginService_Stub(self.channel)
        self.ppc = ''
        self.connectionSession = ''
        self.reporter = None
        self.serversInfo = None
        self.loginInfo = None
        self.randStr = ''

    def set_reporter(self, reporter):
        self.reporter = reporter

    def on_connected(self):
        gamelog.debug('b.e.: loginClient.on_connected')
        self.status = loginClient.ST_FETCH_CONNECTION_SESSION
        message = loginClient.FetchKeyRequest
        message.Clear()
        self.randStr = getRandomStr()
        message.rkey = pub_crypt.Encrypt(self.randStr)
        self.service_stub.FetchKey(None, message)

    def on_disconnected(self):
        gamelog.debug('b.e.: loginClient.on_disconnected')
        self.status = loginClient.ST_INIT
        gameglobal.rds.loginManager.onGtDisconnect()

    def get_status(self):
        return self.status

    def get_ppccoord(self):
        return self.ppc

    def connect(self, address):
        if self.status != loginClient.ST_INIT:
            raise RuntimeError('connect in wrong status %d' % (self.status,))
        self.status = loginClient.ST_CONNECTING
        self.channel.connect(address)
        self.channel.set_buffer(4096)

    def disconnect(self):
        self.channel.disconnect()
        self.status = loginClient.ST_INIT

    def OnFetchKey(self, controller, reply, done):
        gamelog.debug('b.e.: loginClient.QueryReply', reply.skey)
        if self.status != loginClient.ST_FETCH_CONNECTION_SESSION:
            raise RuntimeError('fetch conneciton session in wrong status')
        if self.randStr != reply.rkey:
            self.disconnect()
            return
        self.connectionSession = reply.skey
        self.status = loginClient.ST_CAN_LOGON

    def logon(self, username, password, cdkey, randkey):
        gamelog.debug('b.e.: loginClient.logon', username, password, cdkey, randkey)
        if self.status != loginClient.ST_CAN_LOGON:
            raise RuntimeError('logon in wrong status')
        message = loginClient.LogonRequest
        message.Clear()
        message.username = utils.normaliseAccountName(username)
        message.password = pub_crypt.Encrypt(self.connectionSession + password)
        message.cdkey = cdkey
        message.randkey = randkey
        self.service_stub.Logon(None, message)
        self.status = loginClient.ST_PASSWD_SEND

    def feiHuoLogin(self, webName, cookie, cdkey, randkey):
        gamelog.info('@szh: feiHuoLogin', webName, cookie, cdkey, randkey)
        if self.status != loginClient.ST_CAN_LOGON:
            raise RuntimeError('logon in wrong status', self.status)
        message = loginClient.FeihuoLogonRequest
        message.Clear()
        message.username = webName
        message.cookie = cookie
        message.cdkey = cdkey
        message.randkey = randkey
        self.service_stub.FeihuoLogon(None, message)
        self.status = loginClient.ST_FEIHUO_COOKIE_SEND

    def yiyouLogin(self, uid, token):
        gamelog.info('@cf: yiyouLogin', token)
        if self.status != loginClient.ST_CAN_LOGON:
            raise RuntimeError('logon in wrong status', self.status)
        message = loginClient.YiyouLogonRequest
        message.Clear()
        message.uid = uid
        message.token = token
        self.service_stub.YiyouLogon(None, message)
        self.status = loginClient.ST_YIYOU_TOKEN_SEND

    def logonByMRToken(self, username, password, cdkey, randkey):
        gamelog.debug('zt: loginClient.logonByMRToken', username, password, cdkey, randkey, self.status)
        if self.status != loginClient.ST_CAN_LOGON:
            raise RuntimeError('logon in wrong status')
        message = loginClient.TokenLogonRequest
        message.Clear()
        message.uid = utils.normaliseAccountName(username)
        message.token = self.connectionSession + password
        self.service_stub.LogonByMRToken(None, message)
        self.status = loginClient.ST_PASSWD_SEND

    def logonByEUToken(self, username, password, cdkey, randkey):
        gamelog.debug('zt: loginClient.logonByEUToken', username, password, cdkey, randkey, self.status)
        if self.status != loginClient.ST_CAN_LOGON:
            raise RuntimeError('logon in wrong status')
        message = loginClient.TokenLogonRequest
        message.Clear()
        message.uid = utils.normaliseAccountName(username)
        message.token = self.connectionSession + password
        self.service_stub.LogonByEUToken(None, message)
        self.status = loginClient.ST_PASSWD_SEND

    def checkInitState(self):
        if self.status == loginClient.ST_INIT:
            if self.reporter:
                if hasattr(self.reporter, 'firstPage'):
                    self.reporter.firstPage()
            return True
        return False

    def client_cancel_ekey_mimaka(self):
        if self.checkInitState():
            return
        if self.status == loginClient.ST_NEED_EKEY:
            self.client_cancel_ekey()
        elif self.status == loginClient.ST_NEED_MIMAKA:
            self.client_cancel_mimaka()
        else:
            raise RuntimeError('client_cancel_ekey_mimaka in wrong status')

    def client_cancel_ekey(self):
        if self.checkInitState():
            return
        gamelog.debug('b.e.: client_cancel_ekey')
        if self.status != loginClient.ST_NEED_EKEY:
            raise RuntimeError('client_cancel_ekey in wrong status')
        self.status = loginClient.ST_CAN_LOGON

    def ekey(self, ekey):
        gamelog.info('@szh: loginClient.ekey', ekey)
        if self.checkInitState():
            return
        else:
            if self.status != loginClient.ST_NEED_EKEY:
                raise RuntimeError('ekey in wrong status')
            message = loginClient.EkeyRequest
            message.Clear()
            message.key = pub_crypt.Encrypt(self.connectionSession + ekey)
            self.service_stub.Ekey(None, message)
            self.status = loginClient.ST_EKEY_SEND
            return

    def client_cancel_mimaka(self):
        if self.checkInitState():
            return
        gamelog.debug('b.e.: client_cancel_mimaka')
        if self.status != loginClient.ST_NEED_MIMAKA:
            raise RuntimeError('client_cancel_mimaka in wrong status')
        self.status = loginClient.ST_CAN_LOGON

    def mimaka(self, key):
        gamelog.info('@szh: loginClient.mimaka', key)
        if self.checkInitState():
            return
        else:
            if self.status != loginClient.ST_NEED_MIMAKA:
                raise RuntimeError('mimaka in wrong status')
            message = loginClient.MimakaRequest
            message.Clear()
            message.key = pub_crypt.Encrypt(self.connectionSession + key)
            self.service_stub.Mimaka(None, message)
            self.status = loginClient.ST_MIMAKA_SEND
            return

    def finishRealNameReq(self):
        if self.checkInitState():
            return
        else:
            message = loginClient.FinishRealNameRequest
            message.Clear()
            self.service_stub.FinishRealName(None, message)
            self.status = loginClient.ST_REAL_NAME_FINISH
            return

    def Reply(self, controller, reply, done):
        gamelog.debug('b.e.: loginClient.Reply', repr(controller), repr(reply), repr(done))
        gamelog.debug('b.e.: loginClient.Reply', reply.type, reply.message)
        if reply.type in (login_pb2.LogonReply.LOGINED, login_pb2.LogonReply.FEIHUO_LOGINED):
            if reply.urs:
                self.reporter.userNameSaved = reply.urs if gameglobal.rds.loginAuthType else utils.unnormaliseAccountName(reply.urs)
                self.reporter.reCheckKey = reply.recheckkey
            self.status = loginClient.ST_LOGINED
        elif reply.type == login_pb2.LogonReply.PASSWORD_ERR:
            self.status = loginClient.ST_CAN_LOGON
            if self.reporter:
                if reply.message == gameStrings.TEXT_LOGINCLIENT_296:
                    if gameglobal.rds.ui.loginWin.isQRCodeShow:
                        self.reporter.onClientReply(prevPage=True, popomsg='')
                        gameglobal.rds.ui.messageBox.showMsgBox(reply.message, gameglobal.rds.ui.loginWin.tryQuery)
                elif reply.message == gameStrings.TEXT_LOGINCLIENT_300:
                    self.reporter.onClientReply(prevPage=True, popomsg='')
                    from data import sys_config_data as SCD
                    warnMsg = SCD.data.get('ursLoginWarning', gameStrings.TEXT_ACCOUNT_496)
                    warnMsg = warnMsg % ('ty', 'apijg', self.reporter.userNameSaved)
                    gameglobal.rds.ui.messageBox.showMsgBox(warnMsg)
                else:
                    self.reporter.onClientReply(prevPage=True, popomsg=reply.message)
        elif reply.type == login_pb2.LogonReply.NEED_EKEY:
            self.status = loginClient.ST_NEED_EKEY
        elif reply.type == login_pb2.LogonReply.EKEY_ERR:
            self.status = loginClient.ST_EKEY_ERR
        elif reply.type == login_pb2.LogonReply.REAL_NAME_PASS:
            self.status = loginClient.ST_REAL_NAME_PASS
        elif reply.type == login_pb2.LogonReply.REAL_NAME_WAIT:
            self.status = loginClient.ST_REAL_NAME_WAIT
        elif reply.type == login_pb2.LogonReply.REAL_NAME_NO:
            self.status = loginClient.ST_REAL_NAME_NO
        elif reply.type in (login_pb2.LogonReply.REAL_NAME_FAIL, login_pb2.LogonReply.PLATFORM_REAL_NAME_FAIL):
            self.status = loginClient.ST_REAL_NAME_FAIL
        elif reply.type == login_pb2.LogonReply.NEED_MIMAKA:
            self.status = loginClient.ST_NEED_MIMAKA
            self.ppc = reply.message
        elif reply.type == login_pb2.LogonReply.MIMAKA_ERR:
            if reply.message.startswith('412&'):
                self.status = loginClient.ST_MIMAKA_ERR_LIMIT
            else:
                self.status = loginClient.ST_MIMAKA_ERR
            if reply.message.startswith('494&'):
                self.ppc = reply.message[4:]
        elif reply.type == login_pb2.LogonReply.MOBILE_MIMA_WARNING:
            self.status = loginClient.ST_CAN_LOGON
            if self.reporter:
                self.reporter.onClientReply(prevPage=True, popomsg=reply.message)
        elif reply.type == login_pb2.LogonReply.LOGIN_RESPONSE_HACK:
            self.status = loginClient.ST_CAN_LOGON
            if self.reporter:
                if reply.message:
                    responseMsg = reply.message
                else:
                    responseMsg = gameStrings.TEXT_LOGINCLIENT_344
                self.reporter.onClientReply(prevPage=True, popomsg=responseMsg)
        elif reply.type == login_pb2.LogonReply.FEIHUO_LOGINED:
            if reply.urs:
                self.reporter.userNameSaved = reply.urs
            self.status = loginClient.ST_LOGINED
        elif reply.type == login_pb2.LogonReply.COOKIE_ERR:
            self.status = loginClient.ST_CAN_LOGON
        elif reply.type == login_pb2.LogonReply.COOKIE_TIMEOUT:
            self.status = loginClient.ST_CAN_LOGON
            self.reporter.onClientReply(prevPage=True, popomsg=gameStrings.TEXT_LOGINCLIENT_356)
        elif reply.type == login_pb2.LogonReply.YIYOU_LOGINED:
            if reply.urs:
                self.reporter.userNameSaved = reply.urs
            self.status = loginClient.ST_LOGINED
        elif reply.type == login_pb2.LogonReply.YIYOU_ERR:
            self.status = loginClient.ST_CAN_LOGON

    def query(self, account):
        if self.checkInitState():
            return
        else:
            gamelog.debug('b.e.: loginClient.query', account)
            if self.status != loginClient.ST_LOGINED:
                raise RuntimeError('query in wrong status')
            request = loginClient.QueryRequest
            request.Clear()
            request.username = account
            self.service_stub.QueryUser(None, request)
            return

    def QueryReply(self, controller, reply, done):
        gamelog.debug('b.e.: loginClient.QueryReply1', uuid.UUID(bytes=reply.uuid).hex)
        gamelog.debug('b.e.: loginClient.QueryReply2', uuid.UUID(bytes=reply.server_uuid).hex)
        for treply in reply.reply:
            gamelog.debug('b.e.: loginClient.QueryReply', treply.server, treply.usernum)

        self.serversInfo = reply
        self.status = loginClient.ST_CHOSE_SERVER

    def getServers(self):
        return getattr(self.serversInfo, 'reply', None)

    def getServiceUUID(self):
        return getattr(self.serversInfo, 'uuid', '')

    def getServerUUID(self):
        return getattr(self.serversInfo, 'server_uuid', '')

    def LogonKeyToClient(self, controller, reply, done):
        gamelog.debug('b.e.: loginClient.LogonKeyToClient', repr(controller), repr(reply), repr(done))
        self.status = loginClient.ST_LOGIN_PRE
        self.loginInfo = reply

    def getLoginInfo(self):
        return self.loginInfo

    def queryuser(self, username):
        if self.checkInitState():
            return
        else:
            gamelog.debug('b.e.: loginClient.queryuser', username, self.status)
            if self.status < loginClient.ST_LOGINED:
                raise RuntimeError('queryuser in wrong status')
            message = loginClient.QueryRequest2
            message.Clear()
            message.username = utils.normaliseAccountName(username)
            self.service_stub.QueryUser(None, message)
            self.status = loginClient.ST_QUERYUSER
            return

    def getQRCode(self):
        if self.checkInitState():
            return
        else:
            if self.status != loginClient.ST_CAN_LOGON:
                raise RuntimeError('logon in wrong status')
            self.status = loginClient.ST_QUERY_QRCODE
            message = login_pb2.QRCodeRequest()
            message.randkey = gameglobal.rds.logOnAttemptKey
            self.service_stub.QRCode(None, message)
            print '[loginClient] query_qrcode'
            return

    def OnQRCode(self, controller, reply, done):
        if self.reporter:
            self.reporter.onQRCode(reply.qrcode)

    def cancelQRCode(self):
        self.service_stub.QRCodeCancel()
