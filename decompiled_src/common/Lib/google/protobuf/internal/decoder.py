#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\google\protobuf\internal/decoder.o
"""Code for decoding protocol buffer primitives.

This code is very similar to encoder.py -- read the docs for that module first.

A "decoder" is a function with the signature:
  Decode(buffer, pos, end, message, field_dict)
The arguments are:
  buffer:     The string containing the encoded message.
  pos:        The current position in the string.
  end:        The position in the string where the current message ends.  May be
              less than len(buffer) if we're reading a sub-message.
  message:    The message object into which we're parsing.
  field_dict: message._fields (avoids a hashtable lookup).
The decoder reads the field and stores it into field_dict, returning the new
buffer position.  A decoder for a repeated field may proactively decode all of
the elements of that field, if they appear consecutively.

Note that decoders may throw any of the following:
  IndexError:  Indicates a truncated message.
  struct.error:  Unpacking of a fixed-width field failed.
  message.DecodeError:  Other errors.

Decoders are expected to raise an exception if they are called with pos > end.
This allows callers to be lax about bounds checking:  it's fineto read past
"end" as long as you are sure that someone else will notice and throw an
exception later on.

Something up the call stack is expected to catch IndexError and struct.error
and convert them to message.DecodeError.

Decoders are constructed using decoder constructors with the signature:
  MakeDecoder(field_number, is_repeated, is_packed, key, new_default)
The arguments are:
  field_number:  The field number of the field we want to decode.
  is_repeated:   Is the field a repeated field? (bool)
  is_packed:     Is the field a packed field? (bool)
  key:           The key to use when looking up the field within field_dict.
                 (This is actually the FieldDescriptor but nothing in this
                 file should depend on that.)
  new_default:   A function which takes a message object as a parameter and
                 returns a new instance of the default value for this field.
                 (This is called for repeated fields and sub-messages, when an
                 instance does not already exist.)

As with encoders, we define a decoder constructor for every type of field.
Then, for every field of every message class we construct an actual decoder.
That decoder goes into a dict indexed by tag, so when we decode a message
we repeatedly read a tag, look up the corresponding decoder, and invoke it.
"""
__author__ = 'kenton@google.com (Kenton Varda)'
import struct
from google.protobuf.internal import encoder
from google.protobuf.internal import wire_format
from google.protobuf import message
_POS_INF = float('inf')
_NEG_INF = -_POS_INF
_NAN = _POS_INF * 0
_DecodeError = message.DecodeError

def _VarintDecoder(mask):
    """Return an encoder for a basic varint value (does not include tag).
    
    Decoded values will be bitwise-anded with the given mask before being
    returned, e.g. to limit them to 32 bits.  The returned decoder does not
    take the usual "end" parameter -- the caller is expected to do bounds checking
    after the fact (often the caller can defer such checking until later).  The
    decoder returns a (value, new_pos) pair.
    """
    local_ord = ord

    def DecodeVarint(buffer, pos):
        result = 0
        shift = 0
        while 1:
            b = local_ord(buffer[pos])
            result |= (b & 127) << shift
            pos += 1
            if not b & 128:
                result &= mask
                return (result, pos)
            shift += 7
            if shift >= 64:
                raise _DecodeError('Too many bytes when decoding varint.')

    return DecodeVarint


def _SignedVarintDecoder(mask):
    """Like _VarintDecoder() but decodes signed values."""
    local_ord = ord

    def DecodeVarint(buffer, pos):
        result = 0
        shift = 0
        while 1:
            b = local_ord(buffer[pos])
            result |= (b & 127) << shift
            pos += 1
            if not b & 128:
                if result > 9223372036854775807L:
                    result -= 18446744073709551616L
                    result |= ~mask
                else:
                    result &= mask
                return (result, pos)
            shift += 7
            if shift >= 64:
                raise _DecodeError('Too many bytes when decoding varint.')

    return DecodeVarint


_DecodeVarint = _VarintDecoder(18446744073709551615L)
_DecodeSignedVarint = _SignedVarintDecoder(18446744073709551615L)
_DecodeVarint32 = _VarintDecoder(4294967295L)
_DecodeSignedVarint32 = _SignedVarintDecoder(4294967295L)

