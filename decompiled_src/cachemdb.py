#Embedded file name: /WORKSPACE/data/entities/common/cachemdb.o
import gamelog
from utils import newMDB
try:
    if newMDB:
        import NewMemoryDB as MemoryDB
    else:
        import MemoryDB
except:
    pass

CACHE_SIZE = 200
KEY_TYPE_INT = 1
KEY_TYPE_TUPLE_INT = 2
KEY_TYPE_OTHER = 3
CACHE_SIZE_MAP = {'data_skill_general_data': 500,
 'data_skill_client_data': 500,
 'data_state_client_data': 600,
 'data_state_data': 600}

class DataCache(object):

    def __init__(self, moduleName, cacheSize = None):
        self.moduleName = moduleName
        self.cacheSize = cacheSize if cacheSize else CACHE_SIZE
        customSize = CACHE_SIZE_MAP.get(moduleName, 0)
        if customSize > 0:
            self.cacheSize = customSize
        self.root = [None,
         None,
         None,
         None]
        self.root[0] = self.root[1] = self.root
        self.mapping = {}
        self.hitCount = 0
        self.missCount = 0

    def addCache(self, key, value):
        self.missCount = self.missCount + 1
        mapping = self.mapping
        root = self.root
        if len(mapping) >= self.cacheSize:
            oldest = root[1]
            next_oldest = oldest[1]
            root[1] = next_oldest
            next_oldest[0] = root
            if mapping.has_key(oldest[2]):
                del mapping[oldest[2]]
        last = root[0]
        last[1] = root[0] = mapping[key] = [last,
         root,
         key,
         value]

    def hasCache(self, key):
        return self.mapping.has_key(key)

    def getCache(self, key):
        mapping = self.mapping
        root = self.root
        link = mapping.get(key)
        if link is not None:
            link_prev, link_next, link_key, value = link
            link_prev[1] = link_next
            link_next[0] = link_prev
            last = root[0]
            last[1] = root[0] = link
            link[0] = last
            link[1] = root
            if value is not None:
                return value
        return {}

    def removeCache(self, key):
        if self.hasCache(key):
            del self.mapping[key]

    def getHitRate(self):
        allCount = self.hitCount + self.missCount
        if allCount == 0:
            return 0
        return self.hitCount * 1.0 / allCount


