#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\google\protobuf/message_factory.o
"""Provides a factory class for generating dynamic messages."""
__author__ = 'matthewtoia@google.com (Matt Toia)'
from google.protobuf import descriptor_database
from google.protobuf import descriptor_pool
from google.protobuf import message
from google.protobuf import reflection

class MessageFactory(object):
    """Factory for creating Proto2 messages from descriptors in a pool."""

    def __init__(self):
        """Initializes a new factory."""
        self._classes = {}

    def GetPrototype(self, descriptor):
        """Builds a proto2 message class based on the passed in descriptor.
        
        Passing a descriptor with a fully qualified name matching a previous
        invocation will cause the same class to be returned.
        
        Args:
          descriptor: The descriptor to build from.
        
        Returns:
          A class describing the passed in descriptor.
        """
        if descriptor.full_name not in self._classes:
            result_class = reflection.GeneratedProtocolMessageType(descriptor.name.encode('ascii', 'ignore'), (message.Message,), {'DESCRIPTOR': descriptor})
            self._classes[descriptor.full_name] = result_class
            for field in descriptor.fields:
                if field.message_type:
                    self.GetPrototype(field.message_type)

        return self._classes[descriptor.full_name]


_DB = descriptor_database.DescriptorDatabase()
_POOL = descriptor_pool.DescriptorPool(_DB)
_FACTORY = MessageFactory()

def GetMessages(file_protos):
    """Builds a dictionary of all the messages available in a set of files.
    
    Args:
      file_protos: A sequence of file protos to build messages out of.
    
    Returns:
      A dictionary containing all the message types in the files mapping the
      fully qualified name to a Message subclass for the descriptor.
    """
    result = {}
    for file_proto in file_protos:
        _DB.Add(file_proto)

    for file_proto in file_protos:
        for desc in _GetAllDescriptors(file_proto.message_type, file_proto.package):
            result[desc.full_name] = _FACTORY.GetPrototype(desc)

    return result


def _GetAllDescriptors(desc_protos, package):
    """Gets all levels of nested message types as a flattened list of descriptors.
    
    Args:
      desc_protos: The descriptor protos to process.
      package: The package where the protos are defined.
    
    Yields:
      Each message descriptor for each nested type.
    """
    for desc_proto in desc_protos:
        name = '.'.join((package, desc_proto.name))
        yield _POOL.FindMessageTypeByName(name)
        for nested_desc in _GetAllDescriptors(desc_proto.nested_type, name):
            yield nested_desc
