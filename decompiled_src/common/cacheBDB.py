#Embedded file name: I:/bag/tmp/tw2/res/entities\common/cacheBDB.o
import bsddb
import os
import time
import BigWorld
try:
    from _msgpack import packb, unpackb
except:
    from msgpack import packb, unpackb
    if getattr(BigWorld, 'isBot', False):
        _unpackb = unpackb

        def unpackb(*args, **kwargs):
            if 'use_list' not in kwargs:
                kwargs['use_list'] = False
            return _unpackb(*args, **kwargs)


from struct import pack, unpack
import sys
from bsddb.db import DBLockDeadlockError
import gamelog
db = bsddb.db
CACHE_SIZE = 20971520
INSTANCE = 4
CACHE_DIR = 'cache'
_ignoreBDBCache = False
from time import sleep as _sleep

def DeadlockDecorator(f):

    def deadlock_retry(*args):
        while 1:
            try:
                return f(*args)
            except DBLockDeadlockError:
                _sleep(0.001)

    return deadlock_retry


def _openDBEnv():
    e = db.DBEnv()
    e.set_cachesize(0, CACHE_SIZE)
    e.set_lk_detect(db.DB_LOCK_DEFAULT)
    e.set_lk_max_locks(INSTANCE * 4000)
    e.set_lk_max_lockers(INSTANCE * 4000)
    e.set_lk_max_objects(INSTANCE * 4000)
    gamelog.info('get_lk_max_locks', e.get_lk_max_locks())
    gamelog.info('get_lk_max_lockers', e.get_lk_max_lockers())
    gamelog.info('get_lk_max_objects', e.get_lk_max_objects())
    gamelog.info('get_lg_bsize', e.get_lg_bsize())
    gamelog.info('get_lg_max', e.get_lg_max())
    e.mutex_set_max(INSTANCE * 10000)
    e.set_encrypt('$%RGT#$%^FTYT&*I^&*(HGEDFGHEFGH#$%^$%', db.DB_ENCRYPT_AES)
    e.set_shm_key(123456)
    sep = os.path.sep
    try:
        e.open('.' + sep + CACHE_DIR + sep, db.DB_INIT_TXN | db.DB_SYSTEM_MEM | db.DB_CREATE | db.DB_THREAD | db.DB_INIT_LOCK | db.DB_INIT_MPOOL)
        gamelog.info('jorsef: open normal')
    except bsddb.db.DBRunRecoveryError:
        gamelog.info('jorsef: Run DB_RECOVER')
        e.open('.' + sep + CACHE_DIR + sep, db.DB_INIT_TXN | db.DB_RECOVER | db.DB_SYSTEM_MEM | db.DB_CREATE | db.DB_THREAD | db.DB_INIT_LOCK | db.DB_INIT_MPOOL)
    except bsddb.db.DBRunRecoveryError:
        gamelog.info('jorsef: Run DB_RECOVER_FATAL')
        e.open('.' + sep + CACHE_DIR + sep, db.DB_INIT_TXN | db.DB_RECOVER_FATAL | db.DB_SYSTEM_MEM | db.DB_CREATE | db.DB_THREAD | db.DB_INIT_LOCK | db.DB_INIT_MPOOL)
    except bsddb.db.DBPermissionsError:
        raise 'jorsef: remove database'

    return e


try:
    os.mkdir(CACHE_DIR)
except:
    pass

_env = None
_version = 0
_ver_db = None
_lock_id = None

@DeadlockDecorator
def get_version(name):
    global _ver_db
    v, t = eval(_ver_db.get(name, '(0, 0)'))
    return (int(v), int(t))


@DeadlockDecorator
def set_version(name, ver, timestamp):
    _ver_db[name] = str((ver, timestamp))


@DeadlockDecorator
def is_update(name):
    global _ignoreBDBCache
    global _version
    ver, t = get_version(name)
    if _ignoreBDBCache or ver != 0 and ver == _version:
        return True
    return False


def lock_get():
    global _env
    global _lock_id
    if _lock_id:
        return _env.lock_get(_lock_id, 'update', db.DB_LOCK_WRITE)
    else:
        return None


