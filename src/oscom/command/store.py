from oscom.command.base import Command


class StoreCommand(Command):
    """This is an experimental command

    """
    def __init__(self, quals ):
        super().__init__( "STORE", quals )
        return

    @staticmethod
    def help_description():
        return "STORE", "Stores the changes into OSMON daemon."

    # def _do_command( self, session ):
    #     return
