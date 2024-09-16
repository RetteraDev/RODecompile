#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\keyczar/keyczart.o
"""
Keyczart(ool) is a utility for creating and managing Keyczar keysets.

@author: arkajit.dey@gmail.com (Arkajit Dey)
"""
import os
import sys
import errors
import keyczar
import keydata
import keyinfo
import readers
import util
KEYSETS = [('aes',
  keyinfo.DECRYPT_AND_ENCRYPT,
  None,
  None),
 ('aes-crypted',
  keyinfo.DECRYPT_AND_ENCRYPT,
  None,
  'aes'),
 ('hmac',
  keyinfo.SIGN_AND_VERIFY,
  None,
  None),
 ('rsa',
  keyinfo.DECRYPT_AND_ENCRYPT,
  'rsa',
  None),
 ('rsa-sign',
  keyinfo.SIGN_AND_VERIFY,
  'rsa',
  None),
 ('dsa',
  keyinfo.SIGN_AND_VERIFY,
  'dsa',
  None)]
mock = None

class _Name(object):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Command(_Name):
    """Enum representing keyczart commands."""
    pass


CREATE = Command('create')
ADDKEY = Command('addkey')
PUBKEY = Command('pubkey')
PROMOTE = Command('promote')
DEMOTE = Command('demote')
REVOKE = Command('revoke')
GENKEY = Command('genkey')
commands = {'create': CREATE,
 'addkey': ADDKEY,
 'pubkey': PUBKEY,
 'promote': PROMOTE,
 'demote': DEMOTE,
 'revoke': REVOKE,
 'genkey': GENKEY}

def GetCommand(cmd):
    try:
        return commands[cmd]
    except KeyError:
        raise errors.KeyczarError('Illegal command')


class Flag(_Name):
    """Enum representing keyczart flags."""
    pass


LOCATION = Flag('location')
NAME = Flag('name')
SIZE = Flag('size')
STATUS = Flag('status')
PURPOSE = Flag('purpose')
DESTINATION = Flag('destination')
VERSION = Flag('version')
ASYMMETRIC = Flag('asymmetric')
CRYPTER = Flag('crypter')
flags = {'location': LOCATION,
 'name': NAME,
 'size': SIZE,
 'status': STATUS,
 'purpose': PURPOSE,
 'destination': DESTINATION,
 'version': VERSION,
 'asymmetric': ASYMMETRIC,
 'crypter': CRYPTER}

def GetFlag(flag):
    try:
        return flags[flag]
    except KeyError:
        raise errors.KeyczarError('Unknown flag')


def Create(loc, name, purpose, asymmetric = None):
    if mock is None and loc is None:
        raise errors.KeyczarError('Location missing')
    kmd = None
    if purpose == keyinfo.SIGN_AND_VERIFY:
        if asymmetric is None:
            kmd = keydata.KeyMetadata(name, purpose, keyinfo.HMAC_SHA1)
        elif asymmetric.lower() == 'rsa':
            kmd = keydata.KeyMetadata(name, purpose, keyinfo.RSA_PRIV)
        else:
            kmd = keydata.KeyMetadata(name, purpose, keyinfo.DSA_PRIV)
    elif purpose == keyinfo.DECRYPT_AND_ENCRYPT:
        if asymmetric is None:
            kmd = keydata.KeyMetadata(name, purpose, keyinfo.AES)
        else:
            kmd = keydata.KeyMetadata(name, purpose, keyinfo.RSA_PRIV)
    else:
        raise errors.KeyczarError('Missing or unsupported purpose')
    if mock is not None:
        mock.kmd = kmd
    else:
        fname = os.path.join(loc, 'meta')
        if os.path.exists(fname):
            raise errors.KeyczarError('File already exists')
        util.WriteFile(str(kmd), fname)


def AddKey(loc, status, crypter = None, size = None):
    czar = CreateGenericKeyczar(loc, crypter)
    if size == -1:
        size = None
    czar.AddVersion(status, size)
    UpdateGenericKeyczar(czar, loc, crypter)


def PubKey(loc, dest):
    if mock is None and dest is None:
        raise errors.KeyczarError('Must define destination')
    czar = CreateGenericKeyczar(loc)
    czar.PublicKeyExport(dest, mock)


def Promote(loc, num):
    czar = CreateGenericKeyczar(loc)
    if num < 0:
        raise errors.KeyczarError('Missing version')
    czar.Promote(num)
    UpdateGenericKeyczar(czar, loc)


def Demote(loc, num):
    czar = CreateGenericKeyczar(loc)
    if num < 0:
        raise errors.KeyczarError('Missing version')
    czar.Demote(num)
    UpdateGenericKeyczar(czar, loc)


def Revoke(loc, num):
    czar = CreateGenericKeyczar(loc)
    if num < 0:
        raise errors.KeyczarError('Missing version')
    czar.Revoke(num)
    UpdateGenericKeyczar(czar, loc)
    if mock is not None:
        mock.RemoveKey(num)
    else:
        os.remove(os.path.join(loc, str(num)))