class bytes_dict(dict):

    def __init__(self, name):
        self.table_name = name
        self.table = {}
        self.dKeys = []
        self.dataCache = DataCache(name)
        self.hotfixUpdate = {}
        self.hotfixDelIds = set([])
        self.recurTime = 0

    def __len__(self):
        return len(self.dKeys)

    def __repr__(self):
        return 'bytes_dict:' + self.table_name

    def __str__(self):
        return 'bytes_dict:' + self.table_name

    def clear(self):
        self.table.clear()

    def __getitem__(self, key):
        if key in self.hotfixDelIds:
            return
        elif self.hotfixUpdate.has_key(key):
            return self.hotfixUpdate.get(key)
        elif self.dataCache.hasCache(key):
            return self.dataCache.getCache(key)
        elif key is None:
            return
        else:
            key = self.validateKey(key)
            data = {}
            if type(key) == tuple:
                if len(key) == 2:
                    data = MemoryDB.getDataValue(self.table_name, key[0], key[1])
            else:
                data = MemoryDB.getDataValue(self.table_name, key)
            if data:
                value = self.table.get(key, {})
                if value:
                    data.update(value)
            else:
                data = self.table[key]
                if data == None:
                    data = {}
            self.dataCache.addCache(key, data)
            return data

    def validateKey(self, key):
        if type(key) == tuple:
            try:
                return tuple([ int(a) for a in key ])
            except:
                return None

        else:
            try:
                return int(key)
            except:
                return None

    def get(self, key, default = None):
        if key in self.hotfixDelIds:
            return default
        elif self.hotfixUpdate.has_key(key):
            return self.hotfixUpdate.get(key)
        elif self.dataCache.hasCache(key):
            return self.dataCache.getCache(key)
        else:
            key = self.validateKey(key)
            if not key:
                return default
            data = {}
            if type(key) == tuple:
                if len(key) == 2:
                    data = MemoryDB.getDataValue(self.table_name, key[0], key[1])
            else:
                data = MemoryDB.getDataValue(self.table_name, key)
            if data:
                value = self.table.get(key, {})
                if value:
                    data.update(value)
            else:
                data = self.table.get(key, {})
                if data == None:
                    data = {}
            self.dataCache.addCache(key, data)
            return data

    def __setitem__(self, key, value):
        self.table[key] = value

    def __delitem__(self, key):
        del self.table[key]

    def biSearch(self, key):
        low = 0
        high = len(self.dKeys) - 1
        while low <= high:
            middle = (high - low) / 2 + low
            if self.dKeys[middle] == key:
                return middle
            if self.dKeys[middle] > key:
                high = middle - 1
            else:
                low = middle + 1

        return -1

    def __contains__(self, key):
        return self.biSearch(key) != -1

    def has_key(self, key):
        return self.biSearch(key) != -1

    def __iter__(self):
        for k in self.dKeys:
            yield k

    def iterkeys(self):
        for k in self.dKeys:
            yield k

    def itervalues(self):
        for key in self.dKeys:
            yield self.get(key)

    def iteritems(self):
        for key in self.dKeys:
            yield (key, self.get(key))

    def normal_dict(self):
        raise NotImplemented

    def keys(self):
        return self.dKeys

    def values(self):
        for key in self.dKeys:
            yield self.get(key)

    def items(self):
        for key in self.dKeys:
            yield (key, self.get(key))

    def update(self, other):
        for i, v in other.iteritems():
            self.table[i] = v

    def updateHotfix(self, other):
        if not other:
            return
        for i, v in other.iteritems():
            self.table[i] = v
            self.hotfixUpdate[i] = v
            self.dataCache.removeCache(i)
            if i in self.hotfixDelIds:
                self.hotfixDelIds.remove(i)

    def pop(self):
        raise NotImplemented

    def popitem(self):
        raise NotImplemented


def checkMDBKeyValue(keyType, key, value):
    if keyType == KEY_TYPE_INT:
        if type(key) != int:
            return False
        if key < 0:
            return False
    elif keyType == KEY_TYPE_TUPLE_INT:
        if type(key) != tuple:
            return False
        if len(key) != 2:
            return False
        try:
            if int(key[0]) < 0:
                return False
            if int(key[1]) < 0:
                return False
        except:
            return False

    if type(value) != dict:
        return False
    return True


def _update_bytes_data(bd, data, keyType, name, attrs):
    bd.clear()
    for i, v in data.iteritems():
        if checkMDBKeyValue(keyType, i, v):
            v1 = {}
            keys = v.keys()
            for key in keys:
                if key not in attrs:
                    v1[key] = v[key]

            if v1:
                bd[i] = v1
        else:
            bd[i] = v
        bd.dKeys.append(i)

    bd.dKeys = sorted(bd.dKeys)


def convert_to_bytes_dict(data, keyType, name, attrs):
    assert name
    if type(data) != dict:
        return data
    b = bytes_dict(name)
    _update_bytes_data(b, data, keyType, name, attrs)
    data = None
    return b


def clearCacheFile():
    from helpers import newMDBConverter
    try:
        import os
        os.remove(newMDBConverter.BINARY_ENCRYPT_NAME)
    except Exception as e:
        gamelog.debug('m.l@.clearCacheFile error', e.message)


def convert_to_new_mdb_dict(data, keyType, name, attrs, valueAttrs, writeFile):
    assert name
    if type(data) != dict:
        return data
    from helpers import newMDBConverter
    gamelog.debug('m.l@.convert_to_new_mdb_dict', name, writeFile)
    if writeFile:
        newMDBConverter.MDBConverter.writeMDBModule(data, keyType, name, attrs, valueAttrs)
    b = bytes_dict(name)
    _update_bytes_data(b, data, keyType, name, attrs)
    return b
