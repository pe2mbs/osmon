import getopt
import sys
import oscom.color as con
import pyparsing as pp
import random
from oscom.command import ( OpenCommand, CloseCommand, QuitCommand, HelpCommand, ShutdownCommand,
                            RestartCommand, ReloadCommand, AddCommand, SetCommand, ShowCommand,
                            StoreCommand )
from oscom.command.status import StatusCommand
from oscom.prompt import Prompt


__version__ = '1.0.0'
__date__    = '15 December 2024'

class Parser( object ):
    def __init__( self, experimental: bool = False ):
        self.__experimental = experimental
        self.bnf = self.make_bnf()

        return

    def make_bnf( self ):
        openVerb            = pp.one_of( "OPEN", caseless = True )
        closeVerb           = pp.one_of( "CLOSE", caseless = True )
        quitVerb            = pp.one_of( "QUIT EXIT", caseless = True )
        helpVerb            = pp.one_of( "HELP ?", caseless = True )
        shutdownVerb        = pp.one_of( "SHUTDOWN", caseless = True )
        restartVerb         = pp.one_of( "RESTART", caseless = True )
        reloadVerb          = pp.one_of( "RELOAD", caseless = True )
        statusVerb          = pp.one_of( "STATUS", caseless = True )
        addVerb             = pp.one_of( "ADD", caseless = True )
        setVerb             = pp.one_of( "SET", caseless = True )
        showVerb            = pp.one_of( "SHOW", caseless = True )
        storeVerb           = pp.one_of( "STORE", caseless = True )
        detailsVerb         = pp.one_of( "DETAILS", caseless = True )
        processVerb         = pp.one_of( "PROCESS", caseless = True )
        pidfileVerb         = pp.one_of( "PID PIDFILE", caseless = True )
        cwdVerb             = pp.one_of( "CWD WORKING-DIRECTORY", caseless = True )
        userVerb            = pp.one_of( "USER", caseless = True )
        groupVerb           = pp.one_of( "GROUP", caseless = True )
        delayVerb           = pp.one_of( "DELAY", caseless = True )
        secsVerb            = pp.one_of( "SECS SECONDS", caseless = True )
        minsVerb            = pp.one_of( "MINS MINUTES", caseless = True )
        argumentsVerb       = pp.one_of( 'ARGUMENTS', caseless = True )
        environmentVerb     = pp.one_of( 'ENV ENVIRON ENVIRONMENT', caseless = True )
        dnsReference        = pp.Word( pp.alphas + '.', pp.alphanums + '.' )
        nameReference       = pp.Word( pp.alphas + '_-',  pp.alphanums + '_-' )
        if sys.platform == 'linux':
            filePathReference   = pp.Word( pp.alphanums + '_-+/.,~' )

        else:
            filePathReference = pp.Word( pp.alphanums + '_-+\\.,:~' )

        #
        #   OPEN <node-address>
        #
        openCommand         = openVerb  + dnsReference( "dns" )
        openCommand.set_parse_action( OpenCommand )
        #
        #   CLOSE
        #
        closeCommand        = closeVerb
        closeCommand.set_parse_action( CloseCommand )
        #
        #   QUIT | EXIT
        #
        quitCommand         = quitVerb
        quitCommand.set_parse_action( QuitCommand )
        #
        #   HELP [ <command> ]
        #
        helpCommand         = helpVerb +  pp.Optional( nameReference )
        helpCommand.set_parse_action( HelpCommand )
        #
        #   SHUTDOWN
        #
        shutdownCommand     = shutdownVerb
        shutdownCommand.set_parse_action( ShutdownCommand )
        #
        #   RESTART
        #
        restartCommand      = restartVerb + pp.Optional( nameReference )
        restartCommand.set_parse_action( RestartCommand )
        #
        #   RELOAD
        #
        reloadCommand       = reloadVerb
        reloadCommand.set_parse_action( ReloadCommand )
        #
        #   STATUS
        #
        statusCommand       = statusVerb
        statusCommand.set_parse_action( StatusCommand )
        commands = openCommand | closeCommand | shutdownCommand | restartCommand | statusCommand | \
                   reloadCommand | helpCommand | quitCommand

        if self.__experimental:
            #
            #   ADD <name> <attribute-expression>
            #
            #   attribute-expression
            #       PROGRAM <executable>
            #           [, PIDFILE <pid-filename> ]
            #           [, { CWD | WORKING-DIRECTORY } <folder-name> ]
            #           [, USER <username> ] [, GROUP <group-name> ]
            #           [, RESTART_DELAY <delay> [ SECS | MINS ] ]
            #           [, ARGUMENTS <arguments> ]
            #           [, ENVIRONMENT <environment-assignments> ]
            #
            executableExpr      = pp.Group( processVerb + filePathReference )
            pidFilenameExpr     = pp.Group( pidfileVerb + filePathReference )
            workingFolderExpr   = pp.Group( cwdVerb + filePathReference )
            userNameExpr        = pp.Group( userVerb + (pp.Word( pp.nums ) | pp.Word( pp.alphas )) )
            userGroupExpr       = pp.Group( groupVerb + (pp.Word( pp.nums ) | pp.Word( pp.alphas )) )
            delayExpr           = pp.Group( delayVerb + pp.Word( pp.nums ) + pp.Optional( secsVerb | minsVerb ) )
            argumentsExpr       = pp.Group( argumentsVerb )
            environmentExpr     = pp.Group( environmentVerb )
            attributeExpression = pp.ZeroOrMore( executableExpr | pidFilenameExpr | workingFolderExpr |
                                                 userNameExpr | userGroupExpr | delayExpr | argumentsExpr |
                                                 environmentExpr | statusCommand )
            addCommand          = addVerb + nameReference + attributeExpression
            addCommand.set_parse_action( AddCommand )
            #
            #   SET <name> <attribute-expression>
            #
            #       attribute-expression see above
            setCommand          = setVerb + attributeExpression
            setCommand.set_parse_action( SetCommand )
            #
            #   SHOW <name> [ DETAILS ]
            #
            showCommand          = showVerb + nameReference + pp.Optional( detailsVerb )
            showCommand.set_parse_action( ShowCommand )
            #
            #   STORE
            #
            storeCommand       = storeVerb
            storeCommand.set_parse_action( StoreCommand )
            commands |= addCommand | setCommand | showCommand | storeCommand
        #
        # define parser using all command expressions
        #
        parser = pp.ungroup( commands )( "command" )

        return parser


