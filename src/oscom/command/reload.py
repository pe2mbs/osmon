from oscom.command.base import Command
import oscom.color as con
from osmon.common.interfaces import IMessageRequest, IMessageResponse


class ReloadCommand(Command):
    def __init__(self, quals ):
        super().__init__( "RELOAD", quals )
        return

    @staticmethod
    def help_description() -> tuple:
        return "RELOAD", "Reload the configuration from the stored configuration file."

    def _do_command( self, session ):
        response = self._do_osmon_request( session, 'reload' )
        if isinstance( response, IMessageResponse ):
            if response.status:
                print( "Reload in progress" )

            else:
                self.print_warning( response.message )

        return

    @staticmethod
    def detail_help( self ):
        return """Reload the OSMON daemon.

On the reload of the OSMON daemon, the configuration is re-read and the process that 
where already running are monitored again. New processes are started and monitored.

{0}Note: when a process is removed from the configuration the process and it daemonized
      is NOT killed, this needs to be done manually.{1}     

Example:

    > RESTART
    Restart in progress""".format( con.FG_YELLOW_LIGHT, con.FG_WHITE )