def ReadTag(buffer, pos):
    """Read a tag from the buffer, and return a (tag_bytes, new_pos) tuple.
    
    We return the raw bytes of the tag rather than decoding them.  The raw
    bytes can then be used to look up the proper decoder.  This effectively allows
    us to trade some work that would be done in pure-python (decoding a varint)
    for work that is done in C (searching for a byte string in a hash table).
    In a low-level language it would be much cheaper to decode the varint and
    use that, but not in Python.
    """
    start = pos
    while ord(buffer[pos]) & 128:
        pos += 1

    pos += 1
    return (buffer[start:pos], pos)


def _SimpleDecoder(wire_type, decode_value):
    """Return a constructor for a decoder for fields of a particular type.
    
    Args:
        wire_type:  The field's wire type.
        decode_value:  A function which decodes an individual value, e.g.
          _DecodeVarint()
    """

    def SpecificDecoder(field_number, is_repeated, is_packed, key, new_default):
        if is_packed:
            local_DecodeVarint = _DecodeVarint

            def DecodePackedField(buffer, pos, end, message, field_dict):
                value = field_dict.get(key)
                if value is None:
                    value = field_dict.setdefault(key, new_default(message))
                endpoint, pos = local_DecodeVarint(buffer, pos)
                endpoint += pos
                if endpoint > end:
                    raise _DecodeError('Truncated message.')
                while pos < endpoint:
                    element, pos = decode_value(buffer, pos)
                    value.append(element)

                if pos > endpoint:
                    del value[-1]
                    raise _DecodeError('Packed element was truncated.')
                return pos

            return DecodePackedField
        elif is_repeated:
            tag_bytes = encoder.TagBytes(field_number, wire_type)
            tag_len = len(tag_bytes)

            def DecodeRepeatedField(buffer, pos, end, message, field_dict):
                value = field_dict.get(key)
                if value is None:
                    value = field_dict.setdefault(key, new_default(message))
                while 1:
                    element, new_pos = decode_value(buffer, pos)
                    value.append(element)
                    pos = new_pos + tag_len
                    if buffer[new_pos:pos] != tag_bytes or new_pos >= end:
                        if new_pos > end:
                            raise _DecodeError('Truncated message.')
                        return new_pos

            return DecodeRepeatedField
        else:

            def DecodeField(buffer, pos, end, message, field_dict):
                field_dict[key], pos = decode_value(buffer, pos)
                if pos > end:
                    del field_dict[key]
                    raise _DecodeError('Truncated message.')
                return pos

            return DecodeField

    return SpecificDecoder


def _ModifiedDecoder(wire_type, decode_value, modify_value):
    """Like SimpleDecoder but additionally invokes modify_value on every value
    before storing it.  Usually modify_value is ZigZagDecode.
    """

    def InnerDecode(buffer, pos):
        result, new_pos = decode_value(buffer, pos)
        return (modify_value(result), new_pos)

    return _SimpleDecoder(wire_type, InnerDecode)


def _StructPackDecoder(wire_type, format):
    """Return a constructor for a decoder for a fixed-width field.
    
    Args:
        wire_type:  The field's wire type.
        format:  The format string to pass to struct.unpack().
    """
    value_size = struct.calcsize(format)
    local_unpack = struct.unpack

    def InnerDecode(buffer, pos):
        new_pos = pos + value_size
        result = local_unpack(format, buffer[pos:new_pos])[0]
        return (result, new_pos)

    return _SimpleDecoder(wire_type, InnerDecode)


def _FloatDecoder():
    """Returns a decoder for a float field.
    
    This code works around a bug in struct.unpack for non-finite 32-bit
    floating-point values.
    """
    local_unpack = struct.unpack

    def InnerDecode(buffer, pos):
        new_pos = pos + 4
        float_bytes = buffer[pos:new_pos]
        if float_bytes[3] in '�' and float_bytes[2] >= '�':
            if float_bytes[0:3] != '  �':
                return (_NAN, new_pos)
            if float_bytes[3] == '�':
                return (_NEG_INF, new_pos)
            return (_POS_INF, new_pos)
        result = local_unpack('<f', float_bytes)[0]
        return (result, new_pos)

    return _SimpleDecoder(wire_format.WIRETYPE_FIXED32, InnerDecode)


