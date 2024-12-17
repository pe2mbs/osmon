# OSMON daemon

The OSMON daemon is a program that start and monitor programs to keep them running.
When running on Linux a program can be started as a damon in this case when OSMON 
restarts it re-attaches the running daemon via the PID file. When a program is not
a daemon it restarts as well with OSMON. 

When running on Windows a program can be started detached by configuring a PID file.
When the program is started attached is will be restarted with the OSMON daemon.

OSMON daemon comes with oscom the commandline commander, with this a number of 
commands may be issued to the OSMON daemon;

    *   OPEN <node>     Connect to the machine where OSMON daemon is running.
    *   CLOSE           Close the connection with OSMON daemon.
    *   STATUS          Obtains the status of OSMON daemon and it processes.
    *   RELOAD          Reload the configuration.
    *   RESTART         Restart OSMON daemon. 
    *   EXIT or QUIT    Exit the commander.

Release 1.0.0
This release has a plain text JSON interface. This is for localhost good enough.

Release 1.1.0 (todo)
This release uses a security token to keep the session between OSMON and oscom
secure. In the token the action and timestamp are encrypted. The key for 
encryption is stored in the keyring os the system, this storing of the key is 
performed by oscom. When OSMON detects in the keyring of the configured user.
