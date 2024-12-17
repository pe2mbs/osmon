import oscom.color as con
from datetime import datetime
from oscom.command.base import Command
from osmon.common.interfaces import IMessageRequest, IMessageResponse


class StatusCommand( Command ):
    def __init__(self, quals ):
        super().__init__( "STATUS", quals )
        return

    @staticmethod
    def help_description():
        return "STATUS", "Show the current status of the OSMON daemon and its processes."

    def _do_command( self, session ):
        response = self._do_osmon_request( session, 'status' )
        if not isinstance( response, IMessageResponse ):
            return

        if response.status:
            if response.osmon is not None:
                # Do stats of the OSMON process itself
                start_time = datetime.fromtimestamp( response.osmon.create_time )
                cpu_percent = "{:3.2f}%".format( response.osmon.cpu_percent )
                mem_percent = "{:3.2f}%".format( response.osmon.memory_percent )
                elapsed_time = datetime.now() - start_time
                print( "OSMON daemon" )
                print( f"  Start date & time: {start_time} - {elapsed_time}" )
                print( f"  Status:            {response.osmon.status}" )
                print( f"  Cpu / usage:       {response.osmon.cpu_num:02d} / {cpu_percent}" )
                print( f"  Memory usage:      {mem_percent}" )
                print( f"  Working directory: {response.osmon.cwd}" )

            print( "+----------------------+----------------------------+--------------+--------------*---------+--------------------+" )
            print( "| Task                 | Start date & time          | Status       | Cpu / usage  | Memory  | Working directory   " )
            print( "+----------------------+----------------------------+--------------+--------------*---------+--------------------+" )
            #       | 12345678901234567890 | yyyy-mm-ddThh:mm:ss.ffffff | sleeping     | 99 / 99.99%  | 99.99%  | ....
            for task in response.parameters:
                prcs = task.process
                start_time = datetime.fromtimestamp( prcs.create_time )
                elapsed_time = datetime.now() - start_time
                cpu_percent = "{:3.2f}%".format( prcs.cpu_percent )
                mem_percent = "{:3.2f}%".format( prcs.memory_percent )
                print( f"| {task.name:20} | {start_time} | {prcs.status:12} | {prcs.cpu_num:02d} / {cpu_percent:7} | {mem_percent:7} | {prcs.cwd}" )
                print( f"| {' '*20} | {str(elapsed_time):26} | {' '*12} | {' '*12} | {' '*7} |" )
                print( "+----------------------+----------------------------+--------------+--------------*---------+--------------------+" )

        else:
            self.print_warning( response.message )

        return

    @staticmethod
    def detail_help( self ):
        return """Request the current status of the OSMON daemon.

It provides information about the OSMON daemon it self and the processes that are running under the OSMON daemon.
Information provided are start time of the process / running time, its status, CPU and memory usage and the 
current working directory of the process. 

Example:

    >STATUS
    OSMON daemon
      Start date & time: 2024-12-14 08:43:04.300000 - 1 day, 22:55:53.096556
      Status:            sleeping
      Cpu / usage:       03 / 0.00%
      Memory usage:      0.18%
      Working directory: /
    +----------------------+----------------------------+--------------+--------------*---------+--------------------+
    | Task                 | Start date & time          | Status       | Cpu / usage  | Memory  | Working directory   
    +----------------------+----------------------------+--------------+--------------*---------+--------------------+
    | TEST                 | 2024-12-15 16:56:35.550000 | sleeping     | 00 / 0.00%   | 0.06%   | /
    |                      | 14:42:21.846702            |              |              |         |
    +----------------------+----------------------------+--------------+--------------*---------+--------------------+"""