from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from semver.version import Version
from pydantic import field_serializer, field_validator
from pydantic_xml import BaseXmlModel, attr, element, wrapped
from pathlib import Path
from saltysplits import DATETIME_FORMAT
from PIL import Image
from io import BytesIO
from pydantic import ConfigDict
import pybase64

# TODO LSS format can vary per release,  and add conditional models for {1.0, 1.4, 1.5, 1.6}. Models are currently based on version XX
# TODO add livesplit-core test runs (either directly or as submodule/sparse-checkout:)
# TODO base all optionals and default values on livesplit-core's run_files in /tests
# TODO use more appropriate types where possible (e.g. pathlib for layoutpath,
#  pillow.Image for game_icon, semver.Version for version, datetime for dts, 
# bools for bools). Also implement decoding/encoding for these elements.
# TODO figure out how to compare Splits objects
# TODO go through all example files, see if optional and types all work. Make tests for this



class Splits(BaseXmlModel, tag="Run"):
    version: Optional[str] = attr(name='version', default=None)
    game_icon: Optional[str] = element(tag="GameIcon", default=None)
    game_name: str = element(tag="GameName")
    category_name: str = element(tag="CategoryName")
    layout_path: Optional[str] = element(tag="LayoutPath", default=None)
    metadata: Optional[Metadata] = element(tag="Metadata", default=None)
    offset: Optional[str] = element(tag="Offset", default="00:00:00")
    attempt_count: Optional[int] = element(tag="AttemptCount", default=0)
    attempt_history: List[Attempt] = wrapped("AttemptHistory")
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
    uses_emulator: str = attr(name="usesEmulator", default=None)
    platform: str = None

class Variable(BaseXmlModel, tag="Variable"):
    name: str = attr(name='name', default=None)
    variable: str = None

class Attempt(BaseXmlModel, tag="Attempt"):
    id: str = attr(name='id')
    started: str = attr(name='started')
    is_started_synced: str = attr(name='isStartedSynced')
    ended: str = attr(name='ended')
    is_ended_synced: str = attr(name='isEndedSynced')
    real_time: Optional[str] = element(tag="RealTime", default=None)
    game_time: Optional[str] = element(tag="GameTime", default=None)
    # TODO omit empty times when dumped

    # # how to deal with Optional times
    # @field_serializer('started', 'ended')
    # def encode_content(self, dt_obj: datetime) -> str:
    #     return dt_obj.strftime(DATETIME_FORMAT)

    # @field_validator('started', 'ended', mode='before')
    # def decode_content(cls, value: str) -> datetime:
    #     return datetime.strptime(value, DATETIME_FORMAT)
    
class Segment(BaseXmlModel, tag="Segment"):
    name: str = element(tag="Name")
    icon: Optional[str] = element(tag="Icon", default=None)
    split_times: List[SplitTime] = wrapped("SplitTimes")
    best_segment_time: BestSegmentTime
    segment_history: List[Time] = wrapped("SegmentHistory")

class SplitTime(BaseXmlModel, tag="SplitTime"):
    name: str = attr(name='name')
    real_time: str = element(tag="RealTime")
    game_time: str = element(tag="GameTime")

class BestSegmentTime(BaseXmlModel, tag="BestSegmentTime"):
    real_time: str = element(tag="RealTime")
    game_time: str = element(tag="GameTime")

class Time(BaseXmlModel, tag="Time"):
    id: str = attr(name='id')
    real_time: Optional[str] = element(tag="RealTime", default=None) # sometimes only game_time
    game_time: Optional[str] = element(tag="GameTime", default=None) # sometimes only real_time
    
class AutoSplitterSettings(BaseXmlModel, tag="AutoSplitterSettings"):
    version: Optional[str] = element(tag='version', default=None) #does not follow semver format
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

    splits = Splits.from_xml(xml_string)
    print(splits.attempt_count)