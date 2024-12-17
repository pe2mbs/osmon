from oscom.command.base import Command


class SetCommand(Command):
    """This is an experimental command

    """
    def __init__(self, quals ):
        super().__init__( "SET", quals )
        return

    @staticmethod
    def help_description() -> tuple:
        return "SET <arguments>", "Sets one or more parameters for the specific process"

    def _do_command( self, session ):
        if isinstance( session.program, dict ):
            for idx in range( 1, len( self.quals ) ):
                key, value = self.quals[ idx ]
                session.program[ key.lower() ] = value

        else:
            self.print_error( "Not initialized" )

        return
