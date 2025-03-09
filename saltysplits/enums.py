from enum import Enum

class TimeType(Enum):
    REAL_TIME = 0
    GAME_TIME = 1

class TimeUnit(Enum):
    NANOSECONDS_DAY = 86400 * 10**9
    NANOSECONDS_HOUR = 3600 * 10**9
    NANOSECONDS_MINUTE = 60 * 10**9
    NANOSECONDS_SECOND = 10**9