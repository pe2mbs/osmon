from oscom.command.base import Command


class AddCommand( Command ):
    """This is an experimental command

    """
    def __init__(self, quals ):
        super().__init__( "ADD", quals )
        return

    @staticmethod
    def help_description() -> tuple:
        return "ADD <arguments>", "Add a new process with parameters"

    def _do_command( self, session ):
        super()._do_command( session )
        if len( self.quals ) > 1:
            session.program = {
                'name': self.quals[ 1 ]
            }
            for idx in range( 2, len( self.quals ) ):
                key, value = self.quals[ idx ]
                session.program[ key.lower() ] = value

        return
