import typing as t
from pydantic import BaseModel, Field, AliasChoices


class ITaskConfig( BaseModel ):
    name:               str
    process:            str
    arguments:          t.List[ str ]
    pidfile:            str
    cwd:                str
    user:               int
    group:              int
    #                                                   restart after 5 seconds
    restart_delay:      int                         = Field( 5, validation_alias = AliasChoices( 'restart_delay',
                                                                                                 'restart-delay' ) )


class IConfiguration( BaseModel ):
    version:            int
    #                                               # Default every 30 seconds check the processes
    monitor_interval:   int                         = Field( 30, validation_alias = AliasChoices( 'monitor_interval',
                                                                                                  'monitor-interval' ) )
    #                                               # Default log level is WARNING
    trace_level:        str                         = Field( "WARNING", validation_alias = AliasChoices( 'trace_level',
                                                                                                         'trace-level' ) )
    #                                               # Default syslog is used are logger on Linux
    #                                               # On windows the Windows Eventlog is used
    log_file:           str                         = Field( None, validation_alias = AliasChoices( 'log_file',
                                                                                                    'log-file' ) )
    user:               str                         = Field( None )
    group:              str                         = Field( None )
    cwd:                str                         = Field( None )
    processes:          t.List[ ITaskConfig ]


class IProcessCpuTimes( BaseModel ):
    user:               float
    system:             float
    children_user:      float
    children_system:    float
    iowait:             float


class IProcessMemInfo( BaseModel ):
    rss:                float
    vms:                float
    # Linux
    shared:             t.Optional[ float ]         = Field( None )
    text:               t.Optional[ float ]         = Field( None )
    lib:                t.Optional[ float ]         = Field( None )
    data:               t.Optional[ float ]         = Field( None )
    dirty:              t.Optional[ float ]         = Field( None )
    # Windows
    num_page_faults:    t.Optional[ float ]         = Field( None )      # shared
    peak_wset:          t.Optional[ float ]         = Field( None )      # text
    wset:               t.Optional[ float ]         = Field( None )      # lib
    peak_paged_pool:    t.Optional[ float ]         = Field( None )      # data
    paged_pool:         t.Optional[ float ]         = Field( None )      # paged_pool
    peak_nonpaged_pool: t.Optional[ float ]         = Field( None )
    nonpaged_pool:      t.Optional[ float ]         = Field( None )
    pagefile:           t.Optional[ float ]         = Field( None )
    peak_pagefile:      t.Optional[ float ]         = Field( None )
    private:            t.Optional[ float ]         = Field( None )


class IProcessStatistics( BaseModel ):
    cpu:                int
    cpu_percent:        float
    cpu_times:          IProcessCpuTimes
    memory:             IProcessMemInfo
    status:             str


class IMessageRequest( BaseModel ):
    action:             str
    parameters:         dict                        = Field( None )


class IProcessInfo( BaseModel ):
    cmdline:            t.List[ str ]
    cpu_num:            int
    cpu_percent:        float
    cpu_times:          t.List[ float ]
    create_time:        float
    cwd:                str
    environ:            dict
    exe:                str
    memory_info:        t.List[ int ]
    memory_percent:     float
    name:               str
    num_ctx_switches:   t.List[ int ]
    num_fds:            int
    num_threads:        int
    pid:                int
    ppid:               int
    status:             str
    terminal:           t.Union[ str, None ]        = Field( None )
    username:           str


class ITaskProcessInfo( BaseModel ):
    name:               str
    pid:                str
    status:             str                         = Field( '' )
    process:            IProcessInfo                = Field( None )


class IMessageResponse( BaseModel ):
    status:             bool
    message:            str
    osmon:              IProcessInfo                = Field( None )
    parameters:         t.List[ ITaskProcessInfo ]  = Field( [] )
