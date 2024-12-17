import typing as t
import socket
from osmon.common.json_protocol import JsonProtocol


class SimpleClient( JsonProtocol ):
    def __init__( self, host: str, port: int, return_type: t.Optional[ t.Any ] = str ):
        super().__init__( 2 )
        self._host = host
        self._port = port
        self.__return_type = return_type
        # Create a socket (SOCK_STREAM means a TCP socket)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return

    def sendReceive( self, request, return_type: t.Optional[ t.Any ] = None ) -> t.Any:
        received = None
        try:
            if return_type is None:
                return_type = self.__return_type

            # Connect to server and send data
            self._sock.connect( ( self._host, self._port ) )
            self.serialize( self._sock.send, request )
            received = self.deserialize( self._sock.recv, return_type )

        finally:
            self._sock.close()

        return received