def lock_put(lock):
    if lock:
        _env.lock_put(lock)


def get_cache_file(version):
    return 'game_v' + str(version) + '.cache'


def remove_unused_cache(cache_file):
    try:
        dir_list = os.listdir(os.path.join('..\\game\\', CACHE_DIR))
        for f in dir_list:
            if f.startswith('game') and f.endswith('.cache') and not f == cache_file:
                gamelog.info('clean old cache:', f)
                try:
                    os.unlink('.\\' + CACHE_DIR + '\\' + f)
                except:
                    pass

    except:
        try:
            dir_list = os.listdir(os.path.join(os.getcwd(), CACHE_DIR))
            for f in dir_list:
                if f.startswith('game') and f.endswith('.cache') and not f == cache_file:
                    gamelog.info('clean old cache:', f)
                    try:
                        os.unlink('.\\' + CACHE_DIR + '\\' + f)
                    except:
                        pass

        except:
            pass


def hotfix_update(table, data):
    if hasattr(table, 'sync'):
        for k, v in data.iteritems():
            table[k] = v

        table.sync()
    else:
        import cacheMDB
        if type(table) == cacheMDB.bytes_dict:
            table.updateHotfix(data)
            for k in data.keys():
                if not table.has_key(k):
                    table.dKeys.append(k)

            table.dKeys = sorted(table.dKeys)
        else:
            table.update(data)


def hotfix_del(table, keylist):
    import cacheMDB
    if type(table) == cacheMDB.bytes_dict:
        if keylist:
            table.hotfixDelIds.update(set(keylist))
            for k in keylist:
                if table.table.has_key(k):
                    del table.table[k]
                if table.has_key(k):
                    table.dKeys.remove(k)

    else:
        for k in keylist:
            if k not in table:
                continue
            del table[k]

        if hasattr(table, 'sync'):
            table.sync()


def OpenCache(version):
    global _env
    global _ver_db
    global _version
    global _lock_id
    _version = version
    _env = _openDBEnv()
    if _lock_id:
        _env.lock_id_free(_lock_id)
    _lock_id = _env.lock_id()
    _ver_db = db.DB(_env)
    _ver_db.set_pagesize(4096)
    cache_file = get_cache_file(version)
    remove_unused_cache(cache_file)
    try:
        _ver_db.open(cache_file, '__version_bdb__', dbtype=db.DB_BTREE, flags=db.DB_CREATE)
    except bsddb.db.DBInvalidArgError:
        _ver_db = db.DB(_env)
        _ver_db.remove(cache_file, '__version_bdb__')
        _ver_db = db.DB(_env)
        _ver_db.open(cache_file, '__version_bdb__', dbtype=db.DB_BTREE, flags=db.DB_CREATE)


def stat():
    for i, v in _env.memp_stat()[0].iteritems():
        gamelog.info(i, v)


def miss():
    return float(_env.memp_stat()[0]['cache_miss']) / _env.memp_stat()[0]['cache_hit']


bdbErrorTipShowed = False

def showBdbErrorTip():
    global bdbErrorTipShowed
    if not BigWorld.component == 'client':
        return
    if bdbErrorTipShowed:
        return
    bdbErrorTipShowed = True
    p = BigWorld.player()
    if p and p.__class__.__name__ == 'PlayerAvatar':
        if hasattr(p, 'showBdbErrorTip'):
            p.showBdbErrorTip()


