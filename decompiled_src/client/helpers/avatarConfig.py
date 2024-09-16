#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/avatarConfig.o
import BigWorld

def __f(f):
    return (f - 0.5) / 50


def __check(boneScaleInfo, boneName):
    if boneScaleInfo.has_key(boneName):
        return boneScaleInfo[boneName]
    boneScaleInfo[boneName] = {'scale': {'x': 1,
               'y': 1,
               'z': 1},
     'trans': {'x': 0,
               'y': 0,
               'z': 0},
     'boneScale': 1,
     'boneLengthScale': 1,
     'rot': {'x': 0,
             'y': 0,
             'z': 0}}
    return boneScaleInfo[boneName]


def __cheekH(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_cheek_upper_R')
    __check(boneScaleInfo, 'head_cheek_upper_L')
    __check(boneScaleInfo, 'head_cheek_udder_R')
    __check(boneScaleInfo, 'head_cheek_udder_L')
    f = __f(f)
    boneScaleInfo['head_cheek_upper_R']['trans']['y'] = f
    boneScaleInfo['head_cheek_upper_L']['trans']['y'] = -f
    boneScaleInfo['head_cheek_udder_R']['trans']['y'] = f
    boneScaleInfo['head_cheek_udder_L']['trans']['y'] = -f


def __cheekV(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_upper')['scale']['z'] = f * 2
    __check(boneScaleInfo, 'head_udder')['scale']['z'] = f * 2


def __headUpper(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_upper')
    boneScaleInfo['head_upper']['scale']['z'] = f * 2


def __headMiddle(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_middle')
    boneScaleInfo['head_middle']['scale']['z'] = f * 2


def __headUdder(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_chin')
    __check(boneScaleInfo, 'head_udder')['scale']['z'] = 1 + (1 - f * 2) / 3
    boneScaleInfo['head_chin']['trans']['z'] = -__f(f)
    boneScaleInfo['head_chin']['scale']['y'] = 1 + (0.5 - f) / 2.0


def __headForeheadH(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_forehead')
    boneScaleInfo['head_forehead']['trans']['x'] = __f(f)


def __headForeheadV(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_forehead')
    boneScaleInfo['head_forehead']['trans']['z'] = __f(f)


def __headForeheadZ(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_forehead')
    boneScaleInfo['head_forehead']['trans']['y'] = __f(f)


def __headForeheadRot(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_forehead')
    boneScaleInfo['head_forehead']['rot']['x'] = f - 0.5


def __headForeheadScale(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_forehead')
    boneScaleInfo['head_forehead']['boneScale'] = f * 2


def __headZygomaH(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_zygoma_R')
    __check(boneScaleInfo, 'head_zygoma_L')
    boneScaleInfo['head_zygoma_L']['trans']['x'] = __f(f)
    boneScaleInfo['head_zygoma_R']['trans']['x'] = __f(f)


def __headZygomaV(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_zygoma_R')
    __check(boneScaleInfo, 'head_zygoma_L')
    boneScaleInfo['head_zygoma_L']['trans']['z'] = __f(f)
    boneScaleInfo['head_zygoma_R']['trans']['z'] = __f(f)


def __headZygomaZ(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_zygoma_R')
    __check(boneScaleInfo, 'head_zygoma_L')
    boneScaleInfo['head_zygoma_L']['trans']['y'] = __f(f)
    boneScaleInfo['head_zygoma_R']['trans']['y'] = __f(f)


def __headZygomaRot(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_zygoma_R')['rot']['x'] = f - 0.5
    __check(boneScaleInfo, 'head_zygoma_L')['rot']['x'] = f - 0.5


def __headZygomaScale(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_zygoma_R')
    __check(boneScaleInfo, 'head_zygoma_L')
    boneScaleInfo['head_zygoma_L']['boneScale'] = f * 2
    boneScaleInfo['head_zygoma_R']['boneScale'] = f * 2


def __headChinV(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_chin')
    boneScaleInfo['head_chin']['trans']['z'] = __f(f)


def __headChinZ(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_chin')
    boneScaleInfo['head_chin']['trans']['x'] = __f(f)


def __headChinRot(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_chin')['rot']['y'] = f - 0.5


def __headChinScaleH(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_chin')
    boneScaleInfo['head_chin']['scale']['y'] = f * 2


def __headJawH(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_jaw_R')['trans']['x'] = __f(f)
    __check(boneScaleInfo, 'head_jaw_L')['trans']['x'] = __f(f)


def __headJawV(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_jaw_R')['trans']['z'] = __f(f)
    __check(boneScaleInfo, 'head_jaw_L')['trans']['z'] = __f(f)


def __headJawZ(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_jaw_R')['trans']['x'] = __f(f)
    __check(boneScaleInfo, 'head_jaw_L')['trans']['x'] = __f(f)


def __headJawScaleH(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_jaw_R')['scale']['x'] = f * 2
    __check(boneScaleInfo, 'head_jaw_L')['scale']['x'] = f * 2


def __headJawScaleV(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_jaw_R')['scale']['z'] = f * 2
    __check(boneScaleInfo, 'head_jaw_L')['scale']['z'] = f * 2


def __headJawSpeciel(boneScaleInfo, f):
    pass


def __headEyeballScale(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_eyeball_R')['boneScale'] = f * 2
    __check(boneScaleInfo, 'head_eyeball_L')['boneScale'] = f * 2


def __headEyebrowH(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_eyebrow_R')
    __check(boneScaleInfo, 'head_eyebrow_L')
    boneScaleInfo['head_eyebrow_R']['trans']['y'] = __f(f)
    boneScaleInfo['head_eyebrow_L']['trans']['y'] = -__f(f)


def __headEyebrowV(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_eyebrow_R')
    __check(boneScaleInfo, 'head_eyebrow_L')
    boneScaleInfo['head_eyebrow_R']['trans']['z'] = __f(f)
    boneScaleInfo['head_eyebrow_L']['trans']['z'] = __f(f)


def __headEyebrowZ(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_eyebrow_R')
    __check(boneScaleInfo, 'head_eyebrow_L')
    boneScaleInfo['head_eyebrow_R']['trans']['x'] = __f(f)
    boneScaleInfo['head_eyebrow_L']['trans']['x'] = __f(f)


def __headEyebrowRot(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_eyebrow_R')['rot']['x'] = f - 0.5
    __check(boneScaleInfo, 'head_eyebrow_L')['rot']['x'] = 0.5 - f


def __headEyebrowScaleH(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_eyebrow_R')
    __check(boneScaleInfo, 'head_eyebrow_L')
    boneScaleInfo['head_eyebrow_R']['scale']['y'] = f * 2
    boneScaleInfo['head_eyebrow_L']['scale']['y'] = f * 2


def __headEyebrowScaleV(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_eyebrow_R')
    __check(boneScaleInfo, 'head_eyebrow_L')
    boneScaleInfo['head_eyebrow_R']['scale']['z'] = f * 2
    boneScaleInfo['head_eyebrow_L']['scale']['z'] = f * 2


def __headLipupV(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_lip_up')['trans']['z'] = __f(f)
    __check(boneScaleInfo, 'head_lip_low')['trans']['z'] = __f(f)
    __check(boneScaleInfo, 'head_mouth_up')['trans']['z'] = __f(f)
    __check(boneScaleInfo, 'head_mouth_low')['trans']['z'] = __f(f)
    __check(boneScaleInfo, 'head_mouth_side_R')['trans']['z'] = __f(f)
    __check(boneScaleInfo, 'head_mouth_side_L')['trans']['z'] = __f(f)


def __headLipupScaleH(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_lip_up')['scale']['y'] = f * 2
    __check(boneScaleInfo, 'head_lip_low')['scale']['y'] = f * 2


def __headLipupScaleV(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_lip_up')['scale']['z'] = f * 2


def __headLiplowV(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_lip_low')['trans']['z'] = __f(f)


def __headLiplowScaleH(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_lip_low')['scale']['x'] = f * 2


def __headLiplowScaleV(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_lip_low')['scale']['z'] = f * 2


def __headMouthSide(boneScaleInfo, f):
    __check(boneScaleInfo, 'head_mouth_side_R')['trans']['z'] = __f(f)
    __check(boneScaleInfo, 'head_mouth_side_L')['trans']['z'] = __f(f)


boneModifyFunc = {100: __cheekH,
 101: __cheekV,
 102: __headUpper,
 103: __headMiddle,
 104: __headUdder,
 105: __headForeheadH,
 106: __headForeheadV,
 107: __headForeheadZ,
 108: __headForeheadRot,
 109: __headForeheadScale,
 110: __headZygomaH,
 111: __headZygomaV,
 112: __headZygomaZ,
 113: __headZygomaRot,
 114: __headZygomaScale,
 115: __headChinV,
 116: __headChinZ,
 117: __headChinRot,
 118: __headChinScaleH,
 119: __headJawH,
 120: __headJawV,
 121: __headJawZ,
 122: __headJawScaleH,
 123: __headJawScaleV,
 124: __headJawSpeciel,
 125: __headEyeballScale,
 126: __headEyebrowH,
 127: __headEyebrowV,
 128: __headEyebrowZ,
 129: __headEyebrowRot,
 130: __headEyebrowScaleH,
 131: __headEyebrowScaleV,
 132: __headLipupV,
 133: __headLipupScaleH,
 134: __headLipupScaleV,
 135: __headLiplowV,
 136: __headLiplowScaleH,
 137: __headLiplowScaleV,
 138: __headMouthSide}

class AvatarConfig(object):

    def __init__(self, model = None):
        if model is not None:
            self.model = model
        else:
            self.model = BigWorld.player().model
        self.boneScale = BigWorld.BoneScale()
        self.boneScaleInfo = {}
        self.config = {}

    def save(self, where):
        pass

    def load(self, where):
        pass

    def transformTo(self, partID, f):
        self.config[partID] = f
        return self.model.transformTo(1, partID, f) and self.model.applyMorph(1)

    def selectBaseShape(self, partID, n):
        self.config[partID] = n
        return self.model.selectBaseShape(1, partID, n) and self.model.applyMorph(1)

    def chooseFace(self, n):
        return self.selectBaseShape(1, n)

    def zygomaticWideClose(self, f):
        return self.transformTo(2, f)

    def zygomaticUpLow(self, f):
        return self.transformTo(3, f)

    def zygomaticForwardBackward(self, f):
        return self.transformTo(4, f)

    def zygomaticCwCcw(self, f):
        return self.transformTo(5, f)

    def zygomaticBigSmall(self, f):
        return self.transformTo(6, f)

    def cheekWideClose(self, f):
        return self.transformTo(7, f)

    def cheekUpLow(self, f):
        return self.transformTo(8, f)

    def cheekForwardBackward(self, f):
        return self.transformTo(9, f)

    def cheekBigSmall(self, f):
        return self.transformTo(10, f)

    def chinUpLow(self, f):
        return self.transformTo(11, f)

    def chinForwardBackward(self, f):
        return self.transformTo(12, f)

    def chinCwCcw(self, f):
        return self.transformTo(13, f)

    def chinBigSmall(self, f):
        return self.transformTo(14, f)

    def jawWideClose(self, f):
        return self.transformTo(15, f)

    def jawUpLow(self, f):
        return self.transformTo(16, f)

    def jawForwardBackward(self, f):
        return self.transformTo(17, f)

    def jawBigSmall(self, f):
        return self.transformTo(18, f)

    def jawHScaleoutScalein(self, f):
        return self.transformTo(19, f)

    def jawVScaleoutScalein(self, f):
        return self.transformTo(20, f)

    def chooseEye(self, n):
        return self.selectBaseShape(21, n)

    def eyeHScaleoutScalein(self, f):
        return self.transformTo(22, f)

    def eyeVScaleoutScalein(self, f):
        return self.transformTo(23, f)

    def eyeCwCcw(self, f):
        return self.transformTo(24, f)

    def eyeWideClose(self, f):
        return self.transformTo(25, f)

    def eyeUpLow(self, f):
        return self.transformTo(26, f)

    def eyeForwardBackward(self, f):
        return self.transformTo(27, f)

    def eyeballBigSmall(self, f):
        return self.transformTo(28, f)

    def chooseEyebrow(self, n):
        return self.selectBaseShape(29, n)

    def eyebrowHScaleoutScalein(self, f):
        return self.transformTo(30, f)

    def eyebrowVScaleoutScalein(self, f):
        return self.transformTo(31, f)

    def eyebrowCwCcw(self, f):
        return self.transformTo(32, f)

    def eyebrowWideClose(self, f):
        return self.transformTo(33, f)

    def eyebrowUpLow(self, f):
        return self.transformTo(34, f)

    def eyebrowForwardBackward(self, f):
        return self.transformTo(35, f)

    def chooseNose(self, n):
        return self.selectBaseShape(36, n)

    def noseHScaleoutScalein(self, f):
        return self.transformTo(37, f)

    def noseVScaleoutScalein(self, f):
        return self.transformTo(38, f)

    def noseForwardBackward(self, f):
        return self.transformTo(39, f)

    def noseUpLow(self, f):
        return self.transformTo(40, f)

    def chooseNoseBridge(self, n):
        return self.selectBaseShape(41, n)

    def nosebridgeHScaleoutScalein(self, f):
        return self.transformTo(42, f)

    def nosebridgeHighLow(self, f):
        return self.transformTo(43, f)

    def chooseUpperlipline(self, n):
        return self.selectBaseShape(44, n)

    def chooseLipgroove(self, n):
        return self.selectBaseShape(45, n)

    def chooseLowerlipline(self, n):
        return self.selectBaseShape(46, n)

    def upperlipThickThin(self, f):
        return self.transformTo(47, f)

    def lowerlipThickThin(self, f):
        return self.transformTo(48, f)

    def lipWideClose(self, f):
        return self.transformTo(49, f)

    def lipUpLow(self, f):
        return self.transformTo(50, f)

    def lipForwardBackward(self, f):
        return self.transformTo(51, f)

    def mouthcornerUpLow(self, f):
        return self.transformTo(52, f)

    def chooseEar(self, n):
        return self.selectBaseShape(53, n)

    def earBigSmall(self, f):
        return self.transformTo(54, f)

    def earUpLow(self, f):
        return self.transformTo(55, f)

    def boneModify(self, id, factor):
        self.config[id] = factor
        f = boneModifyFunc.get(id)
        if f:
            f(self.boneScaleInfo, factor)
        else:
            return False
        for i in self.boneScaleInfo:
            v = self.boneScaleInfo[i]
            self.boneScale.setDetailedBoneScale(i, v['scale']['x'], v['scale']['y'], v['scale']['z'], v['trans']['x'], v['trans']['y'], v['trans']['z'])
            self.boneScale.setBoneScale(i, v['boneScale'], v['boneLengthScale'])
            self.boneScale.setBoneRotate(i, v['rot']['x'], v['rot']['y'], v['rot']['z'])

        self.model.boneScale = self.boneScale
        return True
