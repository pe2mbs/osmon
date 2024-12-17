from oscom.command.base import Command


class CloseCommand(Command):
    def __init__(self, quals ):
        super().__init__( "CLOSE", quals )
        return

    @staticmethod
    def help_description() -> tuple:
        return "CLOSE", "Closes the session with the current OSMON"

    def _do_command( self, session ):
        session.host = None
        session.program = None
        print( "Session closed" )
        return

    @staticmethod
    def detail_help( self ):
        return """Close the current opened system node.
        
Example:

    >CLOSE         
    Session closed"""