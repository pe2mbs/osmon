import json
import yaml
from osmon.common.interfaces import IConfiguration


class CConfiguration( object ):
    def __init__( self, filename ):
        self.__filename = filename
        self.__config = None
        return

    def load( self ):
        with open( self.__filename, 'r' ) as stream:
            if self.__filename.endswith( ('.yaml', '.yml', '.conf' ) ):
                self.__config = IConfiguration( **yaml.load( stream, Loader = yaml.Loader ) )

            else:
                self.__config = IConfiguration( **json.load( stream ) )

        return

    @property
    def Config( self ) -> IConfiguration:
        return self.__config
