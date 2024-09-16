#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/strmap.o
import cPickle
import zlib
ENCRYPT_PREFIX = 'avatarmorpher@'
ENCRYPT_PREFIX_HEX = ENCRYPT_PREFIX.encode('hex')

def genStrmapKey():
    from uuControl import genAuthCodeKey
    key = 'avatarmorpher_encrpyt'
    return genAuthCodeKey(key)


def isEncrypted(content):
    l = len(ENCRYPT_PREFIX_HEX)
    if content and len(content) > l and content[0:l] == ENCRYPT_PREFIX_HEX:
        return True
    return False


def encryptContent(content):
    from Crypto.Cipher import AES
    from uuControl import strPad
    key = genStrmapKey()
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = cipher.encrypt(strPad(content))
    return (ENCRYPT_PREFIX + encrypted).encode('hex')


def decryptContent(content):
    l = len(ENCRYPT_PREFIX_HEX)
    if content and len(content) > l and content[0:l] == ENCRYPT_PREFIX_HEX:
        from Crypto.Cipher import AES
        from uuControl import strUnpad
        content = content.decode('hex')
        content = content[len(ENCRYPT_PREFIX):]
        key = genStrmapKey()
        cipher = AES.new(key, AES.MODE_ECB)
        try:
            content = cipher.decrypt(content)
            content = strUnpad(content)
        except:
            pass

    return content


class strmap(object):

    def __init__(self, content):
        content = decryptContent(content)
        try:
            content = zlib.decompress(content)
        except:
            pass

        try:
            self.map = cPickle.loads(content)
        except Exception:
            self.map = dict()

        if not type(self.map) == dict:
            self.map = dict()
        self.checkSkin()

    def set(self, k, v):
        self.map[k] = v

    def get(self, k, default = None):
        if k not in self.map:
            return default
        return self.map[k]

    def __str__(self):
        return cPickle.dumps(self.map)

    def checkSkin(self):
        skinDyes = self.map.get('skinDyes', None)
        headDyes = self.map.get('headDyes', None)
        indexList = []
        for strDyes in (skinDyes, headDyes):
            if strDyes:
                sIdx = strDyes.find('201:')
                if sIdx != -1:
                    eIdx = strDyes[sIdx:].find('\n')
                    if eIdx == -1:
                        eIdx = len(strDyes)
                    else:
                        eIdx = sIdx + eIdx
                indexList.append((sIdx, eIdx))

        if len(indexList) == 2 and headDyes[indexList[1][0]:indexList[1][1]] != skinDyes[indexList[0][0]:indexList[0][1]]:
            headDyes = headDyes.replace(headDyes[indexList[1][0]:indexList[1][1]], skinDyes[indexList[0][0]:indexList[0][1]])
            self.map['headDyes'] = headDyes
