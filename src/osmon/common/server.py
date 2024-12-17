import logging
import socketserver
from osmon.common.interfaces import IMessageRequest, IMessageResponse
from osmon.common.json_protocol import JsonProtocol


__all__ = [ 'JsonServer' ]


logger = logging.getLogger( 'osmon.oscom' )


class JsonServer( socketserver.ThreadingMixIn, socketserver.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    def __init__( self, server_address, RequestHandlerClass: socketserver.BaseRequestHandler ):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)
        return