def _DoubleDecoder():
    """Returns a decoder for a double field.
    
    This code works around a bug in struct.unpack for not-a-number.
    """
    local_unpack = struct.unpack

    def InnerDecode(buffer, pos):
        new_pos = pos + 8
        double_bytes = buffer[pos:new_pos]
        if double_bytes[7] in '�' and double_bytes[6] >= '�' and double_bytes[0:7] != '      �':
            return (_NAN, new_pos)
        result = local_unpack('<d', double_bytes)[0]
        return (result, new_pos)

    return _SimpleDecoder(wire_format.WIRETYPE_FIXED64, InnerDecode)


Int32Decoder = EnumDecoder = _SimpleDecoder(wire_format.WIRETYPE_VARINT, _DecodeSignedVarint32)
Int64Decoder = _SimpleDecoder(wire_format.WIRETYPE_VARINT, _DecodeSignedVarint)
UInt32Decoder = _SimpleDecoder(wire_format.WIRETYPE_VARINT, _DecodeVarint32)
UInt64Decoder = _SimpleDecoder(wire_format.WIRETYPE_VARINT, _DecodeVarint)
SInt32Decoder = _ModifiedDecoder(wire_format.WIRETYPE_VARINT, _DecodeVarint32, wire_format.ZigZagDecode)
SInt64Decoder = _ModifiedDecoder(wire_format.WIRETYPE_VARINT, _DecodeVarint, wire_format.ZigZagDecode)
Fixed32Decoder = _StructPackDecoder(wire_format.WIRETYPE_FIXED32, '<I')
Fixed64Decoder = _StructPackDecoder(wire_format.WIRETYPE_FIXED64, '<Q')
SFixed32Decoder = _StructPackDecoder(wire_format.WIRETYPE_FIXED32, '<i')
SFixed64Decoder = _StructPackDecoder(wire_format.WIRETYPE_FIXED64, '<q')
FloatDecoder = _FloatDecoder()
DoubleDecoder = _DoubleDecoder()
BoolDecoder = _ModifiedDecoder(wire_format.WIRETYPE_VARINT, _DecodeVarint, bool)

def StringDecoder(field_number, is_repeated, is_packed, key, new_default):
    """Returns a decoder for a string field."""
    local_DecodeVarint = _DecodeVarint
    assert not is_packed
    if is_repeated:
        tag_bytes = encoder.TagBytes(field_number, wire_format.WIRETYPE_LENGTH_DELIMITED)
        tag_len = len(tag_bytes)

        def DecodeRepeatedField(buffer, pos, end, message, field_dict):
            value = field_dict.get(key)
            if value is None:
                value = field_dict.setdefault(key, new_default(message))
            while 1:
                size, pos = local_DecodeVarint(buffer, pos)
                new_pos = pos + size
                if new_pos > end:
                    raise _DecodeError('Truncated string.')
                value.append(buffer[pos:new_pos])
                pos = new_pos + tag_len
                if buffer[new_pos:pos] != tag_bytes or new_pos == end:
                    return new_pos

        return DecodeRepeatedField
    else:

        def DecodeField(buffer, pos, end, message, field_dict):
            size, pos = local_DecodeVarint(buffer, pos)
            new_pos = pos + size
            if new_pos > end:
                raise _DecodeError('Truncated string.')
            field_dict[key] = buffer[pos:new_pos]
            return new_pos

        return DecodeField


def BytesDecoder(field_number, is_repeated, is_packed, key, new_default):
    """Returns a decoder for a bytes field."""
    local_DecodeVarint = _DecodeVarint
    assert not is_packed
    if is_repeated:
        tag_bytes = encoder.TagBytes(field_number, wire_format.WIRETYPE_LENGTH_DELIMITED)
        tag_len = len(tag_bytes)

        def DecodeRepeatedField(buffer, pos, end, message, field_dict):
            value = field_dict.get(key)
            if value is None:
                value = field_dict.setdefault(key, new_default(message))
            while 1:
                size, pos = local_DecodeVarint(buffer, pos)
                new_pos = pos + size
                if new_pos > end:
                    raise _DecodeError('Truncated string.')
                value.append(buffer[pos:new_pos])
                pos = new_pos + tag_len
                if buffer[new_pos:pos] != tag_bytes or new_pos == end:
                    return new_pos

        return DecodeRepeatedField
    else:

        def DecodeField(buffer, pos, end, message, field_dict):
            size, pos = local_DecodeVarint(buffer, pos)
            new_pos = pos + size
            if new_pos > end:
                raise _DecodeError('Truncated string.')
            field_dict[key] = buffer[pos:new_pos]
            return new_pos

        return DecodeField