class BDB_dict(dict):

    def __init__(self, name):
        self.table_name = name
        self.table = db.DB(_env)
        self.table.set_pagesize(4096)
        cache_file = get_cache_file(_version)
        try:
            self.table.open(cache_file, self.table_name, dbtype=db.DB_BTREE, flags=db.DB_CREATE)
        except bsddb.db.DBInvalidArgError:
            self.table = db.DB(_env)
            set_version(self.table_name, 0, 0)
            self.table.remove(cache_file, self.table_name)
            self.table = db.DB(_env)
            self.table.open(cache_file, self.table_name, dbtype=db.DB_BTREE, flags=db.DB_CREATE)

    def set_data(self, data):
        self.data = data

    def release_data(self):
        del self.data

    def set_class(self, cls):
        self.cls = cls

    def get_class(self):
        return self.cls

    def release_class(self):
        del self.cls

    def __len__(self):
        while 1:
            l = len(self.table)
            if l >= 0:
                return l
            _sleep(0.001)

    @DeadlockDecorator
    def __repr__(self):
        m = self.normal_dict()
        return repr(m)

    @DeadlockDecorator
    def __str__(self):
        m = self.normal_dict()
        return str(m)

    @DeadlockDecorator
    def clear(self):
        self.table.truncate()

    @DeadlockDecorator
    def __getitem__(self, key):
        return unpackb(self.table[packb(key)])

    @DeadlockDecorator
    def get(self, key, default = None):
        try:
            return unpackb(self.table.get(packb(key), packb(default)))
        except:
            return default

    @DeadlockDecorator
    def __setitem__(self, key, value):
        self.table[packb(key)] = packb(value)

    @DeadlockDecorator
    def __delitem__(self, key):
        del self.table[packb(key)]

    @DeadlockDecorator
    def __contains__(self, key):
        return self.table.has_key(packb(key))

    @DeadlockDecorator
    def has_key(self, key):
        try:
            return self.table.has_key(packb(key))
        except:
            return False

    @DeadlockDecorator
    def __iter__(self):
        keys = self.table.keys()
        for k in keys:
            yield unpackb(k)

    @DeadlockDecorator
    def iterkeys(self):
        ks = self.table.keys()
        for k in ks:
            yield unpackb(k)

    @DeadlockDecorator
    def itervalues(self):
        vs = self.table.values()
        for k in vs:
            yield unpackb(k)

    @DeadlockDecorator
    def iteritems(self):
        its = self.table.items()
        for i, v in its:
            yield (unpackb(i), unpackb(v))

    def normal_dict(self):
        return {unpackb(i):unpackb(v) for i, v in self.table.items()}

    @DeadlockDecorator
    def keys(self):
        ks = self.table.keys()
        return map(unpackb, ks)

    @DeadlockDecorator
    def values(self):
        vs = self.table.values()
        return map(unpackb, vs)

    @DeadlockDecorator
    def items(self):
        try:
            its = self.table.items()
        except:
            return []

        return [ (unpackb(i), unpackb(v)) for i, v in its ]

    @DeadlockDecorator
    def update(self, other):
        for i, v in other.iteritems():
            self.table[packb(i)] = packb(v)

    def pop(self):
        raise NotImplemented

    def popitem(self):
        raise NotImplemented

    def sync(self):
        self.table.sync()


class BDB_int_dict(BDB_dict):

    @DeadlockDecorator
    def __getitem__(self, key):
        try:
            return unpackb(self.table[pack('@i', key)])
        except:
            raise KeyError(key)

    @DeadlockDecorator
    def get(self, key, default = None):
        try:
            k = pack('@i', key)
        except:
            return default

        try:
            return unpackb(self.table.get(k, packb(default)))
        except:
            showBdbErrorTip()
            return default

    @DeadlockDecorator
    def __setitem__(self, key, value):
        self.table[pack('@i', key)] = packb(value)

    @DeadlockDecorator
    def __delitem__(self, key):
        del self.table[pack('@i', key)]

    @DeadlockDecorator
    def __contains__(self, key):
        try:
            return self.table.has_key(pack('@i', key))
        except:
            return False

    @DeadlockDecorator
    def has_key(self, key):
        if key == None:
            return False
        try:
            return self.table.has_key(pack('@i', key))
        except:
            return False

    @DeadlockDecorator
    def __iter__(self):
        keys = self.table.keys()
        for k in keys:
            yield unpack('@i', k)[0]

    @DeadlockDecorator
    def iterkeys(self):
        ks = self.table.keys()
        for k in ks:
            yield unpack('@i', k)[0]

    @DeadlockDecorator
    def itervalues(self):
        vs = self.table.values()
        for v in vs:
            yield unpackb(v)

    @DeadlockDecorator
    def iteritems(self):
        try:
            its = self.table.items()
        except:
            return

        for i, v in its:
            yield (unpack('@i', i)[0], unpackb(v))

    def normal_dict(self):
        return {unpack('@i', i)[0]:unpackb(v) for i, v in self.table.items()}

    @DeadlockDecorator
    def keys(self):
        return [ unpack('@i', k)[0] for k in self.table.keys() ]

    @DeadlockDecorator
    def values(self):
        vs = self.table.values()
        return map(unpackb, vs)

    @DeadlockDecorator
    def items(self):
        its = self.table.items()
        return [ (unpack('@i', i)[0], unpackb(v)) for i, v in its ]

    @DeadlockDecorator
    def update(self, other):
        for i, v in other.iteritems():
            self.table[pack('@i', i)] = packb(v)


