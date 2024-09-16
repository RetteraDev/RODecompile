#Embedded file name: /WORKSPACE/data/entities/common/smath.o
import random
import math
import Math
try:
    import cSMath
except ImportError:
    cSMath = {}

def __script_inRange3D(range, p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    dz = p1[2] - p2[2]
    if dx * dx + dy * dy + dz * dz < range * range:
        return True
    return False


try:
    inRange3D = cSMath.inRange3D
except AttributeError:
    inRange3D = __script_inRange3D

def __script_inRange2D(range, p1, p2):
    dx = p1[0] - p2[0]
    dz = p1[2] - p2[2]
    if dx * dx + dz * dz < range * range:
        return True
    return False


try:
    inRange2D = cSMath.inRange2D
except AttributeError:
    inRange2D = __script_inRange2D

def __script_distance(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    dz = p1[2] - p2[2]
    return math.sqrt(dx * dx + dy * dy + dz * dz)


def distance3D(p1, p2):
    try:
        return cSMath.distance(tuple(p1), tuple(p2))
    except AttributeError:
        return __script_distance(p1, p2)


try:
    distance = cSMath.distance
except AttributeError:
    distance = __script_distance

def __script_distance2D(p1, p2):
    dx = p1[0] - p2[0]
    dz = p1[2] - p2[2]
    return math.sqrt(dx * dx + dz * dz)


try:
    distance2D = cSMath.distance2D
except AttributeError:
    distance2D = __script_distance2D

def inRectRange2D(range, p1, p2):
    dx = p1[0] - p2[0]
    dz = p1[2] - p2[2]
    return abs(dx) <= range and abs(dz) <= range


def __script_limit(value, min, max):
    if value > max:
        value = max
    elif value < min:
        value = min
    return value


limit = __script_limit

def __script_limitf(value, min, max):
    if value > max:
        value = max
    elif value < min:
        value = min
    return float(value)


limitf = __script_limitf
G_VECTORS = ((0, 1),
 (0.866, 0.5),
 (0.866, -0.5),
 (0, -1),
 (-0.866, -0.5),
 (-0.866, 0.5))

def scatter(pos, R, r):
    vPos = Math.Vector2(pos[0], pos[1])
    if R == 0 or r == 0:
        return [vPos]
    if 2 * r > R:
        return [vPos]
    if 2 * r < R and 3 * r >= R:
        return _roundCircleFlat(vPos, r)
    points = []
    points.append(vPos)
    n = 1
    while r * (n * 2 + 1) <= R:
        points += _roundCircleHexagen(n, r, vPos)
        n += 1

    quadrants = [[],
     [],
     [],
     []]
    for vp in points:
        v = vp - vPos
        if v.x > 0 and v.y > 0:
            quadrants[0].append(vp)
        elif v.x < 0 and v.y > 0:
            quadrants[1].append(vp)
        elif v.x > 0 and v.y < 0:
            quadrants[2].append(vp)
        elif v.x < 0 and v.y < 0:
            quadrants[3].append(vp)

    random.shuffle(quadrants)
    sortPoints = []
    i = 0
    while True:
        if len(quadrants[i]) > 1:
            p = random.choice(quadrants[i])
            sortPoints.append(p)
            quadrants[i].remove(p)
            if i >= len(quadrants) - 1:
                i = 0
            else:
                i += 1
        elif len(quadrants[i]) == 1:
            p = random.choice(quadrants[i])
            sortPoints.append(p)
            quadrants.pop(i)
            if len(quadrants) == 0:
                break
            elif i >= len(quadrants) - 1:
                i = 0
            else:
                i += 1
        else:
            quadrants.pop(i)
            if len(quadrants) == 0:
                break
            elif i >= len(quadrants) - 1:
                i = 0
            else:
                i += 1

    sortPoints.append(vPos)
    return sortPoints


def _roundCircleHexagen(layer, r, pos):
    ret = []
    vectors = rotate2D(G_VECTORS)
    dist = layer * 2 * r
    for v in vectors:
        dpos = pos + Math.Vector2(v[0] * dist, v[1] * dist)
        ret.append(dpos)

    hexagen = []
    for n in xrange(len(ret)):
        a = ret[n]
        nn = n + 1
        if nn >= len(ret):
            nn = 0
        b = ret[nn]
        line = b - a
        lineLen = line.length
        interN = int(round((lineLen - 2 * r) / (2 * r)))
        line.normalise()
        for i in xrange(interN):
            dpos = a + Math.Vector2(line[0] * (i + 1) * 2 * r, line[1] * (i + 1) * 2 * r)
            hexagen.append(dpos)

    return ret + hexagen


def _roundCircleFlat(pos, r):
    ret = []
    vectors = rotate2D(G_VECTORS)
    v = vectors[0]
    dpos = pos + Math.Vector2(v[0] * r, v[1] * r)
    ret.append(dpos)
    v = vectors[3]
    dpos = pos + Math.Vector2(v[0] * r, v[1] * r)
    ret.append(dpos)
    return ret


pi = 3.141592653589793

def rotate2D(vector2Ds):
    global pi
    rt = []
    yaw = (random.random() * 2 - 1) * pi
    for vector2D in vector2Ds:
        a = Math.Matrix()
        a.setRotateY(yaw)
        lastP = a.applyPoint((vector2D[0], 0, vector2D[1]))
        rt.append((lastP[0], lastP[2]))

    return rt


def twin(originD, fixP, fixD, relP, relD):
    a = Math.Matrix()
    b = Math.Matrix()
    c = Math.Matrix()
    a.setRotateY(-originD[2])
    b.setRotateY(fixD[2])
    c.setTranslate(fixP)
    a.postMultiply(b)
    a.postMultiply(c)
    lastP = a.applyPoint(relP)
    lastD = (fixD[0] + relD[0], fixD[1] + relD[1], fixD[2] + relD[2])
    return (Math.Vector3(lastP), Math.Vector3(lastD))


def internalPoint(srcPos, dstPos):
    x, y, z = srcPos
    x2, y2, z2 = dstPos
    return ((x + x2) / 2, (y + y2) / 2, (z + z2) / 2)


def getCirclePoints(centerPos, startPos, pointCount):
    if pointCount <= 1:
        return (startPos,)
    mat = Math.Matrix()
    mat.setRotateY(6.283185307 / pointCount)
    result = []
    point = startPos - centerPos
    for i in xrange(pointCount):
        result.append(point + centerPos)
        point = mat.applyPoint(point)

    return tuple(result)


def getSection(dValue):
    totalValue = 0
    vkDict = {}
    sections = []
    for k, v in dValue.iteritems():
        totalValue += v
        sections.append(totalValue)
        vkDict[totalValue] = k

    r = random.randint(0, totalValue - 1)
    for i, s in enumerate(sections):
        if r < s:
            return vkDict[s]
    else:
        return vkDict[s]


def clamp(v, minv, maxv):
    if minv > maxv:
        maxv, minv = minv, maxv
    return max(minv, min(v, maxv))


def circleIntersectRectange2D(cx, cz, r, minx, minz, maxx, maxz):
    closestX = clamp(cx, minx, maxx)
    closestZ = clamp(cz, minz, maxz)
    dx = closestX - cx
    dz = closestZ - cz
    return dx * dx + dz * dz <= r * r


def circleIntersectLineSegment2D(cx, cz, r, x, z):
    """
    refer to http://yehar.com/blog/?p=2926
    
    end points of line segment are (0,0) and (x,y)
    r is the radius of circle, while center of circle is (cx, cz)
    """
    r2 = r * r
    if cx * cx + cz * cz <= r2 or (cx - x) * (cx - x) + (cz - z) * (cz - z) <= r2:
        return True
    a = cx * x + cz * z
    b = cz * x - cx * z
    b2 = b * b
    d2 = x * x + z * z
    return a >= 0 and a <= d2 and b2 <= r2 * d2


def getRatetePositionWithYaw(yaw, pos):
    m = Math.Matrix()
    m.setRotateY(yaw)
    if len(pos) == 2:
        pos = (pos[0], 0, pos[1])
    newPos = m.applyPoint(pos)
    return newPos
