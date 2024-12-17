from oscom.command.add import AddCommand
from oscom.command.base import Command
from oscom.command.close import CloseCommand
from oscom.command.open import OpenCommand
from oscom.command.quit import QuitCommand
from oscom.command.reload import ReloadCommand
from oscom.command.restart import RestartCommand
from oscom.command.set import SetCommand
from oscom.command.show import ShowCommand
from oscom.command.shutdown import ShutdownCommand
from oscom.command.store import StoreCommand


class HelpCommand( Command ):
    def __init__( self, quals ):
        super().__init__( "HELP", quals )
        return

    @staticmethod
    def help_description() -> tuple:
        return "HELP or ? [ <cmd> ]", "Displays this help message"

    def _do_command( self, session ):
        helpCommands = {
            "OPEN":     OpenCommand,
            "CLOSE":    CloseCommand,
            "RELOAD":   ReloadCommand,
            "RESTART":  RestartCommand,
            "SHUTDOWN": ShutdownCommand,
            "QUIT":     QuitCommand,
            "HELP":     HelpCommand
        }
        if session.experimental:
            helpCommands.update( { "SET": SetCommand,
                                   "ADD": AddCommand,
                                   "STORE": StoreCommand,
                                   "SHOW": ShowCommand } )

        if len( self.quals ) > 1:
            topic = self.quals.pop().upper()
            try:
                print( helpCommands[ topic ].detail_help( self ) )

            except KeyError:
                print( f"{ topic } doesn't exists, did you spell it correct?" )

        else:
            print( "Enter any of the following commands (not case sensitive):" )
            for cmd in helpCommands.values():
                command, description = cmd.help_description()
                print( f"  {command:{self.help_cmd_width}} - {description}" )

        print()
        return

    @staticmethod
    def detail_help():
        return """HELP
----
Without argument the help command gives a help summery of all commands available.

When help is called with a argument, a detail help description is given like this 
 
    >HELP <command>
    ...

"""
