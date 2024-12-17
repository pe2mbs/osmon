import getopt
import io
import logging
import sys
import time
import typing as t
import yaml
from datetime import datetime

from oscom.client import SimpleClient
from osmon.common.interfaces import IMessageRequest, IMessageResponse





def usage():
    print( "Bla" )


def dump_txt( data: IMessageResponse, stream: io.IOBase ):
    if data.osmon is not None:
        # Do stats of the OSMON process itself
        start_time = datetime.fromtimestamp( data.osmon.create_time )
        cpu_percent = "{:3.2f}%".format( data.osmon.cpu_percent )
        mem_percent = "{:3.2f}%".format( data.osmon.memory_percent )
        print( "OSMON" )
        print( f"  Start date & time: {start_time}" )
        print( f"  Status:            {data.osmon.status}" )
        print( f"  Cpu / usage:       {data.osmon.cpu_num:02d} / { cpu_percent }" )
        print( f"  Memory usage:      {mem_percent}" )
        print( f"  Working directory: {data.osmon.cwd}" )

    print( "+----------------------+----------------------------+--------------+--------------*---------+--------------------+" )
    print( "| Task                 | Start date & time          | Status       | Cpu / usage  | Memory  | Working directory   ")
    print( "+----------------------+----------------------------+--------------+--------------*---------+--------------------+" )
    #       | 12345678901234567890 | yyyy-mm-ddThh:mm:ss.ffffff | sleeping     | 99 / 99.99%  | 99.99%  | ....
    for task in data.parameters:
        prcs = task.process
        start_time = datetime.fromtimestamp( prcs.create_time )
        cpu_percent = "{:3.2f}%".format( prcs.cpu_percent )
        mem_percent = "{:3.2f}%".format( prcs.memory_percent )
        print( f"| {task.name:20} | {start_time} | {prcs.status:12} | {prcs.cpu_num:02d} / {cpu_percent:7} | {mem_percent:7} | {prcs.cwd}")
        print( "+----------------------+----------------------------+--------------+--------------*---------+--------------------+" )

    return


def main():
    logging.basicConfig( stream = sys.stdout, level = logging.WARNING )
    try:
        opts, args = getopt.getopt( sys.argv[ 1: ], "ho:f:h:p:vr:", [ "help", "output=", "format=", "host=",
                                                                      "port=", "repeat=" ] )

    except getopt.GetoptError as err:
        # print help information and exit:
        print( err )  # will print something like "option -a not recognized"
        usage()
        sys.exit( 2 )

    host = 'localhost'
    port = 5678
    output = sys.stdout
    fmt = 'txt'
    repeat = None
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True

        elif o in ("-h", "--help"):
            usage()
            sys.exit()

        elif o in ("-o", "--output"):
            output = open( a, 'w' )

        elif o in ("-f", "--format"):
            fmt = a

        elif o in ("-h", "--host"):
            host = a

        elif o in ("-p", "--port"):
            port = int( a )

        elif o in ("-r", "--repeat"):
            repeat = int( a )

        else:
            assert False, "unhandled option"  # ...

    def process_args():
        for cmd in args:
            client = SimpleClient( host, port, IMessageResponse )
            if cmd not in ( 'status', 'stop', 'restart', 'reload' ):
                logging.error( f"Error: { cmd } not supported" )
                continue

            data = IMessageRequest( action = cmd )
            received: IMessageResponse = client.sendReceive( data )
            if cmd == 'status':
                logging.info( received.model_dump_json( indent = 4 ) )
                if fmt == 'json':
                    print( received.model_dump_json( indent = 4 ), file = output )

                elif fmt == 'yaml':
                    fp = io.StringIO()
                    yaml.dump( received.model_dump(), fp )
                    print( fp.getvalue(), file = output )

                elif fmt == 'txt':
                    dump_txt( received, output )

            else:
                logging.info( f"{ received.status }, { received.message }" )

    if repeat is None:
        process_args()

    else:
        while True:
            process_args()
            time.sleep( repeat )

    return


if __name__ == '__main__':
    main()