class BDB_int_str_dict(BDB_dict):

    @DeadlockDecorator
    def __getitem__(self, key):
        try:
            return self.table[pack('@i', key)]
        except:
            raise KeyError(key)

    @DeadlockDecorator
    def get(self, key, default = None):
        try:
            k = pack('@i', key)
        except:
            return default

        try:
            return self.table.get(k, default)
        except:
            return default

    @DeadlockDecorator
    def __setitem__(self, key, value):
        self.table[pack('@i', key)] = value

    @DeadlockDecorator
    def __delitem__(self, key):
        del self.table[pack('@i', key)]

    @DeadlockDecorator
    def __contains__(self, key):
        return self.table.has_key(pack('@i', key))

    @DeadlockDecorator
    def has_key(self, key):
        try:
            return self.table.has_key(pack('@i', key))
        except:
            return False

    @DeadlockDecorator
    def __iter__(self):
        keys = self.table.keys()
        for k in keys:
            yield unpack('@i', k)[0]

    @DeadlockDecorator
    def iterkeys(self):
        ks = self.table.keys()
        for k in ks:
            yield unpack('@i', k)[0]

    @DeadlockDecorator
    def itervalues(self):
        vs = self.table.values()
        for v in vs:
            yield v

    @DeadlockDecorator
    def iteritems(self):
        its = self.table.items()
        for i, v in its:
            yield (unpack('@i', i)[0], v)

    def normal_dict(self):
        return {unpack('@i', i)[0]:v for i, v in self.table.items()}

    @DeadlockDecorator
    def keys(self):
        return [ unpack('@i', k)[0] for k in self.table.keys() ]

    @DeadlockDecorator
    def values(self):
        return self.table.values()

    @DeadlockDecorator
    def items(self):
        return [ (unpack('@i', i)[0], v) for i, v in self.table.items() ]

    @DeadlockDecorator
    def update(self, other):
        for i, v in other.iteritems():
            self.table[pack('@i', i)] = v


class BDB_str_dict(BDB_dict):

    @DeadlockDecorator
    def __getitem__(self, key):
        return unpackb(self.table[key])

    @DeadlockDecorator
    def get(self, key, default = None):
        try:
            return unpackb(self.table.get(key, packb(default)))
        except:
            showBdbErrorTip()
            return default

    @DeadlockDecorator
    def __setitem__(self, key, value):
        self.table[key] = packb(value)

    @DeadlockDecorator
    def __delitem__(self, key):
        del self.table[key]

    @DeadlockDecorator
    def __contains__(self, key):
        return self.table.has_key(key)

    @DeadlockDecorator
    def has_key(self, key):
        try:
            return self.table.has_key(key)
        except:
            return False

    @DeadlockDecorator
    def __iter__(self):
        keys = self.table.keys()
        for k in keys:
            yield k

    @DeadlockDecorator
    def iterkeys(self):
        ks = self.table.keys()
        for k in ks:
            yield k

    @DeadlockDecorator
    def iteritems(self):
        its = self.table.items()
        for i, v in its:
            yield (i, unpackb(v))

    def normal_dict(self):
        return {i:unpackb(v) for i, v in self.table.items()}

    @DeadlockDecorator
    def keys(self):
        return self.table.keys()

    @DeadlockDecorator
    def items(self):
        return [ (i, unpackb(v)) for i, v in self.table.items() ]

    @DeadlockDecorator
    def update(self, other):
        for i, v in other.iteritems():
            self.table[i] = packb(v)