def GroupDecoder(field_number, is_repeated, is_packed, key, new_default):
    """Returns a decoder for a group field."""
    end_tag_bytes = encoder.TagBytes(field_number, wire_format.WIRETYPE_END_GROUP)
    end_tag_len = len(end_tag_bytes)
    assert not is_packed
    if is_repeated:
        tag_bytes = encoder.TagBytes(field_number, wire_format.WIRETYPE_START_GROUP)
        tag_len = len(tag_bytes)

        def DecodeRepeatedField(buffer, pos, end, message, field_dict):
            value = field_dict.get(key)
            if value is None:
                value = field_dict.setdefault(key, new_default(message))
            while 1:
                value = field_dict.get(key)
                if value is None:
                    value = field_dict.setdefault(key, new_default(message))
                pos = value.add()._InternalParse(buffer, pos, end)
                new_pos = pos + end_tag_len
                if buffer[pos:new_pos] != end_tag_bytes or new_pos > end:
                    raise _DecodeError('Missing group end tag.')
                pos = new_pos + tag_len
                if buffer[new_pos:pos] != tag_bytes or new_pos == end:
                    return new_pos

        return DecodeRepeatedField
    else:

        def DecodeField(buffer, pos, end, message, field_dict):
            value = field_dict.get(key)
            if value is None:
                value = field_dict.setdefault(key, new_default(message))
            pos = value._InternalParse(buffer, pos, end)
            new_pos = pos + end_tag_len
            if buffer[pos:new_pos] != end_tag_bytes or new_pos > end:
                raise _DecodeError('Missing group end tag.')
            return new_pos

        return DecodeField


def MessageDecoder(field_number, is_repeated, is_packed, key, new_default):
    """Returns a decoder for a message field."""
    local_DecodeVarint = _DecodeVarint
    assert not is_packed
    if is_repeated:
        tag_bytes = encoder.TagBytes(field_number, wire_format.WIRETYPE_LENGTH_DELIMITED)
        tag_len = len(tag_bytes)

        def DecodeRepeatedField(buffer, pos, end, message, field_dict):
            value = field_dict.get(key)
            if value is None:
                value = field_dict.setdefault(key, new_default(message))
            while 1:
                value = field_dict.get(key)
                if value is None:
                    value = field_dict.setdefault(key, new_default(message))
                size, pos = local_DecodeVarint(buffer, pos)
                new_pos = pos + size
                if new_pos > end:
                    raise _DecodeError('Truncated message.')
                if value.add()._InternalParse(buffer, pos, new_pos) != new_pos:
                    raise _DecodeError('Unexpected end-group tag.')
                pos = new_pos + tag_len
                if buffer[new_pos:pos] != tag_bytes or new_pos == end:
                    return new_pos

        return DecodeRepeatedField
    else:

        def DecodeField(buffer, pos, end, message, field_dict):
            value = field_dict.get(key)
            if value is None:
                value = field_dict.setdefault(key, new_default(message))
            size, pos = local_DecodeVarint(buffer, pos)
            new_pos = pos + size
            if new_pos > end:
                raise _DecodeError('Truncated message.')
            if value._InternalParse(buffer, pos, new_pos) != new_pos:
                raise _DecodeError('Unexpected end-group tag.')
            return new_pos

        return DecodeField


MESSAGE_SET_ITEM_TAG = encoder.TagBytes(1, wire_format.WIRETYPE_START_GROUP)

