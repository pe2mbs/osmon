from oscom.command.base import Command
from osmon.common.interfaces import IMessageRequest, IMessageResponse


class ShutdownCommand(Command):
    def __init__(self, quals ):
        super().__init__( "SHUTDOWN", quals )
        return

    @staticmethod
    def help_description() -> tuple:
        return "SHUTDOWN", "Shutdown the OSMON daemon"

    def _do_command( self, session ):
        response = self._do_osmon_request( session, 'shutdown' )
        if isinstance( response, IMessageResponse ):
            if response.status:
                print( "Shutdown in progress" )

            else:
                self.print_warning( response.message )

        return

    @staticmethod
    def detail_help( self ):
        return """Shutdown the OSMON daemon.
        
-   On Linux when a PID file is provided and the processes where started demonized,
    the processes keep running when not demonized processes are killed on shutdown
    of the OSMON daemon.
       
-   On Windows the processes are started detached when a PID file is provided, 
    therefore they shall remain running on OSMON daemon shutdown.
    When no PID is provides the process are are started attached, therefore killed 
    with the OSMON daemon shutdown. 

Example:
    
    >SHUTDOWN
    Shutdown in progress"""