import logging
import logging.handlers
import typing as t
import json
import os
import sys
import getopt
import yaml
import traceback
import osmon.monitor as API
from osmon.common.daemonize import Daemonize
from osmon.common.interfaces import IConfiguration


logger = logging.getLogger()


def usage():
    print( """OSMON process monitor, version 0.1.0, date 13 December 2024

Syntax:
    osmon [ <options> ]  

    """ )
    return


def startup( argv: t.List[ str ] ):
    try:
        try:
            opts, args = getopt.getopt( argv, "hvfp:u:g:c:c:", [ "help", "foreground", "pid=", "user=", "group=", "cwd=", "config=" ] )

        except getopt.GetoptError as err:
            # print help information and exit:
            print( err )  # will print something like "option -a not recognized"
            usage()
            sys.exit( 2 )

        pid = '/run/osmon.pid'
        user = os.getuid()
        group = os.getgid()
        verbose = False
        foreground = False
        chdir = os.getcwd()
        config_filename = None
        for o, a in opts:
            if o == "-v":
                verbose = True

            elif o in ("-h", "--help"):
                usage()
                sys.exit()

            elif o in ("-p", "--pid"):
                pid = a

            elif o in ("-u", "--user"):
                user = int( a )

            elif o in ("-g", "--group"):
                group = int( a )

            elif o in ("-f", "--foreground"):
                foreground = True

            elif o in ("-c", "--cwd"):
                chdir = a
                if not os.path.exists( chdir ):
                    os.makedirs( chdir, exist_ok = True )

            elif o in ("-c", "--config"):
                config_filename = a

            else:
                assert False, "unhandled option"

        if config_filename is None:
            raise Exception( "No configuration provided" )

        config = CConfiguration( config_filename )
        def load_configuration():
            config.load()
            return [ config, load_configuration ]

        if verbose:
            logger.setLevel( logging.DEBUG )
            config.Config.trace_level = 'DEBUG'

        else:
            logger.setLevel( logging.WARNING )

        if config.Config.cwd is not None:
            chdir = config.Config.cwd

        if config.Config.group is not None:
            group = config.Config.group

        if config.Config.user is not None:
            user = config.Config.user

        if config.Config.pid is not None:
            pid = config.Config.pid

        if config.Config.log_file is None:
            # use syslog
            if sys.platform == "darwin":
                syslog_address = "/var/run/syslog"

            else:
                syslog_address = "/dev/log"

            # We will continue with syslog initialization only if actually have such capabilities  # on the machine we are running this.
            if os.path.exists( syslog_address ):
                syslog = logging.handlers.SysLogHandler( syslog_address )

            else:
                # Fall back to localhost:514
                syslog = logging.handlers.SysLogHandler()

            if verbose:
                syslog.setLevel( logging.DEBUG )

            else:
                syslog.setLevel( logging.INFO )

            # Try to mimic to normal syslog messages.
            formatter = logging.Formatter("%(asctime)s %(name)s: %(message)s",
                                          "%b %e %H:%M:%S")
            syslog.setFormatter( formatter )
            logger.addHandler( syslog )

        else:
            # use logfile
            handler = logging.handlers.RotatingFileHandler( filename = config.Config.log_file,
                                                            encoding = 'u8',
                                                            maxBytes = 1024 * 1024 * 10,
                                                            backupCount = 7 )
            formatter = logging.Formatter( "%(asctime)s %(name)s: %(message)s",
                                           "%Y-%m-%d %e %H:%M:%S")
            handler.setFormatter( formatter )
            logger.addHandler( handler )

        daemon = Daemonize( app = "OSMON",
                            pid = pid,
                            action = API.main,
                            verbose = verbose,
                            user = user,
                            group = group,
                            chdir = chdir,
                            logger = logger,
                            foreground = foreground,
                            privileged_action = load_configuration )
        daemon.start()

    except Exception:  # noqa
        print( traceback.format_exc(), file = sys.stderr )

    return
