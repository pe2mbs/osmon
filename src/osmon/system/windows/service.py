'''
SMWinservice
by Davide Mastromatteo

Base class to create winservice in Python
-----------------------------------------

Instructions:

1. Just create a new class that inherits from this base class
2. Define into the new class the variables
   _svc_name_ = "nameOfWinservice"
   _svc_display_name_ = "name of the Winservice that will be displayed in scm"
   _svc_description_ = "description of the Winservice that will be displayed in scm"
3. Override the three main methods:
    def start(self) : if you need to do something at the service initialization.
                      A good idea is to put here the inizialization of the running condition
    def stop(self)  : if you need to do something just before the service is stopped.
                      A good idea is to put here the invalidation of the running condition
    def main(self)  : your actual run loop. Just create a loop based on your running condition
4. Define the entry point of your module calling the method "parse_command_line" of the new class
5. Enjoy
'''
from abc import ABC, abstractmethod
import socket
import win32serviceutil
import servicemanager
import win32event
import win32service


class SMWinservice( win32serviceutil.ServiceFramework, ABC ):
    '''
        Base class to create winservice in Python
    '''

    _svc_name_          = 'pythonService'
    _svc_display_name_  = 'Python Service'
    _svc_description_   = 'Python Service Description'

    def __init__( self, args ):
        '''
        Constructor of the winservice
        '''
        win32serviceutil.ServiceFramework.__init__( self, args )
        self.hWaitStop = win32event.CreateEvent( None, 0, 0, None )
        socket.setdefaulttimeout(60)
        return

    def SvcStop(self):
        '''
            Called when the service is asked to stop

            it’s the method that will be called when the service is requested to stop.
        '''
        self.stop()
        self.ReportServiceStatus( win32service.SERVICE_STOP_PENDING )
        win32event.SetEvent( self.hWaitStop )
        return

    def SvcDoRun(self):
        '''
            Called when the service is asked to start

            it’s the method that will be called when the service is requested to start.
        '''
        self.start()
        servicemanager.LogMsg( servicemanager.EVENTLOG_INFORMATION_TYPE,
                               servicemanager.PYS_SERVICE_STARTED,
                               ( self._svc_name_, '' ) )
        self.main()
        return

    @abstractmethod
    def start(self):
        '''
            Override to add logic before the start
            eg. running condition

            it’s a method that you will be asked to override if you need to do something when the service is starting (before started)

        '''
        pass

    @abstractmethod
    def stop(self):
        '''
            Override to add logic before the stop
            eg. invalidating running condition

            it’s the method that you will be asked to override if you need to do something when the service is stopping (before stopped)

        '''
        pass

    @abstractmethod
    def main(self):
        '''
            Main class to be ovverridden to add logic

            it’s the method that will contain the logic of your script, usually in a loop that keeps it alive until the service is stopped.
        '''
        pass
