#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\google\protobuf\internal/api_implementation.o
"""
This module is the central entity that determines which implementation of the
API is used.
"""
__author__ = 'petar@google.com (Petar Petrov)'
import os
_implementation_type = os.getenv('PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION', None)
if not _implementation_type:
    _implementation_type = 'cpp'
if _implementation_type != 'python':
    try:
        import BigWorld
        if BigWorld.component == 'client':
            BigWorld.protoCpp
        from google.protobuf.internal import cpp_message
        _implementation_type = 'cpp'
        print 'protobuffer use cpp implementation!'
    except ImportError as e:
        _implementation_type = 'python'
        print 'protobuffer use python implementation!'
    except AttributeError as e:
        _implementation_type = 'python'
        print 'protobuffer use python implementation1!'

else:
    print 'protobuffer use python implementation!'
_implementation_version_str = os.getenv('PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION_VERSION', '1')
if _implementation_version_str not in ('1', '2'):
    raise ValueError("unsupported PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION_VERSION: \'" + _implementation_version_str + "\' (supported versions: 1, 2)")
_implementation_version = int(_implementation_version_str)

def Type():
    return _implementation_type


def Version():
    return _implementation_version