class BDB_str_str_dict(BDB_dict):

    @DeadlockDecorator
    def __getitem__(self, key):
        return self.table[key]

    @DeadlockDecorator
    def get(self, key, default = None):
        return self.table.get(key, default)

    @DeadlockDecorator
    def __setitem__(self, key, value):
        self.table[key] = value

    @DeadlockDecorator
    def __delitem__(self, key):
        del self.table[key]

    @DeadlockDecorator
    def __contains__(self, key):
        return self.table.has_key(key)

    @DeadlockDecorator
    def has_key(self, key):
        try:
            return self.table.has_key(key)
        except:
            return False

    @DeadlockDecorator
    def __iter__(self):
        keys = self.table.keys()
        for k in keys:
            yield k

    @DeadlockDecorator
    def iterkeys(self):
        ks = self.table.keys()
        for k in ks:
            yield k

    @DeadlockDecorator
    def itervalues(self):
        vs = self.table.values()
        for v in vs:
            yield v

    @DeadlockDecorator
    def iteritems(self):
        its = self.table.items()
        for i, v in its:
            yield (i, v)

    def normal_dict(self):
        return {i:v for i, v in self.table.items()}

    @DeadlockDecorator
    def keys(self):
        return self.table.keys()

    @DeadlockDecorator
    def values(self):
        return self.table.values()

    @DeadlockDecorator
    def items(self):
        return self.table.items()

    @DeadlockDecorator
    def update(self, other):
        for i, v in other.iteritems():
            self.table[i] = v


def _update_BDB_data(bd, data, name):
    try:
        ver, t = get_version(name)
    except:
        ver, t = (0, 0)

    if not _ignoreBDBCache and _version <= ver:
        gamelog.info('reuse the cache')
        return
    gamelog.info('building new cache')
    bd.clear()
    for i, v in data.iteritems():
        bd[i] = v

    set_version(name, _version, int(time.time()))
    bd.sync()
    _ver_db.sync()


def get_BDB_dict(name, ktype = '', vtype = ''):
    return convert_to_BDB_dict({}, name, ktype, vtype)


def convert_to_BDB_dict(data, name, ktype = '', vtype = '', threshold = 0):
    assert name
    if type(data) != dict:
        gamelog.info('Table can not convert', name, type(data))
        return data
    if threshold and len(data) < threshold:
        return data
    lock = lock_get()
    try:
        if ktype == 'int' and vtype == 'str':
            b = BDB_int_str_dict(name)
        elif ktype == 'str' and vtype == 'str':
            b = BDB_str_str_dict(name)
        elif ktype == 'int':
            b = BDB_int_dict(name)
        elif ktype == 'str':
            b = BDB_str_dict(name)
        else:
            b = BDB_dict(name)
        _update_BDB_data(b, data, name)
    finally:
        lock_put(lock)

    return b


