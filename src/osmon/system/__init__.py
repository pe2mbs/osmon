import platform
if platform.system() == 'Windows':
    from osmon.system.windows.process import ProcessMonitorWindows as ProcessMonitor

elif platform.system() == 'Linux':
    from osmon.system.linux.process import ProcessMonitorLinux as ProcessMonitor

else:
    raise Exception( f"Platform { platform.system() } is not supported (YET) by osmon" )

__all__ = [ 'ProcessMonitor' ]
