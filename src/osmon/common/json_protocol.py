import typing as t
import struct
from pydantic import BaseModel
import json


class JsonProtocol( object ):
    def __init__( self, size: int = 2 ):
        if size <= 2:
            self._format = ">H"
            self.__size = 2

        elif size <= 4:
            self._format = ">I"
            self.__size = 4

        else:
            self._format = ">Q"
            self.__size = 8

        return

    def serialize( self, writer: t.Callable, data: t.Union[ str, bytes, dict, BaseModel ], encoding: str = 'u8' ) -> int:
        if isinstance( data, BaseModel ):
            data = data.model_dump_json( exclude_none = True )

        if isinstance( data, dict ):
            data = json.dumps( data )

        if isinstance( data, str ):
            data = bytes( data, encoding )

        length = len( data )
        return writer( struct.pack( self._format, length) + data )

    def deserialize( self, reader: t.Callable, return_type, encoding: str = 'u8' ) -> t.Union[ str, bytes, dict, BaseModel ]:
        data = reader( self.__size )
        length = struct.unpack( self._format, data )[ 0 ]
        data = reader( length )  # clip input at 1Kb
        if return_type is bytes:
            return data

        data = data.decode( encoding )
        if return_type is dict:
            return json.loads( data )

        if issubclass( return_type, BaseModel ):
            data = return_type.model_validate_json( data )

        return data
