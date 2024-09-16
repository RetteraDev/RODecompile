#Embedded file name: I:/bag/tmp/tw2/res/entities\common/cacheLRU.o


class Node(object):
    __slots__ = ['prev', 'next', 'key']

    def __init__(self, key):
        self.prev = None
        self.next = None
        self.key = key

    def clearNode(self):
        self.prev = None
        self.next = None
        self.key = None


class CacheLRU(object):

    def __init__(self, size):
        self._init_map(size)
        self.__max = size

    def _init_map(self, size):
        self.__map = {}
        nodes = [ Node(i) for i in xrange(size) ]
        for i in xrange(size):
            if i == 0:
                nodes[i].prev = None
                nodes[i].next = nodes[i + 1]
            elif i != size - 1:
                nodes[i].prev = nodes[i - 1]
                nodes[i].next = nodes[i + 1]
            else:
                nodes[i].prev = nodes[i - 1]
                nodes[i].next = None
            self.__map[i] = [None, nodes[i]]

        self.__old = nodes[0]
        self.__new = nodes[size - 1]

    def getMap(self):
        return self.__map

    def _move_to_new(self, node_i):
        node_prev = node_i.prev
        node_next = node_i.next
        if node_next == None:
            pass
        elif node_prev != None:
            node_prev.next = node_next
            node_next.prev = node_prev
            node_i.prev = self.__new
            node_i.next = None
            self.__new.next = node_i
            self.__new = node_i
        else:
            node_next.prev = None
            self.__old = node_next
            node_i.prev = self.__new
            node_i.next = None
            self.__new.next = node_i
            self.__new = node_i

    def get(self, key):
        vnn = self.__map.get(key, None)
        if vnn:
            self._move_to_new(vnn[1])
            return vnn[0]

    def add(self, key, value):
        vt = self.__map.get(key, None)
        if vt:
            vt[0] = value
            self._move_to_new(vt[1])
        else:
            self.__map.pop(self.__old.key)
            self.__old.key = key
            self.__map[key] = [value, self.__old]
            self._move_to_new(self.__old)

    def size(self):
        return reduce(lambda x, y: y[0] and x + 1 or x, self.__map.itervalues(), 0)

    def clear(self):
        for i in self.__map.itervalues():
            i[1].clearNode()

        self._init_map(self.__max)

    def __str__(self):
        result = ''
        node = self.__old
        while node != None:
            result += str(node.key) + ', '
            node = node.next

        return result


def test():
    cache = CacheLRU(5)
    assert cache.size() == 0
    print cache
    cache.add('1', 1)
    print cache
    cache.add('2', 2)
    print cache
    cache.add('3', 3)
    print cache
    cache.add('4', 4)
    print cache
    assert cache.size() == 4
    cache.add('5', 5)
    print cache
    cache.get('1')
    print cache
    cache.add('6', 6)
    print cache
    assert cache.get('2') == None
    assert cache.size() == 5
    cache.add('3', '33')
    print cache
    cache.add('a', 10)
    assert cache.get('4') == None
    print cache
    assert cache.get('5') != None
    assert cache.size() == 5
    print cache
    cache.add(None, 'None')
    assert cache.get(None) == 'None'
    cache.add('abc', 123)
    cache.add('abc', 0)
    assert cache.get('abc') != 123
    print cache
    assert cache.size() == 4
    cache.clear()
    assert cache.size() == 0
    print 'OK'
    import random
    import time
    test_loop = 10000
    random.seed(123)
    cache2 = CacheLRU(50)
    t1 = time.time()
    for i in xrange(test_loop):
        v = random.randint(0, test_loop)
        s = str(v)
        cache2.add(s, v)

    t2 = time.time()
    print 'add1', t2 - t1
    test_loop = 100000
    t1 = time.time()
    for i in xrange(test_loop):
        cache2.get(str(i))

    t2 = time.time()
    print 'get1', t2 - t1


if __name__ == '__main__':
    test()
