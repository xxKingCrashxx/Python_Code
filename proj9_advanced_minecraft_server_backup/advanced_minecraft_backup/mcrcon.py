import socket

RCON_MESSAGE_TYPE = {
    'SERVERDATA_AUTH': 3,
    'SERVERDATA_AUTH_RESPONSE': 2,
    'SERVERDATA_EXECOMMAND': 2,
    'SERVERDATA_RESPONSE_VALUE': 0
}

class RconPacket:
    def __init__(self, id, type, body, size=10):
        self.__size = size
        
        self.__id = id
        self.__type = type
        self.__body = body

    # converts the RconPacket object into a byte stream that can be sent
    # over the network. Converts everything to little endian
    def to_bytes_stream(self):
        body_bytes = self.__body.encode('utf-8') + b'\x00'
        packet = (
            self.__id.to_bytes(4, byteorder="little") +
            self.__type.to_bytes(4, byteorder="little") +
            body_bytes + b"\x00"
        )
        size = len(packet)
        self.__size = size
        return size.to_bytes(4, byteorder="little") + packet
    
    @staticmethod
    def from_bytes_stream(rcon_packet_bytes_stream):
        size = int.from_bytes(rcon_packet_bytes_stream[0:4], byteorder='little')
        id = int.from_bytes(rcon_packet_bytes_stream[4:8], byteorder="little")
        type = int.from_bytes(rcon_packet_bytes_stream[8:12], byteorder="little")
        body = rcon_packet_bytes_stream[12: -2].decode("utf-8")

        return RconPacket(id, type, body, size=size) 
    
class MCRcon:
    def __init__(self, server_ip, rcon_passwd, rcon_port=25575, ):
        self.__server_ip = server_ip
        self.__rcon_passwd = rcon_passwd
        self.__rcon_port = rcon_port
        self.__sock = None
        self.__req_num = 0

    def send_command(self, command_string):
        self.__req_num += 1
        command_packet = RconPacket(self.__req_num, 
                                    RCON_MESSAGE_TYPE["SERVERDATA_EXECOMMAND"],
                                    command_string)
        self.__send_packet(command_packet)
        response = self.__recv_packet()
        return response

    def connect(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.connect((self.__server_ip, self.__rcon_port))
        self.__login()

    def close_connection(self):
        if self.__sock:
            self.__sock.close()
            self.__sock = None

    def __login(self):
        self.__req_num += 1
        login_packet = RconPacket(
            self.__req_num,
            RCON_MESSAGE_TYPE["SERVERDATA_AUTH"],
            self.__rcon_passwd
        )
        self.__send_packet(login_packet)

    def __recv_packet(self, ):
       def recv_exact(num_bytes):
        data = b""
        while len(data) < num_bytes:
            chunk = self.__sock.recv(num_bytes - len(data))
            if not chunk:
                raise ConnectionError("Connection closed while receiving data")
            data += chunk
        return data
       
       size_bytes = recv_exact(4)
       size = int.from_bytes(size_bytes, byteorder="little")
       packet_data = recv_exact(size)
       full_data = size_bytes + packet_data

       return RconPacket.from_bytes_stream(full_data)

    def __send_packet(self, rcon_packet):
        stream = rcon_packet.to_bytes_stream()
        self.__sock.sendall(stream)
