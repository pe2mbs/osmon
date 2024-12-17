import typing as t
import pyparsing as pp
import oscom.color as con
from oscom.client import SimpleClient
from osmon.common.interfaces import IMessageResponse, IMessageRequest


class Command( object ):
    """Base class for commands"""
    help_cmd_width = 25

    def __init__( self, verb, quals ):
        self.verb = verb
        self.quals: pp.ParseResults = quals

    @staticmethod
    def help_description() -> tuple:
        return "", ""

    @staticmethod
    def detail_help( self ):
        return "No detailed help information available."

    def _do_command( self, session ):
        print( con.BG_RED << con.FG_YELLOW_LIGHT, end = '' )
        for idx, item in enumerate( self.quals ):
            print( f"{idx}: {item}" )

        print( con.FG_WHITE << con.BG_BLACK, end = '' )
        return

    def __call__( self, session ):
        # print( self.verb.capitalize() + "..." )
        self._do_command( session )
        return

    def _do_osmon_request( self, session, request: t.Union[ str, IMessageRequest ], response_cls = IMessageResponse ):
        if isinstance( session.host, str ):
            if isinstance( request, str ):
                request = IMessageRequest( action = request )

            elif not isinstance( request, IMessageRequest ):
                raise ValueError( 'request must be str or IMessageRequest')

            client = SimpleClient( session.host, session.port, response_cls )
            return client.sendReceive( request )

        self.print_error( con.BG_RED << con.FG_YELLOW_LIGHT << "Session not opened" << con.FG_WHITE << con.BG_BLACK )
        return

    @staticmethod
    def print_warning( warning ):
        print( con.BG_BLACK << con.FG_YELLOW_LIGHT << warning << con.FG_WHITE << con.BG_BLACK )
        return

    @staticmethod
    def print_error( error ):
        print( con.BG_RED << con.FG_YELLOW_LIGHT << error << con.FG_WHITE << con.BG_BLACK )
        return
