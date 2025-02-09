import re
from datetime import datetime
from typing import Optional, Annotated
from pydantic import BeforeValidator, PlainSerializer
from pandas import Timedelta
from saltysplits import DATETIME_FORMAT


def decode_offset(value: str) -> Timedelta:
    hours, minutes, seconds = map(int, value.split(":"))
    return Timedelta(hours=hours, minutes=minutes, seconds=seconds)


def encode_offset(content: Timedelta) -> str:
    hours, remainder = divmod(content.value, 3600 * 10**9)
    minutes, remainder = divmod(remainder, 60 * 10**9)
    seconds = remainder // 10**9
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def decode_time(value: str) -> Timedelta:
    hours, minutes, seconds, fraction = map(int, re.split("[:.]", value))
    nanoseconds = fraction * 100
    return Timedelta(
        hours=hours, minutes=minutes, seconds=seconds, nanoseconds=nanoseconds
    )


def encode_time(content: Timedelta) -> str:
    hours, remainder = divmod(content.value, 3600 * 10**9)
    minutes, remainder = divmod(remainder, 60 * 10**9)
    seconds, remainder = divmod(remainder, 10**9)
    nanoseconds = remainder // 100
    return f"{hours:02}:{minutes:02}:{seconds:02}.{nanoseconds}"


def decode_datetime(value: str) -> datetime:
    return datetime.strptime(value, DATETIME_FORMAT)



def encode_datetime(content: datetime) -> str:
    return content.strftime(DATETIME_FORMAT)


OffsetOptional = Annotated[
    Optional[Timedelta],
    PlainSerializer(encode_offset, when_used="unless-none"),
    BeforeValidator(decode_offset),
]


TimeOptional = Annotated[
    Optional[Timedelta],
    PlainSerializer(encode_time, when_used="unless-none"),
    BeforeValidator(decode_time),
]


DateTime = Annotated[
    datetime,
    PlainSerializer(encode_datetime, when_used="unless-none"),
    BeforeValidator(decode_datetime),
]


    
