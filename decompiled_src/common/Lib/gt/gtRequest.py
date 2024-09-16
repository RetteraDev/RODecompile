#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\gt/gtRequest.o
from struct import pack, unpack

class request(object):

    def __init__(self):
        super(request, self).__init__()
        self.size = ''
        self.data = ''

    def get_size(self):
        try:
            return unpack('<I', self.size)[0]
        except:
            return -1

    def reset(self):
        self.size = ''
        self.data = ''


class request_parser(object):
    SIZE_BYTES = 4
    ST_SIZE = 0
    ST_DATA = 1
    MAX_DATA_LEN = 16777215

    def __init__(self):
        super(request_parser, self).__init__()
        self.reset()
        self.max_data_len = self.MAX_DATA_LEN

    def set_max_data(self, size):
        self.max_data_len = size

    def reset(self):
        self.status = request_parser.ST_SIZE
        self.need_bytes = request_parser.SIZE_BYTES

    def parse(self, request, data, skip):
        l = len(data) - skip
        if self.status == request_parser.ST_SIZE:
            if self.need_bytes > l:
                request.size += data[skip:]
                self.need_bytes -= l
                return (2, l)
            else:
                request.size += data[skip:skip + self.need_bytes]
                consum = self.need_bytes
                self.status = request_parser.ST_DATA
                data_len = request.get_size()
                if data_len < 1 or data_len > self.max_data_len:
                    return (0, consum)
                self.need_bytes = data_len
                return (2, consum)
        elif self.status == request_parser.ST_DATA:
            if self.need_bytes > l:
                request.data += data[skip:]
                self.need_bytes -= l
                return (2, l)
            else:
                request.data += data[skip:skip + self.need_bytes]
                consum = self.need_bytes
                self.reset()
                return (1, consum)
        else:
            return (0, 0)
