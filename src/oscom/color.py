#
#   Color package, color the console interface.
#   Copyright (C) 2024 Marc Bertens-Nguyen <m.bertens@pe2mbs.nl>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, see <https://www.gnu.org/licenses/>.
#
class CON( object ):
    def __init__( self, atte = '' ):
        self._atte = atte
        return

    def __str__( self ):
        return self._atte

    def __repr__( self ):
        return self._atte

    def __add__( self, other ):
        return CON( self._atte + str( other ) )

    def __rshift__(self, other):
        return CON( self._atte + str( other ) )

    def __lshift__(self, other):
        return CON( self._atte + str( other ) )


DEFAULT             = CON( '\033[0m' )
BOLD                = CON( '\033[1m' )
ITALIC              = CON( '\033[3m' )
UNDERLINE           = CON( '\033[4m' )
STRIKE_THROUGH      = CON( '\033[9m' )
UNDERLINE_THICK     = CON( '\033[21m' )
REVERSED            = CON( '\033[7m' )

BG_BLACK            = CON( '\033[40m' )
BG_RED              = CON( '\033[41m' )
BG_GREEN            = CON( '\033[42m' )
BG_YELLOW           = CON( '\033[43m' )
BG_BLUE             = CON( '\033[44m' )
BG_PURPLE           = CON( '\033[45m' )
BG_CYAN             = CON( '\033[46m' )
BG_GREY             = CON( '\033[47m' )
BG_GREY_LIGHT       = CON( '\033[100m' )
BG_RED_LIGHT        = CON( '\033[101m' )
BG_GREEN_LIGHT      = CON( '\033[102m' )
BG_YELLOW_LIGHT     = CON( '\033[103m' )
BG_BLUE_LIGHT       = CON( '\033[104m' )
BG_PURPLE_LIGHT     = CON( '\033[105m' )
BG_CYAN_LIGHT       = CON( '\033[106m' )
BG_WHITE_LIGHT      = CON( '\033[107m' )

FG_BLACK            = CON( '\033[30m' )
FG_RED              = CON( '\033[31m' )
FG_GREEN            = CON( '\033[32m' )
FG_YELLOW           = CON( '\033[33m' )
FG_BLUE             = CON( '\033[34m' )
FG_PURPLE           = CON( '\033[35m' )
FG_CYAN             = CON( '\033[36m' )
FG_GREY = FG_WHITE  = CON( '\033[37m' )
FG_BLACK_LIGHT      = CON( '\033[90m' )
FG_RED_LIGHT        = CON( '\033[91m' )
FG_GREEN_LIGHT      = CON( '\033[92m' )
FG_YELLOW_LIGHT     = CON( '\033[93m' )
FG_BLUE_LIGHT       = CON( '\033[94m' )
FG_PURPLE_LIGHT     = CON( '\033[95m' )
FG_CYAN_LIGHT       = CON( '\033[96m' )
FG_WHITE_LIGHT      = CON( '\033[97m' )

NORMAL              = DEFAULT << BG_BLACK << FG_WHITE
CLS                 = NORMAL << CON( "\x1b[2J\x1b[H" )
RESET               = CON( '\033[0m' )
endl                = CON( '\n' )


class COUT( object ):
    def __lshift__(self, other):
        print( str( other ), end = '' )
        return self


cout                = COUT()

#
#  Some examples:
#
# print( RESET << CLS, end = '' )
# print( BG_BLACK + FG_RED + STRIKE_THROUGH + "HELLO" + NORMAL + "World" + CLS )
# print( BG_BLACK + FG_GREEN + STRIKE_THROUGH + REVERSED + "HELLO" + NORMAL )
# print( BG_BLACK << FG_YELLOW << UNDERLINE_THICK << "HELLO" << NORMAL )
# print( BG_BLACK << FG_BLUE << UNDERLINE << "HELLO" << NORMAL )
# print( BG_BLACK << FG_PURPLE << ITALIC << "HELLO" << NORMAL )
# print( BG_BLACK << FG_CYAN << BOLD << "HELLO" << NORMAL )
# print( BG_BLACK << FG_GREY << BOLD << "HELLO" << NORMAL )
#
# print( BG_BLACK + FG_RED_LIGHT + STRIKE_THROUGH + "HELLO" + NORMAL + "World" )
# print( BG_BLACK + FG_GREEN_LIGHT + STRIKE_THROUGH + REVERSED + "HELLO" + NORMAL )
# print( BG_BLACK << FG_YELLOW_LIGHT << UNDERLINE_THICK << "HELLO" << NORMAL )
# print( BG_BLACK << FG_BLUE_LIGHT << UNDERLINE << "HELLO" << NORMAL )
# print( BG_BLACK << FG_PURPLE_LIGHT << ITALIC << "HELLO" << NORMAL )
# print( BG_BLACK << FG_CYAN_LIGHT << BOLD << "HELLO" << NORMAL )
# print( BG_BLACK << FG_WHITE_LIGHT << BOLD << "HELLO" << NORMAL )
#
#   c++ style output
#
# cout << BG_BLACK + FG_RED_LIGHT + STRIKE_THROUGH + "HELLO" + NORMAL + "World" << endl
# cout << BG_BLACK + FG_GREEN_LIGHT + STRIKE_THROUGH + REVERSED + "HELLO" + NORMAL << endl
# cout << BG_BLACK << FG_YELLOW_LIGHT << UNDERLINE_THICK << "HELLO" << NORMAL << endl
# cout << BG_BLACK << FG_BLUE_LIGHT << UNDERLINE << "HELLO" << NORMAL << endl
# cout << BG_BLACK << FG_PURPLE_LIGHT << ITALIC << "HELLO" << NORMAL << endl
# cout << BG_BLACK << FG_CYAN_LIGHT << BOLD << "HELLO" << NORMAL << endl
# cout << BG_BLACK << FG_WHITE_LIGHT << BOLD << "HELLO" << NORMAL << endl
