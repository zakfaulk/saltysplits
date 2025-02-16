from __future__ import annotations
from typing import List, Optional
from pydantic_xml import BaseXmlModel, attr, element, wrapped
from pathlib import Path
from saltysplits.annotations import TimeOptional, DateTime, SBool, OffsetOptional
from pandas import Timedelta
from pydantic import conint


class Splits(
    BaseXmlModel, tag="Run", arbitrary_types_allowed=True, search_mode="ordered"
):
    version: Optional[str] = attr(name="version", default=None)
    game_icon: Optional[str] = element(tag="GameIcon", default=None)
    game_name: str = element(tag="GameName")
    category_name: str = element(tag="CategoryName")
    layout_path: Optional[str] = element(tag="LayoutPath", default=None)
    offset: OffsetOptional = element(tag="Offset", default=Timedelta(0))
    attempt_count: Optional[conint(ge=0)] = element(tag="AttemptCount", default=0)
    attempt_history: Optional[List[Attempt]] = wrapped("AttemptHistory", default=None)
    segments: List[Segment] = wrapped("Segments")

    @classmethod
    def from_lss_file(cls, lss_path: Path) -> Splits:
        with open(lss_path, "rb") as file:
            xml_bytes = file.read()
        return cls.from_xml(xml_bytes)


class BaseTime(BaseXmlModel, arbitrary_types_allowed=True, search_mode="ordered"):
    real_time: TimeOptional = element(tag="RealTime", default=None)
    game_time: TimeOptional = element(tag="GameTime", default=None)


class Attempt(BaseTime, tag="Attempt"):
    id: str = attr(name="id")
    started: DateTime = attr(name="started")
    is_started_synced: SBool = attr(name="isStartedSynced")
    ended: DateTime = attr(name="ended")
    is_ended_synced: SBool = attr(name="isEndedSynced")


class Segment(BaseXmlModel, tag="Segment", search_mode="ordered"):
    name: str = element(tag="Name")
    icon: Optional[str] = element(tag="Icon", default=None)
    split_times: List[SplitTime] = wrapped("SplitTimes")
    best_segment_time: BaseTime = element(tag="BestSegmentTime")
    segment_history: Optional[List[Time]] = wrapped("SegmentHistory", default=None)


class SplitTime(BaseTime, tag="SplitTime"):
    name: str = attr(name="name")


class Time(BaseTime, tag="Time"):
    id: str = attr(name="id")


# ensures all model elements are defined when we need them (without relying on arbritrary definition order)
Splits.model_rebuild()
Segment.model_rebuild()
