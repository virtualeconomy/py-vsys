"""
dbput_data_type contains data types for DB Put transactions.
"""
from __future__ import annotations
import abc
import struct
from typing import Type

from py_v_sdk import model as md


class DBPutKey:
    """
    DBPutKey is the key for the data stored by the DB Put transaction.
    """

    def __init__(self, data: md.Str) -> None:
        self.data = data

    @classmethod
    def from_str(cls, s: str) -> DBPutKey:
        """
        from_str creates a DBPutKey from a string.

        Args:
            s (str): The db put key in string format.

        Returns:
            DBPutKey: The DBPutKey object.
        """
        return cls(md.Str(s))

    @property
    def bytes(self) -> bytes:
        """
        bytes returns the bytes representation of the containing data
        It converts the data to bytes only.

        Returns:
            bytes: The bytes representation of the containing data
        """
        return self.data.bytes

    def serialize(self) -> bytes:
        """
        serialize serializes the containing data to bytes

        Returns:
            bytes: The serialization result
        """
        return struct.pack(">H", len(self.data.data)) + self.bytes


class DBPutData(abc.ABC):
    """
    DBPutData is the data for DB put.
    """

    ID = 0

    def __init__(self, data: md.Str) -> None:
        self.data = data

    @classmethod
    def new(cls, data: str, data_type: Type[DBPutData]) -> DBPutData:
        """
        new creates a new DBPutData for the given data & data type

        Args:
            data (str): The data
            data_type (Type[DBPutData]): The data type

        Returns:
            DBPutData: The DBPutData object.
        """
        return data_type(md.Str(data))

    @property
    def id_bytes(self) -> bytes:
        """
        id_bytes returns the id in bytes.

        Returns:
            bytes: The id in bytes.
        """
        return struct.pack(">B", self.ID)

    @property
    def bytes(self) -> bytes:
        """
        bytes returns the bytes representation of the containing data
        It converts the data to bytes only.

        Returns:
            bytes: The bytes representation of the containing data
        """
        return self.data.bytes

    def serialize(self) -> bytes:
        """
        serialize serializes the containing data to bytes

        Returns:
            bytes: The serialization result
        """
        return struct.pack(">H", len(self.data.data) + 1) + self.id_bytes + self.bytes


class ByteArray(DBPutData):
    """
    ByteArray is the DB Put data type for byte array.
    """

    ID = 1
