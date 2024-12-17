import logging
import os.path
import time
from osmon.common.exc import ProcessNotFound
from osmon.common.interfaces import ITaskConfig
from osmon.common.process import ProcessMonitorAbc
from psutil import Process, Popen, NoSuchProcess


__all__ = [ 'ProcessMonitorWindows', 'NoSuchProcess' ]


logger = logging.getLogger( 'osmon.process' )


class ProcessMonitorWindows( ProcessMonitorAbc ):
    def __init__( self, descriptor: ITaskConfig ):
        super().__init__( descriptor )
        return

    def start( self ):
        # TODO: Needs to be tested
        args = self._build_process_argument()
        if isinstance( self._descriptor.pidfile, str ):
            if os.path.exists( self._descriptor.pidfile ):
                try:
                    pid = self._get_pid_child()
                    self._process = Process( pid )
                    args_len = len( args ) - 1
                    prc_args = self._process.cmdline()
                    # This is for when the process runs in the pyCharm debugger
                    prc_args = [ prc_args[ 0 ] ] + prc_args[ -args_len: ]
                    if set( args ) == set( prc_args ):
                        self.monitor()
                        logger.info( "Found existing process" )
                        return

                    logger.warning( "Found existing process, but is invalid" )

                except NoSuchProcess:
                    pass

                finally:
                    self._process = None
                    os.remove( self._descriptor.pidfile )

        self._process = Popen( args )
        logger.info( f"Started process {self._process}" )
        self._process.wait( 5 )
        pid = -1
        if isinstance( self._descriptor.pidfile, str ):
            tries = 10
            while True:
                try:
                    if os.path.exists( self._descriptor.pidfile ):
                        pid = self._get_pid_child()

                    break

                except ValueError:
                    logger.debug( "Waiting on PID file" )
                    time.sleep( 1 )
                    tries -= 1
                    if tries == 0:
                        raise ProcessNotFound( f"PID file not found, process did not create the file: { self._descriptor.process }" )

                except Exception:
                    raise

        if pid == -1:
            raise ProcessNotFound( f"PID file not found { self._descriptor.process }" )

        # Now pickup the daemonized process
        self._process = Process( pid )
        self.monitor()
        return
