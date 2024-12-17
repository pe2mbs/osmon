from oscom.command.base import Command


class QuitCommand(Command):
    def __init__(self, quals):
        super().__init__( "QUIT", quals )

    @staticmethod
    def help_description() -> tuple:
        return "QUIT or EXIT", "Ends the program"

    def _do_command(self, session):
        session.running = False
        return
