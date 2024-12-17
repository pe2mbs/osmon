from oscom.command.base import Command
import oscom.color as con


class ShowCommand( Command ):
    """This is an experimental command

    """
    def __init__(self, quals ):
        super().__init__( "SHOW", quals )
        return

    @staticmethod
    def help_description() -> tuple:
        return "SHOW <proces-name>", "shows the current status of the processes, a specific process"

    def _do_command( self, session ):
        if isinstance( session.program, dict ):
            print( f"data: { session.program }" )

        else:
            self.print_warning( "Use SET command to setup a new program, for more help: HELP ADD" )

        return
