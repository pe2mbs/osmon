import sys

if sys.platform == 'linux':
    from osmon.system.linux.startup import startup

elif sys.platform == 'windows':
    from osmon.system.windows.startup import startup

else:
    print( f"System { sys.platform } is not (YET) supported by OSMON", file = sys.stderr )
    exit( -1 )

startup( sys.argv[ 1: ] )
