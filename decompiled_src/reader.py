#Embedded file name: /WORKSPACE/data/entities/common/lib/yaml/reader.o
__all__ = ['Reader', 'ReaderError']
from error import YAMLError, Mark
import codecs, re, sys
has_ucs4 = sys.maxunicode > 65535

class ReaderError(YAMLError):

    def __init__(self, name, position, character, encoding, reason):
        self.name = name
        self.character = character
        self.position = position
        self.encoding = encoding
        self.reason = reason

    def __str__(self):
        if isinstance(self.character, str):
            return "\'%s\' codec can\'t decode byte #x%02x: %s\n  in \"%s\", position %d" % (self.encoding,
             ord(self.character),
             self.reason,
             self.name,
             self.position)
        else:
            return 'unacceptable character #x%04x: %s\n  in \"%s\", position %d' % (self.character,
             self.reason,
             self.name,
             self.position)


class Reader(object):

    def __init__(self, stream):
        self.name = None
        self.stream = None
        self.stream_pointer = 0
        self.eof = True
        self.buffer = ''
        self.pointer = 0
        self.raw_buffer = None
        self.raw_decode = None
        self.encoding = None
        self.index = 0
        self.line = 0
        self.column = 0
        if isinstance(stream, unicode):
            self.name = '<unicode string>'
            self.check_printable(stream)
            self.buffer = stream + ' '
        elif isinstance(stream, str):
            self.name = '<string>'
            self.raw_buffer = stream
            self.determine_encoding()
        else:
            self.stream = stream
            self.name = getattr(stream, 'name', '<file>')
            self.eof = False
            self.raw_buffer = ''
            self.determine_encoding()

    def peek(self, index = 0):
        try:
            return self.buffer[self.pointer + index]
        except IndexError:
            self.update(index + 1)
            return self.buffer[self.pointer + index]

    def prefix(self, length = 1):
        if self.pointer + length >= len(self.buffer):
            self.update(length)
        return self.buffer[self.pointer:self.pointer + length]

    def forward(self, length = 1):
        if self.pointer + length + 1 >= len(self.buffer):
            self.update(length + 1)
        while length:
            ch = self.buffer[self.pointer]
            self.pointer += 1
            self.index += 1
            if ch in '\n  ' or ch == '\r' and self.buffer[self.pointer] != '\n':
                self.line += 1
                self.column = 0
            elif ch != '﻿':
                self.column += 1
            length -= 1

    def get_mark(self):
        if self.stream is None:
            return Mark(self.name, self.index, self.line, self.column, self.buffer, self.pointer)
        else:
            return Mark(self.name, self.index, self.line, self.column, None, None)

    def determine_encoding(self):
        while not self.eof and len(self.raw_buffer) < 2:
            self.update_raw()

        if not isinstance(self.raw_buffer, unicode):
            if self.raw_buffer.startswith(codecs.BOM_UTF16_LE):
                self.raw_decode = codecs.utf_16_le_decode
                self.encoding = 'utf-16-le'
            elif self.raw_buffer.startswith(codecs.BOM_UTF16_BE):
                self.raw_decode = codecs.utf_16_be_decode
                self.encoding = 'utf-16-be'
            else:
                self.raw_decode = codecs.utf_8_decode
                self.encoding = 'utf-8'
        self.update(1)

    if has_ucs4:
        NON_PRINTABLE = re.compile('[^	\n\r -~ -퟿-�𐀀-􏿿]')
    else:
        NON_PRINTABLE = re.compile('[^	\n\r -~ -퟿-�]')

    def check_printable(self, data):
        match = self.NON_PRINTABLE.search(data)
        if match:
            character = match.group()
            position = self.index + (len(self.buffer) - self.pointer) + match.start()
            raise ReaderError(self.name, position, ord(character), 'unicode', 'special characters are not allowed')

    def update(self, length):
        if self.raw_buffer is None:
            return
        self.buffer = self.buffer[self.pointer:]
        self.pointer = 0
        while len(self.buffer) < length:
            if not self.eof:
                self.update_raw()
            if self.raw_decode is not None:
                try:
                    data, converted = self.raw_decode(self.raw_buffer, 'strict', self.eof)
                except UnicodeDecodeError as exc:
                    character = exc.object[exc.start]
                    if self.stream is not None:
                        position = self.stream_pointer - len(self.raw_buffer) + exc.start
                    else:
                        position = exc.start
                    raise ReaderError(self.name, position, character, exc.encoding, exc.reason)

            else:
                data = self.raw_buffer
                converted = len(data)
            self.check_printable(data)
            self.buffer += data
            self.raw_buffer = self.raw_buffer[converted:]
            if self.eof:
                self.buffer += ' '
                self.raw_buffer = None
                break

    def update_raw(self, size = 1024):
        data = self.stream.read(size)
        if data:
            self.raw_buffer += data
            self.stream_pointer += len(data)
        else:
            self.eof = True