def MessageSetItemDecoder(extensions_by_number):
    """Returns a decoder for a MessageSet item.
    
    The parameter is the _extensions_by_number map for the message class.
    
    The message set message looks like this:
      message MessageSet {
        repeated group Item = 1 {
          required int32 type_id = 2;
          required string message = 3;
        }
      }
    """
    type_id_tag_bytes = encoder.TagBytes(2, wire_format.WIRETYPE_VARINT)
    message_tag_bytes = encoder.TagBytes(3, wire_format.WIRETYPE_LENGTH_DELIMITED)
    item_end_tag_bytes = encoder.TagBytes(1, wire_format.WIRETYPE_END_GROUP)
    local_ReadTag = ReadTag
    local_DecodeVarint = _DecodeVarint
    local_SkipField = SkipField

    def DecodeItem(buffer, pos, end, message, field_dict):
        message_set_item_start = pos
        type_id = -1
        message_start = -1
        message_end = -1
        while 1:
            tag_bytes, pos = local_ReadTag(buffer, pos)
            if tag_bytes == type_id_tag_bytes:
                type_id, pos = local_DecodeVarint(buffer, pos)
            elif tag_bytes == message_tag_bytes:
                size, message_start = local_DecodeVarint(buffer, pos)
                pos = message_end = message_start + size
            elif tag_bytes == item_end_tag_bytes:
                break
            else:
                pos = SkipField(buffer, pos, end, tag_bytes)
                if pos == -1:
                    raise _DecodeError('Missing group end tag.')

        if pos > end:
            raise _DecodeError('Truncated message.')
        if type_id == -1:
            raise _DecodeError('MessageSet item missing type_id.')
        if message_start == -1:
            raise _DecodeError('MessageSet item missing message.')
        extension = extensions_by_number.get(type_id)
        if extension is not None:
            value = field_dict.get(extension)
            if value is None:
                value = field_dict.setdefault(extension, extension.message_type._concrete_class())
            if value._InternalParse(buffer, message_start, message_end) != message_end:
                raise _DecodeError('Unexpected end-group tag.')
        else:
            if not message._unknown_fields:
                message._unknown_fields = []
            message._unknown_fields.append((MESSAGE_SET_ITEM_TAG, buffer[message_set_item_start:pos]))
        return pos

    return DecodeItem


def _SkipVarint(buffer, pos, end):
    """Skip a varint value.  Returns the new position."""
    while ord(buffer[pos]) & 128:
        pos += 1

    pos += 1
    if pos > end:
        raise _DecodeError('Truncated message.')
    return pos


def _SkipFixed64(buffer, pos, end):
    """Skip a fixed64 value.  Returns the new position."""
    pos += 8
    if pos > end:
        raise _DecodeError('Truncated message.')
    return pos


def _SkipLengthDelimited(buffer, pos, end):
    """Skip a length-delimited value.  Returns the new position."""
    size, pos = _DecodeVarint(buffer, pos)
    pos += size
    if pos > end:
        raise _DecodeError('Truncated message.')
    return pos


def _SkipGroup(buffer, pos, end):
    """Skip sub-group.  Returns the new position."""
    while 1:
        tag_bytes, pos = ReadTag(buffer, pos)
        new_pos = SkipField(buffer, pos, end, tag_bytes)
        if new_pos == -1:
            return pos
        pos = new_pos


def _EndGroup(buffer, pos, end):
    """Skipping an END_GROUP tag returns -1 to tell the parent loop to break."""
    return -1


def _SkipFixed32(buffer, pos, end):
    """Skip a fixed32 value.  Returns the new position."""
    pos += 4
    if pos > end:
        raise _DecodeError('Truncated message.')
    return pos


def _RaiseInvalidWireType(buffer, pos, end):
    """Skip function for unknown wire types.  Raises an exception."""
    raise _DecodeError('Tag had invalid wire type.')


def _FieldSkipper():
    """Constructs the SkipField function."""
    WIRETYPE_TO_SKIPPER = [_SkipVarint,
     _SkipFixed64,
     _SkipLengthDelimited,
     _SkipGroup,
     _EndGroup,
     _SkipFixed32,
     _RaiseInvalidWireType,
     _RaiseInvalidWireType]
    wiretype_mask = wire_format.TAG_TYPE_MASK
    local_ord = ord

    def SkipField(buffer, pos, end, tag_bytes):
        """Skips a field with the specified tag.
        
        |pos| should point to the byte immediately after the tag.
        
        Returns:
            The new position (after the tag value), or -1 if the tag is an end-group
            tag (in which case the calling loop should break).
        """
        wire_type = local_ord(tag_bytes[0]) & wiretype_mask
        return WIRETYPE_TO_SKIPPER[wire_type](buffer, pos, end)

    return SkipField


SkipField = _FieldSkipper()
