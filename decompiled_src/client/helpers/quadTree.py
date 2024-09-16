#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/quadTree.o


class QuadTreeNode(object):
    __slots__ = ['_treeDepth',
     'ulx',
     'uly',
     'drx',
     'dry',
     'num',
     'type',
     'elements']
    NODE = 0
    LEAF = 1
    META = 2
    SUB_N = (0, 1)
    SUB_E = (1, 3)
    SUB_S = (2, 3)
    SUB_W = (0, 2)
    SUB_NE = SUB_N + SUB_E
    SUB_SE = SUB_S + SUB_E
    SUB_NW = SUB_N + SUB_W
    SUB_SW = SUB_S + SUB_W

    def __init__(self, _range, _treeDepth, num, parentnum = []):
        self._treeDepth = _treeDepth
        self.ulx = float(_range[0])
        self.uly = float(_range[1])
        self.drx = float(_range[2])
        self.dry = float(_range[3])
        self.num = parentnum + [num]
        self.type = self.LEAF
        self.elements = []

    def inZone(self, pos):
        if self.canAdd(pos):
            if self.type == self.NODE:
                for e in self.elements:
                    t_zone = e.inZone(pos)
                    if t_zone:
                        return t_zone

            return self

    def birthChilds(self):
        if len(self.num) > self._treeDepth:
            return False
        self.type = self.NODE
        mx = (self.drx + self.ulx) / 2.0
        my = (self.uly + self.dry) / 2.0
        tElements = self.elements
        self.elements = []
        _range = [self.ulx,
         self.uly,
         mx,
         my]
        self.elements.append(QuadTreeNode(_range, self._treeDepth, 0, self.num))
        _range = [mx,
         self.uly,
         self.drx,
         my]
        self.elements.append(QuadTreeNode(_range, self._treeDepth, 1, self.num))
        _range = [self.ulx,
         my,
         mx,
         self.dry]
        self.elements.append(QuadTreeNode(_range, self._treeDepth, 2, self.num))
        _range = [mx,
         my,
         self.drx,
         self.dry]
        self.elements.append(QuadTreeNode(_range, self._treeDepth, 3, self.num))
        for te in tElements:
            self.addToChilds(te)

        return True

    def addToChilds(self, point):
        for e in self.elements:
            if e.addPoint(point):
                break

    def doDraw(self, drawObj):
        pass

    def getSubSet(self, directions):
        res = []
        if self.type == self.NODE:
            t_length = len(directions) / 2
            for i in xrange(t_length):
                t_sub = (directions[2 * i], directions[2 * i + 1])
                fa1 = (t_sub[0] + t_sub[1]) % 2
                res += self.elements[(t_sub[0] + fa1 + 1) % 4].getSubSet(t_sub)
                res += self.elements[(t_sub[1] + fa1 + 1) % 4].getSubSet(t_sub)

        else:
            res.append(self)
        return res

    def getZoneByNum(self, num, idx):
        if self.type == self.NODE:
            if idx < len(num):
                return self.elements[num[idx]].getZoneByNum(num, idx + 1)
            else:
                return self
        return self

    def doMark(self, drawObj, color = 'b'):
        pass

    def doPrint(self):
        print 'JUN:',
        if len(self.num) > 1:
            for i in xrange(len(self.num) - 2):
                print '|  ',

            print '|-',
        print str(self.num)
        if self.type == self.LEAF or self.type == self.META:
            for e in self.elements:
                print 'JUN:',
                if len(self.num) > 1:
                    for i in xrange(len(self.num) - 1):
                        print '|  ',

                    print '|-',
                e.doPrint()

        else:
            for e in self.elements:
                e.doPrint()

    def canAdd(self, pos):
        return self.ulx - 1e-09 <= pos[0] <= self.drx + 1e-09 and self.dry - 1e-09 <= pos[2] <= self.uly + 1e-09

    def addPoint(self, point):
        pos = (point.x, 0, point.z)
        if not self.canAdd(pos):
            return False
        if self.type == self.LEAF:
            self.elements.append(point)
            if len(self.elements) > 4:
                if not self.birthChilds():
                    self.type = self.META
        elif self.type == self.META:
            self.elements.append(point)
        elif self.type == self.NODE:
            self.addToChilds(point)
        return True

    def getAdjustZone0(self):
        res = {}
        t = self.num + []
        t[-1] += 1
        res[self.SUB_E] = t
        tt = t
        t = tt + []
        for i in xrange(len(t) - 1):
            if t[-(i + 1)] not in self.SUB_N:
                idx = len(t) - i - 1
                for ti in xrange(idx + 1, len(t)):
                    t[ti] += 2
                    t[ti] %= 4

                t[idx] -= 2
                t[idx] %= 4
                res[self.SUB_NE] = t
                break

        t = tt + []
        t[-1] += 2
        res[self.SUB_SE] = t
        t = self.num + []
        t[-1] += 2
        res[self.SUB_S] = t
        t = t + []
        for i in xrange(len(t) - 1):
            if t[-(i + 1)] not in self.SUB_W:
                idx = len(t) - i - 1
                for ti in xrange(idx + 1, len(t)):
                    t[ti] += 1
                    t[ti] %= 4

                t[idx] -= 1
                t[idx] %= 4
                res[self.SUB_SW] = t
                break

        t = self.num + []
        for i in xrange(len(t) - 1):
            if t[-(i + 1)] not in self.SUB_W:
                idx = len(t) - i - 1
                for ti in xrange(idx + 1, len(t)):
                    t[ti] += 1

                t[idx] -= 1
                res[self.SUB_W] = t
                t = t + []
                for i in xrange(len(t) - 1):
                    if t[-(i + 1)] not in self.SUB_N:
                        idx = len(t) - i - 1
                        for ti in xrange(idx + 1, len(t)):
                            t[ti] += 2
                            t[ti] %= 4

                        t[idx] -= 2
                        t[idx] %= 4
                        res[self.SUB_NW] = t
                        break

                break

        t = self.num + []
        for i in xrange(len(t) - 1):
            if t[-(i + 1)] not in self.SUB_N:
                idx = len(t) - i - 1
                for ti in xrange(idx + 1, len(t)):
                    t[ti] += 2

                t[idx] -= 2
                res[self.SUB_N] = t
                break

        return res

    def getAdjustZone1(self):
        res = {}
        t = self.num + []
        for i in xrange(len(t) - 1):
            if t[-(i + 1)] not in self.SUB_E:
                idx = len(t) - i - 1
                for ti in xrange(idx + 1, len(t)):
                    t[ti] -= 1
                    t[ti] %= 4

                t[idx] += 1
                t[idx] %= 4
                res[self.SUB_E] = t
                break

        t = self.num + []
        t[-1] += 2
        res[self.SUB_S] = t
        tt = t
        t = tt + []
        for i in xrange(len(t) - 1):
            if t[-(i + 1)] not in self.SUB_E:
                idx = len(t) - i - 1
                for ti in xrange(idx + 1, len(t)):
                    t[ti] -= 1
                    t[ti] %= 4

                t[idx] += 1
                t[idx] %= 4
                res[self.SUB_SE] = t
                break

        t = tt + []
        t[-1] -= 1
        res[self.SUB_SW] = t
        t = self.num + []
        t[-1] -= 1
        res[self.SUB_W] = t
        t = t + []
        for i in xrange(len(t) - 1):
            if t[-(i + 1)] not in self.SUB_N:
                idx = len(t) - i - 1
                for ti in xrange(idx + 1, len(t)):
                    t[ti] += 2

                t[idx] -= 2
                res[self.SUB_NW] = t
                break

        t = self.num + []
        for i in xrange(len(t) - 1):
            if t[-(i + 1)] not in self.SUB_N:
                idx = len(t) - i - 1
                for ti in xrange(idx + 1, len(t)):
                    t[ti] += 2
                    t[ti] %= 4

                t[idx] -= 2
                t[idx] %= 4
                res[self.SUB_N] = t
                t = t + []
                for i in xrange(len(t) - 1):
                    if t[-(i + 1)] not in self.SUB_E:
                        idx = len(t) - i - 1
                        for ti in xrange(idx + 1, len(t)):
                            t[ti] -= 1
                            t[ti] %= 4

                        t[idx] += 1
                        t[idx] %= 4
                        res[self.SUB_NE] = t
                        break

                break

        return res

    def getAdjustZone2(self):
        res = {}
        t = self.num + []
        t[-1] += 1
        res[self.SUB_E] = t
        tt = t
        t = tt + []
        t[-1] -= 2
        res[self.SUB_NE] = t
        t = tt + []
        for i in xrange(len(t) - 1):
            if t[-(i + 1)] not in self.SUB_E:
                idx = len(t) - i - 1
                for ti in xrange(idx + 1, len(t)):
                    t[ti] -= 2
                    t[ti] %= 4

                t[idx] += 2
                t[idx] %= 4
                res[self.SUB_SE] = t
                break

        t = self.num + []
        for i in xrange(len(t) - 1):
            if t[-(i + 1)] not in self.SUB_S:
                idx = len(t) - i - 1
                for ti in xrange(idx + 1, len(t)):
                    t[ti] -= 2
                    t[ti] %= 4

                t[idx] += 2
                t[idx] %= 4
                res[self.SUB_S] = t
                break

        t = self.num + []
        for i in xrange(len(t) - 1):
            if t[-(i + 1)] not in self.SUB_W:
                idx = len(t) - i - 1
                for ti in xrange(idx + 1, len(t)):
                    t[ti] += 1
                    t[ti] %= 4

                t[idx] -= 1
                t[idx] %= 4
                res[self.SUB_W] = t
                t = t + []
                for i in xrange(len(t) - 1):
                    if t[-(i + 1)] not in self.SUB_S:
                        idx = len(t) - i - 1
                        for ti in xrange(idx + 1, len(t)):
                            t[ti] -= 2
                            t[ti] %= 4

                        t[idx] += 2
                        t[idx] %= 4
                        res[self.SUB_SW] = t
                        break

                break

        t = self.num + []
        t[-1] -= 2
        res[self.SUB_N] = t
        t = t + []
        for i in xrange(len(t) - 1):
            if t[-(i + 1)] not in self.SUB_W:
                idx = len(t) - i - 1
                for ti in xrange(idx + 1, len(t)):
                    t[ti] += 1

                t[idx] -= 1
                res[self.SUB_NW] = t
                break

        return res

    def getAdjustZone3(self):
        res = {}
        t = self.num + []
        for i in xrange(len(t) - 1):
            if t[-(i + 1)] not in self.SUB_E:
                idx = len(t) - i - 1
                for ti in xrange(idx + 1, len(t)):
                    t[ti] -= 1
                    t[ti] %= 4

                t[idx] += 1
                t[idx] %= 4
                res[self.SUB_E] = t
                break

        t = self.num + []
        for i in xrange(len(t) - 1):
            if t[-(i + 1)] not in self.SUB_S:
                idx = len(t) - i - 1
                for ti in xrange(idx + 1, len(t)):
                    t[ti] -= 2
                    t[ti] %= 4

                t[idx] += 2
                t[idx] %= 4
                res[self.SUB_S] = t
                t = t + []
                for i in xrange(len(t) - 1):
                    if t[-(i + 1)] not in self.SUB_E:
                        idx = len(t) - i - 1
                        for ti in xrange(idx + 1, len(t)):
                            t[ti] -= 1
                            t[ti] %= 4

                        t[idx] += 1
                        t[idx] %= 4
                        res[self.SUB_SE] = t
                        break

                break

        t = self.num + []
        t[-1] -= 1
        res[self.SUB_W] = t
        tt = t
        t = tt + []
        t[-1] -= 2
        res[self.SUB_NW] = t
        t = tt + []
        for i in xrange(len(t) - 1):
            if t[-(i + 1)] not in self.SUB_S:
                idx = len(t) - i - 1
                for ti in xrange(idx + 1, len(t)):
                    t[ti] -= 2
                    t[ti] %= 4

                t[idx] += 2
                t[idx] %= 4
                res[self.SUB_SW] = t
                break

        t = self.num + []
        t[-1] -= 2
        res[self.SUB_N] = t
        t = t + []
        for i in xrange(len(t) - 1):
            if t[-(i + 1)] not in self.SUB_E:
                idx = len(t) - i - 1
                for ti in xrange(idx + 1, len(t)):
                    t[ti] -= 1
                    t[ti] %= 4

                t[idx] += 1
                t[idx] %= 4
                res[self.SUB_NE] = t
                break

        return res

    def getAdjustZone(self):
        if self.type == self.NODE:
            return None
        res = []
        if self.num[-1] == 0:
            res = self.getAdjustZone0()
        elif self.num[-1] == 1:
            res = self.getAdjustZone1()
        elif self.num[-1] == 2:
            res = self.getAdjustZone2()
        elif self.num[-1] == 3:
            res = self.getAdjustZone3()
        return res


class QuadTree(object):

    def __init__(self, _range, _treeDepth = 6):
        self.root = QuadTreeNode(_range, _treeDepth, 0)
        self.root.birthChilds()

    def getZoneByNum(self, num):
        return self.root.getZoneByNum(num, 1)

    def inZone(self, pos):
        return self.root.inZone(pos)

    def addPoint(self, point):
        self.root.addPoint(point)

    def doPrint(self):
        self.root.doPrint()

    def getSubSet(self, directions):
        return self.root.getSubSet(directions)

    def doDraw(self, drawObj):
        self.root.doDraw(drawObj)

    def getAroundPoints(self, pos):
        t_zone = self.inZone(pos)
        if not t_zone:
            return []
        all_points = [ x for x in t_zone.elements ]
        t_adjzones = t_zone.getAdjustZone()
        t_max_subset = []
        for directions, num in t_adjzones.iteritems():
            t_zone = self.getZoneByNum(num)
            if t_zone.type == t_zone.NODE:
                t_max_subset += t_zone.getSubSet(directions)
            else:
                t_max_subset.append(t_zone)

        for ss in t_max_subset:
            all_points += ss.elements

        return all_points