class OsComPrompt( Prompt ):
    def __init__( self, session ):
        super().__init__( program_name = 'oscom' )
        self.parser = Parser( session.experimental )
        self.session = session
        return

    def onecmd( self, cmd_str ):
        try:
            cmd = self.parser.bnf.parse_string( cmd_str )
            if cmd is not None:
                cmd.command( self.session )

        except pp.ParseException as pe:
            print( random.choice( [ "Sorry, I don't understand that.",
                                               "Huh?",
                                               "Excuse me?",
                                               "???",
                                               "What?", ] ) )

        return not self.session.running


class Session( object ):
    def __init__( self, experimental: bool = False):
        super().__init__()
        self.experimental   = experimental
        self.running        = True
        self.host           = 'localhost'
        self.port           = 5678
        self.program        = None
        return


def usage( banner ):
    print( f"{banner}" + """

Syntax:
    
    # oscom [ <options> ] [ <node-name> ] 
    
    # python -m oscom [ <options> ] [ <node-name> ]

Options:
    -h/--help           This help
    -v                  Version information
    
    
""" )


def main():
    banner = """OSCOM control utility for OSMON daemon. version {vers} - {date}.
(C) 2024 Copyright, all rights reserved, Marc Bertens-Nguyen, released under GPL 2.0 (only).      
""".format( vers = __version__, date = __date__ )
    try:
        opts, args = getopt.getopt( sys.argv[ 1: ], "hve", [ "help", "experimental" ] )

    except getopt.GetoptError as err:
        # print help information and exit:
        print( err )  # will print something like "option -a not recognized"
        usage( banner )
        sys.exit( 2 )

    experimental = False
    for o, a in opts:
        if o == "-v":
            print( f"{ banner }\nVersion: {__version__}" )

        elif o in ("-h", "--help"):
            usage( banner )
            sys.exit()

        elif o in ("-e", "--experimental"):
            experimental = True

        else:
            assert False, "unhandled option"

    oscom = OsComPrompt( Session( experimental ) )
    print( con.BG_BLACK << con.FG_WHITE_LIGHT << con.CLS, end = '' )
    oscom.prompt = ">"
    if len( args ) >= 1:
        oscom.onecmd( f"OPEN { args[ 0 ] }" )

    oscom.cmdloop( banner )
    return
