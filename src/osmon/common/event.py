from threading import Condition, Lock


__all__ = [ 'STOP_EVENT', 'RESTART_EVENT', 'RELOAD_EVENT', 'INTERFACE_EVENT', 'FlagEvent' ]


STOP_EVENT      = 1
RESTART_EVENT   = 2
RELOAD_EVENT    = 4
INTERFACE_EVENT: int = 8


class FlagEvent( object ):
    """Class implementing event objects.

    Events manage a flag that can be set to true with the set() method and reset
    to false with the clear() method. The wait() method blocks until the flag is
    true.  The flag is initially false.

    """

    # After Tim Peters' event class (without is_posted())

    def __init__( self ):
        self._cond = Condition( Lock() )
        self._flag = 0x00

    def _reset_internal_locks( self ):
        # private!  called by Thread._reset_internal_locks by _after_fork()
        self._cond.__init__( Lock() )

    def is_set( self, flag: int = 0xFFFFFFFF ):
        """Return true if and only if the internal flag is true."""
        return self._flag & flag

    isSet = is_set

    def set( self, flag: int ):
        """Set the internal flag to true.

        All threads waiting for it to become true are awakened. Threads
        that call wait() once the flag is true will not block at all.

        """
        with self._cond:
            self._flag |= flag
            self._cond.notify_all()

    def clear( self, flag: int = 0 ):
        """Reset the internal flag to false.

        Subsequently, threads calling wait() will block until set() is called to
        set the internal flag to true again.

        """
        with self._cond:
            self._flag &= ~flag

        return

    def wait( self, timeout = None ):
        """Block until the internal flag is true.

        If the internal flag is true on entry, return immediately. Otherwise,
        block until another thread calls set() to set the flag to true, or until
        the optional timeout occurs.

        When the timeout argument is present and not None, it should be a
        floating point number specifying a timeout for the operation in seconds
        (or fractions thereof).

        This method returns the internal flag on exit, so it will always return
        True except if a timeout is given and the operation times out.

        """
        with self._cond:
            signaled = self._flag
            if not signaled:
                signaled = self._cond.wait( timeout )

            return signaled
