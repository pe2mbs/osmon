import os

from psutil import Process

from osmon.system import ProcessMonitor
from osmon.common.interfaces import IConfiguration, IProcessInfo


class ProcessList( object ):
    def __init__( self, cfg: IConfiguration ):
        self._processes = [ ProcessMonitor( proc_class ) for proc_class in cfg.processes ]
        return

    def __del__( self ):
        for proc in self._processes:
            del proc

        self._processes = []
        return

    def start( self ):
        for proc_class in self._processes:
            proc_class.start()

        return

    def stop( self ):
        for proc_class in self._processes:
            proc_class.stop()

        return

    def monitor( self ):
        for proc_class in self._processes:
            proc_class.monitor()

        return

    def __iter__( self ):
        return iter( self._processes )

    def processInfo( self ) -> IProcessInfo:
        process = Process( os.getpid() )
        return IProcessInfo( **process.as_dict( [ 'num_fds', 'pid', 'terminal', 'num_threads', 'create_time',
                                                  'ppid', 'cpu_num', 'cwd', 'exe', 'cpu_times', 'environ',
                                                  'memory_info', 'cmdline', 'name', 'username', 'num_ctx_switches',
                                                  'status', 'cpu_percent', 'memory_percent' ] ) )
