#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\PIL/ImageMode.o
_modes = {}

class ModeDescriptor:

    def __init__(self, mode, bands, basemode, basetype):
        self.mode = mode
        self.bands = bands
        self.basemode = basemode
        self.basetype = basetype

    def __str__(self):
        return self.mode


def getmode(mode):
    if not _modes:
        import Image
        for m, (basemode, basetype, bands) in Image._MODEINFO.items():
            _modes[m] = ModeDescriptor(m, bands, basemode, basetype)

        _modes['LA'] = ModeDescriptor('LA', ('L', 'A'), 'L', 'L')
        _modes['PA'] = ModeDescriptor('PA', ('P', 'A'), 'RGB', 'L')
        _modes['I;16'] = ModeDescriptor('I;16', 'I', 'L', 'L')
        _modes['I;16L'] = ModeDescriptor('I;16L', 'I', 'L', 'L')
        _modes['I;16B'] = ModeDescriptor('I;16B', 'I', 'L', 'L')
    return _modes[mode]