def test():
    data1 = {1: 2,
     3: 4,
     '5': '6',
     (7, 8): (9, 10)}
    data2 = {8: 8,
     9: 9,
     10: 10,
     (11, 11): 11}
    data1 = convert_to_BDB_dict(data1, 'data1')
    data2 = convert_to_BDB_dict(data2, 'data2')
    gamelog.info('size of data1', len(data1))
    gamelog.info('size of data2', len(data2))
    assert len(data1) == 4
    assert len(data2) == 4
    assert 8 in data2
    assert data1.has_key(1)
    assert sorted(data1.keys()) == sorted([(7, 8),
     1,
     3,
     '5'])
    assert sorted(data1.values()) == sorted([(9, 10),
     2,
     4,
     '6'])
    assert sorted(data1.items()) == [(1, 2),
     (3, 4),
     ('5', '6'),
     ((7, 8), (9, 10))]
    assert sorted([ it for it in data1.iteritems() ]) == [(1, 2),
     (3, 4),
     ('5', '6'),
     ((7, 8), (9, 10))]
    assert sorted(data2.keys()) == sorted([10,
     9,
     (11, 11),
     8])
    assert sorted(data2.values()) == sorted([10,
     9,
     11,
     8])
    assert sorted(data2.items()) == [(8, 8),
     (9, 9),
     (10, 10),
     ((11, 11), 11)]
    assert sorted([ it for it in data2.iteritems() ]) == [(8, 8),
     (9, 9),
     (10, 10),
     ((11, 11), 11)]
    assert data1[1] == 2
    del data1[1]
    assert len(data1) == 3
    data1[100] = 100
    assert data1[100] == 100
    assert len(data1) == 4
    assert data1.get(999) == None
    assert data1.get(999, 888) == 888
    data2.clear()
    assert len(data2) == 0
    data1.update({'a': 1,
     'b': 2})
    assert data1.normal_dict() == {'a': 1,
     'b': 2,
     100: 100,
     3: 4,
     '5': '6',
     (7, 8): (9, 10)}
    gamelog.info('end of test')
    return True


def test2():
    data3 = {1: 2,
     3: 4,
     5: 5,
     6L: 6}
    data3 = convert_to_BDB_dict(data3, 'data3', ktype='int', vtype='var')
    gamelog.info('size of data3', len(data3))
    assert len(data3) == 4
    assert data3.has_key(3)
    assert 3 in data3
    assert sorted(data3.keys()) == [1,
     3,
     5,
     6L]
    assert sorted([ k for k in data3.iterkeys() ]) == [1,
     3,
     5,
     6L]
    assert sorted(data3.values()) == [2,
     4,
     5,
     6]
    assert sorted([ v for v in data3.itervalues() ]) == [2,
     4,
     5,
     6]
    assert sorted(data3.items()) == [(1, 2),
     (3, 4),
     (5, 5),
     (6, 6)]
    assert sorted([ it for it in data3.iteritems() ]) == [(1, 2),
     (3, 4),
     (5, 5),
     (6, 6)]
    assert data3[1] == 2
    del data3[1]
    assert len(data3) == 3
    data3[100] = 100
    assert data3[100] == 100
    assert len(data3) == 4
    assert data3.get(999) == None
    assert data3.get(999, 888) == 888
    data3.update({111: 1,
     222: 2})
    assert data3.normal_dict() == {3: 4,
     100: 100,
     5: 5,
     6L: 6,
     111: 1,
     222: 2}
    gamelog.info('end of test 2')
    return True


def test3():
    data4 = {1: 'a',
     2: 'b',
     3: 'c'}
    normal = data4
    data4 = convert_to_BDB_dict(data4, 'data4', ktype='int', vtype='str')
    assert data4.normal_dict() == normal
    assert data4.has_key(1)
    assert 3 in data4
    assert sorted(data4.keys()) == [1, 2, 3]
    assert sorted([ k for k in data4.iterkeys() ]) == [1, 2, 3]
    assert sorted(data4.values()) == ['a', 'b', 'c']
    assert sorted([ v for v in data4.itervalues() ]) == ['a', 'b', 'c']
    assert sorted(data4.items()) == [(1, 'a'), (2, 'b'), (3, 'c')]
    assert sorted([ it for it in data4.iteritems() ]) == [(1, 'a'), (2, 'b'), (3, 'c')]
    assert data4[1] == 'a'
    assert data4[2] == 'b'
    assert data4[3] == 'c'
    assert data4.get(4, 'z') == 'z'
    data4[4] = 'd'
    assert data4[4] == 'd'
    del data4[4]
    assert data4.get(4, 'z') == 'z'
    data4.update({5: 'e'})
    assert data4[5] == 'e'
    gamelog.info('end of test 3')
    return True


