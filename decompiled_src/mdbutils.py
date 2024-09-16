#Embedded file name: /WORKSPACE/data/entities/common/mdbutils.o
import BigWorld
import os
import hashlib
import gamelog
from utils import newMDB
MDBVersionMatch = None
MDBInited = False

def dataCacheInitErrorCB():
    from helpers import newMDBConverter
    path = newMDBConverter.BINARY_ENCRYPT_NAME
    try:
        os.remove(path)
    except:
        pass


def checkVersion():
    from helpers import newMDBConverter
    filePath = newMDBConverter.BINARY_ENCRYPT_NAME
    from data import datarevision
    if os.path.exists(filePath):
        fileSize = os.path.getsize(filePath)
        with open(filePath, 'rb') as f:
            FileVersion = newMDBConverter.MDBConverter.getNewMDBVersion(f, fileSize)
            dataVersion = int(datarevision.REVISION) % newMDBConverter.MAX_INT
            gamelog.debug('m.l@MDBUtils.checkVersion', FileVersion, fileSize, dataVersion)
            if FileVersion == dataVersion:
                MDBVersionMatch = FileVersion
                return MDBVersionMatch


def clearCacheFile():
    from helpers import newMDBConverter
    try:
        import os
        os.remove(newMDBConverter.BINARY_ENCRYPT_NAME)
        os.remove(newMDBConverter.MD5_FILE_NAME)
    except Exception as e:
        import gamelog
        gamelog.debug('m.l@.clearCacheFile error', e.message)


def clearMD5Text():
    from helpers import newMDBConverter
    try:
        import os
        os.remove(newMDBConverter.MD5_FILE_NAME)
    except Exception as e:
        import gamelog
        gamelog.debug('m.l@.clearMD5Text error', e.message)


def initNewMDB(disableConvert = False):
    global newMDB
    global MDBInited
    if not MDBInited:
        import NewMemoryDB
        from data import datarevision
        from helpers import newMDBConverter
        version = datarevision.REVISION % newMDBConverter.MAX_INT
        gamelog.debug('m.l@MDBUtils.initNewMDB', newMDBConverter.BINARY_ENCRYPT_NAME, datarevision.REVISION, version)
        newMDB = NewMemoryDB.initMDB(newMDBConverter.BINARY_ENCRYPT_NAME, datarevision.REVISION % newMDBConverter.MAX_INT)
        MDBInited = True


if BigWorld.component == 'client' and newMDB:
    import NewMemoryDB
    NewMemoryDB.setInitErrorCallback(dataCacheInitErrorCB)
    MDBVersionMatch = checkVersion()
    gamelog.debug('m.l@.MDBUtils', MDBVersionMatch)
    if not MDBVersionMatch:
        newMDB = False
    else:
        initNewMDB()

def convertToMDB(data, name = '', module = None):
    if BigWorld.component == 'client' and newMDB:
        from helpers import newMDBConverter
        import cacheMDB
        keyType = module.keyType
        attrs = module.attrs
        valueAttrs = module.valueAttrs
        needWriteFile = False
        data = cacheMDB.convert_to_new_mdb_dict(data, keyType, name, attrs, valueAttrs, needWriteFile)
        module.attrs = None
        module.valueAttrs = None
        gamelog.debug('m.l@MDBUtils.convertToMDB over', name, keyType, MDBVersionMatch)
    return data
