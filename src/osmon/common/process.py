import typing as t
import logging
import os.path
import sys
import stat
from threading import Timer
from psutil import Process, NoSuchProcess
from osmon.common.exc import NotExecutable
from osmon.common.interfaces import ITaskConfig, IProcessStatistics, IProcessCpuTimes, IProcessMemInfo, ITaskProcessInfo, IProcessInfo
from abc import ABC, abstractmethod


__all__ = [ 'ProcessMonitorAbc' ]


logger = logging.getLogger( 'OSMON.PROCESS' )


class ProcessMonitorAbc( ABC ):
    def __init__( self, descriptor: ITaskConfig ):
        super().__init__()
        self._descriptor    = descriptor
        self._process       = None
        self._process       = None
        self._stats         = None
        self._restart_timer = None
        return

    def _build_process_argument( self ):
        if self._descriptor.process.endswith( '.py' ):
            if not os.path.exists( self._descriptor.process ):
                raise FileNotFoundError( self._descriptor.process )

            # Python program
            args = [ sys.executable, self._descriptor.process ] + self._descriptor.arguments

        else:
            stats = os.stat( self._descriptor.process )
            if stats.st_mode & ( stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH ) == 0:
                raise NotExecutable( self._descriptor.process )

            # Regular executable
            args = [ self._descriptor.process ] + self._descriptor.arguments

        logger.info( f"Process { self._descriptor.name } arguments { ' '.join( args ) }" )
        return args

    def _get_pid_child( self ) -> int:
        with open( self._descriptor.pidfile, 'r' ) as stream:
            pid = int( stream.read() )

        return pid

    @property
    def Name( self ) -> str:
        return self._descriptor.name

    @property
    def Process( self ) -> str:
        return self._descriptor.process

    @property
    def Arguments( self ) -> t.List[ str ]:
        return self._descriptor.arguments

    @property
    def PidFile( self ) -> str:
        return self._descriptor.pidfile

    @abstractmethod
    def start( self ):
        pass

    def stop( self ):
        if isinstance( self._process, Process ):
            self._process.kill()

        return

    def monitor( self ):
        if not isinstance( self._process, Process ):
            logger.warning( f"Waiting for { self._descriptor.name } to be started" )
            # Timer is running and process is not started yes
            return

        logger.debug( f"Checking status of process { self._descriptor.name }" )
        self._process: Process
        try:
            with self._process.oneshot():
                cpu = IProcessCpuTimes( **self._process.cpu_times()._asdict() )     # noqa
                mem = IProcessMemInfo( **self._process.memory_info()._asdict() )    # noqa
                self._stats = IProcessStatistics( cpu = self._process.cpu_num(),
                                                  status = self._process.status(),
                                                  cpu_percent = self._process.cpu_percent(),
                                                  cpu_times = cpu,
                                                  memory = mem )
            logger.debug( f"Usage of {self._descriptor.name}: {cpu}" )
            # Clear the restart timer on a successful poll of the process
            self._restart_timer = None

        except AttributeError:
            logger.exception( "During monitor" )

        except NoSuchProcess:
            logger.error( f"Process {self._descriptor.name} disappeared, needs restarting" )
            if self._descriptor.restart_delay == 0:
                self.start()

            else:
                self._process = None
                logger.warning( f"Process {self._descriptor.name} scheduled for start in { self._descriptor.restart_delay }" )
                self._restart_timer = Timer( self._descriptor.restart_delay, self.start )
                self._restart_timer.start()

        return

    def asDict( self ) -> dict:
        result = ITaskProcessInfo( name = self._descriptor.name, pid = self._descriptor.pidfile )
        if isinstance( self._process, Process ):
            result.status = 'running'
            result.process = IProcessInfo( **self._process.as_dict( [ 'num_fds', 'pid', 'terminal', 'num_threads', 'create_time',
                                                                      'ppid', 'cpu_num', 'cwd', 'exe', 'cpu_times', 'environ',
                                                                      'memory_info', 'cmdline', 'name', 'username', 'num_ctx_switches',
                                                                      'status', 'cpu_percent', 'memory_percent' ] ) )
        else:
            result.status = 'not running/initialized'

        return result
