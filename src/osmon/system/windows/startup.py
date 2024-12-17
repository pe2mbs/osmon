import logging
import sys
from threading import Event, Thread
import win32serviceutil  # ServiceFramework and commandline helper
import win32service  # Events
import servicemanager  # Simple setup and logging
from osmon.common.config import CConfiguration
from osmon.common.event import FlagEvent, STOP_EVENT, RESTART_EVENT, RELOAD_EVENT
from osmon.common.processlist import ProcessList
from osmon.common.server import JsonServer
from osmon.monitor import JsonHandler, dump_configuration
from osmon.system.windows.service import SMWinservice


logger = logging.getLogger( 'OSMON' )


class OsMonService( SMWinservice ):
    _svc_name_          = 'osmon-service'
    _svc_display_name_  = 'OSMON Service'
    _svc_description_   = 'OSMON Service, process monitor for python applications'

    def __init__( self, args ):
        self._redirectSystemStreamsIfNecessary()
        super().__init__( args )
        self._event = FlagEvent()
        print( f"OsMonService.args: {args}" )
        filename = ''
        self.__config = CConfiguration( filename )
        return

    def _redirectSystemStreamsIfNecessary( self ):
        # Python programs running as Windows NT services must not send output to
        # the default sys.stdout or sys.stderr streams, because those streams are
        # not fully functional in the NT service execution environment.  Sending
        # output to them will eventually (but not immediately) cause an IOError
        # ("Bad file descriptor"), which can be quite mystifying to the
        # uninitiated.  This problem can be overcome by replacing the default
        # system streams with a stream that discards any data passed to it (like
        # redirection to /dev/null on Unix).
        #
        # However, the pywin32 service framework supports a debug mode, under which
        # the streams are fully functional and should not be redirected.
        shouldRedirect = True
        if servicemanager.Debugging() or ( hasattr( servicemanager, 'RunningAsService' ) and not servicemanager.RunningAsService() ):
            shouldRedirect = False

        if shouldRedirect:
            sys.stdout = sys.stderr = open( 'nul', 'w' )

        return shouldRedirect

    def start( self ):
        self._event.clear()
        self.__config.load()
        return

    def stop( self ):
        self._event.set( STOP_EVENT )
        return

    def main( self ):
        while not self._event.is_set( STOP_EVENT ):
            logger.setLevel( logging._nameToLevel[ cfg.trace_level ] )  # noqa
            dump_configuration( self.__config.Config )
            logger.warning( "Startup monitoring" )
            processes = ProcessList( self.__config.Config )
            JsonHandler.processes = processes
            JsonHandler.event = self._event
            server = JsonServer( ('localhost', 5678), JsonHandler )
            thread = Thread( target = server.serve_forever )
            thread.start()
            # Start all processes
            processes.start()
            logger.warning( "Enter monitoring" )
            while not self._event.is_set( STOP_EVENT | RESTART_EVENT | RELOAD_EVENT ):
                self._event.wait( self.__config.Config.monitor_interval )
                try:
                    processes.monitor()

                except Exception:  # noqa
                    logger.exception( "During the monitor of processes" )

            logger.warning( "Shutdown monitoring" )
            if not self._event.is_set( RELOAD_EVENT ):
                # On reloading the configuration, don't stop the processes
                processes.stop()

            server.shutdown()
            server.server_close()
            thread.join()
            del processes
            del server
            if self._event.is_set( RESTART_EVENT | RELOAD_EVENT ):
                # Restart / reload the configuration
                self.__config.load()

            self._event.clear( RESTART_EVENT | RELOAD_EVENT )

        logger.warning( "Shutdown osmon service" )
        return


def startup( argv ):
    if len( sys.argv ) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle( OsMonService )
        servicemanager.StartServiceCtrlDispatcher()

    else:
        win32serviceutil.HandleCommandLine( OsMonService )

    return
