import socket
import oscom.color as con
from oscom.client import SimpleClient
from oscom.command.base import Command
from osmon.common.interfaces import IMessageResponse


class OpenCommand( Command ):
    def __init__(self, quals ):
        super().__init__( "OPEN", quals )
        return

    @staticmethod
    def help_description():
        return "OPEN <node-address>", "open the session with an OSMON"

    def _do_command( self, session ):
        host = self.quals.pop()
        try:
            socket.gethostbyname( host )
            SimpleClient( host, session.port, IMessageResponse )
            session.host = host
            print( f"{host} opened." )

        except socket.gaierror as exc:
            self.print_error( f"ERROR: { exc }" )

        return

    @staticmethod
    def detail_help( self ):
        return """Open a system node to access the OSMON daemon.
        
Example:

    >OPEN scuzzy.pe2mbs.nl
    scuzzy.pe2mbs.nl opened."""