def test4():
    data5 = {'A': 1,
     'B': 'b',
     'C': (3,)}
    normal = data5
    data5 = convert_to_BDB_dict(data5, 'data5', ktype='str', vtype='var')
    assert data5.normal_dict() == normal
    assert data5.has_key('A')
    assert 'A' in data5
    assert sorted(data5.keys()) == ['A', 'B', 'C']
    assert sorted([ k for k in data5.iterkeys() ]) == ['A', 'B', 'C']
    assert sorted(data5.values()) == [1, 'b', (3,)]
    assert sorted([ v for v in data5.itervalues() ]) == [1, 'b', (3,)]
    assert sorted(data5.items()) == [('A', 1), ('B', 'b'), ('C', (3,))]
    assert sorted([ it for it in data5.iteritems() ]) == [('A', 1), ('B', 'b'), ('C', (3,))]
    assert data5['A'] == 1
    assert data5['B'] == 'b'
    assert data5['C'] == (3,)
    assert data5.get('D', 'z') == 'z'
    data5['D'] = 'd'
    assert data5['D'] == 'd'
    del data5['D']
    assert data5.get('D', 'z') == 'z'
    data5.update({'E': 5})
    assert data5['E'] == 5
    gamelog.info('end of test 4')
    return True


def test5():
    data6 = {'A': 'a',
     'B': 'b',
     'C': 'c'}
    normal = data6
    data6 = convert_to_BDB_dict(data6, 'data6', ktype='str', vtype='str')
    assert data6.normal_dict() == normal
    assert data6.has_key('A')
    assert 'B' in data6
    assert sorted(data6.keys()) == ['A', 'B', 'C']
    assert sorted([ k for k in data6.iterkeys() ]) == ['A', 'B', 'C']
    assert sorted(data6.values()) == ['a', 'b', 'c']
    assert sorted([ v for v in data6.itervalues() ]) == ['a', 'b', 'c']
    assert sorted(data6.items()) == [('A', 'a'), ('B', 'b'), ('C', 'c')]
    assert sorted([ it for it in data6.iteritems() ]) == [('A', 'a'), ('B', 'b'), ('C', 'c')]
    assert data6['A'] == 'a'
    assert data6['B'] == 'b'
    assert data6['C'] == 'c'
    assert data6.get('D', 'z') == 'z'
    data6['D'] = 'd'
    assert data6['D'] == 'd'
    del data6['D']
    assert data6.get('D', 'z') == 'z'
    data6.update({'E': 'e'})
    assert data6['E'] == 'e'
    gamelog.info('end of test 5')
    return True


def test_recover():
    data_rc = {'A': 'a',
     'B': 'b',
     'C': 'c'}
    data = convert_to_BDB_dict(data_rc, 'data_rc')
    import time
    while 1:
        d = data['A']
        del d
        time.sleep(0.001)


def test_multi():
    import time
    now = time.time()
    x = ({'rand': 1,
      'rpr': 42,
      'sch': (1,),
      'imprint': 1,
      'intro': '',
      'bctype': 1,
      'mwrap': 1,
      'mmax': 7,
      'mdur': 182,
      'can_inlay': 1,
      'hgt': 3,
      'mmin': 4,
      'pmin': 7,
      'type': 1,
      'pmax': 12,
      'pr': 1137,
      'reqlv': 1,
      'twohand': 1,
      'bcprice': 100,
      'atspd': 19,
      'name': '³¤µ¶',
      'atype': 5,
      'range': 6.0,
      'lv': 4,
      'cri': 2,
      'stype': 1},)
    multi_data = {i:x for i in xrange(5000)}
    COUNT = 100
    for i in xrange(COUNT):
        gamelog.info('build', i)
        data = convert_to_BDB_dict(multi_data, 'multi' + str(i), ktype='int')

    gamelog.info('build time:', time.time() - now)
    now = time.time()
    for i in xrange(COUNT):
        gamelog.info('verify', i)
        data = convert_to_BDB_dict(multi_data, 'multi' + str(i), ktype='int')
        for k, v in multi_data.iteritems():
            assert v == data[k]

    gamelog.info('run time:', time.time() - now)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise RuntimeError('args must > 2')
    OpenCache(int(sys.argv[1]))
    assert test()
    assert test2()
    assert test3()
    assert test4()
    assert test5()
