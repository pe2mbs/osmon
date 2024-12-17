from oscom.command.base import Command
from osmon.common.interfaces import IMessageRequest, IMessageResponse


class RestartCommand(Command):
    def __init__(self, quals ):
        super().__init__( "RESTART", quals )
        return

    @staticmethod
    def help_description() -> tuple:
        return "RESTART", "Restart the OSMON daemon"

    def _do_command( self, session ):
        response = self._do_osmon_request( session, 'restart' )
        if isinstance( response, IMessageResponse ):
            if response.status:
                print( "Restart in progress" )

            else:
                self.print_warning( response.message )

        return

    @staticmethod
    def detail_help( self ):
        return """Restart the OSMON daemon.

-   On Linux when the processes are started daemonized the OSMON daemon shall 
    automatically read the PID file of the process and monitor the process.
    When the process is not daemonized the process is killed and restarted with
    the OSMON damon.
    
-   On Windows when a PID file is provided for a process the process keeps running 
    on the restart of the OSMON daemon. A process that have not a PID file is
    killed with the OSMON daemon, and restarted.
    
Example:

    > RESTART
    Restart in progress"""
