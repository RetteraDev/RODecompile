#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\gt/gtService.o
from google.protobuf import service
import gtDispatcher
import gtRequest
import socket
from struct import pack, unpack

class gtRpcController(service.RpcController):
    pass


class gtRpcSyncChannel(service.RpcChannel):

    def __init__(self, service_interface_obj, connected_socket = None):
        super(gtRpcSyncChannel, self).__init__()
        self.service_interface_obj = service_interface_obj
        self.rpc_request = gtRequest.request()
        self.rpc_request_parser = gtRequest.request_parser()
        self.buffer_size = 4096
        if connected_socket:
            self._socket = connected_socket
        else:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sync_on = True

    def sync_mode(self, on):
        self.sync_on = on

    def set_buffer(self, size):
        self.buffer_size = size

    def set_socket_buffer(self, recv_buffer_size, send_buffer_size):
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, recv_buffer_size)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, send_buffer_size)

    def set_max_data(self, size):
        self.rpc_request_parser.set_max_data(size)

    def connect(self, address):
        self._socket.connect(address)

    def disconnect(self):
        self._socket.close()
        self._socket = None
        self.rpc_request.reset()
        self.rpc_request_parser.reset()

    def CallMethod(self, method_descriptor, rpc_controller, request, response_class, done):
        cmd_index = method_descriptor.index
        assert cmd_index < 65535
        data = request.SerializeToString()
        total_len = len(data) + 2
        try:
            self._socket.send(pack('<I', total_len))
            self._socket.send(pack('<H', cmd_index))
            self._socket.send(data)
            if self.sync_on:
                self.fetch_result()
        except:
            self.disconnect()
            self.service_interface_obj.on_disconnected()
            raise

    def input_data(self, data):
        total = len(data)
        skip = 0
        while skip < total:
            result, consum = self.rpc_request_parser.parse(self.rpc_request, data, skip)
            assert consum > 0
            skip += consum
            if result == 1:
                ok = self.on_request()
                self.rpc_request.reset()
                if not ok:
                    return 0
                if skip == total:
                    return 1
                continue
            elif result == 0:
                return 0

        return 2

    def on_request(self):
        l = len(self.rpc_request.data)
        if l < 2:
            print 'Got error request size: ', l
            return False
        index_data = self.rpc_request.data[0:2]
        cmd_index = unpack('<H', index_data)[0]
        s_descriptor = self.service_interface_obj.GetDescriptor()
        if cmd_index > len(s_descriptor.methods):
            print 'Got error method index:', cmd_index
            return False
        method = s_descriptor.methods[cmd_index]
        request = self.service_interface_obj.GetRequestClass(method)()
        serialized = self.rpc_request.data[2:]
        request.ParseFromString(serialized)
        self.service_interface_obj.CallMethod(method, None, request, None)
        return True

    def fetch_result(self):
        while 1:
            data = self._socket.recv(self.buffer_size)
            if data:
                rc = self.input_data(data)
                if rc == 2:
                    continue
                else:
                    if rc == 0:
                        self.disconnect()
                        return
                    break


class gtRpcChannel(service.RpcChannel):

    def __init__(self, service_interface_obj, accept_connection = None):
        super(gtRpcChannel, self).__init__()
        self.service_interface_obj = service_interface_obj
        self.rpc_request = gtRequest.request()
        self.rpc_request_parser = gtRequest.request_parser()
        if accept_connection:
            self.dispatcher = gtDispatcher.dispatcher(self, accept_connection=accept_connection)
        else:
            self.dispatcher = None
        self.recv_buffer_size = 0
        self.recv_socket_buffer_size = 0
        self.send_socket_buffer_size = 0

    def set_buffer(self, size):
        self.recv_buffer_size = size
        if self.dispatcher:
            self.dispatcher.set_buffer(size)

    def set_socket_buffer(self, recv_buffer_size, send_buffer_size):
        self.recv_socket_buffer_size = recv_buffer_size
        self.send_socket_buffer_size = send_buffer_size
        if self.dispatcher:
            self.dispatcher.set_socket_buffer(recv_buffer_size, send_buffer_size)

    def set_max_data(self, size):
        self.rpc_request_parser.set_max_data(size)

    def connect(self, address):
        self.dispatcher = gtDispatcher.dispatcher(self)
        try:
            self.dispatcher.connect(address)
        except:
            pass

        if self.recv_buffer_size:
            self.dispatcher.set_buffer(self.recv_buffer_size)
        if self.recv_socket_buffer_size > 0 and self.send_socket_buffer_size > 0:
            self.dispatcher.set_socket_buffer(self.recv_socket_buffer_size, self.send_socket_buffer_size)

    def on_connected(self):
        print 'gtRpcChannel.on_connected'
        if self.service_interface_obj:
            self.service_interface_obj.on_connected()

    def on_disconnected(self):
        print 'gtRpcChannel.on_disconnected'
        if self.service_interface_obj:
            self.service_interface_obj.on_disconnected()
        self.dispatcher = None
        self.rpc_request.reset()
        self.rpc_request_parser.reset()

    def disconnect(self):
        self.dispatcher.disconnect()
        self.dispatcher = None
        self.rpc_request.reset()
        self.rpc_request_parser.reset()

    def CallMethod(self, method_descriptor, rpc_controller, request, response_class, done):
        cmd_index = method_descriptor.index
        assert cmd_index < 65535
        data = request.SerializeToString()
        total_len = len(data) + 2
        self.dispatcher.send_data(pack('<I', total_len))
        self.dispatcher.send_data(pack('<H', cmd_index))
        self.dispatcher.send_data(data)

    def input_data(self, data):
        total = len(data)
        skip = 0
        while skip < total:
            result, consum = self.rpc_request_parser.parse(self.rpc_request, data, skip)
            assert consum > 0
            skip += consum
            if result == 1:
                ok = self.on_request()
                self.rpc_request.reset()
                if not ok:
                    return 0
                continue
            elif result == 0:
                return 0

        return 2

    def on_request(self):
        l = len(self.rpc_request.data)
        if l < 2:
            print 'Got error request size: ', l
            return False
        index_data = self.rpc_request.data[0:2]
        cmd_index = unpack('<H', index_data)[0]
        s_descriptor = self.service_interface_obj.GetDescriptor()
        if cmd_index > len(s_descriptor.methods):
            print 'Got error method index:', cmd_index
            return False
        method = s_descriptor.methods[cmd_index]
        request = self.service_interface_obj.GetRequestClass(method)()
        serialized = self.rpc_request.data[2:]
        request.ParseFromString(serialized)
        self.service_interface_obj.CallMethod(method, None, request, None)
        return True


class gtSSLRpcChannel(gtRpcChannel):

    def __init__(self, certfile, service_interface_obj):
        super(gtSSLRpcChannel, self).__init__(service_interface_obj)
        self.certfile = certfile

    def connect(self, address):
        self.dispatcher = gtDispatcher.dispatcher_ssl(self.certfile, self)
        self.dispatcher.connect(address)

    def on_handshaked(self):
        print 'gtSSLRpcChannelSSL.on_handshaked'
        if self.service_interface_obj:
            self.service_interface_obj.on_handshaked()
