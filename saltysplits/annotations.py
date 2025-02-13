import re
from datetime import datetime
from typing import Optional, Annotated, List
from pydantic import BeforeValidator, PlainSerializer
from pandas import Timedelta
from saltysplits import DATETIME_FORMAT, NANOSECONDS_DAY, NANOSECONDS_HOUR, NANOSECONDS_MINUTE, NANOSECONDS_SECOND


def decode_time(value: str) -> Timedelta:
    pattern = re.compile(
        r"^(?:(?P<days>\d+)\.)?(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d+)(?:\.(?P<fraction>\d+))?$"
    )
    match = pattern.match(value)
    assert match, (
        "Invalid time format, expected 'HH:MM:SS' (with optional days prefix and fraction suffix)"
    )

    groups = match.group("days", "hours", "minutes", "seconds", "fraction")
    days, hours, minutes, seconds, fraction = map(lambda x: int(x) if x else 0, groups)
    nanoseconds = fraction * 100
    return Timedelta(
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        nanoseconds=nanoseconds,
    )


def parse_timedelta(timedelta: Timedelta) -> List[int]:
    days, remainder = divmod(timedelta.value, NANOSECONDS_DAY)
    hours, remainder = divmod(remainder, NANOSECONDS_HOUR)
    minutes, remainder = divmod(remainder, NANOSECONDS_MINUTE)
    seconds, remainder = divmod(remainder, NANOSECONDS_SECOND)
    nanoseconds = remainder // 100
    return days, hours, minutes, seconds, nanoseconds


def encode_time(content: Timedelta) -> str:
    # always adds n_nanoseconds suffix but only adds n_days prefix if not 0
    days, hours, minutes, seconds, nanoseconds = parse_timedelta(timedelta=content)
    delta_string = f"{hours:02}:{minutes:02}:{seconds:02}.{nanoseconds:07}"
    delta_string = f"{days}.{delta_string}" if days else delta_string
    return delta_string


def encode_offset(content: Timedelta) -> str:
    # only adds n_nanoseconds suffix and n_days prefix if not 0
    days, hours, minutes, seconds, nanoseconds = parse_timedelta(timedelta=content)
    delta_string = f"{hours:02}:{minutes:02}:{seconds:02}"
    delta_string = f"{delta_string}.{nanoseconds:07}" if nanoseconds else delta_string
    delta_string = f"{days}.{delta_string}" if days else delta_string
    return delta_string


def decode_datetime(value: str) -> datetime:
    return datetime.strptime(value, DATETIME_FORMAT)


def encode_datetime(content: datetime) -> str:
    return content.strftime(DATETIME_FORMAT)


TimeOptional = Annotated[
    Optional[Timedelta],
    PlainSerializer(encode_time, when_used="unless-none"),
    BeforeValidator(decode_time),
]

OffsetOptional = Annotated[
    Optional[Timedelta],
    PlainSerializer(encode_offset, when_used="unless-none"),
    BeforeValidator(decode_time),
]

DateTime = Annotated[
    datetime,
    PlainSerializer(encode_datetime, when_used="unless-none"),
    BeforeValidator(decode_datetime),
]


SBool = Annotated[
    bool,
    PlainSerializer(lambda x: str(x), when_used="unless-none"),
]
