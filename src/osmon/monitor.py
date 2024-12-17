import typing as t
import logging
import socketserver
from threading import Thread
from osmon.common.event import FlagEvent, STOP_EVENT, RESTART_EVENT, RELOAD_EVENT
from osmon.common.interfaces import IConfiguration, IMessageRequest, IMessageResponse
from osmon.common.json_protocol import JsonProtocol
from osmon.common.process import ProcessMonitorAbc
from osmon.common.processlist import ProcessList
from osmon.common.server import JsonServer


logger = logging.getLogger( 'OSMON' )


class JsonHandler( socketserver.BaseRequestHandler, JsonProtocol ):
    processes       = None
    event           = None

    def __init__( self, request, client_address, server ):
        JsonProtocol.__init__( self, 2 )
        socketserver.BaseRequestHandler.__init__( self, request, client_address, server )

    "One instance per connection.  Override handle(self) to customize action."
    def handle( self ):
        # self.request is the client connection
        text = self.deserialize( self.request.recv, IMessageRequest )
        try:
            logger.info( f"Request: { text }" )
            if text.action == 'stop':
                self.event.set( STOP_EVENT )
                logger.warning( f"Stop requested" )
                response = IMessageResponse( status = True, message = 'Stop requested' )

            elif text.action == 'restart':
                self.event.set( RESTART_EVENT )
                logger.warning( f"Restart requested" )
                response = IMessageResponse( status = True, message = 'Restart requested' )

            elif text.action == 'reload':
                self.event.set( RELOAD_EVENT )
                logger.warning( f"Reload requested" )
                response = IMessageResponse( status = True, message = 'Reload requested' )

            elif text.action == 'status':
                response = IMessageResponse( status = True, message = '' )
                for process in self.processes:
                    if isinstance( process, ProcessMonitorAbc ):
                        response.parameters.append( process.asDict() )

                response.osmon = self.processes.processInfo()

            else:
                logger.error( f"Unknown request: { text }")
                response = IMessageResponse( status = False, message = 'Unknown request' )

        except Exception as exc:
            logger.exception( "During processing request" )
            response = IMessageResponse( status = False, message = str( exc ) )

        logger.info( f"Response: {response}" )
        self.serialize( self.request.send, response )
        self.request.close()
        return


def dump_configuration( cfg: IConfiguration ):
    result = cfg.model_dump_json( indent = 4 )
    for line in result.split( '\n' ):
        logger.info( line )

    return


def main( cfg: IConfiguration, load_configuration: t.Callable, *argv ):
    event = FlagEvent()
    while not event.is_set( STOP_EVENT ):
        logger.setLevel( logging._nameToLevel[ cfg.trace_level ] )  # noqa
        dump_configuration( cfg )
        logger.warning( "Startup monitoring" )
        processes                   = ProcessList( cfg )
        JsonHandler.processes       = processes
        JsonHandler.event           = event
        server = JsonServer( ( 'localhost', 5678 ), JsonHandler )
        thread = Thread( target = server.serve_forever )
        thread.start()
        # Start all processes
        processes.start()
        logger.warning( "Enter monitoring" )
        while not event.is_set( STOP_EVENT | RESTART_EVENT | RELOAD_EVENT ):
            event.wait( cfg.monitor_interval )
            try:
                processes.monitor()

            except Exception:       # noqa
                logger.exception( "During the monitor of processes" )

        logger.warning( "Shutdown monitoring" )
        if not event.is_set( RELOAD_EVENT ):
            # On reloading the configuration, don't stop the processes
            processes.stop()

        server.shutdown()
        server.server_close()
        thread.join()
        del processes
        del server
        if event.is_set( RESTART_EVENT | RELOAD_EVENT ):
            # Restart / reload the configuration
            cfg, _ = load_configuration()

        event.clear( RESTART_EVENT | RELOAD_EVENT )

    logger.warning( "Shutdown osmon service" )
    return
