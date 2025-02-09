from __future__ import annotations
from typing import List, Optional
from semver.version import Version
from pydantic import field_serializer, field_validator, BeforeValidator, PlainSerializer, BaseModel, SerializerFunctionWrapHandler
from pydantic_xml import BaseXmlModel, attr, element, wrapped
from pathlib import Path
from saltysplits.annotations import OffsetOptional, TimeOptional, DateTime, SBool
from PIL import Image
from io import BytesIO
from pydantic import ConfigDict
import pybase64
from pandas import Timedelta

# TODO LSS format can vary per release,  and add conditional models for {1.0, 1.4, 1.5, 1.6}. Models are currently based on version XX
# TODO base all optionals and default values on livesplit-core's run_files in /tests
# TODO use more appropriate types where possible (e.g. pathlib for layoutpath,
#  pillow.Image for game_icon, semver.Version for version, datetime for dts, 
# bools for bools). Also implement decoding/encoding for these elements.
# TODO figure out how to compare Splits objects
# TODO go through all example files, see if optional and types all work. Make tests for this
# TODO move model_config and generic functionality to custom BaseXmlModel
# TODO add day prefix to GameTime/RealTime encoder like livesplit-core



class Splits(BaseXmlModel, tag="Run"):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    version: Optional[str] = attr(name='version', default=None)
    game_icon: Optional[str] = element(tag="GameIcon", default=None)
    game_name: str = element(tag="GameName")
    category_name: str = element(tag="CategoryName")
    layout_path: Optional[str] = element(tag="LayoutPath", default=None)
    metadata: Optional[Metadata] = element(tag="Metadata", default=None)
    offset: OffsetOptional = element(tag="Offset", default=Timedelta(0))
    attempt_count: Optional[int] = element(tag="AttemptCount", default=0)
    attempt_history: Optional[List[Attempt]] = wrapped("AttemptHistory", default=None)
    segments: List[Segment] = wrapped("Segments")
    autosplittersettings: Optional[AutoSplitterSettings] = element(tag="AutoSplitterSettings", default=None)

    @classmethod
    def from_lss_file(cls, lss_path: Path) -> Splits:
        with open(lss_path, "r", encoding="utf-8") as file:
            xml_string = file.read()
        return cls.from_xml(xml_string)
        
    # @field_validator('game_icon', mode='before')
    # def decode_content(cls, value: str) -> Image.Image:
    #     icon_bytes = pybase64.b64decode(value, validate=True)
    #     png_index = icon_bytes.index(b'\x89PNG\r\n\x1a\n')
    #     img = Image.open(BytesIO(icon_bytes[png_index:]))
    #     return img

class Metadata(BaseXmlModel, tag="Metadata"):
    run: Optional[Run] = element(tag="Run", default=None)
    platform: Optional[Platform] = element(tag="Platform", default=None)
    region: Optional[str] = element(tag="Region", default=None)
    variables: Optional[List[Variable]] = wrapped("Variables", default=None)

class Run(BaseXmlModel, tag="Run"):
    id: str = attr(name='id')

class Platform(BaseXmlModel, tag="Platform"):
    uses_emulator: bool = attr(name="usesEmulator", default=None)
    platform: str = None

class Variable(BaseXmlModel, tag="Variable"):
    name: str = attr(name='name', default=None)
    variable: str = None

class Attempt(BaseXmlModel, tag="Attempt"):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: str = attr(name='id')
    started: DateTime = attr(name='started')
    is_started_synced: SBool = attr(name='isStartedSynced')
    ended: DateTime = attr(name='ended')
    is_ended_synced: SBool = attr(name='isEndedSynced')
    real_time: TimeOptional = element(tag="RealTime", default=None)
    game_time: TimeOptional = element(tag="GameTime", default=None)
    
class Segment(BaseXmlModel, tag="Segment"):
    name: str = element(tag="Name")
    icon: Optional[str] = element(tag="Icon", default=None)
    split_times: List[SplitTime] = wrapped("SplitTimes")
    best_segment_time: BestSegmentTime
    segment_history: Optional[List[Time]] = wrapped("SegmentHistory", default=None)
    
class SplitTime(BaseXmlModel, tag="SplitTime"):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str = attr(name='name')
    real_time: TimeOptional = element(tag="RealTime", default=None)
    game_time: TimeOptional = element(tag="GameTime", default=None)

class BestSegmentTime(BaseXmlModel, tag="BestSegmentTime"):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    real_time: TimeOptional = element(tag="RealTime", default=None)
    game_time: TimeOptional = element(tag="GameTime", default=None)

class Time(BaseXmlModel, tag="Time"):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: str = attr(name='id')
    real_time: TimeOptional = element(tag="RealTime", default=None)
    game_time: TimeOptional = element(tag="GameTime", default=None)
    
class AutoSplitterSettings(BaseXmlModel, tag="AutoSplitterSettings"):
    version: Optional[str] = element(tag='version', default=None)
    custom_settings: Optional[str] = element(tag="CustomSettings", default=None)
    
# ensures all model elements are defined when we need them (without relying on arbritrary definition order)
Splits.model_rebuild()
Segment.model_rebuild()
Metadata.model_rebuild()

if __name__ == "__main__":
    split_path = Path(__file__).parents[1] / "tests/run_files/livesplit1.0.lss"  
    split_path = Path(__file__).parents[1] / "tests/run_files/Tony Hawk's Underground - Any% (Beginner).lss"

    #Splits.from_lss(split_path)
    with open(split_path, "r", encoding="utf-8") as file:
        xml_string = file.read()

    # what makes it a valid LSS file 
    # presence of certain elements?
    # if RunHistory instead of AttemptHistory, too old

    splits = Splits.from_xml(xml_string)
    print(splits.attempt_count)