def GenKeySet(loc):
    print 'Generating private key sets...'
    for name, purpose, asymmetric, crypter in KEYSETS:
        print '.'
        dir = os.path.join(loc, name)
        if crypter:
            crypter = keyczar.Crypter.Read(os.path.join(loc, crypter))
        Clean(dir)
        Create(dir, 'Test', purpose, asymmetric)
        AddKey(dir, keyinfo.PRIMARY, crypter)
        UseKey(purpose, dir, os.path.join(dir, '1.out'), crypter)
        AddKey(dir, keyinfo.PRIMARY, crypter)
        UseKey(purpose, dir, os.path.join(dir, '2.out'), crypter)

    print 'Exporting public key sets...'
    for name in ('dsa', 'rsa-sign'):
        print '.'
        dir = os.path.join(loc, name)
        dest = os.path.join(loc, name + '.public')
        PubKey(dir, dest)

    print 'Done!'


def Clean(directory):
    for file in os.listdir(directory):
        path = os.path.join(directory, file)
        if not os.path.isdir(path):
            os.remove(path)


def UseKey(purpose, loc, dest, crypter = None, msg = 'This is some test data'):
    reader = readers.FileReader(loc)
    answer = ''
    if crypter:
        reader = readers.EncryptedReader(reader, crypter)
    if purpose == keyinfo.DECRYPT_AND_ENCRYPT:
        answer = keyczar.Crypter(reader).Encrypt(msg)
    elif purpose == keyinfo.SIGN_AND_VERIFY:
        answer = keyczar.Signer(reader).Sign(msg)
    util.WriteFile(answer, dest)


def Usage():
    print 'Usage: \"Keyczart command flags\"\n  Commands: create addkey pubkey promote demote revoke\nFlags: location name size status purpose destination version asymmetric crypter\nCommand Usage:\ncreate --location=/path/to/keys --purpose=(crypt|sign) [--name=\"A name\"] [--asymmetric=(dsa|rsa)]\n  Creates a new, empty key set in the given location.\n  This key set must have a purpose of either \"crypt\" or \"sign\"\n  and may optionally be given a name. The optional asymmetric \n  flag will generate a public key set of the given algorithm.\n  The \"dsa\" asymmetric value is valid only for sets with \"sign\" purpose.\n  with the given purpose.\naddkey --location=/path/to/keys [--status=(active|primary)] [--size=size] [--crypter=crypterLocation]\n  Adds a new key to an existing key set. Optionally\n  specify a purpose, which is active by default. Optionally\n  specify a key size in bits. Also optionally specify the\n  location of a set of crypting keys, which will be used to\n  encrypt this key set.\npubkey --location=/path/to/keys --destination=/destination\n  Extracts public keys from a given key set and writes them\n  to the destination. The \"pubkey\" command Only works for\n  key sets that were created with the \"--asymmetric\" flag.\npromote --location=/path/to/keys --version=versionNumber\n  Promotes the status of the given key version in the given \n  location. Active keys are promoted to primary (which demotes \n  any existing primary key to active). Keys scheduled for \n  revocation are promoted to be active.\ndemote --location=/path/to/keys --version=versionNumber\n  Demotes the status of the given key version in the given\n  location. Primary keys are demoted to active. Active keys\n  are scheduled for revocation.\nrevoke --location=/path/to/keys --version=versionNumber\n  Revokes the key of the given version number.\n  This key must have been scheduled for revocation by the\n  promote command. WARNING: The key will be destroyed.\n\nOptional flags are in [brackets]. The notation (a|b|c) means \"a\", \"b\", and \"c\"\nare the valid choices'


def CreateGenericKeyczar(loc, crypter = None):
    if mock is not None:
        return keyczar.GenericKeyczar(mock)
    if loc is None:
        raise errors.KeyczarError('Need location')
    else:
        reader = readers.FileReader(loc)
        if crypter:
            reader = readers.EncryptedReader(reader, crypter)
        return keyczar.GenericKeyczar(reader)


def UpdateGenericKeyczar(czar, loc, encrypter = None):
    if mock is not None:
        mock.kmd = czar.metadata
        for v in czar.versions:
            mock.SetKey(v.version_number, czar.GetKey(v))

    else:
        czar.Write(loc, encrypter)


def main(argv):
    if len(argv) == 0:
        Usage()
    else:
        cmd = GetCommand(argv[0])
        flags = {}
        for arg in argv:
            if arg.startswith('--'):
                arg = arg[2:]
                try:
                    flag, val = arg.split('=')
                    flags[GetFlag(flag)] = val
                except ValueError:
                    print 'Flags incorrectly formatted'
                    Usage()

        try:
            version = int(flags.get(VERSION, -1))
            size = int(flags.get(SIZE, -1))
        except ValueError:
            print 'Size and version flags require an integer'
            Usage()

        loc = flags.get(LOCATION)
        if cmd == CREATE:
            purpose = {'crypt': keyinfo.DECRYPT_AND_ENCRYPT,
             'sign': keyinfo.SIGN_AND_VERIFY}.get(flags.get(PURPOSE))
            Create(loc, flags.get(NAME, 'Test'), purpose, flags.get(ASYMMETRIC))
        elif cmd == ADDKEY:
            status = keyinfo.GetStatus(flags.get(STATUS, 'ACTIVE').upper())
            if CRYPTER in flags:
                crypter = keyczar.Encrypter.Read(flags[CRYPTER])
            else:
                crypter = None
            AddKey(loc, status, crypter, size)
        elif cmd == PUBKEY:
            PubKey(loc, flags.get(DESTINATION))
        elif cmd == PROMOTE:
            Promote(loc, version)
        elif cmd == DEMOTE:
            Demote(loc, version)
        elif cmd == REVOKE:
            Revoke(loc, version)
        elif cmd == GENKEY:
            GenKeySet(loc)
        else:
            Usage()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
