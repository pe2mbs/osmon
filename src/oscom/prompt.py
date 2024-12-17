# -*- coding: utf-8 -*-
"""
    Process monitor commander for running monitored applications

    Copyright (C) 2018 Marc Bertens-Nguyen <m.bertens@pe2mbs.nl>

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""
import string
from abc import ABC, abstractmethod
import logging
import os
import sys
import oscom.color as con


__all__     = [ 'Prompt' ]
__author__  = 'Marc Bertens-Nguyen <m.bertens@pe2mbs.nl>'


class Prompt( ABC ):
    """A simple framework for writing line-oriented command interpreters.

    These are often useful for test harnesses, administrative tools, and
    prototypes that will later be wrapped in a more sophisticated interface.

    A Cmd instance or subclass instance is a line-oriented interpreter
    framework.  There is no good reason to instantiate Cmd itself; rather,
    it's useful as a superclass of an interpreter class you define yourself
    in order to inherit Cmd's methods and encapsulate action methods.

    """
    prompt          = '>> '
    ruler           = '='
    lastcmd         = ''
    intro           = None
    use_rawinput    = 1
    identchars      = string.printable

    def __init__( self, completekey = 'tab', program_name: str = 'commander' ):
        """Instantiate a line-oriented interpreter framework.

        The optional argument 'completekey' is the readline name of a
        completion key; it defaults to the Tab key. If completekey is
        not None and the readline module is available, command completion
        is done automatically.

        """
        self.cmdqueue       = []
        self.completekey    = completekey
        self.history_length = 50
        try:
            import readline
            self.readline = readline

        except:
            import pyreadline
            self.readline = pyreadline.Readline()

        self.readline.set_history_length( self.history_length )
        # TODO: use user host folder
        if os.path.isfile( f'.{program_name}.hist' ):
            self.readline.read_history_file( f'.{program_name}.hist' )

        return

    @abstractmethod
    def onecmd( self, line ):
        """Interpret the argument as though it had been typed in response
        to the prompt.

        This may be overridden, but should not normally need to be;
        see the precmd() and postcmd() methods for useful execution hooks.
        The return value is a flag indicating whether interpretation of
        commands by the interpreter should stop.

        """
        pass

    def cmdloop(self, intro=None ):
        """Repeatedly issue a prompt, accept input, parse an initial prefix
        off the received input, and dispatch to action methods, passing them
        the remainder of the line as argument.

        """
        print( con.CLS, end = '' )
        self.preloop()
        if self.use_rawinput and self.completekey:
            try:
                self.old_completer = self.readline.get_completer()
                self.readline.set_completer(self.complete)
                self.readline.parse_and_bind(self.completekey+": complete")

            except ImportError:
                pass

        try:
            if intro is not None:
                self.intro = intro

            if self.intro:
                print( str( self.intro ) + "\n" )

            stop = None
            while not stop:
                if self.cmdqueue:
                    line = self.cmdqueue.pop( 0 )
                    logging.info( 'POP COMMAND: {}'.format( line ) )

                else:
                    if self.use_rawinput:
                        try:
                            logging.info( 'READ RAW INPUT' )
                            line = input( self.prompt )

                        except EOFError:
                            logging.info( 'EOFError' )
                            line = 'EOF'

                    else:
                        logging.info( 'READ STDIN' )
                        print( self.prompt, end ='' )
                        line = sys.stdin.readline()
                        if not len( line ):
                            line = 'EOF'

                        else:
                            line = line.rstrip( '\r\n' )

                        logging.info( 'READ STDIN [{}]'.format( line ) )

                logging.info( 'EXECUTING COMMAND: {}'.format( line ) )
                line = self.precmd( line )
                stop = self.onecmd( line )
                stop = self.postcmd( stop, line )

            self.postloop()

        finally:
            if self.use_rawinput and self.completekey:
                try:
                    self.readline.set_completer(self.old_completer)

                except ImportError:
                    pass

        return

    def precmd(self, line):
        """Hook method executed just before the command line is
        interpreted, but after the input prompt is generated and issued.

        """
        return line

    def postcmd(self, stop, line):
        """Hook method executed just after a command dispatch is finished."""
        return stop

    def preloop(self):
        """Hook method executed once when the cmdloop() method is called."""
        pass

    def postloop(self):
        """Hook method executed once when the cmdloop() method is about to
        return.

        """
        pass

    def parseline(self, line):
        """Parse the line into a command name and a string containing
        the arguments.  Returns a tuple containing (command, args, line).
        'command' and 'args' may be None if the line couldn't be parsed.
        """
        line = line.strip()
        if not line:
            return None, None, line

        elif line[0] == '?':
            line = 'help ' + line[1:]

        elif line[0] == '!':
            if hasattr(self, 'do_shell'):
                line = 'shell ' + line[1:]

            else:
                return None, None, line

        i, n = 0, len(line)
        while i < n and line[i] in self.identchars:
            i = i+1

        cmd, arg = line[:i], line[i:].strip()
        return cmd, arg, line

    def emptyline(self):
        """Called when an empty line is entered in response to the prompt.

        If this method is not overridden, it repeats the last nonempty
        command entered.

        """
        if self.lastcmd:
            return self.onecmd(self.lastcmd)

        return

    def default(self, line):
        """Called on an input line when the command prefix is not recognized.

        If this method is not overridden, it prints an error message and
        returns.

        """
        print( '*** Unknown syntax: %s' % line )
        return

    def completedefault(self, *ignored):
        """Method called to complete an input line when no command-specific
        complete_*() method is available.

        By default, it returns an empty list.

        """
        return []

    def completenames(self, text, *ignored):
        dotext = 'do_'+text
        return [a[3:] for a in self.get_names() if a.startswith(dotext)]

    def complete(self, text, state):
        """Return the next possible completion for 'text'.

        If a command has not been entered, then complete against command list.
        Otherwise, try to call complete_<command> to get list of completions.
        """
        if state == 0:
            origline = self.readline.get_line_buffer()
            line = origline.lstrip()
            stripped = len(origline) - len(line)
            begidx = self.readline.get_begidx() - stripped
            endidx = self.readline.get_endidx() - stripped
            if begidx>0:
                cmd, args, foo = self.parseline(line)
                if cmd == '':
                    compfunc = self.completedefault

                else:
                    try:
                        compfunc = getattr(self, 'complete_' + cmd)

                    except AttributeError:
                        compfunc = self.completedefault

            else:
                compfunc = self.completenames

            self.completion_matches = compfunc(text, line, begidx, endidx)

        try:
            return self.completion_matches[state]

        except IndexError:
            return None

    def get_names(self):
        # This method used to pull in base class attributes
        # at a time dir() didn't do it yet.
        return dir( self.__class__ )

    def complete_help(self, *args):
        commands = set( self.completenames( *args ) )
        topics = set( a[5:] for a in self.get_names()
                      if a.startswith('help_' + args[0] ) )
        return list( commands | topics )

    def print_topics(self, header, cmds, cmdlen, maxcol):
        if cmds:
            print( header )
            if self.ruler:
                print( self.ruler * len( header ) )

            self.columnize(cmds, maxcol-1)
            print()

        return

    def columnize(self, list, displaywidth=80):
        """Display a list of strings as a compact set of columns.

        Each column is only as wide as necessary.
        Columns are separated by two spaces (one was not legible enough).
        """
        if not list:
            print( "<empty>" )
            return

        nonstrings = [ i for i in range( len( list ) ) if not isinstance( list[ i ], str ) ]
        if nonstrings:
            raise TypeError("list[i] not a string for i in %s"
                            % ", ".join(map(str, nonstrings)))

        size = len( list )
        if size == 1:
            print( str( list[ 0 ] ) )
            return

        # Try every row count from 1 upward
        for nrows in range( 1, len( list ) ):
            ncols = ( size + nrows - 1 ) // nrows
            colwidths = []
            totwidth = -2
            for col in range( ncols ):
                colwidth = 0
                for row in range( nrows ):
                    i = row + nrows * col
                    if i >= size:
                        break

                    x = list[ i ]
                    colwidth = max( colwidth, len( x ) )

                colwidths.append( colwidth )
                totwidth += colwidth + 2
                if totwidth > displaywidth:
                    break

            if totwidth <= displaywidth:
                break

        else:
            nrows = len( list )
            ncols = 1
            colwidths = [ 0 ]

        for row in range( nrows ):
            texts = []
            for col in range( ncols ):
                i = row + nrows * col
                if i >= size:
                    x = ""

                else:
                    x = list[i]

                texts.append( x )

            while texts and not texts[ -1 ]:
                del texts[ -1 ]

            for col in range( len( texts ) ):
                texts[ col ] = texts[ col ].ljust( colwidths[ col ] )

            print( str( "  ".join( texts ) ) )

        return
